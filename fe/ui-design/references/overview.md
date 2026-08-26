# Distyl AI Design System — v1.1
**Status:** Foundation complete · February 2026

This package contains everything needed to understand, enforce, and extend the Distyl design system. Start with this README, then dig into the relevant folder for your role.

---

## What's in this package

```
distyl-design-system-package/
├── README.md                            ← You are here
├── distyl-design-system-reference.md   ← Full token reference + Claude prompt file
├── distyl-design-system-handoff.docx   ← Full context doc (decisions, architecture, next steps)
├── figma-plugin/                        ← Rebuilds all Figma tokens from scratch
│   ├── manifest.json
│   ├── code.js
│   └── ui.html
└── eslint-plugin/                       ← Enforces token usage in code
    ├── index.js                         ← 5 ESLint rules
    ├── package.json
    ← audit.eslintrc.js                  ← Report-only audit config
    ├── run-audit.js                     ← Audit script (no CI impact)
    └── README.md                        ← Full rule documentation
```

---

## For Frontend Engineers

### 1. Install the ESLint plugin

Drop the `eslint-plugin/` folder into the repo:

```
fe-distillery/design-system/eslint-plugin/
```

Add to root `package.json` devDependencies:

```json
"eslint-plugin-distyl-design-system": "file:design-system/eslint-plugin"
```

Add to your `.eslintrc.js`:

```js
module.exports = {
  plugins: ['distyl-design-system'],
  extends: ['plugin:distyl-design-system/recommended'],
};
```

### 2. Run the audit first (nothing breaks, report only)

Before enforcing anything, get the baseline violation count:

```bash
# Drop run-audit.js at:
fe-distillery/design-system/scripts/run-audit.js

# Then run:
node design-system/scripts/run-audit.js
```

Produces:
- `design-system/audit-summary.md` — human-readable violation count by rule and area
- `design-system/audit-report.json` — raw data

### 3. What the rules enforce

| Rule | Severity | Catches |
|---|---|---|
| `no-hardcoded-colors` | error | Hex, rgb(), hsl() values in component files |
| `no-direct-radix-imports` | error | Direct `@radix-ui/*` imports — use shadcn wrappers |
| `no-impl-specific-shared-components` | error | Impl components in shared space |
| `no-hardcoded-spacing` | warn | px values in inline style objects |
| `no-deprecated-src-components` | warn | Legacy `src/` imports with `ui/` equivalents |

### 4. Migration approach

**Don't try to fix everything at once.** The right rollout:

- **Today:** New files error on all rules immediately
- **Sprint 1:** `components/ui/` layer — enforce errors, it's the smallest and cleanest area
- **Ongoing:** Impls migrate naturally as features are touched for product reasons

The audit tells you the debt. It's not a to-do list — it's the before snapshot.

---

## For Designers

### Figma setup (already done — for reference)

- **Workspace:** Distyl AI → Design System and Library
- **Tokens file:** Foundations project — published as team library ✅
- **shadcn kit:** Components project — published as team library ✅
- **Brand:** `primary-light` → `color/purple/500`, `primary-dark` → `color/purple/400`

### To use in a new Figma file

1. Open your file
2. Main menu → Libraries
3. Enable **Tokens** and **shadcn/ui kit for Figma + Pro Blocks**
4. All Distyl-branded components and tokens are now available

### To re-run the token plugin (if tokens need updating)

1. Open the **Tokens file** (not the shadcn kit)
2. Plugins → Development → Distyl Design System — Token Bootstrap
3. Run Bootstrap Tokens
4. File menu → Publish library

---

## Token Architecture

Three layers. All references are aliases — change a primitive, everything cascades.

```
Primitives (76)     Raw values: purple scale, gray scale, feedback colors,
                    spacing, radius, typography

      ↓ aliases

Semantic (37)       Purpose-named: color/background/*, color/text/*,
                    color/border/*, color/icon/*, color/feedback/*
                    Has Light + Dark modes

      ↓ aliases

Components (46)     Scoped: button/*, input/*, badge/*, tag/*, chip/*,
                    card/*, dialog/*, tooltip/*, select/*
```

### Brand expression

Purple is the only Distyl-specific breakout from the shadcn/Tailwind defaults:

```css
--color-purple-500: #5D4EE7;  /* primary actions, focus rings, active states */
--color-purple-400: #7767EF;  /* dark mode primary */
```

Everything else — grays, red, green, amber — matches Tailwind defaults.

### Customer theming

A full customer rebrand is one CSS file:

```css
/* customer-acme/theme.css */
:root {
  --color-purple-500: #22C55E;  /* their green replaces Distyl purple */
  --typography-family-body: Arial, sans-serif;
}
```

No component changes. No impl changes. Everything cascades from primitives.

---

## Key decisions (brief)

| Decision | Why |
|---|---|
| shadcn/ui as component foundation | 360 Button imports already in codebase — don't rebuild what exists |
| ESLint warn during migration, error for new code | Staged rollout — don't block product work |
| Branch not merge for customer themes | Base system is the law, customer brand is a fork |
| Lato + Roboto Mono only | AlliancePlatt is a marketing font, not a product font |
| Manual gate on Figma → code | Code Connect links but doesn't auto-push — human ships the code |

---

## Known repo debt (fe-distillery)

Flagged in audit, not yet fixed:

- 8 unused components: calendar, carousel, drawer, expanding-textarea, input-otp, menubar, navigation-menu, slider
- 3 duplicate pairs: LabelWithInfo ×2, DynamicTextarea ×2, TagInput ×2
- 4 files importing Radix directly (ESLint now catches new violations)
- CoffeyNavigation in shared space (should be in impls/coffey/)
- Two toast systems: sonner (active) + toast/toaster (dead)

---

## Using the reference file with Claude

`distyl-design-system-reference.md` is structured for Claude ingestion. Attach it at the start of any Claude session and Claude will generate token-compliant UI output using correct token names, component patterns, and naming conventions.

---

*Distyl AI Design System · v1.1 · February 2026 · Owner: Tony Yates*
