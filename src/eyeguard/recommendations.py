"""Personalized clinical recommendation engine based on user screen habits and symptom profile."""

from __future__ import annotations

from typing import Any


def analyze_risk_factors(
    age_group: str,
    screen_time: str,
    sleep: str,
    breaks: str,
    device: str,
    vision_correction: str,
    estimated_score: float,
) -> dict[str, Any]:
    """Analyze contributory risk factors and generate tailored clinical recommendations."""
    risk_drivers: list[dict[str, str]] = []
    protective_factors: list[dict[str, str]] = []
    clinical_recommendations: list[dict[str, Any]] = []

    # 1. Screen Time Analysis
    if screen_time in ["6-8 hours", "More than 8 hours"]:
        risk_drivers.append({
            "factor": "High Daily Screen Exposure",
            "impact": "High",
            "detail": f"Reporting {screen_time} increases cumulative corneal tear evaporation and prolonged ciliary muscle contraction.",
        })
        clinical_recommendations.append({
            "category": "Workstation Ergonomics",
            "priority": "High",
            "title": "Optimize Monitor Geometry & Ambient Lighting",
            "action": (
                "Position your screen 20 to 28 inches (arm's length) away with the top of the screen at or "
                "15-20 degrees below eye level. Ensure ambient lighting is balanced to prevent high contrast glare."
            ),
            "evidence": "American Academy of Ophthalmology (AAO) Computer Vision Guidelines",
        })
    elif screen_time in ["Less than 2 hours", "2-4 hours"]:
        protective_factors.append({
            "factor": "Moderate Screen Hours",
            "detail": f"{screen_time} remains within sustainable daily visual exposure limits.",
        })

    # 2. Break Frequency Analysis
    if breaks in ["0", "1-2"]:
        risk_drivers.append({
            "factor": "Insufficient Micro-Breaks",
            "impact": "High",
            "detail": f"Taking only {breaks} breaks per continuous hour starves the ciliary accommodative system of rest.",
        })
        clinical_recommendations.append({
            "category": "20-20-20 Micro-Break Protocol",
            "priority": "High",
            "title": "Strict 20-20-20 Interval Adherence",
            "action": (
                "Every 20 minutes of continuous screen viewing, gaze at an object at least 20 feet (6 meters) away "
                "for at least 20 seconds. This allows the intraocular ciliary muscles to fully relax."
            ),
            "evidence": "American Optometric Association (AOA) 20-20-20 Standard",
        })
    elif breaks in ["4-5", "5 or more"]:
        protective_factors.append({
            "factor": "Frequent Micro-Breaks",
            "detail": f"Taking {breaks} breaks per hour provides superior intermittent accommodation recovery.",
        })

    # 3. Sleep Deficit Analysis
    if sleep in ["Less than 5 hours", "5-6 hours"]:
        risk_drivers.append({
            "factor": "Sleep Deprivation / Insufficient Ocular Rest",
            "impact": "Moderate",
            "detail": f"{sleep} restricts the normal nightly corneal epithelial repair and baseline tear film regeneration.",
        })
        clinical_recommendations.append({
            "category": "Sleep & Circadian Photobiology",
            "priority": "Moderate",
            "title": "Digital Curfew & Night Blue-Light Attenuation",
            "action": (
                "Discontinue active screen use 45-60 minutes before bedtime. Enable software night-shift / warm temperature modes "
                "after sunset to avoid melatonin suppression and ocular fatigue."
            ),
            "evidence": "Circadian Rhythm and Ocular Surface Homeostasis (Review of Optometry)",
        })
    elif sleep in ["7-8 hours", "More than 8 hours"]:
        protective_factors.append({
            "factor": "Adequate Restorative Sleep",
            "detail": f"{sleep} supports tear film maintenance and retinal metabolic clearance.",
        })

    # 4. Device Type Analysis
    if device in ["Phone", "Tab"]:
        risk_drivers.append({
            "factor": "Small Aperture / Close Proximity Device",
            "impact": "Moderate",
            "detail": f"Primary usage of {device} promotes closer viewing distances (< 14 inches) and higher convergence strain.",
        })
        clinical_recommendations.append({
            "category": "Device Distance Management",
            "priority": "Moderate",
            "title": "Enforce Minimum 16-Inch Handheld Distance",
            "action": (
                "Increase system font size so you can comfortably hold mobile devices at least 16 inches away. "
                "Avoid using mobile screens while walking or in vibrating environments."
            ),
            "evidence": "Ergonomics of Handheld Electronic Displays",
        })

    # 5. Vision Correction Analysis
    if vision_correction == "Yes":
        clinical_recommendations.append({
            "category": "Optical & Refractive Verification",
            "priority": "Moderate",
            "title": "Verify Dedicated Computer Prescription",
            "action": (
                "Standard reading glasses or general-distance prescriptions often mismatch intermediate computer screen distances (24-30 in). "
                "Consult your optometrist regarding anti-reflective coated occupational lenses."
            ),
            "evidence": "Computer Vision Syndrome in Corrected Ametropia",
        })
    else:
        if estimated_score > 7.0:
            risk_drivers.append({
                "factor": "Uncorrected Visual Strain",
                "impact": "Moderate",
                "detail": "Elevated symptom frequency without corrective lenses may indicate latent uncorrected hyperopia or astigmatism.",
            })
            clinical_recommendations.append({
                "category": "Clinical Screening",
                "priority": "High",
                "title": "Comprehensive Optometric Examination",
                "action": (
                    "Schedule a formal eye examination. Even minor uncorrected refractive errors (such as 0.50D astigmatism) "
                    "cause substantial compensatory fatigue during sustained display use."
                ),
                "evidence": "Clinical Optometry Asthenopia Studies",
            })

    # Universal Ocular Surface recommendation
    clinical_recommendations.append({
        "category": "Ocular Surface & Tear Film",
        "priority": "High" if estimated_score > 6.0 else "Routine",
        "title": "Conscious Complete Blinking Technique",
        "action": (
            "During screen interaction, blink rates naturally plunge from 18/min down to 5-7/min, and up to 60% of blinks are incomplete. "
            "Periodically perform 5 deliberate, slow, full-closure blinks every 15-20 minutes to redistribute the lipid tear layer."
        ),
        "evidence": "Dry Eye Assessment and Management (TFOS DEWS II Report)",
    })

    # Risk categorization
    if estimated_score <= 4.0:
        severity = "Low Risk"
        badge_class = "status-low"
        summary_text = "Your self-reported habits reflect low risk for digital eye strain. Continue your current protective routines."
    elif estimated_score <= 8.0:
        severity = "Mild Discomfort"
        badge_class = "status-mild"
        summary_text = "Early signs of digital fatigue detected. Proactive micro-breaks and lighting adjustments will prevent progression."
    elif estimated_score <= 11.0:
        severity = "Moderate Strain"
        badge_class = "status-moderate"
        summary_text = "Notable asthenopia risk. Implementing strict 20-20-20 intervals and ergonomic adjustments is strongly advised."
    else:
        severity = "High Digital Strain"
        badge_class = "status-high"
        summary_text = "Elevated digital eye strain profile. We recommend a comprehensive professional eye exam and active workstation revision."

    return {
        "severity": severity,
        "badge_class": badge_class,
        "estimated_score": estimated_score,
        "summary_text": summary_text,
        "risk_drivers": risk_drivers,
        "protective_factors": protective_factors,
        "clinical_recommendations": clinical_recommendations,
    }
