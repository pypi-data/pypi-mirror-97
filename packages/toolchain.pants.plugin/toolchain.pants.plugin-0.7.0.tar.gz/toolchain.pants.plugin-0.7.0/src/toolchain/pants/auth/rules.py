# Copyright © 2019 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

import os
import uuid
import webbrowser
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlencode

import requests
from pants.core.util_rules.pants_environment import PantsEnvironment
from pants.engine.console import Console
from pants.engine.fs import CreateDigest, Digest, FileContent, Workspace
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule, rule
from pants.option.global_options import GlobalOptions
from pants.option.subsystem import Subsystem

from toolchain.pants.auth.client import ACQUIRE_TOKEN_GOAL_NAME, AuthClient, AuthError, AuthToken
from toolchain.pants.auth.server import AuthFlowHttpServer
from toolchain.pants.auth.store import AuthStore
from toolchain.pants.common.network import get_common_request_headers
from toolchain.pants.common.toolchain_setup import ToolchainSetup


def optional_file_option(fn: str) -> str:
    # Similar to Pant's file_option, but doesn't require the file to exist.
    return os.path.normpath(fn)


@unique
class OutputType(Enum):
    FILE = "file"
    CONSOLE = "console"


class AccessTokenAcquisitionGoalOptions(GoalSubsystem):
    name = ACQUIRE_TOKEN_GOAL_NAME
    help = "Acquires access tokens for Toolchain service."

    @classmethod
    def register_options(cls, register):
        super().register_options(register)
        register("--local-port", type=int, default=None, help="Local web server port")
        register(
            "--output",
            type=OutputType,
            default=OutputType.FILE,
            help="Output method for access token. Outputing the console is useful if the token needs to be provided to CI",
        )
        register("--headless", type=bool, default=False, help="Don't open & use a browser to acquire access token")


class AuthStoreOptions(Subsystem):
    options_scope = "auth"
    help = "Setup for authentication with Toolchain."

    @classmethod
    def register_options(cls, register):
        register(
            "--auth-file",
            type=optional_file_option,
            help="Relative path (relative to the build root) for where to store and read the auth token",
        )
        register("--from-env-var", type=str, default=None, help="Loads the access token from an environment variable")
        register("--base-url", type=str, help="auth app base url", default="https://app.toolchain.com/api/v1")
        register(
            "--ci-env-variables",
            type=list,
            help="Environment variables in CI used to identify build (for restricted tokens)",
        )
        register("--org", type=str, default=None, help="organization slug for public repo PRs")


class AccessTokenAcquisition(Goal):
    subsystem_cls = AccessTokenAcquisitionGoalOptions


@dataclass(frozen=True)
class AccessTokenAcquisitionOptions:
    output: OutputType
    auth_options: AuthClient
    repo_name: str
    local_port: Optional[int]
    headless: bool

    @classmethod
    def from_options(
        cls,
        *,
        acquire_options: AccessTokenAcquisitionGoalOptions,
        store_options: AuthStoreOptions,
        pants_bin_name: str,
        repo_name: str,
    ) -> AccessTokenAcquisitionOptions:
        acquire_values = acquire_options.options
        store_values = store_options.options
        auth_opts = AuthClient.create(
            pants_bin_name=pants_bin_name,
            base_url=store_values.base_url,
            auth_file=store_values.auth_file,
        )
        return cls(
            local_port=acquire_values.local_port,
            repo_name=repo_name,
            auth_options=auth_opts,
            output=acquire_values.output,
            headless=acquire_values.headless,
        )

    @property
    def log_only(self) -> bool:
        return self.output == OutputType.CONSOLE

    @property
    def ask_for_impersonation(self) -> bool:
        # For now, the console output is used when creating tokens for CI, so in that case we will also request for impersonation permissions
        # We might want to have a standalone options for that in the future, however, currently CI is the only use case for an impersonation token
        return self.log_only

    @property
    def base_url(self) -> str:
        return self.auth_options.base_url

    def get_auth_url(self, repo: str, params: Dict[str, str]) -> str:
        params["repo"] = repo
        encoded_params = urlencode(params)
        return f"{self.base_url}/token/auth/?{encoded_params}"

    def get_token_exchange_url(self) -> str:
        return f"{self.base_url}/token/exchange/"

    @property
    def auth_file_path(self) -> Path:
        return self.auth_options.auth_file_path


@rule
def construct_auth_store(
    auth_store_config: AuthStoreOptions,
    global_options: GlobalOptions,
    toolchain_setup: ToolchainSetup,
    pants_environment: PantsEnvironment,
) -> AuthStore:
    return AuthStore(
        options=auth_store_config.options,
        pants_bin_name=global_options.options.pants_bin_name,
        env=dict(pants_environment.env),
        repo=toolchain_setup.safe_get_repo_name(),
    )


@goal_rule(desc="Acquires access token from Toolchain Web App and store it locally")
async def acquire_access_token(
    console: Console,
    workspace: Workspace,
    acquire_goal_options: AccessTokenAcquisitionGoalOptions,
    store_options: AuthStoreOptions,
    global_options: GlobalOptions,
    toolchain_setup: ToolchainSetup,
) -> AccessTokenAcquisition:
    repo_name = toolchain_setup.get_repo_name()
    acquire_options = AccessTokenAcquisitionOptions.from_options(
        pants_bin_name=global_options.options.pants_bin_name,
        acquire_options=acquire_goal_options,
        store_options=store_options,
        repo_name=repo_name,
    )
    try:
        auth_token = _acquire_token(console, acquire_options)
    except AuthError as error:
        console.print_stderr(str(error))
        return AccessTokenAcquisition(exit_code=-1)
    if acquire_options.log_only:
        console.print_stdout(f"Access Token is:{auth_token.access_token}")
        return AccessTokenAcquisition(exit_code=0)
    # stores token locally
    auth_file_path = acquire_options.auth_file_path
    digest = await Get(
        Digest, CreateDigest([FileContent(path=auth_file_path.name, content=auth_token.to_json_string().encode())])
    )
    workspace.write_digest(digest=digest, path_prefix=str(auth_file_path.parent))
    console.print_stdout("Access token acquired and stored.")
    return AccessTokenAcquisition(exit_code=0)


def _acquire_token(console: Console, options: AccessTokenAcquisitionOptions) -> AuthToken:
    if options.headless or not _is_browser_available():
        return _acquire_token_headless(console, options)
    return _acquire_token_with_browser(console, options)


def _acquire_token_with_browser(console: Console, options: AccessTokenAcquisitionOptions) -> AuthToken:
    state = str(uuid.uuid4())
    with AuthFlowHttpServer.create_server(port=options.local_port, expected_state=state) as http_server:
        http_server.start_thread()
        callback_url = http_server.server_url
        console.print_stdout(f"Local Web Server running - callback at: {callback_url}")
        params = {"redirect_uri": callback_url, "state": state}
        success = webbrowser.open(options.get_auth_url(options.repo_name, params), new=1, autoraise=True)
        if not success:
            http_server.shutdown()
            raise AuthError(f"Failed to open web browser. {ACQUIRE_TOKEN_GOAL_NAME} can't continue.")
        token_code = http_server.wait_for_code()
        return _exchage_code_for_token(console, options, token_code)


def _exchage_code_for_token(console: Console, options: AccessTokenAcquisitionOptions, token_code: str) -> AuthToken:
    # TODO: Use an engine intrinsic instead of directly going to the network.
    headers = get_common_request_headers()
    data = {"code": token_code}
    if options.ask_for_impersonation:
        data["allow_impersonation"] = "1"
    with requests.post(options.get_token_exchange_url(), data=data, headers=headers) as response:
        if not response.ok:
            console.print_stderr(console.red(_get_error_message(response)))
            raise AuthError("Failed to acquire access token from server")
        resp_data = response.json()
        return AuthToken.from_json_dict(resp_data)


def _acquire_token_headless(console: Console, options: AccessTokenAcquisitionOptions) -> AuthToken:
    url = options.get_auth_url(options.repo_name, {"headless": "1"})
    console.print_stdout(f"Using a web browser navigate to: {url}")
    # TODO: use console to get input from the user. https://github.com/pantsbuild/pants/issues/11398
    token_code = input("Type or paste in the token exchange code: ")
    return _exchage_code_for_token(console, options, token_code)


def _is_browser_available() -> bool:
    try:
        webbrowser.get()
    except webbrowser.Error:
        return False
    return True


def _get_error_message(response) -> str:
    error_message = None
    request_id = response.headers.get("X-Request-ID", "NA")
    if response.headers.get("Content-Type") == "application/json":
        error_message = response.json().get("message")

    if not error_message:
        error_message = f"Unknown error: {response.text}"
    return f"HTTP: {response.status_code}: {error_message} request={request_id}"


def get_auth_rules():
    return collect_rules()
