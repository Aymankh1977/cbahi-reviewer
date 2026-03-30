# utils/report_generator.py
# Downloadable HTML Report Generator
# DentEdTech™ — CBAHI Reviewer Platform

from datetime import datetime


def score_color(score: int) -> str:
    if score >= 85: return "#00C97B"
    if score >= 70: return "#3D7FFF"
    if score >= 50: return "#C9A84C"
    return "#FF4D6D"


def decision_color(decision: str, score: int) -> str:
    d = decision.lower()
    if "accredited" in d and "conditional" not in d and "denied" not in d:
        return "#00C97B"
    if "conditional" in d:
        return "#C9A84C"
    if "denied" in d or "preliminary" in d:
        return "#FF4D6D"
    return score_color(score)


def generate_html_report(result: dict, facility: dict, program: str) -> str:
    score = result.get("overall_score", 0)
    decision = result.get("decision", "Unknown")
    dc = decision_color(decision, score)
    sc = score_color(score)
    date_str = datetime.now().strftime("%d %B %Y")
    program_names = {"ambulatory": "Ambulatory Care Center", "phc": "Primary Healthcare Center", "hospital": "Hospital"}

    chapter_rows = "".join(
        f"""<tr>
          <td><strong>{c.get('code','')}</strong></td>
          <td>{c.get('name','')}</td>
          <td><span class="pill" style="background:{score_color(c.get('score',0))}20;color:{score_color(c.get('score',0))};border:1px solid {score_color(c.get('score',0))}40;">{c.get('score',0)}%</span></td>
          <td>{c.get('status','')}</td>
          <td style="color:#666;font-size:12px;">{c.get('notes','')}</td>
        </tr>"""
        for c in result.get("chapter_scores", [])
    )

    esr_rows = "".join(
        f"""<div class="esr-item {'esr-met' if e.get('met') else 'esr-fail' if e.get('met') is False else 'esr-unk'}">
          <span class="esr-icon">{'✅' if e.get('met') else '❌' if e.get('met') is False else '❓'}</span>
          <div>
            <strong>[{e.get('code','')}] {e.get('name','')}</strong><br>
            <span style="font-size:12px;color:#666;">{e.get('notes','')}</span>
          </div>
        </div>"""
        for e in result.get("esr_status", [])
    )

    gap_rows = "".join(
        f"""<div class="gap-item">
          <div class="gap-header">
            <span class="gap-std">{g.get('standard','')}</span>
            <span class="impact-badge impact-{g.get('impact','Medium').lower()}">{g.get('impact','Medium')}</span>
          </div>
          <div class="gap-issue">{g.get('issue','')}</div>
          <div class="gap-rec">💡 {g.get('recommendation','')}</div>
        </div>"""
        for g in result.get("critical_gaps", [])
    )

    rec_cards = "".join(
        f"""<div class="rec-card rec-{r.get('priority','Suggested').lower()}">
          <div class="rec-priority">{r.get('priority','')} · {r.get('timeline','')}</div>
          <div class="rec-title">{r.get('title','')}</div>
          <div class="rec-desc">{r.get('description','')}</div>
          {f'<div class="rec-std">{" · ".join(r.get("standards",[]))}</div>' if r.get("standards") else ''}
        </div>"""
        for r in result.get("recommendations", [])
    )

    def phase_block(key, icon):
        p = result.get("action_plan", {}).get(key, {})
        if not p: return ""
        tasks = "".join(f"<div class='task'>→ {t}</div>" for t in p.get("tasks", []))
        return f"""<div class="phase-block">
          <div class="phase-title">{icon} {p.get('title','')}</div>
          <div class="phase-desc">{p.get('description','')}</div>
          {tasks}
        </div>"""

    strengths = "".join(f"<li>{s}</li>" for s in result.get("strengths", []))
    missing = "".join(f"<li>{d}</li>" for d in result.get("missing_documents", []))
    risks = "".join(f"<li>{r}</li>" for r in result.get("survey_readiness", {}).get("key_risks", []))

    ready = result.get("survey_readiness", {}).get("ready_to_survey", False)
    readiness_date = result.get("survey_readiness", {}).get("estimated_readiness", "TBD")

    met_esrs = sum(1 for e in result.get("esr_status", []) if e.get("met") is True)
    total_esrs = len(result.get("esr_status", []))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CBAHI Compliance Report — {facility.get('name','')}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono&display=swap');
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{font-family:'DM Sans',sans-serif;background:#f4f6fb;color:#1a1a2e;}}
  .header{{background:linear-gradient(135deg,#0a0e1a,#16213e);color:white;padding:48px 64px;}}
  .header-brand{{font-size:13px;color:#c9a84c;letter-spacing:2px;text-transform:uppercase;font-weight:600;margin-bottom:8px;}}
  .header-title{{font-family:'Playfair Display',serif;font-size:36px;font-weight:900;color:white;margin-bottom:6px;}}
  .header-sub{{font-size:14px;color:#8896b3;margin-bottom:24px;}}
  .header-meta{{display:flex;gap:24px;flex-wrap:wrap;font-size:13px;color:#8896b3;border-top:1px solid rgba(255,255,255,0.1);padding-top:20px;margin-top:20px;}}
  .header-meta span{{display:flex;align-items:center;gap:6px;}}
  .content{{max-width:1100px;margin:0 auto;padding:48px 32px;}}
  .score-hero{{background:white;border-radius:16px;padding:40px;margin-bottom:32px;display:grid;grid-template-columns:auto 1fr auto;gap:40px;align-items:center;box-shadow:0 4px 24px rgba(0,0,0,0.06);border-top:4px solid {dc};}}
  .score-circle{{width:120px;height:120px;border-radius:50%;background:conic-gradient({dc} {score*3.6}deg, #e8ecf4 0deg);display:flex;align-items:center;justify-content:center;position:relative;}}
  .score-inner{{width:90px;height:90px;background:white;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;}}
  .score-num{{font-family:'Playfair Display',serif;font-size:28px;font-weight:900;color:{dc};line-height:1;}}
  .score-pct{{font-size:12px;color:#8896b3;}}
  .score-decision{{font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{dc};margin-bottom:8px;}}
  .score-summary{{font-size:14px;color:#555;line-height:1.7;max-width:500px;}}
  .metrics{{display:flex;flex-direction:column;gap:10px;min-width:160px;}}
  .metric{{background:#f4f6fb;border-radius:8px;padding:10px 14px;display:flex;justify-content:space-between;align-items:center;}}
  .metric-label{{font-size:12px;color:#8896b3;}}
  .metric-value{{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;}}
  h2{{font-family:'Playfair Display',serif;font-size:22px;color:#1a1a2e;margin:40px 0 16px;padding-bottom:10px;border-bottom:2px solid #c9a84c;display:flex;align-items:center;gap:10px;}}
  .card{{background:white;border-radius:12px;padding:28px;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.05);}}
  table{{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.05);margin-bottom:20px;}}
  th{{background:#1a1a2e;color:white;padding:12px 16px;text-align:left;font-size:13px;font-weight:600;}}
  td{{padding:12px 16px;border-bottom:1px solid #f0f0f0;font-size:13px;}}
  tr:last-child td{{border-bottom:none;}}
  tr:nth-child(even){{background:#f8f9ff;}}
  .pill{{padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;font-family:'JetBrains Mono',monospace;}}
  .esr-item{{padding:14px 18px;border-radius:10px;margin-bottom:10px;display:flex;align-items:flex-start;gap:14px;font-size:13px;}}
  .esr-icon{{font-size:20px;flex-shrink:0;margin-top:1px;}}
  .esr-met{{background:#e8fff4;border:1px solid #00c97b30;}}
  .esr-fail{{background:#fff0f3;border:1px solid #ff4d6d30;}}
  .esr-unk{{background:#f4f6fb;border:1px solid #ddd;}}
  .gap-item{{background:white;border-radius:10px;padding:18px;margin-bottom:12px;border-left:4px solid #ff4d6d;box-shadow:0 2px 8px rgba(0,0,0,0.04);}}
  .gap-header{{display:flex;align-items:center;gap:10px;margin-bottom:8px;}}
  .gap-std{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#c9a84c;background:#fffbe8;padding:3px 8px;border-radius:4px;border:1px solid #c9a84c30;}}
  .impact-badge{{font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:1px;}}
  .impact-critical{{background:#fff0f3;color:#cc1f3a;}}
  .impact-high{{background:#fff5e8;color:#c96f00;}}
  .impact-medium{{background:#fffbe8;color:#8c6e0a;}}
  .gap-issue{{font-size:14px;font-weight:600;color:#1a1a2e;margin-bottom:6px;}}
  .gap-rec{{font-size:13px;color:#555;line-height:1.5;}}
  .rec-card{{border-radius:10px;padding:18px;margin-bottom:12px;border-left:4px solid;}}
  .rec-critical{{background:#fff0f3;border-color:#cc1f3a;}}
  .rec-important{{background:#fffbe8;border-color:#c9a84c;}}
  .rec-suggested{{background:#e8f0ff;border-color:#3d7fff;}}
  .rec-priority{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;color:#666;}}
  .rec-title{{font-size:15px;font-weight:700;margin-bottom:6px;color:#1a1a2e;}}
  .rec-desc{{font-size:13px;color:#555;line-height:1.5;}}
  .rec-std{{font-size:11px;font-family:'JetBrains Mono',monospace;color:#999;margin-top:6px;}}
  .phase-block{{background:white;border-radius:10px;padding:22px;margin-bottom:14px;box-shadow:0 2px 8px rgba(0,0,0,0.04);}}
  .phase-title{{font-size:16px;font-weight:700;color:#1a1a2e;margin-bottom:6px;}}
  .phase-desc{{font-size:13px;color:#666;margin-bottom:12px;}}
  .task{{font-size:13px;color:#444;padding:5px 0;border-bottom:1px solid #f0f0f0;line-height:1.5;}}
  .task:last-child{{border-bottom:none;}}
  .readiness-box{{background:white;border-radius:12px;padding:28px;margin-bottom:20px;border:2px solid {'#00c97b' if ready else '#ff4d6d'};box-shadow:0 2px 12px rgba(0,0,0,0.05);}}
  .readiness-title{{font-size:20px;font-weight:700;color:{'#00854d' if ready else '#cc1f3a'};margin-bottom:8px;}}
  ul{{padding-left:20px;}} li{{font-size:13px;padding:4px 0;color:#555;}}
  .footer{{background:#1a1a2e;color:#8896b3;padding:28px 64px;margin-top:40px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;font-size:12px;}}
  .footer-brand{{color:#c9a84c;font-weight:700;font-size:16px;font-family:'Playfair Display',serif;}}
  .disclaimer{{max-width:600px;line-height:1.6;}}
  @media print{{body{{background:white;}} .header{{print-color-adjust:exact;-webkit-print-color-adjust:exact;}}}}
</style>
</head>
<body>

<div class="header">
  <div class="header-brand">CBAHI Reviewer — DentEdTech™</div>
  <div class="header-title">CBAHI Compliance Report</div>
  <div class="header-sub">{facility.get('name','')} · {program_names.get(program, program)}</div>
  <div class="header-meta">
    <span>📅 Generated: {date_str}</span>
    <span>🏥 {facility.get('facility_type','Not specified')}</span>
    <span>📍 {facility.get('city','KSA')}</span>
    <span>🔍 Survey Type: {facility.get('survey_type','Initial')}</span>
    <span>🤖 AI Confidence: {result.get('confidence','High')}</span>
  </div>
</div>

<div class="content">

  <!-- Score Hero -->
  <div class="score-hero">
    <div class="score-circle">
      <div class="score-inner">
        <div class="score-num">{score}%</div>
        <div class="score-pct">overall</div>
      </div>
    </div>
    <div>
      <div class="score-decision">{decision}</div>
      <div class="score-summary">{result.get('executive_summary','')}</div>
    </div>
    <div class="metrics">
      <div class="metric">
        <span class="metric-label">ESRs Met</span>
        <span class="metric-value" style="color:{'#00c97b' if met_esrs==total_esrs else '#ff4d6d'};">{met_esrs}/{total_esrs}</span>
      </div>
      <div class="metric">
        <span class="metric-label">Critical Gaps</span>
        <span class="metric-value" style="color:#ff4d6d;">{len([g for g in result.get('critical_gaps',[]) if g.get('impact')=='Critical'])}</span>
      </div>
      <div class="metric">
        <span class="metric-label">Est. Readiness</span>
        <span class="metric-value" style="color:#c9a84c;font-size:11px;">{readiness_date}</span>
      </div>
      <div class="metric">
        <span class="metric-label">Survey Ready</span>
        <span class="metric-value" style="color:{'#00c97b' if ready else '#ff4d6d'};">{'YES' if ready else 'NOT YET'}</span>
      </div>
    </div>
  </div>

  <!-- Key Strengths -->
  <h2>✅ Identified Strengths</h2>
  <div class="card"><ul>{strengths}</ul></div>

  <!-- Chapter Scores -->
  <h2>📊 Chapter-by-Chapter Compliance</h2>
  <table>
    <thead><tr><th>Code</th><th>Chapter</th><th>Score</th><th>Status</th><th>Notes</th></tr></thead>
    <tbody>{chapter_rows}</tbody>
  </table>

  <!-- ESR Status -->
  <h2>⚠️ Essential Safety Requirements Status</h2>
  {esr_rows}

  <!-- Critical Gaps -->
  <h2>🚨 Critical Gaps Identified</h2>
  {gap_rows if gap_rows else '<div class="card"><p style="color:#00854d;">✅ No critical gaps identified based on the information provided.</p></div>'}

  <!-- Missing Documents -->
  {f'<h2>📋 Missing or Incomplete Documentation</h2><div class="card"><ul>{missing}</ul></div>' if missing else ''}

  <!-- Recommendations -->
  <h2>💡 Prioritized Recommendations</h2>
  {rec_cards}

  <!-- Action Plan -->
  <h2>🗺️ Corrective Action Plan</h2>
  {phase_block('phase1', '🔴')}
  {phase_block('phase2', '🟡')}
  {phase_block('phase3', '🟢')}

  <!-- Survey Readiness -->
  <h2>🎯 Survey Readiness Assessment</h2>
  <div class="readiness-box">
    <div class="readiness-title">{'✅ READY FOR SURVEY' if ready else '❌ NOT YET READY FOR SURVEY'}</div>
    <p style="font-size:14px;color:#555;margin-bottom:16px;">Estimated readiness: <strong>{readiness_date}</strong></p>
    {f'<strong style="font-size:13px;">Key Risks:</strong><ul>{risks}</ul>' if risks else ''}
  </div>

</div>

<div class="footer">
  <div>
    <div class="footer-brand">CBAHI Reviewer — DentEdTech™</div>
    <div class="disclaimer">This report is AI-generated for accreditation preparation purposes only. It does not constitute an official CBAHI survey or guarantee any accreditation outcome. Always consult official CBAHI guidelines and engage certified surveyors for formal preparation.</div>
  </div>
  <div style="text-align:right;">
    <div>© {datetime.now().year} DentEdTech. All rights reserved.</div>
    <div style="margin-top:4px;">CBAHI® is a registered trademark of the Saudi Central Board for Accreditation of Healthcare Institutions.</div>
  </div>
</div>

</body>
</html>"""
