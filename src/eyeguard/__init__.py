"""AsthenoZero clinical, gamification, and analytical modules."""

from eyeguard.blink_monitor import BlinkMonitor
from eyeguard.care_content import CARE_SECTIONS, CARE_SOURCES, URGENT_GUIDANCE
from eyeguard.theme import get_clinical_theme_css, render_risk_gauge_svg
from eyeguard.recommendations import analyze_risk_factors
from eyeguard.sound_alerts import trigger_audio_chime
from eyeguard.analytics import (
    calculate_diary_kpis,
    build_trend_chart,
    build_symptom_correlation_chart,
    get_cohort_comparison,
)
from eyeguard.report_generator import generate_clinical_html_report
from eyeguard.clinical_pathology import (
    get_vulnerable_conditions,
    get_ophthalmic_dietary_protocol,
    calculate_divergence_index,
    simulate_5year_ocular_projection,
)
from eyeguard.eye_exercises import (
    EYE_EXERCISES,
    render_figure_eight_animation,
    render_blink_squeeze_animation,
)
from eyeguard.gamification import (
    ensure_gamification_state,
    award_coins,
    spend_coins,
    notify_activity_completed,
    render_top_navbar_badges,
    render_gamification_sidebar,
    render_strict_rehab_alert,
    break_streak_simulation,
    repair_streak_with_coins,
    buy_shield,
)

__all__ = [
    "BlinkMonitor",
    "CARE_SECTIONS",
    "CARE_SOURCES",
    "URGENT_GUIDANCE",
    "get_clinical_theme_css",
    "render_risk_gauge_svg",
    "analyze_risk_factors",
    "trigger_audio_chime",
    "calculate_diary_kpis",
    "build_trend_chart",
    "build_symptom_correlation_chart",
    "get_cohort_comparison",
    "generate_clinical_html_report",
    "get_vulnerable_conditions",
    "get_ophthalmic_dietary_protocol",
    "calculate_divergence_index",
    "simulate_5year_ocular_projection",
    "EYE_EXERCISES",
    "render_figure_eight_animation",
    "render_blink_squeeze_animation",
    "ensure_gamification_state",
    "award_coins",
    "spend_coins",
    "notify_activity_completed",
    "render_top_navbar_badges",
    "render_gamification_sidebar",
    "render_strict_rehab_alert",
    "break_streak_simulation",
    "repair_streak_with_coins",
    "buy_shield",
]
