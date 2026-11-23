"""Printable clinical summary report generator for AsthenoZero."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from eyeguard.clinical_pathology import get_vulnerable_conditions, get_ophthalmic_dietary_protocol
from eyeguard.theme import render_risk_gauge_svg


def generate_clinical_html_report(
    habit_data: dict[str, Any],
    risk_analysis: dict[str, Any],
    blink_data: dict[str, Any] | None = None,
) -> str:
    """Generate a clean, printable medical-grade HTML clinical assessment report."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score = float(risk_analysis.get("estimated_score", 0.0))
    severity = risk_analysis.get("severity", "Unassessed")
    summary = risk_analysis.get("summary_text", "")

    # Drivers list
    drivers_html = ""
    for driver in risk_analysis.get("risk_drivers", []):
        drivers_html += f"""
        <li style="margin-bottom: 6px;">
            <strong>{driver['factor']}</strong> ({driver['impact']} Impact): {driver['detail']}
        </li>
        """
    if not drivers_html:
        drivers_html = "<li>No significant behavioral risk drivers identified.</li>"

    # Protective factors
    protective_html = ""
    for prot in risk_analysis.get("protective_factors", []):
        protective_html += f"""
        <li style="margin-bottom: 6px;">
            <strong>{prot['factor']}</strong>: {prot['detail']}
        </li>
        """
    if not protective_html:
        protective_html = "<li>None recorded.</li>"

    # Clinical recommendations
    recs_html = ""
    for rec in risk_analysis.get("clinical_recommendations", []):
        priority_color = "#DC2626" if rec['priority'] == "High" else "#0284C7"
        recs_html += f"""
        <div style="border-left: 3px solid {priority_color}; padding-left: 12px; margin-bottom: 14px;">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: {priority_color}; font-weight: 700;">
                {rec['category']} &bull; {rec['priority']} Priority
            </div>
            <div style="font-weight: 600; font-size: 0.95rem; color: #0F172A; margin: 2px 0;">
                {rec['title']}
            </div>
            <div style="font-size: 0.85rem; color: #334155; line-height: 1.5;">
                {rec['action']}
            </div>
            <div style="font-size: 0.75rem; color: #64748B; font-style: italic; margin-top: 3px;">
                Reference: {rec['evidence']}
            </div>
        </div>
        """

    # Blink diagnostic section
    blink_html = ""
    if blink_data and blink_data.get("phase") == "complete" and blink_data.get("blink_rate") is not None:
        rate = float(blink_data["blink_rate"])
        count = int(blink_data["blink_count"])
        coverage = float(blink_data["coverage_percent"])
        quality = blink_data.get("quality", "Standard")

        if rate < 8:
            interp = "Significant blink inhibition during screen reading (< 8/min). Elevated corneal desiccation risk."
            interp_color = "#DC2626"
        elif rate < 14:
            interp = "Typical screen-induced reduction (8-14/min). Mild ocular surface vulnerability."
            interp_color = "#D97706"
        else:
            interp = "Optimal blink frequency maintained (> 14/min). Good tear lipid film stability."
            interp_color = "#059669"

        blink_html = f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin: 16px 0;">
            <h3 style="margin-top:0; color:#0F172A; font-size:1.05rem;">Webcam Blink Diagnostic Summary (60s Reading Task)</h3>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 0.9rem;">
                <tr>
                    <td style="padding: 6px; border-bottom: 1px solid #E2E8F0;"><strong>Estimated Blink Rate:</strong></td>
                    <td style="padding: 6px; border-bottom: 1px solid #E2E8F0; font-weight: 700; color: #0284C7;">{rate:.1f} blinks/min</td>
                    <td style="padding: 6px; border-bottom: 1px solid #E2E8F0;"><strong>Total Blinks Detected:</strong></td>
                    <td style="padding: 6px; border-bottom: 1px solid #E2E8F0;">{count}</td>
                </tr>
                <tr>
                    <td style="padding: 6px;"><strong>Tracking Coverage:</strong></td>
                    <td style="padding: 6px;">{coverage:.0f}%</td>
                    <td style="padding: 6px;"><strong>Measurement Quality:</strong></td>
                    <td style="padding: 6px;">{quality}</td>
                </tr>
            </table>
            <div style="font-size: 0.85rem; color: {interp_color}; font-weight: 600;">
                Clinical Note: {interp}
            </div>
        </div>
        """
    else:
        blink_html = """
        <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 8px; padding: 12px; margin: 14px 0; font-size: 0.85rem; color: #64748B;">
            Live webcam blink test was not performed or not completed in this session.
        </div>
        """

    # Conditions Vulnerability HTML
    conditions = get_vulnerable_conditions(habit_data, score)
    conditions_html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px;">'
    for c in conditions:
        conditions_html += f"""
        <div style="border: 1px solid #E2E8F0; border-left: 4px solid {c['badge_color']}; border-radius: 6px; padding: 10px 12px; background: #F8FAFC;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
                <strong style="color: #0F172A; font-size: 0.9rem;">{c['icon']} {c['name']}</strong>
                <span style="font-size: 0.72rem; font-weight: 700; color: {c['badge_color']}; text-transform: uppercase;">{c['severity']}</span>
            </div>
            <p style="font-size: 0.8rem; color: #475569; margin: 4px 0 6px 0; line-height: 1.4;">{c['etiology']}</p>
            <div style="font-size: 0.76rem; color: #0369A1;"><strong>Prophylaxis:</strong> {c['prevention']}</div>
        </div>
        """
    conditions_html += '</div>'

    # Dietary Protocol HTML
    diet_plan = get_ophthalmic_dietary_protocol(habit_data, score)
    diet_html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px;">'
    for d in diet_plan:
        diet_html += f"""
        <div style="border: 1px solid #E2E8F0; border-left: 4px solid #0284C7; border-radius: 6px; padding: 10px 12px; background: #F8FAFC;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
                <strong style="color: #0F172A; font-size: 0.88rem;">{d['icon']} {d['nutrient']}</strong>
                <span style="font-size: 0.72rem; font-weight: 700; color: #0284C7;">{d['priority']}</span>
            </div>
            <div style="font-size: 0.8rem; color: #059669; font-weight: 600; margin-bottom: 2px;">Target: {d['dosage']}</div>
            <div style="font-size: 0.78rem; color: #334155; margin-bottom: 4px;"><strong>Sources:</strong> {d['food_sources']}</div>
            <div style="font-size: 0.74rem; color: #64748B; line-height: 1.3;">{d['clinical_mechanism']}</div>
        </div>
        """
    diet_html += '</div>'

    gauge_svg = render_risk_gauge_svg(score)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AsthenoZero Clinical Assessment Report - {now_str}</title>
<style>
    @media print {{
        body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; font-size: 11pt; }}
        .no-print {{ display: none; }}
        @page {{ margin: 15mm; }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0F172A;
        line-height: 1.5;
        background: #FFFFFF;
        max-width: 850px;
        margin: 0 auto;
        padding: 24px;
    }}
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 2px solid #0284C7;
        padding-bottom: 16px;
        margin-bottom: 20px;
    }}
    .title-box h1 {{
        font-size: 1.6rem;
        margin: 0;
        color: #0F172A;
    }}
    .title-box p {{
        font-size: 0.85rem;
        color: #64748B;
        margin: 4px 0 0 0;
    }}
    .meta-box {{
        text-align: right;
        font-size: 0.8rem;
        color: #64748B;
    }}
    .section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 4px;
        margin-top: 22px;
        margin-bottom: 12px;
    }}
    .habit-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
        margin-bottom: 16px;
    }}
    .habit-table th, .habit-table td {{
        border: 1px solid #E2E8F0;
        padding: 8px 12px;
        text-align: left;
    }}
    .habit-table th {{
        background: #F8FAFC;
        font-weight: 600;
        color: #475569;
    }}
    .disclaimer-box {{
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 12px;
        font-size: 0.75rem;
        color: #475569;
        margin-top: 24px;
    }}
    .print-btn {{
        background: #0284C7;
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        font-size: 0.9rem;
    }}
    .print-btn:hover {{
        background: #0369A1;
    }}
</style>
</head>
<body>

<div class="no-print" style="margin-bottom: 20px; text-align: right;">
    <button class="print-btn" onclick="window.print()">Print / Save as PDF</button>
</div>

<div class="header">
    <div class="title-box">
        <h1>AsthenoZero &bull; Clinical Assessment Report</h1>
        <p>Digital Eye Strain (Asthenopia) & Ocular Surface Ergonomic Evaluation</p>
    </div>
    <div class="meta-box">
        <strong>Report Date:</strong> {now_str}<br>
        <strong>Document ID:</strong> EG-{int(datetime.now().timestamp())}<br>
        <strong>Protocol:</strong> Ridge Regression Baseline v1.0
    </div>
</div>

<div style="display: flex; gap: 24px; align-items: center; margin-bottom: 20px;">
    <div style="flex: 1; text-align: center;">
        {gauge_svg}
    </div>
    <div style="flex: 1.4; font-size: 0.9rem;">
        <h3 style="margin-top: 0; color: #0F172A;">Clinical Risk Stratification</h3>
        <p style="margin: 6px 0;"><strong>Risk Category:</strong> <span style="font-weight:700; color:#0284C7;">{severity}</span> ({score:.1f} / 15.0)</p>
        <p style="margin: 6px 0; color: #334155;">{summary}</p>
        <div style="background: #EFF6FF; border-left: 3px solid #0284C7; padding: 8px 12px; margin-top: 10px; font-size: 0.82rem; color: #1E40AF;">
            <strong>Interpretation:</strong> Score combines 5 self-reported symptom dimensions (eye fatigue, headache, blurred vision, dryness, difficulty focusing).
        </div>
    </div>
</div>

<div class="section-title">User Screen Habit Telemetry</div>
<table class="habit-table">
    <tr>
        <th>Age Cohort</th>
        <td>{habit_data.get('age_group', 'N/A')}</td>
        <th>Daily Screen Time</th>
        <td>{habit_data.get('screen_time_category', 'N/A')}</td>
    </tr>
    <tr>
        <th>Average Sleep</th>
        <td>{habit_data.get('sleep_category', 'N/A')}</td>
        <th>Breaks Per Hour</th>
        <td>{habit_data.get('breaks_per_hour_category', 'N/A')}</td>
    </tr>
    <tr>
        <th>Primary Display Device</th>
        <td>{habit_data.get('primary_device', 'N/A')}</td>
        <th>Vision Correction / Lenses</th>
        <td>{habit_data.get('vision_correction', 'N/A')}</td>
    </tr>
</table>

<div class="section-title">Contributory Behavioral Factors</div>
<div style="display: flex; gap: 20px; font-size: 0.85rem;">
    <div style="flex: 1;">
        <h4 style="margin: 0 0 6px 0; color: #DC2626;">Risk Drivers:</h4>
        <ul style="padding-left: 18px; margin: 0;">
            {drivers_html}
        </ul>
    </div>
    <div style="flex: 1;">
        <h4 style="margin: 0 0 6px 0; color: #059669;">Protective Factors:</h4>
        <ul style="padding-left: 18px; margin: 0;">
            {protective_html}
        </ul>
    </div>
</div>

<div class="section-title">Diagnostic Objective Blink Evaluation</div>
{blink_html}

<div class="section-title">Ocular Condition Vulnerability & Risk Stratification</div>
{conditions_html}

<div class="section-title">Targeted Ophthalmic Nutritional & Dietary Protocol</div>
{diet_html}

<div class="section-title">Personalized Evidence-Based Clinical Action Plan</div>
{recs_html}

<div class="disclaimer-box">
    <strong>Educational & Investigational Notice:</strong> This summary is generated for educational exploration and personal habit reflection. AsthenoZero does not provide medical diagnosis, prescribe treatments, or substitute for a formal clinical examination by a licensed ophthalmologist or optometrist. Seek immediate emergency care for sudden vision changes, intense pain, or red painful eyes.
</div>

</body>
</html>
"""
    return html
