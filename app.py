"""Nyāya — Adversarial Legal Reasoning · Streamlit application."""
from __future__ import annotations

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(
    page_title="Nyāya — AI Legal Reasoning",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Design system ──────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap');

:root {
    --ground:      #0C1018;
    --surface:     #141B27;
    --surface-2:   #1C2438;
    --border:      #1E2840;
    --text:        #E4DDD1;
    --text-muted:  #7A8599;
    --accent:      #C49A3C;
    --pros:        #9E4040;
    --pros-light:  #D46060;
    --pros-bg:     rgba(158,64,64,0.10);
    --pros-border: rgba(158,64,64,0.40);
    --def:         #2E5F8A;
    --def-light:   #5A9BC0;
    --def-bg:      rgba(46,95,138,0.10);
    --def-border:  rgba(46,95,138,0.40);
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

.main .block-container { max-width: 1080px; padding: 2rem 2rem 5rem; }

@keyframes bar-enter   { from { width: 0 !important; opacity: 0; } }
@keyframes bar-enter-d { from { width: 0 !important; opacity: 0; } }
@keyframes slide-in    { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

.ny-header {
    display: flex; align-items: flex-end; justify-content: space-between;
    border-bottom: 1px solid var(--border); padding-bottom: 1.2rem; margin-bottom: 2rem;
}
.ny-wordmark {
    font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 900;
    color: var(--text); letter-spacing: -0.01em; margin: 0; line-height: 1;
}
.ny-tagline { font-size: 0.72rem; color: var(--text-muted); letter-spacing: 0.08em; text-transform: uppercase; margin-left: 1rem; }
.ny-badge { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.25rem 0.65rem; border-radius: 3px; background: rgba(196,154,60,0.12); border: 1px solid rgba(196,154,60,0.3); color: var(--accent); }
.ny-badge.missing { background: rgba(200,60,60,0.1); border-color: rgba(200,60,60,0.3); color: #C05050; }

.ny-section { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin: 2rem 0 0.75rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border); }

.ny-round-label { display: flex; align-items: center; gap: 0.75rem; margin: 2rem 0 0.75rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border); animation: slide-in 0.3s ease both; }
.ny-round-badge { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.2rem 0.55rem; border-radius: 2px; background: rgba(196,154,60,0.12); color: var(--accent); border: 1px solid rgba(196,154,60,0.25); }
.ny-round-text { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); }

.ny-casefile { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; animation: slide-in 0.35s ease both; }
.ny-cf-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }
.ny-cf-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem; }
.ny-cf-value { font-size: 0.88rem; color: var(--text); font-weight: 500; }
.ny-cf-value.bns { color: var(--accent); }
.ny-cf-value.ipc { color: #7A9BB5; }
.ny-q-list { list-style: none; padding: 0; margin: 0; }
.ny-q-list li { font-size: 0.83rem; color: var(--text); padding: 0.45rem 0; border-bottom: 1px solid var(--border); line-height: 1.55; display: flex; gap: 0.75rem; }
.ny-q-list li:last-child { border-bottom: none; }
.ny-q-num { font-size: 0.6rem; color: var(--accent); font-weight: 700; padding-top: 0.2rem; flex-shrink: 0; min-width: 1.5rem; }

.ny-scoreboard { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 1rem 1.4rem 1.1rem; margin: 0.5rem 0 0.5rem; animation: slide-in 0.35s ease both; }
.ny-sb-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.85rem; }
.ny-sb-title { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); }
.ny-sb-lead { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.15rem 0.5rem; border-radius: 3px; }
.ny-sb-lead.pros { background: var(--pros-bg); color: var(--pros-light); border: 1px solid var(--pros-border); }
.ny-sb-lead.def  { background: var(--def-bg);  color: var(--def-light);  border: 1px solid var(--def-border); }
.ny-sb-lead.bal  { background: rgba(196,154,60,0.08); color: var(--accent); border: 1px solid rgba(196,154,60,0.25); }
.ny-sb-bars { display: flex; flex-direction: column; gap: 0.55rem; margin-bottom: 0.85rem; }
.ny-sb-row { display: flex; align-items: center; gap: 0.75rem; }
.ny-sb-name { font-size: 0.68rem; color: var(--text-muted); font-weight: 600; width: 100px; flex-shrink: 0; letter-spacing: 0.03em; }
.ny-sb-track { flex: 1; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; position: relative; }
.ny-sb-fill-p { height: 100%; background: linear-gradient(90deg, #6B2020, #9E4040); border-radius: 4px; animation: bar-enter 0.7s cubic-bezier(0.16,1,0.3,1) both; }
.ny-sb-fill-d { height: 100%; background: linear-gradient(90deg, #1A3A5C, #2E5F8A); border-radius: 4px; animation: bar-enter-d 0.7s cubic-bezier(0.16,1,0.3,1) both; }
.ny-sb-score-val { font-size: 0.8rem; font-weight: 700; color: var(--text); width: 40px; text-align: right; flex-shrink: 0; }
.ny-sb-trend { font-size: 0.65rem; color: var(--text-muted); margin-left: 0.4rem; }
.ny-sb-divider { height: 1px; background: var(--border); margin: 0.7rem 0; }
.ny-sb-history { font-size: 0.68rem; color: var(--text-muted); line-height: 1.7; font-family: 'SF Mono', 'Consolas', monospace; letter-spacing: 0.02em; }
.ny-sb-history-round { display: inline-block; margin-right: 1.1rem; }
.ny-sb-history-round .rn { color: var(--accent); font-weight: 700; }
.ny-sb-history-round .ps { color: var(--pros-light); }
.ny-sb-history-round .ds { color: var(--def-light); }

.ny-args-row { display: flex; gap: 1rem; align-items: flex-start; animation: slide-in 0.3s ease both; }
.ny-args-col { flex: 1; min-width: 0; }
.ny-card { border-radius: 6px; padding: 1.25rem 1.4rem; margin-bottom: 0.75rem; border: 1px solid transparent; }
.ny-card.pros { background: var(--pros-bg); border-color: var(--pros-border); border-left: 3px solid var(--pros); }
.ny-card.def  { background: var(--def-bg);  border-color: var(--def-border);  border-left: 3px solid var(--def); }
.ny-card.pending { background: rgba(255,255,255,0.02); border-color: var(--border); border-style: dashed; opacity: 0.7; }
.ny-card-side { font-size: 0.58rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.9rem; }
.ny-card-side.pros { color: var(--pros-light); }
.ny-card-side.def  { color: var(--def-light); }
.ny-card-side.pending { color: var(--text-muted); }
.ny-claim { font-size: 0.84rem; color: var(--text); line-height: 1.7; margin-bottom: 0.75rem; padding-left: 1.4rem; position: relative; }
.ny-claim::before { content: attr(data-n); position: absolute; left: 0; top: 0.05rem; font-size: 0.58rem; font-weight: 700; color: var(--text-muted); }
.ny-cite-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.85rem; padding-top: 0.75rem; border-top: 1px solid var(--border); }
.ny-cite-label { font-size: 0.58rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); padding-top: 0.25rem; margin-right: 0.25rem; flex-shrink: 0; }
.ny-pill { font-size: 0.66rem; font-weight: 500; padding: 0.2rem 0.55rem; border-radius: 3px; background: rgba(196,154,60,0.1); border: 1px solid rgba(196,154,60,0.2); color: #D4B46C; font-family: 'SF Mono', 'Consolas', monospace; }
.ny-prec-pill { font-size: 0.66rem; font-style: italic; padding: 0.2rem 0.55rem; border-radius: 3px; background: rgba(255,255,255,0.04); border: 1px solid var(--border); color: var(--text-muted); }
.ny-rebuttal-block { margin-top: 0.9rem; padding: 0.75rem 1rem; background: rgba(0,0,0,0.2); border-radius: 4px; border-left: 2px solid var(--border); }
.ny-rebuttal-label { font-size: 0.56rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.4rem; }
.ny-rebuttal-text { font-size: 0.8rem; color: var(--text-muted); line-height: 1.65; }
.ny-pending-pulse { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: var(--text-muted); opacity: 0.5; margin-right: 0.5rem; vertical-align: middle; }

.ny-judge { background: var(--surface-2); border: 1px solid var(--border); border-radius: 6px; padding: 1.1rem 1.4rem; margin-top: 0; margin-bottom: 0.5rem; animation: slide-in 0.35s ease both; }
.ny-judge-title { font-size: 0.58rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.8rem; }
.ny-score-row { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.55rem; }
.ny-score-name { font-size: 0.68rem; color: var(--text-muted); font-weight: 600; width: 100px; flex-shrink: 0; }
.ny-score-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.ny-score-fill-p { height: 100%; background: linear-gradient(90deg, #6B2020, #9E4040); border-radius: 3px; animation: bar-enter 0.6s cubic-bezier(0.16,1,0.3,1) both; }
.ny-score-fill-d { height: 100%; background: linear-gradient(90deg, #1A3A5C, #2E5F8A); border-radius: 3px; animation: bar-enter-d 0.6s cubic-bezier(0.16,1,0.3,1) both; }
.ny-score-num { font-size: 0.75rem; font-weight: 700; color: var(--text); width: 36px; text-align: right; flex-shrink: 0; }
.ny-decision { display: inline-block; font-size: 0.58rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.6rem; border-radius: 3px; margin-top: 0.5rem; }
.ny-decision.loop { background: rgba(196,154,60,0.12); color: var(--accent); border: 1px solid rgba(196,154,60,0.3); }
.ny-decision.stop { background: rgba(46,95,138,0.15); color: #7AABCC; border: 1px solid rgba(46,95,138,0.3); }
.ny-judge-reason { font-size: 0.8rem; color: var(--text-muted); line-height: 1.65; margin-top: 0.7rem; padding-top: 0.7rem; border-top: 1px solid var(--border); }

.ny-audit { border-radius: 6px; padding: 1rem 1.4rem; border: 1px solid transparent; animation: slide-in 0.35s ease both; }
.ny-audit.pass { background: rgba(46,138,80,0.08); border-color: rgba(46,138,80,0.25); }
.ny-audit.fail { background: rgba(200,60,60,0.08); border-color: rgba(200,60,60,0.25); }
.ny-audit-title { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }
.ny-audit.pass .ny-audit-title { color: #4CAF80; }
.ny-audit.fail .ny-audit-title { color: #C05050; }
.ny-audit-body { font-size: 0.82rem; color: var(--text-muted); line-height: 1.55; }

.ny-hitl { background: var(--surface); border: 1px solid rgba(196,154,60,0.35); border-radius: 6px; padding: 1.4rem 1.6rem; margin: 1.5rem 0; }
.ny-hitl-title { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }
.ny-hitl-body { font-size: 0.84rem; color: var(--text-muted); line-height: 1.6; }

.ny-verdict-wrap { border-radius: 6px; overflow: hidden; margin-top: 0.5rem; animation: slide-in 0.4s ease both; }
.ny-verdict-panel { padding: 2.8rem 2rem; text-align: center; }
.ny-verdict-panel.liable      { background: rgba(158,64,64,0.15);  border: 1px solid rgba(158,64,64,0.4); }
.ny-verdict-panel.not_liable  { background: rgba(46,138,80,0.12);  border: 1px solid rgba(46,138,80,0.35); }
.ny-verdict-panel.inconclusive{ background: rgba(196,154,60,0.10); border: 1px solid rgba(196,154,60,0.35); }
.ny-verdict-ruling { font-family: 'Playfair Display', serif; font-size: 3.8rem; font-weight: 900; letter-spacing: -0.02em; line-height: 1; margin-bottom: 0.5rem; animation: slide-in 0.5s ease both; }
.liable       .ny-verdict-ruling { color: #D46060; }
.not_liable   .ny-verdict-ruling { color: #4CAF80; }
.inconclusive .ny-verdict-ruling { color: var(--accent); }
.ny-conf-wrap { display: flex; flex-direction: column; align-items: center; gap: 0.4rem; margin-top: 1.2rem; }
.ny-conf-label { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); }
.ny-conf-track { width: 220px; height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; }
.ny-conf-fill { height: 100%; border-radius: 4px; animation: bar-enter 0.8s cubic-bezier(0.16,1,0.3,1) both; }
.liable       .ny-conf-fill { background: linear-gradient(90deg, #6B2020, #D46060); }
.not_liable   .ny-conf-fill { background: linear-gradient(90deg, #1A5C35, #4CAF80); }
.inconclusive .ny-conf-fill { background: linear-gradient(90deg, #7A5020, var(--accent)); }
.ny-conf-value { font-size: 1.1rem; font-weight: 700; color: var(--text); }
.ny-conf-desc { font-size: 0.72rem; color: var(--text-muted); font-style: italic; }
.ny-verdict-body { padding: 1.6rem 1.8rem; background: var(--surface); border: 1px solid var(--border); border-top: none; border-radius: 0 0 6px 6px; }
.ny-verdict-score-row { display: flex; gap: 2rem; margin-bottom: 1.2rem; padding-bottom: 1.2rem; border-bottom: 1px solid var(--border); }
.ny-verdict-score-item { flex: 1; }
.ny-verdict-score-side { font-size: 0.58rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.4rem; }
.ny-verdict-score-side.pros { color: var(--pros-light); }
.ny-verdict-score-side.def  { color: var(--def-light); }
.ny-verdict-score-bar { height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; margin-bottom: 0.3rem; }
.ny-verdict-score-bar-fill-p { height: 100%; background: linear-gradient(90deg, #6B2020, #9E4040); border-radius: 3px; animation: bar-enter 0.8s cubic-bezier(0.16,1,0.3,1) 0.2s both; }
.ny-verdict-score-bar-fill-d { height: 100%; background: linear-gradient(90deg, #1A3A5C, #2E5F8A); border-radius: 3px; animation: bar-enter-d 0.8s cubic-bezier(0.16,1,0.3,1) 0.2s both; }
.ny-verdict-score-num { font-size: 0.72rem; color: var(--text-muted); }
.ny-verdict-reasoning { font-size: 0.88rem; color: var(--text); line-height: 1.8; margin-bottom: 1rem; }
.ny-verdict-cites { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.4rem; line-height: 1.6; }
.ny-verdict-disclaimer { font-size: 0.72rem; color: var(--text-muted); font-style: italic; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); }

div[data-testid="stButton"] button { border-radius: 4px; font-size: 0.8rem; letter-spacing: 0.05em; font-weight: 600; transition: all 0.15s ease; }
div[data-testid="stTextArea"] textarea { background: var(--surface) !important; border-color: var(--border) !important; color: var(--text) !important; font-size: 0.87rem; line-height: 1.7; border-radius: 5px; }
div[data-testid="stSelectbox"] > div { background: var(--surface) !important; border-color: var(--border) !important; border-radius: 5px; }
div[data-testid="stAlert"] { background: rgba(196,154,60,0.08) !important; border-color: rgba(196,154,60,0.3) !important; border-radius: 5px; }
</style>
"""


# ── Session state ──────────────────────────────────────────────────────────────

def _init_state() -> None:
    defaults: dict = {
        "phase": "idle",
        "thread_id": None,
        "facts_raw": "",
        "clerk_output": None,
        "rounds": [],
        "audit_result": None,
        "verdict": None,
        "error_msg": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _get_graph():
    if "graph" not in st.session_state:
        from langgraph.checkpoint.memory import MemorySaver
        from graph.court import build_graph
        st.session_state["graph"] = build_graph(checkpointer=MemorySaver())
    return st.session_state["graph"]


def _reset() -> None:
    for k in ["phase", "thread_id", "facts_raw", "clerk_output",
              "rounds", "audit_result", "verdict", "error_msg"]:
        st.session_state.pop(k, None)
    _init_state()


def _corpus_ready() -> bool:
    chroma_dir = Path(__file__).parent / "chroma_db"
    return chroma_dir.exists() and any(chroma_dir.iterdir())


def _pills_html(items: list[str], cls: str = "ny-pill") -> str:
    if not items:
        return "<span style='color:var(--text-muted);font-size:0.72rem'>—</span>"
    return " ".join(f"<span class='{cls}'>{s}</span>" for s in items[:6])


# ── Sample cases ───────────────────────────────────────────────────────────────

SAMPLE_CASES = {
    "Select a sample case…": "",
    "Theft with CCTV — BNS (Aug 2024)": (
        "On 15 August 2024, the accused Ravi Kumar, aged 27, entered a mobile phone retail "
        "shop — 'Smart Zone Electronics' — in Koramangala, Bengaluru at approximately 3:42 PM. "
        "The shop was busy with three other customers present. The shop owner, Mr. Arjun Shetty, "
        "was attending to a customer at the billing counter. Ravi picked up two Samsung Galaxy S24 "
        "smartphones (total retail value Rs 1,10,000) from an unlocked display shelf, concealed them "
        "inside a cloth shopping bag he had brought with him, and attempted to walk out through the "
        "main entrance without making any payment. He was stopped by a security guard, Mahesh, at "
        "the exit after the anti-theft alarm was triggered. The entire sequence was recorded on four "
        "CCTV cameras inside the store. The phones were recovered intact from his bag. Ravi claimed "
        "he 'forgot to pay' and had intended to return. No prior criminal record was found. No "
        "violence was used. The phones were in working condition when recovered."
    ),
    "Dowry death — IPC (Mar 2024)": (
        "On 14 March 2024, Sunita Devi, aged 24, was found dead at her matrimonial home in "
        "Patna, Bihar. The official cause of death was strangulation, confirmed by post-mortem "
        "conducted at Patna Medical College on 15 March 2024. Sunita had been married to the "
        "accused Rajesh Kumar for 18 months. Her parents filed a complaint stating that Rajesh "
        "and his parents had been demanding Rs 5 lakh additional dowry since the marriage and had "
        "subjected Sunita to physical and mental harassment. Sunita spoke to her mother by phone "
        "three days before her death, expressing fear for her life and stating she was being beaten "
        "for not bringing money from her parents. Two neighbours corroborated hearing arguments and "
        "sounds of physical altercation from the house on the night of 12 March. Rajesh claims "
        "Sunita died by suicide due to depression. No suicide note was found. Forensic examination "
        "found Sunita's skin cells under Rajesh's fingernails."
    ),
    "Grievous hurt — circumstantial (BNS)": (
        "On 3 November 2024, Mr. Harish Goel, aged 45, was found unconscious near the rear "
        "exit of Centurion Mall's underground parking lot in Hyderabad at 10:15 PM with severe "
        "head injuries. He remains in a coma. The accused, Vikram Singh aged 38, was Harish's "
        "business partner with whom he had a documented financial dispute over Rs 40 lakh. A "
        "restaurant waiter witnessed a heated argument between Vikram and Harish inside the mall "
        "at 8:30 PM. CCTV at the parking lot entrance shows Harish entering at 9:45 PM and "
        "Vikram's registered vehicle entering two minutes later at 9:47 PM. Vikram's jacket had "
        "a bloodstain on the left sleeve matching Harish's blood group B+. Vikram claims he went "
        "to his car to retrieve documents and did not encounter Harish."
    ),
    "Drug possession — NDPS Act (Sep 2024)": (
        "On 7 September 2024, officers from the Narcotics Control Bureau conducted a raid at "
        "Flat 4B, Sunrise Apartments, Vile Parle, Mumbai. The accused, Aakash Mehta, aged 31, "
        "was present in the flat. During the search, officers recovered 52 grams of heroin "
        "concealed inside a hollow book on a bookshelf. The flat is rented in Aakash's name. "
        "A mobile phone found on Aakash contained encrypted WhatsApp messages referencing "
        "'deliveries' and quantities consistent with drug transactions. Cash of Rs 2.3 lakh "
        "was found in a drawer. The search was authorised by a gazetted officer under Section "
        "42 NDPS but without a prior magistrate's warrant. No independent witness was present."
    ),
}


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    _init_state()
    st.markdown(CSS, unsafe_allow_html=True)

    corpus_ok = _corpus_ready()
    badge_cls = "ny-badge" if corpus_ok else "ny-badge missing"
    badge_text = "Corpus loaded" if corpus_ok else "Corpus not built"
    st.markdown(f"""
<div class='ny-header'>
  <div style='display:flex;align-items:baseline;gap:1rem'>
    <h1 class='ny-wordmark'>Ny&#257;ya</h1>
    <span class='ny-tagline'>Adversarial Legal Reasoning &middot; Indian Law</span>
  </div>
  <span class='{badge_cls}'>{badge_text}</span>
</div>""", unsafe_allow_html=True)

    if not corpus_ok:
        st.warning(
            "Legal corpus not built — citation validation will not work. "
            "Run `python -m ingestion.build_corpus` to build the RAG corpus."
        )

    if st.session_state.phase == "idle":
        st.markdown("<div class='ny-section'>Fact Scenario</div>", unsafe_allow_html=True)
        sample = st.selectbox(
            "Load a sample",
            options=list(SAMPLE_CASES.keys()),
            label_visibility="collapsed",
        )
        prefill = SAMPLE_CASES.get(sample, "")
        facts = st.text_area(
            "Facts",
            value=prefill,
            height=180,
            placeholder=(
                "Describe the facts of the case in detail — who, what, when, where, what evidence exists. "
                "Include the date of the offence."
            ),
            label_visibility="collapsed",
        )
        col_btn, col_note = st.columns([2, 6])
        with col_btn:
            go = st.button("Convene Court", type="primary", use_container_width=True)
        with col_note:
            st.markdown(
                "<p style='color:var(--text-muted);font-size:0.73rem;margin-top:0.5rem'>"
                "Educational simulation only &mdash; not legal advice.</p>",
                unsafe_allow_html=True,
            )
        if go:
            if not facts.strip():
                st.error("Please enter a fact scenario before convening court.")
            else:
                st.session_state.facts_raw = facts.strip()
                st.session_state.phase = "running"
                st.rerun()

    elif st.session_state.phase == "error":
        st.error(f"An error occurred: {st.session_state.error_msg}")
        if st.button("Reset and try again"):
            _reset()
            st.rerun()


if __name__ == "__main__":
    main()
