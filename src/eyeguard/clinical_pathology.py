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
            "food_sources": "Wild salmon, sardines, mackerel, chia seeds, flaxseed oil, walnuts, algae oil",
            "clinical_mechanism": (
                "Directly incorporates into Meibomian gland lipids, lowering the melting point of meibum "
                "so it flows smoothly across the ocular surface. Confirmed by the TFOS DEWS II international dry eye workshop."
            ),
            "priority": "High Priority" if screen_time in ["6-8 hours", "More than 8 hours"] or score >= 6.0 else "Core Habit",
        },
        {
            "nutrient": "Macular Carotenoids (Lutein 10mg & Zeaxanthin 2mg)",
            "icon": "🥬",
            "dosage": "10 mg Lutein + 2 mg Zeaxanthin daily",
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
            "food_sources": "Tart cherry juice, pumpkin seeds, dark chocolate (>85%), almonds",
            "clinical_mechanism": (
                "Naturally promotes endogenous melatonin release and relaxes hyper-contracted extraocular muscles, "
                "enabling restorative overnight ocular surface epithelial mitotic repair."
            ),
            "priority": "Targeted Sleep Support",
        })

    return diet_items
