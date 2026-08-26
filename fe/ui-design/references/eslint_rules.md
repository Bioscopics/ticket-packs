# eslint-plugin-distyl-design-system

ESLint rules that enforce the Distyl AI design system token architecture and component conventions. These rules make the *right way* also the *only way* — no hardcoded values, no bypassed abstractions.

---

## Installation

From the repo root, add the plugin as a local package reference:

```bash
# In your root package.json or the specific impl's package.json
pnpm add -D file:../../design-system/eslint-plugin
```

Or for workspace-wide enforcement, add to the root:

```json
{
  "devDependencies": {
    "eslint-plugin-distyl-design-system": "workspace:design-system/eslint-plugin"
  }
}
```

---

## Setup

In your `.eslintrc.js` or `eslint.config.js`:

```js
// .eslintrc.js
module.exports = {
  plugins: ['distyl-design-system'],
  extends: ['plugin:distyl-design-system/recommended'],
};

// or manually configure rules:
module.exports = {
  plugins: ['distyl-design-system'],
  rules: {
    'distyl-design-system/no-hardcoded-colors': 'error',
    'distyl-design-system/no-hardcoded-spacing': 'warn',
    'distyl-design-system/no-direct-radix-imports': 'error',
    'distyl-design-system/no-deprecated-src-components': 'warn',
    'distyl-design-system/no-impl-specific-shared-components': 'error',
  },
};
```

---

## Rules

### `no-hardcoded-colors` — error

Prevents hex, rgb(), hsl() color values anywhere in component files. All colors must reference CSS variable tokens.

```jsx
// ❌ Fails
<div style={{ color: '#5D4EE7' }} />
<div style={{ background: 'rgb(93, 78, 231)' }} />

// ✅ Passes
<div style={{ color: 'var(--color-text-primary)' }} />
<div className="text-text-primary" />
```

---

### `no-hardcoded-spacing` — warn

Flags hardcoded pixel values in inline style objects for spacing and sizing properties.

```jsx
// ❌ Warns
<div style={{ padding: '16px', marginTop: '24px' }} />

// ✅ Passes
<div style={{ padding: 'var(--space-4)' }} />
<div className="p-4 mt-6" />
```

> Set to `warn` during migration to avoid blocking existing work. Promote to `error` once the codebase is clean.

---

### `no-direct-radix-imports` — error

All Radix UI usage must go through the shadcn wrappers in `components/ui/`. Direct Radix imports bypass the abstraction layer and won't receive design token updates.

```jsx
// ❌ Fails — 4 existing violations flagged in audit
import * as Tabs from '@radix-ui/react-tabs'
import * as Collapsible from '@radix-ui/react-collapsible'

// ✅ Passes
import { Tabs, TabsList, TabsTrigger } from '@distyl/components'
```

---

### `no-deprecated-src-components` — warn

Flags imports of components from the legacy `src/` layer that have canonical equivalents in `ui/`.

```jsx
// ❌ Warns
import { InputLabel } from '../src/InputLabel'
import { LabelWithInfo } from '../src/LabelWithInfo'

// ✅ Passes
import { Label } from '@distyl/components'
```

> The full migration list is in `design-system/docs/migration.md`.

---

### `no-impl-specific-shared-components` — error

Prevents impl-specific components from being imported into shared component space. This was the root cause of `CoffeyNavigation` ending up in `components/src/`.

```jsx
// ❌ Fails (when in components/src/ or components/ui/)
import { CoffeyNavigation } from '../CoffeyNavigation'

// ✅ Passes (in impls/coffey/ only)
import { CoffeyNavigation } from './CoffeyNavigation'
```

---

## Customer Theming

These rules apply to the **base Distyl system only**. Customer theme branches override primitive tokens via CSS variable files — they do not change component code. The ESLint rules enforce this by ensuring no colors are hardcoded at the component level, making theming purely a token-layer concern.

```css
/* impls/customer-x/theme.css — all that's needed for a full rebrand */
:root {
  --color-purple-500: #22C55E;  /* their green replaces our purple */
  --typography-family-body: Arial, sans-serif;
}
```

---

## Adding New Rules

Add new rule files to `design-system/eslint-plugin/rules/` and register them in `index.js`. Follow the pattern in existing rules — each rule has `meta`, `create`, and is registered in both `rules` and `configs.recommended`.

---

## Suppressing Rules

Use standard ESLint suppression with a comment explaining why:

```jsx
// eslint-disable-next-line distyl-design-system/no-hardcoded-colors -- third-party component requires raw value
```

Suppression without a comment will be flagged in code review.
