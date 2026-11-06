# Apple HIG Components Modular Blueprint

Source Reference: [Apple Human Interface Guidelines - Components](https://developer.apple.com/design/human-interface-guidelines/components)

Use this blueprint to expand the **flatJSON2csv** UI component library with modular specifications mirroring Apple's 8 official HIG Component categories.

## 1. Directory Architecture for Multi-Component Expansion

```text
docs/ui-mantra/04-apple-hig-components/
├── blueprint.md                              # This master expansion roadmap
├── 01-content/
│   ├── charts.md
│   ├── collections.md
│   ├── image-views.md
│   └── web-views.md
├── 02-layout-and-organization/
│   ├── boxes.md
│   ├── disclosure-controls.md
│   ├── labels.md
│   ├── lists-and-tables.md
│   ├── lockups.md
│   ├── outline-views.md
│   ├── scroll-views.md
│   ├── split-views.md
│   └── tab-views.md
├── 03-menus-and-actions/
│   ├── activity-views.md
│   ├── buttons.md                            # Implemented
│   ├── context-menus.md
│   ├── dock-menus.md
│   ├── edit-menus.md
│   ├── home-screen-quick-actions.md
│   ├── menus.md
│   ├── ornaments.md
│   ├── pop-up-buttons.md
│   ├── pull-down-buttons.md
│   ├── the-menu-bar.md
│   └── toolbars.md
├── 04-navigation-and-search/
│   ├── navigation-bars.md
│   ├── path-controls.md
│   ├── search-fields.md
│   ├── sidebars.md
│   └── tab-bars.md
├── 05-presentation/
│   ├── action-sheets.md
│   ├── alerts.md
│   ├── page-controls.md
│   ├── panels.md
│   ├── popovers.md
│   ├── sheets.md
│   └── windows.md
├── 06-selection-and-input/
│   ├── color-wells.md
│   ├── combo-boxes.md
│   ├── date-pickers.md
│   ├── digit-entry-views.md
│   ├── image-wells.md
│   ├── pickers.md
│   ├── segmented-controls.md
│   ├── sliders.md
│   ├── steppers.md
│   ├── text-fields.md
│   └── toggles.md
├── 07-status/
│   ├── gauges.md
│   ├── activity-rings.md
│   ├── progress-indicators.md
│   └── rating-indicators.md
└── 08-system-experiences/
    ├── app-clips.md
    ├── complications.md
    ├── live-activities.md
    ├── notifications.md
    ├── top-shelf.md
    └── widgets.md
```

## 2. Apple HIG Component Categories Overview

| Category | Core Purpose | Priority Components to Author Next |
| :--- | :--- | :--- |
| **1. Content** | Display structured data, media, and rich visual layouts | `charts.md`, `collections.md`, `image-views.md` |
| **2. Layout & Organization** | Group, separate, and structure information hierarchies | `lists-and-tables.md`, `split-views.md`, `disclosure-controls.md`, `tab-views.md` |
| **3. Menus & Actions** | Initiate instantaneous actions or reveal contextual command sets | `buttons.md` *(Completed)*, `menus.md`, `pop-up-buttons.md`, `pull-down-buttons.md`, `toolbars.md`, `context-menus.md` |
| **4. Navigation & Search** | Move across app sections and filter/locate content | `sidebars.md`, `navigation-bars.md`, `tab-bars.md`, `search-fields.md` |
| **5. Presentation** | Display modal, transient, or auxiliary flows | `alerts.md`, `sheets.md`, `popovers.md`, `panels.md`, `windows.md` |
| **6. Selection & Input** | Capture user choices, values, and text entry | `toggles.md`, `segmented-controls.md`, `text-fields.md`, `pickers.md`, `sliders.md` |
| **7. Status** | Communicate determinate/indeterminate progress and metrics | `progress-indicators.md`, `gauges.md` |
| **8. System Experiences** | Integrate with OS-level surfaces and ambient glanceables | `notifications.md`, `widgets.md`, `live-activities.md` |

## 3. Standard Template for Future Component Specifications

Every new component Markdown file added to this directory must follow this 6-section structure:

1. **Component Identity & Anatomy**: Single-sentence definition of when to use the component vs. related controls.
2. **Ergonomics, Metrics, & Hit Targets**: Minimum hit areas (`44x44 pt` / `44x44 px`), padding, spacing, and alignment rules.
3. **Visual Hierarchy, States, & Materials**: Idle, Hover, Pressed, Focused, Selected, Disabled, and Liquid Glass / surface adaptation rules.
4. **Content, Labeling, & Keyboard Behavior**: Title/sentence capitalization rules, icon pairing (Google Fonts Icons / Material Symbols), and standard keyboard shortcuts (`Return`, `Space`, `Esc`, Arrow keys).
5. **Platform & Brand Adaptation (`flatJSON2csv`)**: Platform nuances and **flatJSON2csv** styling rules (`rgba(14, 63, 42, 1.00)`, zero emojis, high-contrast legibility).
6. **Anti-Patterns (Gotchas)**: Verifiable list of mistakes to reject during UI code generation or PR review.
