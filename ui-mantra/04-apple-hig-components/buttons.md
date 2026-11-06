# Apple HIG Buttons: Technical Specification & Implementation Tokens

Source Reference: [Apple Human Interface Guidelines - Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)

## 1. Button Size, Shape, and Hit-Target Matrix

| Size Tier | Control Height | Minimum Hit Region | Supported Shapes | Recommended Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Mini** | `28 pt` (`28 px`) | `44x44 pt` (`60x60 pt` visionOS) | Circular (`1:1`) | Dense inspector views; never stack vertically or align in horizontal rows |
| **Small** | `32 pt` (`32 px`) | `44x44 pt` (`60x60 pt` visionOS) | Circular, Capsule (text-only), Rounded Rect | Compact secondary view controls; avoid in primary stacks or rows |
| **Regular** | `44 pt` (`44 px`) | `44x44 pt` (`60x60 pt` visionOS) | Circular, Capsule (text / icon+text), Rounded Rect | Default size for dialogs, toolbars, forms, and inline actions |
| **Large** | `52 pt` (`52 px`) | `52x52 pt` (`60x60 pt` visionOS) | Circular, Capsule (text / icon+text), Rounded Rect | Primary hero CTAs, bottom sheets, and full-width mobile buttons |
| **Extra Large** | `64 pt` (`64 px`) | `68x68 pt` (`64 pt` + `4 pt` pad) | Circular (`1:1`) | Prominent spatial or media-transport controls |

## 2. Shape Selection Rules by Layout Context

| Layout Context | Content Type | Required Shape | Border Radius Token |
| :--- | :--- | :--- | :--- |
| **Standalone Action** | Text or Icon + Text | **Capsule** | `9999px` (pill) |
| **Horizontal Row of Buttons** | Text or Icon + Text | **Capsule** | `9999px` (pill) |
| **Vertical Stack of Buttons** | Text (1 or 2 lines) | **Rounded Rectangle** | `10px` - `12px` (continuous squircle) |
| **Icon-Only Toolbar / Floating Action** | Symbol / Icon Only | **Circular** | `50%` / `9999px` (`width == height`) |
| **View-Attached Table / List Action (macOS)** | Symbol Only (`+`, `-`, gear) | **Small Square** | `6px` (attached directly beneath or inside view) |
| **Contextual Help Trigger (macOS)** | Question Mark Symbol (`?`) | **Circular Help Button** | `50%` (`20pt-22pt` visual, `44pt` hit area, lower corner) |

## 3. Style Hierarchy and Role Mapping

| Style Tier | Semantic Role | Visual Treatment (Apple System) | Visual Treatment (flatJSON2csv Adaptation) | Max Per View |
| :--- | :--- | :--- | :--- | :--- |
| **Prominent (Filled)** | `Primary` | Solid system accent color fill, white/contrasting label, responds to `Return` | `rgba(14, 63, 42, 1.00)` (`#0E3F2A`) fill, `#FFFFFF` label, subtle top specular border | `1 - 2` |
| **Bordered / Tinted** | `Normal` | Translucent accent or neutral tint (`12-16%` alpha) with matching or neutral text | `rgba(14, 63, 42, 0.14)` fill, `1px solid rgba(14, 63, 42, 0.35)`, high-contrast text | Unlimited |
| **Liquid Glass / Material** | `Normal` / Toolbar | `backdrop-filter: blur(20px) saturate(180%)`, thin translucent surface fill | `rgba(255, 255, 255, 0.08)` over dark glass with `1px solid rgba(255, 255, 255, 0.16)` | Context-dependent |
| **Plain / Borderless** | `Cancel` / Inline | Transparent background at rest; subtle tint on `:hover` and `:active` | Transparent at rest; `rgba(255, 255, 255, 0.06)` hover surface | Unlimited |
| **Destructive** | `Destructive` | Tinted red surface at rest or solid system red (`#FF3B30` / `#FF453A`); **never** default `Primary` | `#B91C1C` / `#EF4444` semantic danger palette; never bound to default `Return` key | `1` per dialog |

## 4. Reference CSS / Web Component Tokens

```css
:root {
  /* flatJSON2csv + Apple HIG Hybrid Tokens */
  --btn-primary-bg: rgba(14, 63, 42, 1.00);
  --btn-primary-bg-hover: rgba(19, 82, 55, 1.00);
  --btn-primary-bg-active: rgba(10, 46, 31, 1.00);
  --btn-primary-fg: #FFFFFF;

  --btn-tinted-bg: rgba(14, 63, 42, 0.14);
  --btn-tinted-border: rgba(14, 63, 42, 0.32);
  --btn-tinted-fg: #E6F4ED;

  --btn-glass-bg: rgba(255, 255, 255, 0.10);
  --btn-glass-border: rgba(255, 255, 255, 0.18);
  --btn-destructive-bg: rgba(220, 38, 38, 0.16);
  --btn-destructive-fg: #FCA5A5;
  --btn-destructive-solid: #DC2626;

  --btn-height-mini: 28px;
  --btn-height-small: 32px;
  --btn-height-regular: 44px;
  --btn-height-large: 52px;
  --btn-radius-capsule: 9999px;
  --btn-radius-rect: 12px;
}

.hig-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: var(--btn-height-regular);
  min-width: 44px;
  padding: 0 18px;
  border-radius: var(--btn-radius-capsule);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
  font-size: 15px;
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.01em;
  text-decoration: none;
  white-space: nowrap;
  user-select: none;
  cursor: pointer;
  transition: transform 120ms cubic-bezier(0.2, 0, 0, 1),
              background-color 150ms ease,
              box-shadow 150ms ease,
              opacity 150ms ease;
}

/* Ensure 44x44px minimum hit region even on Mini/Small visual buttons */
.hig-btn::after {
  content: "";
  position: absolute;
  inset: min(0px, calc((var(--btn-height-regular) - 100%) / 2));
  min-width: 44px;
  min-height: 44px;
}

/* Mandatory Press State */
.hig-btn:active:not(:disabled) {
  transform: scale(0.975);
}

.hig-btn:focus-visible {
  outline: 2px solid #34D399;
  outline-offset: 2px;
}

.hig-btn:disabled,
.hig-btn[aria-disabled="true"] {
  opacity: 0.42;
  cursor: not-allowed;
  pointer-events: none;
}

@media (prefers-reduced-motion: reduce) {
  .hig-btn {
    transition: none;
  }
  .hig-btn:active:not(:disabled) {
    transform: none;
  }
}
```
