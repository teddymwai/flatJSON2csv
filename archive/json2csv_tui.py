"""Guided terminal interface for the local JSON to CSV converter (Archived Prototype)."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from converter import DEFAULTS, ConverterError, discover_inputs, load_config, run_conversion


def ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    return answer or default


def main() -> int:
    print("flatJSON2csv | Local JSON to CSV")
    print("Configure a local conversion. Press Return to keep each shown default.\n")
    try:
        config_file = ask("Config file (optional)")
        settings = load_config(config_file or None)
        input_spec = ask("Input file, glob, or directory")
        output_spec = ask("Output CSV file or directory")
        settings["input_path"] = ask("Input array path", settings["input_path"] or "") or None
        settings["flatten"] = ask("Flatten strategy", settings["flatten"])
        settings["array_strategy"] = ask("Array strategy (explode/columns/json/join)", settings["array_strategy"])
        settings["array_cap"] = int(ask("Array column cap", str(settings["array_cap"])))
        settings["array_delimiter"] = ask("Array join delimiter", settings["array_delimiter"])
        settings["allow_cartesian"] = ask(
            "Allow Cartesian expansion (yes/no)", "yes" if settings["allow_cartesian"] else "no"
        ).lower() in ("yes", "y", "true")
        settings["column_order"] = ask("Column order (sorted/first_seen)", settings["column_order"])
        settings["encoding"] = ask("Encoding", settings["encoding"])
        quote_default = "all" if settings["quoting"] == csv.QUOTE_ALL else "minimal"
        quote_mode = ask("CSV quoting (minimal/all)", quote_default)
        settings["quoting"] = {"all": csv.QUOTE_ALL, "minimal": csv.QUOTE_MINIMAL}[quote_mode]
        columns_text = ask("Explicit columns (comma-separated; blank for discovery)", ",".join(settings["columns"] or []))
        settings["columns"] = [item.strip() for item in columns_text.split(",") if item.strip()] or None
        overrides_text = ask("Path overrides as JSON array", json.dumps(settings["overrides"]))
        settings["overrides"] = json.loads(overrides_text)
        dry_run = ask("Discover columns only (yes/no)", "no").lower() in ("yes", "y", "true")
        verbose = ask("Verbose progress (yes/no)", "yes").lower() in ("yes", "y", "true")
        inputs = discover_inputs(input_spec)
        output = Path(output_spec).expanduser()
        multiple = len(inputs) > 1 or (len(inputs) == 1 and Path(input_spec).expanduser().is_dir())
        if multiple and not dry_run:
            output.mkdir(parents=True, exist_ok=True)
        for source in inputs:
            target = output / f"{source.stem}.csv" if multiple else output
            if target.exists() and target.is_dir():
                target = target / f"{source.stem}.csv"
            columns = run_conversion(source, target, settings, dry_run=dry_run, verbose=verbose)
            print(f"\n{source}: {len(columns)} columns")
            if dry_run:
                for column in columns:
                    print(f"  {column}")
        return 0
    except (ConverterError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"flatJSON2csv-tui: {exc}", file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nConversion cancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

