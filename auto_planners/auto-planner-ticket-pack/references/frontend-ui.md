# Frontend UI Reference

- Load the target repository's documented frontend styling or design-system skill when available; do not substitute a global product convention.
- Before changing a portal, popout, overlay, or detached root, inspect how that repository scopes utilities, themes, and CSS variables. If the app root uses a scope wrapper or selector, preserve the same wrapper around content rendered outside that root.
- Ticket packs for detached-root UI changes should include an acceptance check that the rendered state still receives the repository's scoped utilities, themes, and semantic token colors.
