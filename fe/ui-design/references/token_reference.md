# Distyl AI Design System — Claude Reference Package
# Version 1.1 | February 2026
# Optimized for Claude ingestion. Use this file to generate token-compliant UI output.

---

## IDENTITY

- **Brand**: Distyl AI
- **Product fonts**: Lato (body/UI), Roboto Mono (code only)
- **Brand color**: Purple — `#5D4EE7` (purple/500)
- **Philosophy**: One canonical base, infinite branded forks. Customer themes override primitives only.
- **Architecture**: Three layers — Primitives → Semantic → Components. All references are aliases, never raw values in components.

---

## TOKEN ARCHITECTURE

### Layer 1 — Primitives (raw values, never use directly in components)

#### Purple Scale
| Token | Value |
|---|---|
| color/purple/50 | #EFEDFD |
| color/purple/100 | #DDD9FB |
| color/purple/200 | #BDB4F7 |
| color/purple/300 | #9D8EF3 |
| color/purple/400 | #7D69EF |
| color/purple/500 | #5D4EE7 ← BRAND PRIMARY |
| color/purple/600 | #4A3EBA |
| color/purple/700 | #382F8C |
| color/purple/800 | #251F5E |
| color/purple/900 | #131030 |
| color/purple/950 | #0A0818 |

#### Gray Scale
| Token | Value |
|---|---|
| color/gray/0 | #FFFFFF |
| color/gray/50 | #F9FAFB |
| color/gray/100 | #F3F4F6 |
| color/gray/200 | #E5E7EB |
| color/gray/300 | #D1D5DB |
| color/gray/400 | #9CA3AF |
| color/gray/500 | #6B7280 |
| color/gray/600 | #4B5563 |
| color/gray/700 | #374151 |
| color/gray/800 | #1F2937 |
| color/gray/900 | #111827 |
| color/gray/950 | #0F1117 |

#### Feedback Primitives
| Token | Value |
|---|---|
| color/green/50 | #F0FDF4 |
| color/green/100 | #DCFCE7 |
| color/green/500 | #22C55E |
| color/green/600 | #16A34A |
| color/green/700 | #15803D |
| color/red/50 | #FEF2F2 |
| color/red/100 | #FEE2E2 |
| color/red/400 | #F87171 |
| color/red/500 | #EF4444 |
| color/red/600 | #DC2626 |
| color/red/700 | #B91C1C |
| color/amber/50 | #FFFBEB |
| color/amber/100 | #FEF3C7 |
| color/amber/400 | #FBBF24 |
| color/amber/500 | #F59E0B |
| color/amber/600 | #D97706 |
| color/amber/700 | #B45309 |

#### Spacing (4px base unit)
| Token | Value |
|---|---|
| space/px | 1px |
| space/0-5 | 2px |
| space/1 | 4px |
| space/2 | 8px |
| space/3 | 12px |
| space/4 | 16px |
| space/5 | 20px |
| space/6 | 24px |
| space/8 | 32px |
| space/10 | 40px |
| space/12 | 48px |
| space/16 | 64px |

#### Border Radius
| Token | Value |
|---|---|
| radius/none | 0px |
| radius/sm | 4px |
| radius/md | 6px |
| radius/lg | 8px |
| radius/xl | 12px |
| radius/2xl | 16px |
| radius/full | 9999px |

#### Typography
| Token | Value |
|---|---|
| typography/family/body | Lato, sans-serif |
| typography/family/code | Roboto Mono, monospace |
| typography/size/xs | 12px |
| typography/size/sm | 14px |
| typography/size/base | 16px |
| typography/size/lg | 18px |
| typography/size/xl | 20px |
| typography/size/2xl | 24px |
| typography/size/3xl | 30px |
| typography/size/4xl | 36px |
| typography/weight/regular | 400 |
| typography/weight/medium | 500 |
| typography/weight/semibold | 600 |
| typography/weight/bold | 700 |
| typography/lineheight/tight | 1.25 |
| typography/lineheight/normal | 1.5 |
| typography/lineheight/relaxed | 1.75 |

---

### Layer 2 — Semantic (purpose-named, has Light and Dark modes)

#### Background
| Token | Light | Dark |
|---|---|---|
| color/background/default | color/gray/0 | color/gray/950 |
| color/background/subtle | color/gray/50 | color/gray/900 |
| color/background/secondary | color/gray/100 | color/gray/800 |
| color/background/accent | color/purple/50 | color/purple/900 |
| color/background/primary | color/purple/500 | color/purple/500 |
| color/background/inverse | color/gray/950 | color/gray/0 |
| color/background/danger | color/red/50 | color/red/950 |
| color/background/success | color/green/50 | color/green/950 |
| color/background/warning | color/amber/50 | color/amber/950 |

#### Text
| Token | Light | Dark |
|---|---|---|
| color/text/default | color/gray/950 | color/gray/50 |
| color/text/subtle | color/gray/500 | color/gray/400 |
| color/text/disabled | color/gray/300 | color/gray/600 |
| color/text/inverse | color/gray/0 | color/gray/950 |
| color/text/primary | color/purple/500 | color/purple/400 |
| color/text/danger | color/red/600 | color/red/400 |
| color/text/success | color/green/700 | color/green/500 |
| color/text/warning | color/amber/700 | color/amber/500 |

#### Border
| Token | Light | Dark |
|---|---|---|
| color/border/default | color/gray/200 | color/gray/700 |
| color/border/subtle | color/gray/100 | color/gray/800 |
| color/border/strong | color/gray/400 | color/gray/500 |
| color/border/primary | color/purple/500 | color/purple/400 |
| color/border/success | color/green/600 | color/green/500 |
| color/border/warning | color/amber/600 | color/amber/500 |
| color/border/danger | color/red/600 | color/red/500 |
| color/border/info | color/purple/300 | color/purple/400 |

#### Icon
| Token | Light | Dark |
|---|---|---|
| color/icon/default | color/gray/500 | color/gray/400 |
| color/icon/subtle | color/gray/300 | color/gray/600 |
| color/icon/primary | color/purple/500 | color/purple/400 |
| color/icon/inverse | color/gray/0 | color/gray/950 |

#### Feedback
| Token | Value |
|---|---|
| color/feedback/danger | color/red/500 |
| color/feedback/success | color/green/600 |
| color/feedback/warning | color/amber/500 |
| color/feedback/info | color/purple/400 |

---

### Layer 3 — Components (scoped, always reference semantic layer)

#### Button
| Token | Value |
|---|---|
| button/background/primary | color/background/primary |
| button/background/secondary | color/background/secondary |
| button/background/ghost | transparent |
| button/background/destructive | color/feedback/danger |
| button/text/primary | color/text/inverse |
| button/text/secondary | color/text/default |
| button/text/ghost | color/text/default |
| button/border/outline | color/border/default |
| button/border/focus | color/border/primary |
| button/radius | radius/md |

#### Input
| Token | Value |
|---|---|
| input/background/default | color/background/default |
| input/background/disabled | color/background/subtle |
| input/text/default | color/text/default |
| input/text/placeholder | color/text/subtle |
| input/border/default | color/border/default |
| input/border/focus | color/border/primary |
| input/border/error | color/border/danger |
| input/radius | radius/md |

#### Badge (semantic/status — non-interactive)
| Token | Value |
|---|---|
| badge/background/default | color/background/secondary |
| badge/background/primary | color/background/accent |
| badge/background/success | color/background/success |
| badge/background/warning | color/background/warning |
| badge/background/danger | color/background/danger |
| badge/text/default | color/text/subtle |
| badge/text/primary | color/text/primary |
| badge/text/success | color/text/success |
| badge/text/warning | color/text/warning |
| badge/text/danger | color/text/danger |
| badge/radius | radius/full |

#### Tag (non-interactive label)
| Token | Value |
|---|---|
| tag/background | color/background/secondary |
| tag/text | color/text/subtle |
| tag/border | color/border/default |
| tag/radius | radius/sm |

#### Chip (interactive filter/toggle)
| Token | Value |
|---|---|
| chip/background/default | color/background/default |
| chip/background/selected | color/background/primary |
| chip/text/default | color/text/subtle |
| chip/text/selected | color/text/inverse |
| chip/border/default | color/border/default |
| chip/border/selected | color/border/primary |
| chip/radius | radius/full |

#### Card
| Token | Value |
|---|---|
| card/background | color/background/default |
| card/border | color/border/default |
| card/radius | radius/lg |
| card/shadow | 0 1px 3px rgba(0,0,0,0.08) |

#### Dialog / Modal
| Token | Value |
|---|---|
| dialog/background | color/background/default |
| dialog/border | color/border/default |
| dialog/radius | radius/xl |
| dialog/overlay | rgba(0,0,0,0.5) |

#### Tooltip
| Token | Value |
|---|---|
| tooltip/background | color/background/inverse |
| tooltip/text | color/text/inverse |
| tooltip/radius | radius/sm |

---

## COMPONENT DEFINITIONS (semantic distinctions — enforce strictly)

| Component | Purpose | Interactive? | Example use |
|---|---|---|---|
| Button | Triggers an action | Yes | Submit, Save, Delete, Open dialog |
| Link | Navigation only | Yes | Go to page, external URL |
| Tag | Non-interactive label | No | Vertical, Region, Stage |
| Badge | Status or count indicator | No | Risk level, Momentum, Score tier |
| Chip | Interactive filter or toggle | Yes | Filter by vertical, select option |

**Rule**: Never use Button where Tag, Badge, or Chip is semantically correct. The 360-import Button problem in the codebase comes from this violation.

---

## USAGE RULES (enforced by ESLint plugin)

### Always
- Reference tokens, never raw values. `var(--color-text-primary)` not `#5D4EE7`
- Use semantic tokens in components, not primitives. `color/text/danger` not `color/red/600`
- Use Lato for all UI text. Roboto Mono for code blocks only.
- Use the correct component semantically (see Component Definitions above)

### Never
- Hardcode hex, rgb(), or hsl() in component files
- Import Radix UI directly — always use shadcn wrappers in components/ui/
- Use Button as a non-interactive display element
- Place impl-specific components (CoffeyNavigation, etc.) in shared component space
- Use AlliancePlatt or any other brand font in product UI

---

## ESLINT RULES (installed at design-system/eslint-plugin/)

| Rule | Severity | What it catches |
|---|---|---|
| no-hardcoded-colors | error | Any hex, rgb(), hsl() in component files |
| no-direct-radix-imports | error | Direct @radix-ui/* imports |
| no-impl-specific-shared-components | error | Impl components in shared space |
| no-hardcoded-spacing | warn | px values in inline style objects |
| no-deprecated-src-components | warn | Legacy src/ component imports |

Run audit (report only, nothing breaks):
```bash
node design-system/scripts/run-audit.js
```

---

## REACT TOKEN USAGE PATTERN

In React artifacts or components, map semantic tokens to a JS object like this:

```javascript
const t = {
  // Background
  bgDefault: "var(--color-background-default)",      // #FFFFFF light
  bgSubtle: "var(--color-background-subtle)",         // #F9FAFB light
  bgSecondary: "var(--color-background-secondary)",   // #F3F4F6 light
  bgAccent: "var(--color-background-accent)",         // #EFEDFD light
  bgPrimary: "var(--color-background-primary)",       // #5D4EE7
  bgInverse: "var(--color-background-inverse)",       // #0F1117 light
  bgDanger: "var(--color-background-danger)",         // #FEF2F2 light
  bgSuccess: "var(--color-background-success)",       // #F0FDF4 light
  bgWarning: "var(--color-background-warning)",       // #FFFBEB light

  // Text
  textDefault: "var(--color-text-default)",           // #0F1117 light
  textSubtle: "var(--color-text-subtle)",             // #6B7280 light
  textDisabled: "var(--color-text-disabled)",         // #D1D5DB light
  textInverse: "var(--color-text-inverse)",           // #FFFFFF light
  textPrimary: "var(--color-text-primary)",           // #5D4EE7 light
  textDanger: "var(--color-text-danger)",             // #DC2626 light
  textSuccess: "var(--color-text-success)",           // #15803D light
  textWarning: "var(--color-text-warning)",           // #B45309 light

  // Border
  borderDefault: "var(--color-border-default)",       // #E5E7EB light
  borderSubtle: "var(--color-border-subtle)",         // #F3F4F6 light
  borderStrong: "var(--color-border-strong)",         // #9CA3AF light
  borderPrimary: "var(--color-border-primary)",       // #5D4EE7 light
  borderSuccess: "var(--color-border-success)",       // #16A34A light ← NEW
  borderWarning: "var(--color-border-warning)",       // #D97706 light ← NEW
  borderDanger: "var(--color-border-danger)",         // #DC2626 light ← NEW
  borderInfo: "var(--color-border-info)",             // #9D8EF3 light ← NEW

  // Feedback
  feedbackDanger: "var(--color-feedback-danger)",     // #EF4444
  feedbackSuccess: "var(--color-feedback-success)",   // #16A34A
  feedbackWarning: "var(--color-feedback-warning)",   // #F59E0B
  feedbackInfo: "var(--color-feedback-info)",         // #7D69EF
};
```

For artifacts where CSS vars aren't available (claude.ai sandbox), use raw hex values 
from the token tables above. The token names are still the reference — raw values 
are the fallback for rendering only.

---

## COMPONENT PATTERNS

### Badge (copy this pattern)
```jsx
const Badge = ({ children, style }) => (
  <span style={{
    display: "inline-flex", alignItems: "center",
    padding: "2px 8px", borderRadius: 9999,           // radius/full
    fontSize: 12, fontWeight: 500,
    fontFamily: "Lato, sans-serif",
    ...style
  }}>{children}</span>
);

// Usage — always pass explicit background + color from token object
<Badge style={{ background: t.bgAccent, color: t.textPrimary }}>Active</Badge>
<Badge style={{ background: t.bgDanger, color: t.textDanger }}>Error</Badge>
<Badge style={{ background: t.bgSuccess, color: t.textSuccess }}>Done</Badge>
```

### Tag (copy this pattern)
```jsx
const Tag = ({ children }) => (
  <span style={{
    display: "inline-flex", alignItems: "center",
    padding: "2px 8px", borderRadius: 4,              // radius/sm
    fontSize: 12, fontWeight: 400,
    fontFamily: "Lato, sans-serif",
    background: t.bgSecondary,
    color: t.textSubtle,
    border: `1px solid ${t.borderDefault}`,
    whiteSpace: "nowrap"
  }}>{children}</span>
);
```

### Chip (copy this pattern)
```jsx
const Chip = ({ children, selected, onClick }) => (
  <button onClick={onClick} style={{
    padding: "4px 12px", borderRadius: 9999,           // radius/full
    fontSize: 12, fontWeight: selected ? 600 : 400,
    fontFamily: "Lato, sans-serif",
    cursor: "pointer", border: "none",
    background: selected ? t.bgPrimary : t.bgDefault,
    color: selected ? t.textInverse : t.textSubtle,
    border: `1px solid ${selected ? t.borderPrimary : t.borderDefault}`,
  }}>{children}</button>
);
```

### Input (copy this pattern)
```jsx
<input style={{
  width: "100%", padding: "10px 12px",               // space/3 vertical, space/3 horizontal (per guidelines)
  borderRadius: 6,                                    // radius/md — 6px per Guidelines_General.md
  border: `1px solid ${t.borderDefault}`,
  fontSize: 14,                                       // typography/size/sm — 14px body per guidelines
  fontFamily: "Lato, sans-serif",
  color: t.textDefault,
  background: t.bgDefault,
  outline: "none",
}} />
```

### Nav bar (copy this pattern)
```jsx
<nav style={{
  background: t.bgDefault,
  borderBottom: `1px solid ${t.borderDefault}`,
  padding: "0 20px",                                  // space/5
  height: 48,                                         // space/12
  display: "flex", alignItems: "center",
  position: "sticky", top: 0, zIndex: 10,
}} />
```

---

## GUIDELINES (from Guidelines_General.md — baked into tokens)

| Rule | Token |
|---|---|
| Body text: 14px | typography/size/sm |
| Input radius: 6px | radius/md |
| Label to input gap: 8px | space/2 |
| Label color: foreground, 14px | color/text/default + typography/size/sm |
| Placeholder: muted-foreground | color/text/subtle |
| Input padding: 12px top/bottom, 8px left/right | space/3 + space/2 |
| Form field gap: 24px | space/6 |
| Dropdown hover: gray-100 bg | color/background/secondary |
| Message container radius: 12px | radius/xl |
| Panel header padding: 20px | space/5 |
| Panel container radius: 6px | radius/md |
| AI message: left-aligned, white bg | color/background/default |
| User message: right-aligned, gray-50 bg | color/background/subtle |
| No line dividers | use border/subtle only when structurally necessary |

---

## DARK MODE

Dark mode is implemented at the **Semantic layer only**. Primitives don't change. 
Components don't change. Only semantic token values swap.

In CSS:
```css
:root { --color-background-default: #FFFFFF; --color-text-default: #0F1117; }
[data-theme="dark"] { --color-background-default: #0F1117; --color-text-default: #F9FAFB; }
```

---

## CUSTOMER THEMING

A full customer rebrand is one CSS file overriding primitives only:

```css
/* customer-acme.css — all that's needed for a full rebrand */
:root {
  --color-purple-500: #22C55E;   /* their green replaces Distyl purple */
  --color-purple-400: #16A34A;
  --color-purple-50: #F0FDF4;
  --typography-family-body: Arial, sans-serif;
}
```

No component code changes. No impl changes. Semantic and component layers 
cascade automatically.

---

## FIGMA

- **Workspace**: Distyl AI → Design System and Library
- **Tokens file**: Foundations project (published as team library)
  - Collections: Primitives (69), Semantic (33), Components (46)
- **shadcn kit**: Components project → shadcn/ui kit for Figma + Pro Blocks (Feb 2026)
  - Collections: TailwindCSS (452), Theme (235), Mode (74), Custom (26), Icon Library (5)
- **Brand swap**: In kit Theme collection, remap 4 tokens to Distyl purple:
  - primary-light → color/purple/500
  - primary-dark → color/purple/400
  - primary-foreground-light → color/gray/0
  - primary-foreground-dark → color/gray/0

---

## REPO

- **Monorepo**: fe-distillery (github.com/DistylAI/fe-distillery)
- **Design system files**: fe-distillery/design-system/
  - eslint-plugin/ — 5 ESLint rules
  - scripts/ — Figma token bootstrap plugin
- **Component library**: components/ui/ (shadcn wrappers — source of truth)
- **Impls**: impls/tower, impls/pennycai, impls/platform, impls/coffey, impls/apprentice, impls/eagle
- **Known debt**: 8 unused components, 3 duplicate pairs, 4 direct Radix imports, 
  CoffeyNavigation in shared space, dead toast/toaster system

---

## WHAT'S COMPLETE vs IN PROGRESS

| Item | Status |
|---|---|
| Token naming spec (Google Docs) | ✅ Complete |
| Figma Tokens file (148 vars, 3 collections) | ✅ Complete + published |
| Figma bootstrap plugin | ✅ Complete |
| ESLint plugin (5 rules + audit script) | ✅ Complete |
| shadcn kit imported to Figma | ✅ Complete |
| Tokens library enabled in shadcn kit | ⏳ Next step |
| 4 primary token swaps in kit | ⏳ Next step |
| Code Connect setup | ⏳ Not started |
| Component cleanup (unused/duplicates) | ⏳ Not started |
| ESLint plugin installed in repo | ⏳ Not started |

---
*Distyl AI Design System · Reference Package v1.1 · February 2026*
