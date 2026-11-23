"""Premium Health-Tech & Clinical Styling System for AsthenoZero."""

from __future__ import annotations


def get_clinical_theme_css() -> str:
    """Return an ultra-modern, luxury health-tech dark/light CSS theme for Streamlit."""
    return """<style>
/* =====================================================================
   AsthenoZero Ultra-Modern Health-Tech Design System
   Aesthetic: Premium Clinical SaaS (Deep Obsidian, Cyber Cyan, Emerald Glow)
   ===================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

/* Global Font & Smoothness */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    letter-spacing: -0.01em;
}

/* Base App Atmosphere */
.stApp {
    background: radial-gradient(circle at 15% 10%, rgba(6, 182, 212, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 85% 20%, rgba(99, 102, 241, 0.07) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 60%),
                #090D16 !important;
    color: #F1F5F9 !important;
}

/* Sidebar Atmosphere */
section[data-testid="stSidebar"] {
    background: rgba(11, 17, 30, 0.95) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Streamlit Top Header Bar */
header[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: blur(10px) !important;
}

/* Container Spacing (clears top header bar for full visibility) */
.block-container {
    padding-top: 5rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1320px !important;
}

/* Top Navigation / Brand Banner */
.premium-navbar {
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-top: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 24px;
    box-shadow: 0 12px 36px -4px rgba(0, 0, 0, 0.5), 0 0 20px rgba(6, 182, 212, 0.08);
    backdrop-filter: blur(16px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}
.brand-identity {
    display: flex;
    align-items: center;
    gap: 16px;
}
.brand-logo-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #0284C7 0%, #06B6D4 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.brand-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.brand-title span.pro-pill {
    font-size: 0.68rem;
    font-weight: 800;
    background: linear-gradient(135deg, #06B6D4, #3B82F6);
    color: #FFFFFF;
    padding: 3px 8px;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.brand-tagline {
    font-size: 0.88rem;
    color: #94A3B8;
    margin-top: 4px;
    font-weight: 400;
}
.telemetry-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.telemetry-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #CBD5E1;
    letter-spacing: 0.02em;
}
.telemetry-pill.active-cyan {
    background: rgba(6, 182, 212, 0.12);
    border-color: rgba(6, 182, 212, 0.35);
    color: #38BDF8;
}
.telemetry-pill.active-emerald {
    background: rgba(16, 185, 129, 0.12);
    border-color: rgba(16, 185, 129, 0.35);
    color: #34D399;
}

/* Glassmorphic Cards */
.clinical-card {
    background: rgba(17, 24, 39, 0.72) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 8px 24px -2px rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(14px) !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease !important;
}
.clinical-card:hover {
    border-color: rgba(6, 182, 212, 0.3) !important;
    box-shadow: 0 12px 32px -4px rgba(0, 0, 0, 0.45), 0 0 16px rgba(6, 182, 212, 0.12) !important;
    transform: translateY(-2px);
}

/* Luxury Metric Cards */
.metric-tile {
    background: rgba(17, 24, 39, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-top: 2px solid #06B6D4;
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
.metric-tile-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-bottom: 6px;
}
.metric-tile-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 800;
    color: #F8FAFC;
    line-height: 1.1;
}
.metric-tile-sub {
    font-size: 0.75rem;
    color: #64748B;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Tabs Redesign */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.8) !important;
    padding: 6px 8px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    gap: 6px !important;
    margin-bottom: 24px !important;
}
.stTabs [data-baseweb="tab"] {
    height: 42px !important;
    border-radius: 8px !important;
    color: #94A3B8 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #F8FAFC !important;
    background: rgba(255, 255, 255, 0.05) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284C7 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(6, 182, 212, 0.35) !important;
}

/* Streamlit Buttons Overhaul */
div.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 10px 22px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background: rgba(255, 255, 255, 0.06) !important;
    color: #F1F5F9 !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}
div.stButton > button:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0284C7 0%, #06B6D4 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 18px rgba(6, 182, 212, 0.4) !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0369A1 0%, #0891B2 100%) !important;
    box-shadow: 0 6px 24px rgba(6, 182, 212, 0.6) !important;
    transform: translateY(-2px) !important;
}

/* Streamlit Inputs & Selectboxes Styling */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-baseweb="select"]:hover > div,
div[data-baseweb="input"]:hover > div {
    border-color: rgba(6, 182, 212, 0.5) !important;
}
div[data-baseweb="select"] [aria-selected="true"] {
    color: #F8FAFC !important;
}

/* Timer Display Card */
.timer-radial-card {
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(9, 13, 22, 0.95));
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 24px;
    padding: 36px 24px;
    text-align: center;
    color: #F8FAFC;
    margin: 20px 0;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(6, 182, 212, 0.15);
    position: relative;
    overflow: hidden;
}
.timer-radial-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(6, 182, 212, 0.08) 0%, transparent 60%);
    pointer-events: none;
}
.timer-big-digits {
    font-family: 'JetBrains Mono', monospace;
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: #38BDF8;
    text-shadow: 0 0 30px rgba(56, 189, 248, 0.5);
    line-height: 1;
    margin: 12px 0;
}
.timer-mode-badge {
    display: inline-block;
    padding: 4px 14px;
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(6, 182, 212, 0.4);
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #22D3EE;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Pulsing Animation */
.pulse-glow {
    animation: neon-pulse 2.2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes neon-pulse {
    0%, 100% {
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 25px rgba(6, 182, 212, 0.15);
    }
    50% {
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 45px rgba(6, 182, 212, 0.35);
    }
}

/* Reading Passage Modern Card */
.reading-passage-luxury {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-left: 4px solid #06B6D4;
    border-radius: 12px;
    padding: 22px 28px;
    font-size: 1.08rem;
    line-height: 1.8;
    color: #E2E8F0;
    margin: 16px 0;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Status Badges */
.status-pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-low {
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.4);
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.2);
}
.badge-mild {
    background: rgba(6, 182, 212, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(6, 182, 212, 0.4);
    box-shadow: 0 0 12px rgba(6, 182, 212, 0.2);
}
.badge-moderate {
    background: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.4);
    box-shadow: 0 0 12px rgba(245, 158, 11, 0.2);
}
.badge-high {
    background: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
    box-shadow: 0 0 12px rgba(239, 68, 68, 0.2);
}

/* Urgent Alert Box */
.urgent-banner-glow {
    background: linear-gradient(135deg, rgba(69, 10, 10, 0.8) 0%, rgba(30, 10, 10, 0.9) 100%);
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-left: 5px solid #EF4444;
    border-radius: 12px;
    padding: 18px 24px;
    color: #FECACA;
    margin: 18px 0;
    box-shadow: 0 8px 25px rgba(239, 68, 68, 0.15);
}

/* Guided Breathing Relaxation Circle */
.breathing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    margin: 16px 0;
    text-align: center;
}
.breathing-circle-outer {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, rgba(6, 182, 212, 0.05) 70%, transparent 100%);
    border: 2px solid rgba(6, 182, 212, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: breathing-cycle 12s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    box-shadow: 0 0 30px rgba(6, 182, 212, 0.25);
    margin: 16px auto;
}
.breathing-circle-inner {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284C7, #06B6D4);
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
}
@keyframes breathing-cycle {
    0%, 100% {
        transform: scale(0.85);
        border-color: rgba(6, 182, 212, 0.3);
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
    }
    35%, 65% {
        transform: scale(1.2);
        border-color: rgba(16, 185, 129, 0.7);
        box-shadow: 0 0 45px rgba(16, 185, 129, 0.4);
    }
}

/* Scrollbar polish */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: #090D16;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #06B6D4;
}
</style>"""


def render_risk_gauge_svg(score: float, max_score: float = 15.0) -> str:
    """Render a luxury health-tech vector dial gauge."""
    clamped_score = max(0.0, min(max_score, float(score)))
    percentage = clamped_score / max_score

    # Determine risk category & colors
    if clamped_score <= 4.0:
        category = "LOW RISK"
        badge_cls = "badge-low"
        accent_color = "#10B981"
        glow_color = "rgba(16, 185, 129, 0.4)"
        desc = "Optimal Visual Comfort & Minimal Asthenopia"
    elif clamped_score <= 8.0:
        category = "MILD DISCOMFORT"
        badge_cls = "badge-mild"
        accent_color = "#06B6D4"
        glow_color = "rgba(6, 182, 212, 0.4)"
        desc = "Subclinical Strain; Regular Micro-Pauses Advised"
    elif clamped_score <= 11.0:
        category = "MODERATE STRAIN"
        badge_cls = "badge-moderate"
        accent_color = "#F59E0B"
        glow_color = "rgba(245, 158, 11, 0.4)"
        desc = "Noticeable Asthenopia; Ergonomic Workstation Revision"
    else:
        category = "HIGH DIGITAL STRAIN"
        badge_cls = "badge-high"
        accent_color = "#EF4444"
        glow_color = "rgba(239, 68, 68, 0.4)"
        desc = "Frequent Symptoms; Optometric Examination Advised"

    # Needle Angle (-90 to +90 degrees)
    needle_angle = -90 + (percentage * 180)

    # Completely flush-left SVG string without any 4-space indentation
    return f"""<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 14px 0;">
<div style="position:relative; width:300px; height:165px;">
<svg width="300" height="165" viewBox="0 0 300 165" style="overflow:visible; display:block;">
<defs>
<linearGradient id="neonArcGradient" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#10B981" />
<stop offset="28%" stop-color="#06B6D4" />
<stop offset="68%" stop-color="#F59E0B" />
<stop offset="100%" stop-color="#EF4444" />
</linearGradient>
<filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
<feGaussianBlur stdDeviation="5" result="blur" />
<feMerge>
<feMergeNode in="blur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
<filter id="needleGlow" x="-20%" y="-20%" width="140%" height="140%">
<feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="{glow_color}"/>
</filter>
</defs>
<!-- Track Base Rim -->
<path d="M 28 140 A 122 122 0 0 1 272 140" fill="none" stroke="rgba(255, 255, 255, 0.08)" stroke-width="22" stroke-linecap="round" />
<!-- Inner Dark Track -->
<path d="M 28 140 A 122 122 0 0 1 272 140" fill="none" stroke="#111827" stroke-width="16" stroke-linecap="round" />
<!-- Vibrant Gradient Arc with Glow -->
<path d="M 28 140 A 122 122 0 0 1 272 140" fill="none" stroke="url(#neonArcGradient)" stroke-width="14" stroke-linecap="round" filter="url(#neonGlow)" opacity="0.9" />
<!-- Dial Tick Marks -->
<circle cx="28" cy="140" r="2.5" fill="#64748B" />
<circle cx="64" cy="74" r="2.5" fill="#64748B" />
<circle cx="150" cy="18" r="3" fill="#64748B" />
<circle cx="236" cy="74" r="2.5" fill="#64748B" />
<circle cx="272" cy="140" r="2.5" fill="#64748B" />
<!-- Scale Labels -->
<text x="28" y="160" font-size="11" fill="#64748B" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">0</text>
<text x="64" y="65" font-size="10" fill="#64748B" font-family="'JetBrains Mono', monospace" text-anchor="middle">4</text>
<text x="150" y="36" font-size="11" fill="#94A3B8" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">8</text>
<text x="236" y="65" font-size="10" fill="#64748B" font-family="'JetBrains Mono', monospace" text-anchor="middle">11</text>
<text x="272" y="160" font-size="11" fill="#64748B" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">15</text>
<!-- Center Pivot Hub (Metallic Rim + Luminous Core) -->
<circle cx="150" cy="140" r="14" fill="#0B132B" stroke="rgba(255, 255, 255, 0.2)" stroke-width="2" />
<circle cx="150" cy="140" r="6" fill="{accent_color}" />
<!-- Needle -->
<g transform="rotate({needle_angle}, 150, 140)" filter="url(#needleGlow)">
<polygon points="147.5,140 152.5,140 150.8,24 149.2,24" fill="#F8FAFC" />
<circle cx="150" cy="24" r="4.5" fill="{accent_color}" />
</g>
</svg>
</div>
<div style="text-align:center; margin-top: -6px;">
<div style="font-size: 2.5rem; font-weight: 800; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; line-height: 1; text-shadow: 0 0 20px {glow_color};">
{clamped_score:.1f} <span style="font-size: 1.15rem; color: #64748B; font-weight: 500;">/ 15</span>
</div>
<div style="margin-top: 8px;">
<span class="status-pill-badge {badge_cls}">
● {category}
</span>
</div>
<div style="font-size: 0.84rem; color: #94A3B8; margin-top: 8px; font-weight: 500;">
{desc}
</div>
</div>
</div>"""
