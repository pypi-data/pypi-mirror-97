# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import logging
from typing import Mapping, Optional

from pants.option.option_value_container import OptionValueContainer

from toolchain.pants.auth.client import AuthClient, AuthError, AuthState, AuthToken

_logger = logging.getLogger(__name__)


class AuthStore:
    def __init__(
        self, options: OptionValueContainer, pants_bin_name: str, env: Mapping[str, str], repo: Optional[str]
    ) -> None:
        repo_slug = f"{options.org}/{repo}" if options.org and repo else None
        self._access_token: Optional[AuthToken] = None
        self._state = AuthState.UNKNOWN
        self._env = env
        self._client = AuthClient.create(
            pants_bin_name=pants_bin_name,
            base_url=options.base_url,
            auth_file=options.auth_file,
            env_var=options.from_env_var,
            ci_env_vars=tuple(options.ci_env_variables),
            repo_slug=repo_slug,
        )

    def _get_access_token(self) -> Optional[AuthToken]:
        access_token = self._access_token
        if access_token and not access_token.has_expired():
            return access_token
        try:
            self._access_token = self._client.acquire_access_token(self._env)
        except AuthError as error:
            _logger.warning(f"Error loading access token: {error!r}")
            self._state = error.get_state()
        else:
            self._state = AuthState.OK
        return self._access_token

    def get_access_token(self) -> AuthToken:
        return self._get_access_token() or AuthToken.no_token()

    def get_auth_state(self) -> AuthState:
        if self._state.is_final:
            return self._state
        self._get_access_token()
        return self._state
