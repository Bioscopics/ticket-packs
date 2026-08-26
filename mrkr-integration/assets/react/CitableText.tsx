import React, { useEffect, useId, useMemo, useRef, useState } from "react"

import type { CitableToken, CitationBundle } from "./citation-model"
import { safeCitationResolver, tokenizeCitableText } from "./citation-model"

type CitationToken = Extract<CitableToken, { kind: "citation" }>

export interface CitableTextProps {
  text: string
  citationBundle: CitationBundle
  className?: string
}

/**
 * Dependency-light fallback. Prefer adapting the parser to the host's existing
 * rich-text renderer and dialog/drawer components.
 */
export function CitableText({ text, citationBundle, className }: CitableTextProps) {
  const tokens = useMemo(
    () => tokenizeCitableText(text, citationBundle),
    [citationBundle, text]
  )
  const [active, setActive] = useState<CitationToken | null>(null)
  const dialogRef = useRef<HTMLDialogElement>(null)
  const titleId = useId()

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (active && !dialog.open) dialog.showModal()
    if (!active && dialog.open) dialog.close()
  }, [active])

  const resolver = safeCitationResolver(active?.source.resolver)

  return (
    <>
      <span className={["mrkr-citable-text", className].filter(Boolean).join(" ")}>
        {tokens.map((token, index) =>
          token.kind === "text" ? (
            <span key={`text-${index}`}>{token.text}</span>
          ) : (
            <button
              aria-haspopup="dialog"
              aria-label={`Open citation ${token.ordinal}: ${token.source.title}`}
              className="mrkr-citation-trigger"
              key={`${token.markerId}-${index}`}
              onClick={() => setActive(token)}
              type="button"
            >
              {token.ordinal}
            </button>
          )
        )}
      </span>
      <dialog
        aria-labelledby={titleId}
        className="mrkr-citation-dialog"
        onCancel={() => setActive(null)}
        onClose={() => setActive(null)}
        ref={dialogRef}
      >
        {active ? (
          <div className="mrkr-citation-dialog-body">
            <header className="mrkr-citation-dialog-header">
              <div>
                <p className="mrkr-citation-eyebrow">Citation {active.ordinal}</p>
                <h2 id={titleId}>{active.source.title}</h2>
              </div>
              <button
                aria-label="Close citation"
                className="mrkr-citation-close"
                onClick={() => setActive(null)}
                type="button"
              >
                ×
              </button>
            </header>
            <div className="mrkr-citation-excerpts">
              {active.anchors.length ? (
                active.anchors.slice(0, 3).map((anchor, index) => (
                  <blockquote key={`${active.markerId}-anchor-${index}`}>{anchor}</blockquote>
                ))
              ) : (
                <p>No retained excerpt is available.</p>
              )}
            </div>
            {resolver ? (
              <a className="mrkr-citation-open" href={resolver} rel="noreferrer" target="_blank">
                Open source
              </a>
            ) : null}
          </div>
        ) : null}
      </dialog>
    </>
  )
}
