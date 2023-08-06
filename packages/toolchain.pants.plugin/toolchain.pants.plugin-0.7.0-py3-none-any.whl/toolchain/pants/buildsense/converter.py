# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import json
import logging
import uuid
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Union

import chardet
from pants.engine.fs import Digest, DigestContents, FileDigest, Snapshot

from toolchain.pants.buildsense.common import Artifacts, WorkUnits, WorkUnitsMap

_NAMES = {"start": ("start_secs", "start_nanos"), "duration": ("duration_secs", "duration_nanos")}

_logger = logging.getLogger(__name__)


Artifact = Union[str, bytes, Dict[str, str]]
ArtifactsMap = Dict[str, Artifact]

_logger = logging.getLogger(__name__)


def _to_usecs(data, name) -> int:
    secs, nanos = _NAMES[name]
    return (data[secs] * 1_000_000) + round(data[nanos] / 1_000)


@dataclass(frozen=True)
class ArtifactRef:
    wu_id: str
    name: str
    digest: Optional[Digest] = None
    snapshot: Optional[Snapshot] = None

    @classmethod
    def create(cls, wu_id: str, name: str, artifact: Union[Digest, Snapshot]):
        if isinstance(artifact, Digest):
            digest = artifact
            snapshot = None
        else:
            digest = None
            snapshot = artifact
        return cls(
            wu_id=wu_id,
            name=name,
            digest=digest,
            snapshot=snapshot,
        )

    @property
    def key(self) -> str:
        return f"{self.wu_id}_{self.name}"


class WorkUnitCoverter:
    _ARTIFACT_SIZE_FILE_THRESHOLD = 1024 * 1024 * 30  # over 30kb
    _ALLOWED_ENCODINGS = {"ascii", "utf-8"}

    @classmethod
    def create(cls):
        return cls(snapshot_type=Snapshot)

    def __init__(self, snapshot_type, *additional_keys: str) -> None:
        self._workunit_map: WorkUnitsMap = {}
        self._allowed_levels = {"INFO"}
        self._allowed_artifacts_keys = {"stdout", "stderr", "xml_results"}
        self._allowed_standalone_artifacts = {"coverage_xml"}
        self._allowed_metadata = {"exit_code"}
        if additional_keys:
            self._allowed_artifacts_keys.update(additional_keys)
        self._standalone_artifacts: Dict[str, ArtifactRef] = {}
        self._snapshot_type = snapshot_type

    def set_context(self, context) -> None:
        self._context = context

    def _maybe_capture_standalone_artifacts(self, wu_json: dict, name: str, artifact: Union[Digest, Snapshot]) -> bool:
        size = (
            artifact.digest.serialized_bytes_length
            if isinstance(artifact, self._snapshot_type)
            else artifact.serialized_bytes_length
        )
        if size < self._ARTIFACT_SIZE_FILE_THRESHOLD and name not in self._allowed_standalone_artifacts:
            return False
        ref = ArtifactRef.create(wu_json["span_id"], name, artifact)
        if ref.key not in self._standalone_artifacts:
            self._standalone_artifacts[ref.key] = ref
        return True

    def transform(self, workunits: WorkUnitsMap, call_num: int, last_update_timestamp: int) -> WorkUnits:
        self._workunit_map.update(workunits)
        return [self._wu_dict(wu, call_num, last_update_timestamp) for wu in self._filter_work_units(workunits)]

    def get_all_work_units(self, call_num: int, last_update_timestamp: int) -> WorkUnits:
        all_wus = [
            self._wu_dict_with_artifacts(wu, call_num, last_update_timestamp) for wu in self._workunit_map.values()
        ]
        if self._standalone_artifacts:
            _logger.debug(f"Collected standalone artifacts: {self._standalone_artifacts}")
        return all_wus

    def get_standalone_artifacts(self) -> Optional[Artifacts]:
        if not self._standalone_artifacts:
            return None
        return self._get_standalone_snapshot_artifacts()

    def _get_standalone_snapshot_artifacts(self) -> Artifacts:
        refs = []
        snapshots = []
        for ref in self._standalone_artifacts.values():
            if not ref.snapshot:
                continue
            snapshots.append(ref.snapshot)
            refs.append(ref)
        artifacts_files = {}
        artifacts_descriptors = {}

        for index, digest_contents in enumerate(self._context.snapshots_to_file_contents(snapshots)):
            ref = refs[index]
            for fc in digest_contents:
                filename = uuid.uuid1().hex
                artifacts_files[filename] = fc.content
                artifacts_descriptors[filename] = {
                    "workunit_id": ref.wu_id,
                    "name": ref.name,
                    "path": fc.path,
                }
        artifacts_files["descriptors.json"] = json.dumps(artifacts_descriptors).encode()
        return artifacts_files

    def _filter_work_units(self, workunits: WorkUnitsMap) -> Iterator[dict]:
        reported_ids = set()
        for wu_id, wu_json in workunits.items():
            if wu_id in reported_ids:
                continue
            should_report = wu_json.get("artifacts") or wu_json["level"] in self._allowed_levels
            if not should_report:
                continue
            reported_ids.add(wu_id)
            parent_id = wu_json.get("parent_id")
            while parent_id:
                parent_wu = self._workunit_map[parent_id]
                wu_id = parent_wu["span_id"]
                if wu_id not in reported_ids:
                    reported_ids.add(wu_id)
                    yield parent_wu
                parent_id = parent_wu.get("parent_id")
            yield wu_json

    def _wu_dict(self, wu_json: dict, version: int, last_update_timestamp: int) -> dict:
        """"Create a work unit json in a structure expected by the buildsense service."""
        start_usecs = _to_usecs(wu_json, "start")
        is_finished = "duration_secs" in wu_json
        wu_id = wu_json["span_id"]
        wu = {
            "workunit_id": wu_id,
            "name": wu_json["name"],
            "state": "finished" if is_finished else "started",
            "version": version,
            "parent_id": wu_json.get("parent_id") or None,
            "last_update": last_update_timestamp,
            "start_usecs": start_usecs,
        }
        description = wu_json.get("description")
        if description:
            wu["description"] = description

        if is_finished:
            duration_usecs = _to_usecs(wu_json, "duration")
            wu["end_usecs"] = start_usecs + duration_usecs
        return wu

    def _wu_dict_with_artifacts(self, wu_json: dict, version: int, last_update_timestamp: int) -> dict:
        wu = self._wu_dict(wu_json, version, last_update_timestamp)
        counters = wu_json.get("counters")
        metadata = wu_json.get("metadata", {}).items()
        allowed_metadata = {key: value for key, value in metadata if key in self._allowed_metadata}
        if counters:
            wu["counters"] = counters
        if allowed_metadata:
            wu["metadata"] = allowed_metadata
        artifacts = self._get_artifacts(wu_json)
        if not artifacts:
            return wu
        wu["artifacts"] = artifacts
        return wu

    def _get_digest_artifacts(
        self, wu_json: dict, keys: List[str], digests: List[Union[FileDigest, Digest]]
    ) -> ArtifactsMap:
        if not keys:
            return {}
        try:
            artifacts = (artifact.decode() for artifact in self._context.single_file_digests_to_bytes(digests))
        except Exception:
            _logger.exception(f"Failed to get digests. keys={keys} digests={digests} {wu_json}")
            raise
        return dict(zip(keys, artifacts))

    def _get_snapshot_artifacts(self, keys: List[str], snapshots: List[Snapshot]) -> ArtifactsMap:
        if not keys:
            return {}

        def dump_dc(dc: DigestContents) -> Dict[str, str]:
            # Primitive mechanism using chardet to make sure we don't try to dump binary data here.
            # if needed, binary data should be captured via standalone artifacts
            return {
                fc.path: fc.content.decode()
                for fc in dc
                if chardet.detect(fc.content)["encoding"] in self._ALLOWED_ENCODINGS
            }

        artifacts = (dump_dc(dc) for dc in self._context.snapshots_to_file_contents(snapshots))
        return dict(zip(keys, artifacts))

    def _get_artifacts(self, wu_json: dict) -> Optional[ArtifactsMap]:
        digest_keys = []
        digests = []
        snapshot_keys = []
        snapshots = []
        for key, artifact in wu_json.get("artifacts", {}).items():
            if not isinstance(artifact, (self._snapshot_type, Digest, FileDigest)):
                _logger.warning(f"unexpected artifact type: {type(artifact)} {artifact}")
                continue
            if self._maybe_capture_standalone_artifacts(wu_json, key, artifact):
                continue
            if isinstance(artifact, self._snapshot_type) and artifact.digest.serialized_bytes_length:
                snapshot_keys.append(key)
                snapshots.append(artifact)
            elif isinstance(artifact, (Digest, FileDigest)) and artifact.serialized_bytes_length:
                digest_keys.append(key.replace("_digest", ""))
                digests.append(artifact)
        # This is somewhat wasteful since we ask pants for artifacts we are going to end up filtering out.
        # However, this will let us know if there artifacts we can't read.
        # Eventually, we will need to better optimize it.
        artifacts = self._get_digest_artifacts(wu_json, digest_keys, digests)
        artifacts.update(self._get_snapshot_artifacts(snapshot_keys, snapshots))
        filtered_artifacts = {key: value for key, value in artifacts.items() if key in self._allowed_artifacts_keys}
        return filtered_artifacts or None
