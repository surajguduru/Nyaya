# AI Moot Court — Multi-Agent Adversarial Legal Reasoning

> **Disclaimer:** This system is an AI-powered educational simulation. It does **not** constitute legal advice. All outputs are for academic and research purposes only.

---

## Problem Statement

**User:** Law students, moot-court competitors, legal-aid paralegals, and citizens who need to understand how a case might be reasoned in an Indian court.

**Pain point:** Single-prompt LLMs give one-sided, ungrounded answers and routinely hallucinate Indian statute numbers — which is dangerous in a legal context. There is no accessible tool that (a) argues both sides rigorously, (b) grounds every claim in real statutory text, (c) applies the correct code regime (BNS vs IPC based on offence date), and (d) delivers a judge-adjudicated verdict with a citation-integrity guarantee.

**Solution:** A multi-agent moot court: two opposing advocate agents debate across up to 3 rounds, each retrieving real statute sections from a local RAG corpus. An independent Judge agent evaluates round quality and controls the loop. A Citation Auditor blocks any verdict containing hallucinated sections. A human legal reviewer approves before the verdict is finalised.

---

## System Architecture

```
                     ┌─────────────────────────────────────┐
                     │         AI Moot Court Graph          │
                     │          (LangGraph DAG)             │
                     └─────────────────────────────────────┘

Fact Scenario
     │
     ▼
┌─────────┐    ┌───────────────┐    ┌──────────────┐
│  Clerk  │───►│  Prosecution  │───►│   Defence    │
│ (Intake)│    │   Advocate    │    │   Advocate   │
└─────────┘    └───────────────┘    └──────────────┘
                      ▲ loop ◄──────────────┤
                      │                     ▼
                      │               ┌───────────┐
                      └───────────────│   Judge   │──► proceed_to_verdict
                                      └───────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │   Auditor    │ ◄─── deterministic
                                     │ (Citation    │       citation check
                                     │  Validator)  │
                                     └──────────────┘
                                            │ citations clean
                                            ▼
                                     ┌──────────────┐
                                     │ Human Review │ (HITL interrupt)
                                     └──────────────┘
                                            │ approved
                                            ▼
                                     ┌──────────────┐
                                     │   Verdict    │
                                     └──────────────┘
```

### Three Conditional Branches (Decision Points)

| Branch | Trigger | Options |
|--------|---------|---------|
| Code regime | Clerk extracts offence date | BNS (≥ Jul 2024) or IPC (< Jul 2024) |
| Judge routing | After each round | `another_round` (loop) or `proceed_to_verdict` |
| Auditor routing | After citation audit | `re-argue` (hallucinations found) or `hitl` (clean) |

---

## Agent Roles

| Agent | Role | Tools | Output Type |
|-------|------|-------|-------------|
| **Clerk** | Parses facts → structured CaseFile; sets code regime deterministically | None | `CaseFile` |
| **Prosecution Advocate** | Argues liability; must cite ≥2 statutes + 1 precedent | `statute_retrieval_tool`, `precedent_search_tool` | `Argument` |
| **Defence Advocate** | Argues exculpation; same citation requirements | `statute_retrieval_tool`, `precedent_search_tool` | `Argument` |
| **Judge** | Scores each round (1–10), decides loop vs proceed | None | `JudgeScore` |
| **Auditor** | Validates every cited statute against corpus; blocks hallucinations | `citation_validator_tool` | `CitationAuditResult` |

---

## AI vs Deterministic Steps

| Step | Type | Why |
|------|------|-----|
| Fact parsing (Clerk) | **AI** | Requires natural-language understanding to extract legal questions |
| Code regime selection | **Deterministic** | `offence_date < 2024-07-01 → IPC` — pure Python rule |
| Statute retrieval | **Deterministic** | Chroma vector search with metadata filter |
| Advocacy (Prosecution/Defence) | **AI** | Requires legal reasoning, argument construction, rebuttal |
| Round scoring (Judge) | **AI** | Requires evaluative judgment over transcript |
| Loop vs proceed decision | **Deterministic** | `round < MAX_ROUNDS AND score ≤ 5 → loop` |
| Citation validation (Auditor) | **Deterministic** | Exact metadata lookup in Chroma — no LLM involved |
| Verdict rendering | **AI** | Requires synthesis of all rounds into a reasoned conclusion |
| HITL gate | **Human** | High-stakes output; mandatory review before finalisation |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent framework | LangGraph (StateGraph + interrupt) |
| LLM | Groq — `llama-3.3-70b-versatile` (free tier) |
| Vector database | ChromaDB (local persistent, no Docker) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (free, local) |
| Precedent search | Tavily API (internet search) |
| Observability | LangSmith tracing |
| PDF parsing | PyMuPDF |
| Precedent scraping | BeautifulSoup4 + Indian Kanoon |

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in GROQ_API_KEY and TAVILY_API_KEY in .env
```

### 3. Build the legal corpus (RAG)
```bash
python -m ingestion.build_corpus
```
This downloads statute PDFs, scrapes landmark precedents, chunks them, and embeds into ChromaDB. Expect ~15–30 min on first run.

### 4. Run a case
```bash
# Interactive (with HITL prompt)
python -m cli.run_case "On 15 August 2024, accused Ravi was caught stealing..."

# From a file
python -m cli.run_case --file path/to/case.txt

# Auto-approve HITL (for demo/eval)
python -m cli.run_case --auto "Fact scenario here..."
```

### 5. Run the evaluation suite
```bash
python -m eval.evaluate
```

---

## Corpus Contents

### Statutes (RAG)
| Act | Regime | Year |
|-----|--------|------|
| Bharatiya Nyaya Sanhita (BNS) | BNS | 2023 |
| Bharatiya Nagarik Suraksha Sanhita (BNSS) | BNS | 2023 |
| Bharatiya Sakshya Adhiniyam (BSA) | BNS | 2023 |
| Indian Penal Code (IPC) | IPC | 1860 |
| Code of Criminal Procedure (CrPC) | IPC | 1973 |
| Constitution of India (Part III + IV) | CONST | 1950 |

### Precedents (Scraped from Indian Kanoon)
25+ landmark Supreme Court judgments across: fundamental rights, murder/culpable homicide, theft/robbery, bail, private defence, evidence law, and sentencing.

---

## Evaluation Results

| # | Case | Code Regime | Expected Ruling | Audit | Status |
|---|------|-------------|-----------------|-------|--------|
| 1 | Clear liability (CCTV theft) | BNS ✓ | liable | Pass | ✓ |
| 2 | Clear acquittal (verified alibi) | BNS ✓ | not_liable | Pass | ✓ |
| 3 | Borderline (circumstantial) | BNS ✓ | inconclusive | Pass | ✓ |
| 4 | Citation trap (hallucination test) | BNS ✓ | blocked by Auditor | Pass | ✓ |
| 5 | Pre-July 2024 offence | **IPC** ✓ | any | Pass | ✓ |

---

## Guardrails

- **Mandatory disclaimer** on every `Verdict` object — cannot be suppressed
- **HITL gate** — LangGraph `interrupt()` suspends graph; human must type `approve` before verdict is finalised
- **Citation validator** — deterministic Chroma metadata lookup, not LLM — cannot hallucinate
- **Max rounds cap** — controlled by `MOOT_COURT_MAX_ROUNDS` env var (default 3)
- **Refusal** — Clerk system prompt rejects personal legal advice requests framed as "my case"

---

## Limitations & Future Work

- RAG corpus covers the main statutes but not all subordinate legislation (rules, regulations)
- Precedent retrieval via Tavily is internet-dependent; could be replaced with a local precedent index
- LLM may still reason incorrectly even when citing real sections — the Auditor checks existence, not interpretation accuracy
- Future: add a sub-agent for sentencing guidelines and quantum of punishment

---

## Individual Contributions

| Contributor | Responsibilities |
|-------------|-----------------|
| **Suraj Guduru** | LangGraph graph architecture (`graph/state.py`, `graph/edges.py`, `graph/court.py`), Judge agent, CLI entry point, integration and evaluation harness |
| **Venkatesh** | RAG ingestion pipeline (`ingestion/download_statutes.py`, `chunker.py`, `embedder.py`, `build_corpus.py`), `rag/retriever.py`, `tools/statute_tool.py`, `tools/citation_validator.py` |
| **Thrishal** | Precedent scraping (`ingestion/scrape_kanoon.py`), `rag/precedent_search.py`, `tools/precedent_tool.py`, all agent system prompts (`agents/prompts.py`), Clerk/Prosecution/Defence/Auditor agent nodes, evaluation case scenarios |

---

## Project Structure

```
moot_court/
├── agents/          # 5 agent nodes + system prompts
├── cli/             # CLI entry point
├── corpus/          # Downloaded statutes + scraped precedents
├── eval/            # 5 evaluation cases + evaluator
├── graph/           # LangGraph state, edges, graph assembly
├── ingestion/       # Download, scrape, chunk, embed pipeline
├── rag/             # Retriever + precedent search
├── tools/           # LangChain tools (statute, precedent, citation validator)
└── utils/           # LLM factory
```
