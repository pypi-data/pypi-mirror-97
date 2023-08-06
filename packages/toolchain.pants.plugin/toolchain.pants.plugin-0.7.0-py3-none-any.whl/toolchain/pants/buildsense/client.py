# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

import json
import logging
import zlib
from typing import Dict, Optional, Tuple
from urllib.parse import urljoin

import requests
from pants.goal.run_tracker import RunTrackerOptionEncoder
from pants.option.option_value_container import OptionValueContainer
from requests.exceptions import RequestException

from toolchain.pants.auth.client import AuthToken
from toolchain.pants.auth.store import AuthStore
from toolchain.pants.buildsense.common import Artifacts, WorkUnits
from toolchain.pants.common.network import get_common_request_headers

_logger = logging.getLogger(__name__)


class BuildSenseClient:
    _IMPERSONATE_HEADER = "X-Toolchain-Impersonate"

    @classmethod
    def from_options(cls, client_options: OptionValueContainer, auth: AuthStore, repo: str) -> BuildSenseClient:
        return cls(
            base_url=client_options.base_url,
            auth=auth,
            repo=repo,
            timeout=client_options.timeout,
            dry_run=client_options.dry_run,
        )

    def __init__(
        self,
        *,
        base_url: str,
        repo: str,
        auth: AuthStore,
        timeout: int,
        dry_run: bool,
    ) -> None:
        self._base_url = base_url
        self._successful_calls = 0
        self._dry_run = dry_run
        self._timeout = timeout
        self._auth = auth
        self._repo = repo
        self._compression_threshold = 10 * 1024  # 10kb
        self._session = requests.Session()
        self._session.mount(self._base_url, requests.adapters.HTTPAdapter(max_retries=3))
        self._last_error: Optional[type] = None

    def _get_headers(self, user_api_id: Optional[str], token: AuthToken) -> Dict[str, str]:
        headers = get_common_request_headers()
        headers.update(token.get_headers())
        headers["X-Pants-Stats-Version"] = "3"
        if user_api_id:
            headers[self._IMPERSONATE_HEADER] = user_api_id
        return headers

    def is_auth_available(self) -> bool:
        return not self._auth.get_auth_state().no_auth_possible

    @property
    def has_successful_calls(self) -> bool:
        return self._successful_calls > 0

    def _call_success(self) -> None:
        self._successful_calls += 1
        self._last_error = None

    def _prepare_request(self, api_call_desc: str, data: str, as_file: bool) -> Tuple[dict, dict, int]:
        req_kwargs = {}
        headers = {}
        compression = len(data) > self._compression_threshold
        file_upload = compression and as_file
        uncompressed_size = len(data)
        if compression:
            headers["Content-Encoding"] = "compress"
            data = zlib.compress(data.encode())  # type: ignore
            if file_upload:
                req_kwargs = {"files": {"buildsense": data}}
        if not req_kwargs:
            headers["Content-Type"] = "application/json"
            req_kwargs = {"data": data}  # type: ignore[dict-item]
        if compression:
            compressed_size = len(data)
            rate = compressed_size / uncompressed_size
            compression_str = f" file={file_upload} compressed={compressed_size:,} rate={rate:.2%}"
        else:
            compression_str = ""
            compressed_size = len(data)

        _logger.debug(
            f"send_json_data {api_call_desc}. compression={compression} payload_size={uncompressed_size:,}{compression_str}"
        )
        return req_kwargs, headers, compressed_size

    def _send_json_data(
        self,
        *,
        api_call_desc: str,
        method: str,
        path: str,
        data: str,
        user_api_id: Optional[str],
        as_file: bool = False,
    ) -> Optional[dict]:
        url = urljoin(self._base_url, path)
        req_kwargs, headers, compressed_size = self._prepare_request(api_call_desc, data, as_file)
        token = self._auth.get_access_token()
        if not token.has_token:
            return None
        headers.update(self._get_headers(user_api_id, token))
        if self._dry_run:
            return None
        try:
            response = self._session.request(
                method=method, url=url, headers=headers, timeout=self._timeout, **req_kwargs  # type: ignore[arg-type]
            )
            response.raise_for_status()
        except RequestException as error:
            self._process_error(api_call_desc, compressed_size, error)
            return None
        # Only returning a response if we got a HTTP 20x
        self._call_success()
        return response.json()

    def _send_files_data(
        self,
        *,
        api_call_desc: str,
        path: str,
        files_data: Dict[str, bytes],
        compressed: bool,
        user_api_id: Optional[str],
    ) -> bool:
        token = self._auth.get_access_token()
        url = urljoin(self._base_url, path)
        if not token.has_token:
            return False
        headers = self._get_headers(user_api_id, token)
        if compressed:
            headers["Content-Encoding"] = "compress"
        if self._dry_run:
            return True
        try:
            response = self._session.post(url=url, headers=headers, timeout=self._timeout, files=files_data)
            response.raise_for_status()
        except RequestException as error:
            self._process_error(api_call_desc, sum(len(fl) for fl in files_data.values()), error)
            return False
        # Only returning a response if we got a HTTP 20x
        self._call_success()
        return True

    def _process_error(self, api_call_desc: str, payload_size: int, error: RequestException) -> None:
        # TODO: handle errors better.
        response = error.response
        if response is not None:  # bool(response) will return False for failed requests.
            request_id = response.headers.get("X-Request-ID", "N/A")
            error_message = f" request id: {request_id} error message: {error.response.text}"
        elif error.request:
            error_message = error.request.url
        else:
            error_message = ""
        level = logging.DEBUG if self._last_error == type(error) else logging.WARNING
        self._last_error = type(error)
        _logger.log(
            level=level,
            msg=f"Error reporting {api_call_desc}. payload_size={payload_size:,}: {error!r} {error_message}",
        )

    def submit_workunits(self, *, run_id: str, call_num: int, user_api_id: Optional[str], workunits: WorkUnits):
        wu_json = json.dumps({"workunits": workunits, "run_id": run_id})
        _logger.debug(f"workunits(call_num={call_num}, work_units={len(workunits)})")
        self._send_json_data(
            api_call_desc=f"workunits(call_num={call_num}, work_units={len(workunits)})",
            method="post",
            path=f"{self._repo}/buildsense/{run_id}/workunits/",
            data=wu_json,
            user_api_id=user_api_id,
        )

    def submit_run_start(self, *, run_id: str, build_stats: dict) -> Tuple[bool, Optional[str]]:
        data = json.dumps(build_stats, cls=RunTrackerOptionEncoder)
        json_response = self._send_json_data(
            api_call_desc="run_start",
            method="post",
            path=f"{self._repo}/buildsense/{run_id}/",
            data=data,
            user_api_id=None,
            as_file=True,
        )
        success = json_response is not None
        return success, json_response["ci_user_api_id"] if json_response else None

    def submit_run_end(self, *, run_id: str, user_api_id: Optional[str], build_stats: dict) -> Optional[str]:
        """Sends the final build report to the service.

        If it fails to upload, it returns the data so it can be queued for upload at a later time.
        """
        data = json.dumps(build_stats, cls=RunTrackerOptionEncoder)
        response = self._send_json_data(
            api_call_desc="run_end",
            method="patch",
            path=f"{self._repo}/buildsense/{run_id}/",
            data=data,
            user_api_id=user_api_id,
            as_file=True,
        )
        return None if response else data

    def submit_batch(self, *, batched_data: str, batch_name: str, user_api_id: Optional[str]) -> bool:
        response = self._send_json_data(
            api_call_desc=f"batch_upload={batch_name}",
            method="post",
            path=f"{self._repo}/buildsense/batch/",
            data=batched_data,
            user_api_id=user_api_id,
            as_file=True,
        )
        return bool(response)

    def upload_artifacts(self, *, run_id, artifacts: Artifacts, user_api_id: Optional[str]) -> bool:
        files_data = {name: zlib.compress(data) for name, data in artifacts.items()}
        return self._send_files_data(
            api_call_desc=f"upload_artifacts artifacts={len(artifacts)}",
            path=f"{self._repo}/buildsense/{run_id}/artifacts/",
            files_data=files_data,
            compressed=True,
            user_api_id=user_api_id,
        )
