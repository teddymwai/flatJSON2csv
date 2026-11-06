# 02. Iconography & Strict Zero-Emoji Mandate

## 1. The Strict Zero-Emoji Rule

- **Policy:** Never use emojis in user interface labels, navigation items, buttons, state indicators, cards, or decorative headers.
- **Why:** Emojis create an amateurish, playful, or "AI-slop" impression that undermines the executive, high-craft brand of **flatJSON2csv**. They render inconsistently across operating systems and clash with dark-mode contrast.

---

## 2. Google Fonts Material Symbols

All iconography must draw exclusively from **Google Fonts Icons / Material Symbols**:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

### Optical Treatment & Sizing Rules
1. **Consistent Sizing:**
   - Small inline actions / badges: `14px` or `16px`
   - Default toolbar / button icons: `16px` or `18px`
   - Header / section leading icons: `20px`
2. **Stroke Weight:** Standard `1.5px`–`2px` stroke weight (`wght@400` or `opsz@20,wght@400`).
3. **Monochrome Tinting:** Icons inherit text or state role color (`#9bb1a4` for secondary, `#f0f6f2` for active, `#2ea043` for success). Never give icons arbitrary multicolored backgrounds.
4. **Alignment:** Vertically and optically centered with paired text (`vertical-align: middle;`).
