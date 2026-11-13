# Changelog

## Unreleased

### Fixed
- Fixed CLI failure on standard environments lacking `ijson` by adding an automatic fallback to Python's built-in `json` module, allowing local conversion with zero third-party dependencies.
- Fixed sticky stale `input-path` state in the Web GUI that silently broke conversion of subsequent files after loading an enveloped dataset or demo sample.
- Fixed conversion of primitive arrays (e.g. `[1, 2, 3]` or `["a", "b"]`) in both CLI and Web GUI by assigning them to a clean `value` column instead of throwing errors or empty headers.
- Fixed CLI `--dry-run` and single file conversion requiring `-o` (now defaults to `<input>.csv` for single files and skips `-o` requirement for dry runs).

### Improved
- Added direct "Paste JSON" textarea tab in the Web GUI to allow pasting raw JSON/NDJSON directly from clipboard, matching konklone.io and convertcsv.com workflows.
- Added global `Cmd+V` / `Ctrl+V` paste shortcut to load JSON from clipboard anywhere on the Web GUI.
- Added instant live preview (table view and raw CSV) upon file drop or text paste without requiring an immediate download click.
- Added one-click "Copy CSV" and "Download CSV" actions in the results toolbar.
- Added "Reset" button to cleanly clear all inputs, meters, and tables.
- Replace embedded line breaks in CSV cell values with spaces in both CLI and browser exports, keeping each record on one physical line for line-oriented readers.
- Delay revoking browser download URLs so generated CSV files have time to download reliably.
- Refresh the service worker cache version so clients load the updated converter.

### Planned
- Cleaner titles after conversion by removing the metadata structure.
- A more guided interface that explains what each option does.
- A more stable user experience.
