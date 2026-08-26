import { describe, expect, it } from "vitest"

import type { CitationBundle } from "./citation-model"
import { safeCitationResolver, tokenizeCitableText } from "./citation-model"

const bundle: CitationBundle = {
  version: 1,
  citations: {
    deadbeef: {
      label: "Service manual",
      anchors: ["Inspect the inlet before resetting the motor."],
      sourceId: "manual-1",
    },
  },
  sources: [
    {
      sourceId: "manual-1",
      title: "Pump service manual",
      resolver: "/sources/manual-1",
    },
  ],
}

describe("tokenizeCitableText", () => {
  it("turns only bundle-verified markers into citation tokens", () => {
    expect(
      tokenizeCitableText(
        "Inspect the inlet. 【mrkr: ||Service manual|| deadbeef】",
        bundle
      )
    ).toEqual([
      { kind: "text", text: "Inspect the inlet. " },
      {
        kind: "citation",
        markerId: "deadbeef",
        ordinal: 1,
        label: "Service manual",
        anchors: ["Inspect the inlet before resetting the motor."],
        source: bundle.sources[0],
      },
    ])
  })

  it("removes unknown, mislabeled, and malformed citation-looking tokens", () => {
    const tokens = tokenizeCitableText(
      [
        "A 【mrkr: ||Unknown|| c0ffee00】",
        "B 【mrkr: ||Wrong label|| deadbeef】",
        "C 【mrkr: broken】",
      ].join(" "),
      bundle
    )
    const renderedText = tokens
      .filter((token) => token.kind === "text")
      .map((token) => token.text)
      .join("")
    expect(renderedText).not.toContain("mrkr:")
    expect(tokens.some((token) => token.kind === "citation")).toBe(false)
  })

  it("rejects ambiguous source ids", () => {
    const ambiguous = { ...bundle, sources: [...bundle.sources, { ...bundle.sources[0] }] }
    expect(tokenizeCitableText("Claim. 【mrkr: ||Service manual|| deadbeef】", ambiguous)).toEqual([
      { kind: "text", text: "Claim. " },
    ])
  })
})

describe("safeCitationResolver", () => {
  it("accepts relative and HTTP(S) targets", () => {
    expect(safeCitationResolver("/sources/1")).toBe("/sources/1")
    expect(safeCitationResolver("https://example.com/source")).toBe(
      "https://example.com/source"
    )
  })

  it("rejects protocol-relative and active-content targets", () => {
    expect(safeCitationResolver("//evil.example/source")).toBeNull()
    expect(safeCitationResolver("javascript:alert(1)")).toBeNull()
  })
})
