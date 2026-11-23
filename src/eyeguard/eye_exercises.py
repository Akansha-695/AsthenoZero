"""Interactive ophthalmic eye relaxation exercises and vision gym routines."""

from __future__ import annotations

from typing import Any


EYE_EXERCISES = [
    {
        "id": "figure_eight",
        "title": "Figure-8 Smooth Pursuit",
        "category": "Extraocular Muscle Flexibility",
        "duration_seconds": 60,
        "icon": "♾️",
        "summary": "Follow an imaginary or animated infinity loop to decompress the 6 extraocular muscles and relieve ocular motor stiffness.",
        "clinical_benefit": "Promotes smooth pursuit eye movements, relieves spasm of the rectus and oblique muscles, and reduces tension headaches caused by fixed-gaze fixation.",
        "steps": [
            "Keep your head completely still, facing straight forward.",
            "Follow the moving glowing dot with your eyes only as it traces a wide figure-8.",
            "Maintain smooth, continuous eye movement without jumping or blinking rapidly.",
            "Complete 30 seconds clockwise, then reverse direction for 30 seconds.",
        ],
    },
    {
        "id": "blink_squeeze",
        "title": "Meibomian Blink & Squeeze",
        "category": "Dry Eye & Tear Film Restoration",
        "duration_seconds": 45,
        "icon": "💧",
        "summary": "Deliberate 4-phase blinking drill that stimulates lipid secretion from the Meibomian glands.",
        "clinical_benefit": "Reduces tear evaporation and dry eye discomfort. Normalizes tear break-up time (TBUT) after prolonged display-induced blink suppression.",
        "steps": [
            "Close both eyes gently for 2 seconds (normal close).",
            "Open your eyes normally for 2 seconds.",
            "Close your eyes again and gently squeeze the eyelids together for 2 seconds (expresses protective oils).",
            "Open and relax for 2 seconds.",
            "Repeat this 4-step sequence 5 to 6 times.",
        ],
    },
    {
        "id": "near_far",
        "title": "Near-Far Accommodation Shift",
        "category": "Ciliary Muscle De-Spasm",
        "duration_seconds": 60,
        "icon": "🎯",
        "summary": "Alternating gaze shifts between near and far focal distances to break sustained accommodative spasm.",
        "clinical_benefit": "Relaxes the intraocular ciliary muscle and restores flexible accommodative amplitude, eliminating blurred distance vision after screen sessions.",
        "steps": [
            "Hold your thumb or a pen roughly 10 inches (25 cm) in front of your nose.",
            "Focus intently on the tip for 5 seconds until it is crisp and clear.",
            "Shift your gaze to an object at least 20 feet (6 meters) away or out a window for 5 seconds.",
            "Shift focus back to your thumb for 5 seconds.",
            "Alternate smoothly between near and far focal targets for 10 repetitions.",
        ],
    },
    {
        "id": "palming",
        "title": "Thermal Warm Palming",
        "category": "Photoreceptor & Optic Rest",
        "duration_seconds": 60,
        "icon": "🤲",
        "summary": "Gentle sensory darkness and soothing hand warmth over closed orbits.",
        "clinical_benefit": "Allows retinal photopigments (rhodopsin) to regenerate, dampens excessive sympathetic visual stimulation, and relaxes peri-orbital fascial tension.",
        "steps": [
            "Vigorously rub your palms together for 10-15 seconds until they feel comfortably warm.",
            "Close your eyes and cup your warm palms gently over your eye sockets.",
            "Rest the heel of your palms on your cheekbones with fingers crossed over your forehead.",
            "Do not put pressure on your eyeballs; allow total darkness inside the cups.",
            "Breathe deeply and visualize pure, comforting blackness for 45-60 seconds.",
        ],
    },
    {
        "id": "orbital_compass",
        "title": "Orbital Compass Gaze Stretch",
        "category": "Range of Motion & Neuromuscular Stretch",
        "duration_seconds": 45,
        "icon": "🧭",
        "summary": "Full range-of-motion cardinal gaze holds in four directional extremes.",
        "clinical_benefit": "Stretches underutilized gaze positions, increases peri-ocular microcirculation, and prevents postural neck strain.",
        "steps": [
            "Keep your head stationary and spine upright.",
            "Look as far UP as comfortable without moving your head; hold for 3 seconds.",
            "Look as far DOWN as comfortable; hold for 3 seconds.",
            "Look as far to the extreme LEFT; hold for 3 seconds.",
            "Look as far to the extreme RIGHT; hold for 3 seconds.",
            "Finish with two gentle circular rolls clockwise and counter-clockwise.",
        ],
    },
]


def render_figure_eight_animation() -> str:
    """Render an interactive animated glowing SVG figure-8 infinity pursuit path."""
    return """<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 24px; text-align: center; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
<div style="font-weight: 700; font-size: 1.1rem; color: #38BDF8; margin-bottom: 6px;">
♾️ Smooth Pursuit Infinity Tracker
</div>
<div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">
Keep your head stationary. Follow the glowing neon beacon smoothly with your eyes only.
</div>

<div style="display:flex; justify-content:center; align-items:center;">
<svg width="340" height="170" viewBox="0 0 340 170" style="overflow: visible;">
<defs>
<linearGradient id="infinityGrad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#06B6D4" />
<stop offset="50%" stop-color="#3B82F6" />
<stop offset="100%" stop-color="#10B981" />
</linearGradient>
<filter id="beaconGlow" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur stdDeviation="6" result="blur" />
<feMerge>
<feMergeNode in="blur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
</defs>

<!-- Track Path: Lemniscate / Infinity Curve -->
<path id="infinityPath" d="M 170 85 C 120 10, 40 10, 40 85 C 40 160, 120 160, 170 85 C 220 10, 300 10, 300 85 C 300 160, 220 160, 170 85 Z" fill="none" stroke="rgba(255, 255, 255, 0.12)" stroke-width="8" stroke-linecap="round" />
<path d="M 170 85 C 120 10, 40 10, 40 85 C 40 160, 120 160, 170 85 C 220 10, 300 10, 300 85 C 300 160, 220 160, 170 85 Z" fill="none" stroke="url(#infinityGrad)" stroke-width="3" stroke-linecap="round" opacity="0.8" />

<!-- Animated Moving Neon Eye Beacon -->
<circle r="9" fill="#38BDF8" filter="url(#beaconGlow)">
<animateMotion dur="8s" repeatCount="indefinite" path="M 170 85 C 120 10, 40 10, 40 85 C 40 160, 120 160, 170 85 C 220 10, 300 10, 300 85 C 300 160, 220 160, 170 85 Z" />
</circle>
<circle r="4" fill="#FFFFFF">
<animateMotion dur="8s" repeatCount="indefinite" path="M 170 85 C 120 10, 40 10, 40 85 C 40 160, 120 160, 170 85 C 220 10, 300 10, 300 85 C 300 160, 220 160, 170 85 Z" />
</circle>
</svg>
</div>

<div style="font-size: 0.78rem; color: #64748B; margin-top: 14px;">
Speed: 8 seconds per full cycle &bull; Smooth tracking strengthens extraocular muscle coordination
</div>
</div>"""


def render_blink_squeeze_animation() -> str:
    """Render an animated rhythm coach for the Meibomian blink squeeze exercise."""
    return """<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 16px; padding: 24px; text-align: center; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
<div style="font-weight: 700; font-size: 1.1rem; color: #34D399; margin-bottom: 6px;">
💧 Meibomian Blink & Squeeze Rhythm Coach
</div>
<div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">
Synchronize your blinking with the visual prompt below to express corneal lipid oils.
</div>

<div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap; margin: 16px 0;">
<div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px 16px; min-width:130px;">
<div style="font-size:1.6rem;">😌</div>
<div style="font-weight:700; color:#38BDF8; font-size:0.9rem; margin-top:4px;">1. Close Softly</div>
<div style="font-size:0.75rem; color:#94A3B8;">Hold 2 seconds</div>
</div>

<div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px 16px; min-width:130px;">
<div style="font-size:1.6rem;">👀</div>
<div style="font-weight:700; color:#34D399; font-size:0.9rem; margin-top:4px;">2. Open Gently</div>
<div style="font-size:0.75rem; color:#94A3B8;">Hold 2 seconds</div>
</div>

<div style="background:rgba(255,255,255,0.05); border:1px solid rgba(16, 185, 129, 0.4); border-radius:12px; padding:12px 16px; min-width:130px; box-shadow:0 0 15px rgba(16,185,129,0.2);">
<div style="font-size:1.6rem;">😣</div>
<div style="font-weight:700; color:#10B981; font-size:0.9rem; margin-top:4px;">3. Squeeze Firm</div>
<div style="font-size:0.75rem; color:#A7F3D0;">Hold 2 seconds</div>
</div>

<div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px 16px; min-width:130px;">
<div style="font-size:1.6rem;">✨</div>
<div style="font-weight:700; color:#38BDF8; font-size:0.9rem; margin-top:4px;">4. Release & Relax</div>
<div style="font-size:0.75rem; color:#94A3B8;">Hold 2 seconds</div>
</div>
</div>

<div style="font-size: 0.8rem; color: #64748B;">
Performing this 4-step cycle 5 times redistributes the lipid layer across the corneal tear film.
</div>
</div>"""
