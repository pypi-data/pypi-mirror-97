# Copyright © 2021 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

import logging
import os
from typing import Mapping, Optional

from pants.option.global_options import AuthPluginResult, AuthPluginState
from pants.option.options import Options

from toolchain.pants.auth.rules import AuthStoreOptions
from toolchain.pants.auth.store import AuthStore
from toolchain.pants.common.toolchain_setup import ToolchainSetup

_DISABLED_AUTH = AuthPluginResult(
    state=AuthPluginState.UNAVAILABLE, execution_headers={}, store_headers={}, instance_name=None
)

_logger = logging.getLogger(__name__)


def toolchain_auth_plugin(
    initial_execution_headers: dict[str, str],
    initial_store_headers: dict[str, str],
    options: Options,
    env: Optional[Mapping[str, str]] = None,
) -> AuthPluginResult:
    if initial_execution_headers or initial_store_headers:
        _logger.warning(
            f"Specified execution/store headers will be ignored when the Toolchain plugin is enabled. execution_headers={initial_execution_headers} store_headers={initial_store_headers}"
        )

    # TODO: Remove fallback to `os.environ` after https://github.com/pantsbuild/pants/pull/11641
    # is in wide use.
    env = env if env is not None else dict(os.environ)
    store = _auth_store_from_options(options, env)
    if not store:
        return _DISABLED_AUTH
    access_token = store.get_access_token()
    if not access_token.has_token:
        return _DISABLED_AUTH
    return AuthPluginResult(
        state=AuthPluginState.OK,
        execution_headers={},
        store_headers=access_token.get_headers(),
        instance_name=access_token.customer_id,
    )


def _auth_store_from_options(options: Options, env: Mapping[str, str]) -> AuthStore | None:
    pants_bin_name = options.for_global_scope().pants_bin_name
    auth_options = options.for_scope(AuthStoreOptions.options_scope)
    repo_slug = options.for_scope(ToolchainSetup.options_scope).repo
    if not repo_slug:
        return None
    return AuthStore(options=auth_options, pants_bin_name=pants_bin_name, env=env, repo=repo_slug)
