"""Build a visually stunning, magnetic 16:9 PowerPoint presentation deck for AsthenoZero.
Includes real application screenshots, generated scientific diagrams, rich layout variety,
and compelling narrative flow.
"""

from __future__ import annotations

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "output" / "presentation" / "assets"
OUTPUT_DIR = PROJECT_ROOT / "output" / "presentation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PPTX_PATH_1 = OUTPUT_DIR / "AsthenoZero_Presentation.pptx"
PPTX_PATH_2 = PROJECT_ROOT / "AsthenoZero_Presentation.pptx"

# Color Palette: Obsidian Health-Tech Theme
COLOR_BG = RGBColor(10, 15, 29)          # Deep Obsidian #0A0F1D
COLOR_CARD = RGBColor(17, 26, 46)        # Card Surface #111A2E
COLOR_CARD_BORDER = RGBColor(35, 52, 84) # Card Border #233454
COLOR_CYAN = RGBColor(56, 189, 248)       # Electric Cyan #38BDF8
COLOR_EMERALD = RGBColor(16, 185, 129)    # Emerald Accent #10B981
COLOR_AMBER = RGBColor(245, 158, 11)      # Amber Warning #F59E0B
COLOR_CORAL = RGBColor(244, 63, 94)       # Coral Alert #F43F5E
COLOR_WHITE = RGBColor(248, 250, 252)     # Primary Text #F8FAFC
COLOR_MUTED = RGBColor(148, 163, 184)     # Secondary Text #94A3B8


def set_slide_background(slide):
    """Sets a dark slate background on the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, category: str, title: str):
    """Adds a standardized category badge and high-impact title."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.15))
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


def add_card(slide, left: float, top: float, width: float, height: float, border_color=COLOR_CARD_BORDER, fill_color=COLOR_CARD):
    """Adds a rounded rectangle card container."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape


def add_image_safe(slide, img_name: str, left: float, top: float, width: float | None = None, height: float | None = None):
    """Safely adds an image if present, returning the shape."""
    img_path = ASSETS_DIR / img_name
    if not img_path.exists():
        print(f"Warning: Image not found: {img_path}")
        return None
    kwargs = {"left": Inches(left), "top": Inches(top)}
    if width:
        kwargs["width"] = Inches(width)
    if height:
        kwargs["height"] = Inches(height)
    return slide.shapes.add_picture(str(img_path), **kwargs)


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide (Hero Visual Layout)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Left content box
    add_card(s1, 0.8, 1.2, 7.0, 5.3, border_color=COLOR_CYAN)
    tbox = s1.shapes.add_textbox(Inches(1.1), Inches(1.4), Inches(6.4), Inches(4.9))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "PRECISION HEALTH-TECH & BIOMETRICS • 2026"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf1.add_paragraph()
    p.text = "AsthenoZero"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

    p = tf1.add_paragraph()
    p.text = "Precision Ocular Ergonomics & Digital Asthenopia Suite"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_before = Pt(2)

    p = tf1.add_paragraph()
    p.text = "A breakthrough closed-loop system uniting Machine Learning risk triage, real-time MediaPipe computer vision kinematics, a physiologically-gated habit credit economy, and clinical nutritional ophthalmology."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Lead Author & Researcher: Akansha Kashyap\nLinkedIn: linkedin.com/in/akansha-kashyap-b6a32b362\nClassification: Digital Health / Software as a Medical Device (SaMD) Prototype"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(16)

    # Right side image preview
    add_card(s1, 8.1, 1.2, 4.4, 5.3, border_color=COLOR_CARD_BORDER)
    add_image_safe(s1, "app_risk_gauge.png", 8.3, 1.4, width=4.0)
    add_image_safe(s1, "app_eye_twin_slider.jpg", 8.3, 3.8, width=4.0)

    # =========================================================================
    # SLIDE 2: The Medical Crisis (Split: Medical Problem + Chart)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Medical Epidemic", "Digital Asthenopia & The Silent Vision Crisis")

    # Left card: Clinical pathology
    add_card(s2, 0.8, 1.7, 6.2, 5.2)
    c2_box = s2.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.8), Inches(4.8))
    c2tf = c2_box.text_frame
    c2tf.word_wrap = True

    p = c2tf.paragraphs[0]
    p.text = "The 4 Hidden Pathological Drivers:"
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    items2 = [
        ("Blink Reflex Arc Suppression:", "Cognitive visual fixation suppresses involuntary blinking. Staring at screens causes blink rate to collapse from 18-20 down to <5 blinks/min."),
        ("Precorneal Tear Film Rupture:", "Without regular eyelid apposition, the outer lipid layer collapses. Tear Break-Up Time (TBUT) falls under 5 seconds, exposing corneal sensory nerves."),
        ("Accommodative Ciliary Spasm:", "Near-point convergence locks intraocular ciliary muscles in continuous isometric contraction ('screen pseudomyopia' & frontal brow aches)."),
        ("Permanent Meibomian Dropout:", "Incomplete micro-blinks fail to mechanically pump eyelid oils. Glands clog and permanently atrophy over 2 to 5 years."),
    ]
    for h, desc in items2:
        p_item = c2tf.add_paragraph()
        p_item.space_before = Pt(6)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: Blink suppression timeline chart
    add_card(s2, 7.3, 1.7, 5.2, 5.2, border_color=COLOR_CORAL)
    add_image_safe(s2, "blink_suppression_chart.png", 7.45, 1.85, width=4.9)

    # =========================================================================
    # SLIDE 3: 5-Pillar Architecture (Visual Workflow Cards)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Architecture", "The AsthenoZero 5-Pillar Closed-Loop Platform")

    pillars = [
        ("1. ML Predictive Core", "Trained on N=139 cohort. Evaluates 6 lifestyle factors and predicts baseline asthenopia (0–15) via L2 Ridge Regression.", COLOR_CYAN),
        ("2. Computer Vision", "468-point MediaPipe mesh in volatile RAM. Tracks EAR, blink completeness, screen distance & ambient lux.", COLOR_EMERALD),
        ("3. Behavioral Economy", "AsthenoCredits vault with Strict Rehabilitation Challenge. Physiologically gates streak unfreezing when coins hit 0.", COLOR_AMBER),
        ("4. Pathology & Diet", "Stratifies risk for 5 ocular conditions and provides AREDS 2 & TFOS DEWS II targeted nutritional protocols.", COLOR_CORAL),
        ("5. Ocular Relaxation", "Vision Gym with animated SVG pursue drills and smart 20-20-20 timer with 432 Hz synthetic alpha acoustic waves.", COLOR_CYAN),
    ]

    for i, (p_title, p_desc, p_color) in enumerate(pillars):
        x = 0.8 + (i * 2.45)
        add_card(s3, x, 1.7, 2.3, 5.2, border_color=p_color)
        pbox = s3.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(2.0), Inches(4.8))
        ptf = pbox.text_frame
        ptf.word_wrap = True

        p = ptf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = p_color

        p_body = ptf.add_paragraph()
        p_body.text = p_desc
        p_body.font.size = Pt(10)
        p_body.font.color.rgb = COLOR_WHITE
        p_body.space_before = Pt(10)

    # =========================================================================
    # SLIDE 4: Machine Learning Predictive Core (Split: Specs + Dual-Panel Chart)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Predictive Modeling", "Machine Learning Core: L2 Ridge Regression Pipeline")

    # Left side: ML specifications
    add_card(s4, 0.8, 1.7, 5.5, 5.2)
    s4_box = s4.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.1), Inches(4.8))
    s4tf = s4_box.text_frame
    s4tf.word_wrap = True

    p = s4tf.paragraphs[0]
    p.text = "Grouped 5-Fold Cross-Validation Metrics:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    ml_items = [
        ("Cohort Sample Size:", "N = 139 clinical research survey participants."),
        ("Leakage Prevention:", "Grouped identical response tuples into the same fold to prevent optimistic train-test leakage."),
        ("Model Benchmark:", "Outperformed Dummy Baseline (MAE 2.63) and Random Forest (MAE 2.47) with an optimized L2 Ridge (alpha=5.0) achieving MAE 2.40 ± 0.32."),
        ("Top Feature Drivers:", "Sleep Duration (+0.086 MAE loss upon permutation) and Vision Correction (+0.077) are the dominant predictors."),
        ("Interactive Vector Gauge:", "Renders an SVG semi-circle risk meter color-coded into 4 risk tiers (Low, Mild, Moderate, High Digital Strain)."),
    ]
    for h, desc in ml_items:
        p_item = s4tf.add_paragraph()
        p_item.space_before = Pt(5)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: Chart
    add_card(s4, 6.6, 1.7, 5.9, 5.2, border_color=COLOR_EMERALD)
    add_image_safe(s4, "ml_benchmark_chart.png", 6.75, 1.85, width=5.6)

    # =========================================================================
    # SLIDE 5: Computer Vision Diagnostics (Split: Formula + Live App Screenshot)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Computer Vision Kinematics", "MediaPipe 468-Point Mesh & 60-Second Reading Protocol")

    # Left side: CV details
    add_card(s5, 0.8, 1.7, 5.6, 5.2)
    s5_box = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    s5tf = s5_box.text_frame
    s5tf.word_wrap = True

    p = s5tf.paragraphs[0]
    p.text = "Mathematical Precision Eye Tracking:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    cv_items = [
        ("Eye Aspect Ratio (EAR):", "Formula: EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|). Accurately distinguishes eyelid closure from gaze shift."),
        ("5-Second Calibration:", "Dynamically establishes personal threshold = resting_EAR * 0.72 to match individual facial anatomy."),
        ("Isomorphic 60s Reading Text:", "Standardizes cognitive demand with a calibrated 231-word clinical passage, eliminating erratic testing variance."),
        ("Zero-Retention Privacy:", "Processed 100% in volatile client RAM buffers. Zero video frames or facial vectors are stored or transmitted."),
    ]
    for h, desc in cv_items:
        p_item = s5tf.add_paragraph()
        p_item.space_before = Pt(6)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: App screenshot
    add_card(s5, 6.7, 1.7, 5.8, 5.2, border_color=COLOR_CYAN)
    add_image_safe(s5, "app_blink_diagnostic.png", 6.85, 1.85, width=5.5)

    # =========================================================================
    # SLIDE 6: Incomplete Blinks & Meibomian Pump % (Split: Novelty + Diagram)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Patent Novelty Claim #1", "Incomplete Blink Ratio & Meibomian Gland Pump Efficiency")

    # Left side: Novelty breakdown
    add_card(s6, 0.8, 1.7, 5.5, 5.2)
    s6_box = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.1), Inches(4.8))
    s6tf = s6_box.text_frame
    s6tf.word_wrap = True

    p = s6tf.paragraphs[0]
    p.text = "Why Blink Depth Outweighs Simple Count:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    ib_items = [
        ("The Medical Finding:", "In dry eye disease, patients often blink frequently, but 70%+ are shallow micro-blinks where eyelid margins never touch!"),
        ("The Gland Pump Failure:", "Micro-blinks fail to mechanically compress the tarsal Meibomian glands, halting lipid secretion and accelerating evaporative tear breakdown."),
        ("The AsthenoZero Innovation:", "Every existing blink app only counts blinks as 0 or 1. AsthenoZero is the FIRST to classify blink completeness and calculate Meibomian Pump Efficiency %."),
        ("Biometric Formulation:", "Blinks reaching EAR_min < 0.70 * threshold are Complete; shallower dips are Incomplete. Pump % = (Complete / Total) * 100."),
        ("Clinical Threshold:", "Efficiency < 65% triggers targeted 4-phase squeeze exercise therapy."),
    ]
    for h, desc in ib_items:
        p_item = s6tf.add_paragraph()
        p_item.space_before = Pt(5)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: Kinematics diagram
    add_card(s6, 6.6, 1.7, 5.9, 5.2, border_color=COLOR_EMERALD)
    add_image_safe(s6, "cv_ear_landmarks.png", 6.75, 1.85, width=5.6)

    # =========================================================================
    # SLIDE 7: Screen Distance & Ambient Lighting (Infographic Layout)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Zero-Hardware Environmental Telemetry", "Canthal Distance Triangulation & Ambient Lux Analyzer")

    # 2 Big Cards
    add_card(s7, 0.8, 1.7, 5.7, 5.2, border_color=COLOR_CYAN)
    d_box = s7.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    dtf = d_box.text_frame
    dtf.word_wrap = True

    p = dtf.paragraphs[0]
    p.text = "📐 Screen Distance & Postural Slouching"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    d_items = [
        ("Canthal Triangulation:", "Uses outer canthal landmarks (33 & 263) calibrated against adult 9.5 cm anatomical baseline to measure distance in inches."),
        ("No External Sensors Needed:", "Delivers continuous posture telemetry through a standard webcam without requiring LiDAR or infrared depth cameras."),
        ("Optimal Zone (20–28 inches):", "Maintains relaxed ciliary muscle focal accommodation and physiological vergence."),
        ("Slouch Warning (<18 inches):", "Detects forward-head slouching and warns user of severe ciliary spasm risk and cervical strain."),
    ]
    for h, desc in d_items:
        p_item = dtf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    add_card(s7, 6.8, 1.7, 5.7, 5.2, border_color=COLOR_AMBER)
    l_box = s7.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    ltf = l_box.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "💡 Ambient Lighting & Display Contrast Stress"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    l_items = [
        ("Peripheral Lux Sampling:", "Samples non-face corner pixels from video stream to compute relative luminance: Y = 0.299R + 0.587G + 0.114B."),
        ("The Contrast Stress Danger:", "Staring at a bright screen in a pitch-dark room causes extreme pupil diameter oscillation and acute retinal fatigue."),
        ("Balanced Lux Zone (70–190 Y):", "Promotes optimal pupillary equilibrium and reduces glare reflection."),
        ("Glare / Excessive Alert (>190 Y):", "Flags harsh specular lighting causing reflection and squint-induced asthenopia."),
    ]
    for h, desc in l_items:
        p_item = ltf.add_paragraph()
        p_item.space_before = Pt(8)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 8: Silent Asthenopia Detector (SO-DI 4-Quadrant Matrix)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Clinical Innovation #2", "Subjective-Objective Divergence Index (Silent Asthenopia)")

    # 4 Quadrants
    quads = [
        ("🚨 SILENT ASTHENOPIA", "High Objective Suppression + Low Subjective Pain\nCorneal sensory nerve desensitization. The patient feels 'fine' while tears evaporate and Meibomian glands clog. High risk of permanent tissue dropout.", COLOR_CORAL),
        ("⚠️ CONCORDANT HIGH STRAIN", "Severe Discomfort + Severe Objective Suppression\nAcute alignment: Patient feels severe burning and headache while camera confirms 75%+ blink suppression. Requires immediate micro-break.", COLOR_AMBER),
        ("🛡️ CONCORDANT HOMEOSTASIS", "Low Discomfort + Healthy Physiological Blinking\nOptimal visual equilibrium: Precorneal tear film and ciliary focus remain in healthy biological balance (>=14 blinks/min).", COLOR_EMERALD),
        ("🔄 COMPENSATORY STRAIN", "Mild to Moderate Divergent Strain\nUser is beginning to show early signs of accommodative fatigue or sporadic blink suppression. Preventative micro-pacing recommended.", COLOR_CYAN),
    ]

    for i, (q_title, q_desc, q_color) in enumerate(quads):
        row = i // 2
        col = i % 2
        x = 0.8 + (col * 5.95)
        y = 1.7 + (row * 2.65)
        add_card(s8, x, y, 5.75, 2.45, border_color=q_color)
        qbox = s8.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(5.35), Inches(2.15))
        qtf = qbox.text_frame
        qtf.word_wrap = True

        p = qtf.paragraphs[0]
        p.text = q_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = q_color

        p_desc = qtf.add_paragraph()
        p_desc.text = q_desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_WHITE
        p_desc.space_before = Pt(6)

    # =========================================================================
    # SLIDE 9: 5-Year Digital Eye Twin (Split: Concept + Real Screenshot + Graph)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Longitudinal Simulation", "Interactive 5-Year Ocular Health Projection Simulator")

    # Left card: Concept
    add_card(s9, 0.8, 1.7, 5.5, 5.2)
    s9_box = s9.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.1), Inches(4.8))
    s9tf = s9_box.text_frame
    s9tf.word_wrap = True

    p = s9tf.paragraphs[0]
    p.text = "A 'Time Machine' for Visual Longevity:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    twin_items = [
        ("The Psychology of Neglect:", "Users ignore eye strain because it accumulates slowly. This simulator visually exposes the compounding 5-year consequences of unmitigated screen exposure."),
        ("Interactive 1-to-5 Year Slider:", "Users drag the slider to simulate their exact trajectory over time, observing compounding biophysical degradation."),
        ("Side-by-Side Contrast:", "Directly contrasts the Unmitigated Trajectory (Red Card) against Preserved Homeostasis with AsthenoZero (Green Card)."),
        ("Compounding Biophysical Formulas:", "Simulates Meibomian duct atrophy %, Tear Break-Up Time (TBUT) decay, and intraocular ciliary tonic spasm burden."),
    ]
    for h, desc in twin_items:
        p_item = s9tf.add_paragraph()
        p_item.space_before = Pt(6)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: Embed actual screenshot and trajectory graph
    add_card(s9, 6.6, 1.7, 5.9, 5.2, border_color=COLOR_CORAL)
    add_image_safe(s9, "app_eye_twin_slider.jpg", 6.75, 1.85, width=5.6)
    add_image_safe(s9, "digital_eye_twin_trajectory.png", 6.75, 4.0, width=5.6)

    # =========================================================================
    # SLIDE 10: Behavioral Economics (Split: Rules + App Screenshot)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Behavioral Economics", "AsthenoCredits Economy & Strict Rehabilitation Protocol")

    # Left card: Economy rules
    add_card(s10, 0.8, 1.7, 5.5, 5.2)
    s10_box = s10.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.1), Inches(4.8))
    s10tf = s10_box.text_frame
    s10tf.word_wrap = True

    p = s10tf.paragraphs[0]
    p.text = "Physiologically-Gated Habit Enforcement:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    econ_items = [
        ("Branded AsthenoCredits Economy:", "Rebranded currency to align with Asthenopia mitigation. Users earn credits solely by performing verifiable clinical habits."),
        ("Earning Schedule:", "+15 🪙 Daily Habit Diary, +20 🪙 20-20-20 Micro-Break, +25 🪙 Vision Gym Exercise, +35 🪙 Webcam Blink Diagnostic."),
        ("Vault Protections:", "Spend 40 🪙 on Streak Shields to auto-protect missed days, or 50 🪙 to repair broken streaks."),
        ("The Strict Rehabilitation Protocol:", "Unlike consumer apps that allow cash bypasses, when your streak breaks and coins hit 0, bypass is locked. You must complete 3 physical therapy milestones to reinstate your streak!"),
    ]
    for h, desc in econ_items:
        p_item = s10tf.add_paragraph()
        p_item.space_before = Pt(6)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: Real screenshot of vault
    add_card(s10, 6.6, 1.7, 5.9, 5.2, border_color=COLOR_AMBER)
    add_image_safe(s10, "app_conditions_and_vault.jpg", 6.75, 1.85, width=5.6)

    # =========================================================================
    # SLIDE 11: 20-20-20 Smart Adaptive Break Suite (Visual 3-Tier Grid)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Pacing & Ergonomic Safeguards", "Smart AI Adaptive Pacing & Neuro-Acoustic Suite")

    tiers = [
        ("🔴 Intensive Corneal Recovery", "15m Focus • 5m Rest", "Automatically engaged when asthenopia fatigue score >= 60. Provides frequent micro-pauses to replenish tear film lipid layers.", COLOR_CORAL),
        ("🟡 Standard Micro-Pacing", "20m Focus • 3m Rest", "Standard 20-20-20 cadence for moderate fatigue scores (35–59). Disengages continuous intraocular ciliary accommodation.", COLOR_AMBER),
        ("🟢 Sustained Focus & Preventative", "25m Focus • 5m Rest", "Calibrated for low baseline fatigue (<35). Allows sustained deep focus while preserving long-term visual comfort.", COLOR_EMERALD),
    ]

    for i, (t_title, t_cadence, t_desc, t_color) in enumerate(tiers):
        x = 0.8 + (i * 4.0)
        add_card(s11, x, 1.7, 3.75, 3.3, border_color=t_color)
        tbox = s11.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(3.45), Inches(3.0))
        ttf = tbox.text_frame
        ttf.word_wrap = True

        p = ttf.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = t_color

        p_cad = ttf.add_paragraph()
        p_cad.text = t_cadence
        p_cad.font.size = Pt(14)
        p_cad.font.bold = True
        p_cad.font.color.rgb = COLOR_WHITE
        p_cad.space_before = Pt(4)

        p_desc = ttf.add_paragraph()
        p_desc.text = t_desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_MUTED
        p_desc.space_before = Pt(8)

    # Bottom feature card: Interlock & 432 Hz
    add_card(s11, 0.8, 5.2, 11.7, 1.7, border_color=COLOR_CYAN)
    bot_box = s11.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.5))
    btf = bot_box.text_frame
    btf.word_wrap = True

    p = btf.paragraphs[0]
    p.text = "🔒 AsthenoZero Strict Interlock & 432 Hz Alpha Acoustic Tone"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p_sub = btf.add_paragraph()
    p_sub.text = "• Strict Interlock: During rest breaks, pause and reset controls are disabled, enforcing uninterrupted 20-foot optical recovery without cheating.\n• 432 Hz Synthetic Tone: Generates zero-latency 432 Hz + 540 Hz harmonic sine waves via the browser Web Audio API for neuro-muscular ciliary muscle relaxation."
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = COLOR_WHITE
    p_sub.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: Vision Gym & Physical Therapy (5 Visual Drills)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Ophthalmic Physical Therapy", "Vision Gym: Animated Ocular Muscle Decompression")

    drills = [
        ("♾️ Figure-8 Pursuit", "Animated SVG infinity loop guides continuous circular tracking to decompress all 6 extraocular rectus muscles.", COLOR_CYAN),
        ("💧 Meibomian Squeeze", "4-phase isometric drill: 2s Close -> 2s Squeeze -> 2s Open -> 2s Rest to express stagnant tarsal lipid oils.", COLOR_EMERALD),
        ("🎯 Near-Far Switcher", "Rhythmically shifts optical gaze between near text and 20-foot distance to break tonic ciliary spasm.", COLOR_AMBER),
        ("🔥 Warm Palming", "Thermal palm heat (40°C) with light exclusion to induce dark photoreceptor recovery and retinal rest.", COLOR_CORAL),
        ("🧭 Compass Stretch", "8-direction cardinal gaze elongation to relieve chronic extraocular oculomotor muscle stiffness.", COLOR_CYAN),
    ]

    for i, (d_title, d_desc, d_color) in enumerate(drills):
        x = 0.8 + (i * 2.45)
        add_card(s12, x, 1.7, 2.3, 5.2, border_color=d_color)
        dbox = s12.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(2.0), Inches(4.8))
        dtf = dbox.text_frame
        dtf.word_wrap = True

        p = dtf.paragraphs[0]
        p.text = d_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = d_color

        p_desc = dtf.add_paragraph()
        p_desc.text = d_desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_WHITE
        p_desc.space_before = Pt(10)

    # =========================================================================
    # SLIDE 13: Clinical Pathology & Targeted Nutrition
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Biochemical Therapeutics", "Clinical Pathology & Targeted Nutritional Ophthalmology")

    add_card(s13, 0.8, 1.7, 5.6, 5.2, border_color=COLOR_CORAL)
    p13_box = s13.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    ptf13 = p13_box.text_frame
    ptf13.word_wrap = True

    p = ptf13.paragraphs[0]
    p.text = "Stratification of 5 Primary Eye Conditions:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CORAL

    c_items = [
        ("Meibomian Gland Dysfunction (MGD):", "Blink suppression causes meibum stagnation, gland plugging, and rapid tear break-up time (TBUT <5s)."),
        ("Accommodative Ciliary Spasm:", "Near-point convergence locks ciliary body in continuous spasm, resulting in brow ache and transient distance blur."),
        ("Contact Lens Micro-Friction Keratitis:", "Hydrophilic lens dehydration under screen air causes friction on corneal epithelium."),
        ("Convergence Insufficiency:", "Close mobile screens (<14 in) force steep downward gaze and medial rectus muscle fatigue."),
        ("Circadian Phototoxicity:", "HEV blue light suppresses pineal melatonin, truncating overnight corneal mitotic repair."),
    ]
    for h, desc in c_items:
        p_item = ptf13.add_paragraph()
        p_item.space_before = Pt(5)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_MUTED

    add_card(s13, 6.7, 1.7, 5.8, 5.2, border_color=COLOR_EMERALD)
    d13_box = s13.shapes.add_textbox(Inches(6.9), Inches(1.85), Inches(5.4), Inches(4.8))
    dtf13 = d13_box.text_frame
    dtf13.word_wrap = True

    p = dtf13.paragraphs[0]
    p.text = "Evidence-Based AREDS 2 & TFOS DEWS II Protocols:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    diet_items = [
        ("Omega-3 Fatty Acids (1,000–1,200 mg/day):", "Lowers the melting point of meibum lipids so oils flow smoothly over the cornea."),
        ("Macular Carotenoids (Lutein 10mg + Zeaxanthin 2mg):", "Internal blue-light filter absorbing high-energy visible wavelengths (450-480nm)."),
        ("Bioflavonoids & Anthocyanins:", "Wild blueberries & bilberries enhance microcapillary blood flow to extraocular muscles."),
        ("Systemic Hydration Protocol (2.5–3.0 L/day):", "Prevents hyperosmolar tear film breakdown and burning sensations."),
        ("Magnesium Glycinate (200–300 mg):", "Promotes nocturnal corneal epithelial repair and relaxes hyper-contracted muscles."),
    ]
    for h, desc in diet_items:
        p_item = dtf13.add_paragraph()
        p_item.space_before = Pt(5)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 14: Competitive Advantage Matrix (Contrast Table)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Market Differentiation", "AsthenoZero vs Existing Commercial Solutions")

    add_card(s14, 0.8, 1.7, 11.7, 5.2)
    s14_box = s14.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(4.8))
    s14tf = s14_box.text_frame
    s14tf.word_wrap = True

    p = s14tf.paragraphs[0]
    p.text = "Feature-by-Feature Competitor Benchmark:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    matrix_rows = [
        ("Predictive ML Risk Scoring (CV MAE 2.40)", "AsthenoZero: YES (Trained L2 Ridge)", "Competitors: NONE (Arbitrary scores or static surveys)"),
        ("Incomplete vs Complete Blink Ratio & Pump %", "AsthenoZero: YES (EAR min formulation)", "Competitors: NONE (Binary open/close count only)"),
        ("Zero-Hardware Screen Distance & Posture", "AsthenoZero: YES (Canthal Triangulation)", "Competitors: NONE (Requires LiDAR or unmonitored)"),
        ("Silent Asthenopia Divergence Index (SO-DI)", "AsthenoZero: YES (Multi-modal cross-analysis)", "Competitors: NONE (No psychometric-biometric pairing)"),
        ("Interactive 5-Year Digital Eye Twin", "AsthenoZero: YES (1-5 Year Simulator)", "Competitors: NONE (Zero long-term predictive models)"),
        ("Habit Economy with Strict Physiological Lock", "AsthenoZero: YES (AsthenoCredits + Drills)", "Competitors: NONE (Cash bypass, ad views, or snoozes)"),
        ("Ophthalmic Vision Gym (SVG Visual Coaches)", "AsthenoZero: YES (5 Guided Animated Drills)", "Competitors: NONE (Static bulleted text tips)"),
        ("Zero-Retention Local RAM Privacy Architecture", "AsthenoZero: YES (0 frames stored)", "Competitors: Varies (Often streams video to cloud)"),
    ]

    for f_name, az_val, comp_val in matrix_rows:
        p_row = s14tf.add_paragraph()
        p_row.space_before = Pt(5)
        r_f = p_row.add_run()
        r_f.text = f"• {f_name}: "
        r_f.font.bold = True
        r_f.font.size = Pt(10.5)
        r_f.font.color.rgb = COLOR_WHITE

        r_az = p_row.add_run()
        r_az.text = f"[{az_val}]  "
        r_az.font.bold = True
        r_az.font.size = Pt(10)
        r_az.font.color.rgb = COLOR_EMERALD

        r_comp = p_row.add_run()
        r_comp.text = f"vs  {comp_val}"
        r_comp.font.size = Pt(9.5)
        r_comp.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 15: Deployment, Privacy & Conclusion
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Validation & Live Deployment", "Production Status, Privacy Integrity & Future Horizons")

    add_card(s15, 0.8, 1.7, 6.0, 5.2, border_color=COLOR_EMERALD)
    s15_box = s15.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.6), Inches(4.8))
    s15tf = s15_box.text_frame
    s15tf.word_wrap = True

    p = s15tf.paragraphs[0]
    p.text = "🚀 Live Production & Open Source Access:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD

    end_items = [
        ("Live Cloud URL:", "Fully deployed on Streamlit Community Cloud: https://asthenozero.streamlit.app/"),
        ("Open-Source Repository:", "Publicly available on GitHub with complete source code and documentation: https://github.com/Akansha-695/AsthenoZero.git"),
        ("Zero-Retention Privacy:", "All frames processed in volatile RAM. Zero pictures, videos, or landmark vectors are written to disk or sent to servers (100% HIPAA/GDPR compliant)."),
        ("Patent Novelty Viability:", "Formulated across 7 distinct inventive steps for provisional patent application."),
        ("Future Roadmap:", "Smart Home IoT auto-dimming room lights and real-time pupillometric sympathetic stress tracking."),
    ]
    for h, desc in end_items:
        p_item = s15tf.add_paragraph()
        p_item.space_before = Pt(7)
        r1 = p_item.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p_item.add_run()
        r2.text = desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED

    # Right side: Summary Badges Card
    add_card(s15, 7.1, 1.7, 5.4, 5.2, border_color=COLOR_CYAN)
    badge_box = s15.shapes.add_textbox(Inches(7.3), Inches(1.85), Inches(5.0), Inches(4.8))
    btf15 = badge_box.text_frame
    btf15.word_wrap = True

    p = btf15.paragraphs[0]
    p.text = "💎 Platform Summary by the Numbers:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    badges = [
        ("468 Points", "MediaPipe 3D Facial Mesh Topology"),
        ("MAE 2.40", "Grouped 5-Fold Cross-Validation Accuracy"),
        ("< 0.70x EAR", "Complete vs Incomplete Blink Threshold"),
        ("1 to 5 Years", "Interactive Digital Eye Twin Horizon"),
        ("5 Drills", "Animated SVG Ophthalmic Vision Gym"),
        ("432 Hz", "Synthetic Alpha Resonance Audio Waves"),
        ("0 Frames", "Stored (Absolute Client-Side Privacy)"),
    ]
    for num, lbl in badges:
        p_b = btf15.add_paragraph()
        p_b.space_before = Pt(8)
        r_n = p_b.add_run()
        r_n.text = f"{num}  "
        r_n.font.bold = True
        r_n.font.size = Pt(14)
        r_n.font.color.rgb = COLOR_WHITE

        r_l = p_b.add_run()
        r_l.text = lbl
        r_l.font.size = Pt(10)
        r_l.font.color.rgb = COLOR_MUTED

    return prs


def save_deck(prs):
    """Saves presentation deck with fallback if user has PowerPoint open."""
    paths_to_save = [
        OUTPUT_DIR / "AsthenoZero_Executive_Deck.pptx",
        OUTPUT_DIR / "AsthenoZero_Presentation.pptx",
        PROJECT_ROOT / "AsthenoZero_Executive_Deck.pptx",
        PROJECT_ROOT / "AsthenoZero_Presentation.pptx",
    ]
    for p in paths_to_save:
        try:
            prs.save(str(p))
            print(f"Saved: {p}")
        except PermissionError:
            print(f"Notice: {p.name} is currently open in PowerPoint (locked).")
            fallback = p.parent / f"{p.stem}_updated.pptx"
            try:
                prs.save(str(fallback))
                print(f"Saved to fallback: {fallback}")
            except Exception as e:
                print(f"Could not save fallback {fallback}: {e}")


if __name__ == "__main__":
    prs = build_deck()
    save_deck(prs)

