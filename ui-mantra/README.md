# flatJSON2csv UI Mantra & Design System

This directory houses the foundational design principles, component specifications, brand palette guidelines, and iconography standards for **flatJSON2csv** interfaces, guides, web pages, and online tooling.

---

## 1. Pillars of the UI Mantra

1. **[01. Brand Identity & Palette](01-brand-identity-and-palette.md)**
   - Grounded in **`rgba(14, 63, 42, 1.00)`** (`#0e3f2a` / deep luxury forest green).
   - High-contrast obsidian/graphite dark surfaces (`#090d0b`, `#0d1310`, `#151f1a`).
   - WCAG AAA contrast typography (`#f0f6f2` primary copy).
   - Canonical name: **`flatJSON2csv`** | Tagline: *"ted thought this was functional & fancy"*

2. **[02. Iconography & Zero Emojis](02-iconography-and-zero-emojis.md)**
   - Strict **ZERO EMOJIS** policy across all UI elements, labels, buttons, cards, and headers.
   - **Google Fonts Material Symbols** exclusively (standard 16px–20px sizing, muted tinting).

3. **[03. UI Unslop Methodology](03-ui-unslop-methodology.md)**
   - Quiet Chrome: Navbars, sidebars, cards, and table borders remain calm and muted.
   - One Bright Element: Reserve vibrant accents for the primary focal point or metric.
   - Strict 4px Grid: All spacing, paddings, margins, gaps, and line heights follow multiples of 4 (4px, 8px, 12px, 16px, 20px, 24px, 32px, 48px).
   - Ban on AI-slop tells: No purple gradients, glowing borders, glossy blobs, or pulsing elements.

4. **[04. Apple HIG Component Foundation](04-apple-hig-components/buttons.md)**
   - Component geometry: **Capsule** (`border-radius: 9999px`) for standalone actions; **Rounded Rectangle** (`10px`–`12px`) for vertical stacks.
   - Ergonomics: Mandatory minimum interactive hit region of **`44x44 px`** (using `::after` targets).
   - Visual hierarchy: Differentiate importance through **Style Prominence** (`Prominent Filled`, `Tinted Glass`, `Plain`), never by mixing different button heights side by side.
   - Tactile feedback: Mandatory press state (`transform: scale(0.97)` on `:active`).

---

## 2. Directory Structure

```text
ui-mantra/
├── README.md                              # This document
├── 01-brand-identity-and-palette.md       # Color hierarchy, hex tokens, and contrast ratios
├── 02-iconography-and-zero-emojis.md      # Icon standards & strict zero-emoji mandate
├── 03-ui-unslop-methodology.md            # Quiet chrome, 4px rhythm, 9-pass execution
└── 04-apple-hig-components/               # Apple HIG Component specifications
    ├── blueprint.md                       # 8-category modular HIG expansion roadmap
    └── buttons.md                         # Button tokens, capsule rules, hit targets, CSS
```
