"""Portable MRKR adapter and finalizer reference.

Copy and adapt this module at an existing evidence/model boundary. It does not
own retrieval, persistence, authorization, model invocation, or UI behavior.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from mrkr import (
    MRKR_PATTERN,
    async_build_citable_packet_from_documents,
    build_citable_packet,
    scrub_all_markers,
    scrub_unverified_markers,
)

InvalidMarkerPolicy = Literal["raise", "remove"]

_MALFORMED_MRKR_PATTERN = re.compile(
    r"(?:【|〚|\[)\s*mrkr\s*:[^\n】〛\]]*(?:】|〛|\])?",
    re.IGNORECASE,
)


class CitationContractError(ValueError):
    """Raised when provider or model output violates the citation contract."""


@dataclass(frozen=True, slots=True)
class SourceRecord:
    """Model-external source metadata retained by the host application."""

    source_id: str
    label: str
    title: str
    resolver: str | None = None
    checksum: str | None = None

    def to_bundle_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "sourceId": self.source_id,
            "title": self.title,
        }
        if self.resolver is not None:
            result["resolver"] = self.resolver
        if self.checksum is not None:
            result["checksum"] = self.checksum
        return result


@dataclass(frozen=True, slots=True)
class TextSource:
    """Authorized text returned by a web, RAG, or internal-search adapter."""

    source_id: str
    label: str
    title: str
    text: str
    resolver: str | None = None
    checksum: str | None = None


@dataclass(frozen=True, slots=True)
class DocumentSource:
    """Authorized uploaded/stored document bytes and model-external metadata."""

    source_id: str
    filename: str
    title: str
    content: bytes
    mime_type: str | None = None
    resolver: str | None = None
    checksum: str | None = None


@dataclass(frozen=True, slots=True)
class ProviderEnvelope:
    """Current-invocation citable context plus model-external resolver state."""

    model_context: str
    valid_marker_ids: frozenset[str]
    match_hints: Mapping[str, Any]
    sources_by_label: Mapping[str, SourceRecord]
    source_index: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True, slots=True)
class FinalizedCitationText:
    """Sanitized model text and the backend-built bundle used by the UI."""

    text: str
    citation_bundle: Mapping[str, Any]
    diagnostics: Mapping[str, Any]


def _required(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise CitationContractError(f"{field_name} must be non-empty")
    return normalized


def _source_records(records: Sequence[SourceRecord]) -> dict[str, SourceRecord]:
    if not records:
        raise CitationContractError("at least one authorized source is required")
    by_label: dict[str, SourceRecord] = {}
    source_ids: set[str] = set()
    for record in records:
        label = _required(record.label, "source label")
        source_id = _required(record.source_id, "source id")
        _required(record.title, "source title")
        if label in by_label:
            raise CitationContractError(f"duplicate source label: {label}")
        if source_id in source_ids:
            raise CitationContractError(f"duplicate source id: {source_id}")
        by_label[label] = record
        source_ids.add(source_id)
    return by_label


def _strip_source_markers(text: str) -> str:
    """Prevent retrieved content from injecting an unregistered marker."""
    without_canonical = scrub_all_markers(text).text
    return _MALFORMED_MRKR_PATTERN.sub("", without_canonical)


def _make_envelope(packet: Any, records: Sequence[SourceRecord]) -> ProviderEnvelope:
    sources_by_label = _source_records(records)
    marker_ids = frozenset(packet.marker_ids)
    hints = packet.citation_match_hints
    citations = hints.get("citations", {}) if isinstance(hints, Mapping) else {}
    if marker_ids != frozenset(citations):
        raise CitationContractError("packet marker ids and match hints disagree")

    for match in MRKR_PATTERN.finditer(packet.text):
        label, marker_id = match.group(1), match.group(2)
        hint = citations.get(marker_id)
        if hint is None:
            raise CitationContractError(f"provider context contains unregistered marker id: {marker_id}")
        if hint.get("label") != label:
            raise CitationContractError(f"provider context label mismatch for marker id: {marker_id}")
        if label not in sources_by_label:
            raise CitationContractError(f"no source record for packet label: {label}")

    return ProviderEnvelope(
        model_context=packet.text,
        valid_marker_ids=marker_ids,
        match_hints=hints,
        sources_by_label=sources_by_label,
        source_index=tuple(packet.source_index),
    )


def build_text_envelope(
    sources: Sequence[TextSource],
    *,
    additional_citation_requirements: Sequence[str] | None = None,
) -> ProviderEnvelope:
    """Build a packet from authorized web, RAG, or internal source text."""
    records: list[SourceRecord] = []
    documents: list[dict[str, str]] = []
    for source in sources:
        label = _required(source.label, "source label")
        text = _strip_source_markers(_required(source.text, "source text"))
        if not text.strip():
            raise CitationContractError(f"source is empty after marker sanitization: {label}")
        records.append(
            SourceRecord(
                source_id=source.source_id,
                label=label,
                title=source.title,
                resolver=source.resolver,
                checksum=source.checksum,
            )
        )
        documents.append({"text": text, "label": label})

    _source_records(records)
    packet = build_citable_packet(
        documents,
        additional_citation_requirements=additional_citation_requirements,
    )
    return _make_envelope(packet, records)


async def build_document_envelope(
    documents: Sequence[DocumentSource],
    *,
    additional_citation_requirements: Sequence[str] | None = None,
) -> ProviderEnvelope:
    """Build a packet from authorized document bytes using package extraction."""
    document_by_filename: dict[str, DocumentSource] = {}
    source_ids: set[str] = set()
    packet_documents: list[dict[str, Any]] = []
    for document in documents:
        filename = _required(document.filename, "document filename")
        if not document.content:
            raise CitationContractError(f"document content is empty: {filename}")
        if filename in document_by_filename:
            raise CitationContractError(f"duplicate document filename: {filename}")
        source_id = _required(document.source_id, "source id")
        if source_id in source_ids:
            raise CitationContractError(f"duplicate source id: {source_id}")
        document_by_filename[filename] = document
        source_ids.add(source_id)
        packet_documents.append(
            {
                "content": document.content,
                "filename": filename,
                "mime_type": document.mime_type,
            }
        )

    packet = await async_build_citable_packet_from_documents(
        packet_documents,
        additional_citation_requirements=additional_citation_requirements,
    )
    records: list[SourceRecord] = []
    indexed_filenames: set[str] = set()
    for entry in packet.source_index:
        filename = entry.get("filename")
        label = entry.get("label")
        if not isinstance(filename, str) or not isinstance(label, str):
            raise CitationContractError("document packet source index is incomplete")
        document = document_by_filename.get(filename)
        if document is None or filename in indexed_filenames:
            raise CitationContractError("document packet source index is ambiguous")
        records.append(
            SourceRecord(
                source_id=document.source_id,
                label=label,
                title=document.title,
                resolver=document.resolver,
                checksum=document.checksum or entry.get("source_checksum"),
            )
        )
        indexed_filenames.add(filename)
    if indexed_filenames != set(document_by_filename):
        raise CitationContractError("document packet omitted an authorized source")
    return _make_envelope(packet, records)


def _remove_or_raise_malformed(text: str, policy: InvalidMarkerPolicy) -> str:
    text_without_canonical = MRKR_PATTERN.sub("", text)
    if not _MALFORMED_MRKR_PATTERN.search(text_without_canonical):
        return text
    if policy == "raise":
        raise CitationContractError("model output contains malformed MRKR syntax")
    parts: list[str] = []
    cursor = 0
    for match in MRKR_PATTERN.finditer(text):
        parts.append(_MALFORMED_MRKR_PATTERN.sub("", text[cursor : match.start()]))
        parts.append(match.group(0))
        cursor = match.end()
    parts.append(_MALFORMED_MRKR_PATTERN.sub("", text[cursor:]))
    return "".join(parts)


def finalize_text(
    model_output: str,
    envelope: ProviderEnvelope,
    *,
    require_citation: bool = False,
    invalid_marker_policy: InvalidMarkerPolicy = "raise",
) -> FinalizedCitationText:
    """Verify a designated text field and build its UI citation bundle."""
    if invalid_marker_policy not in {"raise", "remove"}:
        raise CitationContractError("invalid marker policy must be 'raise' or 'remove'")

    scrub_mode = "keep" if invalid_marker_policy == "raise" else "remove"
    candidate, scrub_stats = scrub_unverified_markers(
        model_output,
        set(envelope.valid_marker_ids),
        mode=scrub_mode,
    )
    if scrub_stats.invalid_markers and invalid_marker_policy == "raise":
        invalid = ", ".join(scrub_stats.invalid_ids)
        raise CitationContractError(f"model output contains unknown marker ids: {invalid}")

    candidate = _remove_or_raise_malformed(candidate, invalid_marker_policy)
    citations = envelope.match_hints.get("citations", {})
    wrong_labels: list[str] = []
    for match in MRKR_PATTERN.finditer(candidate):
        label, marker_id = match.group(1), match.group(2)
        expected = citations.get(marker_id, {}).get("label")
        if expected != label:
            wrong_labels.append(marker_id)
    if wrong_labels and invalid_marker_policy == "raise":
        raise CitationContractError(
            "model output changes provider labels for marker ids: " + ", ".join(sorted(set(wrong_labels)))
        )
    if wrong_labels:
        rejected = set(wrong_labels)
        candidate = MRKR_PATTERN.sub(
            lambda match: "" if match.group(2) in rejected else match.group(0),
            candidate,
        )

    bundle_citations: dict[str, dict[str, Any]] = {}
    used_source_ids: set[str] = set()
    for match in MRKR_PATTERN.finditer(candidate):
        label, marker_id = match.group(1), match.group(2)
        hint = citations.get(marker_id)
        source = envelope.sources_by_label.get(label)
        if hint is None or source is None:
            raise CitationContractError(f"marker cannot resolve to a source: {marker_id}")
        bundle_citations[marker_id] = {
            "label": label,
            "anchors": list(hint.get("anchors", [])),
            "sourceId": source.source_id,
        }
        used_source_ids.add(source.source_id)

    if require_citation and not bundle_citations:
        raise CitationContractError("at least one verified citation is required")

    bundle_sources = [
        source.to_bundle_dict() for source in envelope.sources_by_label.values() if source.source_id in used_source_ids
    ]
    return FinalizedCitationText(
        text=candidate,
        citation_bundle={
            "version": 1,
            "citations": bundle_citations,
            "sources": bundle_sources,
        },
        diagnostics={
            "totalMarkers": scrub_stats.total_markers,
            "validIdMarkers": scrub_stats.valid_markers,
            "unknownIdMarkers": scrub_stats.invalid_markers,
            "wrongLabelMarkers": len(wrong_labels),
        },
    )


def project_history_text(text: str) -> str:
    """Remove current/old canonical markers from a prompt-only history copy."""
    return scrub_all_markers(text).text


def validate_persisted_result(
    text: str,
    citation_bundle: Mapping[str, Any],
    *,
    require_citation: bool = False,
) -> None:
    """Validate the internal consistency of a sanitized persisted/API result."""
    if citation_bundle.get("version") != 1:
        raise CitationContractError("citation bundle version must be 1")
    citations = citation_bundle.get("citations")
    sources = citation_bundle.get("sources")
    if not isinstance(citations, Mapping) or not isinstance(sources, list):
        raise CitationContractError("citation bundle has an invalid shape")

    source_by_id: dict[str, Mapping[str, Any]] = {}
    for source in sources:
        if not isinstance(source, Mapping):
            raise CitationContractError("citation source rows must be objects")
        source_id = source.get("sourceId")
        if not isinstance(source_id, str) or not source_id or source_id in source_by_id:
            raise CitationContractError("citation source ids must be unique non-empty strings")
        source_by_id[source_id] = source

    text = _remove_or_raise_malformed(text, "raise")
    referenced: set[str] = set()
    used_source_ids: set[str] = set()
    for match in MRKR_PATTERN.finditer(text):
        label, marker_id = match.group(1), match.group(2)
        entry = citations.get(marker_id)
        if not isinstance(entry, Mapping) or entry.get("label") != label:
            raise CitationContractError(f"unresolved or mislabeled citation: {marker_id}")
        source_id = entry.get("sourceId")
        if not isinstance(source_id, str) or source_id not in source_by_id:
            raise CitationContractError(f"citation has no retained source: {marker_id}")
        referenced.add(marker_id)
        used_source_ids.add(source_id)

    if set(citations) != referenced:
        raise CitationContractError("citation bundle contains missing or unreferenced ids")
    if set(source_by_id) != used_source_ids:
        raise CitationContractError("citation bundle contains missing or unreferenced sources")
    if require_citation and not referenced:
        raise CitationContractError("at least one citation is required")
