# flatJSON2csv

> *ted thought this was functional & fancy*

A local, streaming command-line tool for converting large JSON and NDJSON files to deterministic CSV. Built specifically for sensitive datasets where data cannot leave the local machine, `flatJSON2csv` ingests records incrementally with `ijson` and never loads the entire document into memory.

The converter operates in a streaming, two-pass model:
1. **Pass 1 (Discovery):** Streams the input to identify all unique flattened columns across all records and orders them deterministically.
2. **Pass 2 (Writing):** Streams the input again to write CSV rows with standard `csv.DictWriter`.

Passing explicit columns via `--columns` skips Pass 1 entirely, streaming directly to disk. Memory usage remains bounded by the single largest record rather than the overall file size.

Line breaks inside cell values are replaced with spaces in CSV output so each record stays on one physical line for line-oriented readers. This applies to both the CLI and browser converter.

---

## Requirements and Installation

- Python 3.11 or newer
- `ijson` 3.x (sole runtime dependency)

Install locally in editable mode:

```sh
python -m pip install -e .
```

Or run directly with Python:

```sh
python flatJSON2csv.py input.json -o output.csv
```

---

## Web GUI (Local & GitHub Pages)

`flatJSON2csv` includes a self-contained, client-side web application inspired by the `ui-mantra/` design specifications. It runs with zero data exfiltration: all parsing, flattening, and CSV generation occur purely in-browser via JavaScript.

### 1. Launching Locally via CLI

```sh
# Start loopback server and open default browser at http://127.0.0.1:8765
flatJSON2csv --web

# Or specify a custom port
flatJSON2csv --web 9000
```

You can also simply open `flatJSON/web/index.html` directly in any browser (`file:///...`).

### 2. Deploying Online via GitHub Pages

Because the web interface is 100% client-side with zero backend dependencies, it is ready for instant deployment to GitHub Pages:
- The hosted app is published from `web/` by the GitHub Actions workflow.
- After deployment, open <https://teddymwai.github.io/flatJSON2csv/>.

When deployed to `https://<username>.github.io/<repo>/`, users can drop sensitive JSON files directly into their browser. **Input data stays in the browser and is never uploaded**—the conversion executes entirely on the user's local CPU.

---

## Usage (CLI)

### Single File

```sh
flatJSON2csv response.json -o response.csv
```

### Directory or Glob (Batch Mode)

```sh
# All JSON/NDJSON files in a directory
flatJSON2csv exports/ -o converted/

# Recursive glob
flatJSON2csv 'exports/**/*.json' -o converted/
```

### Inspect Schema Without Writing (`--dry-run`)

```sh
flatJSON2csv response.json -o unused.csv --dry-run
```
Discovers all columns and prints them to `stdout` along with the column count, without writing a CSV file to disk.

### Explicit Array Selection (`--input-path`)

For top-level JSON objects containing enveloped data (e.g., `{"status":"ok", "data":{"items":[...]}}`):

```sh
flatJSON2csv api_response.json -o output.csv --input-path data.items
```

If `--input-path` is omitted for a top-level object, `flatJSON2csv` automatically locates the shallowest object array.

---

## Flattening Strategies

Configurable via `--flatten` (default: `depth:2`):

- `none`: Top-level keys only; nested objects/arrays serialize as compact JSON strings.
- `depth:N`: Expand nested objects up to N levels deep; deeper levels become JSON strings.
- `full`: Expand all nested objects with dot-separated column names (e.g. `user.profile.address.city`).
- `--columns col1,col2`: Extract only specified paths in exact order, skipping column discovery.

```sh
flatJSON2csv input.json -o out.csv --flatten depth:3
flatJSON2csv input.json -o out.csv --columns id,user.name,status
```

---

## Array Handling Strategies

Configurable via `--array-strategy` (default: `json`):

- `json`: Compact JSON string in a single cell (safe, deterministic, zero row multiplication).
- `columns`: Expand array elements into indexed columns (`tags_0`, `tags_1`) up to `--array-cap` (default 10).
- `join`: Join scalar items with `--array-delimiter` (default `; `).
- `explode`: Emit a new CSV row per array element. Use `--allow-cartesian` if multiple arrays are exploded simultaneously.

```sh
flatJSON2csv input.json -o out.csv --array-strategy join --array-delimiter " | "
flatJSON2csv input.json -o out.csv --array-strategy columns --array-cap 5
flatJSON2csv input.json -o out.csv --array-strategy explode --allow-cartesian
```

---

## CLI Options

| Flag | Description | Default |
|---|---|---|
| `input` | Path to JSON/NDJSON file, glob pattern, or directory | *Required* |
| `-o, --output` | Output CSV file or directory | *Required* |
| `--config` | Path to JSON configuration file | `None` |
| `--input-path` | Dot-separated path to record array inside top-level object | Auto-detected |
| `--flatten` | Flattening mode: `none`, `depth:N`, `full` | `depth:2` |
| `--array-strategy` | Array handling: `json`, `columns`, `join`, `explode` | `json` |
| `--array-cap` | Column limit for `columns` strategy | `10` |
| `--array-delimiter` | Separator for `join` strategy | `; ` |
| `--allow-cartesian` | Opt in to multi-array Cartesian row explosion | `False` |
| `--columns` | Comma-separated paths to select (skips Pass 1) | Auto-discovered |
| `--override` | JSON string defining per-path overrides (repeatable) | `[]` |
| `--column-order` | Column ordering: `sorted` or `first_seen` | `sorted` |
| `--quote` | CSV quoting style: `minimal` or `all` | `minimal` |
| `--encoding` | Text encoding for input and output | `utf-8` |
| `--verbose` | Output row progress and elapsed time to `stderr` | `False` |
| `--dry-run` | Run discovery only and print columns without writing CSV | `False` |

---

## Privacy & Local-Only Guarantees

- Input files are parsed and converted entirely in the browser and are never uploaded.
- The hosted interface loads its icon font stylesheet from Google Fonts; input data is not included in that request.
- No telemetry, analytics, or update checks.
- Streaming architecture prevents memory exhaustion on large datasets.

---

## Design System & Future Interfaces

The design tokens and interface standards in [`ui-mantra/`](ui-mantra/README.md) define the visual language (typography, dark forest palette, Apple HIG geometry, and zero-emoji mandate) for upcoming web and online interfaces for `flatJSON2csv`.
