"""flatJSON2csv: ted thought this was functional & fancy

Local, streaming JSON and NDJSON to CSV converter designed for sensitive,
deeply nested datasets.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from converter import ConverterError, discover_inputs, load_config, run_conversion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flatJSON2csv",
        description="flatJSON2csv — ted thought this was functional & fancy\nLocal, streaming JSON and NDJSON to CSV converter for sensitive datasets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="JSON/NDJSON file, glob, or directory (optional with --web)")
    parser.add_argument("-o", "--output", help="CSV file or output directory (required unless using --web)")
    parser.add_argument(
        "--web",
        nargs="?",
        const=8765,
        type=int,
        help="Launch the local web GUI server on 127.0.0.1 (default port: 8765)",
    )
    parser.add_argument("--config", help="JSON configuration file")
    parser.add_argument("--input-path", help="Array path inside a top-level object, e.g. data.results")
    parser.add_argument("--flatten", help="none, depth:N, full, or paths:a.b,c.d (default: depth:2)")
    parser.add_argument(
        "--array-strategy",
        choices=("explode", "columns", "json", "join"),
        help="Strategy for arrays: json (default), columns, join, or explode",
    )
    parser.add_argument("--array-cap", type=int, help="Maximum columns for 'columns' strategy (default: 10)")
    parser.add_argument("--array-delimiter", help="Delimiter for 'join' strategy (default: '; ')")
    parser.add_argument(
        "--allow-cartesian",
        action="store_true",
        default=None,
        help="Allow Cartesian product row expansion when exploding multiple arrays",
    )
    parser.add_argument("--columns", help="Comma-separated paths to select in order (skips discovery pass)")
    parser.add_argument("--override", action="append", help="JSON override object for specific paths; repeatable")
    parser.add_argument(
        "--column-order",
        choices=("sorted", "first_seen"),
        help="Column ordering: sorted alphabetically (default) or first_seen",
    )
    parser.add_argument("--quote", choices=("minimal", "all"), help="CSV quoting: minimal (default) or all")
    parser.add_argument("--encoding", help="File encoding (default: utf-8)")
    parser.add_argument("--verbose", action="store_true", help="Report row progress and elapsed time to stderr")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover and display columns only; do not write CSV output",
    )
    return parser


def launch_web(port: int = 8765) -> int:
    import http.server
    import socketserver
    import webbrowser

    web_dir = Path(__file__).resolve().parent / "web"
    if not web_dir.exists():
        web_dir = Path(__file__).resolve().parent

    class LocalHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(web_dir), **kwargs)

        def log_message(self, format, *args):
            pass  # Keep loopback server quiet

    url = f"http://127.0.0.1:{port}"
    print(f"flatJSON2csv: launching local web GUI at {url}")
    print("Zero network telemetry · 100% in-browser processing")
    print("Press Ctrl+C to stop server.")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        with socketserver.TCPServer(("127.0.0.1", port), LocalHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nflatJSON2csv web GUI stopped.")
        return 0
    except OSError as err:
        print(f"flatJSON2csv: could not bind to port {port}: {err}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.web is not None:
        return launch_web(args.web)

    if not args.input or not args.output:
        parser.error("the following arguments are required: input, -o/--output (or use --web)")

    try:
        settings = load_config(args.config)
        overrides = {
            "input_path": args.input_path,
            "flatten": args.flatten,
            "array_strategy": args.array_strategy,
            "array_cap": args.array_cap,
            "array_delimiter": args.array_delimiter,
            "allow_cartesian": args.allow_cartesian,
            "column_order": args.column_order,
            "quoting": {"minimal": csv.QUOTE_MINIMAL, "all": csv.QUOTE_ALL}.get(args.quote),
            "encoding": args.encoding,
        }
        if args.columns is not None:
            overrides["columns"] = [part.strip() for part in args.columns.split(",") if part.strip()]
        if args.override:
            overrides["overrides"] = [json.loads(value) for value in args.override]
        for key, value in overrides.items():
            if value is not None:
                settings[key] = value

        inputs = discover_inputs(args.input)
        output = Path(args.output).expanduser()
        multiple = len(inputs) > 1 or (len(inputs) == 1 and inputs[0].parent.is_dir() and Path(args.input).is_dir())
        if multiple and not args.dry_run:
            output.mkdir(parents=True, exist_ok=True)

        for source in inputs:
            target = output / f"{source.stem}.csv" if multiple else output
            if target.exists() and target.is_dir():
                target = target / f"{source.stem}.csv"
            columns = run_conversion(
                source, target, settings, dry_run=args.dry_run, verbose=args.verbose
            )
            print(f"{source}: {len(columns)} columns", file=sys.stderr if args.dry_run else sys.stdout)
            if args.dry_run:
                for column in columns:
                    print(column)
        return 0
    except (ConverterError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"flatJSON2csv: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
