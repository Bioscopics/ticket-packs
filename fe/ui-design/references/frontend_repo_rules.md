# Distyl AI — fe-distillery
## Claude Code System Guide · v1.1 · February 2026

This file gives you full context on the fe-distillery codebase, design system, and the rules that govern it. Read this before touching components, tokens, or shared code.

---

## What this repo is

`fe-distillery` is the frontend monorepo for Distyl AI — an enterprise data and AI platform. It serves multiple product implementations from a single shared component library.

### Implementations
| Impl | Description |
|---|---|
| Tower | Core Distyl product |
| PennyCai | Conversational AI interface |
| Platform | Admin and infrastructure layer |
| Coffey | Customer-specific impl |
| Apprentice | Training and onboarding product |
| Eagle | Analytics and reporting impl |

### Repo structure
```
fe-distillery/
├── components/
│   ├── ui/           ← shadcn wrappers — source of truth for all primitives
│   └── shared/       ← Distyl shared components — used across impls
├── impls/
│   ├── tower/        ← Tower-specific components and pages
│   ├── pennycai/     ← PennyCai-specific
│   ├── platform/     ← Platform-specific
│   ├── coffey/       ← Coffey-specific
│   ├── apprentice/   ← Apprentice-specific
│   └── eagle/        ← Eagle-specific
└── design-system/
    ├── eslint-plugin/   ← 5 ESLint rules enforcing the token system
    └── scripts/         ← Figma token bootstrap plugin
```

---

## Design system architecture

Three layers. All token references are aliases — change a primitive and everything cascades.

```
Primitives (76)
  Raw values: purple scale, gray scale, feedback colors,
  spacing, radius, typography families and sizes

        ↓ aliases

Semantic (37)
  Purpose-named: color/background/*, color/text/*,
  color/border/*, color/icon/*, color/feedback/*
  Has Light and Dark modes

        ↓ aliases

Components (46)
  Scoped: button/*, input/*, badge/*, tag/*, chip/*,
  card/*, dialog/*, tooltip/*, select/*
```

In code, always reference semantic or component tokens via CSS custom properties. Never use raw values.

---

## Color tokens — always use these, never hardcode

### Background
```css
var(--color-background-default)     /* white in light, near-black in dark */
var(--color-background-subtle)      /* gray-50 / gray-900 */
var(--color-background-secondary)   /* gray-100 / gray-800 */
var(--color-background-accent)      /* purple-50 / purple-900 */
var(--color-background-primary)     /* purple-500 — buttons, CTAs, active states */
var(--color-background-inverse)     /* near-black / white */
var(--color-background-danger)      /* red-50 */
var(--color-background-success)     /* green-50 */
var(--color-background-warning)     /* amber-50 */
```

### Text
```css
var(--color-text-default)           /* gray-950 / gray-50 */
var(--color-text-subtle)            /* gray-500 / gray-400 */
var(--color-text-disabled)          /* gray-300 / gray-600 */
var(--color-text-inverse)           /* white / near-black */
var(--color-text-primary)           /* purple-500 / purple-400 */
var(--color-text-danger)            /* red-600 / red-400 */
var(--color-text-success)           /* green-700 / green-500 */
var(--color-text-warning)           /* amber-700 / amber-500 */
```

### Border
```css
var(--color-border-default)         /* gray-200 / gray-700 */
var(--color-border-subtle)          /* gray-100 / gray-800 */
var(--color-border-strong)          /* gray-400 / gray-500 */
var(--color-border-primary)         /* purple-500 / purple-400 */
var(--color-border-success)         /* green-600 / green-500 */
var(--color-border-warning)         /* amber-600 / amber-500 */
var(--color-border-danger)          /* red-600 / red-500 */
var(--color-border-info)            /* purple-300 / purple-400 */
```

### Feedback
```css
var(--color-feedback-danger)        /* red-500 */
var(--color-feedback-success)       /* green-600 */
var(--color-feedback-warning)       /* amber-500 */
var(--color-feedback-info)          /* purple-400 */
```

---

## Spacing and radius

Use the token scale. Never use arbitrary px values.

```css
/* Spacing — 4px base unit */
var(--space-1): 4px    var(--space-2): 8px    var(--space-3): 12px
var(--space-4): 16px   var(--space-5): 20px   var(--space-6): 24px
var(--space-8): 32px   var(--space-10): 40px  var(--space-12): 48px

/* Radius */
var(--radius-sm): 4px   var(--radius-md): 6px   var(--radius-lg): 8px
var(--radius-xl): 12px  var(--radius-full): 9999px
```

In Tailwind: use standard scale classes (`p-4`, `gap-2`, `rounded-md`), never arbitrary values (`p-[13px]`, `text-[#5D4EE7]`).

---

## Typography

- **UI text:** `Lato, sans-serif` — always
- **Code/monospace:** `Roboto Mono, monospace` — code blocks only
- **Never use:** system-ui, Inter, AlliancePlatt, or any other family
- **Body size:** 14px (`typography/size/sm`) per guidelines
- **Label size:** 14px, `color/text/default`
- **Placeholder:** `color/text/subtle`

---

## Component rules

### Always import from shadcn wrappers
```ts
// ✅ Correct
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { Select, SelectTrigger } from "@/components/ui/select"

// ❌ Never — direct Radix imports bypass the token system
import * as Dialog from "@radix-ui/react-dialog"
import * as Select from "@radix-ui/react-select"
```

### Component semantic distinctions — this matters

| Component | Purpose | Interactive | Use for |
|---|---|---|---|
| Button | Triggers an action | Yes | Submit, Save, Delete, open dialogs |
| Link | Navigation | Yes | Routing, external URLs |
| Tag | Non-interactive label | No | Vertical, Region, Stage, Category |
| Badge | Status or count indicator | No | Risk level, Momentum, Score tier |
| Chip | Interactive filter/toggle | Yes | Filter by vertical, toggle selection |

**The Button problem:** Button has 360+ imports in this codebase. Many of those should be Tag, Badge, or Chip. Before adding another Button import, ask whether the element is actually triggering an action or just displaying information.

---

## Shared vs impl boundaries

```
components/ui/       ← shadcn primitives only. No Distyl-specific logic.
components/shared/   ← Used across ALL impls. Must be generic.
impls/*/             ← Impl-specific. Never imported by other impls or shared/.
```

**Hard rules:**
- Never put impl-specific components in `components/shared/`
- Never import from `impls/tower/` inside `impls/coffey/` or vice versa
- CoffeyNavigation, TowerSidebar, etc. belong in their impl folder only
- If something is used in 2+ impls, it belongs in `components/shared/`

---

## Dark mode

Handled at the semantic token layer. CSS variables swap automatically via `[data-theme="dark"]`.

```tsx
// ✅ Correct — token handles both modes
<div style={{ background: 'var(--color-background-default)' }}>

// ❌ Wrong — manual dark mode utilities bypass the token system
<div className="bg-white dark:bg-gray-950">
```

Never write `dark:` Tailwind utilities for color. If you find them, replace with token variables.

---

## Customer theming

The system supports full customer rebranding via primitive overrides only. When building components, never assume the brand color is purple — it must work with any value of `--color-background-primary`.

```css
/* A complete customer rebrand is only ever this */
:root {
  --color-purple-500: #22C55E;
  --typography-family-body: Arial, sans-serif;
}
```

---

## Known debt — don't add to these, flag if you touch them

### Unused components (remove, don't extend)
calendar, carousel, drawer, expanding-textarea, input-otp, menubar, navigation-menu, slider

### Duplicate components (consolidate before using)
LabelWithInfo ×2, DynamicTextarea ×2, TagInput ×2

### Dead code
- `toast/toaster` system — dead, sonner is active. Don't add new toast/toaster usage.
- `penny.*` legacy color classes — verify usage before touching

### Misplaced components
- `CoffeyNavigation` is in shared space — belongs in `impls/coffey/`

### Direct Radix imports
4 files currently bypass shadcn wrappers. ESLint catches new violations. Don't add more.

---

## ESLint enforcement

The ESLint plugin at `design-system/eslint-plugin/` enforces the token system.

| Rule | Severity | Catches |
|---|---|---|
| no-hardcoded-colors | error | Hex, rgb(), hsl() in component files |
| no-direct-radix-imports | error | Direct @radix-ui/* imports |
| no-impl-specific-shared-components | error | Impl components in shared space |
| no-hardcoded-spacing | warn | px values in inline style objects |
| no-deprecated-src-components | warn | Legacy src/ imports |

### Run the audit (no CI impact — report only)
```bash
node design-system/scripts/run-audit.js
```

Produces:
- `design-system/audit-summary.md` — violations by rule and area
- `design-system/audit-report.json` — raw data

Run this first to get the baseline before making changes. It tells you where the debt is.

---

## When you need a token that doesn't exist

Follow the naming convention and flag it — don't patch inline:

```
color/{category}/{variant}
  categories: background | text | border | icon | feedback
  variants:   default | subtle | strong | primary | inverse
              danger | success | warning | info

space/{scale}      → Tailwind scale (1=4px, 2=8px, 4=16px...)
radius/{size}      → none | sm | md | lg | xl | 2xl | full
typography/{category}/{variant}
```

Missing tokens should be added to the system properly, not worked around inline. Raise it with the design system owner (Tony Yates).

---

## Figma

Both libraries are published in the Design System and Library workspace:
- **Tokens** — 158 token variables across 3 collections, Light + Dark modes
- **shadcn/ui kit** — fully branded components wired to Distyl tokens

To use in a new Figma file: Main menu → Libraries → enable both.

---

## Using Claude for this codebase

Attach `distyl-design-system-reference.md` (in this package) to any Claude.ai session to get token-compliant output. It contains the full token set, component patterns, and naming conventions in a format Claude can parse directly.

For Claude Code sessions in this repo, this `CLAUDE.md` file loads automatically.

---

*Distyl AI · fe-distillery · CLAUDE.md · v1.1 · February 2026*
*Design system owner: Tony Yates*
