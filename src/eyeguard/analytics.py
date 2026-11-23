"""Clinical and analytical data processing and visualizations for EyeGuard AI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import altair as alt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
COHORT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "responses_clean.csv"


def calculate_diary_kpis(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate summary KPIs and trends from user habit diary entries."""
    if not entries:
        return {
            "total_days": 0,
            "avg_screen": 0.0,
            "avg_sleep": 0.0,
            "avg_breaks": 0.0,
            "avg_symptoms": None,
            "symptom_trend": "No data",
            "health_score": 100,
        }

    df = pd.DataFrame(entries)
    total_days = len(df)
    avg_screen = float(df["screen_hours"].mean())
    avg_sleep = float(df["sleep_hours"].mean())
    avg_breaks = float(df["breaks"].mean())

    valid_scores = df["symptom_score"].dropna()
    avg_symptoms = float(valid_scores.mean()) if not valid_scores.empty else None

    # Trend direction over time if >= 3 entries with symptoms
    symptom_trend = "Stable"
    if len(valid_scores) >= 3:
        first_half = valid_scores.iloc[: len(valid_scores) // 2].mean()
        second_half = valid_scores.iloc[len(valid_scores) // 2 :].mean()
        diff = second_half - first_half
        if diff < -0.5:
            symptom_trend = "Improving (Decreasing strain)"
        elif diff > 0.5:
            symptom_trend = "Worsening (Increasing strain)"
        else:
            symptom_trend = "Stable"

    # Composite Visual Wellness Score (0-100)
    score = 100.0
    if avg_screen > 6:
        score -= min(30.0, (avg_screen - 6.0) * 6.0)
    if avg_sleep < 7:
        score -= min(25.0, (7.0 - avg_sleep) * 8.0)
    if avg_breaks < 3:
        score -= min(20.0, (3.0 - avg_breaks) * 7.0)
    if avg_symptoms is not None:
        score -= min(25.0, (avg_symptoms / 15.0) * 25.0)

    health_score = int(max(10, min(100, round(score))))

    return {
        "total_days": total_days,
        "avg_screen": round(avg_screen, 1),
        "avg_sleep": round(avg_sleep, 1),
        "avg_breaks": round(avg_breaks, 1),
        "avg_symptoms": round(avg_symptoms, 1) if avg_symptoms is not None else None,
        "symptom_trend": symptom_trend,
        "health_score": health_score,
    }


def build_trend_chart(entries: list[dict[str, Any]]) -> alt.Chart | None:
    """Build a luxury dark-theme Altair chart showing Screen Time vs. Sleep."""
    if not entries:
        return None

    df = pd.DataFrame(entries).sort_values("date").copy()
    df["date"] = pd.to_datetime(df["date"])

    melted = df.melt(
        id_vars=["date"],
        value_vars=["screen_hours", "sleep_hours"],
        var_name="Metric",
        value_name="Hours",
    )
    metric_labels = {
        "screen_hours": "Screen Exposure (hrs)",
        "sleep_hours": "Sleep Duration (hrs)",
    }
    melted["Metric"] = melted["Metric"].map(metric_labels)

    color_scale = alt.Scale(
        domain=["Screen Exposure (hrs)", "Sleep Duration (hrs)"],
        range=["#06B6D4", "#10B981"],
    )

    chart = (
        alt.Chart(melted)
        .mark_line(strokeWidth=3, point=alt.OverlayMarkDef(size=60, filled=True), interpolate="monotone")
        .encode(
            x=alt.X(
                "date:T",
                title=None,
                axis=alt.Axis(
                    format="%b %d",
                    labelAngle=-25,
                    labelColor="#94A3B8",
                    tickColor="transparent",
                    domainColor="#334155",
                    gridColor="rgba(255, 255, 255, 0.05)",
                ),
            ),
            y=alt.Y(
                "Hours:Q",
                title="Daily Hours",
                scale=alt.Scale(domain=[0, 16]),
                axis=alt.Axis(
                    labelColor="#94A3B8",
                    titleColor="#94A3B8",
                    domainColor="#334155",
                    gridColor="rgba(255, 255, 255, 0.05)",
                ),
            ),
            color=alt.Color(
                "Metric:N",
                scale=color_scale,
                legend=alt.Legend(
                    orient="top",
                    title=None,
                    labelColor="#E2E8F0",
                    labelFontSize=12,
                    labelFontWeight="bold",
                ),
            ),
            tooltip=["date:T", "Metric:N", "Hours:Q"],
        )
        .properties(
            title=alt.TitleParams(
                "Habit Trajectory: Screen Exposure vs. Restorative Sleep",
                color="#F8FAFC",
                fontSize=14,
                fontWeight=700,
            ),
            height=280,
            background="transparent",
        )
        .configure_view(stroke="transparent")
        .interactive()
    )

    return chart


def build_symptom_correlation_chart(entries: list[dict[str, Any]]) -> alt.Chart | None:
    """Scatter plot with regression trendline of screen hours vs symptom score."""
    if not entries:
        return None

    df = pd.DataFrame(entries).dropna(subset=["symptom_score"]).copy()
    if len(df) < 2:
        return None

    points = (
        alt.Chart(df)
        .mark_circle(size=110, color="#F43F5E", opacity=0.85, stroke="#FDA4AF", strokeWidth=1.5)
        .encode(
            x=alt.X(
                "screen_hours:Q",
                title="Daily Screen Exposure (Hours)",
                axis=alt.Axis(
                    labelColor="#94A3B8",
                    titleColor="#94A3B8",
                    domainColor="#334155",
                    gridColor="rgba(255, 255, 255, 0.05)",
                ),
            ),
            y=alt.Y(
                "symptom_score:Q",
                title="Symptom Discomfort Score (0-15)",
                scale=alt.Scale(domain=[0, 15]),
                axis=alt.Axis(
                    labelColor="#94A3B8",
                    titleColor="#94A3B8",
                    domainColor="#334155",
                    gridColor="rgba(255, 255, 255, 0.05)",
                ),
            ),
            tooltip=["date", "screen_hours", "sleep_hours", "breaks", "symptom_score"],
        )
    )

    trendline = points.transform_regression("screen_hours", "symptom_score").mark_line(
        color="#F43F5E", strokeDash=[5, 5], strokeWidth=2.5
    )

    chart = (
        (points + trendline)
        .properties(
            title=alt.TitleParams(
                "Correlation: Screen Time Exposure vs. Discomfort Severity",
                color="#F8FAFC",
                fontSize=13,
                fontWeight=700,
            ),
            height=250,
            background="transparent",
        )
        .configure_view(stroke="transparent")
        .interactive()
    )

    return chart


def get_cohort_comparison(screen_hours: float, sleep_hours: float) -> dict[str, str]:
    """Compare user's current habits against the 139-participant research cohort."""
    if not COHORT_DATA_PATH.exists():
        return {
            "screen_percentile": "Cohort data unavailable",
            "sleep_percentile": "Cohort data unavailable",
        }

    try:
        cohort = pd.read_csv(COHORT_DATA_PATH)
        screen_map = {
            "Less than 2 hours": 1.5,
            "2-4 hours": 3.0,
            "4-6 hours": 5.0,
            "6-8 hours": 7.0,
            "More than 8 hours": 9.5,
        }
        sleep_map = {
            "Less than 5 hours": 4.5,
            "5-6 hours": 5.5,
            "6-7 hours": 6.5,
            "7-8 hours": 7.5,
            "More than 8 hours": 8.5,
        }
        cohort_screen = cohort["screen_time_category"].map(screen_map).dropna()
        cohort_sleep = cohort["sleep_category"].map(sleep_map).dropna()

        screen_pct = int((cohort_screen < screen_hours).mean() * 100)
        sleep_pct = int((cohort_sleep < sleep_hours).mean() * 100)

        return {
            "screen_percentile": f"Higher than {screen_pct}% of surveyed cohort",
            "sleep_percentile": f"Higher than {sleep_pct}% of surveyed cohort",
        }
    except Exception:
        return {
            "screen_percentile": "Baseline comparison unavailable",
            "sleep_percentile": "Baseline comparison unavailable",
        }
