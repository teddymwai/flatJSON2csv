# Unnest Studio Release Notes (v2.0.0)

> **Release Version:** `v2.0.0`  
> **Codename:** `Strigops`  
> **Tag Identifier:** `Strigops_v2.0.0` / `v2.0.0`  
> **Stage:** `GA (Production)`  
> **Target Environments:** Modern Web Browsers (Web, PWA, Airgap HTML) & Python 3.11+ Environments  
> **Release Date:** 2026-11-13  
> **Owner / Author:** Ted Mwai (@teddymwai)  

---

## 1. Executive Summary

The `v2.0.0` (`Strigops`) major release transforms **Unnest Studio** (`flatJSON2csv`) from a CSV converter into a comprehensive, multi-format tabular data engineering and inspection studio.

Key milestones delivered in this release:
1. **Zero-Dependency Native `.xlsx` Engine:** Generates valid, multi-column OpenXML Microsoft Excel workbooks directly in-browser using pure vanilla JavaScript and a micro-ZIP builder. Zero external scripts or network calls required, guaranteeing 100% offline air-gap compatibility.
2. **CLI Streaming Excel Exports:** Added direct `.xlsx` output streaming in Python via `openpyxl.Workbook(write_only=True)`, enabling bounded memory usage when exporting multi-gigabyte datasets directly to Excel.
3. **Online JSON Editor & Beautifier Suite:** Integrated interactive JSON formatting (2-space indentation), compact minification, and real-time syntax error coordinate pinpointing (`Line X, Col Y`) directly into the input workspace.
4. **Production v2.0.0 Interface Upgrades:** Updated status chrome, version pill badges (`v2.0.0 GA`), table quick-export actions, and bumped PWA service worker caching to `flatJSON2csv-v7`.

---

## 2. Core Subsystems & Architectural Changes

### A. Subsystem 1: In-Browser OpenXML `.xlsx` Generator
- **Location:** `unnest_studio.html`, `web/unnest_studio.html`, `web/index.html`
- **Methodology:**
  - Constructs OpenXML spreadsheet parts (`[Content_Types].xml`, `_rels/.rels`, `xl/_rels/workbook.xml.rels`, `xl/workbook.xml`, `xl/worksheets/sheet1.xml`).
  - Serializes parts into a standard Method 0 (STORE) ZIP container using native `Uint8Array`, `DataView`, and standard CRC32 checksums.
  - Automatically maps and converts cell types:
    - Clean integers and floats $\rightarrow$ numeric cells (`<c t="n"><v>...</v></c>`).
    - Booleans $\rightarrow$ native boolean cells (`<c t="b"><v>1|0</v></c>`).
    - Multiline text & XML special characters $\rightarrow$ inline escaped text strings with `xml:space="preserve"`.
  - Supports arbitrary column dimensions via algorithmic column-to-letter translation ($A \dots Z \dots AA \dots ZZ \dots AAA$).

### B. Subsystem 2: Streaming CLI `.xlsx` Pipeline
- **Location:** `converter.py`, `flatJSON2csv.py`
- **Flag & Inferences:**
  - `--format xlsx`: Forces `.xlsx` generation.
  - `-o output.xlsx`: Automatically triggers Excel output mode.
  - Omitted `-o` with `--format xlsx`: Automatically infers `<stem>.xlsx`.
- **Memory Safety:** Uses `openpyxl.Workbook(write_only=True)` to stream records row-by-row to disk without buffering the full document in RAM.

### C. Subsystem 3: Online JSON Beautifier & Diagnostic Suite
- **Location:** `unnest_studio.html` `#paste-input-wrapper`
- **Features:**
  - **Beautify:** Formats raw JSON with 2-space indentation and displays record tally.
  - **Minify:** Collapses whitespace and reports percentage space saved.
  - **Validate:** Analyzes structure (Array vs Object vs Primitive) and reports key count.
  - **Syntax Diagnostics:** Pinpoints exact error coordinates (`Line N, Col M`) from `SyntaxError` position offsets.

---

## 3. Verification & Evidence

- **Unit Test Suite:** 12/12 passing tests in `tests/test_flatjson.py` including `test_xlsx_export` and `test_cli_xlsx_format_flag`.
- **Spreadsheet Verification:** Generated spreadsheets verified via `openpyxl.load_workbook()` ensuring structural compliance, dimension accuracy (`A1:AM1051`), and exact cell value fidelity.
- **JavaScript Syntax:** 100% valid script compilation confirmed across all web distributions.
