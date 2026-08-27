---
name: fe-ui-design
description: Design, implement, refactor, or audit frontend UI by discovering and following the target repository's existing design system, component boundaries, tokens, and enforcement rules. Use for repository-native UI work; do not invent or replace a design system unless the user asks.
---

# Frontend UI Design

Build UI that looks and behaves native to the target repository. Preserve the user's requested design while expressing it through the repository's established components, tokens, patterns, and boundaries.

## Discover Before Editing

Inspect the smallest relevant set of repository sources before choosing an implementation:

- repository instructions and framework guidance;
- theme, token, and global-style definitions;
- shared component wrappers or primitives;
- nearby screens that demonstrate current layout and interaction patterns;
- lint rules, generators, and visual or browser test commands.

Name the concrete components, tokens, and examples being reused. If the repository has no relevant system, follow its closest established convention and keep the new surface local. Do not introduce a new shared abstraction, dependency, token taxonomy, or styling framework without a demonstrated need.

## Implementation Contract

### Use Repository-Native Components

- Prefer existing semantic components and wrappers over raw primitives or parallel implementations.
- Choose elements by behavior: actions use action controls, navigation uses links, status and labels remain non-interactive, and filters or toggles expose their actual state.
- Preserve the wrapper layer when it owns accessibility, variants, analytics, or styling contracts.

### Use Semantic Tokens

- Use the repository's semantic color, typography, spacing, radius, elevation, and motion tokens where they exist.
- Avoid raw values or arbitrary utilities when an established token represents the same role.
- Do not assume token names or values from another repository.
- When a needed token is missing, first check whether an existing semantic role fits. Add or extend a token only when the task truly requires a reusable role.

### Keep Themes at the Token Layer

Theme variants should override primitive or semantic token values. Avoid component-level theme branches, copied themed components, or hardcoded brand choices when the existing token layer can express the difference.

### Preserve Ownership Boundaries

- Keep shared primitives generic and reusable.
- Keep feature-specific behavior and domain logic in the owning feature.
- Promote a component to shared space only when more than one real consumer needs the same stable contract.
- Do not move logic across boundaries merely to make the current change convenient.

### Preserve User Experience

Verify the changed flow at representative viewport sizes and input methods. Preserve:

- keyboard access, focus visibility, and semantic structure;
- labels, validation, empty, loading, error, and disabled states;
- usable overflow, content wrapping, and touch targets;
- readable contrast and reduced-motion behavior where supported.

## Modes

### Build or Refactor

1. Identify the user flow and relevant UI states.
2. Reuse the nearest native layout and components.
3. Express visual decisions through existing semantic tokens.
4. Keep the diff within the owning feature unless a shared contract is clearly required.
5. Exercise the real user flow early, then run the narrow repository checks that cover the touched surface.

### Audit

Report findings by user impact and include a concrete repository-native replacement. Prioritize broken interaction, accessibility, responsiveness, theme behavior, and boundary violations over cosmetic preference.

### Design-System Migration or Enforcement

Treat broad migration and new enforcement as separate scope unless explicitly requested. When requested:

- inventory existing violations before choosing strictness;
- use the repository's own lint or codemod infrastructure when present;
- keep new and touched code compliant without requiring unrelated cleanup;
- stage enforcement when immediate strictness would fail on untouched legacy code.

## Completion Evidence

Report:

- repository-native components and tokens reused;
- any new component or token and why reuse was insufficient;
- accessibility and responsive states exercised;
- exact lint, type, build, or browser-flow validation run;
- any remaining limitation or repository rule that could not be verified.

Do not claim conformance from compilation alone when the change affects an interactive user flow.
