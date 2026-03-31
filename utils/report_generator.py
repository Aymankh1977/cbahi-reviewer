# utils/report_generator.py
# Downloadable HTML Report Generator
# DentEdTech — CBAHI Reviewer Platform

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
  <div class="header-brand">CBAHI Reviewer — DentEdTech</div>
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
    <div class="footer-brand">CBAHI Reviewer — DentEdTech</div>
    <div class="disclaimer">This report is AI-generated for accreditation preparation purposes only. It does not constitute an official CBAHI survey or guarantee any accreditation outcome. Always consult official CBAHI guidelines and engage certified surveyors for formal preparation.</div>
  </div>
  <div style="text-align:right;">
    <div>© 2026 DentEdTech. All rights reserved.</div>
    <div style="margin-top:4px;">CBAHI® is a registered trademark of the Saudi Central Board for Accreditation of Healthcare Institutions.</div>
  </div>
</div>

</body>
</html>"""


def generate_pdf_report(result: dict, facility: dict, program: str) -> bytes:
    """Generate a print-ready PDF compliance report using ReportLab."""
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, KeepTogether, PageBreak
    )
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
    from reportlab.platypus import Flowable
    import io

    # ── Palette ──────────────────────────────────────────────────────────
    GOLD      = colors.HexColor("#C9A84C")
    DARK_NAVY = colors.HexColor("#0A0E1A")
    NAVY      = colors.HexColor("#131C35")
    NAVY_MID  = colors.HexColor("#1E2D50")
    GREEN     = colors.HexColor("#00C97B")
    RED       = colors.HexColor("#FF4D6D")
    BLUE      = colors.HexColor("#3D7FFF")
    TEAL      = colors.HexColor("#00C9B1")
    GREY      = colors.HexColor("#F4F6FB")
    MID_GREY  = colors.HexColor("#8896B3")
    TEXT      = colors.HexColor("#1A1A2E")
    WHITE     = colors.white
    BORDER    = colors.HexColor("#E0E4EE")

    PAGE_W, PAGE_H = A4
    MARGIN = 2.0 * cm
    CW = PAGE_W - 2 * MARGIN

    # ── Score helpers ─────────────────────────────────────────────────────
    def scol(s):
        s = int(s or 0)
        if s >= 85: return GREEN
        if s >= 70: return BLUE
        if s >= 50: return GOLD
        return RED

    def dcol(decision, score):
        d = decision.lower()
        if "accredited" in d and "conditional" not in d and "denied" not in d: return GREEN
        if "conditional" in d: return GOLD
        if "denied" in d: return RED
        return scol(score)

    # ── Styles ────────────────────────────────────────────────────────────
    def st(name, **kw):
        defaults = dict(fontName="Helvetica", fontSize=10, textColor=TEXT,
                        spaceBefore=3, spaceAfter=3, leading=14)
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    S = {
        "h1":   st("h1", fontName="Helvetica-Bold", fontSize=18, textColor=DARK_NAVY,
                   spaceBefore=14, spaceAfter=6, leading=24),
        "h2":   st("h2", fontName="Helvetica-Bold", fontSize=13, textColor=DARK_NAVY,
                   spaceBefore=10, spaceAfter=5, leading=18),
        "h3":   st("h3", fontName="Helvetica-Bold", fontSize=10.5, textColor=NAVY_MID,
                   spaceBefore=7, spaceAfter=3, leading=15),
        "body": st("body", alignment=TA_JUSTIFY),
        "sm":   st("sm", fontSize=9, leading=13),
        "cap":  st("cap", fontName="Helvetica-Oblique", fontSize=8,
                   textColor=MID_GREY, alignment=TA_CENTER),
        "mono": st("mono", fontName="Courier", fontSize=8.5,
                   textColor=DARK_NAVY, backColor=GREY),
        "ctr":  st("ctr", alignment=TA_CENTER),
    }

    # ── Helpers ───────────────────────────────────────────────────────────
    def hr():
        return HRFlowable(width="100%", thickness=1, color=GOLD,
                          spaceBefore=4*mm, spaceAfter=4*mm)

    def pill(text, bg, tc=WHITE):
        d = [[Paragraph(text, ParagraphStyle("p", fontName="Helvetica-Bold",
                  fontSize=8, textColor=tc, alignment=TA_CENTER))]]
        t = Table(d, colWidths=[24*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), bg),
            ("TOPPADDING", (0,0),(-1,-1), 3),
            ("BOTTOMPADDING",(0,0),(-1,-1), 3),
            ("ROUNDEDCORNERS",[4]),
        ]))
        return t

    def section(title, icon=""):
        return [
            Spacer(1, 4*mm),
            HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=2*mm),
            Paragraph(f"{icon}  {title}".strip(), S["h1"]),
            Spacer(1, 2*mm),
        ]

    def tbl(rows, headers, widths=None):
        data = [[Paragraph(f"<b>{h}</b>",
                    ParagraphStyle("th", fontName="Helvetica-Bold",
                    fontSize=8.5, textColor=WHITE)) for h in headers]]
        for row in rows:
            data.append([Paragraph(str(c), S["sm"]) for c in row])
        w = widths or [CW / len(headers)] * len(headers)
        t = Table(data, colWidths=w)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), DARK_NAVY),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [GREY, WHITE]),
            ("GRID",          (0,0),(-1,-1), 0.3, BORDER),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 7),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ]))
        return t

    def info(text, border=GOLD, bg=None):
        if bg is None:
            bg = colors.HexColor("#FFFBE8")
        d = [[Paragraph(text, S["sm"])]]
        t = Table(d, colWidths=[CW])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), bg),
            ("LINEABOVE",    (0,0),(-1,0),  2, border),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("RIGHTPADDING", (0,0),(-1,-1), 10),
            ("TOPPADDING",   (0,0),(-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ]))
        return t

    def bul(text):
        return Paragraph(f"\u2022  {text}",
            ParagraphStyle("b", parent=S["body"], leftIndent=12))

    # ── Page callbacks ────────────────────────────────────────────────────
    score    = int(result.get("overall_score", 0) or 0)
    decision = result.get("decision", "Unknown")
    DC       = dcol(decision, score)
    prog_names = {"ambulatory":"Ambulatory Care Center",
                  "phc":"Primary Healthcare Center",
                  "hospital":"Hospital"}
    prog_label = prog_names.get(program, program)

    def on_first(canvas, doc):
        w, h = A4
        canvas.saveState()
        canvas.setFillColor(DARK_NAVY)
        canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(0, h-8*mm, w, 8*mm, fill=1, stroke=0)
        canvas.rect(0, 0, w, 4*mm, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#0F1628"))
        canvas.rect(0, 0, 18*mm, h-8*mm, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(16*mm, 0, 2*mm, h-8*mm, fill=1, stroke=0)
        # Logo
        canvas.setFillColor(GOLD)
        canvas.roundRect(MARGIN+18*mm, h-76*mm, 22*mm, 22*mm, 5, fill=1, stroke=0)
        canvas.setFillColor(DARK_NAVY)
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawCentredString(MARGIN+18*mm+11*mm, h-68*mm, "CR")
        # Title
        canvas.setFillColor(GOLD)
        canvas.setFont("Helvetica-Bold", 32)
        canvas.drawString(MARGIN+18*mm, h-108*mm, "CBAHI Compliance Report")
        # Facility
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(MARGIN+18*mm, h-120*mm, facility.get("name",""))
        # Rule
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(1)
        canvas.line(MARGIN+18*mm, h-127*mm, w-MARGIN, h-127*mm)
        # Meta grid
        meta = [
            ("Program",      prog_label),
            ("Survey Type",  facility.get("survey_type","Initial Survey")),
            ("City",         facility.get("city","KSA")),
            ("Generated",    datetime.now().strftime("%d %B %Y")),
        ]
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(GOLD)
        for i, (k, v) in enumerate(meta):
            mx = MARGIN+18*mm + i*43*mm
            canvas.drawString(mx, h-137*mm, k.upper())
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(WHITE)
        for i, (k, v) in enumerate(meta):
            mx = MARGIN+18*mm + i*43*mm
            canvas.drawString(mx, h-145*mm, v[:20])
        # Big score
        canvas.setFillColor(DC)
        canvas.setFont("Helvetica-Bold", 72)
        canvas.drawString(MARGIN+18*mm, h-200*mm, f"{score}%")
        canvas.setFont("Helvetica-Bold", 22)
        canvas.drawString(MARGIN+18*mm, h-213*mm, decision)
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(MID_GREY)
        canvas.drawString(MARGIN+18*mm, h-222*mm,
            f"AI Confidence: {result.get('confidence','High')}")
        # Brand footer
        canvas.setFillColor(GOLD)
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(MARGIN+18*mm, 36*mm, "DentEdTech")
        canvas.setFillColor(MID_GREY)
        canvas.setFont("Helvetica", 9)
        canvas.drawString(MARGIN+18*mm, 28*mm, "© 2026 DentEdTech. All rights reserved.")
        canvas.drawString(MARGIN+18*mm, 20*mm,
            "AI-generated report for accreditation preparation. Not an official CBAHI survey.")
        canvas.restoreState()

    def on_later(canvas, doc):
        w, h = A4
        canvas.saveState()
        canvas.setFillColor(DARK_NAVY)
        canvas.rect(0, h-14*mm, w, 14*mm, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(0, h-15.5*mm, w, 1.5*mm, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(MARGIN, h-9.5*mm, "CBAHI Compliance Report")
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawCentredString(w/2, h-9.5*mm, facility.get("name",""))
        canvas.setFillColor(MID_GREY)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawRightString(w-MARGIN, h-9.5*mm, "DentEdTech")
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 14*mm, w-MARGIN, 14*mm)
        canvas.setFillColor(MID_GREY)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(MARGIN, 9*mm, "AI-generated. Not an official CBAHI survey.")
        canvas.drawRightString(w-MARGIN, 9*mm, f"Page {doc.page}")
        canvas.restoreState()

    # ── Build story ───────────────────────────────────────────────────────
    buf  = io.BytesIO()
    doc  = SimpleDocTemplate(buf, pagesize=A4,
               leftMargin=MARGIN, rightMargin=MARGIN,
               topMargin=2.8*cm, bottomMargin=2.2*cm,
               title=f"CBAHI Report — {facility.get('name','')}",
               author="DentEdTech")
    story = []
    story.append(Spacer(1, 1))   # cover drawn by on_first callback

    met_esrs   = sum(1 for e in result.get("esr_status",[]) if e.get("met") is True)
    total_esrs = len(result.get("esr_status",[]))
    ready      = result.get("survey_readiness",{}).get("ready_to_survey", False)
    readiness  = result.get("survey_readiness",{}).get("estimated_readiness","TBD")

    # ── Executive Summary ──────────────────────────────────────────────────
    story.append(PageBreak())
    story += section("Executive Summary", "")

    # KPI cards row
    kpis = [
        (f"{score}%",       "Overall Score",  DC),
        (f"{met_esrs}/{total_esrs}", "ESRs Met",
            GREEN if met_esrs==total_esrs else RED),
        (str(len([g for g in result.get("critical_gaps",[])
                  if g.get("impact")=="Critical"])), "Critical Gaps", RED),
        ("READY" if ready else "NOT YET", "Survey Ready",
            GREEN if ready else RED),
        (readiness, "Est. Readiness", GOLD),
    ]
    kpi_data = [[
        Paragraph(f"<b>{v}</b>",
            ParagraphStyle("kv", fontName="Helvetica-Bold", fontSize=12,
                textColor=c, alignment=TA_CENTER)),
        Paragraph(k, ParagraphStyle("kl", fontName="Helvetica", fontSize=7.5,
            textColor=MID_GREY, alignment=TA_CENTER))
    ] for v, k, c in kpis]
    # render as a 5-col table
    row1 = [kpi_data[i][0] for i in range(5)]
    row2 = [kpi_data[i][1] for i in range(5)]
    kpi_t = Table([row1, row2], colWidths=[CW/5]*5)
    kpi_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), NAVY),
        ("TOPPADDING",   (0,0),(-1,0), 10),
        ("BOTTOMPADDING",(0,-1),(-1,-1), 8),
        ("TOPPADDING",   (0,1),(-1,1), 2),
        ("LINEBELOW",    (0,0),(-1,0), 0.3, BORDER),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(kpi_t)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(result.get("executive_summary",""), S["body"]))

    # Strengths
    strengths = result.get("strengths", [])
    if strengths:
        story += section("Identified Strengths", "")
        for s_item in strengths:
            story.append(bul(s_item))

    # ── Chapter Scores ─────────────────────────────────────────────────────
    story += section("Chapter-by-Chapter Compliance", "")
    ch_rows = []
    for ch in result.get("chapter_scores", []):
        sc = int(ch.get("score", 0) or 0)
        col = scol(sc)
        ch_rows.append([
            ch.get("code",""), ch.get("name",""),
            f"{sc}%", ch.get("status",""), ch.get("notes","")
        ])
    if ch_rows:
        story.append(tbl(ch_rows,
            ["Code","Chapter","Score","Status","Notes"],
            widths=[14*mm, 50*mm, 16*mm, 22*mm, CW-102*mm]))

    # ── ESR Status ─────────────────────────────────────────────────────────
    story += section("Essential Safety Requirements", "")
    story.append(info(
        "All ESRs must be fully met for Accreditation to be granted. "
        "Any ESR marked Not Met must be resolved before the official survey.",
        border=RED, bg=colors.HexColor("#FFF0F3")))
    story.append(Spacer(1, 3*mm))
    esr_rows = []
    for e in result.get("esr_status", []):
        met = e.get("met")
        status = "Met" if met is True else "Not Met" if met is False else "Unclear"
        esr_rows.append([e.get("code",""), e.get("name",""), status, e.get("notes","")])
    if esr_rows:
        story.append(tbl(esr_rows,
            ["Code","Requirement","Status","Notes"],
            widths=[16*mm, 52*mm, 18*mm, CW-86*mm]))

    # ── Critical Gaps ──────────────────────────────────────────────────────
    gaps = result.get("critical_gaps", [])
    if gaps:
        story += section("Critical Gaps Identified", "")
        for g in gaps:
            impact = g.get("impact","Medium")
            ic = RED if impact=="Critical" else GOLD if impact=="High" else BLUE
            story.append(KeepTogether([
                Table([[
                    Paragraph(f"<b>{g.get('standard','')}</b>",
                        ParagraphStyle("gc", fontName="Helvetica-Bold",
                            fontSize=9, textColor=GOLD)),
                    Paragraph(impact,
                        ParagraphStyle("gi", fontName="Helvetica-Bold",
                            fontSize=8, textColor=ic, alignment=TA_RIGHT)),
                ]], colWidths=[CW*0.7, CW*0.3]),
                Paragraph(f"<b>{g.get('issue','')}</b>", S["h3"]),
                Paragraph(f"Recommendation: {g.get('recommendation','')}", S["sm"]),
                Spacer(1, 3*mm),
                HRFlowable(width="100%", thickness=0.3, color=BORDER, spaceAfter=2*mm),
            ]))

    # ── Missing Documents ──────────────────────────────────────────────────
    missing = result.get("missing_documents", [])
    if missing:
        story += section("Missing Documentation", "")
        for d_item in missing:
            story.append(bul(d_item))

    # ── Recommendations ────────────────────────────────────────────────────
    recs = result.get("recommendations", [])
    if recs:
        story += section("Prioritised Recommendations", "")
        for r in recs:
            p  = r.get("priority","Suggested")
            pc = RED if p=="Critical" else GOLD if p=="Important" else BLUE
            bg = colors.HexColor("#FFF5F5") if p=="Critical" else                  colors.HexColor("#FFFBE8") if p=="Important" else                  colors.HexColor("#F0F4FF")
            stds = " · ".join(r.get("standards",[]))
            body_parts = [
                Paragraph(f"<b>{p} — {r.get('title','')}</b>  |  {r.get('timeline','')}",
                    ParagraphStyle("rh", fontName="Helvetica-Bold", fontSize=10,
                        textColor=pc)),
                Paragraph(r.get("description",""), S["sm"]),
            ]
            if stds:
                body_parts.append(Paragraph(stds,
                    ParagraphStyle("rs", fontName="Courier", fontSize=8,
                        textColor=MID_GREY)))
            card_data = [[body_parts]]
            card = Table(card_data, colWidths=[CW])
            card.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), bg),
                ("LINEBEFORE",   (0,0),(0,-1),  3, pc),
                ("LEFTPADDING",  (0,0),(-1,-1), 10),
                ("RIGHTPADDING", (0,0),(-1,-1), 8),
                ("TOPPADDING",   (0,0),(-1,-1), 7),
                ("BOTTOMPADDING",(0,0),(-1,-1), 7),
            ]))
            story.append(card)
            story.append(Spacer(1, 3*mm))

    # ── Action Plan ────────────────────────────────────────────────────────
    ap = result.get("action_plan", {})
    if ap:
        story += section("Corrective Action Plan", "")
        for key, icon, col in [("phase1","Phase 1 — 0 to 30 days",RED),
                                ("phase2","Phase 2 — 30 to 90 days",GOLD),
                                ("phase3","Phase 3 — 90 to 180 days",GREEN)]:
            phase = ap.get(key, {})
            if not phase: continue
            story.append(KeepTogether([
                Paragraph(f"<b>{icon}: {phase.get('title','')}</b>",
                    ParagraphStyle("ph", fontName="Helvetica-Bold",
                        fontSize=10.5, textColor=col, spaceBefore=6)),
                Paragraph(phase.get("description",""), S["sm"]),
                *[bul(t) for t in phase.get("tasks",[])],
                Spacer(1, 3*mm),
            ]))

    # ── Survey Readiness ───────────────────────────────────────────────────
    sr = result.get("survey_readiness", {})
    if sr:
        story += section("Survey Readiness", "")
        rc = GREEN if ready else RED
        story.append(info(
            f"{'READY FOR SURVEY' if ready else 'NOT YET READY FOR SURVEY'}  |  "
            f"Estimated readiness: {readiness}",
            border=rc,
            bg=colors.HexColor("#E8FFF4") if ready else colors.HexColor("#FFF0F3")))
        story.append(Spacer(1, 3*mm))
        for risk in sr.get("key_risks", []):
            story.append(bul(risk))

    # ── Footer page ────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 60*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD,
                             spaceBefore=4*mm, spaceAfter=6*mm))
    story.append(Paragraph("DentEdTech — CBAHI Reviewer",
        ParagraphStyle("fb", fontName="Helvetica-Bold", fontSize=13,
            textColor=DARK_NAVY, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph(
        "© 2026 DentEdTech. All rights reserved. "
        "This report is AI-generated for accreditation preparation purposes only. "
        "It does not constitute an official CBAHI survey or guarantee any accreditation outcome. "
        "CBAHI is a registered trademark of the Saudi Central Board for Accreditation of Healthcare Institutions.",
        ParagraphStyle("fd", fontName="Helvetica", fontSize=8,
            textColor=MID_GREY, alignment=TA_CENTER, leading=12)))

    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
    buf.seek(0)
    return buf.read()
