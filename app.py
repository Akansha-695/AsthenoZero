"""AsthenoZero: Premium Clinical Screen-Care & Digital Asthenopia Suite.

Provides exploratory survey risk estimation, live webcam blink-rate diagnostics,
a private longitudinal habit diary, a 20-20-20 smart break timer with audio chimes,
and dynamic clinical screen-care guidance.
"""

from __future__ import annotations

import io
import sys
import time
import uuid
from datetime import date
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from eyeguard.analytics import (  # noqa: E402
    build_symptom_correlation_chart,
    build_trend_chart,
    calculate_diary_kpis,
    get_cohort_comparison,
)
from eyeguard.blink_monitor import BlinkMonitor  # noqa: E402
from eyeguard.care_content import CARE_SECTIONS, CARE_SOURCES, URGENT_GUIDANCE  # noqa: E402
from eyeguard.clinical_pathology import (  # noqa: E402
    get_vulnerable_conditions,
    get_ophthalmic_dietary_protocol,
)
from eyeguard.eye_exercises import (  # noqa: E402
    EYE_EXERCISES,
    render_blink_squeeze_animation,
    render_figure_eight_animation,
)
from eyeguard.gamification import (  # noqa: E402
    award_coins,
    ensure_gamification_state,
    notify_activity_completed,
    render_gamification_sidebar,
    render_strict_rehab_alert,
    render_top_navbar_badges,
)
from eyeguard.recommendations import analyze_risk_factors  # noqa: E402
from eyeguard.report_generator import generate_clinical_html_report  # noqa: E402
from eyeguard.sound_alerts import trigger_audio_chime  # noqa: E402
from eyeguard.theme import get_clinical_theme_css, render_risk_gauge_svg  # noqa: E402


MODEL_PATH = PROJECT_ROOT / "models" / "eyeguard_ridge.joblib"
MANUAL_PATH = PROJECT_ROOT / "output" / "pdf" / "eyeguard_user_manual.pdf"

AGE_GROUPS = ["15-18", "19-24", "25-34", "35-45", "45+"]
SCREEN_TIME = [
    "Less than 2 hours",
    "2-4 hours",
    "4-6 hours",
    "6-8 hours",
    "More than 8 hours",
]
SLEEP = [
    "Less than 5 hours",
    "5-6 hours",
    "6-7 hours",
    "7-8 hours",
    "More than 8 hours",
]
BREAKS = ["0", "1-2", "2-3", "4-5", "5 or more"]
DEVICES = ["Phone", "Laptop / PC", "Tab", "All roughly equal"]
VISION_CORRECTION = ["No", "Yes"]
SYMPTOMS = [
    ("Eye strain or tiredness", "symptom_eye_strain"),
    ("Headache", "symptom_headache"),
    ("Blurred vision", "symptom_blurred_vision"),
    ("Dry or irritated eyes", "symptom_dry_eyes"),
    ("Difficulty focusing after screen use", "symptom_difficulty_focusing"),
]
FREQUENCY_VALUES = ["Never", "Sometimes", "Often", "Always"]
FREQUENCY_SCORES = {answer: score for score, answer in enumerate(FREQUENCY_VALUES)}


@st.cache_resource
def load_model(model_path: str, modified_time: float) -> dict:
    del modified_time
    return joblib.load(model_path)


def _ensure_session_state() -> None:
    st.session_state.setdefault("blink_monitor", None)
    st.session_state.setdefault("last_blink_report", None)
    st.session_state.setdefault("habit_entries", [])
    st.session_state.setdefault("paired_exports", [])
    st.session_state.setdefault("timer_running", False)
    st.session_state.setdefault("timer_deadline", None)
    st.session_state.setdefault("timer_started_at", None)
    st.session_state.setdefault("timer_duration", 0)
    st.session_state.setdefault("timer_kind", "")
    st.session_state.setdefault("timer_paused_remaining", 0)
    st.session_state.setdefault("timer_complete", False)
    st.session_state.setdefault("last_risk_assessment", None)
    st.session_state.setdefault("audio_enabled", True)
    st.session_state.setdefault("reader_font_size", "Medium (16px)")
    st.session_state.setdefault("reader_high_contrast", False)
    st.session_state.setdefault("exercises_completed_today", 0)
    st.session_state.setdefault("strict_interlock", False)
    ensure_gamification_state()


def _render_sidebar() -> None:
    with st.sidebar:
        st.html(
            """<div style="display:flex; align-items:center; gap:12px; margin-bottom: 12px; padding: 4px 0;">
<div style="width:42px; height:42px; border-radius:12px; background:linear-gradient(135deg, #0284C7, #06B6D4); display:flex; align-items:center; justify-content:center; font-size:22px; box-shadow:0 0 18px rgba(6,182,212,0.45); border:1px solid rgba(255,255,255,0.2);">👁️</div>
<div>
<div style="font-size:1.2rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.03em;">AsthenoZero</div>
<div style="font-size:0.68rem; font-weight:700; color:#38BDF8; letter-spacing:0.08em; text-transform:uppercase;">Precision Suite v2.5 Pro</div>
</div>
</div>"""
        )
        st.caption("Investigational precision health-tech platform for digital asthenopia and ocular ergonomics.")
        st.divider()

        render_gamification_sidebar()

        st.divider()
        st.markdown("### 🔔 Audio Alerts & Chimes")
        audio_toggle = st.checkbox(
            "Enable chime on timer completion",
            value=st.session_state["audio_enabled"],
            help="Plays a pleasant Web Audio chime when the 20-20-20 or focus timer completes.",
        )
        st.session_state["audio_enabled"] = audio_toggle

        if st.button("🔔 Test Notification Chime", help="Play a sample notification chime", use_container_width=True):
            trigger_audio_chime("focus_complete")
            st.toast("Playing synthetic medical chime...", icon="🔔")

        st.divider()
        st.markdown("### 🩺 Diagnostic Engine")
        st.html(
            """<div class="clinical-card" style="padding: 14px 16px !important; margin-bottom: 10px !important;">
<div style="font-size: 0.8rem; line-height: 1.8; color: #94A3B8;">
<div><span style="color:#38BDF8; font-weight:700;">● ML Regressor:</span> Ridge (CV MAE 2.40)</div>
<div><span style="color:#34D399; font-weight:700;">● Eye Tracking:</span> MediaPipe Face Mesh</div>
<div><span style="color:#FBBF24; font-weight:700;">● Break Regimen:</span> 20-20-20 Ophthalmic</div>
<div><span style="color:#A78BFA; font-weight:700;">● Data Privacy:</span> In-Memory Isolation</div>
</div>
</div>"""
        )

        st.divider()
        st.markdown("### 📚 Clinical Documentation")
        if MANUAL_PATH.exists():
            st.download_button(
                "📥 Download User Manual (PDF)",
                data=MANUAL_PATH.read_bytes(),
                file_name="asthenozero_user_manual.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.caption("PDF user manual is available in the output directory.")

        st.divider()
        with st.expander("🔬 Model Validation & Telemetry (Examiner)", expanded=False):
            st.caption("Grouped 5-Fold Cross-Validation Metrics & Permutation Importance for technical evaluators.")
            results_table = pd.DataFrame(
                [
                    {"Model Architecture": "Mean Dummy Baseline", "MAE": "2.63 ± 0.27", "RMSE": "3.18", "R²": "-0.03"},
                    {"Model Architecture": "L2 Ridge (alpha=5.0)", "MAE": "2.40 ± 0.32", "RMSE": "2.88", "R²": "0.15"},
                    {"Model Architecture": "Random Forest Regressor", "MAE": "2.47 ± 0.33", "RMSE": "2.96", "R²": "0.11"},
                ]
            )
            st.dataframe(results_table, use_container_width=True, hide_index=True)
            st.markdown(
                """**Top Predictive Drivers:**
1. **Sleep Category** (`+0.086` Mean MAE Increase)
2. **Vision Correction** (`+0.077` Mean MAE Increase)
3. **Screen Exposure** (`+0.041` Mean MAE Increase)
4. **Primary Display** (`+0.032` Mean MAE Increase)
"""
            )
            st.caption("Evaluated on N=139 survey cohort with grouped cross-validation.")

        st.divider()
        st.html(
            """<div style="font-size: 0.72rem; color: #64748B; line-height: 1.5; padding: 4px;">
<strong>Educational Notice:</strong> AsthenoZero is an investigational screening tool for personal reflection. It does not diagnose medical conditions or substitute for professional ophthalmic examination.
</div>
<div style="font-size: 0.76rem; color: #94A3B8; line-height: 1.6; padding: 6px 4px 2px 4px; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 8px;">
<div><strong>Author:</strong> <span style="color:#F8FAFC; font-weight:600;">Akansha Kashyap</span></div>
<div style="margin-top: 3px;"><a href="https://www.linkedin.com/in/akansha-kashyap-b6a32b362" target="_blank" style="color:#38BDF8; text-decoration:none; font-weight:500;">🔗 View LinkedIn Profile</a></div>
<div style="font-size: 0.68rem; color: #64748B; margin-top: 3px;">License: Permissive Open-Source &bull; &copy; 2026</div>
</div>"""
        )


def _render_hero_banner() -> None:
    streak_badges = render_top_navbar_badges()
    st.html(
        f"""<div class="premium-navbar">
<div class="brand-identity">
<div class="brand-logo-icon">👁️</div>
<div>
<div class="brand-title">AsthenoZero <span class="pro-pill">PRO CLINICAL v2.5</span></div>
<div class="brand-tagline">Precision Digital Asthenopia Screening, Real-time Blink Diagnostics & Ocular Ergonomics</div>
</div>
</div>
<div class="telemetry-badges">
{streak_badges}
<span class="telemetry-pill">● L2 Ridge Model (MAE 2.40)</span>
<span class="telemetry-pill">● Zero Data Retention</span>
</div>
</div>"""
    )


def _render_survey_estimate() -> None:
    st.markdown("### 📊 Clinical Symptom & Habit Risk Assessment")
    st.write(
        "Evaluate your daily digital device habits to calculate your estimated digital eye strain "
        "(asthenopia) risk score, identify behavioral risk drivers, and generate a tailored clinical care plan."
    )

    if not MODEL_PATH.exists():
        st.error(
            "The local Ridge model artifact was not found. Please run "
            "`python src\\eyeguard\\train_baseline.py` in PowerShell to generate it."
        )
        return

    artifact = load_model(str(MODEL_PATH), MODEL_PATH.stat().st_mtime)
    model = artifact["model"]
    cv_metrics = artifact["cv_metrics"]

    preset_choice = st.selectbox(
        "⚡ Quick Occupational Archetype (Auto-Fill Profile)",
        [
            "Custom Profile (Manual Selection)",
            "Software Engineer / Data Analyst (10+ hrs screen, 6h sleep, Laptop)",
            "Student / Mobile Focus (8 hrs screen, Phone/Tab, irregular sleep)",
            "Office Executive (7 hrs screen, Laptop, 7h sleep, Glasses)",
            "Ergonomically Mindful (3 hrs screen, 8h sleep, frequent breaks)",
        ],
        index=0,
        help="Select a typical occupational archetype to populate input parameters instantly.",
    )

    if "Software Engineer" in preset_choice:
        def_age, def_screen, def_sleep, def_breaks, def_device, def_vis = 2, 4, 1, 1, 1, 1
    elif "Student" in preset_choice:
        def_age, def_screen, def_sleep, def_breaks, def_device, def_vis = 1, 3, 0, 0, 0, 0
    elif "Office Executive" in preset_choice:
        def_age, def_screen, def_sleep, def_breaks, def_device, def_vis = 2, 3, 2, 1, 1, 1
    elif "Ergonomically Mindful" in preset_choice:
        def_age, def_screen, def_sleep, def_breaks, def_device, def_vis = 2, 1, 3, 3, 1, 0
    else:
        def_age, def_screen, def_sleep, def_breaks, def_device, def_vis = 1, 3, 2, 1, 1, 0

    col_inputs, col_gauge = st.columns([1.1, 1], gap="large")

    with col_inputs:
        with st.form("survey_clinical_form"):
            st.markdown("#### Patient Habit Profile")
            age_group = st.selectbox("Age Cohort", AGE_GROUPS, index=def_age, help="Age group of the user")
            screen_time = st.selectbox(
                "Average Daily Screen Exposure",
                SCREEN_TIME,
                index=def_screen,
                help="Cumulative hours spent on digital displays per day",
            )
            sleep = st.selectbox(
                "Nightly Sleep Duration",
                SLEEP,
                index=def_sleep,
                help="Average restorative sleep obtained per night",
            )
            breaks = st.selectbox(
                "Micro-Breaks Per Hour of Continuous Screen Use",
                BREAKS,
                index=def_breaks,
                help="Frequency of pauses (>20 seconds) per continuous hour of viewing",
            )
            device = st.selectbox(
                "Primary Screen Device",
                DEVICES,
                index=def_device,
                help="Device accounting for majority of daily visual engagement",
            )
            vision_correction = st.selectbox(
                "Corrective Lenses Worn",
                VISION_CORRECTION,
                index=def_vis,
                help="Whether you wear prescription glasses or contact lenses during screen work",
            )
            calculate_btn = st.form_submit_button("🩺 Compute Clinical Assessment", type="primary", use_container_width=True)

    if calculate_btn or st.session_state.get("last_risk_assessment") is None:
        input_row = pd.DataFrame(
            {
                "age_group": [age_group],
                "screen_time_category": [screen_time],
                "sleep_category": [sleep],
                "breaks_per_hour_category": [breaks],
                "primary_device": [device],
                "vision_correction": [vision_correction],
            }
        )
        predicted_score = float(model.predict(input_row)[0])
        predicted_score = max(0.0, min(15.0, predicted_score))

        habit_dict = {
            "age_group": age_group,
            "screen_time_category": screen_time,
            "sleep_category": sleep,
            "breaks_per_hour_category": breaks,
            "primary_device": device,
            "vision_correction": vision_correction,
        }
        analysis = analyze_risk_factors(
            age_group=age_group,
            screen_time=screen_time,
            sleep=sleep,
            breaks=breaks,
            device=device,
            vision_correction=vision_correction,
            estimated_score=predicted_score,
        )
        st.session_state["last_risk_assessment"] = {
            "habit_dict": habit_dict,
            "analysis": analysis,
            "predicted_score": predicted_score,
        }
        if calculate_btn:
            award_coins(10, "Clinical Risk Assessment")

    cached = st.session_state.get("last_risk_assessment")
    if cached:
        analysis = cached["analysis"]
        habit_dict = cached["habit_dict"]
        score = cached["predicted_score"]

        with col_gauge:
            st.markdown("#### Clinical Risk Stratification")
            # Dedicated high-tech vector gauge
            st.html(render_risk_gauge_svg(score))

            # Cohort comparison
            screen_hours_map = {
                "Less than 2 hours": 1.5,
                "2-4 hours": 3.0,
                "4-6 hours": 5.0,
                "6-8 hours": 7.0,
                "More than 8 hours": 9.5,
            }
            sleep_hours_map = {
                "Less than 5 hours": 4.5,
                "5-6 hours": 5.5,
                "6-7 hours": 6.5,
                "7-8 hours": 7.5,
                "More than 8 hours": 8.5,
            }
            cohort_comp = get_cohort_comparison(
                screen_hours=screen_hours_map.get(habit_dict["screen_time_category"], 6.0),
                sleep_hours=sleep_hours_map.get(habit_dict["sleep_category"], 7.0),
            )

            st.html(
                f"""<div class="clinical-card" style="margin-top: 14px; font-size: 0.88rem;">
<div style="font-weight: 700; color: #38BDF8; margin-bottom: 8px; font-size:0.95rem;">📊 Research Cohort Benchmark</div>
<div style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
<span style="color:#94A3B8;">Screen Exposure:</span>
<span style="font-weight:700; color:#F8FAFC;">{cohort_comp['screen_percentile']}</span>
</div>
<div style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
<span style="color:#94A3B8;">Sleep Duration:</span>
<span style="font-weight:700; color:#F8FAFC;">{cohort_comp['sleep_percentile']}</span>
</div>
<div style="font-size: 0.75rem; color: #64748B; margin-top: 8px;">
Percentile rankings calibrated against N=139 clinical research survey participants.
</div>
</div>"""
            )

        # Contributory Factor Breakdown
        st.markdown("---")
        st.markdown("#### Behavioral Risk & Protective Telemetry")
        factor_col1, factor_col2 = st.columns(2, gap="medium")

        with factor_col1:
            st.html(
                """<div style="font-size: 0.95rem; font-weight: 700; color: #F87171; margin-bottom: 10px; display:flex; align-items:center; gap:6px;">
<span>⚠️</span> Contributory Risk Drivers
</div>"""
            )
            drivers = analysis.get("risk_drivers", [])
            if drivers:
                for driver in drivers:
                    st.html(
                        f"""<div class="clinical-card" style="border-left: 4px solid #EF4444 !important; background: rgba(239, 68, 68, 0.08) !important; padding: 14px 18px !important; margin-bottom: 10px !important;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span style="font-weight: 700; font-size: 0.92rem; color: #F8FAFC;">{driver['factor']}</span>
<span style="font-size: 0.7rem; background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.4); padding: 2px 8px; border-radius: 20px; font-weight:700;">{driver['impact']} IMPACT</span>
</div>
<div style="font-size: 0.84rem; color: #CBD5E1; margin-top: 6px; line-height:1.5;">{driver['detail']}</div>
</div>"""
                    )
            else:
                st.info("No primary behavioral risk drivers detected in current habits.")

        with factor_col2:
            st.html(
                """<div style="font-size: 0.95rem; font-weight: 700; color: #34D399; margin-bottom: 10px; display:flex; align-items:center; gap:6px;">
<span>🛡️</span> Protective Visual Habits
</div>"""
            )
            protectives = analysis.get("protective_factors", [])
            if protectives:
                for prot in protectives:
                    st.html(
                        f"""<div class="clinical-card" style="border-left: 4px solid #10B981 !important; background: rgba(16, 185, 129, 0.08) !important; padding: 14px 18px !important; margin-bottom: 10px !important;">
<div style="font-weight: 700; font-size: 0.92rem; color: #F8FAFC;">{prot['factor']}</div>
<div style="font-size: 0.84rem; color: #CBD5E1; margin-top: 6px; line-height:1.5;">{prot['detail']}</div>
</div>"""
                    )
            else:
                st.info("Consider adopting regular micro-breaks and screen-free sleep routines.")

        # Tailored Clinical Action Plan
        st.markdown("---")
        st.markdown("#### 📋 Tailored Clinical Action Plan")
        for rec in analysis.get("clinical_recommendations", []):
            priority_color = "#EF4444" if rec["priority"] == "High" else "#06B6D4"
            st.html(
                f"""<div class="clinical-card" style="border-left: 4px solid {priority_color} !important; padding: 16px 20px !important; margin-bottom: 12px !important;">
<div style="display:flex; justify-content: space-between; align-items:center; flex-wrap:wrap; gap:6px;">
<span style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: {priority_color}; letter-spacing:0.06em;">
{rec['category']} &bull; {rec['priority']} Priority
</span>
<span style="font-size: 0.72rem; color: #64748B; font-style: italic;">{rec['evidence']}</span>
</div>
<div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC; margin: 6px 0;">{rec['title']}</div>
<div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6;">{rec['action']}</div>
</div>"""
            )

        # Assessment Report Generation
        st.markdown("---")
        report_col1, report_col2 = st.columns([1, 1], gap="medium")
        with report_col1:
            st.markdown("#### 📄 Clinical Assessment Report")
            st.caption("Generate a publication-grade printable clinical summary report.")

            report_html = generate_clinical_html_report(
                habit_data=habit_dict,
                risk_analysis=analysis,
                blink_data=st.session_state.get("last_blink_report"),
            )
            st.download_button(
                "📥 Download Clinical Report (HTML / Printable PDF)",
                data=report_html.encode("utf-8"),
                file_name=f"asthenozero_clinical_report_{date.today().isoformat()}.html",
                mime="text/html",
                type="primary",
                use_container_width=True,
                help="Open in your browser and use Ctrl+P to save or print as PDF.",
            )

        with report_col2:
            st.markdown("#### 🔍 Model Diagnostics")
            st.html(
                f"""<div class="clinical-card" style="font-size: 0.85rem; color: #94A3B8;">
<div style="padding:4px 0;"><span style="color:#F8FAFC; font-weight:600;">&bull; Cross-Validation Mean MAE:</span> {cv_metrics['mae_mean']:.2f} score points</div>
<div style="padding:4px 0;"><span style="color:#F8FAFC; font-weight:600;">&bull; Fold-to-Fold Standard Deviation:</span> ±{cv_metrics['mae_sd']:.2f} points</div>
<div style="padding:4px 0;"><span style="color:#F8FAFC; font-weight:600;">&bull; Training Cohort:</span> N=139 survey responses</div>
<div style="padding:4px 0;"><span style="color:#F8FAFC; font-weight:600;">&bull; Algorithm:</span> L2 Ridge (alpha=5.0)</div>
</div>"""
            )

        # Potential Ocular Conditions & Disease Vulnerability
        st.markdown("---")
        st.markdown("#### 🩺 Potential Ocular Conditions & Disease Vulnerability")
        st.caption("Stratification of specific ocular surface and refractive conditions you are vulnerable to based on your telemetry:")
        vulnerable_conditions = get_vulnerable_conditions(habit_dict, score)
        
        cond_cols = st.columns(2)
        for idx, cond in enumerate(vulnerable_conditions):
            with cond_cols[idx % 2]:
                symptoms_list = "".join(f"<li>{s}</li>" for s in cond['hallmark_symptoms'])
                st.html(
                    f"""<div class="clinical-card" style="border-left: 4px solid {cond['badge_color']} !important; margin-bottom: 12px !important; height: calc(100% - 12px);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
    <strong style="color:#F8FAFC; font-size:1.02rem;">{cond['icon']} {cond['name']}</strong>
    <span style="font-size:0.72rem; font-weight:800; color:{cond['badge_color']}; text-transform:uppercase; background:rgba(0,0,0,0.3); padding:3px 8px; border-radius:4px; border:1px solid {cond['badge_color']};">{cond['severity']}</span>
</div>
<div style="font-size:0.85rem; color:#CBD5E1; line-height:1.5; margin-bottom:10px;">
    {cond['etiology']}
</div>
<div style="font-size:0.8rem; font-weight:700; color:#38BDF8; margin-bottom:3px;">Hallmark Symptoms to Monitor:</div>
<ul style="padding-left:18px; margin:0 0 10px 0; font-size:0.8rem; color:#94A3B8; line-height:1.5;">
    {symptoms_list}
</ul>
<div style="font-size:0.8rem; background:rgba(6,182,212,0.1); border:1px solid rgba(6,182,212,0.25); border-radius:6px; padding:8px 10px; color:#E2E8F0;">
    <strong style="color:#38BDF8;">Clinical Prophylaxis:</strong> {cond['prevention']}
</div>
</div>"""
                )

        # Targeted Ophthalmic Nutritional & Dietary Protocol
        st.markdown("---")
        st.markdown("#### 🥗 Targeted Ocular Nutrition & Dietary Protocol")
        st.caption("Nutritional ophthalmology interventions scientifically proven to optimize tear film stability and ciliary muscle recovery:")
        diet_plan = get_ophthalmic_dietary_protocol(habit_dict, score)
        
        diet_cols = st.columns(2)
        for idx, d_item in enumerate(diet_plan):
            with diet_cols[idx % 2]:
                st.html(
                    f"""<div class="clinical-card" style="border-left: 4px solid #06B6D4 !important; margin-bottom: 12px !important; height: calc(100% - 12px);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
    <strong style="color:#F8FAFC; font-size:1rem;">{d_item['icon']} {d_item['nutrient']}</strong>
    <span style="font-size:0.72rem; font-weight:800; color:#38BDF8; background:rgba(6,182,212,0.15); padding:2px 8px; border-radius:4px;">{d_item['priority']}</span>
</div>
<div style="font-size:0.82rem; color:#34D399; font-weight:700; margin-bottom:4px;">Target Daily Intake: {d_item['dosage']}</div>
<div style="font-size:0.84rem; color:#E2E8F0; margin-bottom:6px;"><strong>High-Potency Sources:</strong> {d_item['food_sources']}</div>
<div style="font-size:0.8rem; color:#94A3B8; line-height:1.45;"><strong>Biological Mechanism:</strong> {d_item['clinical_mechanism']}</div>
</div>"""
                )


def _render_blink_status(monitor: BlinkMonitor) -> None:
    @st.fragment(run_every=1)
    def status_panel() -> None:
        snapshot = monitor.snapshot()
        phase = snapshot["phase"]

        if phase == "waiting_for_face":
            st.info("📡 Camera feed initialized. Center your face in good lighting to begin calibration.")
        elif phase == "calibrating":
            st.info("🔬 Calibrating baseline ocular landmarks. Maintain a relaxed, natural forward gaze.")
            st.progress(snapshot["progress"], text=f"Ocular Calibration: {snapshot['seconds_remaining']} sec remaining")
        elif phase == "reading":
            st.info("📖 Standardized reading in progress. Read comfortably; blink naturally.")
            st.progress(snapshot["progress"], text=f"Diagnostic Test: {snapshot['seconds_remaining']} sec remaining")
            col_b1, col_b2 = st.columns(2)
            col_b1.metric("Blinks Detected", snapshot["blink_count"])
            col_b2.metric("Elapsed Time", f"{60 - snapshot['seconds_remaining']}s / 60s")
        elif phase == "complete":
            st.success("✅ Standardized 60-second reading diagnostic complete.")
            if snapshot["blink_rate"] is None:
                st.warning(
                    "Insufficient tracking coverage to calculate a reliable blink frequency. "
                    "Ensure adequate front lighting, remove thick frames if possible, and re-test."
                )
                st.metric("Tracking Coverage", f"{snapshot['coverage_percent']:.0f}%")
            else:
                m1, m2, m3, m4 = st.columns(4)
                rate = snapshot["blink_rate"]
                m1.metric("Blink Frequency", f"{rate:.1f} / min", delta="Resting: 15-20" if rate >= 15 else "Reduced", delta_color="normal" if rate >= 15 else "inverse")
                m2.metric("Blinks Counted", snapshot["blink_count"])
                m3.metric("Tracking Coverage", f"{snapshot['coverage_percent']:.0f}%")
                m4.metric("Signal Quality", snapshot["quality"])

                if rate < 8:
                    clinical_badge = "<span class='status-pill-badge badge-high'>● Severe Blink Inhibition (&lt; 8/min)</span>"
                    clinical_text = (
                        "Blink rate dropped significantly during display interaction. This precipitates rapid "
                        "tear film evaporation, corneal exposure, and acute dry eye discomfort."
                    )
                elif rate < 14:
                    clinical_badge = "<span class='status-pill-badge badge-moderate'>● Moderate Screen Reduction (8-14/min)</span>"
                    clinical_text = (
                        "Typical screen-induced reduction in spontaneous blink rate. Conscious blinking breaks "
                        "will maintain ocular surface hydration."
                    )
                else:
                    clinical_badge = "<span class='status-pill-badge badge-low'>● Optimal Blink Rate (&ge; 14/min)</span>"
                    clinical_text = (
                        "Excellent blink preservation during reading. Tear film homeostasis is well maintained."
                    )

                st.html(
                    f"""<div class="clinical-card" style="margin-top: 14px;">
<div style="margin-bottom: 8px;">{clinical_badge}</div>
<div style="font-size: 0.9rem; color: #E2E8F0; line-height: 1.6;">{clinical_text}</div>
</div>"""
                )
                if st.session_state.get("last_blink_report") != snapshot:
                    st.session_state["last_blink_report"] = snapshot
                    notify_activity_completed("diagnostic")
                else:
                    st.session_state["last_blink_report"] = snapshot
            if snapshot["error"]:
                st.caption(f"Telemetry warning: {snapshot['error']}")
        elif phase == "calibration_failed":
            st.error("❌ Calibration failed. Unable to establish stable eye landmark contours. Please check lighting.")
        elif phase == "camera_timeout":
            st.warning("⏱️ Face detection timeout. Face was not continuously visible. Reset and re-align.")
        elif phase == "idle":
            st.caption("Camera ready. Click 'Begin Diagnostic Test' below.")

        _render_paired_export(st.session_state.get("last_blink_report"))

    status_panel()


def _render_paired_export(report: dict | None) -> None:
    with st.expander("🔬 Optional Anonymous Paired-Data Research Export"):
        st.write(
            "Enables contributing anonymous paired habit, symptom, and blink diagnostic records for future "
            "model development. Data remains purely in local session memory until exported by you. Restricted to adults aged 18+."
        )
        if not report or report.get("phase") != "complete" or report.get("blink_rate") is None:
            st.info("Complete a valid blink test first to generate a research export record.")
            return

        with st.form("paired_export_form"):
            adult = st.checkbox("I confirm I am 18 years of age or older.")
            consent = st.checkbox("I freely agree to generate an anonymous project research export.")
            age_band = st.selectbox("Age Bracket", ["18-24", "25-34", "35-45", "45+"])
            screen_time = st.selectbox("Daily Screen Time", SCREEN_TIME, key="pair_screen")
            sleep = st.selectbox("Nightly Sleep", SLEEP, key="pair_sleep")
            breaks = st.selectbox("Hourly Breaks", BREAKS, key="pair_breaks")
            device = st.selectbox("Primary Display", DEVICES, key="pair_device")
            vision = st.selectbox("Corrective Lenses", VISION_CORRECTION, key="pair_vision")
            symptoms = {
                column: st.selectbox(label, FREQUENCY_VALUES, key=f"pair_{column}")
                for label, column in SYMPTOMS
            }
            add_export = st.form_submit_button("Generate Paired Research Row", type="primary")

        if add_export:
            if not adult or not consent:
                st.error("Both adult status confirmation and research consent are required.")
            else:
                row = {
                    "sample_id": str(uuid.uuid4()),
                    "test_date": date.today().isoformat(),
                    "age_band": age_band,
                    "screen_time_category": screen_time,
                    "sleep_category": sleep,
                    "breaks_per_hour_category": breaks,
                    "primary_device": device,
                    "vision_correction": vision,
                    **symptoms,
                    "exploratory_symptom_score": sum(
                        FREQUENCY_SCORES[value] for value in symptoms.values()
                    ),
                    "blink_rate_per_minute": round(float(report["blink_rate"]), 3),
                    "blink_count": int(report["blink_count"]),
                    "valid_tracking_seconds": round(float(report["valid_seconds"]), 2),
                    "tracking_coverage_percent": round(float(report["coverage_percent"]), 1),
                    "test_type": "standardized_60_second_reading",
                }
                st.session_state["paired_exports"].append(row)
                st.success("Paired row compiled in local session memory.")

        rows = st.session_state["paired_exports"]
        if rows:
            paired = pd.DataFrame(rows)
            st.download_button(
                "📥 Download Paired Dataset CSV",
                data=paired.to_csv(index=False).encode("utf-8"),
                file_name="eyeguard_paired_blink_survey_data.csv",
                mime="text/csv",
                help="Saves CSV locally. Never uploaded externally.",
            )


def _render_blink_test() -> None:
    st.markdown("### 👁️ Live Blink Diagnostic Suite")
    st.write(
        "Quantitative ocular surface assessment measuring spontaneous blink frequency during a "
        "standardized 60-second reading task. Evaluates blink inhibition induced by visual display engagement."
    )

    with st.expander("🔬 Biophysical Rationale & Clinical Principles", expanded=False):
        st.markdown(
            """
            - **Normal Physiology:** Resting human blink frequency typically ranges from **15 to 20 blinks per minute**.
            - **Visual Display Syndrome:** During sustained reading on digital screens, cognitive focus suppresses spontaneous blinking by **50% to 70%** (often dropping to 4–7 blinks/min).
            - **Incomplete Blinking:** Furthermore, up to 60% of blinks during screen engagement are partial, preventing complete apposition of the upper and lower eyelids and preventing full expression of the Meibomian lipid layer.
            - **Ocular Surface Result:** This acceleration of tear film breakup (TBUT < 10s) causes direct corneal desiccation, irritation, and reflex hyperlacrimation (watery eyes).
            """
        )

    st.html(
        """<div class="clinical-card" style="border-left: 4px solid #06B6D4 !important; padding: 14px 18px !important; margin: 14px 0 !important;">
<div style="display:flex; gap:10px; align-items:center;">
<span style="font-size:1.3rem;">🔒</span>
<div style="font-size:0.86rem; color:#E2E8F0; line-height:1.5;">
<strong>Privacy & Architecture Guarantee:</strong> Video frames are processed in-memory directly on your local device via Google MediaPipe. AsthenoZero never records, saves, or transmits camera frames.
</div>
</div>
</div>"""
    )

    camera_consent = st.checkbox(
        "I understand the local camera processing protocol and give consent to activate the camera widget."
    )
    if not camera_consent:
        st.info("The camera stream remains inactive until explicit consent is given above.")
        return

    monitor = st.session_state.get("blink_monitor")
    if monitor is None:
        monitor = BlinkMonitor()
        st.session_state["blink_monitor"] = monitor

    try:
        monitor.initialize()
        from streamlit_webrtc import webrtc_streamer
    except Exception as error:
        st.error(f"Could not initialize computer vision subsystem: {error}")
        return

    col_cam, col_task = st.columns([1, 1.2], gap="large")

    with col_cam:
        st.markdown("#### Live Vision Stream")

        def process_frame(frame):
            return monitor.process_frame(frame)

        context = webrtc_streamer(
            key="eyeguard-blink-camera",
            video_frame_callback=process_frame,
            media_stream_constraints={
                "video": {"width": {"ideal": 640}, "height": {"ideal": 480}},
                "audio": False,
            },
        )

        b_start, b_reset = st.columns(2)
        with b_start:
            if st.button(
                "🚀 Begin Diagnostic Test",
                type="primary",
                disabled=not bool(context.state.playing),
                use_container_width=True,
            ):
                monitor.start_test()
                st.session_state["last_blink_report"] = None
        with b_reset:
            if st.button("🔄 Reset Diagnostic", use_container_width=True):
                monitor.reset()
                st.session_state["last_blink_report"] = None

        if not context.state.playing:
            st.caption("Press 'START' in the camera widget above to launch your webcam.")

    with col_task:
        st.markdown("#### Standardized Reading Task")
        st.caption("Read the clinical passage below at a comfortable, natural pace during the 60-second diagnostic window.")

        # Reading accessibility controls
        acc1, acc2 = st.columns(2)
        with acc1:
            font_choice = st.selectbox(
                "Reading Typography Size",
                ["Standard (15px)", "Large (18px)", "High Legibility (21px)"],
                index=0,
            )
        with acc2:
            high_contrast = st.toggle("High Contrast Mode", value=False)

        font_size = "15px" if "Standard" in font_choice else ("18px" if "Large" in font_choice else "21px")
        bg_color = "rgba(10, 15, 29, 0.95)" if high_contrast else "rgba(15, 23, 42, 0.85)"
        text_color = "#38BDF8" if high_contrast else "#E2E8F0"

        st.html(
            f"""<div class="reading-passage-luxury" style="background: {bg_color}; color: {text_color}; font-size: {font_size}; max-height: 400px; overflow-y: auto;">
Digital display engagement fundamentally alters natural human oculomotor kinematics and tear film stability. When visually fixating on high-density alphanumeric characters, the intraocular ciliary muscle maintains uninterrupted tonic contraction to sustain positive dioptric accommodation. Simultaneously, cortical concentration suppresses the trigeminal blink reflex arc, causing spontaneous blink frequency to precipitously decline from a physiological baseline of 15–20 blinks per minute down to fewer than 5–7 blinks per minute.
<br><br>
This acute blink inhibition destabilizes the trilaminar pre-corneal tear film. Without frequent, complete eyelid apposition, the superficial lipid monolayer—secreted by the tarsal Meibomian glands—rapidly ruptures. Exposed aqueous tear fluid evaporates into ambient air currents, precipitating localized corneal desiccation, micro-epithelial friction, photophobia, and the burning sensation characteristic of digital asthenopia.
<br><br>
Furthermore, prolonged static gaze restricts physiological saccadic excursions and micro-fluctuations of accommodation, producing significant extraocular muscle fatigue across the recti and oblique muscle groups. Implementing periodic visual micro-breaks—such as directing gaze toward an optical infinity target situated at least twenty feet away for twenty seconds—permits complete mechanical relaxation of the ciliary ring and restores zonular tension equilibrium.
<br><br>
By engaging with this standardized reading passage, your visual system is subjected to a calibrated cognitive and optical workload. This uniform visual stimulus ensures that the real-time computer vision landmarker can isolate involuntary blink suppression patterns from variable baseline tasks, delivering an objective, reproducible assessment of your real-time ocular ergonomics.
</div>"""
        )

    st.markdown("---")
    _render_blink_status(monitor)


def _read_diary_upload(uploaded_file) -> list[dict]:
    frame = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))
    required = ["date", "screen_hours", "sleep_hours", "breaks", "symptom_score"]
    missing = set(required) - set(frame.columns)
    if missing:
        raise ValueError(f"Diary CSV missing required columns: {', '.join(sorted(missing))}")
    frame = frame[required].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise").dt.date.astype(str)
    for column in ["screen_hours", "sleep_hours", "breaks", "symptom_score"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if frame[["screen_hours", "sleep_hours", "breaks"]].isna().any().any():
        raise ValueError("Missing values in mandatory numeric columns.")
    if (frame["screen_hours"] < 0).any() or (frame["sleep_hours"] < 0).any():
        raise ValueError("Screen and sleep values cannot be negative.")
    if (frame["screen_hours"] > 24).any() or (frame["sleep_hours"] > 24).any():
        raise ValueError("Hours cannot exceed 24 per day.")
    if (frame["breaks"] < 0).any():
        raise ValueError("Break count cannot be negative.")
    return frame.to_dict(orient="records")


def _render_habit_diary() -> None:
    st.markdown("### 📈 Longitudinal Habit Diary & Visual Wellness Analytics")
    st.write(
        "Track your daily screen hours, restorative sleep, break adherence, and discomfort symptoms. "
        "Discover personalized trends, correlations, and evaluate your composite visual wellness index."
    )

    kpis = calculate_diary_kpis(st.session_state["habit_entries"])

    # Luxury Stats Tiles
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.html(
            f"""<div class="metric-tile" style="border-top-color: #38BDF8;">
<div class="metric-tile-label">Days Logged</div>
<div class="metric-tile-value">{kpis['total_days']}</div>
<div class="metric-tile-sub">Session history</div>
</div>"""
        )
    with k2:
        st.html(
            f"""<div class="metric-tile" style="border-top-color: #06B6D4;">
<div class="metric-tile-label">Mean Screen</div>
<div class="metric-tile-value">{kpis['avg_screen']:.1f}<span style="font-size:1rem; color:#94A3B8;">h/d</span></div>
<div class="metric-tile-sub">Daily exposure</div>
</div>"""
        )
    with k3:
        st.html(
            f"""<div class="metric-tile" style="border-top-color: #10B981;">
<div class="metric-tile-label">Mean Sleep</div>
<div class="metric-tile-value">{kpis['avg_sleep']:.1f}<span style="font-size:1rem; color:#94A3B8;">h/n</span></div>
<div class="metric-tile-sub">Restorative sleep</div>
</div>"""
        )
    with k4:
        st.html(
            f"""<div class="metric-tile" style="border-top-color: #F59E0B;">
<div class="metric-tile-label">Breaks / Hour</div>
<div class="metric-tile-value">{kpis['avg_breaks']:.1f}</div>
<div class="metric-tile-sub">Ocular rests</div>
</div>"""
        )
    with k5:
        score_color = "#10B981" if kpis['health_score'] >= 80 else ("#F59E0B" if kpis['health_score'] >= 60 else "#EF4444")
        st.html(
            f"""<div class="metric-tile" style="border-top-color: {score_color};">
<div class="metric-tile-label">Wellness Index</div>
<div class="metric-tile-value" style="color: {score_color};">{kpis['health_score']}<span style="font-size:1rem; color:#94A3B8;">/100</span></div>
<div class="metric-tile-sub">Composite score</div>
</div>"""
        )

    # Regain-Style Asthenopia Screen Exposure Budgeting
    with st.expander("🎯 Regain-Style Daily Screen Exposure Budget & Overuse Shield", expanded=False):
        budget_col1, budget_col2 = st.columns([1, 1.2])
        with budget_col1:
            screen_budget = st.slider(
                "Daily Safe Screen Limit Target (Hours)",
                min_value=3.0,
                max_value=12.0,
                value=7.0,
                step=0.5,
                help="Recommended safe threshold to avoid dry eye evaporative tear breakdown",
            )
        with budget_col2:
            avg_screen = kpis["avg_screen"]
            usage_pct = min(100.0, (avg_screen / screen_budget) * 100) if screen_budget > 0 else 0
            if avg_screen > screen_budget:
                st.html(
                    f"""<div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; border-radius:10px; padding:12px 16px; margin-top:6px;">
<div style="font-weight:800; color:#FCA5A5;">⚠️ Asthenopia Overuse Warning (+{avg_screen - screen_budget:.1f}h)</div>
<div style="font-size:0.84rem; color:#E2E8F0; margin-top:4px;">
Your current average screen exposure ({avg_screen:.1f}h) exceeds your daily budget. Tear film evaporation rate increases exponentially beyond 7h. Take a 20s optical break now!
</div>
</div>"""
                )
            else:
                st.html(
                    f"""<div style="background:rgba(16,185,129,0.15); border:1px solid #10B981; border-radius:10px; padding:12px 16px; margin-top:6px;">
<div style="font-weight:800; color:#6EE7B7;">✅ Within Safe Ocular Bounds ({usage_pct:.0f}% Consumed)</div>
<div style="font-size:0.84rem; color:#E2E8F0; margin-top:4px;">
Excellent ergonomic discipline. Mean daily exposure is {avg_screen:.1f}h of your {screen_budget:.1f}h safe threshold.
</div>
</div>"""
                )

    # Demo Telemetry Loader & Reset Controls
    d_btn1, d_btn2 = st.columns([1.2, 1])
    with d_btn1:
        if st.button("✨ Load 14-Day Sample Clinical History", use_container_width=True, help="Populate 14 days of realistic telemetry to explore analytics and charts"):
            today = date.today()
            sample_data = []
            for i in range(13, -1, -1):
                d = today - pd.Timedelta(days=int(i))
                base_screen = 7.5 + (1.2 if i % 7 < 5 else -1.8) + (i % 3) * 0.3
                base_sleep = 6.8 + (i % 2) * 0.5 - (0.6 if base_screen > 8.0 else 0)
                breaks = 1 if base_screen > 8.0 else (3 if i % 2 == 0 else 2)
                symptom = int(max(2, min(12, round(base_screen * 0.8 - base_sleep * 0.4 + (3 - breaks)))))
                sample_data.append({
                    "date": d.isoformat(),
                    "screen_hours": round(float(base_screen), 1),
                    "sleep_hours": round(float(base_sleep), 1),
                    "breaks": int(breaks),
                    "symptom_score": symptom,
                })
            st.session_state["habit_entries"] = sample_data
            st.toast("Loaded 14-day sample clinical history!", icon="✨")
            st.rerun()
    with d_btn2:
        if st.button("🗑️ Reset Diary History", use_container_width=True):
            st.session_state["habit_entries"] = []
            st.toast("Diary history cleared.", icon="🗑️")
            st.rerun()

    st.markdown("---")

    col_entry, col_charts = st.columns([1, 1.4], gap="large")

    with col_entry:
        st.markdown("#### 📝 Log Daily Telemetry")
        with st.form("habit_diary_entry_form"):
            entry_date = st.date_input("Entry Date", value=date.today())
            screen_hours = st.number_input(
                "Daily Screen Time (hours)",
                min_value=0.0,
                max_value=24.0,
                value=6.5,
                step=0.5,
                help="Total hours of digital display exposure today",
            )
            sleep_hours = st.number_input(
                "Sleep Last Night (hours)",
                min_value=0.0,
                max_value=24.0,
                value=7.0,
                step=0.5,
                help="Total hours of restorative sleep obtained",
            )
            breaks = st.number_input(
                "Hourly Micro-Breaks Taken",
                min_value=0,
                max_value=20,
                value=2,
                step=1,
                help="Average short breaks taken per continuous hour of screen use",
            )
            track_symptoms = st.checkbox("Record Today's Symptom Score", value=True)
            symptom_score = st.slider(
                "Symptom Discomfort Total (0-15)",
                min_value=0,
                max_value=15,
                value=4,
                disabled=not track_symptoms,
                help="Sum of 5 symptom items (Eye strain, headache, blur, dryness, focusing difficulty, 0-3 each)",
            )
            submit_log = st.form_submit_button("💾 Save Daily Log", type="primary", use_container_width=True)

        if submit_log:
            new_entry = {
                "date": entry_date.isoformat(),
                "screen_hours": float(screen_hours),
                "sleep_hours": float(sleep_hours),
                "breaks": int(breaks),
                "symptom_score": int(symptom_score) if track_symptoms else None,
            }
            existing = [item for item in st.session_state["habit_entries"] if str(item.get("date")) != new_entry["date"]]
            existing.append(new_entry)
            st.session_state["habit_entries"] = sorted(existing, key=lambda x: x["date"])
            notify_activity_completed("diary")
            st.success(f"Log for {entry_date.isoformat()} successfully saved.")
            st.rerun()

        # Diary CSV Import
        st.markdown("#### 📂 Import Historical Diary")
        with st.form("diary_import_form"):
            uploaded = st.file_uploader("Upload previously exported CSV", type=["csv"])
            import_btn = st.form_submit_button("Import CSV", use_container_width=True)

        if import_btn and uploaded is not None:
            try:
                imported = _read_diary_upload(uploaded)
                by_date = {str(item["date"]): item for item in st.session_state["habit_entries"]}
                by_date.update({str(item["date"]): item for item in imported})
                st.session_state["habit_entries"] = sorted(by_date.values(), key=lambda x: x["date"])
                st.success(f"Imported {len(imported)} historical diary entries.")
                st.rerun()
            except Exception as err:
                st.error(f"Import validation error: {err}")

    with col_charts:
        st.markdown("#### 📊 Analytical Visualizations")
        entries = st.session_state["habit_entries"]

        if entries:
            trend_chart = build_trend_chart(entries)
            if trend_chart:
                st.altair_chart(trend_chart, use_container_width=True)

            corr_chart = build_symptom_correlation_chart(entries)
            if corr_chart:
                st.altair_chart(corr_chart, use_container_width=True)

            df_entries = pd.DataFrame(entries).sort_values("date")
            st.markdown("##### Detailed Log Records")
            st.dataframe(df_entries, use_container_width=True, hide_index=True)

            st.download_button(
                "📥 Export Complete Diary CSV",
                data=df_entries.to_csv(index=False).encode("utf-8"),
                file_name="eyeguard_habit_diary.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info(
                "No diary records entered yet. Log your daily telemetry on the left or upload a historical CSV."
            )


def _start_timer(kind: str, minutes: int) -> None:
    duration = int(minutes * 60)
    now = time.monotonic()
    st.session_state["timer_kind"] = kind
    st.session_state["timer_duration"] = duration
    st.session_state["timer_deadline"] = now + duration
    st.session_state["timer_started_at"] = now
    st.session_state["timer_paused_remaining"] = duration
    st.session_state["timer_running"] = True
    st.session_state["timer_complete"] = False


def _render_break_timer() -> None:
    st.markdown("### ⏱️ 20-20-20 Smart Break Timer & Micro-Pause Suite")
    st.write(
        "Structured interval pacing designed to counteract continuous accommodative spasm of the ciliary muscle. "
        "Includes ophthalmic audio chimes and guided micro-break ocular exercises."
    )

    @st.fragment(run_every=1)
    def timer_panel() -> None:
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        with p_col1:
            st.html(
                """<div class="clinical-card" style="text-align:center; padding: 14px !important;">
<div style="font-weight:700; color:#38BDF8; font-size:0.95rem;">20-20-20 Rule</div>
<div style="font-size:0.75rem; color:#94A3B8;">20m Work &bull; 20s Rest</div>
</div>"""
            )
        with p_col2:
            st.html(
                """<div class="clinical-card" style="text-align:center; padding: 14px !important;">
<div style="font-weight:700; color:#38BDF8; font-size:0.95rem;">Pomodoro Classic</div>
<div style="font-size:0.75rem; color:#94A3B8;">25m Focus &bull; 5m Rest</div>
</div>"""
            )
        with p_col3:
            st.html(
                """<div class="clinical-card" style="text-align:center; padding: 14px !important;">
<div style="font-weight:700; color:#38BDF8; font-size:0.95rem;">Deep Focus</div>
<div style="font-size:0.75rem; color:#94A3B8;">50m Focus &bull; 10m Rest</div>
</div>"""
            )
        with p_col4:
            st.html(
                """<div class="clinical-card" style="text-align:center; padding: 14px !important;">
<div style="font-weight:700; color:#38BDF8; font-size:0.95rem;">Custom Pacing</div>
<div style="font-size:0.75rem; color:#94A3B8;">Configurable</div>
</div>"""
            )

        running = st.session_state["timer_running"]

        c_int1, c_int2 = st.columns(2)
        with c_int1:
            focus_minutes = st.number_input(
                "Focus Work Duration (minutes)", min_value=1, max_value=120, value=20, step=1, disabled=running
            )
        with c_int2:
            rest_minutes = st.number_input(
                "Micro-Break Rest Duration (minutes)", min_value=1, max_value=30, value=5, step=1, disabled=running
            )

        regain_col1, regain_col2 = st.columns(2)
        with regain_col1:
            strict_toggle = st.toggle(
                "🔒 Regain Strict Interlock",
                value=st.session_state.get("strict_interlock", False),
                disabled=running,
                help="Locks pause/reset during break sessions so you cannot cheat or skip ocular rest.",
            )
            st.session_state["strict_interlock"] = strict_toggle
        with regain_col2:
            if st.button("🎧 Play 432Hz Calm Alpha Tone", use_container_width=True, help="Science-backed frequency for deep focus & ocular rest"):
                trigger_audio_chime("alpha_focus")
                st.toast("Playing 432Hz alpha harmonic tone...", icon="🎵")

        if running:
            remaining = max(0, int(st.session_state["timer_deadline"] - time.monotonic()))
            duration = max(1, int(st.session_state["timer_duration"]))
            progress_val = max(0.0, min(1.0, 1 - remaining / duration))

            mins = remaining // 60
            secs = remaining % 60

            st.html(
                f"""<div class="timer-radial-card pulse-glow">
<div class="timer-mode-badge">{st.session_state['timer_kind']} INTERVAL IN PROGRESS</div>
<div class="timer-big-digits">{mins:02d}:{secs:02d}</div>
<div style="font-size: 0.88rem; color: #94A3B8; font-weight:500;">Maintain upright posture &bull; Relax ocular convergence</div>
</div>"""
            )
            st.progress(progress_val)

            if remaining <= 0:
                st.session_state["timer_running"] = False
                st.session_state["timer_complete"] = True
                st.session_state["timer_paused_remaining"] = 0
                notify_activity_completed("timer")
                if st.session_state["audio_enabled"]:
                    trigger_audio_chime("focus_complete" if st.session_state["timer_kind"] == "Focus" else "break_complete")
                st.rerun()

            if st.session_state.get("strict_interlock", False) and st.session_state["timer_kind"] == "Break":
                st.html(
                    """<div style="background:rgba(239,68,68,0.15); border:1px solid #EF4444; border-radius:8px; padding:10px 14px; margin-top:8px; text-align:center;">
<strong style="color:#FCA5A5;">🔒 Regain Strict Interlock Active:</strong> Look away at 20+ feet. Pausing is disabled until the break finishes.
</div>"""
                )
            else:
                btn_col1, btn_col2 = st.columns(2)
                if btn_col1.button("⏸️ Pause Timer", use_container_width=True):
                    st.session_state["timer_paused_remaining"] = remaining
                    st.session_state["timer_running"] = False
                    st.session_state["timer_complete"] = False
                    st.rerun()
                if btn_col2.button("⏹️ Reset Timer", use_container_width=True):
                    st.session_state["timer_running"] = False
                    st.session_state["timer_complete"] = False
                    st.session_state["timer_paused_remaining"] = 0
                    st.rerun()

        else:
            if st.session_state["timer_complete"]:
                if st.session_state["timer_kind"] == "Focus":
                    st.success("🎉 Focus interval complete! Take your planned micro-pause and rest your eyes.")
                else:
                    st.success("✨ Micro-break complete! Resume your tasks with refreshed vision.")

            if st.session_state["timer_paused_remaining"] > 0:
                rem = int(st.session_state["timer_paused_remaining"])
                st.html(
                    f"""<div class="timer-radial-card" style="border-color: rgba(245, 158, 11, 0.5);">
<div class="timer-mode-badge" style="background:rgba(245,158,11,0.2); border-color:#F59E0B; color:#FBBF24;">TIMER PAUSED</div>
<div class="timer-big-digits" style="color: #FBBF24; text-shadow:0 0 25px rgba(245,158,11,0.5);">{rem // 60:02d}:{rem % 60:02d}</div>
</div>"""
                )
                r_col1, r_col2 = st.columns(2)
                if r_col1.button("▶️ Resume Timer", type="primary", use_container_width=True):
                    now = time.monotonic()
                    st.session_state["timer_deadline"] = now + rem
                    st.session_state["timer_running"] = True
                    st.session_state["timer_complete"] = False
                    st.rerun()
                if r_col2.button("⏹️ Reset", use_container_width=True):
                    st.session_state["timer_paused_remaining"] = 0
                    st.session_state["timer_complete"] = False
                    st.rerun()
            else:
                st.html(
                    f"""<div class="timer-radial-card">
<div class="timer-mode-badge" style="background:rgba(255,255,255,0.06); border-color:rgba(255,255,255,0.15); color:#94A3B8;">STANDBY READY</div>
<div class="timer-big-digits" style="color: #64748B; text-shadow:none;">{int(focus_minutes):02d}:00</div>
<div style="font-size: 0.84rem; color: #64748B;">Select duration and launch session below</div>
</div>"""
                )
                s_col1, s_col2 = st.columns(2)
                if s_col1.button("🚀 Start Focus Work Session", type="primary", use_container_width=True):
                    _start_timer("Focus", int(focus_minutes))
                    st.rerun()
                if s_col2.button("☕ Start Micro-Break Interval", use_container_width=True):
                    _start_timer("Break", int(rest_minutes))
                    st.rerun()

    timer_panel()

    # Guided Ocular Exercises
    st.markdown("---")
    st.markdown("#### 🧘 Guided Ophthalmic Micro-Break Protocol")
    st.caption("Perform these four targeted exercises during your break intervals to restore visual homeostasis:")

    ex1, ex2, ex3, ex4 = st.columns(4)
    with ex1:
        st.html(
            """<div class="clinical-card" style="height: 100%;">
<div style="font-size: 1.8rem; margin-bottom: 8px;">🔭</div>
<div style="font-weight: 700; font-size: 1rem; color: #38BDF8;">1. 20-Foot Gaze</div>
<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 6px; line-height: 1.6;">
Look at an object at least 20 feet away. Completely disengages intraocular ciliary accommodation.
</div>
</div>"""
        )
    with ex2:
        st.html(
            """<div class="clinical-card" style="height: 100%;">
<div style="font-size: 1.8rem; margin-bottom: 8px;">💧</div>
<div style="font-weight: 700; font-size: 1rem; color: #38BDF8;">2. Conscious Blinks</div>
<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 6px; line-height: 1.6;">
Close eyelids gently for 2 seconds, then open. Repeat 5 times to express lipid oils across the cornea.
</div>
</div>"""
        )
    with ex3:
        st.html(
            """<div class="clinical-card" style="height: 100%;">
<div style="font-size: 1.8rem; margin-bottom: 8px;">🤲</div>
<div style="font-weight: 700; font-size: 1rem; color: #38BDF8;">3. Warm Palming</div>
<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 6px; line-height: 1.6;">
Rub hands together until warm, cup gently over closed eyes without pressure for 30s of thermal rest.
</div>
</div>"""
        )
    with ex4:
        st.html(
            """<div class="clinical-card" style="height: 100%;">
<div style="font-size: 1.8rem; margin-bottom: 8px;">🔄</div>
<div style="font-weight: 700; font-size: 1rem; color: #38BDF8;">4. Cervical Stretch</div>
<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 6px; line-height: 1.6;">
Roll shoulders backwards and tilt head side-to-side to relieve suboccipital tension referring to eyes.
</div>
</div>"""
        )

    # Interactive Breathing & Visual Gaze Coach
    with st.expander("🧘 Interactive 20-Second Guided Breathing & Gaze Synchronizer", expanded=True):
        st.html(
            """<div class="breathing-container">
<div style="font-weight:700; font-size:1.1rem; color:#38BDF8; margin-bottom:4px;">Synchronized Ocular Relaxation Cycle</div>
<div style="font-size:0.86rem; color:#94A3B8;">Follow the luminous breathing beacon with a soft, distant gaze (20+ feet away)</div>
<div class="breathing-circle-outer">
<div class="breathing-circle-inner"></div>
</div>
<div style="display:flex; justify-content:center; gap:20px; font-size:0.82rem; color:#CBD5E1; margin-top:8px; flex-wrap:wrap;">
<span><strong style="color:#38BDF8;">Phase 1 (4s):</strong> Inhale & Gaze Distantly</span>
<span>&bull;</span>
<span><strong style="color:#34D399;">Phase 2 (4s):</strong> Hold & Soften Brow Muscles</span>
<span>&bull;</span>
<span><strong style="color:#06B6D4;">Phase 3 (4s):</strong> Exhale & Perform Slow Full Blink</span>
</div>
</div>"""
        )
        if st.button("✨ Complete 20-Second Guided Optical Reset", type="primary", use_container_width=True):
            notify_activity_completed("timer")
            st.rerun()


def _render_eye_exercises() -> None:
    st.markdown("### 🧘 Ophthalmic Eye Relaxation Studio & Vision Gym")
    st.write(
        "Clinically structured ocular exercises designed to relieve sustained ciliary accommodative spasm, "
        "decompress the 6 extraocular motor muscles, and restore Meibomian lipid tear film homeostasis."
    )

    # Top summary metrics
    em1, em2, em3 = st.columns(3)
    with em1:
        st.html(
            """<div class="metric-tile" style="border-top-color: #38BDF8;">
<div class="metric-tile-label">Ocular Exercises</div>
<div class="metric-tile-value">5 <span style="font-size:1rem; color:#94A3B8;">Protocols</span></div>
<div class="metric-tile-sub">Clinical vision gym</div>
</div>"""
        )
    with em2:
        completed = st.session_state.get("exercises_completed_today", 0)
        st.html(
            f"""<div class="metric-tile" style="border-top-color: #10B981;">
<div class="metric-tile-label">Completed Today</div>
<div class="metric-tile-value">{completed} <span style="font-size:1rem; color:#94A3B8;">Drills</span></div>
<div class="metric-tile-sub">Ocular relief logged</div>
</div>"""
        )
    with em3:
        st.html(
            """<div class="metric-tile" style="border-top-color: #06B6D4;">
<div class="metric-tile-label">Biophysical Target</div>
<div class="metric-tile-value" style="font-size:1.4rem; padding-top:6px;">Ciliary & Tears</div>
<div class="metric-tile-sub">Accommodative de-spasm</div>
</div>"""
        )

    st.markdown("---")

    # Interactive Guided Exercise Player
    st.markdown("#### 🎯 Interactive Guided Exercise Player")
    st.caption("Select an exercise below to launch the live interactive visual coach:")

    exercise_titles = [f"{ex['icon']} {ex['title']} ({ex['duration_seconds']}s)" for ex in EYE_EXERCISES]
    selected_idx = st.selectbox(
        "Choose an Exercise Drill",
        range(len(EYE_EXERCISES)),
        format_func=lambda i: exercise_titles[i],
        index=0,
    )
    current_ex = EYE_EXERCISES[selected_idx]

    player_col1, player_col2 = st.columns([1.4, 1], gap="large")

    with player_col1:
        # Dynamic visual animation depending on selected exercise
        if current_ex["id"] == "figure_eight":
            st.html(render_figure_eight_animation())
        elif current_ex["id"] == "blink_squeeze":
            st.html(render_blink_squeeze_animation())
        elif current_ex["id"] == "near_far":
            st.html(
                """<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 24px; text-align: center; margin: 16px 0;">
<div style="font-weight: 700; font-size: 1.1rem; color: #38BDF8; margin-bottom: 6px;">
🎯 Dynamic Accommodative Switcher
</div>
<div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 20px;">
Alternate your focal distance to train ciliary muscle elasticity.
</div>
<div style="display:flex; justify-content:center; align-items:center; gap:24px; flex-wrap:wrap;">
<div style="padding:16px 20px; border-radius:12px; background:rgba(6, 182, 212, 0.15); border:1px solid #06B6D4; min-width:140px;">
<div style="font-size:2rem;">👍</div>
<div style="font-weight:700; color:#38BDF8; margin-top:4px;">NEAR FOCUS</div>
<div style="font-size:0.75rem; color:#CBD5E1;">Thumb (10 in) for 5s</div>
</div>
<div style="font-size:1.8rem; color:#64748B;">⇄</div>
<div style="padding:16px 20px; border-radius:12px; background:rgba(16, 185, 129, 0.15); border:1px solid #10B981; min-width:140px;">
<div style="font-size:2rem;">🏔️</div>
<div style="font-weight:700; color:#34D399; margin-top:4px;">DISTANT FOCUS</div>
<div style="font-size:0.75rem; color:#CBD5E1;">Horizon (20+ ft) for 5s</div>
</div>
</div>
<div style="font-size:0.8rem; color:#94A3B8; margin-top:16px;">
Perform 10 smooth alternating transitions to restore flexible accommodation.
</div>
</div>"""
            )
        elif current_ex["id"] == "palming":
            st.html(
                """<div style="background: rgba(10, 15, 29, 0.95); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 16px; padding: 28px; text-align: center; margin: 16px 0;">
<div style="font-size: 2.2rem; margin-bottom: 8px;">🤲</div>
<div style="font-weight: 700; font-size: 1.15rem; color: #FBBF24; margin-bottom: 6px;">
Thermal Darkness & Photoreceptor Therapy
</div>
<div style="font-size: 0.88rem; color: #CBD5E1; max-width: 480px; margin: 0 auto; line-height: 1.6;">
Rub hands together vigorously until warm. Cup palms gently over closed eyes without applying pressure to the globe.
Immerse your eyes in soothing darkness to allow rhodopsin photopigments to replenish.
</div>
</div>"""
            )
        elif current_ex["id"] == "orbital_compass":
            st.html(
                """<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 16px; padding: 24px; text-align: center; margin: 16px 0;">
<div style="font-weight: 700; font-size: 1.1rem; color: #A78BFA; margin-bottom: 6px;">
🧭 4-Cardinal Compass Gaze Stretch
</div>
<div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">
Hold each extreme position for 3 seconds without moving your head.
</div>
<div style="display:grid; grid-template-columns: repeat(3, 1fr); max-width:240px; margin: 0 auto; gap: 8px; text-align:center;">
<div></div>
<div style="background:rgba(255,255,255,0.06); padding:8px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); color:#38BDF8; font-weight:700;">⬆️ UP</div>
<div></div>
<div style="background:rgba(255,255,255,0.06); padding:8px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); color:#38BDF8; font-weight:700;">⬅️ LEFT</div>
<div style="background:rgba(139,92,246,0.2); padding:8px; border-radius:8px; border:1px solid #8B5CF6; color:#C4B5FD; font-weight:700;">● CENTER</div>
<div style="background:rgba(255,255,255,0.06); padding:8px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); color:#38BDF8; font-weight:700;">➡️ RIGHT</div>
<div></div>
<div style="background:rgba(255,255,255,0.06); padding:8px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); color:#38BDF8; font-weight:700;">⬇️ DOWN</div>
<div></div>
</div>
</div>"""
            )

        # Session Completion Button
        if st.button(f"✅ Mark '{current_ex['title']}' Completed", type="primary", use_container_width=True):
            st.session_state["exercises_completed_today"] = st.session_state.get("exercises_completed_today", 0) + 1
            notify_activity_completed("exercise")
            if st.session_state.get("audio_enabled", True):
                trigger_audio_chime("focus_complete")
            st.toast(f"Logged completion of {current_ex['title']}!", icon="🎉")
            st.success("🎉 Ocular relaxation completed! Extraocular muscles refreshed and tear film stimulated.")

    with player_col2:
        st.html(
            f"""<div class="clinical-card" style="border-left: 4px solid #06B6D4 !important; height:100%;">
<div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #06B6D4; letter-spacing: 0.08em;">
{current_ex['category']} &bull; {current_ex['duration_seconds']}s
</div>
<div style="font-weight: 800; font-size: 1.2rem; color: #F8FAFC; margin: 6px 0;">
{current_ex['icon']} {current_ex['title']}
</div>
<div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6; margin-bottom: 12px;">
{current_ex['summary']}
</div>
<div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.25); border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; font-size: 0.82rem; color: #38BDF8; line-height: 1.5;">
<strong>Clinical Mechanism:</strong> {current_ex['clinical_benefit']}
</div>
<div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">Protocol Steps:</div>
<ol style="padding-left: 18px; margin: 0; font-size: 0.84rem; color: #CBD5E1; line-height: 1.7;">
{"".join(f"<li>{s}</li>" for s in current_ex['steps'])}
</ol>
</div>"""
        )

    # Full Exercise Library Cards
    st.markdown("---")
    st.markdown("#### 📚 Complete Vision Gym Library")
    st.caption("Overview of all 5 clinical ocular relaxation protocols:")

    grid_cols = st.columns(len(EYE_EXERCISES))
    for idx, ex in enumerate(EYE_EXERCISES):
        with grid_cols[idx]:
            st.html(
                f"""<div class="clinical-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
<div>
<div style="font-size: 2rem; margin-bottom: 6px;">{ex['icon']}</div>
<div style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC; margin-bottom: 4px;">{ex['title']}</div>
<div style="font-size: 0.72rem; color: #38BDF8; font-weight: 600; margin-bottom: 8px;">{ex['category']}</div>
<div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.5;">{ex['summary']}</div>
</div>
<div style="margin-top: 12px; font-size: 0.75rem; color: #64748B; font-weight: 600;">
⏱️ {ex['duration_seconds']} Seconds
</div>
</div>"""
            )


def _render_care_guide() -> None:
    st.markdown("### 💡 Evidence-Based Screen-Care Guide & Clinical Guidance")
    st.write(
        "Scientific ergonomic principles, display optimization standards, and clinical referral guidelines "
        "synthesized from ophthalmic research bodies."
    )

    # Interactive Workstation Ergonomic Self-Checklist
    st.markdown("#### 📐 Interactive Workstation Ergonomic Readiness Audit")
    st.caption("Verify your physical desk configuration to compute your personalized Ergonomic Compliance Score:")
    ec1, ec2 = st.columns(2)
    with ec1:
        e1 = st.checkbox("Display positioned 20 to 28 inches (arm's length) away", value=True)
        e2 = st.checkbox("Top third of monitor positioned at or 15-20° below eye level", value=True)
        e3 = st.checkbox("Monitor perpendicular to windows to eliminate harsh glare and reflections", value=False)
    with ec2:
        e4 = st.checkbox("Screen brightness calibrated to match ambient room illumination", value=True)
        e5 = st.checkbox("Night light / warm color temperature filter active after sunset", value=True)
        e6 = st.checkbox("Text and font size scaled up so you read effortlessly without leaning forward", value=True)

    passed = sum([e1, e2, e3, e4, e5, e6])
    score_pct = int((passed / 6) * 100)
    badge_color = "#10B981" if score_pct >= 80 else ("#F59E0B" if score_pct >= 60 else "#EF4444")
    st.html(
        f"""<div class="clinical-card" style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; margin-bottom:18px; border-left: 4px solid {badge_color} !important;">
<div>
<div style="font-weight:700; font-size:1.05rem; color:#F8FAFC;">Workstation Ergonomic Readiness Score</div>
<div style="font-size:0.84rem; color:#94A3B8;">{passed} of 6 clinical ergonomic standards verified</div>
</div>
<div style="font-family:'JetBrains Mono', monospace; font-size:1.8rem; font-weight:800; color:{badge_color};">
{score_pct}%
</div>
</div>"""
    )

    # Urgent Guidance Banner
    st.html(
        """<div class="urgent-banner-glow">
<div style="font-weight: 800; font-size: 1.05rem; margin-bottom: 6px; color:#FCA5A5; display:flex; align-items:center; gap:8px;">
<span>🚨</span> Critical Ophthalmic Warning: When to Seek Immediate Care
</div>
<div style="font-size: 0.88rem; line-height: 1.6; color:#FECACA;">
Computer vision syndrome produces mild, reversible asthenopia. Seek <strong>immediate emergency medical attention</strong> if you experience:
<ul style="margin: 8px 0 0 0; padding-left: 20px;">
<li>Sudden loss, distortion, or persistent shadow across your vision</li>
<li>Severe, acute eye pain or deep ocular ache</li>
<li>Foreign body sensation or painful red eye while wearing contact lenses (risk of bacterial keratitis)</li>
<li>Sudden onset of flashes of light or numerous new floaters</li>
</ul>
</div>
</div>"""
    )

    g_col1, g_col2 = st.columns(2, gap="large")

    with g_col1:
        for section_title, tips in CARE_SECTIONS[:2]:
            st.markdown(f"#### 🖥️ {section_title}")
            for tip in tips:
                st.markdown(f"- {tip}")

    with g_col2:
        for section_title, tips in CARE_SECTIONS[2:]:
            st.markdown(f"#### 🌿 {section_title}")
            for tip in tips:
                st.markdown(f"- {tip}")

        st.markdown("#### 📖 Peer-Reviewed Sources & References")
        for label, url in CARE_SOURCES:
            st.markdown(f"- [{label}]({url})")

    st.markdown("---")
    st.markdown("#### 📥 Official AsthenoZero User Guide & Manual")
    if MANUAL_PATH.exists():
        st.download_button(
            "Download Comprehensive User Manual (PDF)",
            data=MANUAL_PATH.read_bytes(),
            file_name="eyeguard_user_manual.pdf",
            mime="application/pdf",
            type="primary",
        )
    else:
        st.caption("PDF user guide is accessible in the project output directory.")


def _render_results_and_limitations() -> None:
    st.markdown("### 🔬 Model Insights, Methodology & Scientific Boundaries")
    st.write(
        "Comprehensive documentation of the machine learning pipeline, grouped cross-validation results, "
        "and vital scientific boundaries."
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Study Cohort Size", "N = 139", help="Survey participants retained for exploratory modeling")
    m2.metric("Cross-Validation Folds", "5-Fold Grouped", help="Grouped by identical feature-target tuples")
    m3.metric("Selected Model", "L2 Ridge Regression", help="Lowest MAE and RMSE across evaluation candidates")

    st.markdown("#### 📊 Comparative Model Evaluation (Held-Out Folds)")
    results_table = pd.DataFrame(
        [
            {"Model Architecture": "Mean Dummy Baseline", "MAE (Score Points)": "2.63 ± 0.27", "RMSE (Points)": "3.18 ± 0.31", "R² Score": "-0.03 ± 0.03"},
            {"Model Architecture": "Ridge Regression (alpha=5.0)", "MAE (Score Points)": "2.40 ± 0.32", "RMSE (Points)": "2.88 ± 0.34", "R² Score": "0.15 ± 0.13"},
            {"Model Architecture": "Random Forest Regressor", "MAE (Score Points)": "2.47 ± 0.33", "RMSE (Points)": "2.96 ± 0.31", "R² Score": "0.11 ± 0.12"},
        ]
    )
    st.dataframe(results_table, use_container_width=True, hide_index=True)

    st.markdown("#### 🔎 Permutation Feature Importance Analysis")
    st.markdown(
        """
        Permutation importance measures the increase in cross-validation MAE when a feature column is randomly shuffled.
        A higher positive value indicates greater model reliance:
        """
    )
    importance_data = pd.DataFrame(
        [
            {"Feature": "Sleep Category", "Mean MAE Increase": 0.086, "Positive Folds": "3 / 5"},
            {"Feature": "Vision Correction Status", "Mean MAE Increase": 0.077, "Positive Folds": "4 / 5"},
            {"Feature": "Daily Screen Time Category", "Mean MAE Increase": 0.041, "Positive Folds": "5 / 5"},
            {"Feature": "Primary Display Device", "Mean MAE Increase": 0.032, "Positive Folds": "5 / 5"},
            {"Feature": "Age Cohort", "Mean MAE Increase": 0.018, "Positive Folds": "3 / 5"},
            {"Feature": "Breaks Per Hour Category", "Mean MAE Increase": 0.015, "Positive Folds": "3 / 5"},
        ]
    )
    st.dataframe(importance_data, use_container_width=True, hide_index=True)

    st.markdown("#### ⚠️ Essential Scientific Boundaries")
    st.markdown(
        """
        - **Exploratory Outcome Metric:** The symptom score is an unvalidated sum of five survey questions (0 to 15), not a standardized clinical ophthalmic instrument such as the Ocular Surface Disease Index (OSDI).
        - **Modest Effect Size:** The Ridge regression model improves held-out prediction by approximately 0.23 score points over a simple mean baseline on this small sample.
        - **Camera Data Separation:** Camera blink diagnostics are evaluated independently and are not currently paired into the survey model weights.
        - **Non-Causal Associations:** Correlation does not establish causation; self-reported sleep and screen times reflect associative behavioral patterns only.
        """
    )


def main() -> None:
    st.set_page_config(
        page_title="AsthenoZero | Precision Ophthalmic Suite",
        page_icon="👁️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _ensure_session_state()

    # Inject modern clinical theme CSS
    st.html(get_clinical_theme_css())

    # Render persistent clinical sidebar
    _render_sidebar()

    # Render main hero header
    _render_hero_banner()

    # Render strict rehabilitation alert / streak warning if active
    render_strict_rehab_alert()

    # Clinical navigation tabs
    tabs = st.tabs(
        [
            "📊 Clinical Risk Assessment",
            "👁️ Live Blink Diagnostic",
            "📈 Habit Diary & Analytics",
            "⏱️ 20-20-20 Smart Timer",
            "🧘 Eye Relaxation & Vision Gym",
            "💡 Care Guide & Protocols",
        ]
    )

    with tabs[0]:
        _render_survey_estimate()
    with tabs[1]:
        _render_blink_test()
    with tabs[2]:
        _render_habit_diary()
    with tabs[3]:
        _render_break_timer()
    with tabs[4]:
        _render_eye_exercises()
    with tabs[5]:
        _render_care_guide()


if __name__ == "__main__":
    main()
