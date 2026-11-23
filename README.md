# AsthenoZero &bull; Precision Ophthalmic Suite v2.5 Pro

**AsthenoZero** is a state-of-the-art precision digital health suite for quantifying, monitoring, and mitigating digital eye strain (asthenopia) and ocular surface micro-trauma.

The v2.5 release integrates an ultra-modern clinical dashboard, real-time computer vision blink diagnostics, Altair-powered longitudinal telemetry, synthetic neuro-ocular audio chimes, guided ocular muscle physical therapy, and an advanced **OcuCoins Habit Credit Economy & Strict Rehabilitation Protocol**.

The platform is investigational and educational. It does not replace formal examination by a licensed ophthalmologist or optometrist.

> 📖 **Full System Documentation:** For comprehensive technical, clinical, and architectural details (including machine learning validation, computer vision algorithms, patent novelty claims, and nutritional ophthalmology), read the complete [DOCUMENTATION.md](file:///d:/Eye-Risk/DOCUMENTATION.md).

---

## Key Features

1. **Clinical Risk Assessment & Interactive Vector Gauge**
   - Estimates exploratory digital eye strain severity (0–15) using a trained L2 Ridge regression model.
   - Real-time SVG semi-circle clinical risk meter with color-coded risk bands: *Low Risk*, *Mild Discomfort*, *Moderate Strain*, and *High Digital Strain*.
   - Factor attribution engine: identifies behavioral risk drivers vs. protective visual habits.
   - Cohort benchmarking against N=139 survey participants.

2. **Tailored Evidence-Based Clinical Action Plan**
   - Automatically generates prioritized interventions across Workstation Ergonomics, 20-20-20 Micro-Breaks, Ocular Surface & Blinking Mechanics, and Circadian Sleep Hygiene.
   - **One-Click Clinical Assessment Report**: Export a publication-quality, printable HTML summary report with vector gauges, telemetry tables, and care recommendations (printable to PDF with `Ctrl+P`).

3. **Live Blink Diagnostic Suite (Webcam Computer Vision)**
   - Powered by Google MediaPipe Face Mesh in-memory video stream.
   - 5-second resting baseline calibration followed by a standardized 60-second reading task.
   - Rich clinical reading passage with customizable typography sizing and high-contrast night mode.
   - Quantitative blink frequency comparison against clinical baselines (resting 15–20 vs screen reading 5–8 blinks/min).
   - Optional anonymous paired-data CSV export for clinical research.

4. **OcuCoins Credit Economy & Strict Rehabilitation Protocol**
   - Daily habit streak maintenance coupled with earning **OcuCoins** (`+15` for diary logging, `+20` for break timers, `+25` for vision gym drills, `+35` for blink diagnostics).
   - Streak Shields & emergency streak repairs using accumulated coins.
   - **Strict Ocular Rehabilitation Protocol**: If a user's streak breaks and their coin vault is depleted (0 coins), bypass purchases are locked. The user must fulfill all 3 therapeutic recovery tasks (Vision Gym exercise, 20-20-20 micro-break, and calibrated 60s blink diagnostic) to reinstate their streak.

5. **Longitudinal Habit Diary & Altair Analytics**
   - Daily logging of screen hours, sleep duration, micro-breaks, and discomfort scores.
   - Visual Wellness Composite Index (0–100) and multi-metric KPI tracking.
   - Interactive Altair charts: habit exposure timeline, rolling trends, and screen-time vs symptom severity regression scatter plots.
   - CSV export and historical CSV import with schema validation.

6. **20-20-20 Smart Break Timer with Audio Chimes**
   - Ophthalmic interval presets: Standard 20-20-20, Pomodoro Classic (25/5), Deep Focus (50/10), and Custom.
   - Large clinical digital display with visual pulsing animation during active sessions.
   - Native Web Audio API synthetic bell chimes on interval completion (no external audio files required).
   - Guided 4-step micro-break exercises: 20-Foot Gaze, Conscious Blinking, Warm Palming, and Cervical Decompression.

7. **Ophthalmic Eye Relaxation Studio & Vision Gym**
   - Interactive guided exercise studio with animated visual tracking coaches.
   - **Figure-8 Smooth Pursuit**: Animated SVG infinity loop to decompress extraocular muscles.
   - **Meibomian Blink & Squeeze**: 4-phase rhythm drill to express corneal lipid oils.
   - **Near-Far Accommodation Switcher**: Rhythmic gaze cycling to relieve ciliary muscle spasm.
   - **Thermal Warm Palming & Compass Gaze Stretches**: Complete retinal photoreceptor rest.
   - Daily exercise completion tracker with reward chimes.

8. **Care Guide & Clinical Research Telemetry**
   - Comprehensive ergonomic setup rules, display calibration tips, and peer-reviewed ophthalmic citations.
   - Interactive Workstation Ergonomic Readiness Audit (0–100%).
   - Urgent Ophthalmic Warning red flag protocol for symptoms requiring immediate medical evaluation.
   - Grouped 5-fold cross-validation transparency tables.

---

## 1. Quick Start

Ensure Python 3.13 is installed, then run from PowerShell in `D:\Eye-Risk`:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Open the local server URL displayed in your terminal (typically `http://localhost:8501`).

---

## 2. Project Architecture

```
Eye-Risk/
├── app.py                          # Main Streamlit v2.0 clinical application
├── models/
│   ├── eyeguard_ridge.joblib       # Trained Ridge regression pipeline & CV metrics
│   └── face_landmarker.task        # MediaPipe Vision Landmarker model asset
├── data/
│   ├── raw/survey_responses.xlsx   # Survey workbook (139 responses)
│   └── processed/responses_clean.csv
├── src/eyeguard/
│   ├── __init__.py                 # Public package exports
│   ├── theme.py                    # Clinical & analytical CSS theme & SVG risk meter
│   ├── recommendations.py          # Evidence-based clinical action plan engine
│   ├── sound_alerts.py             # Web Audio API synthetic notification chimes
│   ├── eye_exercises.py            # Ophthalmic relaxation exercises & animated visual coach
│   ├── gamification.py             # OcuCoins credit economy & strict rehabilitation protocol
│   ├── analytics.py                # Altair visualizations, KPIs & cohort percentiles
│   ├── report_generator.py         # Printable clinical summary HTML/PDF generator
│   ├── blink_monitor.py            # MediaPipe real-time blink detection & EAR calculation
│   ├── care_content.py             # Ophthalmic guidance & peer-reviewed sources
│   ├── prepare_data.py             # Data hygiene & survey preprocessing
│   ├── analyze_data.py             # Descriptive statistics on survey data
│   └── train_baseline.py           # Grouped 5-fold CV & Ridge regression training
├── output/pdf/
│   └── eyeguard_user_manual.pdf    # Comprehensive user manual
└── scripts/
    └── build_user_manual.py        # ReportLab PDF documentation builder
```

---

## Camera and Data Privacy

- **Zero Frame Storage**: Webcam frames are processed in-memory directly on the local Python server for landmark tracking and are immediately discarded. Frames are never stored, written to disk, or sent to cloud APIs.
- **Local Isolation**: Diary records and paired research entries stay inside your local browser session memory until you explicitly choose to export them as CSV.
