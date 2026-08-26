---
name: fe-ui-design
description: "Use when designing, implementing, refactoring, or auditing frontend UI that should follow the Distyl design system: token-compliant styling, shadcn wrapper usage, semantic component choice, themeable CSS variables, shared-vs-impl boundaries, and staged migration/enforcement via the Distyl ESLint rules."
---

# FE / UI Design

Use this skill for frontend UI work that should conform to the Distyl design system.

This skill is for:

- building new Distyl-style UI,
- refactoring existing UI onto the token system,
- choosing the right semantic component (`Button`, `Tag`, `Badge`, `Chip`, `Link`),
- enforcing themeable styling with CSS variables,
- keeping shared vs impl boundaries clean,
- setting up or using the Distyl ESLint enforcement rules.

## Default Workflow

1. Identify the task type:
   - new screen or component,
   - refactor / migration,
   - design-system audit,
   - token / theme / component-system setup.
2. Read only the references needed for that task.
3. Map the UI to semantic roles before writing code:
   - action,
   - navigation,
   - status,
   - label,
   - filter / toggle,
   - input,
   - container,
   - dialog / overlay.
4. Implement or redesign using:
   - shadcn wrapper components,
   - token-backed CSS variables for color,
   - standard Tailwind spacing / radius scale,
   - Distyl font rules.
5. Before finishing, check:
   - no hardcoded colors,
   - no direct Radix imports,
   - no arbitrary spacing values unless truly unavoidable,
   - no manual dark-mode color branches,
   - no component-semantic misuse,
   - no impl-specific logic leaking into shared space.

## Core Rules

### 1. Never Hardcode Color

Do not use:

- hex literals,
- `rgb()` / `hsl()`,
- Tailwind brand color utilities such as `text-purple-500`,
- separate light/dark color branches in component code.

Use semantic or component token variables instead.

Read [references/token_reference.md](references/token_reference.md) for the canonical token sets.

### 2. Use Distyl Font Rules

- UI text: `Lato, sans-serif`
- code / monospace only: `Roboto Mono, monospace`
- never use `Inter`, `system-ui`, or `AlliancePlatt` in product UI

### 3. Use shadcn Wrappers, Not Direct Radix

Import primitives from the wrapper layer, not from `@radix-ui/*`.

If the task is in `fe-distillery` or a repo with the same component architecture, read [references/frontend_repo_rules.md](references/frontend_repo_rules.md).

### 4. Respect Component Semantics

Choose components by meaning, not by visual convenience:

- `Button` = triggers an action
- `Link` = navigation
- `Tag` = non-interactive label
- `Badge` = non-interactive status / count
- `Chip` = interactive filter / toggle

If a UI element is clickable but not a primary action, it is often a `Chip` or `Link`, not a `Button`.

### 5. Use Token Scale for Spacing and Radius

Prefer:

- standard Tailwind spacing classes (`p-4`, `gap-2`, `mt-6`)
- token scale radius (`rounded-md`, `rounded-lg`, pills via full radius)

Avoid arbitrary values like:

- `p-[13px]`
- `gap-[7px]`
- one-off radius values

### 6. Dark Mode Belongs in the Token Layer

Do not manually encode color decisions with `dark:` utilities or parallel inline color branches when the token system should handle it.

### 7. Shared vs Impl Boundaries Matter

When working in multi-impl repos:

- shared primitives stay generic,
- shared components must work across implementations,
- impl-specific behavior stays in the impl layer,
- never move a customer/product-specific component into shared space for convenience.

Read [references/frontend_repo_rules.md](references/frontend_repo_rules.md) when boundary decisions matter.

### 8. Customer Theming Must Flow Through Primitives

A customer rebrand should be a primitive override, not a component rewrite.

Do not bake Distyl purple assumptions into component logic if the component should work under future brand overrides.

## Which Reference To Read

Read only what is relevant:

- [references/overview.md](references/overview.md)
  - use for package structure, rollout approach, and high-level design-system orientation
- [references/token_reference.md](references/token_reference.md)
  - use for token names, token architecture, component token mappings, semantic layers, and naming rules
- [references/frontend_repo_rules.md](references/frontend_repo_rules.md)
  - use when editing `fe-distillery`-style repos, resolving shared-vs-impl boundaries, imports, dark mode, and component semantics
- [references/generation_rules.md](references/generation_rules.md)
  - use when generating frontend code directly and you want the most compact rule set
- [references/eslint_rules.md](references/eslint_rules.md)
  - use when installing, configuring, auditing, or explaining design-system enforcement
- [references/handoff.md](references/handoff.md)
  - use for rationale, migration strategy, repo debt, rollout sequencing, and architecture decisions

## Task Patterns

### New UI

When building a new screen or component:

1. identify the semantic roles in the interface,
2. choose wrapper components first,
3. map states to semantic tokens,
4. keep colors token-backed and spacing scale-backed,
5. check whether any part should be a shared component vs impl-local component.

### Refactor / Migration

When migrating existing UI:

1. remove hardcoded colors first,
2. replace direct Radix usage with wrapper imports,
3. normalize spacing and radius,
4. correct semantic misuse of `Button` / `Badge` / `Tag` / `Chip`,
5. run or describe the relevant ESLint audit if enforcement is part of the task.

### Audit / Enforcement

When asked to audit or set up enforcement:

1. read [references/eslint_rules.md](references/eslint_rules.md),
2. identify which rules should apply immediately vs staged migration,
3. prefer report-first rollout when the repo has large existing debt,
4. keep new code strict even if legacy code is still migrating.

## Output Expectations

When producing UI code or recommendations under this skill:

- be explicit about token usage,
- be explicit about component semantics,
- call out any place where the current UI violates the design system,
- prefer concrete replacements over abstract advice,
- preserve themeability and dark-mode correctness,
- avoid average-looking defaults if the task is visual design, but stay inside the token system.

## Quick Pre-Ship Checklist

- Are all colors token-backed?
- Are fonts compliant?
- Are component choices semantically correct?
- Are spacing and radius on scale?
- Are imports going through wrappers?
- Is dark mode handled through tokens?
- Is impl-specific logic kept out of shared space?
- Would a customer primitive override still work without changing component code?
