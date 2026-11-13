# Sample Datasets & Conversion Outputs

This directory contains real-world, production-scale JSON datasets used for benchmarking, stress-testing, and regression validation of **Unnest Studio** (`flatJSON2csv`).

---

## Datasets Overview

| Filename | File Size | Records | Description / Structure |
|---|---|---|---|
| `cyberec_scenario.json` | ~5.1 MiB | 1,050 | Cyber security incident scenario object containing enveloped arrays, deeply nested network logs, and multi-level attributes (39 flattened columns). |
| `iev2_cloudtemplates_1114.json` | ~19.8 MiB | 1,114 | Cloud infrastructure template metadata with extensive configuration trees, policy maps, and template parameters (37 flattened columns). |
| `iev3_cloudtemplates_616.json` | ~15.3 MiB | 616 | Complex enterprise cloud templates with nested resource mappings and array attributes under `data.content` (35 flattened columns). |

---

## Converted Output References

- `iev3-616.csv` (~13.3 MiB): Deterministic CSV output generated from `iev3_cloudtemplates_616.json` with Cartesian array expansion.
- `iev3.csv` (~13.3 MiB): Baseline reference CSV conversion.

---

> [!NOTE]
> Large sample data files (`*.json` and `*.csv`) in this directory are excluded from version control via `.gitignore` to keep repository clone sizes compact.
