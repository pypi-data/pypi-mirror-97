# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import logging
import queue
import time
from enum import Enum, unique
from pathlib import Path
from typing import List, Optional, Tuple

from pants.util.logging import LogLevel

from toolchain.base.datetime_tools import utcnow
from toolchain.pants.buildsense.client import BuildSenseClient
from toolchain.pants.buildsense.common import Artifacts, RunTrackerBuildInfo, WorkUnitsMap
from toolchain.pants.buildsense.converter import WorkUnitCoverter
from toolchain.pants.buildsense.local_store import LocalBuildsStore

logger = logging.getLogger(__name__)
WorkUnitsChunk = Tuple[int, WorkUnitsMap, int]


class InvalidStateError(Exception):
    """Raised when there is an invalid state in the reporter logic."""


@unique
class ReportOperation(Enum):
    NO_OP = "no_op"
    SENT = "sent"
    ERROR = "error"

    def is_sent(self) -> bool:
        return self == self.SENT

    def is_error(self) -> bool:
        return self == self.ERROR


class BuildState:
    _PANTS_LOG_ARTIFACT_NAME = "pants_run_log"

    def __init__(
        self,
        client: BuildSenseClient,
        local_store_base_path: Path,
        max_batch_size_mb: int,
        local_store_enabled: bool,
    ):
        self._enabled = True
        self._client = client
        self._initial_report: Optional[RunTrackerBuildInfo] = None
        self._end_report_data: Optional[Tuple[RunTrackerBuildInfo, int]] = None
        self._sent_initial_report = False
        self._run_id: Optional[str] = None
        self._ci_user_api_id: Optional[str] = None
        self._workunits_chunks_queue: queue.LifoQueue = queue.LifoQueue(maxsize=300)
        self._converter = WorkUnitCoverter.create()
        self._local_store = LocalBuildsStore(
            base_path=local_store_base_path, max_batch_size_mb=max_batch_size_mb, enabled=local_store_enabled
        )
        self._sumbit_batches = True

    def set_context(self, context) -> None:
        self._converter.set_context(context)

    def queue_workunits(self, call_num: int, workunits: WorkUnitsMap, timestamp: Optional[int] = None) -> None:
        timestamp = timestamp or int(utcnow().timestamp())
        run_id = self._run_id
        if not workunits:
            return
        if not run_id:
            raise InvalidStateError("run_id must be initialized.")
        self._workunits_chunks_queue.put_nowait((call_num, workunits, timestamp))

    def set_run_id(self, run_tracker_info: RunTrackerBuildInfo) -> None:
        self._run_id = run_tracker_info.run_id

    def queue_initial_report(self, run_tracker_info: RunTrackerBuildInfo) -> None:
        self.set_run_id(run_tracker_info)
        self._initial_report = run_tracker_info

    def build_ended(self, run_tracker_info: RunTrackerBuildInfo, call_count: int, work_units_map: WorkUnitsMap) -> None:
        self.set_run_id(run_tracker_info)
        self.queue_workunits(call_count, work_units_map)
        self.submit_final_report(run_tracker_info, call_count)

    def submit_final_report(self, run_tracker_info: RunTrackerBuildInfo, calls_count: int) -> None:
        if not run_tracker_info.has_ended:
            logger.warning("RunTracker.end() was not called")
            return
        self._run_id = self._run_id or run_tracker_info.run_id
        logger.debug(
            f"submit_final_report run_id={self._run_id} calls={calls_count} keys={run_tracker_info.build_stats.keys()}"
        )
        self._end_report_data = run_tracker_info, calls_count

    def send_report(self) -> ReportOperation:
        # Expects to be non-reentrant
        if not self._enabled:
            return ReportOperation.ERROR
        if not self._client.is_auth_available():
            logger.warning("Auth failed - BuildSense plugin is disabled.")
            self._enabled = False
            return ReportOperation.ERROR
        operation = self._maybe_send_initial_report()
        if operation.is_error():
            return operation
        sent = self._send_workunit_queue()
        if sent:
            return ReportOperation.SENT
        batch_sent = self._maybe_send_batched_build()
        return ReportOperation.SENT if batch_sent or operation.is_sent() else ReportOperation.NO_OP

    def _get_log_file(self, run_tracker_info: RunTrackerBuildInfo) -> Optional[bytes]:
        if not run_tracker_info.log_file:
            logger.debug("no log file associated in run tracker")
            return None
        build_stats = run_tracker_info.build_stats
        is_fail = build_stats["run_info"]["outcome"] != "SUCCESS"
        log_level = build_stats["recorded_options"]["GLOBAL"].get("level", "")
        if isinstance(log_level, LogLevel):
            log_level = log_level.value.lower()
        logger.debug(f"get_log_file log_level={log_level} is_fail={is_fail}")
        if not is_fail and log_level not in {"debug", "trace"}:
            return None
        return run_tracker_info.log_file.read_bytes()

    def _get_artifacts(self, run_tracker_info: RunTrackerBuildInfo) -> Artifacts:
        artifacts = self._converter.get_standalone_artifacts() or {}
        pants_run_log = self._get_log_file(run_tracker_info)
        if pants_run_log:
            artifacts[self._PANTS_LOG_ARTIFACT_NAME] = pants_run_log
        return artifacts

    def send_final_report(self) -> None:
        if self._end_report_data is None:
            raise InvalidStateError("End report data not captured.")
        run_tracker_info, calls_count = self._end_report_data
        build_stats = run_tracker_info.build_stats
        # Make sure we don't miss any work units we didn't de-queue yet
        call_num, workunits, timestamp = self._get_lastest_workunits()
        self._converter.transform(workunits, call_num, timestamp)
        all_workunits = self._converter.get_all_work_units(call_num=calls_count, last_update_timestamp=int(time.time()))
        build_stats["workunits"] = all_workunits
        run_id = self._run_id
        if not run_id:
            logger.warning("run_id is missing")
            return
        if not build_stats:
            logger.warning("final build report missing")
            return
        artifacts = self._get_artifacts(run_tracker_info)
        logger.debug(f"send_final_report workunits={len(all_workunits)} artifacts={len(artifacts)}")
        data = self._client.submit_run_end(run_id=run_id, user_api_id=self._ci_user_api_id, build_stats=build_stats)
        if data:
            # If submition failed, submit_run_end returns the data so we can store it for later upload
            self._local_store.store_build(run_id=run_id, json_build_data=data)
            return
        self._maybe_upload_artifacts(run_id, artifacts)

    def _maybe_upload_artifacts(self, run_id: str, artifacts: Artifacts) -> None:
        if not artifacts:
            return
        self._client.upload_artifacts(run_id=run_id, artifacts=artifacts, user_api_id=self._ci_user_api_id)
        # TODO: Store artifacts for later in self._local_store if upload fails.

    def _maybe_send_initial_report(self) -> ReportOperation:
        if self._sent_initial_report:
            return ReportOperation.NO_OP
        run_tracker_info = self._initial_report
        if self._sent_initial_report or not run_tracker_info:
            return ReportOperation.NO_OP
        success, self._ci_user_api_id = self._client.submit_run_start(
            run_id=run_tracker_info.run_id, build_stats=dict(run_tracker_info.build_stats)
        )
        if not success:
            return ReportOperation.ERROR
        self._sent_initial_report = True
        return ReportOperation.SENT

    def _send_workunit_queue(self) -> bool:
        call_num, workunits, timestamp = self._get_lastest_workunits()
        if not workunits:
            return False
        logger.debug(f"send_workunit_queue {len(workunits)} {call_num}")
        run_id = self._run_id
        if not run_id:
            raise InvalidStateError("run_id must be initialized.")
        buildsense_workunits = self._converter.transform(workunits, call_num, timestamp)
        if not buildsense_workunits:
            return False
        self._client.submit_workunits(
            run_id=run_id, call_num=call_num, user_api_id=self._ci_user_api_id, workunits=buildsense_workunits
        )
        return True

    def _maybe_send_batched_build(self) -> bool:
        if not self._client.has_successful_calls and self._sumbit_batches:
            return False
        batched_build = self._local_store.get_upload_batch()
        if not batched_build:
            return False
        success = self._client.submit_batch(
            batched_data=batched_build.get_batched_data(),
            batch_name=batched_build.name,
            user_api_id=self._ci_user_api_id,
        )
        if success:
            self._local_store.delete_batch_file(batched_build)
        else:
            # If we failed, don't try again during this run
            self._sumbit_batches = False
        return True

    def _empty_queue(self) -> List[WorkUnitsChunk]:
        data = []
        while self._workunits_chunks_queue.not_empty:
            try:
                data.append(self._workunits_chunks_queue.get_nowait())
            except queue.Empty:
                break
        return data

    def _get_lastest_workunits(self) -> WorkUnitsChunk:
        data = self._empty_queue()
        if not data:
            return -1, dict(), 0
        workunits_dict: WorkUnitsMap = {}
        # Ensures that we handle the latest chunks first (based on the call_num)
        # Protects against a race in which data is queued while we try to empty the queue.
        data = sorted(data, reverse=True, key=lambda x: x[0])
        for _, wu_chunk, _ in data:
            for wu_id, workunit in wu_chunk.items():
                workunits_dict.setdefault(wu_id, workunit)
        last_chunk = data[0]
        last_call_num = last_chunk[0]
        timestamp = last_chunk[2]
        return last_call_num, workunits_dict, timestamp
