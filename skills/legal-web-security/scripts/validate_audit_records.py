#!/usr/bin/env python3
"""Validate the machine-readable artifacts produced by audit mode.

Usage:
    python3 validate_audit_records.py <audit-output-directory>

The validator is intentionally dependency-free. It checks the artifact contract
and evidence bookkeeping; it does not establish security, legal compliance, or
the truth of an application claim.
"""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any, Iterable


MAX_INPUT_BYTES = 5 * 1024 * 1024
MAX_DEPTH = 64
MAX_COLLECTION_ITEMS = 1000
MAX_ERRORS = 100

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
FINGERPRINT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$")
STATUS_VALUES = {
    "planned",
    "in_progress",
    "covered",
    "candidate",
    "blocked",
    "deferred",
    "out_of_scope",
    "not_applicable",
}
CHECK_STATUS_VALUES = {"covered", "candidate", "blocked"}
METHOD_VALUES = {"source", "local", "runtime", "provided"}
PRIOR_STATUS_VALUES = {
    "none",
    "new",
    "prior_confirmed_same_source",
    "prior_confirmed_changed_source",
    "prior_needs_validation",
    "prior_rejected_claim_changed",
    "prior_covered_same_source",
    "prior_covered_changed_source",
    "prior_deferred",
    "prior_blocked",
    "prior_out_of_scope",
}
VERDICT_VALUES = {"confirmed", "needs_validation", "rejected"}
LEGAL_STATUS_VALUES = {"not_assessed", "route_only", "needs_counsel", "verified_source"}
EVIDENCE_STATUS_VALUES = {
    "observed",
    "provided",
    "assumed",
    "unknown",
    "needs_counsel",
    "not_verified",
}
SEVERITY_ORDER = ("informational", "low", "medium", "high", "critical")
SEVERITY_VALUES = set(SEVERITY_ORDER)
SEVERITY_RANK = {name: index for index, name in enumerate(SEVERITY_ORDER)}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def add(self, location: str, message: str) -> None:
        if len(self.errors) < MAX_ERRORS:
            self.errors.append(f"{location}: {message}")

    def extend(self, other: "Validation") -> None:
        for error in other.errors:
            if len(self.errors) >= MAX_ERRORS:
                break
            self.errors.append(error)


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_string(value: Any, location: str, result: Validation) -> None:
    if not is_nonempty_string(value):
        result.add(location, "must be a non-empty string")


def check_string_list(
    value: Any,
    location: str,
    result: Validation,
    *,
    allow_empty: bool = True,
    unique: bool = True,
) -> None:
    if not isinstance(value, list):
        result.add(location, "must be an array of strings")
        return
    if not allow_empty and not value:
        result.add(location, "must contain at least one item")
    if len(value) > MAX_COLLECTION_ITEMS:
        result.add(location, f"exceeds {MAX_COLLECTION_ITEMS} items")
    seen: set[str] = set()
    for index, item in enumerate(value):
        check_string(item, f"{location}[{index}]", result)
        if isinstance(item, str) and unique:
            if item in seen:
                result.add(f"{location}[{index}]", "duplicates an earlier item")
            seen.add(item)


def check_enum(value: Any, location: str, values: Iterable[str], result: Validation) -> None:
    allowed = set(values)
    if value not in allowed:
        result.add(location, f"must be one of {', '.join(sorted(allowed))}")


def check_object(value: Any, location: str, result: Validation) -> bool:
    if not isinstance(value, dict):
        result.add(location, "must be an object")
        return False
    if len(value) > MAX_COLLECTION_ITEMS:
        result.add(location, f"exceeds {MAX_COLLECTION_ITEMS} fields")
    return True


def check_allowed_fields(value: dict[str, Any], allowed: set[str], location: str, result: Validation) -> None:
    for key in value:
        if key not in allowed:
            result.add(f"{location}.{key}", "unexpected field")


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    if "\\" in value or ":" in value or "\x00" in value:
        return False
    path = Path(value)
    if path.is_absolute() or value.startswith("~"):
        return False
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    return True


def check_path(value: Any, location: str, result: Validation) -> None:
    if not safe_relative_path(value):
        result.add(location, "must be a safe repository-relative path")


def check_slug(value: Any, location: str, result: Validation) -> None:
    if not isinstance(value, str) or not SLUG_RE.fullmatch(value):
        result.add(location, "must be a lowercase slug using letters, digits, '.', '_' or '-'")


def check_agent_id(value: Any, location: str, result: Validation, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        result.add(location, "must be a lowercase reviewer ID")


def check_fingerprint(value: Any, location: str, result: Validation) -> None:
    if not isinstance(value, str) or not FINGERPRINT_RE.fullmatch(value):
        result.add(location, "must be a stable non-empty fingerprint")


def check_depth(value: Any, location: str, result: Validation, depth: int = 0) -> None:
    if len(result.errors) >= MAX_ERRORS:
        return
    if depth > MAX_DEPTH:
        result.add(location, f"exceeds {MAX_DEPTH} nesting levels")
        return
    if isinstance(value, dict):
        if len(value) > MAX_COLLECTION_ITEMS:
            result.add(location, f"exceeds {MAX_COLLECTION_ITEMS} fields")
        for key, child in value.items():
            check_depth(child, f"{location}.{key}", result, depth + 1)
    elif isinstance(value, list):
        if len(value) > MAX_COLLECTION_ITEMS:
            result.add(location, f"exceeds {MAX_COLLECTION_ITEMS} items")
        for index, child in enumerate(value):
            check_depth(child, f"{location}[{index}]", result, depth + 1)


def read_json(path: Path, result: Validation) -> Any:
    location = str(path)
    try:
        info = os.lstat(path)
    except OSError as error:
        result.add(location, f"cannot stat file: {error}")
        return None
    if stat.S_ISLNK(info.st_mode):
        result.add(location, "must not be a symlink")
        return None
    if not stat.S_ISREG(info.st_mode):
        result.add(location, "must be a regular file")
        return None
    if info.st_size > MAX_INPUT_BYTES:
        result.add(location, f"exceeds {MAX_INPUT_BYTES} bytes")
        return None
    try:
        with path.open("rb") as handle:
            contents = handle.read(MAX_INPUT_BYTES + 1)
    except OSError as error:
        result.add(location, f"cannot read file: {error}")
        return None
    if len(contents) > MAX_INPUT_BYTES:
        result.add(location, f"exceeds {MAX_INPUT_BYTES} bytes")
        return None
    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        result.add(location, "must be valid UTF-8")
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        result.add(location, f"invalid JSON: {error.msg} at line {error.lineno} column {error.colno}")
        return None
    check_depth(value, "$", result)
    return value


def check_trace(value: Any, location: str, result: Validation) -> None:
    if not isinstance(value, list) or not value:
        result.add(location, "must contain at least one trace item")
        return
    if len(value) > MAX_COLLECTION_ITEMS:
        result.add(location, f"exceeds {MAX_COLLECTION_ITEMS} items")
        return
    allowed = {"kind", "file", "line", "scope", "description"}
    for index, item in enumerate(value):
        item_location = f"{location}[{index}]"
        if not check_object(item, item_location, result):
            continue
        check_allowed_fields(item, allowed, item_location, result)
        check_enum(item.get("kind"), f"{item_location}.kind", {"entrypoint", "propagation", "sink"}, result)
        check_path(item.get("file"), f"{item_location}.file", result)
        if not isinstance(item.get("line"), int) or isinstance(item.get("line"), bool) or item.get("line", 0) < 1:
            result.add(f"{item_location}.line", "must be a positive integer")
        check_string(item.get("scope"), f"{item_location}.scope", result)
        check_string(item.get("description"), f"{item_location}.description", result)
    if len(value) == 1:
        if isinstance(value[0], dict) and value[0].get("kind") not in {"entrypoint", "sink"}:
            result.add(f"{location}[0].kind", "a one-item trace must be entrypoint or sink")
    elif isinstance(value[0], dict) and value[0].get("kind") != "entrypoint":
        result.add(f"{location}[0].kind", "a multi-item trace must start at entrypoint")
    elif isinstance(value[-1], dict) and value[-1].get("kind") != "sink":
        result.add(f"{location}[{len(value) - 1}].kind", "a multi-item trace must end at sink")
    for index in range(1, len(value) - 1):
        if isinstance(value[index], dict) and value[index].get("kind") != "propagation":
            result.add(f"{location}[{index}].kind", "a middle trace item must be propagation")


def check_evidence(value: Any, location: str, result: Validation) -> None:
    if not isinstance(value, list) or not value:
        result.add(location, "must contain at least one evidence item")
        return
    allowed = {"file", "line", "description", "status", "kind"}
    for index, item in enumerate(value):
        item_location = f"{location}[{index}]"
        if not check_object(item, item_location, result):
            continue
        check_allowed_fields(item, allowed, item_location, result)
        check_path(item.get("file"), f"{item_location}.file", result)
        if not isinstance(item.get("line"), int) or isinstance(item.get("line"), bool) or item.get("line", 0) < 1:
            result.add(f"{item_location}.line", "must be a positive integer")
        check_string(item.get("description"), f"{item_location}.description", result)
        check_enum(item.get("status"), f"{item_location}.status", EVIDENCE_STATUS_VALUES, result)
        if "kind" in item:
            check_string(item.get("kind"), f"{item_location}.kind", result)


def check_context(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {"jurisdictions", "data_categories", "legal_status", "legal_questions", "source_refs"}
    check_allowed_fields(value, allowed, location, result)
    check_string_list(value.get("jurisdictions"), f"{location}.jurisdictions", result, allow_empty=False)
    check_string_list(value.get("data_categories"), f"{location}.data_categories", result)
    check_enum(value.get("legal_status"), f"{location}.legal_status", LEGAL_STATUS_VALUES, result)
    check_string_list(value.get("legal_questions", []), f"{location}.legal_questions", result)
    check_string_list(value.get("source_refs", []), f"{location}.source_refs", result)
    if value.get("legal_status") == "verified_source" and not value.get("source_refs"):
        result.add(f"{location}.source_refs", "verified_source requires at least one source reference")
    if value.get("legal_status") == "needs_counsel" and not value.get("legal_questions"):
        result.add(f"{location}.legal_questions", "needs_counsel requires a concrete legal question")


def check_verification(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {"hunted_by", "validated_by", "record_checked_by", "notes"}
    check_allowed_fields(value, allowed, location, result)
    check_agent_id(value.get("hunted_by"), f"{location}.hunted_by", result)
    check_agent_id(value.get("validated_by"), f"{location}.validated_by", result)
    if value.get("hunted_by") == value.get("validated_by"):
        result.add(location, "hunted_by and validated_by must be different reviewers")
    record_checked_by = value.get("record_checked_by", [])
    check_string_list(record_checked_by, f"{location}.record_checked_by", result, allow_empty=False)
    for index, reviewer in enumerate(record_checked_by if isinstance(record_checked_by, list) else []):
        check_agent_id(reviewer, f"{location}.record_checked_by[{index}]", result)
        if reviewer == value.get("hunted_by"):
            result.add(f"{location}.record_checked_by[{index}]", "must not be the hunter")
    if "notes" in value:
        check_string(value.get("notes"), f"{location}.notes", result)


def check_severity(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {"likelihood", "impact", "overall_severity"}
    check_allowed_fields(value, allowed, location, result)
    for field in ("likelihood", "impact"):
        field_location = f"{location}.{field}"
        if not check_object(value.get(field), field_location, result):
            continue
        check_allowed_fields(value[field], {"score", "reason"}, field_location, result)
        check_enum(value[field].get("score"), f"{field_location}.score", SEVERITY_VALUES, result)
        check_string(value[field].get("reason"), f"{field_location}.reason", result)
    check_enum(value.get("overall_severity"), f"{location}.overall_severity", SEVERITY_VALUES, result)
    impact = value.get("impact", {}).get("score") if isinstance(value.get("impact"), dict) else None
    overall = value.get("overall_severity")
    if impact in SEVERITY_RANK and overall in SEVERITY_RANK and SEVERITY_RANK[overall] > SEVERITY_RANK[impact]:
        result.add(f"{location}.overall_severity", "cannot exceed demonstrated impact")


def check_execution(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {"attacker_perspective", "payloads", "instructions", "observed_result"}
    check_allowed_fields(value, allowed, location, result)
    check_string(value.get("attacker_perspective"), f"{location}.attacker_perspective", result)
    check_string_list(value.get("payloads"), f"{location}.payloads", result, allow_empty=False)
    check_string_list(value.get("instructions"), f"{location}.instructions", result, allow_empty=False, unique=False)
    check_string(value.get("observed_result"), f"{location}.observed_result", result)


def check_remediation(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {"strategy", "code_changes", "regression_test"}
    check_allowed_fields(value, allowed, location, result)
    check_string(value.get("strategy"), f"{location}.strategy", result)
    if "regression_test" in value:
        check_string(value.get("regression_test"), f"{location}.regression_test", result)
    changes = value.get("code_changes", [])
    if not isinstance(changes, list):
        result.add(f"{location}.code_changes", "must be an array")
    else:
        for index, change in enumerate(changes):
            change_location = f"{location}.code_changes[{index}]"
            if not check_object(change, change_location, result):
                continue
            check_allowed_fields(change, {"file_name", "fixed_code"}, change_location, result)
            check_path(change.get("file_name"), f"{change_location}.file_name", result)
            check_string(change.get("fixed_code"), f"{change_location}.fixed_code", result)


def check_conditions(value: Any, location: str, result: Validation) -> None:
    if not isinstance(value, list) or not value:
        result.add(location, "must contain at least one condition")
        return
    for index, condition in enumerate(value):
        condition_location = f"{location}[{index}]"
        if not check_object(condition, condition_location, result):
            continue
        check_allowed_fields(condition, {"kind", "description"}, condition_location, result)
        check_string(condition.get("kind"), f"{condition_location}.kind", result)
        check_string(condition.get("description"), f"{condition_location}.description", result)


def check_validation_plan(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {"local", "deployment", "owner"}
    check_allowed_fields(value, allowed, location, result)
    present = False
    for field in allowed:
        if field in value:
            check_string(value.get(field), f"{location}.{field}", result)
            present = present or is_nonempty_string(value.get(field))
    if not present:
        result.add(location, "must contain a concrete local, deployment, or owner plan")


def check_finding(finding: Any, location: str, result: Validation) -> None:
    if not check_object(finding, location, result):
        return
    base_fields = {
        "verdict",
        "fingerprint",
        "title",
        "description",
        "affected_surface",
        "trace",
        "evidence",
        "context",
        "verification",
    }
    verdict = finding.get("verdict")
    check_enum(verdict, f"{location}.verdict", VERDICT_VALUES, result)
    check_fingerprint(finding.get("fingerprint"), f"{location}.fingerprint", result)
    for field in ("title", "description", "affected_surface"):
        check_string(finding.get(field), f"{location}.{field}", result)
    check_trace(finding.get("trace"), f"{location}.trace", result)
    check_evidence(finding.get("evidence"), f"{location}.evidence", result)
    check_context(finding.get("context"), f"{location}.context", result)
    check_verification(finding.get("verification"), f"{location}.verification", result)

    if verdict == "confirmed":
        allowed = base_fields | {
            "root_cause",
            "intended_behavior",
            "conditions",
            "execution",
            "remediation",
            "severity",
            "confidence",
        }
        required = {
            "root_cause",
            "intended_behavior",
            "conditions",
            "execution",
            "remediation",
            "severity",
            "confidence",
        }
        for field in required:
            if field not in finding:
                result.add(location, f"confirmed record is missing {field}")
        for field in ("root_cause", "intended_behavior"):
            check_string(finding.get(field), f"{location}.{field}", result)
        check_conditions(finding.get("conditions"), f"{location}.conditions", result)
        check_execution(finding.get("execution"), f"{location}.execution", result)
        check_remediation(finding.get("remediation"), f"{location}.remediation", result)
        check_severity(finding.get("severity"), f"{location}.severity", result)
        confidence = finding.get("confidence")
        if check_object(confidence, f"{location}.confidence", result):
            check_allowed_fields(confidence, {"score", "reason"}, f"{location}.confidence", result)
            check_enum(confidence.get("score"), f"{location}.confidence.score", {"low", "medium", "high"}, result)
            check_string(confidence.get("reason"), f"{location}.confidence.reason", result)
    elif verdict == "needs_validation":
        allowed = base_fields | {"claimed_root_cause", "blockers", "validation_plan"}
        required = {"claimed_root_cause", "blockers", "validation_plan"}
        for field in required:
            if field not in finding:
                result.add(location, f"needs_validation record is missing {field}")
        check_string(finding.get("claimed_root_cause"), f"{location}.claimed_root_cause", result)
        check_string_list(finding.get("blockers"), f"{location}.blockers", result, allow_empty=False)
        check_validation_plan(finding.get("validation_plan"), f"{location}.validation_plan", result)
    elif verdict == "rejected":
        allowed = base_fields | {"claimed_root_cause", "reason"}
        required = {"claimed_root_cause", "reason"}
        for field in required:
            if field not in finding:
                result.add(location, f"rejected record is missing {field}")
        check_string(finding.get("claimed_root_cause"), f"{location}.claimed_root_cause", result)
        check_string(finding.get("reason"), f"{location}.reason", result)
    else:
        allowed = base_fields

    check_allowed_fields(finding, allowed, location, result)


def check_findings(value: Any, result: Validation) -> None:
    if not isinstance(value, list):
        result.add("findings.json", "top-level value must be an array")
        return
    if len(value) > MAX_COLLECTION_ITEMS:
        result.add("findings.json", f"exceeds {MAX_COLLECTION_ITEMS} findings")
    previous: str | None = None
    fingerprints: set[str] = set()
    for index, finding in enumerate(value):
        location = f"findings.json[{index}]"
        check_finding(finding, location, result)
        if isinstance(finding, dict):
            fingerprint = finding.get("fingerprint")
            if isinstance(fingerprint, str):
                if fingerprint in fingerprints:
                    result.add(f"{location}.fingerprint", "duplicates another finding")
                fingerprints.add(fingerprint)
                if previous is not None and fingerprint < previous:
                    result.add(f"{location}.fingerprint", "findings must be sorted lexicographically")
                previous = fingerprint


def check_check(value: Any, location: str, result: Validation) -> set[str]:
    paths: set[str] = set()
    if not check_object(value, location, result):
        return paths
    allowed = {
        "check_id",
        "agent_id",
        "method",
        "status",
        "reviewed_paths",
        "local_checks",
        "result_fingerprints",
        "unresolved",
    }
    check_allowed_fields(value, allowed, location, result)
    check_string(value.get("check_id"), f"{location}.check_id", result)
    check_agent_id(value.get("agent_id"), f"{location}.agent_id", result)
    check_enum(value.get("method"), f"{location}.method", METHOD_VALUES, result)
    check_enum(value.get("status"), f"{location}.status", CHECK_STATUS_VALUES, result)
    reviewed = value.get("reviewed_paths")
    check_string_list(reviewed, f"{location}.reviewed_paths", result, allow_empty=value.get("status") == "blocked")
    for index, path in enumerate(reviewed if isinstance(reviewed, list) else []):
        check_path(path, f"{location}.reviewed_paths[{index}]", result)
        if isinstance(path, str):
            paths.add(path)
    check_string_list(value.get("local_checks"), f"{location}.local_checks", result)
    check_string_list(value.get("result_fingerprints"), f"{location}.result_fingerprints", result)
    for index, fingerprint in enumerate(value.get("result_fingerprints", []) if isinstance(value.get("result_fingerprints"), list) else []):
        check_fingerprint(fingerprint, f"{location}.result_fingerprints[{index}]", result)
    check_string_list(value.get("unresolved"), f"{location}.unresolved", result)
    if value.get("method") in {"local", "runtime"} and not value.get("local_checks"):
        result.add(f"{location}.local_checks", "local/runtime checks require at least one named check")
    return paths


def check_unit(value: Any, location: str, result: Validation) -> None:
    if not check_object(value, location, result):
        return
    allowed = {
        "coverage_id",
        "surface",
        "boundary",
        "subsystem",
        "attack_class",
        "status",
        "prior_status",
        "owner",
        "reviewed_paths",
        "checks",
        "result_fingerprints",
        "unresolved",
    }
    check_allowed_fields(value, allowed, location, result)
    for field in ("surface", "boundary", "subsystem", "attack_class"):
        check_slug(value.get(field), f"{location}.{field}", result)
    expected_id = "|".join(str(value.get(field)) for field in ("surface", "boundary", "subsystem", "attack_class"))
    if value.get("coverage_id") != expected_id:
        result.add(f"{location}.coverage_id", f"must equal canonical ID {expected_id!r}")
    check_enum(value.get("status"), f"{location}.status", STATUS_VALUES, result)
    check_enum(value.get("prior_status"), f"{location}.prior_status", PRIOR_STATUS_VALUES, result)
    check_agent_id(value.get("owner"), f"{location}.owner", result, nullable=True)
    reviewed = value.get("reviewed_paths")
    check_string_list(reviewed, f"{location}.reviewed_paths", result)
    reviewed_set: set[str] = set()
    for index, path in enumerate(reviewed if isinstance(reviewed, list) else []):
        check_path(path, f"{location}.reviewed_paths[{index}]", result)
        if isinstance(path, str):
            reviewed_set.add(path)
    check_string_list(value.get("result_fingerprints"), f"{location}.result_fingerprints", result)
    for index, fingerprint in enumerate(value.get("result_fingerprints", []) if isinstance(value.get("result_fingerprints"), list) else []):
        check_fingerprint(fingerprint, f"{location}.result_fingerprints[{index}]", result)
    check_string_list(value.get("unresolved"), f"{location}.unresolved", result)

    checks = value.get("checks")
    if not isinstance(checks, list):
        result.add(f"{location}.checks", "must be an array")
        checks = []
    check_ids: set[str] = set()
    check_paths: set[str] = set()
    check_fingerprints: set[str] = set()
    for index, check in enumerate(checks):
        check_location = f"{location}.checks[{index}]"
        check_paths.update(check_check(check, check_location, result))
        if isinstance(check, dict):
            check_id = check.get("check_id")
            if isinstance(check_id, str):
                if check_id in check_ids:
                    result.add(f"{check_location}.check_id", "duplicates another check")
                check_ids.add(check_id)
            fingerprints = check.get("result_fingerprints", [])
            if isinstance(fingerprints, list):
                check_fingerprints.update(item for item in fingerprints if isinstance(item, str))
    if reviewed_set != check_paths:
        result.add(f"{location}.reviewed_paths", "must equal the union of check reviewed_paths")
    result_fingerprints = value.get("result_fingerprints")
    if isinstance(result_fingerprints, list) and set(result_fingerprints) != check_fingerprints:
        result.add(f"{location}.result_fingerprints", "must equal the union of check result_fingerprints")

    status = value.get("status")
    if status == "planned":
        if value.get("owner") is not None or reviewed_set or checks or value.get("result_fingerprints") or value.get("unresolved"):
            result.add(location, "planned unit must not contain review evidence or an owner")
    elif status == "in_progress":
        if value.get("owner") is None:
            result.add(f"{location}.owner", "in_progress unit requires an owner")
        if reviewed_set or checks or value.get("result_fingerprints") or value.get("unresolved"):
            result.add(location, "in_progress unit must not claim completed evidence")
    elif status in {"not_applicable", "out_of_scope", "deferred"}:
        if not value.get("unresolved"):
            result.add(f"{location}.unresolved", f"{status} unit requires a reason")
        if value.get("owner") is not None or reviewed_set or checks or value.get("result_fingerprints"):
            result.add(location, f"{status} unit must not contain review evidence")
    elif status == "blocked":
        if value.get("owner") is None or not checks or not reviewed_set or not value.get("unresolved"):
            result.add(location, "blocked unit requires owner, partial checks, reviewed paths, and a blocker")
    elif status == "candidate":
        if value.get("owner") is None or not checks or not reviewed_set or not value.get("result_fingerprints"):
            result.add(location, "candidate unit requires owner, checks, reviewed paths, and a fingerprint")
    elif status == "covered":
        if not checks or not reviewed_set or value.get("unresolved"):
            result.add(location, "covered unit requires checks and paths and must have no unresolved blocker")


def check_coverage(value: Any, result: Validation) -> set[str]:
    finding_fingerprints: set[str] = set()
    if not check_object(value, "coverage-ledger.json", result):
        return finding_fingerprints
    check_allowed_fields(value, {"schema_version", "run", "units"}, "coverage-ledger.json", result)
    if value.get("schema_version") != 1:
        result.add("coverage-ledger.json.schema_version", "must be integer 1")
    run = value.get("run")
    if check_object(run, "coverage-ledger.json.run", result):
        check_allowed_fields(
            run,
            {"run_id", "profile", "status", "scope", "target_ref", "prior_run_ids", "incomplete_reason"},
            "coverage-ledger.json.run",
            result,
        )
        check_string(run.get("run_id"), "coverage-ledger.json.run.run_id", result)
        check_enum(run.get("profile"), "coverage-ledger.json.run.profile", {"quick", "standard", "deep"}, result)
        check_enum(run.get("status"), "coverage-ledger.json.run.status", {"complete", "incomplete"}, result)
        check_string(run.get("scope"), "coverage-ledger.json.run.scope", result)
        check_string(run.get("target_ref"), "coverage-ledger.json.run.target_ref", result)
        check_string_list(run.get("prior_run_ids", []), "coverage-ledger.json.run.prior_run_ids", result)
        if run.get("status") == "incomplete":
            check_string(run.get("incomplete_reason"), "coverage-ledger.json.run.incomplete_reason", result)
    units = value.get("units")
    if not isinstance(units, list):
        result.add("coverage-ledger.json.units", "must be an array")
        return finding_fingerprints
    if len(units) > MAX_COLLECTION_ITEMS:
        result.add("coverage-ledger.json.units", f"exceeds {MAX_COLLECTION_ITEMS} units")
    ids: set[str] = set()
    semantics: set[tuple[Any, ...]] = set()
    previous: str | None = None
    for index, unit in enumerate(units):
        location = f"coverage-ledger.json.units[{index}]"
        check_unit(unit, location, result)
        if isinstance(unit, dict):
            coverage_id = unit.get("coverage_id")
            if isinstance(coverage_id, str):
                if coverage_id in ids:
                    result.add(f"{location}.coverage_id", "duplicates another coverage unit")
                ids.add(coverage_id)
                if previous is not None and coverage_id < previous:
                    result.add(f"{location}.coverage_id", "units must be sorted lexicographically")
                previous = coverage_id
            semantic = tuple(unit.get(field) for field in ("surface", "boundary", "subsystem", "attack_class"))
            if all(isinstance(item, str) for item in semantic):
                if semantic in semantics:
                    result.add(location, "duplicates another surface/boundary/subsystem/attack_class tuple")
                semantics.add(semantic)
            fingerprints = unit.get("result_fingerprints", [])
            if isinstance(fingerprints, list):
                finding_fingerprints.update(item for item in fingerprints if isinstance(item, str))
    return finding_fingerprints


def validate_directory(directory: Path) -> int:
    result = Validation()
    if not directory.exists() or not directory.is_dir() or directory.is_symlink():
        result.add(str(directory), "must be a real audit output directory")
        print_errors(result)
        return 1
    coverage = read_json(directory / "coverage-ledger.json", result)
    findings = read_json(directory / "findings.json", result)
    ledger_fingerprints: set[str] = set()
    if coverage is not None:
        ledger_fingerprints = check_coverage(coverage, result)
    if findings is not None:
        check_findings(findings, result)
        if isinstance(findings, list):
            for index, finding in enumerate(findings):
                if isinstance(finding, dict) and isinstance(finding.get("fingerprint"), str):
                    if finding["fingerprint"] not in ledger_fingerprints:
                        result.add(
                            f"findings.json[{index}].fingerprint",
                            "must be linked from a coverage unit result_fingerprints list",
                        )
    if result.errors:
        print_errors(result)
        return 1
    print("PASS: audit coverage ledger and findings are structurally valid")
    return 0


def print_errors(result: Validation) -> None:
    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    suffix = "; output capped at 100" if len(result.errors) == MAX_ERRORS else ""
    print(f"FAIL: {len(result.errors)} validation error(s){suffix}", file=sys.stderr)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 validate_audit_records.py <audit-output-directory>", file=sys.stderr)
        return 2
    return validate_directory(Path(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
