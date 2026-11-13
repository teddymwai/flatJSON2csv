# Release Notes: Unnest Studio v2.1.0 (Codename: Strigops)

**Release Date:** November 13, 2026  
**Codename:** Strigops  
**Stage:** General Availability (GA)  
**Architect:** `@teddymwai`

---

## Executive Summary

Unnest Studio **v2.1.0** introduces a high-performance **Interactive Hierarchical JSON Tree Explorer** designed to inspect, fold, and cross-reference deeply nested JSON datasets directly inside the browser with zero network transmission.

Building on top of the v2.0.0 architecture (native `.xlsx` exports & online JSON beautifier), v2.1.0 fulfills the vision of a truly tactile JSON inspection workflow: users can hide and unhide objects per hierarchy level, expand or collapse specific branches, and click on any word or token to illuminate all matching occurrences across the dataset with automatic ancestor unrolling.

---

## What's New in v2.1.0

### 1. Interactive Hierarchical JSON Tree Explorer
- **Dedicated Results Tab:** Integrated seamlessly as the 4th tab (`JSON Explorer`) in `#results-stage` alongside Table Preview, Column Schema, and Raw CSV.
- **Fast Jump Shortcut:** Direct `[ Explore Tree ↗ ]` action button embedded inside the `#paste-input-wrapper` beautifier toolbar for immediate 1-click inspection from raw pasted text.
- **Micro-Node Rendering:** Custom virtualized node builder (`buildTreeHtml`) rendering keys, values, brackets, and element count badges (`X keys`, `Y items`) with sub-millisecond execution times.

### 2. Multi-Level Object Folding & Unfolding
- **Level-Specific Controls:** Dedicated toolbar buttons to fold the dataset to uniform structural depths:
  - **Expand All:** Recursively unfolds all nodes across the entire document.
  - **Level 1:** Folds all nested objects below root depth 1.
  - **Level 2:** Folds all nested objects below depth 2.
  - **Level 3:** Folds all nested objects below depth 3.
  - **Collapse All:** Folds all branches to immediate top-level structures.
- **Granular Branch Toggling:** Interactive Material Symbols chevrons on every object and array node allowing 0ms instant branch folding with CSS-accelerated rotation transitions.

### 3. Word & Token Click-to-Highlight Engine
- **Instant Token Illuminator:** Clicking on any word inside object keys, string values, numbers, or booleans instantly highlights every matching occurrence across the entire tree.
- **Auto-Ancestor Unfolding:** If matching occurrences reside inside currently collapsed branches, the engine automatically traverses the DOM hierarchy and uncollapses the parent branches so matches are immediately visible.
- **Champagne Match Badge:** Displays a glowing capsule badge with exact match counts (e.g., `2 matches for "water"`), an active indicator, and a dismiss `✕` button.
- **Real-Time Word Search:** Dedicated search input in the tree toolbar allowing ad-hoc substring queries and highlighting.
- **Quick Dismiss:** Keyboard `Escape` or badge `✕` click instantly clears highlights and resets the view.

---

## Design System & Theme Alignment
- **Palette Continuity:** Highlighting styled using champagne luminescence (`rgba(230, 201, 143, 0.45)`, `#ffffff` text, box-shadow glow) strictly conforming to the Forest Luxury palette.
- **Zero-Emoji Policy:** Material Symbols Outlined exclusively (`account_tree`, `unfold_more`, `unfold_less`, `highlight`, `search`).
- **Snug Monospace Typography:** Natural character spacing with zero artificial letter gaps.

---

## Verification & Quality Assurance
- **Browser Automation Verification:** Verified via Chrome DevTools MCP:
  - Level 1 / Level 2 / Expand All / Collapse All state transitions tested.
  - Word-click token selection, match counting, and ancestor unrolling tested.
  - Direct jump navigation from the Beautifier toolbar tested.
- **Unit Test Suite:** 12/12 passing Python CLI tests in `tests/test_flatjson.py`.
- **Syntax Validation:** 100% valid JavaScript compilation verified via Node.js runtime check.
