# Toolkit Frontend UI Reference

- For Toolkit app styling work, load the repo's `.agents/skills/frontend-styling/SKILL.md` when available.
- Portal/popout convention: UI rendered outside the app root with `createPortal` or a similar popout mechanism must reintroduce the app scope wrapper (`.dtk-<app>`, for example `.dtk-button`) around the portaled content. This preserves Tailwind `important: '.dtk-<app>'` scoping and app-local `--dtk-*` CSS variables.
- Ticket packs for portal/popout UI changes should include an acceptance check that the portaled state still receives scoped Tailwind utilities and semantic token colors.
