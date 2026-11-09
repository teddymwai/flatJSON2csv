# Changelog

## Unreleased

### Improved
- Replace embedded line breaks in CSV cell values with spaces in both CLI and browser exports, keeping each record on one physical line for line-oriented readers.
- Delay revoking browser download URLs so generated CSV files have time to download reliably.
- Refresh the service worker cache version so clients load the updated converter.

### Planned
- Cleaner titles after conversion by removing the metadata structure.
- A more guided interface that explains what each option does.
- A more stable user experience.
