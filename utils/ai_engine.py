# utils/ai_engine.py
# AI Analysis Engine — Claude-powered CBAHI compliance analysis
# DentEdTech™ — CBAHI Reviewer Platform

import anthropic
import json
import re
from utils.cbahi_data import CHAPTERS, ESR_LIST, SCORING_THRESHOLDS, TOTAL_STANDARDS


def build_prompt(facility: dict, program: str) -> str:
    chapters = CHAPTERS.get(program, [])
    esrs = ESR_LIST.get(program, [])
    thresholds = SCORING_THRESHOLDS.get(program, {"accredited": 85, "conditional": 75})
    total = TOTAL_STANDARDS.get(program, 0)
    program_names = {"ambulatory": "Ambulatory Care Center", "phc": "Primary Healthcare Center", "hospital": "Hospital"}

    chapter_list = "\n".join(
        f"  {c['code']}: {c['name']} ({c['standards']} standards{', ' + str(c['esrs']) + ' ESRs' if c['esrs'] else ''})"
        for c in chapters
    )
    esr_list = "\n".join(
        f"  {i+1}. [{e['code']}] {e['name']} (Chapter: {e['chapter']})"
        for i, e in enumerate(esrs)
    )
    selected_chapters = ", ".join(facility.get("selected_chapters", [c["code"] for c in chapters]))
    docs_text = "\n".join(f"  - {d}" for d in facility.get("uploaded_docs", [])) or "  None uploaded"

    return f"""You are a senior CBAHI accreditation consultant with 15+ years of experience conducting surveys across Saudi Arabia. Perform a rigorous, evidence-based CBAHI compliance analysis for the following facility.

═══════════════════════════════════════════════════
FACILITY PROFILE
═══════════════════════════════════════════════════
Name:                {facility.get('name', 'Unknown')}
Program:             {program_names.get(program, program)} ({total} total standards)
Facility Type:       {facility.get('facility_type', 'Not specified')}
Capacity:            {facility.get('capacity', 'Not specified')}
City / Region:       {facility.get('city', 'Kingdom of Saudi Arabia')}
Survey Type:         {facility.get('survey_type', 'Initial Survey')}
Previous Status:     {facility.get('prev_status', 'Never Accredited')}
Self-Estimated:      {facility.get('est_compliance', 'Unknown')}
Target Survey Date:  {facility.get('target_date', 'Not specified')}
Chapters Selected:   {selected_chapters}

UPLOADED DOCUMENTS:
{docs_text}

═══════════════════════════════════════════════════
FACILITY DESCRIPTION & CURRENT STATUS
═══════════════════════════════════════════════════
{facility.get('description', 'No description provided.')}

═══════════════════════════════════════════════════
CHAPTERS TO EVALUATE
═══════════════════════════════════════════════════
{chapter_list}

═══════════════════════════════════════════════════
ESSENTIAL SAFETY REQUIREMENTS — ALL MUST BE MET
═══════════════════════════════════════════════════
{esr_list}

═══════════════════════════════════════════════════
CBAHI SCORING METHODOLOGY
═══════════════════════════════════════════════════
Score 0 = Insufficient Compliance (<50%)
Score 1 = Partial Compliance (50–85%)
Score 2 = Satisfactory Compliance (≥85%)

ACCREDITED:    Overall ≥{thresholds['accredited']}% AND all ESRs met
CONDITIONAL:   Overall ≥{thresholds['conditional']}% (some ESRs may be partially met)
DENIED:        Overall <{thresholds['conditional']}% OR critical ESR failures

═══════════════════════════════════════════════════
ANALYSIS INSTRUCTIONS
═══════════════════════════════════════════════════
1. Be rigorous — do NOT assume compliance for anything not explicitly described
2. ESR failures are the most critical — flag any that are unclear or missing
3. Base scoring on what IS described, not what might exist
4. Provide specific, actionable recommendations with referenced standard codes
5. The action plan must be realistic and achievable within the given timeframe

Return ONLY valid JSON (no markdown, no explanation, no code blocks):

{{
  "overall_score": 72,
  "decision": "Conditional Accreditation",
  "confidence": "High",
  "executive_summary": "2–3 sentence assessment of the facility's current accreditation readiness and overall posture.",
  "strengths": [
    "Strength 1 — specific and evidence-based",
    "Strength 2",
    "Strength 3",
    "Strength 4",
    "Strength 5"
  ],
  "critical_gaps": [
    {{
      "standard": "LD.13",
      "issue": "No formal credentialing committee described in the facility information",
      "impact": "Critical",
      "recommendation": "Establish a multidisciplinary credentialing committee, develop privileging policy, and verify credentials from primary sources for all clinical staff within 30 days"
    }}
  ],
  "chapter_scores": [
    {{
      "code": "LD",
      "name": "Leadership",
      "score": 70,
      "status": "Partial",
      "notes": "Good organizational structure evident; credentialing gaps are significant"
    }}
  ],
  "esr_status": [
    {{
      "code": "LD.13",
      "name": "Credentialing & Re-credentialing",
      "met": false,
      "notes": "No credentialing committee or privileging process described"
    }}
  ],
  "missing_documents": [
    "Credentialing and privileging policy and procedure",
    "List of approved clinical privileges per physician"
  ],
  "recommendations": [
    {{
      "priority": "Critical",
      "title": "Establish Credentialing Committee",
      "description": "Form a multidisciplinary credentialing committee. Develop and implement a privileging policy. Verify all clinical staff credentials from primary sources.",
      "standards": ["LD.13", "LD.14"],
      "timeline": "0–30 days"
    }},
    {{
      "priority": "Important",
      "title": "Implement Incident Reporting System",
      "description": "Develop a structured incident reporting policy with risk scoring matrix, root cause analysis workflow, and quarterly reporting to governance.",
      "standards": ["LD.32", "QM.8"],
      "timeline": "30–60 days"
    }},
    {{
      "priority": "Suggested",
      "title": "Enhance Patient Education Documentation",
      "description": "Standardize patient education forms, train clinical staff on documentation requirements, and audit medical records monthly for compliance.",
      "standards": ["PC.9"],
      "timeline": "60–90 days"
    }}
  ],
  "action_plan": {{
    "phase1": {{
      "title": "Immediate Actions (0–30 days)",
      "description": "Address all ESR failures and critical gaps that would cause denial of accreditation",
      "tasks": [
        "Form credentialing and privileging committee",
        "Conduct gap analysis using CBAHI self-assessment tool",
        "Assign accreditation coordinator and chapter owners"
      ]
    }},
    "phase2": {{
      "title": "Short-term Actions (30–90 days)",
      "description": "Resolve important compliance gaps and build documentation portfolio",
      "tasks": [
        "Develop and approve all missing policies and procedures",
        "Conduct staff orientation and education sessions",
        "Perform internal mock survey using CBAHI standards"
      ]
    }},
    "phase3": {{
      "title": "Sustained Compliance (90–180 days)",
      "description": "Embed accreditation culture, sustain compliance, and prepare for survey",
      "tasks": [
        "Launch quality improvement projects and KPI monitoring",
        "Conduct interdisciplinary safety rounds quarterly",
        "Submit CBAHI survey application and complete SAT"
      ]
    }}
  }},
  "survey_readiness": {{
    "ready_to_survey": false,
    "estimated_readiness": "60–90 days",
    "key_risks": [
      "ESR LD.13 non-compliance would trigger immediate denial",
      "Incomplete medical records may reveal documentation gaps during survey"
    ]
  }}
}}"""


def run_analysis(client: anthropic.Anthropic, facility: dict, program: str) -> dict:
    """Run the full AI analysis pipeline with streaming."""
    prompt = build_prompt(facility, program)

    full_text = ""
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_text += text
            yield text  # stream chunks back to UI

    # After streaming, parse the result
    return full_text


def parse_result(raw_text: str) -> dict:
    """Extract and parse JSON from Claude's response."""
    text = raw_text.strip()

    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Return a graceful fallback
        return {
            "overall_score": 0,
            "decision": "Parse Error",
            "confidence": "Low",
            "executive_summary": "The AI response could not be parsed. Please try again.",
            "strengths": [],
            "critical_gaps": [],
            "chapter_scores": [],
            "esr_status": [],
            "missing_documents": [],
            "recommendations": [],
            "action_plan": {"phase1": {"title": "", "tasks": []}, "phase2": {"title": "", "tasks": []}, "phase3": {"title": "", "tasks": []}},
            "survey_readiness": {"ready_to_survey": False, "estimated_readiness": "Unknown", "key_risks": []},
            "raw_text": raw_text,
        }


def extract_text_from_file(uploaded_file) -> str:
    """Extract readable text from uploaded files."""
    name = uploaded_file.name.lower()
    content = uploaded_file.read()

    if name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        try:
            import PyPDF2, io
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except Exception:
            return f"[PDF: {uploaded_file.name} — could not extract text]"

    if name.endswith((".docx", ".doc")):
        try:
            import docx, io
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception:
            return f"[DOCX: {uploaded_file.name} — could not extract text]"

    if name.endswith((".xlsx", ".xls")):
        try:
            import openpyxl, io
            wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
            rows = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    rows.append(" | ".join(str(c) for c in row if c is not None))
            return "\n".join(rows[:200])  # cap at 200 rows
        except Exception:
            return f"[XLSX: {uploaded_file.name} — could not extract text]"

    return f"[{uploaded_file.name} — unsupported format for text extraction]"
