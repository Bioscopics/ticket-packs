export interface CitationEntry {
  label: string
  anchors: string[]
  sourceId: string
}

export interface CitationSource {
  sourceId: string
  title: string
  resolver?: string | null
  checksum?: string | null
}

export interface CitationBundle {
  version: 1
  citations: Record<string, CitationEntry>
  sources: CitationSource[]
}

export type CitableToken =
  | { kind: "text"; text: string }
  | {
      kind: "citation"
      markerId: string
      ordinal: number
      label: string
      anchors: string[]
      source: CitationSource
    }

const MRKR_PATTERN_SOURCE = String.raw`【mrkr: \|\|([^|\r\n]+)\|\| ([a-f0-9]{8})】`
const MALFORMED_MRKR_PATTERN = /(?:【|〚|\[)\s*mrkr\s*:[^\n】〛\]]*(?:】|〛|\])?/gi

function markerPattern(): RegExp {
  return new RegExp(MRKR_PATTERN_SOURCE, "g")
}

function stripMarkerLikeText(text: string): string {
  return text.replace(MALFORMED_MRKR_PATTERN, "")
}

function pushText(tokens: CitableToken[], value: string): void {
  const text = stripMarkerLikeText(value)
  if (!text) return
  const prior = tokens.at(-1)
  if (prior?.kind === "text") {
    prior.text += text
  } else {
    tokens.push({ kind: "text", text })
  }
}

function sourceIndex(bundle: CitationBundle): Map<string, CitationSource> | null {
  const byId = new Map<string, CitationSource>()
  for (const source of bundle.sources) {
    if (!source.sourceId || byId.has(source.sourceId)) return null
    byId.set(source.sourceId, source)
  }
  return byId
}

export function tokenizeCitableText(text: string, bundle: CitationBundle): CitableToken[] {
  if (bundle.version !== 1) return [{ kind: "text", text: stripMarkerLikeText(text) }]
  const sources = sourceIndex(bundle)
  if (!sources) return [{ kind: "text", text: stripMarkerLikeText(text) }]

  const tokens: CitableToken[] = []
  const ordinals = new Map<string, number>()
  let cursor = 0
  for (const match of text.matchAll(markerPattern())) {
    const offset = match.index ?? 0
    pushText(tokens, text.slice(cursor, offset))

    const label = match[1]
    const markerId = match[2]
    const citation = bundle.citations[markerId]
    const source = citation ? sources.get(citation.sourceId) : undefined
    if (citation && source && citation.label === label) {
      let ordinal = ordinals.get(markerId)
      if (ordinal === undefined) {
        ordinal = ordinals.size + 1
        ordinals.set(markerId, ordinal)
      }
      tokens.push({
        kind: "citation",
        markerId,
        ordinal,
        label,
        anchors: citation.anchors,
        source,
      })
    }
    cursor = offset + match[0].length
  }
  pushText(tokens, text.slice(cursor))
  return tokens
}

export function safeCitationResolver(resolver?: string | null): string | null {
  if (!resolver) return null
  if (resolver.startsWith("/") && !resolver.startsWith("//")) return resolver
  try {
    const parsed = new URL(resolver)
    return parsed.protocol === "https:" || parsed.protocol === "http:" ? resolver : null
  } catch {
    return null
  }
}
