# Changelog

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
- **CLI `-v` / `--version` Flag:** Added standard version inspection reporting `flatJSON2csv 1.0.0`.

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
