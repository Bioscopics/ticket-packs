# Distyl AI Design System — Cursor Rules
# Drop this file at the root of fe-distillery as .cursorrules
# Version 1.1 | February 2026

## IDENTITY

You are building UI for Distyl AI, an enterprise data and AI platform.
The design system is built on shadcn/ui components with a custom token layer.
All UI output must be token-compliant, semantically correct, and themeable.

---

## FONTS

- UI text: `Lato, sans-serif` — always
- Code, monospace display: `Roboto Mono, monospace` — only for code blocks and technical strings
- Never use system-ui, Inter, or any other font family
- Never use AlliancePlatt — it is a marketing font, not a product font

---

## COLORS — NEVER HARDCODE

Never use raw hex, rgb(), hsl(), or Tailwind color utilities directly in components.
Always use CSS custom properties from the token system.

### Background tokens
```
var(--color-background-default)    /* white / near-black in dark */
var(--color-background-subtle)     /* gray-50 / gray-900 */
var(--color-background-secondary)  /* gray-100 / gray-800 */
var(--color-background-accent)     /* purple-50 / purple-900 */
var(--color-background-primary)    /* purple-500 — buttons, CTAs */
var(--color-background-inverse)    /* near-black / white */
var(--color-background-danger)     /* red-50 */
var(--color-background-success)    /* green-50 */
var(--color-background-warning)    /* amber-50 */
```

### Text tokens
```
var(--color-text-default)          /* gray-950 / gray-50 */
var(--color-text-subtle)           /* gray-500 / gray-400 */
var(--color-text-disabled)         /* gray-300 / gray-600 */
var(--color-text-inverse)          /* white / near-black */
var(--color-text-primary)          /* purple-500 / purple-400 */
var(--color-text-danger)           /* red-600 / red-400 */
var(--color-text-success)          /* green-700 / green-500 */
var(--color-text-warning)          /* amber-700 / amber-500 */
```

### Border tokens
```
var(--color-border-default)        /* gray-200 / gray-700 */
var(--color-border-subtle)         /* gray-100 / gray-800 */
var(--color-border-strong)         /* gray-400 / gray-500 */
var(--color-border-primary)        /* purple-500 / purple-400 */
var(--color-border-success)        /* green-600 / green-500 */
var(--color-border-warning)        /* amber-600 / amber-500 */
var(--color-border-danger)         /* red-600 / red-500 */
var(--color-border-info)           /* purple-300 / purple-400 */
```

### Feedback tokens
```
var(--color-feedback-danger)       /* red-500 */
var(--color-feedback-success)      /* green-600 */
var(--color-feedback-warning)      /* amber-500 */
var(--color-feedback-info)         /* purple-400 */
```

### Icon tokens
```
var(--color-icon-default)
var(--color-icon-subtle)
var(--color-icon-primary)
var(--color-icon-inverse)
```

---

## SPACING — USE TOKEN SCALE

Use the spacing scale. Never use arbitrary px values in className or inline styles.

```
--space-px: 1px      --space-1: 4px     --space-2: 8px
--space-3: 12px      --space-4: 16px    --space-5: 20px
--space-6: 24px      --space-8: 32px    --space-10: 40px
--space-12: 48px     --space-16: 64px
```

In Tailwind: use standard scale classes (p-2, gap-4, mt-6) not arbitrary values (p-[13px]).

---

## BORDER RADIUS — USE TOKEN SCALE

```
--radius-none: 0px    --radius-sm: 4px     --radius-md: 6px
--radius-lg: 8px      --radius-xl: 12px    --radius-2xl: 16px
--radius-full: 9999px
```

Per guidelines: inputs and panels use radius-md (6px). Cards use radius-lg (8px). Pills and badges use radius-full.

---

## COMPONENT RULES

### Imports — always use shadcn wrappers
```ts
// ✅ CORRECT
import { Button } from "@/components/ui/button"
import { Dialog } from "@/components/ui/dialog"
import { Select } from "@/components/ui/select"

// ❌ NEVER — direct Radix imports
import * as Dialog from "@radix-ui/react-dialog"
import * as Select from "@radix-ui/react-select"
```

### Component semantic distinctions — enforce strictly

| Component | Purpose | Interactive | When to use |
|---|---|---|---|
| Button | Triggers an action | Yes | Submit, Save, Delete, Open dialog |
| Link | Navigation | Yes | Go to page, external URL |
| Tag | Non-interactive label | No | Vertical, Region, Stage, Category |
| Badge | Status or count | No | Risk level, Momentum, Score, State |
| Chip | Interactive filter/toggle | Yes | Filter by vertical, toggle selection |

**Never use Button as a display element.**
**Never use Badge or Tag where a Chip should be (i.e. if it's clickable, it's a Chip).**

### Button variants
```tsx
<Button variant="default">Primary action</Button>      // purple fill
<Button variant="secondary">Secondary action</Button>  // gray outline
<Button variant="ghost">Ghost action</Button>          // no border
<Button variant="destructive">Delete</Button>          // red fill
<Button variant="outline">Outline</Button>             // border only
```

### Form field pattern (per guidelines)
```tsx
<div className="flex flex-col gap-2">          {/* gap = space/2 = 8px */}
  <Label htmlFor="field">Label text</Label>    {/* text-sm = 14px */}
  <Input
    id="field"
    placeholder="Placeholder..."
    className="rounded-md"                     {/* radius/md = 6px */}
  />
</div>
```

Form section gap: `gap-6` (24px = space/6) between fields.

---

## DARK MODE

Dark mode is handled at the semantic token layer — CSS variables swap automatically.
Never write separate dark: Tailwind utilities for color. Use the token variables.

```tsx
// ✅ CORRECT — token handles light/dark automatically
<div style={{ background: 'var(--color-background-default)' }}>

// ❌ WRONG — don't manually specify dark mode colors
<div className="bg-white dark:bg-gray-950">
```

---

## SHARED VS IMPL COMPONENTS

```
components/ui/          ← shadcn primitives — shared, token-connected
components/shared/      ← Distyl shared components — used across impls
impls/tower/            ← Tower-specific components
impls/pennycai/         ← PennyCai-specific components
impls/coffey/           ← Coffey-specific components
impls/platform/         ← Platform-specific components
```

**Never put impl-specific components in `components/shared/`.**
**Never put Tower, Coffey, or PennyCai-specific logic in shared space.**

---

## CUSTOMER THEMING

The system supports full customer rebranding via primitive token overrides only.
When building new components, ensure they work with any value of `--color-background-primary`
and `--color-text-primary` — don't assume purple.

```css
/* A customer rebrand is only ever this: */
:root {
  --color-purple-500: #22C55E;
  --typography-family-body: Arial, sans-serif;
}
```

---

## REACT COMPONENT PATTERN

When building React components in this codebase:

```tsx
// ✅ Token-compliant React component pattern
export function StatusBadge({ status }: { status: 'success' | 'warning' | 'danger' }) {
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '2px 8px',
        borderRadius: 'var(--radius-full)',
        fontSize: '12px',
        fontWeight: 500,
        fontFamily: 'Lato, sans-serif',
        background: `var(--color-background-${status})`,
        color: `var(--color-text-${status})`,
      }}
    >
      {status}
    </span>
  )
}
```

---

## TAILWIND USAGE GUIDELINES

- Use standard Tailwind scale classes — `p-4`, `gap-2`, `mt-6`, `rounded-md`
- Never use arbitrary values — `p-[13px]`, `gap-[7px]`, `text-[#5D4EE7]`
- Never use Tailwind color utilities for brand colors — `text-purple-500`, `bg-purple-500`
  (these bypass the token system and break customer theming)
- For colors, always use CSS variable approach via `style` prop or a CSS class

---

## WHEN ADDING NEW TOKENS

If a design decision isn't covered by an existing token, follow the naming convention:

```
color/{category}/{variant}
  category: background | text | border | icon | feedback
  variant:  default | subtle | strong | primary | inverse | danger | success | warning | info

space/{scale}        → matches Tailwind scale (1=4px, 2=8px, etc.)
radius/{size}        → none | sm | md | lg | xl | 2xl | full
typography/{category}/{variant}
```

Don't invent one-off values. If a token is genuinely missing, flag it — it should be added
to the system properly, not patched inline.

---

## LINTING

The ESLint plugin at `design-system/eslint-plugin/` enforces these rules automatically.
If you see a lint error:
- `no-hardcoded-colors` → replace with CSS variable from token system
- `no-direct-radix-imports` → use the shadcn wrapper in `components/ui/`
- `no-impl-specific-shared-components` → move to the correct impl folder
- `no-hardcoded-spacing` → use spacing scale
- `no-deprecated-src-components` → use the `components/ui/` equivalent

---

*Distyl AI Design System · .cursorrules · v1.1 · February 2026*
