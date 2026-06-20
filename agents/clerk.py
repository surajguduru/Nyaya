"""Clerk / Intake agent — parses raw facts into a structured CaseFile."""
from __future__ import annotations

import re
from datetime import date, datetime

from langchain_core.messages import HumanMessage, SystemMessage

from agents.prompts import CLERK_SYSTEM
from graph.state import CaseFile, GraphState
from utils.llm import get_structured_llm


_BNS_CUTOVER = date(2024, 7, 1)

_DATE_FMTS = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%B %d, %Y", "%d %B %Y"]


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    for fmt in _DATE_FMTS:
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    # Last resort: extract 4-digit year and check
    m = re.search(r"\b(\d{4})\b", s)
    if m:
        try:
            return date(int(m.group(1)), 1, 1)
        except ValueError:
            pass
    return None


def _determine_regime(offence_date_str: str | None) -> str:
    d = _parse_date(offence_date_str)
    if d is None:
        return "BNS"
    return "BNS" if d >= _BNS_CUTOVER else "IPC"


def clerk_node(state: GraphState) -> dict:
    """LangGraph node: parse the user's fact-scenario into a CaseFile."""
    facts_raw: str = state.get("facts_raw", "")

    structured_llm = get_structured_llm(CaseFile)

    _schema_hint = (
        '{"facts": "...", "legal_questions": ["...", "..."], '
        '"code_regime": "BNS", "offence_date": "YYYY-MM-DD or null", '
        '"accused_name": "...", "offence_type": "..."}'
    )

    messages = [
        SystemMessage(content=CLERK_SYSTEM),
        HumanMessage(
            content=(
                f"Parse the following fact-scenario into a structured CaseFile.\n"
                f"Return ONLY a valid JSON object with exactly these keys:\n"
                f"{_schema_hint}\n\n"
                f"FACT SCENARIO:\n{facts_raw}"
            )
        ),
    ]

    case_file: CaseFile = structured_llm.invoke(messages)

    # Deterministic override of code_regime based on offence date (string → date parse)
    case_file.code_regime = _determine_regime(case_file.offence_date)

    return {
        "case_file": case_file,
        "current_round": 1,
        "current_phase": "argue",
        "round_transcript": [],
        "judge_scores": [],
        "audit_result": None,
        "audit_passed": False,
        "hitl_approved": False,
        "verdict": None,
        "error": None,
    }
