# 03. UI Unslop Methodology

Based on the unslopping design architecture, every interface in **flatJSON2csv** is designed with clear character, calm structure, and high legibility.

---

## 1. Core Principles

1. **Quiet Chrome:**
   - Navbars, sidebars, headers, cards, and borders must stay calm and understated. Chrome serves to frame content, not compete with it.
2. **One Bright Element:**
   - Each view highlights one deliberate focal point (for example: an interactive resource gauge, an active execution graph, or the primary telemetry meter).
   - Avoid spreading rainbow colors across every component.
3. **Strict 4px Grid Rhythm:**
   - All spatial dimensions—paddings, margins, gaps, line heights, and icon sizes—must be multiples of 4:
     `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`, `48px`, `64px`.
   - Arbitrary pixel values (such as `13px`, `27px`, `7px`) are prohibited.
4. **Elimination of AI-Slop Tells:**
   - No purple, violet, or cyan glowing backgrounds.
   - No neon outer glow drop-shadows.
   - No gradient text or rainbow gradient fills.
   - No arbitrary glossy bubble blobs or heavy frosted glass.
   - No excessive uppercase tracked shouting labels.
   - No pulsing badges or bouncing badges.

---

## 2. Nine-Pass Execution Order

When reviewing, designing, or refactoring a screen, apply changes in this strict sequential order:

1. **Spacing:** Align all padding, margins, and gaps to the 4px grid.
2. **Color:** Ground the view in deep obsidian/emerald neutrals; establish one bright focal point.
3. **Icons:** Replace any emojis with consistent Google Fonts Material Symbols.
4. **Copy:** Eliminate hype and verbose AI phrasing; use crisp, verb-led labels.
5. **Typography:** Establish clean type hierarchy, optical weights, and high WCAG contrast.
6. **Layout:** Structure clear visual containers without nesting excessive cards.
7. **Details:** Add hairline borders (`1px solid rgba(14, 63, 42, 0.45)`), subtle hover states.
8. **Visuals:** Add clean telemetry meters, structured tables, and crisp indicators.
9. **Motion:** Restrained, purposeful micro-transitions (`120ms`–`150ms` cubic-bezier; respect `prefers-reduced-motion`).
