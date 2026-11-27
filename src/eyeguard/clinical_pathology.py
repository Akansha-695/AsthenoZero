"""AsthenoZero - Ocular Disease Vulnerability & Nutritional Ophthalmology Protocol.

Evaluates user ergonomic telemetry to identify specific ocular surface and refractive
vulnerabilities (e.g., MGD, Accommodative Spasm, Keratitis) and provides evidence-based
ophthalmic dietary protocols (Omega-3, Lutein/Zeaxanthin, Hydration).
"""

from __future__ import annotations

from typing import Any


def get_vulnerable_conditions(habit_dict: dict[str, Any], score: float) -> list[dict[str, Any]]:
    """Evaluates ergonomic inputs to identify specific ocular conditions the user is vulnerable to."""
    screen_time = str(habit_dict.get("screen_time_category", ""))
    sleep = str(habit_dict.get("sleep_category", ""))
    breaks = str(habit_dict.get("breaks_per_hour_category", ""))
    device = str(habit_dict.get("primary_device", ""))
    vision_corr = str(habit_dict.get("vision_correction", ""))

    conditions: list[dict[str, Any]] = []

    # 1. Meibomian Gland Dysfunction (MGD) & Evaporative Dry Eye
    if screen_time in ["6-8 hours", "More than 8 hours"] or breaks in ["0", "1-2"] or score >= 6.5:
        severity = "High Vulnerability" if screen_time == "More than 8 hours" or score >= 9.0 else "Moderate Vulnerability"
        conditions.append({
            "name": "Meibomian Gland Dysfunction (MGD) & Evaporative Dry Eye",
            "icon": "💧",
            "severity": severity,
            "badge_color": "#EF4444" if severity == "High Vulnerability" else "#F59E0B",
            "risk_pct": 88 if severity == "High Vulnerability" else 65,
            "short_summary": "Blink suppression thickens eyelid oils, accelerating evaporative tear film collapse.",
            "visual_tags": ["Rapid Tear Loss", "Oil Gland Plugging", "TBUT < 5s"],
            "rx_short": "4-Phase Squeeze Drills + 40°C Warm Compress (5 min)",
            "etiology": (
                "Sustained screen stare suppresses the involuntary blink reflex by 50% to 70%. "
                "This blink inhibition causes meibum lipid secretions to thicken and stagnate within the tarsal glands, "
                "leading to rapid tear break-up time (TBUT < 5s) and chronic corneal desiccation."
            ),
            "hallmark_symptoms": [
                "Gritty, sandy sensation under the eyelids",
                "Episodic reflex tearing in air-conditioned rooms",
                "Fluctuating visual clarity that briefly sharpens upon hard blinking",
            ],
            "prevention": "Perform 4-phase Meibomian blink squeeze exercises daily and apply warm compress (40°C) for 5 minutes.",
        })

    # 2. Accommodative Ciliary Spasm (Screen-Induced Pseudomyopia)
    if breaks in ["0", "1-2"] or screen_time in ["6-8 hours", "More than 8 hours"] or device in ["Phone", "Tab"]:
        severity = "High Vulnerability" if breaks == "0" or score >= 8.0 else "Moderate Vulnerability"
        conditions.append({
            "name": "Accommodative Ciliary Spasm (Screen-Induced Pseudomyopia)",
            "icon": "🎯",
            "severity": severity,
            "badge_color": "#EF4444" if severity == "High Vulnerability" else "#F59E0B",
            "risk_pct": 85 if severity == "High Vulnerability" else 60,
            "short_summary": "Continuous near-point focus locks the intraocular focusing muscle in tonic spasm.",
            "visual_tags": ["Ciliary Muscle Lock", "Distance Refocus Lag", "Brow Tension"],
            "rx_short": "20-20-20 Rule (Look 20+ ft away to relax zonular fibers)",
            "etiology": (
                "Continuous near-point focal fixation locks the intraocular ciliary sphincter in continuous tonic contraction. "
                "Upon shifting gaze to distance objects, the zonular fibers cannot promptly relax, resulting in temporary distant blur "
                "and radiating frontal brow aches."
            ),
            "hallmark_symptoms": [
                "Temporary distance blur after looking up from laptop or phone",
                "Tension headaches focused around the eyebrow ridges and temples",
                "Sluggish optical refocusing when switching between notebook and monitor",
            ],
            "prevention": "Strictly enforce the 20-20-20 rule; look at least 20 feet away to completely disengage ciliary accommodation.",
        })

    # 3. Contact Lens-Related Micro-Friction Keratitis
    if vision_corr == "Yes" and (screen_time in ["4-6 hours", "6-8 hours", "More than 8 hours"] or score >= 7.0):
        conditions.append({
            "name": "Contact Lens-Induced Desiccation & Micro-Friction Keratitis",
            "icon": "🔍",
            "severity": "Elevated Vulnerability",
            "badge_color": "#F59E0B",
            "risk_pct": 60,
            "short_summary": "Dehydrated contact lenses draw water from the cornea, creating microscopic epithelial friction.",
            "visual_tags": ["Lens Dehydration", "Epithelial Friction", "End-of-Day Redness"],
            "rx_short": "Preservative-free rewetting drops every 90m + computer glasses",
            "etiology": (
                "Under reduced digital blink rates, hydrophilic contact lenses draw moisture away from the pre-corneal tear film. "
                "The dehydrated lens edge creates mechanical shear friction against the delicate corneal epithelium."
            ),
            "hallmark_symptoms": [
                "Premature lens intolerance (eyes feeling tired or burning after 4 hours)",
                "Circumcorneal conjunctival redness after screen sessions",
                "Difficulty removing dry contact lenses at night",
            ],
            "prevention": "Instill preservative-free rewetting drops every 90 minutes or alternate with dedicated anti-reflective glasses.",
        })

    # 4. Circadian Melatonin Suppression & Nocturnal Asthenopia
    if sleep in ["Less than 5 hours", "5-6 hours"] or (score >= 6.0 and screen_time in ["6-8 hours", "More than 8 hours"]):
        conditions.append({
            "name": "Circadian Phototoxicity & Melatonin-Suppressed Ocular Fatigue",
            "icon": "🌙",
            "severity": "Elevated Vulnerability",
            "badge_color": "#8B5CF6",
            "risk_pct": 62,
            "short_summary": "Late-night screen blue light blocks melatonin, disrupting cellular eye recovery during sleep.",
            "visual_tags": ["Melatonin Blocked", "Truncated Mitosis", "Morning Eye Heaviness"],
            "rx_short": "Strict 60-min digital curfew before bed + 7-8h restorative sleep",
            "etiology": (
                "High-energy visible (HEV) blue wavelength exposure (450–480 nm) prior to sleep suppresses pineal melatonin secretion. "
                "Insufficient deep sleep truncates the nocturnal metabolic clearance of corneal waste products and impairs lacrimal gland renewal."
            ),
            "hallmark_symptoms": [
                "Heavy, strained eyelids upon waking in the morning",
                "Photophobia (abnormal light sensitivity) under indoor fluorescent bulbs",
                "Chronic ocular surface redness and slow daytime visual recovery",
            ],
            "prevention": "Enforce a strict 60-minute digital curfew before sleep and maintain 7–8 hours of uninterrupted rest.",
        })

    # 5. Handheld Convergence Insufficiency & Extraocular Rectus Strain
    if device in ["Phone", "Tab"]:
        conditions.append({
            "name": "Binocular Convergence Insufficiency & Handheld Oculomotor Strain",
            "icon": "📱",
            "severity": "Moderate Vulnerability",
            "badge_color": "#06B6D4",
            "risk_pct": 55,
            "short_summary": "Holding phones too close (<14 in) forces inward eye convergence and neck strain.",
            "visual_tags": ["Extreme Convergence", "Close-Range <14 in", "Medial Rectus Strain"],
            "rx_short": "Enforce 16+ inch viewing distance + Figure-8 smooth pursuit drills",
            "etiology": (
                "Handheld mobile displays are held at an average distance of 10–14 inches (substantially closer than monitors), "
                "demanding severe downward gaze angulation and continuous medial rectus muscle convergence."
            ),
            "hallmark_symptoms": [
                "Double vision (diplopia) during prolonged mobile reading",
                "Words appearing to vibrate or swim after 30 minutes of phone focus",
                "Suboccipital neck and shoulder tension radiating to the back of the eyes",
            ],
            "prevention": "Maintain a minimum viewing distance of 16 inches and practice Figure-8 smooth pursuit tracking exercises.",
        })

    # If remarkably healthy profile
    if not conditions:
        conditions.append({
            "name": "Physiological Homeostasis (Low Pathological Risk)",
            "icon": "🛡️",
            "severity": "Low Risk",
            "badge_color": "#10B981",
            "risk_pct": 15,
            "short_summary": "Your screen habits and regular breaks keep your tear film and focusing muscles in healthy balance.",
            "visual_tags": ["Tear Film Intact", "Relaxed Ciliary Focus", "Low Stress"],
            "rx_short": "Maintain routine 20-20-20 preventative micro-breaks",
            "etiology": (
                "Your screen habits, regular micro-breaks, and sleep duration currently provide adequate recuperation time. "
                "Ocular surface tear film dynamics and ciliary accommodative tone remain in healthy equilibrium."
            ),
            "hallmark_symptoms": [
                "Crisp visual acuity maintained throughout the workday",
                "Comfortable blink rhythm without dry or gritty sensation",
            ],
            "prevention": "Maintain your balanced workstation ergonomics and continue routine preventative micro-breaks.",
        })

    return conditions


def get_ophthalmic_dietary_protocol(habit_dict: dict[str, Any], score: float) -> list[dict[str, Any]]:
    """Returns targeted clinical nutrition and dietary prescriptions for ocular health."""
    screen_time = str(habit_dict.get("screen_time_category", ""))
    sleep = str(habit_dict.get("sleep_category", ""))

    diet_items: list[dict[str, Any]] = [
        {
            "nutrient": "Omega-3 Fatty Acids (EPA & DHA)",
            "icon": "🐟",
            "dosage": "1,000 – 1,200 mg / day",
            "benefit": "Unclogs eyelid oil glands & prevents dry burning",
            "benefit_icon": "💧",
            "food_chips": ["🐟 Wild Salmon", "🐟 Sardines", "🌱 Chia Seeds", "🥑 Flaxseed Oil", "🥜 Walnuts"],
            "food_sources": "Wild salmon, sardines, mackerel, chia seeds, flaxseed oil, walnuts, algae oil",
            "clinical_mechanism": (
                "Directly incorporates into Meibomian gland lipids, lowering the melting point of meibum "
                "so it flows smoothly across the ocular surface. Confirmed by the TFOS DEWS II international dry eye workshop."
            ),
            "priority": "High Priority" if screen_time in ["6-8 hours", "More than 8 hours"] or score >= 6.0 else "Core Habit",
        },
        {
            "nutrient": "Macular Carotenoids (Lutein & Zeaxanthin)",
            "icon": "🥬",
            "dosage": "10 mg Lutein + 2 mg Zeaxanthin daily",
            "benefit": "Internal biological sunglasses — filters 90% of toxic screen blue light",
            "benefit_icon": "🛡️",
            "food_chips": ["🥬 Steamed Spinach", "🥬 Curly Kale", "🥚 Pasture Egg Yolks", "🫑 Bell Peppers", "🥜 Pistachios"],
            "food_sources": "Steamed spinach, curly kale, Swiss chard, pasture-raised egg yolks, orange bell peppers, pistachios",
            "clinical_mechanism": (
                "Deposits directly into the macular fovea, acting as 'internal biological sunglasses' that absorb high-energy "
                "short-wavelength blue light (440–460 nm) and neutralize photo-oxidative free radicals."
            ),
            "priority": "High Priority",
        },
        {
            "nutrient": "Bioflavonoids & Anthocyanins (Micro-Vascular Flow)",
            "icon": "🫐",
            "dosage": "1 cup daily (or 160 mg standardized extract)",
            "benefit": "Relaxes eye focusing muscles & boosts micro-circulation",
            "benefit_icon": "⚡",
            "food_chips": ["🫐 Wild Blueberries", "🍒 Dark Cherries", "🫐 Bilberries", "🍇 Blackcurrants"],
            "food_sources": "Wild blueberries, bilberries, blackcurrants, aronia berries, dark cherries",
            "clinical_mechanism": (
                "Stimulates micro-capillary blood perfusion to the intraocular ciliary muscle and extraocular recti, "
                "hastening recovery from near-work accommodative spasm and reducing visual fatigue."
            ),
            "priority": "Recommended",
        },
        {
            "nutrient": "Vitamin A & Preformed Beta-Carotene",
            "icon": "🥕",
            "dosage": "700 – 900 mcg RAE daily",
            "benefit": "Repairs corneal protective mucin layer & stops friction",
            "benefit_icon": "✨",
            "food_chips": ["🥕 Carrots", "🍠 Sweet Potatoes", "🎃 Pumpkin", "🍑 Dried Apricots"],
            "food_sources": "Carrots, roasted sweet potatoes, butternut squash, cantaloupe, dried apricots",
            "clinical_mechanism": (
                "Crucial for the differentiation of conjunctival goblet cells that secrete the hydrophilic mucin layer—the "
                "fundamental anchoring layer that binds tear film to the hydrophobic corneal surface."
            ),
            "priority": "Recommended",
        },
        {
            "nutrient": "Systemic Osmotic Hydration Protocol",
            "icon": "💧",
            "dosage": "2.5 – 3.0 Liters water + balanced electrolytes",
            "benefit": "Prevents tear film hyperosmolarity, saltiness & stinging",
            "benefit_icon": "🌊",
            "food_chips": ["💧 Mineral Water", "🥥 Coconut Water", "🍋 Lemon Infused Water", "🥒 Cucumber"],
            "food_sources": "Mineral water, coconut water, water infused with lemon & pinch of Himalayan salt, cucumber",
            "clinical_mechanism": (
                "The lacrimal glands produce the aqueous tear layer directly from systemic circulating blood volume. "
                "Sub-clinical dehydration of just 1.5% causes hyperosmolar tear film, precipitating ocular surface burning."
            ),
            "priority": "High Priority" if screen_time in ["6-8 hours", "More than 8 hours"] else "Core Habit",
        },
    ]

    # Additional targeted nutrient for low sleep
    if sleep in ["Less than 5 hours", "5-6 hours"]:
        diet_items.append({
            "nutrient": "Magnesium Glycinate & Tart Cherry (Nocturnal Repair)",
            "icon": "🍒",
            "dosage": "200 – 300 mg Magnesium at night",
            "benefit": "Overnight muscle relaxation & cellular corneal healing",
            "benefit_icon": "💤",
            "food_chips": ["🍒 Tart Cherry Juice", "🎃 Pumpkin Seeds", "🍫 Dark Chocolate (>85%)", "🥜 Almonds"],
            "food_sources": "Tart cherry juice, pumpkin seeds, dark chocolate (>85%), almonds",
            "clinical_mechanism": (
                "Naturally promotes endogenous melatonin release and relaxes hyper-contracted extraocular muscles, "
                "enabling restorative overnight ocular surface epithelial mitotic repair."
            ),
            "priority": "Targeted Sleep Support",
        })

    return diet_items


def calculate_divergence_index(
    survey_score: float,
    blink_rate: float | None = None,
    pump_efficiency: float | None = None,
) -> dict[str, Any]:
    """Calculates the Subjective-Objective Asthenopia Divergence Index (SO-DI).

    Identifies 'Silent Asthenopia' where users perceive low discomfort but exhibit
    severe physiological blink suppression or high incomplete blink rates.
    """
    if blink_rate is None:
        return {
            "has_camera_data": False,
            "quadrant": "Survey Only (Webcam Unpaired)",
            "divergence_score": 0.0,
            "silent_risk": False,
            "badge_color": "#64748B",
            "interpretation": "Run the 60-second webcam diagnostic to cross-validate perceived symptoms against objective blink kinematics.",
        }

    # Normalize survey score (0-15) to 0-100% scale
    subj_stress_pct = (min(15.0, max(0.0, survey_score)) / 15.0) * 100.0

    # Normalize blink suppression (18 blinks/min is 0% suppression; 4 blinks/min is 100% suppression)
    obj_suppression_pct = max(0.0, min(100.0, (18.0 - blink_rate) / 14.0 * 100.0))

    # Incorporate incomplete blink penalty if available
    if pump_efficiency is not None:
        incomplete_penalty = (100.0 - pump_efficiency) * 0.4
        obj_suppression_pct = min(100.0, obj_suppression_pct + incomplete_penalty)

    # Divergence delta = Objective suppression - Subjective report
    delta = obj_suppression_pct - subj_stress_pct

    # Quadrant Classification
    if subj_stress_pct <= 30.0 and obj_suppression_pct >= 60.0:
        quadrant = "Silent Asthenopia (High Asymptomatic Risk)"
        badge_color = "#EF4444"
        silent_risk = True
        interp = (
            "Critical Discrepancy: You report feeling comfortable, but your objective webcam blink rate "
            f"({blink_rate:.1f}/min) indicates acute 70%+ blink suppression. Your corneal sensory nerves may be "
            "experiencing desensitization from chronic tear evaporation. High risk of unperceived Meibomian gland stagnation."
        )
    elif subj_stress_pct >= 55.0 and obj_suppression_pct >= 55.0:
        quadrant = "Concordant High Asthenopia"
        badge_color = "#EF4444"
        silent_risk = False
        interp = (
            f"Acute Alignment: Severe subjective discomfort matches severe objective blink suppression ({blink_rate:.1f}/min). "
            "Both extraocular muscles and tear film are experiencing active desiccating stress. Immediate micro-break advised."
        )
    elif subj_stress_pct <= 35.0 and obj_suppression_pct <= 35.0:
        quadrant = "Concordant Ocular Homeostasis"
        badge_color = "#10B981"
        silent_risk = False
        interp = (
            f"Optimal Harmony: Low reported discomfort is verified by healthy physiological blinking ({blink_rate:.1f}/min). "
            "Precorneal tear film and ciliary focus remain in balance."
        )
    else:
        quadrant = "Compensatory Adaptive Strain"
        badge_color = "#F59E0B"
        silent_risk = False
        interp = (
            f"Moderate Divergence (Delta: {delta:+.1f}%): Discomfort is present but blinking remains partially adaptive. "
            "Visual strain is likely driven by viewing proximity or cervical neck posture rather than tear film collapse alone."
        )

    return {
        "has_camera_data": True,
        "quadrant": quadrant,
        "divergence_score": round(delta, 1),
        "silent_risk": silent_risk,
        "badge_color": badge_color,
        "subjective_pct": round(subj_stress_pct, 1),
        "objective_pct": round(obj_suppression_pct, 1),
        "interpretation": interp,
    }


def simulate_5year_ocular_projection(
    screen_hours: float,
    breaks_per_hr: int,
    years: int,
) -> dict[str, Any]:
    """Projects future Meibomian gland atrophy, Tear Break-Up Time (TBUT), and ciliary spasm risk over 1 to 5 years."""
    # Base risk factor from daily screen exposure and break deficiency
    exposure_factor = max(0.5, screen_hours / 6.0)
    break_deficiency = max(0.2, (3.0 - breaks_per_hr) / 3.0)
    risk_scalar = exposure_factor * (1.0 + break_deficiency * 0.8)

    # Unmitigated projection over time
    meibomian_atrophy_unmitigated = min(68.0, 6.0 + (years * 9.5 * risk_scalar))
    tbut_unmitigated = max(2.2, 11.5 - (years * 1.6 * risk_scalar))
    ciliary_spasm_idx = min(95.0, 15.0 + (years * 14.0 * risk_scalar))

    # Mitigated with AsthenoZero protocol (20-20-20 breaks + blink exercises + Omega-3)
    meibomian_atrophy_mitigated = min(8.0, 3.5 + (years * 0.8))
    tbut_mitigated = min(12.5, max(9.5, 11.0 - (years * 0.2)))
    ciliary_spasm_mitigated = min(18.0, max(5.0, 10.0 - (years * 0.5)))

    # Risk tiers
    if meibomian_atrophy_unmitigated > 35.0:
        gland_status = "Severe Meibomian Gland Drop-Out (Permanent Duct Atrophy)"
        status_color = "#EF4444"
    elif meibomian_atrophy_unmitigated > 20.0:
        gland_status = "Moderate Meibomian Duct Tortuosity & Thickened Secretions"
        status_color = "#F59E0B"
    else:
        gland_status = "Mild Reversible Evaporative Stress"
        status_color = "#38BDF8"

    return {
        "years": years,
        "unmitigated_atrophy_pct": round(meibomian_atrophy_unmitigated, 1),
        "mitigated_atrophy_pct": round(meibomian_atrophy_mitigated, 1),
        "unmitigated_tbut_seconds": round(tbut_unmitigated, 1),
        "mitigated_tbut_seconds": round(tbut_mitigated, 1),
        "ciliary_spasm_index": round(ciliary_spasm_idx, 1),
        "mitigated_ciliary_index": round(ciliary_spasm_mitigated, 1),
        "gland_status": gland_status,
        "status_color": status_color,
    }
