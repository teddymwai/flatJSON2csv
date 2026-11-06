# Performance Benchmarks

One user-provided API response has been measured. Timing includes a fresh Python process and the complete conversion command; peak RSS is the child process maximum reported by macOS `resource.getrusage` (bytes on this platform). Results are environment-specific.

When representative small, medium, and large files are available, record:

| Sample | Input size | Shape | Rows | Elapsed time | Peak RSS | Machine / Python |
|---|---:|---|---:|---:|---:|---|
| `iev3_cloudtemplates_616.json` | 15.3 MiB | API object with `data.content` array | 616 | 0.859 s | 27.7 MiB | macOS, Python 3.15.2, ijson 3.6.0 |
| Small | Pending | Pending | Pending | Pending | Pending | Pending |
| Large | Pending | Pending | Pending | Pending | Pending | Pending |

The 20MB, 100MB, and 433MB target sizes are not represented yet. Only one medium sample is available for this measurement; small/large runs and target-size validation remain pending.
