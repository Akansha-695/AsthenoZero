"""Build an executive, high-impact PowerPoint presentation deck for AsthenoZero."""

from __future__ import annotations

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output" / "presentation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PPTX_PATH_1 = OUTPUT_DIR / "AsthenoZero_Presentation.pptx"
PPTX_PATH_2 = PROJECT_ROOT / "AsthenoZero_Presentation.pptx"

# Color Palette: Clinical Tech Dark Theme
COLOR_BG = RGBColor(11, 17, 32)         # Deep Obsidian #0B1120
COLOR_CARD = RGBColor(21, 32, 54)       # Card Surface #152036
COLOR_CARD_BORDER = RGBColor(40, 60, 95)
COLOR_CYAN = RGBColor(56, 189, 248)      # Tech Cyan #38BDF8
COLOR_EMERALD = RGBColor(16, 185, 129)   # Accent Emerald #10B981
COLOR_AMBER = RGBColor(245, 158, 11)     # Warning Amber #F59E0B
COLOR_CORAL = RGBColor(239, 68, 68)      # Alert Red #EF4444
COLOR_WHITE = RGBColor(248, 250, 252)    # Main Text #F8FAFC
COLOR_MUTED = RGBColor(148, 163, 184)    # Secondary Text #94A3B8


def set_slide_background(slide):
    """Sets a dark slate background on the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, category: str, title: str):
    """Adds a standardized category badge and high-impact title."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = "Calibri"
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    p_title.space_before = Pt(2)


def add_card(slide, left: float, top: float, width: float, height: float, border_color=COLOR_CARD_BORDER):
    """Adds a rounded rectangle card container."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_CARD
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape


def add_numbers_box(slide, left: float, top: float, width: float, height: float, title: str, stats: list[tuple[str, str]]):
    """Adds a highlighted metrics and numbers box."""
    add_card(slide, left, top, width, height, border_color=COLOR_EMERALD)
    box = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.2), Inches(width - 0.4), Inches(height - 0.4))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_head = tf.paragraphs[0]
    p_head.text = f"📊 {title.upper()}"
    p_head.font.name = "Calibri"
    p_head.font.size = Pt(11.5)
    p_head.font.bold = True
    p_head.font.color.rgb = COLOR_EMERALD

    for num, label in stats:
        p_num = tf.add_paragraph()
        p_num.space_before = Pt(8)
        r_num = p_num.add_run()
        r_num.text = num
        r_num.font.name = "Calibri"
        r_num.font.size = Pt(16)
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_WHITE

        r_lbl = p_num.add_run()
        r_lbl.text = f"  {label}"
        r_lbl.font.name = "Calibri"
        r_lbl.font.size = Pt(10)
        r_lbl.font.color.rgb = COLOR_MUTED


def build_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "HEALTH-TECH & PRECISION BIOMETRICS • 2026"
    p0.font.name = "Calibri"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN

    p1 = tf1.add_paragraph()
    p1.text = "AsthenoZero"
    p1.font.name = "Calibri"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(6)

    p2 = tf1.add_paragraph()
    p2.text = "Precision Ocular Ergonomics & Digital Asthenopia Suite"
    p2.font.name = "Calibri"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_EMERALD
    p2.space_before = Pt(4)

    p3 = tf1.add_paragraph()
    p3.text = "A closed-loop platform uniting Machine Learning risk modeling, real-time MediaPipe computer vision kinematics, an enforceable behavioral credit economy, and clinical nutritional ophthalmology."
    p3.font.name = "Calibri"
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = Pt(14)

    p4 = tf1.add_paragraph()
    p4.text = "Lead Author & Researcher: Akansha Kashyap  |  LinkedIn: linkedin.com/in/akansha-kashyap-b6a32b362\nSystem Classification: Digital Health / Software as a Medical Device (SaMD) Prototype"
    p4.font.name = "Calibri"
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_CYAN
    p4.space_before = Pt(22)

    # =========================================================================
    # SLIDE 2: The Clinical Problem
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Clinical Problem & Medical Crisis", "Digital Asthenopia & Computer Vision Syndrome (CVS)")

    add_card(slide2, 0.8, 1.7, 7.8, 5.2)
    c_box = slide2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    ctf = c_box.text_frame
    ctf.word_wrap = True

    p = ctf.paragraphs[0]
    p.text = "The Modern Screen Fatigue Epidemic:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    items2 = [
        ("Blink Reflex Arc Suppression:", "Cognitive visual fixation suppresses involuntary blinking. Staring at screens causes blinking frequency to plummet, leaving the cornea uncovered and drying out."),
        ("Precorneal Tear Film Rupture:", "Without regular eyelid closure, the outer lipid layer collapses. Tear Break-Up Time drops rapidly, exposing corneal sensory nerves to painful evaporation."),
        ("Accommodative Ciliary Spasm:", "Near-point focal fixation forces the intraocular ciliary sphincter into continuous isometric cramping. When looking up, distance vision is blurry ('screen pseudomyopia')."),
        ("Permanent Meibomian Gland Dropout:", "Partial incomplete blinks fail to express tarsal gland oils. Over 2 to 5 years, oil glands permanently atrophy, causing irreversible chronic dry eye."),
    ]
    for h, desc in items2:
        p_item = ctf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide2, 8.9, 1.7, 3.6, 5.2, "Clinical Numbers", [
        ("50% – 70%", "Reduction in spontaneous blink rate on screens"),
        ("18-20 → <5", "Blinks/min drop (healthy baseline vs screen read)"),
        ("< 5 Seconds", "Tear Break-Up Time (TBUT) under dry eye strain"),
        ("68.4%", "Computer workers suffering active asthenopia"),
        ("2.5x", "Higher tear evaporation rate in air-conditioned rooms")
    ])

    # =========================================================================
    # SLIDE 3: System Architecture
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Architectural Foundation", "AsthenoZero 5-Pillar Closed-Loop Platform")

    pillars = [
        ("1. ML Predictive Core", "Trained on N=139 cohort. Evaluates 6 lifestyle factors and predicts exploratory asthenopia score (0–15) via L2 Ridge Regression.", COLOR_CYAN),
        ("2. Real-Time Computer Vision", "Processes 468-pt MediaPipe mesh in volatile memory. Calculates EAR, blink completeness, screen distance, and ambient lux.", COLOR_EMERALD),
        ("3. Behavioral Habit Economy", "AsthenoCredits reward pacing. Strict Rehabilitation Protocol physiologically gates streak unfreezing when coins hit 0.", COLOR_AMBER),
        ("4. Clinical Pathology & Diet", "Stratifies vulnerability for 5 ocular conditions and provides AREDS 2 & TFOS DEWS II targeted nutritional protocols.", COLOR_CORAL),
        ("5. Ocular Relaxation Studio", "Guided Vision Gym with animated SVG pursue drills and smart 20-20-20 timer with 432 Hz synthetic alpha acoustic tones.", COLOR_CYAN),
    ]

    for i, (p_title, p_desc, p_color) in enumerate(pillars):
        x = 0.8 + (i * 2.45)
        add_card(slide3, x, 1.7, 2.3, 5.2, border_color=p_color)
        pbox = slide3.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(2.0), Inches(4.8))
        ptf = pbox.text_frame
        ptf.word_wrap = True
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0

        p = ptf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = p_color

        p_body = ptf.add_paragraph()
        p_body.text = p_desc
        p_body.font.size = Pt(10.5)
        p_body.font.color.rgb = COLOR_WHITE
        p_body.space_before = Pt(12)

    # =========================================================================
    # SLIDE 4: Machine Learning Predictive Core
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Predictive Modeling", "Machine Learning Core: L2 Ridge Regression Pipeline")

    add_card(slide4, 0.8, 1.7, 7.8, 5.2)
    ml_box = slide4.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    mtf = ml_box.text_frame
    mtf.word_wrap = True

    p = mtf.paragraphs[0]
    p.text = "How the Predictive Engine Works:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    ml_points = [
        ("Why We Added It:", "Provides instant diagnostic triage before the user even turns on their webcam. Calculates personalized baseline risk from routine workstation behavior."),
        ("Rigorous Grouped Validation:", "Trained on N=139 clinical survey responses. Identical response profiles were grouped within folds to completely eliminate data leakage."),
        ("Model Comparison & Winner:", "Benchmarked against Mean Baseline (MAE 2.63) and Random Forest (MAE 2.47). L2 Regularized Ridge (alpha=5.0) achieved superior generalization: MAE 2.40 ± 0.32."),
        ("Interactive Vector Gauge:", "Generates a real-time SVG semi-circular gauge color-coded into 4 clinical risk tiers (Low, Mild, Moderate, High Digital Strain)."),
    ]
    for h, desc in ml_points:
        p_item = mtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide4, 8.9, 1.7, 3.6, 5.2, "ML Model Metrics", [
        ("N = 139", "Clinical survey cohort sample size"),
        ("MAE 2.40", "Grouped 5-Fold Cross-Validation Error"),
        ("RMSE 2.88", "Root Mean Squared Error (alpha=5.0)"),
        ("+0.086 MAE", "Sleep Category (Top Permutation Feature)"),
        ("+0.077 MAE", "Vision Correction (2nd Dominant Driver)")
    ])

    # =========================================================================
    # SLIDE 5: Computer Vision Blink Diagnostics
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Computer Vision Kinematics", "MediaPipe 468-Point Mesh & 60-Second Reading Protocol")

    add_card(slide5, 0.8, 1.7, 7.8, 5.2)
    cv_box = slide5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    cvtf = cv_box.text_frame
    cvtf.word_wrap = True

    p = cvtf.paragraphs[0]
    p.text = "Mathematical Precision Eye Tracking:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    cv_points = [
        ("Eye Aspect Ratio (EAR) Formulation:", "Computes bilateral ratio using 6 anatomical landmarks: EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|). Accurately distinguishes eyelid closure from gaze shift."),
        ("5-Second Baseline Calibration:", "Calibrates to the user's unique eye aperture size at rest. Dynamically establishes personal closure threshold = resting_EAR * 0.72."),
        ("Isomorphic 60s Reading Protocol:", "Solves the flaw of random blink trackers. Uses a calibrated 231-word clinical reading text so all users undergo identical cognitive load."),
        ("Zero-Retention Privacy Architecture:", "Processed entirely in volatile RAM buffers. Zero video frames or biometric face vectors are stored to disk or transmitted over networks."),
    ]
    for h, desc in cv_points:
        p_item = cvtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide5, 8.9, 1.7, 3.6, 5.2, "Kinematic Numbers", [
        ("468 Points", "High-precision 3D facial topology landmarks"),
        ("6 Fiducials", "Anatomical coordinate points tracked per eye"),
        ("231 Words", "Standardized alphanumeric reading stimulus"),
        ("60 Seconds", "Clinical diagnostic duration"),
        ("0 Frames", "Saved to disk (100% Volatile Client RAM)")
    ])

    # =========================================================================
    # SLIDE 6: Incomplete Blinks & Meibomian Pump Efficiency
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Patent Novelty Claim #1", "Incomplete Blink Ratio & Meibomian Gland Pump Efficiency")

    add_card(slide6, 0.8, 1.7, 7.8, 5.2)
    ib_box = slide6.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    ibtf = ib_box.text_frame
    ibtf.word_wrap = True

    p = ibtf.paragraphs[0]
    p.text = "Why Blink Quality Matters More Than Quantity:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    ib_points = [
        ("The Clinical Discovery:", "In dry eye disease, patients often blink frequently, but 70%+ of the blinks are incomplete micro-blinks where eyelid margins never touch!"),
        ("The Consequence:", "Incomplete blinks fail to mechanically compress the tarsal Meibomian glands, halting lipid oil flow and causing rapid tear evaporation."),
        ("What Makes AsthenoZero Unique:", "Every existing blink tracker merely counts blinks as 0 or 1. AsthenoZero is the FIRST to classify blink completeness and calculate Meibomian Pump Efficiency %."),
        ("Biometric Formulation:", "Blinks reaching EAR_min < 0.70 * threshold are Complete; shallower dips are Incomplete. Efficiency = (Complete / Total) * 100."),
    ]
    for h, desc in ib_points:
        p_item = ibtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide6, 8.9, 1.7, 3.6, 5.2, "Biometric Thresholds", [
        ("< 0.70x", "Threshold factor for Complete Blink verification"),
        ("< 65%", "Pump Efficiency trigger for squeeze therapy"),
        ("30-40", "Meibomian gland orifices in upper eyelid"),
        ("20-30", "Meibomian gland orifices in lower eyelid"),
        ("100%", "Automated lipid pump efficiency calculation")
    ])

    # =========================================================================
    # SLIDE 7: Screen Distance & Ambient Lighting
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Zero-Hardware Ergonomics", "Canthal Distance Triangulation & Ambient Lux Analyzer")

    add_card(slide7, 0.8, 1.7, 7.8, 5.2)
    dist_box = slide7.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    dtf = dist_box.text_frame
    dtf.word_wrap = True

    p = dtf.paragraphs[0]
    p.text = "Hardware-Free Workstation Environmental Telemetry:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    dist_points = [
        ("Screen Distance Telemetry:", "Uses outer canthal landmarks (33 & 263) calibrated against adult 9.5 cm anatomical span to measure viewing distance in inches without LiDAR."),
        ("Postural Slouch Warning:", "Detects forward-head slouch when distance drops <18 inches. Flags acute accommodative spasm risk and cervical spine strain."),
        ("Ambient Room Lighting (Lux Proxy):", "Samples non-face corner pixels to calculate relative luminance: Y = 0.299R + 0.587G + 0.114B."),
        ("Display Contrast Stress Analyzer:", "Identifies eye-straining dark rooms where bright monitor luminescence forces extreme pupil oscillation and retinal fatigue."),
    ]
    for h, desc in dist_points:
        p_item = dtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide7, 8.9, 1.7, 3.6, 5.2, "Ergonomic Zones", [
        ("20 – 28 in", "Optimal Ergonomic Screen Distance"),
        ("< 18 in", "Warning Threshold: Excessive Ciliary Spasm"),
        ("> 30 in", "Distant Posture / Small Font Squinting"),
        ("9.5 cm", "Anatomical adult inter-canthal calibration baseline"),
        ("70 – 190 Y", "Balanced Room-to-Screen Lux Zone")
    ])

    # =========================================================================
    # SLIDE 8: Silent Asthenopia Detector (SO-DI)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Clinical Innovation #2", "Subjective-Objective Divergence Index (Silent Asthenopia)")

    add_card(slide8, 0.8, 1.7, 7.8, 5.2)
    sodi_box = slide8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    soditf = sodi_box.text_frame
    soditf.word_wrap = True

    p = soditf.paragraphs[0]
    p.text = "Detecting Asymptomatic Ocular Desiccation:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    sodi_points = [
        ("The Silent Asthenopia Trap:", "Software engineers, gamers, and students often adapt cognitively, reporting feeling 'fine' while their blink rate has collapsed to 4/min."),
        ("Sensory Nerve Desensitization:", "Chronic tear evaporation numbs corneal subbasal nerve plexus endings, suppressing pain signals until permanent tissue breakdown occurs."),
        ("The SO-DI Metric:", "Delta = Norm(Objective Blink Suppression & Incomplete Ratio) - Norm(Subjective Reported Discomfort)."),
        ("Diagnostic Quadrant Alert:", "When subjective score is low (<30%) but objective suppression is severe (>60%), AsthenoZero triggers 'Silent Asthenopia Alert' to prevent irreversible damage."),
    ]
    for h, desc in sodi_points:
        p_item = soditf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide8, 8.9, 1.7, 3.6, 5.2, "Diagnostic Quadrants", [
        ("Silent Asthenopia", "High Objective Suppression + Low Pain"),
        ("Concordant High", "Severe Discomfort + Severe Suppression"),
        ("Homeostasis", "Healthy Blinking + Low Discomfort"),
        ("Compensatory", "Moderate Adaptive Strain"),
        ("4 Quadrants", "Multi-modal psychometric-biometric pairing")
    ])

    # =========================================================================
    # SLIDE 9: 5-Year Digital Eye Twin Simulator
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Longitudinal Simulation", "Interactive 5-Year Ocular Health Projection Simulator")

    add_card(slide9, 0.8, 1.7, 7.8, 5.2)
    twin_box = slide9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    twintf = twin_box.text_frame
    twintf.word_wrap = True

    p = twintf.paragraphs[0]
    p.text = "A 'Time Machine' for Visual Homeostasis:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    twin_points = [
        ("Why Required:", "Users dismiss eye strain because it accumulates slowly. This simulator visually proves the compounding long-term danger of unmitigated screen exposure."),
        ("Interactive Horizon Slider:", "Allows users to slide between 1 and 5 years to view projected biophysical deterioration under their exact habits."),
        ("Side-by-Side Contrast:", "Directly contrasts the Unmitigated Trajectory (red card) against the Preserved Trajectory achieved with AsthenoZero (green card)."),
        ("Compounding Biophysical Formulas:", "Simulates Meibomian duct atrophy %, Tear Break-Up Time (TBUT) decay, and intraocular ciliary tonic spasm burden."),
    ]
    for h, desc in twin_points:
        p_item = twintf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide9, 8.9, 1.7, 3.6, 5.2, "3-Year Projection", [
        ("57.0% vs <5.9%", "Meibomian Gland Atrophy (Unmitigated vs Care)"),
        ("2.9s vs 10.4s", "Tear Break-Up Time (Severe Dry Eye vs Normal)"),
        ("90.1 vs 8.5", "Ciliary Spasm Burden / 100 (Cramp vs Fluid)"),
        ("1 to 5 Years", "Continuous interactive projection horizon"),
        ("Permanent", "Drop-out risk of Meibomian tarsal ducts")
    ])

    # =========================================================================
    # SLIDE 10: Behavioral Economics: AsthenoCredits
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Behavioral Economics", "AsthenoCredits Economy & Strict Rehabilitation Protocol")

    add_card(slide10, 0.8, 1.7, 7.8, 5.2)
    econ_box = slide10.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    econtf = econ_box.text_frame
    econtf.word_wrap = True

    p = econtf.paragraphs[0]
    p.text = "Physiologically-Gated Digital Habit Enforcement:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    econ_points = [
        ("Why We Replaced OcuCoins with AsthenoCredits:", "Created an aligned, professional economy branded after Asthenopia mitigation ('AsthenoCredits')."),
        ("Earned Through Clinical Action:", "Users earn credits by performing healthy visual behaviors (+15 Habit Diary, +20 Breaks, +25 Vision Gym, +35 Diagnostics)."),
        ("Streak Insurance & Vault:", "Users can spend 40 credits on Streak Shields to auto-protect missed days, or 50 credits to repair broken streaks."),
        ("The Strict Rehabilitation Protocol:", "When streak is broken and coins hit 0, bypass purchases are LOCKED. The user must complete all 3 physical therapy tasks to reinstate their streak."),
    ]
    for h, desc in econ_points:
        p_item = econtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide10, 8.9, 1.7, 3.6, 5.2, "Economy Structure", [
        ("+15 🪙", "Log Daily Screen Diary"),
        ("+20 🪙", "Complete 20-20-20 Micro-Break"),
        ("+25 🪙", "Execute Guided Vision Gym Exercise"),
        ("+35 🪙", "Complete 60s Webcam Blink Diagnostic"),
        ("+60 🪙", "Strict Rehabilitation Graduation Bonus")
    ])

    # =========================================================================
    # SLIDE 11: 20-20-20 Smart Adaptive Break Suite
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Pacing & Ergonomic Interlocks", "Smart AI Adaptive Pacing & Neuro-Acoustic Suite")

    add_card(slide11, 0.8, 1.7, 7.8, 5.2)
    pace_box = slide11.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    pacetf = pace_box.text_frame
    pacetf.word_wrap = True

    p = pacetf.paragraphs[0]
    p.text = "Pacing Beyond Rigid Fixed Timers:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    pace_points = [
        ("Smart Biometric Adaptive Pacing:", "Dynamically recalibrates interval cadence based on live asthenopia score (15m/5m for severe fatigue >=60, 20m/3m standard, 25m/5m preventative)."),
        ("AsthenoZero Strict Interlock:", "Eliminates cheating. During a 20-second break, pause and reset controls are disabled, enforcing genuine 20-foot optical rest."),
        ("432 Hz Calm Alpha Tone Generator:", "Synthesizes zero-latency 432 Hz sine waves with 540 Hz overtones via native browser Web Audio API for neuro-muscular ciliary relaxation."),
        ("Daily Screen Exposure Budget:", "Allows users to set safe daily limits (e.g. 7.0h), triggering an Asthenopia Overuse Shield when exceeded."),
    ]
    for h, desc in pace_points:
        p_item = pacetf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide11, 8.9, 1.7, 3.6, 5.2, "Timer Parameters", [
        ("15m / 5m", "Intensive Corneal Recovery Cadence (Score >=60)"),
        ("20m / 3m", "Standard 20-20-20 Micro-Pacing"),
        ("25m / 5m", "Sustained Focus & Preventative Care"),
        ("432 Hz", "Harmonic Alpha Brainwave Resonance Frequency"),
        ("100% Locked", "Strict Interlock during break rest intervals")
    ])

    # =========================================================================
    # SLIDE 12: Vision Gym & Physical Therapy
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "Ophthalmic Physical Therapy", "Vision Gym: Animated Ocular Muscle Decompression")

    add_card(slide12, 0.8, 1.7, 7.8, 5.2)
    gym_box = slide12.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    gymtf = gym_box.text_frame
    gymtf.word_wrap = True

    p = gymtf.paragraphs[0]
    p.text = "Active Counter-Strain Muscle Rehabilitation:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    gym_points = [
        ("Why Physical Exercises Are Required:", "Looking away is passive. Extraocular rectus muscles and the ciliary body require dynamic elongation and lipid gland compression."),
        ("Figure-8 Smooth Pursuit:", "Animated SVG infinity loop guides continuous circular gaze tracking to release tonic contractions in the 6 extraocular muscles."),
        ("4-Phase Meibomian Blink & Squeeze:", "Guides users through Light Close (2s) -> Squeeze Shut (2s) -> Open (2s) -> Rest (2s) to express thickened meibum oils."),
        ("Near-Far Accommodation Switcher:", "Rhythmically shifts optical focus between near text and 20-foot distance targets, breaking ciliary spasm loops."),
    ]
    for h, desc in gym_points:
        p_item = gymtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide12, 8.9, 1.7, 3.6, 5.2, "Clinical Drills", [
        ("5 Protocols", "Targeted Ocular Relaxation Drills"),
        ("6 Muscles", "Extraocular rectus & oblique muscles mobilized"),
        ("4 Phases", "Meibomian Isometric Squeeze Cycle"),
        ("40°C Warm", "Palming thermal photoreceptor relaxation"),
        ("0 Plugins", "Pure SVG mathematical vector animations")
    ])

    # =========================================================================
    # SLIDE 13: Clinical Pathology & Nutrition
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "Biochemical Therapeutics", "Clinical Pathology & Nutritional Ophthalmology")

    add_card(slide13, 0.8, 1.7, 7.8, 5.2)
    path_box = slide13.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    pathtf = path_box.text_frame
    pathtf.word_wrap = True

    p = pathtf.paragraphs[0]
    p.text = "Targeted Disease Vulnerability & Diet Protocols:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    path_points = [
        ("Stratification of 5 Conditions:", "Translates user habits into vulnerability for MGD/Dry Eye, Ciliary Spasm, Contact Lens Keratitis, Convergence Insufficiency, and Phototoxicity."),
        ("Evidence-Based Clinical Nutrition:", "Formulated from AREDS 2 and TFOS DEWS II international dry eye clinical trials."),
        ("Omega-3 Fatty Acids (EPA/DHA):", "Lowers the melting point of meibum lipid secretions so oils flow smoothly over the cornea."),
        ("Macular Carotenoids (Lutein & Zeaxanthin):", "Acts as an internal biological blue-light filter, absorbing high-energy 450-480nm wavelengths before reaching the retina."),
    ]
    for h, desc in path_points:
        p_item = pathtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide13, 8.9, 1.7, 3.6, 5.2, "Clinical Prescriptions", [
        ("1,000 – 1,200 mg", "Daily EPA & DHA Omega-3 Fatty Acids"),
        ("10 mg / 2 mg", "Daily Lutein & Zeaxanthin Macular Carotenoids"),
        ("2.5 – 3.0 Liters", "Daily Hydration to prevent tear hyperosmolarity"),
        ("200 – 300 mg", "Magnesium Glycinate for nocturnal epithelial repair"),
        ("5 Conditions", "Pathologies mapped to individual user habits")
    ])

    # =========================================================================
    # SLIDE 14: Competitive Advantage Matrix
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14)
    add_header(slide14, "Market Differentiation", "AsthenoZero vs Existing Commercial Solutions")

    add_card(slide14, 0.8, 1.7, 11.7, 5.2)
    comp_box = slide14.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(4.8))
    comptf = comp_box.text_frame
    comptf.word_wrap = True

    p = comptf.paragraphs[0]
    p.text = "Feature-by-Feature Competitor Benchmark:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    comp_rows = [
        ("Predictive ML Risk Scoring (CV MAE 2.40)", "AsthenoZero: YES (Trained Ridge)", "Competitors: NONE (Static questionnaires or none)"),
        ("Incomplete vs Complete Blink Ratio", "AsthenoZero: YES (EAR min calculation)", "Competitors: NONE (Binary open/close count only)"),
        ("Zero-Hardware Screen Distance & Posture", "AsthenoZero: YES (Canthal Triangulation)", "Competitors: NONE (Requires LiDAR or unmonitored)"),
        ("Silent Asthenopia Divergence Index (SO-DI)", "AsthenoZero: YES (Subjective vs Objective)", "Competitors: NONE (No multi-modal cross-analysis)"),
        ("Interactive 5-Year Digital Eye Twin", "AsthenoZero: YES (1-5 Year Simulator)", "Competitors: NONE (Zero long-term predictive models)"),
        ("Habit Economy with Strict Physiological Lock", "AsthenoZero: YES (AsthenoCredits + Drills)", "Competitors: NONE (Cash bypass, ad views, or snoozes)"),
        ("Zero-Retention Local RAM Privacy", "AsthenoZero: YES (0 frames stored)", "Competitors: Varies (Often streams to cloud/servers)"),
    ]

    for f_name, az_val, comp_val in comp_rows:
        p_row = comptf.add_paragraph()
        p_row.space_before = Pt(6)
        r_f = p_row.add_run()
        r_f.text = f"• {f_name}: "
        r_f.font.bold = True
        r_f.font.size = Pt(11)
        r_f.font.color.rgb = COLOR_WHITE

        r_az = p_row.add_run()
        r_az.text = f"[{az_val}]  "
        r_az.font.bold = True
        r_az.font.size = Pt(10.5)
        r_az.font.color.rgb = COLOR_EMERALD

        r_comp = p_row.add_run()
        r_comp.text = f"vs  {comp_val}"
        r_comp.font.size = Pt(10)
        r_comp.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 15: Deployment & Conclusion
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15)
    add_header(slide15, "Project Conclusion & Deployment", "Validation, Live Deployment & Future Horizons")

    add_card(slide15, 0.8, 1.7, 7.8, 5.2)
    end_box = slide15.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(7.2), Inches(4.8))
    endtf = end_box.text_frame
    endtf.word_wrap = True

    p = endtf.paragraphs[0]
    p.text = "Deployment, Integrity & Roadmap:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    end_points = [
        ("Live Cloud Deployment:", "Fully deployed and accessible worldwide at https://asthenozero.streamlit.app/ on Streamlit Community Cloud."),
        ("Open-Source GitHub Repository:", "Publicly available with full documentation, tests, and CI/CD at https://github.com/Akansha-695/AsthenoZero.git."),
        ("Clinical & Patent Viability:", "Patent novelty matrix formulated across 7 distinct inventive steps for provisional patent application."),
        ("Planned Next Steps:", "Direct integration with Smart Home lighting protocols (auto-dimming room lux) and deep pupillometric sympathetic arousal tracking."),
    ]
    for h, desc in end_points:
        p_item = endtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_MUTED

    add_numbers_box(slide15, 8.9, 1.7, 3.6, 5.2, "Platform Status", [
        ("100% Live", "Production Cloud Deployment"),
        ("15 Slides", "Comprehensive Project Deck"),
        ("7 Claims", "Patent Novelty Matrix Disclosures"),
        ("0 Latency", "Web Audio API 432 Hz Sound Engine"),
        ("v2.5 Pro", "Precision Release Architecture")
    ])

    # Save to both paths
    prs.save(str(PPTX_PATH_1))
    prs.save(str(PPTX_PATH_2))
    print(f"Presentation saved successfully to:\n - {PPTX_PATH_1}\n - {PPTX_PATH_2}")


if __name__ == "__main__":
    build_deck()
