# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

import base64
import datetime
import json
import logging
from dataclasses import asdict, dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Dict, Mapping, Optional, Tuple, cast

import requests
from dateutil.parser import parse

from toolchain.base.datetime_tools import utcnow
from toolchain.pants.common.network import get_common_request_headers

_logger = logging.getLogger(__name__)

ACQUIRE_TOKEN_GOAL_NAME = "auth-acquire"  # nosec


@unique
class AuthState(Enum):
    UNKNOWN = "unknown"
    OK = "ok"  # We are able to auth
    UNAVAILABLE = "unavailable"  # local state is preventing auth (no or expired token file/env variable)
    FAILED = "failed"  # auth failed on the server side, don't retry (HTTP 400/403).
    TRANSIENT_FAILURE = "transient_failure"  # Server encountered a transient error (HTTP 503), it is ok to retry.

    @property
    def is_ok(self) -> bool:
        return self == self.OK

    @property
    def is_final(self) -> bool:
        return self in {self.OK, self.FAILED, self.UNAVAILABLE}

    @property
    def no_auth_possible(self) -> bool:
        return self.is_final and not self.is_ok


class AuthError(Exception):
    def __init__(
        self, message: str, request_id: Optional[str] = None, should_retry: bool = False, server_failure=False
    ) -> None:
        if request_id:
            message = f"{message} request_id={request_id}"
        super().__init__(message)
        self._should_retry = should_retry
        self._server_failure = server_failure

    def get_state(self) -> AuthState:
        if self._should_retry:
            return AuthState.TRANSIENT_FAILURE
        if self._server_failure:
            return AuthState.FAILED
        return AuthState.UNAVAILABLE


@dataclass(frozen=True)
class AuthToken:
    access_token: str
    expires_at: datetime.datetime
    user: Optional[str] = None
    repo: Optional[str] = None
    repo_id: Optional[str] = None
    customer_id: Optional[str] = None

    @classmethod
    def no_token(cls) -> AuthToken:
        return cls(access_token="", expires_at=datetime.datetime(2020, 1, 1))  # nosec

    @classmethod
    def from_json_dict(cls, json_dict: dict):
        return cls(
            access_token=json_dict["access_token"],
            expires_at=parse(json_dict["expires_at"]),
            user=json_dict.get("user"),
            repo=json_dict.get("repo"),
            repo_id=json_dict.get("repo_id"),
            customer_id=json_dict.get("customer_id"),
        )

    @classmethod
    def from_access_token_string(cls, token_str: str) -> AuthToken:
        claims_json = base64.decodebytes(token_str.split(".")[1].encode())
        claims = json.loads(claims_json)
        expires_at = datetime.datetime.utcfromtimestamp(claims["exp"]).replace(tzinfo=datetime.timezone.utc)
        return cls(
            access_token=token_str, expires_at=expires_at, user=claims["toolchain_user"], repo=claims["toolchain_repo"]
        )

    def get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def has_expired(self) -> bool:
        expiration_time = cast(datetime.datetime, self.expires_at) - datetime.timedelta(
            seconds=10
        )  # Give some room for clock deviation and processing time.
        return utcnow() > expiration_time

    @property
    def has_token(self) -> bool:
        return bool(self.access_token)

    def to_json_string(self) -> str:
        token_dict = asdict(self)
        token_dict["expires_at"] = self.expires_at.isoformat()
        return json.dumps(token_dict)


@dataclass
class AuthClient:
    _DEFAULT_FILE = ".pants.d/toolchain_auth/auth_token.json"
    _DEFAULT_ENV_VAR = "TOOLCHAIN_AUTH_TOKEN"
    pants_bin_name: str
    base_url: str
    auth_file: str
    env_var: Optional[str]
    repo_slug: Optional[str]
    ci_env_variables: Tuple[str, ...]

    @classmethod
    def create(
        cls,
        *,
        pants_bin_name: str,
        base_url: str,
        auth_file: Optional[str],
        env_var: Optional[str] = None,
        repo_slug: Optional[str] = None,
        ci_env_vars: Tuple[str, ...] = tuple(),
    ):
        return cls(
            pants_bin_name=pants_bin_name,
            base_url=base_url,
            auth_file=auth_file or cls._DEFAULT_FILE,
            env_var=env_var,
            ci_env_variables=ci_env_vars,
            repo_slug=repo_slug,
        )

    @property
    def auth_file_path(self) -> Path:
        return Path(self.auth_file)

    def _check_refresh_token(self, refresh_token: Optional[AuthToken]) -> None:
        if not refresh_token:
            return
        call_to_action = f"Run `{self.pants_bin_name} {ACQUIRE_TOKEN_GOAL_NAME}` to acquire a new token."
        if refresh_token.has_expired():
            raise AuthError(f"Access token has expired - {call_to_action}")
        time_until_expiration = refresh_token.expires_at - utcnow()
        if time_until_expiration < datetime.timedelta(days=10):
            _logger.warning(f"Access token will expire in {time_until_expiration.days} days. - {call_to_action}")

    def acquire_access_token(self, complete_env: Mapping[str, str]) -> AuthToken:
        refresh_token = self._load_refresh_token(complete_env)
        self._check_refresh_token(refresh_token)
        headers = get_common_request_headers()
        with requests.Session() as session:
            session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
            if refresh_token:
                _logger.debug("Acquire access token")
                headers.update(refresh_token.get_headers())
                response = self._post(path="token/refresh/", headers=headers, timeout=4)
            else:
                env_vars = {key: complete_env[key] for key in self.ci_env_variables if key in complete_env}
                if not env_vars:
                    raise AuthError("Can't acquire restricted access token without environment variables.")
                json_data = {"repo_slug": self.repo_slug, "env": env_vars}
                _logger.debug(f"Acquire restricted access token: {json_data}")
                response = self._post(path="token/restricted/", headers=headers, timeout=8, json_data=json_data)
        self._process_response(response)
        return AuthToken.from_json_dict(response.json())

    def _post(self, path: str, headers: Dict[str, str], timeout: int, json_data: Optional[dict] = None):
        with requests.Session() as session:
            session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
            url = f"{self.base_url}/{path}"
            try:
                return session.post(url, headers=headers, timeout=timeout, json=json_data)
            except requests.RequestException as error:
                raise AuthError(str(error), should_retry=True)

    def _process_response(self, response) -> None:
        if response.ok:
            return
        request_id = response.headers.get("X-Request-ID")
        if response.status_code == 503:
            raise AuthError(
                "Auth failed, transient server error", request_id=request_id, should_retry=True, server_failure=True
            )
        is_json = response.headers.get("Content-Type") == "application/json"
        if not is_json:
            raise AuthError(
                "Auth failed, unknown error", request_id=request_id, should_retry=False, server_failure=True
            )
        resp_json = response.json()
        if response.status_code == 403 and resp_json.get("rejected") is True:
            raise AuthError("Auth rejected by server", request_id=request_id, server_failure=True)
        # TODO build a better string/error message
        errors = resp_json.get("errors") or "N/A"
        raise AuthError(f"API Errors: {errors}", request_id=request_id, server_failure=True)

    def _load_refresh_token(self, complete_env: Mapping[str, str]) -> Optional[AuthToken]:
        if self.env_var:
            token = _load_from_env(complete_env, self.env_var)
            if token:
                return token
            if not self.repo_slug or not self.ci_env_variables:
                raise AuthError(
                    f"Access token not set in environment variable: {self.env_var}. customer_slug & ci_env_vars must be defined in order to acquire restricted access token."
                )
            return token

        auth_file_path = self.auth_file_path
        if auth_file_path.exists():
            return _load_from_file(self.pants_bin_name, auth_file_path)

        token = _load_from_env(complete_env, AuthClient._DEFAULT_ENV_VAR)
        if token:
            return token
        raise AuthError(
            f"Failed to load auth token (no default file or environment variable). Run `{self.pants_bin_name} {ACQUIRE_TOKEN_GOAL_NAME}` to set up authentication."
        )


def _load_from_env(complete_env: Mapping[str, str], env_var_name: str) -> Optional[AuthToken]:
    token_str = complete_env.get(env_var_name)
    if not token_str:
        return None
    return AuthToken.from_access_token_string(token_str)


def _load_from_file(pants_bin_name: str, auth_file_path: Path) -> AuthToken:
    try:
        with open(auth_file_path, "r") as auth_file:
            token_json = json.loads(auth_file.read())
    except (FileNotFoundError, ValueError) as err:
        raise AuthError(
            f"Failed to load auth token: {err!r}. Run `{pants_bin_name} {ACQUIRE_TOKEN_GOAL_NAME}` to set up authentication."
        )
    # TODO: Handle TypeError (due to malformed json)
    return AuthToken.from_json_dict(token_json)
