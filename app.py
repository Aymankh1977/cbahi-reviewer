# app.py — CBAHI Reviewer Main Application
# DentEdTech™ Platform
# Deployed via Streamlit Cloud — API key stored in st.secrets

import streamlit as st
import anthropic
import json
import io
from datetime import datetime, timedelta

from utils.cbahi_data import PROGRAMS, CHAPTERS, ESR_LIST, SCORING_THRESHOLDS, TOTAL_STANDARDS
from utils.ai_engine import run_analysis, parse_result, extract_text_from_file
from utils.report_generator import generate_html_report

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CBAHI Reviewer — DentEdTech™",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "mailto:support@dentedtech.com",
        "About": "CBAHI Reviewer by DentEdTech™ — AI-powered accreditation intelligence platform.",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background-color: #0A0E1A; }
section[data-testid="stSidebar"] { background: #0F1628; border-right: 1px solid rgba(255,255,255,0.06); }

/* Header */
.cbahi-header {
    background: linear-gradient(135deg, #0a0e1a 0%, #16213e 100%);
    border-bottom: 2px solid #C9A84C;
    padding: 28px 40px;
    margin: -20px -20px 32px -20px;
    display: flex; align-items: center; justify-content: space-between;
}
.cbahi-logo {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #C9A84C, #E8C870);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 22px; font-weight: 900; color: #0A0E1A;
    box-shadow: 0 4px 20px rgba(201,168,76,0.4);
    flex-shrink: 0;
}
.cbahi-title { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 900; color: #F0F4FF; letter-spacing: -0.5px; }
.cbahi-subtitle { font-size: 12px; color: #C9A84C; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
.cbahi-trademark { font-size: 12px; color: #4a5878; }

/* Metric cards */
.metric-card {
    background: #131C35; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 20px 22px; text-align: center;
    transition: all 0.2s;
}
.metric-card:hover { border-color: rgba(201,168,76,0.3); transform: translateY(-2px); }
.metric-value { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; line-height: 1; margin-bottom: 6px; }
.metric-label { font-size: 12px; color: #4a5878; text-transform: uppercase; letter-spacing: 1px; }

/* Score display */
.score-hero {
    background: #131C35; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 32px; margin-bottom: 24px;
    border-top: 3px solid #C9A84C;
}
.score-number { font-family: 'Playfair Display', serif; font-size: 72px; font-weight: 900; line-height: 1; }
.decision-text { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; margin-bottom: 10px; }

/* Chapter score cards */
.chapter-card {
    background: #131C35; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 16px; margin-bottom: 10px;
}
.chapter-code { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #00C9B1; background: rgba(0,201,177,0.1); padding: 2px 8px; border-radius: 4px; font-weight: 600; }

/* ESR cards */
.esr-met    { background: rgba(0,201,123,0.08);  border: 1px solid rgba(0,201,123,0.2);  border-radius: 10px; padding: 14px; margin-bottom: 8px; }
.esr-fail   { background: rgba(255,77,109,0.08); border: 1px solid rgba(255,77,109,0.2); border-radius: 10px; padding: 14px; margin-bottom: 8px; }
.esr-unknown{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; margin-bottom: 8px; }

/* Recommendation cards */
.rec-critical  { border-left: 4px solid #FF4D6D; background: rgba(255,77,109,0.06);  border-radius: 8px; padding: 16px; margin-bottom: 10px; }
.rec-important { border-left: 4px solid #C9A84C; background: rgba(201,168,76,0.06); border-radius: 8px; padding: 16px; margin-bottom: 10px; }
.rec-suggested { border-left: 4px solid #3D7FFF; background: rgba(61,127,255,0.06);  border-radius: 8px; padding: 16px; margin-bottom: 10px; }

/* Gap cards */
.gap-card { background: rgba(255,77,109,0.06); border: 1px solid rgba(255,77,109,0.15); border-radius: 10px; padding: 16px; margin-bottom: 10px; }

/* Timeline */
.phase-card { background: #131C35; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 20px; margin-bottom: 12px; }
.phase-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 6px; }

/* Sidebar labels */
.sidebar-label { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: #4a5878; font-weight: 700; margin-bottom: 8px; margin-top: 20px; padding-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.06); }

/* Section dividers */
.section-title { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: #F0F4FF; margin: 28px 0 16px; display: flex; align-items: center; gap: 10px; }
.section-title::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.06); }

/* Buttons */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    border-radius: 10px !important; transition: all 0.2s !important;
}

/* Progress bar colors */
.stProgress > div > div > div { background: linear-gradient(90deg, #C9A84C, #E8C870) !important; }

/* Status indicators */
.status-accredited { color: #00C97B; font-weight: 700; }
.status-conditional { color: #C9A84C; font-weight: 700; }
.status-denied { color: #FF4D6D; font-weight: 700; }

/* Info boxes */
.info-box { background: rgba(61,127,255,0.08); border: 1px solid rgba(61,127,255,0.2); border-radius: 10px; padding: 16px; margin-bottom: 16px; font-size: 14px; color: #8896b3; }

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# API CLIENT
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    """Initialise Anthropic client — key read from Streamlit secrets."""
    try:
        return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    except Exception:
        st.error("⚠️ API key not configured. Add `ANTHROPIC_API_KEY` to your Streamlit secrets.")
        st.stop()

client = get_client()

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for key, val in {
    "result": None,
    "raw_text": "",
    "facility": {},
    "program": "ambulatory",
    "uploaded_doc_texts": [],
    "uploaded_doc_names": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cbahi-header">
  <div style="display:flex;align-items:center;gap:16px;">
    <div class="cbahi-logo">CR</div>
    <div>
      <div class="cbahi-title">CBAHI Reviewer</div>
      <div class="cbahi-subtitle">DentEdTech™ · AI Accreditation Intelligence</div>
    </div>
  </div>
  <div class="cbahi-trademark">© 2025 DentEdTech™ · All Rights Reserved</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FACILITY INTAKE FORM
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">📋 Accreditation Program</div>', unsafe_allow_html=True)
    program = st.selectbox(
        "Program", options=list(PROGRAMS.keys()),
        format_func=lambda k: PROGRAMS[k], label_visibility="collapsed",
        key="program_select"
    )
    st.session_state.program = program

    st.markdown('<div class="sidebar-label">🏥 Facility Information</div>', unsafe_allow_html=True)
    facility_name     = st.text_input("Facility Name *", placeholder="e.g. Al-Noor Medical Center")
    facility_type     = st.selectbox("Facility Sub-type", [
        "General Polyclinic", "Specialty Clinic", "Dental Center",
        "Medical Complex", "Day Surgery Center", "Primary Health Center",
        "General Hospital", "Specialty Hospital", "Teaching Hospital",
        "Military / Government Hospital", "Private Hospital"
    ])
    capacity          = st.text_input("Capacity", placeholder="e.g. 200 beds  /  15 clinics")
    city              = st.text_input("City / Region", placeholder="e.g. Riyadh, Eastern Province")

    st.markdown('<div class="sidebar-label">📅 Survey Details</div>', unsafe_allow_html=True)
    survey_type       = st.selectbox("Survey Type", ["Initial Survey", "Triennial Re-accreditation", "Focused Survey", "Mock Survey"])
    prev_status       = st.selectbox("Previous Accreditation Status", [
        "Never Accredited", "Previously Accredited", "Conditionally Accredited",
        "Accreditation Denied", "Accreditation Suspended"
    ])
    est_compliance    = st.selectbox("Self-Estimated Compliance Level", [
        "Unknown", "Low (Below 50%)", "Medium (50–75%)", "High (75–90%)", "Very High (Above 90%)"
    ])
    default_date      = datetime.now() + timedelta(days=90)
    target_date       = st.date_input("Target Survey Date", value=default_date)

    st.markdown('<div class="sidebar-label">📂 Upload Documents</div>', unsafe_allow_html=True)
    st.caption("Policies, procedures, quality reports, organograms, etc.")
    uploaded_files = st.file_uploader(
        "Upload files", type=["pdf","docx","doc","xlsx","xls","txt","csv"],
        accept_multiple_files=True, label_visibility="collapsed"
    )

    if uploaded_files:
        st.session_state.uploaded_doc_texts = []
        st.session_state.uploaded_doc_names = []
        for f in uploaded_files:
            text = extract_text_from_file(f)
            st.session_state.uploaded_doc_texts.append(text)
            st.session_state.uploaded_doc_names.append(f.name)
        st.success(f"✅ {len(uploaded_files)} document(s) loaded")

    st.markdown('<div class="sidebar-label">📝 Chapter Selection</div>', unsafe_allow_html=True)
    all_chapters   = CHAPTERS.get(program, [])
    default_sel    = [c["code"] for c in all_chapters]
    chapter_labels = {c["code"]: f"{c['code']} — {c['name']}" for c in all_chapters}
    selected_ch    = st.multiselect(
        "Select chapters to analyze",
        options=list(chapter_labels.keys()),
        default=default_sel,
        format_func=lambda code: chapter_labels.get(code, code),
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-label">💬 Facility Description *</div>', unsafe_allow_html=True)
    description = st.text_area(
        "Describe current status",
        height=240,
        placeholder=(
            "Describe your facility's current state in as much detail as possible:\n\n"
            "• Governance structure and leadership team\n"
            "• Quality and patient safety programs\n"
            "• Credentialing and privileging process\n"
            "• Infection control practices\n"
            "• Policies and procedures status\n"
            "• Staff qualifications and training\n"
            "• Medical records and documentation\n"
            "• Equipment and facility management\n"
            "• Previous accreditation findings\n"
            "• Areas of concern or known gaps\n\n"
            "The more detail you provide, the more accurate the analysis."
        ),
        label_visibility="collapsed"
    )

    st.markdown("---")
    run_btn = st.button(
        "🚀 Run AI Analysis",
        use_container_width=True,
        type="primary",
        help="Runs a comprehensive CBAHI compliance analysis using Claude AI"
    )

# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT — TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_analyzer, tab_selfassess, tab_standards, tab_about = st.tabs([
    "🔍 AI Analyzer", "📋 Self-Assessment", "📚 Standards Explorer", "ℹ️ About"
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — AI ANALYZER
# ═════════════════════════════════════════════════════════════════════════════
with tab_analyzer:

    # ── OVERVIEW METRICS ──
    chapters_data = CHAPTERS.get(program, [])
    total_stds    = TOTAL_STANDARDS.get(program, 0)
    total_esrs    = len(ESR_LIST.get(program, []))
    total_chaps   = len(chapters_data)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, color in [
        (c1, total_stds,  "Total Standards",  "#C9A84C"),
        (c2, total_chaps, "Chapters",          "#3D7FFF"),
        (c3, total_esrs,  "ESR Requirements",  "#FF4D6D"),
        (c4, PROGRAMS[program].split("(")[0].strip(), "Program", "#00C9B1"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:{color};">{val}</div>
              <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RUN ANALYSIS ──
    if run_btn:
        if not facility_name.strip():
            st.error("❌ Please enter a facility name.")
        elif not description.strip() or len(description.strip()) < 40:
            st.error("❌ Please provide a more detailed facility description (at least 40 characters).")
        else:
            # Build facility dict
            doc_texts = "\n\n---\n\n".join(
                f"### Document: {name}\n{text}"
                for name, text in zip(
                    st.session_state.uploaded_doc_names,
                    st.session_state.uploaded_doc_texts
                )
            )
            full_desc = description
            if doc_texts:
                full_desc += f"\n\n═══ UPLOADED DOCUMENTS ═══\n{doc_texts[:12000]}"  # cap at 12k chars

            facility = {
                "name": facility_name,
                "facility_type": facility_type,
                "capacity": capacity,
                "city": city,
                "survey_type": survey_type,
                "prev_status": prev_status,
                "est_compliance": est_compliance,
                "target_date": str(target_date),
                "selected_chapters": selected_ch,
                "uploaded_docs": st.session_state.uploaded_doc_names,
                "description": full_desc,
            }
            st.session_state.facility = facility

            # Stream the analysis
            with st.spinner(""):
                progress_placeholder = st.empty()
                stream_placeholder   = st.empty()

                steps = [
                    "🔍 Reading facility information...",
                    "📊 Mapping against CBAHI standards...",
                    "⚠️  Evaluating ESR compliance...",
                    "📋 Identifying gaps and missing documents...",
                    "💡 Generating prioritized recommendations...",
                    "🗺️  Building corrective action plan...",
                    "📄 Finalizing report...",
                ]

                progress_placeholder.info(steps[0])
                raw_chunks = []
                chunk_count = 0

                try:
                    for chunk in run_analysis(client, facility, program):
                        raw_chunks.append(chunk)
                        chunk_count += 1
                        step_idx = min(chunk_count // 60, len(steps) - 1)
                        progress_placeholder.info(steps[step_idx])

                    raw_text = "".join(raw_chunks)
                    st.session_state.raw_text = raw_text
                    result = parse_result(raw_text)
                    st.session_state.result = result
                    progress_placeholder.empty()
                    stream_placeholder.empty()
                    st.success("✅ Analysis complete! See results below.")
                    st.rerun()

                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ Analysis failed: {str(e)}")

    # ── DISPLAY RESULTS ──
    if st.session_state.result:
        result   = st.session_state.result
        facility = st.session_state.facility
        score    = int(result.get("overall_score", 0) or 0)
        decision = result.get("decision", "Unknown")

        # Color helper — takes the decision string only
        def dc(decision_str):
            d = decision_str.lower()
            if "accredited" in d and "conditional" not in d and "denied" not in d:
                return "#00C97B"
            if "conditional" in d:
                return "#C9A84C"
            if "denied" in d or "preliminary" in d:
                return "#FF4D6D"
            # Fallback on numeric score
            if score >= 85: return "#00C97B"
            if score >= 75: return "#C9A84C"
            return "#FF4D6D"

        decision_color = dc(decision)

        # Score Hero
        met_esrs   = sum(1 for e in result.get("esr_status", []) if e.get("met") is True)
        total_esrs = len(result.get("esr_status", []))
        ready      = result.get("survey_readiness", {}).get("ready_to_survey", False)
        readiness  = result.get("survey_readiness", {}).get("estimated_readiness", "TBD")

        col_score, col_info = st.columns([1, 2])
        with col_score:
            st.markdown(f"""
            <div class="score-hero" style="text-align:center;border-top-color:{decision_color};">
              <div class="score-number" style="color:{decision_color};">{score}%</div>
              <div style="font-size:13px;color:#8896b3;margin-bottom:16px;">Overall Compliance</div>
              <div class="decision-text" style="color:{decision_color};font-size:20px;">{decision}</div>
              <div style="font-size:13px;color:#8896b3;">AI Confidence: {result.get('confidence','High')}</div>
            </div>""", unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
            <div class="score-hero" style="border-top-color:{decision_color};">
              <div style="font-size:14px;color:#8896b3;line-height:1.8;margin-bottom:16px;">{result.get('executive_summary','')}</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                <div class="metric-card"><div class="metric-value" style="color:{'#00C97B' if met_esrs==total_esrs else '#FF4D6D'};font-size:28px;">{met_esrs}/{total_esrs}</div><div class="metric-label">ESRs Met</div></div>
                <div class="metric-card"><div class="metric-value" style="color:{'#00C97B' if ready else '#FF4D6D'};font-size:22px;">{'READY' if ready else 'NOT YET'}</div><div class="metric-label">Survey Ready</div></div>
                <div class="metric-card"><div class="metric-value" style="color:#FF4D6D;font-size:28px;">{len([g for g in result.get('critical_gaps',[]) if g.get('impact')=='Critical'])}</div><div class="metric-label">Critical Gaps</div></div>
                <div class="metric-card"><div class="metric-value" style="color:#C9A84C;font-size:18px;">{readiness}</div><div class="metric-label">Est. Readiness</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Download Report
        st.markdown("---")
        html_report = generate_html_report(result, facility, st.session_state.program)
        col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1])
        with col_dl1:
            st.markdown(f"""
            <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.3);border-radius:12px;padding:20px;">
              <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;margin-bottom:6px;">📥 Download Full Report</div>
              <div style="font-size:13px;color:#8896b3;">Comprehensive HTML report including all findings, chapter scores, ESR matrix, recommendations, and corrective action plan.</div>
            </div>""", unsafe_allow_html=True)
        with col_dl2:
            st.download_button(
                label="📄 Download HTML Report",
                data=html_report.encode("utf-8"),
                file_name=f"CBAHI_Report_{facility_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
        with col_dl3:
            st.download_button(
                label="📊 Download Raw JSON",
                data=json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8"),
                file_name=f"CBAHI_Analysis_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

        st.markdown("---")

        # ── CHAPTER SCORES ──
        st.markdown('<div class="section-title">📊 Chapter-by-Chapter Compliance</div>', unsafe_allow_html=True)

        chapter_scores = result.get("chapter_scores", [])
        if chapter_scores:
            cols = st.columns(2)
            for i, ch in enumerate(chapter_scores):
                s = int(ch.get("score", 0) or 0)
                color = "#00C97B" if s >= 85 else "#3D7FFF" if s >= 70 else "#C9A84C" if s >= 50 else "#FF4D6D"
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="chapter-card">
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <div style="display:flex;align-items:center;gap:8px;">
                          <span class="chapter-code">{ch.get('code','')}</span>
                          <span style="font-size:13px;font-weight:600;">{ch.get('name','')}</span>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:{color};">{s}%</span>
                      </div>
                      <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:4px;margin-bottom:8px;">
                        <div style="width:{s}%;height:100%;background:{color};border-radius:4px;"></div>
                      </div>
                      <div style="font-size:12px;color:#8896b3;">{ch.get('notes','')}</div>
                    </div>""", unsafe_allow_html=True)

        # ── ESR STATUS ──
        st.markdown('<div class="section-title">⚠️ Essential Safety Requirements</div>', unsafe_allow_html=True)
        st.caption("All ESRs must be fully met for accreditation to be granted.")

        esr_status = result.get("esr_status", [])
        if esr_status:
            cols = st.columns(2)
            for i, e in enumerate(esr_status):
                met = e.get("met")
                cls = "esr-met" if met is True else "esr-fail" if met is False else "esr-unknown"
                icon = "✅" if met is True else "❌" if met is False else "❓"
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="{cls}">
                      <div style="display:flex;gap:10px;align-items:flex-start;">
                        <span style="font-size:18px;">{icon}</span>
                        <div>
                          <div style="font-size:13px;font-weight:700;">[{e.get('code','')}] {e.get('name','')}</div>
                          <div style="font-size:12px;color:#8896b3;margin-top:4px;">{e.get('notes','')}</div>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

        # ── STRENGTHS ──
        strengths = result.get("strengths", [])
        if strengths:
            st.markdown('<div class="section-title">✅ Identified Strengths</div>', unsafe_allow_html=True)
            for s in strengths:
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                  <span style="color:#00C97B;flex-shrink:0;">✓</span>
                  <span style="font-size:14px;color:#8896b3;">{s}</span>
                </div>""", unsafe_allow_html=True)

        # ── CRITICAL GAPS ──
        gaps = result.get("critical_gaps", [])
        if gaps:
            st.markdown('<div class="section-title">🚨 Critical Gaps</div>', unsafe_allow_html=True)
            for g in gaps:
                impact = g.get("impact", "Medium")
                ic = "#FF4D6D" if impact == "Critical" else "#C9A84C" if impact == "High" else "#3D7FFF"
                st.markdown(f"""
                <div class="gap-card">
                  <div style="display:flex;gap:10px;align-items:center;margin-bottom:8px;">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#C9A84C;background:rgba(201,168,76,0.1);padding:2px 8px;border-radius:4px;">{g.get('standard','')}</span>
                    <span style="font-size:11px;font-weight:700;color:{ic};background:{ic}20;padding:2px 8px;border-radius:4px;text-transform:uppercase;">{impact}</span>
                  </div>
                  <div style="font-size:14px;font-weight:600;margin-bottom:6px;">{g.get('issue','')}</div>
                  <div style="font-size:13px;color:#8896b3;">💡 {g.get('recommendation','')}</div>
                </div>""", unsafe_allow_html=True)

        # ── MISSING DOCUMENTS ──
        missing = result.get("missing_documents", [])
        if missing:
            st.markdown('<div class="section-title">📋 Missing Documentation</div>', unsafe_allow_html=True)
            for d in missing:
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                  <span style="color:#FF4D6D;flex-shrink:0;">✗</span>
                  <span style="font-size:13px;color:#8896b3;">{d}</span>
                </div>""", unsafe_allow_html=True)

        # ── RECOMMENDATIONS ──
        recs = result.get("recommendations", [])
        if recs:
            st.markdown('<div class="section-title">💡 Prioritized Recommendations</div>', unsafe_allow_html=True)
            for r in recs:
                p = r.get("priority", "Suggested")
                cls = "rec-critical" if p == "Critical" else "rec-important" if p == "Important" else "rec-suggested"
                pc  = "#FF4D6D" if p == "Critical" else "#C9A84C" if p == "Important" else "#3D7FFF"
                stds = " · ".join(r.get("standards", []))
                st.markdown(f"""
                <div class="{cls}">
                  <div style="font-size:11px;font-weight:700;color:{pc};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">{p} · {r.get('timeline','')}</div>
                  <div style="font-size:15px;font-weight:700;margin-bottom:6px;">{r.get('title','')}</div>
                  <div style="font-size:13px;color:#8896b3;line-height:1.6;">{r.get('description','')}</div>
                  {f'<div style="font-size:11px;font-family:monospace;color:#4a5878;margin-top:8px;">{stds}</div>' if stds else ''}
                </div>""", unsafe_allow_html=True)

        # ── ACTION PLAN ──
        ap = result.get("action_plan", {})
        if ap:
            st.markdown('<div class="section-title">🗺️ Corrective Action Plan</div>', unsafe_allow_html=True)
            for key, icon, color in [("phase1","🔴","#FF4D6D"),("phase2","🟡","#C9A84C"),("phase3","🟢","#00C97B")]:
                phase = ap.get(key, {})
                if not phase: continue
                tasks_html = "".join(
                    f'<div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;color:#8896b3;"><span style="color:{color};flex-shrink:0;">→</span>{t}</div>'
                    for t in phase.get("tasks", [])
                )
                st.markdown(f"""
                <div class="phase-card">
                  <div class="phase-label" style="color:{color};">{icon} {phase.get('title','')}</div>
                  <div style="font-size:13px;color:#8896b3;margin-bottom:12px;">{phase.get('description','')}</div>
                  {tasks_html}
                </div>""", unsafe_allow_html=True)

        # ── SURVEY READINESS ──
        sr = result.get("survey_readiness", {})
        if sr:
            st.markdown('<div class="section-title">🎯 Survey Readiness</div>', unsafe_allow_html=True)
            ready  = sr.get("ready_to_survey", False)
            rc     = "#00C97B" if ready else "#FF4D6D"
            risks  = sr.get("key_risks", [])
            risks_html = "".join(f'<div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;color:#8896b3;"><span style="color:#FF4D6D;">⚠</span>{r}</div>' for r in risks)
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:2px solid {rc}30;border-radius:12px;padding:24px;">
              <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:{rc};margin-bottom:8px;">{'✅ READY FOR SURVEY' if ready else '❌ NOT YET READY FOR SURVEY'}</div>
              <div style="font-size:14px;color:#8896b3;margin-bottom:16px;">Estimated readiness: <strong style="color:#F0F4FF;">{sr.get('estimated_readiness','TBD')}</strong></div>
              {risks_html}
            </div>""", unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style="text-align:center;padding:80px 40px;">
          <div style="font-size:64px;margin-bottom:20px;opacity:0.3;">🔍</div>
          <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:#8896b3;margin-bottom:12px;">Ready to Analyze</div>
          <div style="font-size:15px;color:#4a5878;max-width:500px;margin:0 auto;line-height:1.7;">
            Fill in your facility details in the sidebar, describe your current accreditation status, optionally upload documents — then click <strong style="color:#C9A84C;">Run AI Analysis</strong>.
          </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;max-width:800px;margin:0 auto;padding:0 20px;">
          <div class="metric-card"><div style="font-size:28px;margin-bottom:8px;">⚡</div><div style="font-size:13px;font-weight:600;margin-bottom:4px;">Instant Results</div><div style="font-size:12px;color:#4a5878;">AI analysis in seconds</div></div>
          <div class="metric-card"><div style="font-size:28px;margin-bottom:8px;">📊</div><div style="font-size:13px;font-weight:600;margin-bottom:4px;">Chapter Scores</div><div style="font-size:12px;color:#4a5878;">Standards-level analysis</div></div>
          <div class="metric-card"><div style="font-size:28px;margin-bottom:8px;">⚠️</div><div style="font-size:13px;font-weight:600;margin-bottom:4px;">ESR Tracking</div><div style="font-size:12px;color:#4a5878;">All ESRs evaluated</div></div>
          <div class="metric-card"><div style="font-size:28px;margin-bottom:8px;">📄</div><div style="font-size:13px;font-weight:600;margin-bottom:4px;">Report Export</div><div style="font-size:12px;color:#4a5878;">HTML & JSON download</div></div>
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — SELF-ASSESSMENT
# ═════════════════════════════════════════════════════════════════════════════
with tab_selfassess:
    st.markdown("### 📋 Interactive Self-Assessment Tool")
    st.caption("Score each standard manually. Based on official CBAHI 0–2 scoring methodology.")

    prog = st.session_state.program
    thresholds = SCORING_THRESHOLDS.get(prog, {"accredited": 85, "conditional": 75})

    # Key areas per program
    assessment_areas = {
        "ambulatory": [
            ("LD — Leadership", [
                ("LD.1",  "Governing body defines structure and operational responsibilities in a written document"),
                ("LD.2",  "Governing body approves and evaluates quality and patient safety program"),
                ("LD.4",  "Center managed effectively by a qualified director with written job description"),
                ("LD.10", "Staffing plan developed for the center"),
                ("LD.12", "All staff categories have clearly written job descriptions"),
                ("LD.13", "⚠️ ESR: Credentialing and re-credentialing process for all healthcare providers"),
                ("LD.14", "⚠️ ESR: All medical staff have current delineated clinical privileges"),
                ("LD.15", "All new employees attend mandatory orientation program"),
                ("LD.19", "Staff trained in CPR (BLS/ACLS) and certification maintained"),
                ("LD.28", "Policy for development and maintenance of key documents"),
                ("LD.29", "Comprehensive quality improvement and patient safety program"),
                ("LD.31", "Comprehensive risk management program implemented"),
                ("LD.32", "Incident reporting policy developed and implemented"),
            ]),
            ("PC — Provision of Care", [
                ("PC.1",  "Patients have access to services based on health needs"),
                ("PC.2",  "⚠️ ESR: Correct patient identification using at least 2 identifiers"),
                ("PC.3",  "Patients clinically assessed through established assessment policy"),
                ("PC.5",  "Process for reporting critical test results on-site or outsourced"),
                ("PC.6",  "Care plan developed by attending physician"),
                ("PC.8",  "Patients/families assisted in making informed care decisions"),
                ("PC.9",  "Patients/families educated about healthcare needs"),
                ("PC.10", "Informed consent obtained from patient or guardian"),
                ("PC.12", "Effective process for CPR care provision"),
                ("PC.13", "Policies for urgent patient transfer to hospitals"),
                ("PC.14", "Ambulance services available and meet patient needs"),
                ("PC.15", "Emergency services available for minor emergencies"),
            ]),
            ("IPC — Infection Prevention & Control", [
                ("IPC.1",  "Coordinated program to reduce healthcare-associated infections"),
                ("IPC.2",  "IPC activities integrated and coordinated by interdisciplinary team"),
                ("IPC.3",  "IPC policies targeting important infection risk processes"),
                ("IPC.6",  "Effective hand hygiene program implemented"),
                ("IPC.7",  "⚠️ ESR: Sterilization services follow rigorous sterilization rules"),
                ("IPC.9",  "Personal protective equipment available and used correctly"),
                ("IPC.11", "⚠️ ESR: Safe procedures for waste collection, storage and disposal"),
                ("IPC.12", "Program for prevention and management of sharp injuries"),
                ("IPC.13", "Sharps discarded in appropriate puncture-proof containers"),
            ]),
            ("FMS — Facility Management & Safety", [
                ("FMS.1", "Facility management and safety program established and supported"),
                ("FMS.2", "Interdisciplinary safety rounds conducted at least quarterly"),
                ("FMS.3", "Center environment safe for patients, visitors, and staff"),
                ("FMS.4", "Fire prevention program developed and monitored"),
                ("FMS.5", "Center secured and protects users"),
                ("FMS.6", "Plan for inspection, testing and maintenance of medical equipment"),
                ("FMS.7", "Emergency plan developed and staff trained annually"),
            ]),
            ("MM — Medication Management", [
                ("MM.1",  "Medication use processes managed by qualified licensed staff"),
                ("MM.2",  "Updated and well-structured drug formulary available"),
                ("MM.3",  "Appropriate storage of medications maintained"),
                ("MM.5",  "Process for identifying and handling expired medications"),
                ("MM.6",  "Policy for safe prescribing of medications"),
                ("MM.8",  "Narcotics and controlled medications managed per laws"),
                ("MM.9",  "High-alert and LASA medications safely managed"),
                ("MM.12", "Medication error reporting policy implemented"),
            ]),
            ("MOI — Management of Information", [
                ("MOI.1",  "Information management plan defined by leaders"),
                ("MOI.3",  "All patients have unique medical records"),
                ("MOI.4",  "Policy on rules for writing in patients' medical records"),
                ("MOI.5",  "Process for completing and storing patient medical records"),
                ("MOI.6",  "Policy for use of information technology including downtime"),
                ("MOI.7",  "⚠️ ESR: Effective clinical documentation improvement (CDI) program"),
            ]),
        ],
    }

    areas = assessment_areas.get(prog, assessment_areas.get("ambulatory", []))
    if "sa_scores" not in st.session_state:
        st.session_state.sa_scores = {}

    # Calculate scores
    all_scored = {k: v for k, v in st.session_state.sa_scores.items() if v is not None}
    numeric_scores = [v for v in all_scored.values() if isinstance(v, int)]
    pct = round((sum(numeric_scores) / (len(numeric_scores) * 2)) * 100) if numeric_scores else 0
    compliant     = sum(1 for v in numeric_scores if v == 2)
    partial_s     = sum(1 for v in numeric_scores if v == 1)
    noncompliant  = sum(1 for v in numeric_scores if v == 0)
    decision_sa   = "Accredited" if pct >= thresholds["accredited"] else "Conditional" if pct >= thresholds["conditional"] else "Denied"
    dc_sa = "#00C97B" if decision_sa == "Accredited" else "#C9A84C" if decision_sa == "Conditional" else "#FF4D6D"

    # Summary bar
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    for col, val, label, color in [
        (col_a, f"{pct}%",       "Overall Score",    "#C9A84C"),
        (col_b, compliant,        "Compliant",        "#00C97B"),
        (col_c, partial_s,        "Partial",          "#3D7FFF"),
        (col_d, noncompliant,     "Non-Compliant",    "#FF4D6D"),
        (col_e, decision_sa,      "Predicted Decision", dc_sa),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-value" style="color:{color};font-size:{'24px' if isinstance(val,str) and len(val)>4 else '32px'};">{val}</div>
              <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    if pct > 0:
        st.progress(pct / 100)

    st.markdown("---")

    # Score inputs
    for area_name, standards in areas:
        with st.expander(f"**{area_name}** — {len(standards)} standards", expanded=True):
            for code, text in standards:
                is_esr = "⚠️ ESR" in text
                col1, col2 = st.columns([4, 1])
                with col1:
                    label_color = "#FF4D6D" if is_esr else "#F0F4FF"
                    st.markdown(f"""
                    <div style="padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                      <div style="font-size:11px;font-family:monospace;color:#00C9B1;margin-bottom:2px;">{code}</div>
                      <div style="font-size:13px;color:{label_color};">{text}</div>
                    </div>""", unsafe_allow_html=True)
                with col2:
                    current = st.session_state.sa_scores.get(code)
                    options = ["—", "✕ 0", "~ 1", "✓ 2", "N/A"]
                    idx = 0
                    if current == 0:   idx = 1
                    elif current == 1: idx = 2
                    elif current == 2: idx = 3
                    elif current == "na": idx = 4
                    sel = st.selectbox(f"Score for {code}", options, index=idx, label_visibility="collapsed", key=f"sa_{code}")
                    mapping = {"—": None, "✕ 0": 0, "~ 1": 1, "✓ 2": 2, "N/A": "na"}
                    st.session_state.sa_scores[code] = mapping[sel]

    st.markdown("---")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("📊 Recalculate Score", use_container_width=True):
            st.rerun()
    with col_exp2:
        if st.button("↺ Reset All Scores", use_container_width=True):
            st.session_state.sa_scores = {}
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — STANDARDS EXPLORER
# ═════════════════════════════════════════════════════════════════════════════
with tab_standards:
    st.markdown("### 📚 CBAHI Standards Explorer")

    exp_prog = st.selectbox(
        "Select Program", list(PROGRAMS.keys()),
        format_func=lambda k: PROGRAMS[k], key="exp_prog"
    )
    chapters_exp = CHAPTERS.get(exp_prog, [])
    esrs_exp     = ESR_LIST.get(exp_prog, [])

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("**Chapters**")
        chap_label_map = {
            c["code"]: f"{c['code']} — {c['name']}" + (" ⚠️" if c.get("esrs", 0) > 0 else "")
            for c in chapters_exp
        }
        selected_chap = st.radio(
            "Select chapter",
            options=[c["code"] for c in chapters_exp],
            format_func=lambda code: chap_label_map.get(code, code),
            label_visibility="collapsed"
        )

    with col_right:
        chap_info = next((c for c in chapters_exp if c["code"] == selected_chap), None)
        if chap_info:
            st.markdown(f"#### {chap_info['code']} — {chap_info['name']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Standards", chap_info.get("standards", "—"))
            c2.metric("ESRs", chap_info.get("esrs", 0))
            c3.metric("Program", PROGRAMS[exp_prog].split("(")[0].strip())

            # Show ESRs for this chapter
            chap_esrs = [e for e in esrs_exp if e.get("chapter") == selected_chap]
            if chap_esrs:
                st.markdown("**⚠️ Essential Safety Requirements in this chapter:**")
                for e in chap_esrs:
                    st.markdown(f"""
                    <div style="background:rgba(255,77,109,0.08);border:1px solid rgba(255,77,109,0.2);border-radius:8px;padding:12px;margin-bottom:8px;">
                      <div style="font-family:monospace;font-size:12px;color:#C9A84C;margin-bottom:4px;">{e['code']}</div>
                      <div style="font-size:13px;font-weight:600;">{e['name']}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"""
            <div class="info-box">
              ℹ️ This chapter contains <strong>{chap_info.get('standards', '—')} standards</strong>.
              Full sub-standard text is embedded in the AI Analysis engine.
              Run an analysis to receive chapter-specific compliance findings and recommendations.
            </div>""", unsafe_allow_html=True)

            if st.button("→ Analyze This Chapter", key=f"go_{selected_chap}"):
                st.info("Switch to the AI Analyzer tab, select this chapter, and run your analysis.")

    # ESR Reference Table
    st.markdown("---")
    st.markdown(f"### All ESRs for {PROGRAMS[exp_prog]}")
    st.caption("Essential Safety Requirements — all must be fully met for accreditation.")
    for e in esrs_exp:
        st.markdown(f"""
        <div style="display:flex;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
          <span style="font-family:monospace;font-size:11px;color:#C9A84C;background:rgba(201,168,76,0.1);padding:3px 8px;border-radius:4px;flex-shrink:0;border:1px solid rgba(201,168,76,0.2);">{e['code']}</span>
          <span style="font-size:12px;color:#8896b3;background:rgba(255,77,109,0.08);padding:2px 6px;border-radius:4px;flex-shrink:0;">CH: {e['chapter']}</span>
          <span style="font-size:13px;">{e['name']}</span>
        </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ═════════════════════════════════════════════════════════════════════════════
with tab_about:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ## About CBAHI Reviewer

        **CBAHI Reviewer** is an AI-powered accreditation readiness platform built for
        Saudi healthcare facilities seeking CBAHI accreditation. It combines the official
        CBAHI standards with Claude AI to deliver predictive compliance analysis,
        gap identification, and corrective action planning.

        ### 🏛️ Standards Coverage
        - **Hospital Accreditation** — 3rd Edition (600+ standards, 23 mandatory chapters)
        - **Primary Healthcare (PHC)** — Edition 1.1 (400 standards, 23 chapters, 14 ESRs)
        - **Ambulatory Care Centers** — 1st Edition 2019 (133 standards, 11 chapters, 7 ESRs)

        ### 🤖 AI Engine
        Powered by **Claude Sonnet** (Anthropic) with specialized multi-level prompting
        that applies CBAHI scoring methodology across structure, process, and outcome domains.

        ### 📄 Key Features
        - AI compliance analysis with chapter-by-chapter scoring
        - ESR status tracking (Essential Safety Requirements)
        - Gap analysis and missing documentation detection
        - Prioritized recommendations with standard references
        - Phased corrective action plan (0–30, 30–90, 90–180 days)
        - Survey readiness prediction
        - Downloadable HTML reports

        ### ⚠️ Disclaimer
        This platform is an educational and preparatory tool. Results are AI-generated
        estimates based on information provided. They do not constitute an official CBAHI
        survey or guarantee accreditation outcomes. Always consult official CBAHI guidelines
        and engage certified surveyors for formal accreditation preparation.
        """)

    with col2:
        st.markdown(f"""
        <div style="background:#131C35;border:1px solid rgba(201,168,76,0.3);border-radius:16px;padding:32px;text-align:center;margin-top:20px;">
          <div class="cbahi-logo" style="width:70px;height:70px;font-size:28px;margin:0 auto 20px;">CR</div>
          <div style="font-family:'Playfair Display',serif;font-size:24px;font-weight:900;color:#F0F4FF;margin-bottom:4px;">CBAHI Reviewer</div>
          <div style="font-size:13px;color:#C9A84C;letter-spacing:2px;text-transform:uppercase;font-weight:600;margin-bottom:24px;">DentEdTech™</div>
          <div style="font-size:12px;color:#4a5878;line-height:1.8;">
            Healthcare Education<br>& Technology Platform<br><br>
            © {datetime.now().year} DentEdTech<br>All rights reserved<br><br>
            CBAHI® is a registered trademark<br>of the Saudi Central Board for<br>Accreditation of Healthcare Institutions
          </div>
        </div>
        """, unsafe_allow_html=True)
