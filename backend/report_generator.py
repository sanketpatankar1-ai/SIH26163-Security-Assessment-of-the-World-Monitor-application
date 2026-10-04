"""
backend/report_generator.py
=============================
PDF Security Assessment Report Generator

Uses ReportLab to create a professional PDF report.

The report follows the structure:
  1. Cover Page
  2. Executive Summary
  3. Assessment Scope & Methodology
  4. Security Score Overview
  5. Findings Summary Table
  6. Detailed Findings (one per section)
  7. Limitations
  8. Conclusion
"""

import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import (
    HexColor, black, white, grey
)
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from xml.sax.saxutils import escape as xml_escape

def safe_html(text: str) -> str:
    """Safely escape text for ReportLab's XML-based Paragraph parser."""
    if not text:
        return ""
    return xml_escape(str(text)).replace("\n", "<br/>")

# ─── Color Palette ────────────────────────────────────────────────────────────
COLOR_PRIMARY = HexColor("#1e40af")     # Professional blue
COLOR_CRITICAL = HexColor("#dc2626")   # Red
COLOR_HIGH = HexColor("#ea580c")       # Orange
COLOR_MEDIUM = HexColor("#ca8a04")     # Yellow/amber
COLOR_LOW = HexColor("#2563eb")        # Blue
COLOR_INFO = HexColor("#6b7280")       # Gray
COLOR_SUCCESS = HexColor("#16a34a")    # Green
COLOR_LIGHT_BG = HexColor("#f8fafc")   # Light gray background
COLOR_BORDER = HexColor("#e2e8f0")     # Border gray

SEVERITY_COLORS = {
    "Critical": COLOR_CRITICAL,
    "High": COLOR_HIGH,
    "Medium": COLOR_MEDIUM,
    "Low": COLOR_LOW,
    "Informational": COLOR_INFO,
}

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def _get_styles():
    """Create and return custom paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        textColor=COLOR_PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        fontName="Helvetica",
        fontSize=13,
        textColor=grey,
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=COLOR_PRIMARY,
        spaceBefore=16,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="FindingTitle",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=black,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontName="Helvetica",
        fontSize=9,
        textColor=HexColor("#374151"),
        spaceAfter=4,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="Label",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=HexColor("#6b7280"),
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="Evidence",
        fontName="Courier",
        fontSize=8,
        textColor=HexColor("#1e293b"),
        backColor=HexColor("#f1f5f9"),
        spaceAfter=6,
        leftIndent=10,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name="Disclaimer",
        fontName="Helvetica-Oblique",
        fontSize=8,
        textColor=HexColor("#6b7280"),
        alignment=TA_CENTER,
        spaceAfter=4,
    ))

    return styles


def generate_pdf_report(findings, last_assessment=None) -> str:
    """
    Generate a PDF assessment report.

    Args:
        findings: List of FindingModel objects from the database
        last_assessment: AssessmentModel object (optional)

    Returns:
        Absolute path to the generated PDF file
    """
    today = datetime.date.today()
    filename = f"world-monitor-security-report-{today}.pdf"
    output_path = os.path.join(REPORTS_DIR, filename)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = _get_styles()
    story = []

    # ── Cover Page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("🔒 Security Assessment Report", styles["ReportTitle"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("World Monitor Application", styles["ReportSubtitle"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        f"SIH26163 — Smart India Hackathon 2026",
        styles["ReportSubtitle"]
    ))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_PRIMARY))
    story.append(Spacer(1, 0.5*cm))

    # Meta table
    meta_data = [
        ["Report Date:", str(today)],
        ["Target Application:", "World Monitor (Simulated Prototype)"],
        ["Assessment Type:", "Web Application Security Assessment"],
        ["Classification:", "PROTOTYPE — For Educational/Demonstration Use"],
    ]
    meta_table = Table(meta_data, colWidths=[5*cm, 11*cm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), HexColor("#6b7280")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ── 1. Executive Summary ────────────────────────────────────────────────
    story.append(Paragraph("1. Executive Summary", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.3*cm))

    open_count = sum(1 for f in findings if f.status == "Open")
    severity_counts = {}
    for f in findings:
        severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

    # Calculate score
    deductions = {"Critical": 15, "High": 8, "Medium": 4, "Low": 1, "Informational": 0}
    total_deduction = sum(
        deductions.get(f.severity, 0)
        for f in findings if f.status == "Open"
    )
    score = max(0, 100 - total_deduction)

    if score >= 90: grade = "A (Excellent)"
    elif score >= 75: grade = "B (Good)"
    elif score >= 60: grade = "C (Fair)"
    elif score >= 40: grade = "D (Poor)"
    else: grade = "F (Critical Risk)"

    summary_text = (
        f"A security assessment was conducted on the World Monitor application as part of the "
        f"SIH26163 Smart India Hackathon 2026 prototype. The assessment covered seven security "
        f"domains: Authentication, Authorization, API Security, Input Validation, "
        f"Communication Security, Client-Side Security, and Data Storage & Privacy. "
        f"<br/><br/>"
        f"The assessment identified <b>{len(findings)} security findings</b>, of which "
        f"<b>{open_count} are currently Open</b>. The prototype security score is "
        f"<b>{score}/100 ({grade})</b>."
        f"<br/><br/>"
        f"<b>Note:</b> This assessment was performed on a controlled simulated target for "
        f"demonstration purposes. This is not an industry-certified security audit."
    )
    story.append(Paragraph(summary_text, styles["BodyText2"]))
    story.append(Spacer(1, 0.5*cm))

    # Score table
    score_data = [
        ["Security Score", "Grade", "Total Findings", "Open", "Critical", "High", "Medium"],
        [
            str(score) + "/100",
            grade.split()[0],
            str(len(findings)),
            str(open_count),
            str(severity_counts.get("Critical", 0)),
            str(severity_counts.get("High", 0)),
            str(severity_counts.get("Medium", 0)),
        ],
    ]
    score_table = Table(score_data, colWidths=[2.5*cm]*7)
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_LIGHT_BG, white]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(score_table)
    story.append(PageBreak())

    # ── 2. Scope & Methodology ──────────────────────────────────────────────
    story.append(Paragraph("2. Assessment Scope & Methodology", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.3*cm))

    scope_text = (
        "<b>Target:</b> Simulated World Monitor Web Application (http://localhost:5001)<br/>"
        "<b>Assessment Type:</b> White-box inspection of a controlled prototype<br/>"
        "<b>Scope:</b> Authentication, Authorization, API Security, Input Validation, "
        "Communication Security, Client-Side Security, Data Storage &amp; Privacy<br/><br/>"
        "<b>Methodology:</b> Safe, non-destructive HTTP request inspection. Each check module "
        "sends legitimate HTTP requests and analyzes responses for security weaknesses. "
        "No exploit payloads, no denial-of-service tests, no database manipulation.<br/><br/>"
        "<b>Scoring Methodology:</b> Prototype Security Score starts at 100 and deducts: "
        "Critical −15, High −8, Medium −4, Low −1, Informational −0 per open finding."
    )
    story.append(Paragraph(scope_text, styles["BodyText2"]))
    story.append(PageBreak())

    # ── 3. Findings ─────────────────────────────────────────────────────────
    story.append(Paragraph("3. Security Findings", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.3*cm))

    # Summary table
    table_data = [["ID", "Title", "Category", "Severity", "Status", "Source"]]
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}
    sorted_findings = sorted(findings, key=lambda f: severity_order.get(f.severity, 5))

    for f in sorted_findings:
        table_data.append([
            f.id, f.title[:40] + ("..." if len(f.title) > 40 else ""),
            f.category, f.severity, f.status, f.source
        ])

    col_widths = [1.8*cm, 5.5*cm, 3*cm, 2*cm, 2*cm, 1.5*cm]
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_LIGHT_BG, white]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    # Color severity column
    for i, f in enumerate(sorted_findings, start=1):
        c = SEVERITY_COLORS.get(f.severity, grey)
        t.setStyle(TableStyle([("TEXTCOLOR", (3, i), (3, i), c),
                                ("FONTNAME", (3, i), (3, i), "Helvetica-Bold")]))

    story.append(t)
    story.append(PageBreak())

    # ── 4. Detailed Findings ─────────────────────────────────────────────────
    story.append(Paragraph("4. Detailed Findings", styles["SectionHeading"]))

    for f in sorted_findings:
        sev_color = SEVERITY_COLORS.get(f.severity, grey)

        story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
        story.append(Spacer(1, 0.2*cm))

        # Finding header
        header_data = [[
            Paragraph(f"<b>{f.id}</b> — {f.title}", styles["FindingTitle"]),
            Paragraph(f"<b><font color='{sev_color.hexval()}'>{f.severity}</font></b> | {f.category} | {f.status} | <i>{f.source}</i>", styles["BodyText2"]),
        ]]
        header_table = Table(header_data, colWidths=[9*cm, 7*cm])
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(header_table)

        story.append(Paragraph("Description", styles["Label"]))
        story.append(Paragraph(safe_html(f.description), styles["BodyText2"]))

        story.append(Paragraph("Affected Component", styles["Label"]))
        story.append(Paragraph(safe_html(f.affected_component), styles["BodyText2"]))

        story.append(Paragraph("Evidence", styles["Label"]))
        story.append(Paragraph(safe_html(f.evidence), styles["Evidence"]))

        story.append(Paragraph("Impact", styles["Label"]))
        story.append(Paragraph(safe_html(f.impact), styles["BodyText2"]))

        story.append(Paragraph("Recommendation", styles["Label"]))
        story.append(Paragraph(safe_html(f.recommendation), styles["BodyText2"]))

        if f.cwe_id:
            story.append(Paragraph(f"CWE Reference: {safe_html(f.cwe_id)}", styles["Disclaimer"]))

        story.append(Spacer(1, 0.4*cm))

    story.append(PageBreak())

    # ── 5. Limitations & Conclusion ─────────────────────────────────────────
    story.append(Paragraph("5. Limitations", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "• This assessment was performed on a simulated/controlled prototype target, not a real production system.<br/>"
        "• The security score is a prototype educational metric, not an industry-certified rating (e.g., CVSS).<br/>"
        "• Dynamic checks requiring a running browser (DOM XSS, CSRF tokens) were not performed.<br/>"
        "• No penetration testing, fuzzing, or destructive testing was performed.<br/>"
        "• Results apply only to the assessed version of the target application.",
        styles["BodyText2"]
    ))

    story.append(Paragraph("6. Conclusion", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"The World Monitor Security Assessment Platform (SIH26163 Prototype) successfully "
        f"demonstrates a complete security assessment workflow including automated checks, "
        f"structured findings, severity classification, evidence documentation, impact "
        f"assessment, remediation recommendations, and report generation.<br/><br/>"
        f"The prototype security score of {score}/100 reflects the identified issues in the "
        f"simulated target. Addressing the Critical and High severity findings would "
        f"significantly improve the application's security posture.",
        styles["BodyText2"]
    ))

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Paragraph(
        "PROTOTYPE — SIH26163 | Smart India Hackathon 2026 | For Educational/Demonstration Use Only",
        styles["Disclaimer"]
    ))

    doc.build(story)
    print(f"Report generated: {output_path}")
    return output_path
