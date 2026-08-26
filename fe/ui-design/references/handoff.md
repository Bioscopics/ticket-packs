# Distyl AI Design System — Full Context Handoff
**Version 1.1 · February 2026**

---

## 1. What We Built and Why

Distyl AI is building a multi-tenant design system to support fast-moving product development across multiple implementations (Tower, PennyCai, Platform, Coffey, Apprentice, Eagle). The goal is: one canonical base, infinite branded forks. A customer wants pink buttons and Arial fonts? That's one CSS file override — no component code changes needed.

The system is built on three principles:

- **Velocity** — new impls start from a complete, tested library, not from copying another impl
- **Scale** — customer theming is a token override, not a codebase fork
- **Enforcement** — ESLint rules make the right way the only way. No hardcoded values, no bypassed abstractions

---

## 2. What Has Been Built

### 2.1 Token System — COMPLETE

158 design tokens across three collections in the Figma Tokens file (Foundations project, Design System and Library workspace). Published as a team library.

| Collection | Count | Details |
|---|---|---|
| Primitives | 76 | Purple scale (50–950), gray scale (0–950), green/red/amber feedback colors, spacing (4px base), radius (none–full), typography (Lato, Roboto Mono), type sizes (xs–4xl), weights, line heights |
| Semantic | 37 | Purpose-named aliases: color/background/\*, color/text/\*, color/border/\*, color/icon/\*, color/feedback/\*. Light AND Dark modes built in. |
| Components | 46 | Scoped tokens: button/\*, tag/\*, badge/\*, input/\*, card/\*, dialog/\*, tooltip/\*, select/\*, chip/\* |

Three-layer alias chain: change a primitive → semantic updates → component updates → every Figma component using that token updates automatically.

### 2.2 Figma Plugin — COMPLETE

Custom Figma plugin (no third-party subscription required) that bootstraps all tokens in one shot.

- Location: `figma-plugin/` in this package
- Install: Figma → Plugins → Development → Import plugin from manifest
- Re-runnable anytime to reset or update the entire token set

### 2.3 ESLint Plugin — COMPLETE

Production-ready ESLint plugin enforcing the token system in code.

| Rule | Severity | What it catches |
|---|---|---|
| no-hardcoded-colors | error | Hex, rgb(), hsl() values in component files |
| no-direct-radix-imports | error | Direct @radix-ui/\* imports — use shadcn wrappers |
| no-impl-specific-shared-components | error | Impl components in shared space |
| no-hardcoded-spacing | warn | px values in inline style objects |
| no-deprecated-src-components | warn | Legacy src/ imports with ui/ equivalents |

Audit script runs report-only mode and produces a markdown summary. No CI impact.

### 2.4 Cursor Rules — COMPLETE

`.cursorrules` file for the fe-distillery repo root. Makes Cursor generate token-compliant code automatically — fonts, color tokens, component semantics, import rules, dark mode, shared vs impl boundaries.

### 2.5 Token Naming Specification — COMPLETE

Full governance document covering naming syntax, three-layer architecture, versioning rules (semantic versioning), deprecation process, dark mode strategy, and critical component definitions.

- Button vs Tag vs Badge vs Chip are semantically distinct — ends the "button for everything" pattern
- Versioning: add token = MINOR, rename/delete = MAJOR with 2-week deprecation, value change = PATCH

### 2.6 shadcn Kit — COMPLETE

Matt Wierzbicki shadcn/ui kit for Figma (Pro license, 25 users, February 2026). Duplicated into Components project, Tokens library enabled, four primary token swaps complete. Published as team library.

Brand expression: `primary-light` → `color/purple/500`, `primary-dark` → `color/purple/400`. Everything else stays as shipped — their neutral = our gray. "Mr. Shad has a new hat."

---

## 3. The Four Token Swaps (Already Done)

These four changes in the shadcn kit Theme collection complete the Distyl brand expression:

| Token | Was | Now |
|---|---|---|
| primary-light | tailwind colors/neutral/900 | color/purple/500 |
| primary-dark | tailwind colors/neutral/200 | color/purple/400 |
| primary-foreground-light | tailwind colors/neutral/50 | color/gray/0 |
| primary-foreground-dark | tailwind colors/neutral/900 | color/gray/0 |

---

## 4. Key Decisions

| Decision | Rationale |
|---|---|
| Don't touch Theme collection directly | Keep kit updatable — overrides reference our Tokens library so kit updates don't overwrite Distyl customizations |
| Purple is the only brand breakout | Everything else matches Tailwind defaults. No unnecessary divergence. |
| Lato + Roboto Mono only | AlliancePlatt is a marketing/website font, not a product UI font |
| ESLint warn during migration, error for new code | Staged rollout — new files error immediately, existing files migrate incrementally |
| Custom Figma plugin over Tokens Studio | Tokens Studio is $50/month with poor reviews. Plugin uses Figma Plugin API, fully owned by Distyl. |
| Three-layer token architecture | Primitives → Semantic → Component. Customer theming only touches primitives. |
| Branch not merge for customer themes | Base system is the law. Customer brand is a fork that inherits everything and overrides only what differs. |

---

## 5. Repo Audit Findings (fe-distillery)

### Top Components by Usage
| Component | Imports |
|---|---|
| Button | 360 — the "button for everything" problem |
| Input | 111 |
| Label | 108 |
| Card | 89 |
| Dialog | 86 |
| Badge | 85 |
| Tooltip | 66 |
| Select | 62 |

### Known Debt to Fix
- 8 unused components: calendar, carousel, drawer, expanding-textarea, input-otp, menubar, navigation-menu, slider
- 3 duplicate pairs: LabelWithInfo ×2, DynamicTextarea ×2, TagInput ×2
- CoffeyNavigation in shared space (should be impl-specific)
- Two toast systems: sonner (active) + toast/toaster (dead, remove)
- 4 files importing Radix directly (ESLint now catches new violations)
- penny.\* legacy colors — verify usage before removing

---

## 6. Tower Audit (Chat + Simulations)

Combined score: B+ (84.6%). The score measures shadcn adoption, not token compliance.

- Chat color token usage: 72% — hardcoded grays, `bg-[#f5f5f5]`, `border-black`
- Simulations color token usage: 87% — still uses `text-gray-*`, `border-gray-*` directly

**The reframe:** The Guidelines_General.md document defines rules in plain English because those decisions live nowhere in code. Our token system is that document translated into enforcement. The audit document itself is evidence of the cost — hours of manual work that the system makes automatic or unnecessary.

---

## 7. File Locations

| Item | Location |
|---|---|
| Figma workspace | Distyl AI → Design System and Library |
| Tokens file | Foundations project (published as library) |
| shadcn kit | Components project → shadcn/ui kit for Figma + Pro Blocks |
| fe-distillery repo | github.com/DistylAI/fe-distillery |
| ESLint plugin | fe-distillery/design-system/eslint-plugin/ |
| Figma plugin | fe-distillery/design-system/scripts/ |

---

## 8. Next Steps (In Order)

1. ~~Enable Tokens library in shadcn kit~~ ✅
2. ~~Four primary token swaps~~ ✅
3. ~~Publish both Figma libraries~~ ✅
4. **Commit plugin + ESLint plugin to fe-distillery** — first design system PR
5. **Install ESLint plugin in repo and run audit** — get baseline violation count
6. **Set up Code Connect** — bridge Figma components to React implementations
7. **Publish shadcn kit as library** — so all design files can consume components
8. **Component cleanup** — remove 8 unused, consolidate duplicates, fix 4 direct Radix imports

---

## 9. Open Questions

- penny.\* legacy colors — still used anywhere? Verify before removing
- CoffeyNavigation — confirm it can move to impls/coffey/ without breaking anything
- Code Connect — requires Figma Enterprise or developer add-on. Check current plan.
- shadcn kit Custom collection — Desktop/Mobile responsive typography. Adopt their scale or define Distyl-specific breakpoint tokens?
- Dark mode rollout — semantic tokens have modes built in. When to surface the toggle in product?

---

## 10. The Argument for Skeptics

**For FE Engineers:** The system removes decisions that were slowing you down invisibly. No more "what hex was that gray." No more rebuilt buttons per impl. ESLint catches drift before PR review — faster feedback, not slower.

**For Product Designers:** Constraints enable speed. The mundane decisions are already made. A full customer rebrand is one token file — more creative leverage, not less.

**The closing argument:** The Tower audit document exists because there was no system. Someone spent hours manually documenting what should be auto-generated or never needed. The audit shows 85% compliance through pure discipline. The system makes that automatic and protects it from regressing.

The question isn't whether to pay the cost. It's whether to pay it once upfront or continuously in small invisible chunks that never feel like a choice.

---

*Distyl AI Design System · Handoff Document · v1.1 · February 2026 · Owner: Tony Yates*
