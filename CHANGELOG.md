# Changelog

## [1.1.1] - 2026-11-13 (Directory Architecture & Tool-Role Renaming)

### Added
- **Dedicated Sub-Directories:**
  - `samples/`: Centralized real-world sample datasets (`cyberec_scenario.json`, `iev2_cloudtemplates_1114.json`, `iev3_cloudtemplates_616.json`) and converted reference CSV outputs with `samples/README.md`.
  - `tests/`: Organized test suite into standard `tests/` directory with `tests/__init__.py` and dynamic sample path resolution.
  - `docs/`: Relocated technical data specification into `docs/SCHEMA.md`.
- **Offline PWA Cache Update:** Bumped Service Worker cache to `flatJSON2csv-v6` caching both `./index.html` and `./unnest_studio.html`.

### Changed
- **Renamed Web Entry to Tool-Role Format (`unnest_studio.html`):** Renamed root `index.html` to `unnest_studio.html` following `<tool>_<role>.html` conventions to clearly showcase its role as the Unnest Web Studio.
- **Root Directory Cleanup:** Cleaned loose sample data files from the repository root, keeping only essential project root configuration, modules, and documentation.


## [1.1.0] - 2026-11-13 (Unnest Studio Architecture Redesign)

### Added
- **Project Rebrand to Unnest Studio:** Rebranded project and interface to **Unnest Studio** with official tagline: *"The local, privacy-first JSON to tabular studio."*
- **Integrated IDE Telemetry Status Bar:** Re-engineered the middle 80px telemetry cards into an ultra-quiet bottom IDE status bar (`#status-bar`) displaying input filename/size, records processed, column width, rows/sec speed, and client-side security status.
- **In-Table Real-Time Column Filter:** Added live column filter input (`#col-filter-input`) in the preview toolbar allowing real-time searching across wide schemas.
- **Author & Social Network Links:** Added verified links in the architectural guidance footer for:
  - *ted thought this was functional & fancy*
  - GitHub (`https://github.com/teddymwai/flatJSON2csv`)
  - GitLab (`https://gitlab.com/teddymwai`)
  - Twitter/X (`https://x.com/teddymwai`)
  - Instagram (`https://instagram.com/teddymwai`)
  - LinkedIn (`https://linkedin.com/in/teddymwai/`)
- **Dual CLI Command Support:** Added `unnest` command script entrypoint in `pyproject.toml` alongside `flatJSON2csv`.

### Fixed
- **Single-Row Header Layout (100% Zoom):** Eliminated awkward second-row wrapping where `Air-Gap HTML` and timer were pushed off-row on standard laptops and 1080p displays. Re-architected header into a two-sided Quiet Chrome layout fitting screens from 800px upwards without wrapping.
- **Workspace Canvas Recovery:** Gained 80px of vertical viewing area for the data table and configuration sidebar by removing the middle telemetry card band.
- **Service Worker Cache:** Bumped PWA service worker cache identifier to `flatJSON2csv-v5`.

---

## [1.0.0] - 2026-11-13 (Production Architecture Release)

### Added
- **Interactive Tooltip System:** Added responsive, accessible tooltips across all controls, flattening depth options, array strategies, action buttons, table columns, and meters with keyboard focus and hover support.
- **Architectural Guidance Footer:** Integrated a luxury forest guidance and reference documentation section beneath the workspace explaining:
  - What JSON flattening achieves when transforming hierarchical tree structures into 2D rectangular tables.
  - Flattening depth decisions and trade-offs (`none`, `depth:1`, `depth:2`, `full`).
  - Comparative analysis of array handling strategies (`compact`, `columns`, `join`, `explode`) and cartesian multiplication safeguards.
  - Air-gapped privacy guarantees and CLI parity.
- **Dynamic Feedback & Error Cards:** Added loading spinner and real-time status reporting during file ingestion, along with graceful in-place error diagnostics replacing native browser alerts.
- **Global Drag & Drop:** Added window-level drag-and-drop listener allowing users to drop JSON/NDJSON files anywhere on the application viewport.
- **CLI `-v` / `--version` Flag:** Added standard version inspection reporting `Unnest Studio 1.0.0 (flatJSON2csv)`.

### Fixed
- **File Upload & Preview Ingestion:** Fixed issue where uploaded JSON files failed to render in the preview table by:
  - Moving the hidden `<input type="file">` outside the clickable dropzone to prevent duplicate event bubbling.
  - Clearing `fileInput.value` immediately after file selection to allow selecting the same file repeatedly.
  - Automatically activating the "Table Preview" tab upon file or paste load so converted records are immediately visible.
  - Wrapping asynchronous conversion loops in robust `try ... catch ... finally` blocks guaranteeing that conversion lock states (`isConverting`) and button disabled states are always released.
- **Smart Envelope Array Detection:** Upgraded candidate array discovery to prioritize the largest record array count over shallow auxiliary arrays (e.g. `data.content` with 1,114 items taking precedence over shallow `warnings` or `sort` singletons).
- **Service Worker Cache:** Bumped PWA service worker cache identifier to `flatJSON2csv-v4` for immediate client cache invalidation.

### Previous Fixes & Improvements
- Added Python built-in `json` module fallback for zero-dependency execution when `ijson` is not installed.
- Fixed primitive array handling (e.g. `[1, 2, 3]`) by mapping them into a clean `value` column.
- Fixed multiline YAML templates breaking CSV records by replacing embedded newlines with spaces.
- Increased CSV field size limits to support cells larger than 128 KB.
- Added direct paste tab, global `Cmd+V` / `Ctrl+V` shortcut, toolbar copy/download actions, and reset state.
