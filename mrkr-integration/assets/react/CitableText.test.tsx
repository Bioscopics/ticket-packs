import "@testing-library/jest-dom/vitest"

import { cleanup, render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import React from "react"
import { afterEach, beforeAll, describe, expect, it } from "vitest"

import { CitableText } from "./CitableText"
import type { CitationBundle } from "./citation-model"

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

beforeAll(() => {
  HTMLDialogElement.prototype.showModal = function showModal() {
    this.setAttribute("open", "")
  }
  HTMLDialogElement.prototype.close = function close() {
    this.removeAttribute("open")
    this.dispatchEvent(new Event("close"))
  }
})

afterEach(cleanup)

describe("CitableText", () => {
  it("opens an accessible source dialog from a verified citation", async () => {
    const user = userEvent.setup()
    render(
      <CitableText
        citationBundle={bundle}
        text="Inspect the inlet. 【mrkr: ||Service manual|| deadbeef】"
      />
    )

    await user.click(screen.getByRole("button", { name: "Open citation 1: Pump service manual" }))
    expect(screen.getByRole("dialog")).toHaveAttribute("open")
    expect(screen.getByRole("heading", { name: "Pump service manual" })).toBeVisible()
    expect(screen.getByText("Inspect the inlet before resetting the motor.")).toBeVisible()
    expect(screen.getByRole("link", { name: "Open source" })).toHaveAttribute(
      "href",
      "/sources/manual-1"
    )
  })

  it("does not expose an unresolved raw marker", () => {
    render(
      <CitableText
        citationBundle={bundle}
        text="Unsafe. 【mrkr: ||Unknown|| c0ffee00】"
      />
    )
    expect(screen.queryByText(/mrkr:/i)).not.toBeInTheDocument()
    expect(screen.queryByRole("button", { name: /Open citation/i })).not.toBeInTheDocument()
  })
})
