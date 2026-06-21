"""Bias & Citation Integrity Auditor — validates every statutory citation deterministically."""
from __future__ import annotations

from graph.state import CitationAuditResult, GraphState
from rag.retriever import section_exists


def _collect_all_citations(transcript: list[dict]) -> list[str]:
    """Extract every unique statute citation from the trial transcript."""
    cited: set[str] = set()
    for argument in transcript:
        for s in argument.get("statutes_cited", []):
            cited.add(s.strip())
    return list(cited)


def auditor_node(state: GraphState) -> dict:
    """LangGraph node: deterministically validate all citations against the corpus."""
    transcript = state.get("round_transcript", [])
    all_citations = _collect_all_citations(transcript)

    verified: list[str] = []
    hallucinated: list[str] = []

    for citation in all_citations:
        if section_exists(citation):
            verified.append(citation)
        else:
            hallucinated.append(citation)

    passed = len(hallucinated) == 0
    notes = (
        f"Checked {len(all_citations)} citations. "
        f"{len(verified)} verified, {len(hallucinated)} not found in corpus."
    )
    if hallucinated:
        notes += f" Suspected hallucinations: {hallucinated}"

    audit = CitationAuditResult(
        hallucinated_citations=hallucinated,
        verified_citations=verified,
        audit_passed=passed,
        audit_notes=notes,
    )

    # Always set current_phase to "hitl" regardless of audit outcome.
    # The original "argue" value triggered an infinite re-argue loop:
    # LLM re-generated citations → new hallucinations → auditor failed again.
    return {
        "audit_result": audit.model_dump(),
        "audit_passed": passed,
        "current_phase": "hitl",
    }
