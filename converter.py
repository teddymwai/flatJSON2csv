"""Streaming conversion primitives used by the flatJSON2csv command."""

from __future__ import annotations

import csv
import fnmatch
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterator

try:
    import ijson
except ImportError as exc:  # pragma: no cover - import message is for end users
    ijson = None
    _IJSON_IMPORT_ERROR = exc
else:
    _IJSON_IMPORT_ERROR = None


class ConverterError(Exception):
    """Invalid input, configuration, or conversion operation."""


DEFAULTS: dict[str, Any] = {
    "input_path": None,
    "flatten": "depth:2",
    "array_strategy": "json",
    "array_cap": 10,
    "array_delimiter": "; ",
    "allow_cartesian": False,
    "column_order": "sorted",
    "encoding": "utf-8",
    "quoting": csv.QUOTE_MINIMAL,
    "overrides": [],
    "columns": None,
}
CONFIG_KEYS = set(DEFAULTS)


def validate_settings(config: dict[str, Any]) -> dict[str, Any]:
    if isinstance(config["quoting"], str):
        quote_modes = {"minimal": csv.QUOTE_MINIMAL, "all": csv.QUOTE_ALL}
        if config["quoting"] not in quote_modes:
            raise ConverterError("quoting must be 'minimal' or 'all'.")
        config["quoting"] = quote_modes[config["quoting"]]
    if config["flatten"] not in ("none", "full") and not (
        isinstance(config["flatten"], str)
        and (config["flatten"].startswith("depth:") or config["flatten"].startswith("paths:"))
    ):
        raise ConverterError("flatten must be 'none', 'full', 'depth:N', or 'paths:path.one,path.two'.")
    if isinstance(config["flatten"], str) and config["flatten"].startswith("depth:"):
        try:
            depth = int(config["flatten"].split(":", 1)[1])
        except ValueError as exc:
            raise ConverterError("flatten depth must be a positive integer.") from exc
        if depth < 1:
            raise ConverterError("flatten depth must be a positive integer.")
    if isinstance(config["flatten"], str) and config["flatten"].startswith("paths:") and not config["flatten"][6:].strip():
        raise ConverterError("paths flattening requires at least one path.")
    if config["array_strategy"] not in ("explode", "columns", "json", "join"):
        raise ConverterError("array_strategy must be explode, columns, json, or join.")
    if not isinstance(config["array_cap"], int) or isinstance(config["array_cap"], bool) or config["array_cap"] < 0:
        raise ConverterError("array_cap must be zero or greater.")
    if config["column_order"] not in ("sorted", "first_seen"):
        raise ConverterError("column_order must be 'sorted' or 'first_seen'.")
    if not isinstance(config["encoding"], str) or not config["encoding"]:
        raise ConverterError("encoding must be a non-empty encoding name.")
    if not isinstance(config["overrides"], list):
        raise ConverterError("overrides must be an array.")
    for entry in config["overrides"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ConverterError("Each override must be an object with a string 'path'.")
        unknown_override_keys = set(entry) - {"path", "flatten", "array_strategy", "array_cap", "array_delimiter"}
        if unknown_override_keys:
            raise ConverterError(f"Unknown override key(s): {', '.join(sorted(unknown_override_keys))}")
        if entry.get("array_strategy", config["array_strategy"]) not in ("explode", "columns", "json", "join"):
            raise ConverterError("Override array_strategy must be explode, columns, json, or join.")
        if "flatten" in entry:
            flatten = entry["flatten"]
            if not isinstance(flatten, str) or not (
                flatten in ("none", "full") or flatten.startswith("depth:") or flatten.startswith("paths:")
            ):
                raise ConverterError("Override flatten must be none, full, depth:N, or paths:path.one,path.two.")
        if "array_delimiter" in entry and not isinstance(entry["array_delimiter"], str):
            raise ConverterError("Override array_delimiter must be a string.")
        cap = entry.get("array_cap", config["array_cap"])
        if not isinstance(cap, int) or isinstance(cap, bool) or cap < 0:
            raise ConverterError("Override array_cap must be zero or greater.")
    if config["columns"] is not None and (
        not isinstance(config["columns"], list) or not all(isinstance(item, str) for item in config["columns"])
    ):
        raise ConverterError("columns must be an array of strings or null.")
    if config["input_path"] is not None and not isinstance(config["input_path"], str):
        raise ConverterError("input_path must be a dot-separated string or null.")
    if not isinstance(config["array_delimiter"], str):
        raise ConverterError("array_delimiter must be a string.")
    if not isinstance(config["allow_cartesian"], bool):
        raise ConverterError("allow_cartesian must be true or false.")
    if config["quoting"] not in (csv.QUOTE_MINIMAL, csv.QUOTE_ALL):
        raise ConverterError("quoting must be 'minimal' or 'all'.")
    return config


def load_config(path: str | None) -> dict[str, Any]:
    config = DEFAULTS.copy()
    if not path:
        return config
    with open(Path(path).expanduser(), "r", encoding="utf-8") as stream:
        loaded = json.load(stream)
    if not isinstance(loaded, dict):
        raise ConverterError("Configuration must be a JSON object.")
    unknown = set(loaded) - CONFIG_KEYS
    if unknown:
        raise ConverterError(f"Unknown configuration key(s): {', '.join(sorted(unknown))}")
    config.update(loaded)
    return validate_settings(config)


def discover_inputs(spec: str) -> list[Path]:
    candidate = Path(spec).expanduser()
    if candidate.is_dir():
        matches = sorted(p for p in candidate.iterdir() if p.is_file() and p.suffix.lower() in (".json", ".ndjson", ".jsonl"))
    else:
        expanded = [Path(value) for value in glob_paths(spec)]
        matches = sorted(p for p in expanded if p.is_file() and p.suffix.lower() in (".json", ".ndjson", ".jsonl"))
    if not matches:
        raise ConverterError(f"No JSON or NDJSON input files found for {spec!r}.")
    return matches


def glob_paths(spec: str) -> list[str]:
    import glob

    result = glob.glob(str(Path(spec).expanduser()), recursive=True)
    return result or ([str(Path(spec).expanduser())] if Path(spec).expanduser().exists() else [])


def _stream_json_array(stream, prefix: str) -> Iterator[Any]:
    try:
        yield from ijson.items(stream, prefix, use_float=True)
    except Exception as exc:
        raise ConverterError(f"Could not parse JSON stream at {prefix!r}: {exc}") from exc


def resolve_record_array(path: Path, settings: dict[str, Any]) -> tuple[str | None, bool]:
    """Return (array path, is_single_root_object) for a regular JSON document.

    A missing input_path means a top-level array is used directly. For a top-level
    object, choose the shallowest array of objects and then the largest at that
    depth. If there is no such array, treat the object as one record.
    """
    if ijson is None:
        raise ConverterError(
            "Missing dependency 'ijson'. Install the local requirements with: python -m pip install -r requirements.txt"
        ) from _IJSON_IMPORT_ERROR
    if settings.get("input_path"):
        return settings["input_path"], False
    try:
        with path.open("rb") as stream:
            candidates: dict[str, int] = {}
            first_event = None
            try:
                for prefix, event, _ in ijson.parse(stream):
                    if first_event is None:
                        first_event = event
                        if event == "start_array":
                            return "", False
                        if event != "start_map":
                            raise ConverterError(
                                f"Expected a JSON array or object at the top level in {path}."
                            )
                    if event == "start_map" and prefix.endswith(".item"):
                        array_path = prefix[:-5]
                        candidates[array_path] = candidates.get(array_path, 0) + 1
            except ConverterError:
                raise
            except Exception as exc:
                raise ConverterError(f"Could not inspect JSON input {path}: {exc}") from exc
    except OSError:
        raise
    if first_event is None:
        raise ConverterError(f"JSON input is empty: {path}")
    if not candidates:
        return None, True
    shallowest = min(candidate.count(".") + 1 for candidate in candidates)
    nearest = {candidate: count for candidate, count in candidates.items() if candidate.count(".") + 1 == shallowest}
    ordered = sorted(nearest.items(), key=lambda item: (-item[1], item[0]))
    chosen, count = ordered[0]
    if len(ordered) > 1:
        details = ", ".join(f"{name} ({items} objects)" for name, items in ordered[:6])
        print(
            f"flatJSON2csv: multiple object arrays found at the nearest level; using {chosen!r} ({count} objects). "
            f"Use --input-path to choose another. Candidates: {details}",
            file=sys.stderr,
        )
    return chosen, False


def iter_records(
    path: Path,
    settings: dict[str, Any],
    record_array_path: str | None = None,
    single_root_object: bool = False,
) -> Iterator[Any]:
    if ijson is None:
        raise ConverterError(
            "Missing dependency 'ijson'. Install the local requirements with: python -m pip install -r requirements.txt"
        ) from _IJSON_IMPORT_ERROR
    is_ndjson = path.suffix.lower() in (".ndjson", ".jsonl")
    if is_ndjson:
        try:
            with path.open("r", encoding=settings["encoding"]) as stream:
                for line_number, line in enumerate(stream, 1):
                    if line.strip():
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError as exc:
                            raise ConverterError(f"{path}:{line_number}: invalid NDJSON: {exc.msg}") from exc
        except UnicodeError as exc:
            raise ConverterError(f"Cannot decode {path} as {settings['encoding']}: {exc}") from exc
        return
    input_path = settings.get("input_path")
    prefix = "" if single_root_object else (
        "item" if record_array_path == "" else f"{record_array_path}.item"
        if record_array_path is not None else ("item" if not input_path else f"{input_path}.item")
    )
    try:
        with path.open("rb") as stream:
            for record in _stream_json_array(stream, prefix):
                if not isinstance(record, dict):
                    raise ConverterError(f"Expected each selected record to be an object in {path}.")
                yield record
    except OSError:
        raise


def _override(path: str, settings: dict[str, Any]) -> dict[str, Any]:
    effective: dict[str, Any] = {}
    for entry in settings.get("overrides", []):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ConverterError("Each override must contain a string 'path'.")
        if fnmatch.fnmatchcase(path, entry["path"]):
            effective.update({k: v for k, v in entry.items() if k != "path"})
    return effective


def _strategy(path: str, settings: dict[str, Any], name: str, fallback: Any) -> Any:
    return _override(path, settings).get(name, fallback)


def _json_cell(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _scalar_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _values_at_path(record: Any, path: str) -> list[Any]:
    parts = path.split(".") if path else []
    current = [record]
    for part in parts:
        next_values = []
        for node in current:
            if part == "*":
                if isinstance(node, dict):
                    next_values.extend(node.values())
                elif isinstance(node, list):
                    next_values.extend(node)
            elif isinstance(node, dict) and part in node:
                next_values.append(node[part])
        current = next_values
    return current


def _flatten_value(value: Any, prefix: str, depth: int, settings: dict[str, Any], base_path: str) -> list[dict[str, Any]]:
    flatten_mode = _strategy(base_path, settings, "flatten", settings["flatten"])
    array_mode = _strategy(base_path, settings, "array_strategy", settings["array_strategy"])
    if isinstance(flatten_mode, str) and flatten_mode.startswith("paths:"):
        flatten_mode = "paths"
    if isinstance(value, dict) and flatten_mode != "none" and (
        flatten_mode == "full" or (flatten_mode.startswith("depth:") and depth < int(flatten_mode.split(":", 1)[1]))
    ):
        rows: list[dict[str, Any]] = [{}]
        for key, child in value.items():
            child_path = f"{base_path}.{key}" if base_path else key
            child_prefix = f"{prefix}.{key}" if prefix else key
            child_rows = _flatten_value(child, child_prefix, depth + 1, settings, child_path)
            rows = _merge_rows(rows, child_rows, settings.get("allow_cartesian", False), child_path)
        return rows
    if isinstance(value, (dict, list)):
        if isinstance(value, list) and array_mode == "explode":
            rows: list[dict[str, Any]] = []
            for item in value:
                item_path = f"{base_path}.*" if base_path else "*"
                rows.extend(_flatten_value(item, prefix, depth, settings, item_path))
            return rows or [{prefix: ""}]
        if isinstance(value, list) and array_mode == "join":
            delimiter = _strategy(base_path, settings, "array_delimiter", settings.get("array_delimiter", "; "))
            rendered = delimiter.join(
                _json_cell(item) if isinstance(item, (dict, list)) else "" if item is None else str(item)
                for item in value
            )
            return [{prefix: rendered}]
        if isinstance(value, list) and array_mode == "columns":
            cap = int(_strategy(base_path, settings, "array_cap", settings["array_cap"]))
            if cap < 0:
                raise ConverterError("array_cap must be zero or greater.")
            if len(value) > cap:
                return [{prefix: _json_cell(value)}]
            rows: list[dict[str, Any]] = [{}]
            for index, item in enumerate(value):
                item_prefix = f"{prefix}_{index}" if prefix else str(index)
                expanded = _flatten_value(item, item_prefix, depth + 1, settings, f"{base_path}.*")
                rows = _merge_rows(rows, expanded, settings.get("allow_cartesian", False), base_path)
            return rows or [{prefix: ""}]
        return [{prefix: _json_cell(value)}]
    if value is None:
        value = ""
    elif isinstance(value, bool):
        value = "true" if value else "false"
    return [{prefix: _scalar_cell(value)}]


def _merge_rows(left: list[dict[str, Any]], right: list[dict[str, Any]], allow_cartesian: bool, path: str) -> list[dict[str, Any]]:
    if len(left) > 1 and len(right) > 1 and not allow_cartesian:
        raise ConverterError(
            f"Multiple exploded arrays create a Cartesian product near {path!r}; opt in with --allow-cartesian or allow_cartesian in config."
        )
    return [{**a, **b} for a in left for b in right]


def flatten_record(record: Any, settings: dict[str, Any], path_prefix: str = "*") -> list[dict[str, Any]]:
    selected = settings.get("columns")
    if selected is not None:
        row: dict[str, Any] = {}
        for path in selected:
            values = _values_at_path(record, path)
            value = values[0] if len(values) == 1 else values if values else None
            row[path] = _json_cell(value) if isinstance(value, (dict, list)) else _scalar_cell(value)
        return [row]
    mode = settings["flatten"]
    paths = None
    if isinstance(mode, str) and mode.startswith("paths:"):
        paths = [part.strip() for part in mode[6:].split(",") if part.strip()]
    if paths is not None:
        row = {}
        for path in paths:
            found = _values_at_path(record, path)
            value = found[0] if len(found) == 1 else found if found else None
            row[path] = _json_cell(value) if isinstance(value, (dict, list)) else _scalar_cell(value)
        return [row]
    return _flatten_value(record, "", 0, settings, path_prefix)


def run_conversion(
    source: Path, target: Path, settings: dict[str, Any], *, dry_run: bool = False, verbose: bool = False
) -> list[str]:
    settings = validate_settings(settings)
    if settings.get("input_path") and source.suffix.lower() in (".ndjson", ".jsonl"):
        raise ConverterError("input_path applies to JSON documents; NDJSON records are already selected.")
    array_path, single_root_object = (None, False)
    if source.suffix.lower() not in (".ndjson", ".jsonl"):
        array_path, single_root_object = resolve_record_array(source, settings)
    settings = settings.copy()
    columns = settings.get("columns")
    if columns is None and isinstance(settings["flatten"], str) and settings["flatten"].startswith("paths:"):
        columns = [part.strip() for part in settings["flatten"][6:].split(",") if part.strip()]
    if columns is None:
        columns = []
        known: set[str] = set()
        record_path = "" if single_root_object else f"{array_path}.*" if array_path else "*"
        for record in iter_records(source, settings, array_path, single_root_object):
            for row in flatten_record(record, settings, record_path):
                for name in row:
                    if name not in known:
                        known.add(name)
                        columns.append(name)
        if settings["column_order"] == "sorted":
            columns.sort()
        elif settings["column_order"] != "first_seen":
            raise ConverterError("column_order must be 'sorted' or 'first_seen'.")
    else:
        columns = list(columns)
    if dry_run:
        return columns
    quoting = settings.get("quoting", csv.QUOTE_MINIMAL)
    target.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    row_count = 0
    with target.open("w", encoding=settings["encoding"], newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, quoting=quoting, extrasaction="ignore", lineterminator="\r\n")
        writer.writeheader()
        record_path = "" if single_root_object else f"{array_path}.*" if array_path else "*"
        for record in iter_records(source, settings, array_path, single_root_object):
            for row in flatten_record(record, settings, record_path):
                writer.writerow(row)
                row_count += 1
                if verbose and row_count % 10000 == 0:
                    elapsed = time.monotonic() - started
                    print(f"{source}: {row_count} rows, {elapsed:.1f}s", file=os.sys.stderr, flush=True)
    if verbose:
        elapsed = time.monotonic() - started
        print(f"{source}: complete, {row_count} rows, {elapsed:.1f}s", file=os.sys.stderr)
    return columns
