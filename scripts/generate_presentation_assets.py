"""Generate high-resolution dark-themed scientific charts and prepare image assets for AsthenoZero presentation."""

from __future__ import annotations

import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "output" / "presentation" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

USER_UPLOADED_DIR = Path(r"C:\Users\hp\.gemini\antigravity\brain\9b46ca75-6679-40e6-8e26-7ed3443520a1\.user_uploaded")

# Style configurations: Obsidian Dark Theme
DARK_BG = "#0B1120"
CARD_BG = "#152036"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#94A3B8"
CYAN = "#38BDF8"
EMERALD = "#10B981"
CORAL = "#EF4444"
AMBER = "#F59E0B"


def setup_dark_style():
    plt.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor": CARD_BG,
        "axes.edgecolor": "#283C5F",
        "axes.labelcolor": TEXT_COLOR,
        "text.color": TEXT_COLOR,
        "xtick.color": MUTED_TEXT,
        "ytick.color": MUTED_TEXT,
        "grid.color": "#1E2D4A",
        "font.family": "sans-serif",
    })


def copy_app_screenshots():
    """Copies real user-uploaded application screenshots into assets directory."""
    print("Copying app screenshots...")
    mapping = {
        "media_1795774527769_0637d5d6.jpg": "app_eye_twin_slider.jpg",
        "media_1795676015455_61a69392.jpg": "app_conditions_and_vault.jpg",
        "media_1795412478284_eaecbdcd.png": "app_blink_diagnostic.png",
        "media_1795412279256_7a649bb5.png": "app_risk_gauge.png",
    }
    for src_name, dst_name in mapping.items():
        src_path = USER_UPLOADED_DIR / src_name
        dst_path = ASSETS_DIR / dst_name
        if src_path.exists():
            shutil.copy(str(src_path), str(dst_path))
            print(f"  Copied {src_name} -> {dst_name}")
        else:
            print(f"  Warning: {src_path} not found")


def generate_ml_benchmark_chart():
    """Generates grouped CV MAE comparison chart and feature importances."""
    print("Generating ML benchmark chart...")
    setup_dark_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=200)

    # 1. Model MAE Comparison
    models = ["Dummy Baseline", "Random Forest", "AsthenoZero L2 Ridge"]
    maes = [2.63, 2.47, 2.40]
    colors = ["#475569", "#0284C7", EMERALD]

    bars = ax1.bar(models, maes, color=colors, width=0.55, edgecolor="#38BDF8", linewidth=1.2)
    ax1.set_ylim(0, 3.2)
    ax1.set_ylabel("Cross-Validation MAE (Lower is Better)", fontsize=10, fontweight="bold", color=TEXT_COLOR)
    ax1.set_title("Grouped 5-Fold CV Model Error", fontsize=12, fontweight="bold", pad=12, color=CYAN)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.08, f"MAE {h:.2f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold", color=TEXT_COLOR)

    # 2. Permutation Feature Importance
    features = ["Screen Breaks", "Age Cohort", "Device Type", "Screen Hours", "Vision Error", "Sleep Category"]
    importances = [0.015, 0.018, 0.032, 0.041, 0.077, 0.086]

    y_pos = np.arange(len(features))
    ax2.barh(y_pos, importances, color=CYAN, height=0.55, edgecolor="#0284C7", linewidth=1.0)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(features, fontsize=9.5, fontweight="bold")
    ax2.set_xlabel("Mean MAE Loss Increase Upon Permutation", fontsize=10, fontweight="bold", color=TEXT_COLOR)
    ax2.set_title("Key Behavioral Risk Drivers", fontsize=12, fontweight="bold", pad=12, color=EMERALD)
    ax2.grid(axis="x", linestyle="--", alpha=0.5)

    for i, v in enumerate(importances):
        ax2.text(v + 0.002, i, f"+{v:.3f}", va="center", fontsize=9, fontweight="bold", color=TEXT_COLOR)

    plt.tight_layout()
    out_path = ASSETS_DIR / "ml_benchmark_chart.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path}")


def generate_eye_twin_trajectory_chart():
    """Generates 5-Year compound projection curve for Meibomian Gland Atrophy and TBUT."""
    print("Generating Eye Twin trajectory chart...")
    setup_dark_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=200)

    years = np.array([1, 2, 3, 4, 5])

    # 1. Meibomian Duct Atrophy %
    unmitigated_atrophy = [15.5, 36.2, 57.0, 68.0, 68.0]
    mitigated_atrophy = [4.3, 5.1, 5.9, 6.7, 7.5]

    ax1.plot(years, unmitigated_atrophy, marker="o", linewidth=2.8, color=CORAL, label="Unmitigated Habits")
    ax1.plot(years, mitigated_atrophy, marker="s", linewidth=2.8, color=EMERALD, label="With AsthenoZero Care")
    ax1.fill_between(years, unmitigated_atrophy, mitigated_atrophy, color=CORAL, alpha=0.15)
    ax1.set_xlabel("Horizon (Years)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Meibomian Gland Atrophy (%)", fontsize=10, fontweight="bold", color=TEXT_COLOR)
    ax1.set_title("5-Year Meibomian Gland Duct Dropout", fontsize=12, fontweight="bold", pad=12, color=CYAN)
    ax1.set_xticks(years)
    ax1.set_ylim(0, 80)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", facecolor=CARD_BG, edgecolor="#283C5F")

    # Annotate Year 3 delta
    ax1.annotate("57.0% Drop-Out\n(Permanent Loss)", xy=(3, 57.0), xytext=(2.6, 68),
                 arrowprops=dict(facecolor=CORAL, shrink=0.08, width=1.5, headwidth=6),
                 fontsize=9, fontweight="bold", color=CORAL, ha="center")
    ax1.annotate("< 5.9% Preserved", xy=(3, 5.9), xytext=(3.4, 18),
                 arrowprops=dict(facecolor=EMERALD, shrink=0.08, width=1.5, headwidth=6),
                 fontsize=9, fontweight="bold", color=EMERALD, ha="center")

    # 2. Tear Break-Up Time (TBUT)
    unmitigated_tbut = [8.3, 5.6, 2.9, 2.2, 2.2]
    mitigated_tbut = [10.8, 10.6, 10.4, 10.2, 10.0]

    ax2.plot(years, unmitigated_tbut, marker="o", linewidth=2.8, color=CORAL, label="Unmitigated TBUT")
    ax2.plot(years, mitigated_tbut, marker="s", linewidth=2.8, color=EMERALD, label="Mitigated TBUT")
    ax2.axhline(10.0, color="#38BDF8", linestyle=":", linewidth=1.5, label="Normal Physiological Baseline (10s)")
    ax2.axhline(5.0, color=AMBER, linestyle="--", linewidth=1.5, label="Severe Dry Eye Threshold (5s)")
    ax2.set_xlabel("Horizon (Years)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Tear Break-Up Time (Seconds)", fontsize=10, fontweight="bold", color=TEXT_COLOR)
    ax2.set_title("Precorneal Tear Film Stability (TBUT)", fontsize=12, fontweight="bold", pad=12, color=EMERALD)
    ax2.set_xticks(years)
    ax2.set_ylim(0, 14)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="lower left", facecolor=CARD_BG, edgecolor="#283C5F", fontsize=8.5)

    plt.tight_layout()
    out_path = ASSETS_DIR / "digital_eye_twin_trajectory.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path}")


def generate_cv_kinematics_diagram():
    """Generates EAR fiducials schematic and complete vs incomplete blink profile."""
    print("Generating CV kinematics diagram...")
    setup_dark_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=200)

    # 1. Eye Aspect Ratio Geometry Schematic
    # Draw schematic eye opening
    t = np.linspace(-np.pi, np.pi, 200)
    top_lid = 0.5 * np.cos(t / 2) ** 2
    bot_lid = -0.35 * np.cos(t / 2) ** 2

    ax1.plot(t, top_lid, color=CYAN, linewidth=3)
    ax1.plot(t, bot_lid, color=CYAN, linewidth=3)
    # Pupil circle
    circle = plt.Circle((0, 0.05), 0.22, color="#0284C7", alpha=0.6)
    iris = plt.Circle((0, 0.05), 0.10, color="#0F172A")
    ax1.add_patch(circle)
    ax1.add_patch(iris)

    # Landmarks points
    pts = [(-np.pi, 0, "p1"), (-1.0, 0.38, "p2"), (1.0, 0.38, "p3"),
           (np.pi, 0, "p4"), (1.0, -0.27, "p5"), (-1.0, -0.27, "p6")]
    for x, y, name in pts:
        ax1.plot(x, y, "o", color=EMERALD, markersize=8)
        ax1.text(x, y + (0.08 if y >= 0 else -0.12), name, color=TEXT_COLOR,
                 fontsize=10, fontweight="bold", ha="center")

    # Connect vertical heights
    ax1.plot([-1.0, -1.0], [-0.27, 0.38], "--", color=AMBER, linewidth=1.8)
    ax1.plot([1.0, 1.0], [-0.27, 0.38], "--", color=AMBER, linewidth=1.8)
    ax1.plot([-np.pi, np.pi], [0, 0], ":", color="#64748B", linewidth=1.2)

    ax1.set_xlim(-3.6, 3.6)
    ax1.set_ylim(-0.7, 0.8)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("MediaPipe 6-Fiducial EAR Formulation\nEAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)",
                  fontsize=11.5, fontweight="bold", color=CYAN, pad=10)

    # 2. Complete vs Incomplete Blink Waveforms
    timeline = np.linspace(0, 4, 400)
    # Baseline EAR = 0.32
    baseline = 0.32
    ear_wave = np.full_like(timeline, baseline)

    # Complete blink at t=1.0 (drops below 0.12)
    complete_dip = 0.25 * np.exp(-((timeline - 1.0) / 0.12) ** 2)
    # Incomplete blink at t=2.6 (only drops to 0.22)
    incomplete_dip = 0.10 * np.exp(-((timeline - 2.6) / 0.12) ** 2)

    ear_wave = ear_wave - complete_dip - incomplete_dip

    threshold = 0.23  # Calibrated closure threshold
    complete_thresh = threshold * 0.70  # 0.161

    ax2.plot(timeline, ear_wave, color="#38BDF8", linewidth=2.4, label="Measured EAR Waveform")
    ax2.axhline(threshold, color=AMBER, linestyle="--", linewidth=1.5, label=f"Closure Threshold ({threshold:.2f})")
    ax2.axhline(complete_thresh, color=EMERALD, linestyle=":", linewidth=1.8, label="Complete Blink Seal (<0.70x)")

    ax2.annotate("COMPLETE BLINK\nFull Meibomian Expression", xy=(1.0, 0.08), xytext=(1.0, 0.01),
                 arrowprops=dict(facecolor=EMERALD, shrink=0.08, width=1.5, headwidth=6),
                 fontsize=8.5, fontweight="bold", color=EMERALD, ha="center")
    ax2.annotate("INCOMPLETE BLINK\nZero Oil Pumped (Stagnation)", xy=(2.6, 0.22), xytext=(2.6, 0.12),
                 arrowprops=dict(facecolor=CORAL, shrink=0.08, width=1.5, headwidth=6),
                 fontsize=8.5, fontweight="bold", color=CORAL, ha="center")

    ax2.set_xlabel("Time (Seconds)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Eye Aspect Ratio (EAR)", fontsize=10, fontweight="bold", color=TEXT_COLOR)
    ax2.set_title("Blink Kinematics: Complete vs Incomplete Micro-Blink", fontsize=11.5, fontweight="bold", pad=12, color=EMERALD)
    ax2.set_ylim(-0.02, 0.40)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", facecolor=CARD_BG, edgecolor="#283C5F", fontsize=8)

    plt.tight_layout()
    out_path = ASSETS_DIR / "cv_ear_landmarks.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path}")


def generate_blink_suppression_chart():
    """Generates the 60-second blink suppression timeline comparison chart."""
    print("Generating blink suppression chart...")
    setup_dark_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=200)

    time_sec = np.linspace(0, 60, 61)
    # Healthy cumulative blinks: ~18 blinks per 60 sec (slope = 0.3)
    healthy_blinks = time_sec * (18.0 / 60.0)
    # Straining screen reading: ~5 blinks per 60 sec (slope = 0.083)
    screen_blinks = time_sec * (5.0 / 60.0)

    ax.plot(time_sec, healthy_blinks, color=EMERALD, linewidth=2.8, label="Healthy Resting Baseline (18 blinks/min)")
    ax.plot(time_sec, screen_blinks, color=CORAL, linewidth=2.8, label="Screen Reading / Coding (5 blinks/min)")
    ax.fill_between(time_sec, healthy_blinks, screen_blinks, color=CORAL, alpha=0.18, label="72% Blink Deficit Zone")

    # TBUT rupture point
    ax.axvline(5, color=AMBER, linestyle="--", linewidth=1.5)
    ax.text(6, 14, "TBUT Tear Rupture (<5s)\nCorneal Desiccation Begins", color=AMBER, fontsize=8.5, fontweight="bold")

    ax.set_xlabel("Observation Time (Seconds)", fontsize=10, fontweight="bold")
    ax.set_ylabel("Cumulative Blink Count", fontsize=10, fontweight="bold", color=TEXT_COLOR)
    ax.set_title("The 60-Second Cognitive Blink Suppression Arc", fontsize=11.5, fontweight="bold", pad=12, color=CYAN)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 20)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", facecolor=CARD_BG, edgecolor="#283C5F", fontsize=8.5)

    plt.tight_layout()
    out_path = ASSETS_DIR / "blink_suppression_chart.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path}")


if __name__ == "__main__":
    copy_app_screenshots()
    generate_ml_benchmark_chart()
    generate_eye_twin_trajectory_chart()
    generate_cv_kinematics_diagram()
    generate_blink_suppression_chart()
    print("All presentation visual assets generated successfully!")
