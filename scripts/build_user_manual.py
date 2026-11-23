"""Build the printable EyeGuard user guide from shared in-app care content."""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from eyeguard.care_content import CARE_SECTIONS, CARE_SOURCES, URGENT_GUIDANCE  # noqa: E402


OUTPUT_PATH = PROJECT_ROOT / "output" / "pdf" / "eyeguard_user_manual.pdf"
NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#168C86")
PALE = colors.HexColor("#EAF5F4")
MUTED = colors.HexColor("#526477")


class ManualDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str) -> None:
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=0.72 * inch,
            rightMargin=0.72 * inch,
            topMargin=0.72 * inch,
            bottomMargin=0.62 * inch,
            title="EyeGuard AI User Guide and Screen-Care Tips",
            author="EyeGuard AI Project",
            subject="How to use the EyeGuard AI project prototype",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="main",
        )
        self.addPageTemplates([PageTemplate(id="pages", frames=[frame], onPage=self._draw_page)])

    @staticmethod
    def _draw_page(canvas, doc) -> None:
        canvas.saveState()
        width, height = letter
        canvas.setFillColor(NAVY)
        canvas.rect(0, height - 0.18 * inch, width, 0.18 * inch, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#DCE5EA"))
        canvas.line(doc.leftMargin, 0.48 * inch, width - doc.rightMargin, 0.48 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 0.31 * inch, "EyeGuard AI | Educational project guide")
        canvas.drawRightString(width - doc.rightMargin, 0.31 * inch, f"Page {doc.page}")
        canvas.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "EyeGuardTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=27,
            leading=31, textColor=NAVY, alignment=TA_LEFT, spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "EyeGuardSubtitle", parent=base["Normal"], fontName="Helvetica", fontSize=12,
            leading=17, textColor=MUTED, spaceAfter=16,
        ),
        "heading": ParagraphStyle(
            "EyeGuardHeading", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=16,
            leading=20, textColor=NAVY, spaceBefore=8, spaceAfter=7, keepWithNext=True,
        ),
        "subheading": ParagraphStyle(
            "EyeGuardSubheading", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=11,
            leading=14, textColor=TEAL, spaceBefore=5, spaceAfter=4, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "EyeGuardBody", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2,
            leading=13.3, textColor=NAVY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "EyeGuardBullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.0,
            leading=12.7, leftIndent=12, firstLineIndent=-9, textColor=NAVY, spaceAfter=4,
        ),
        "callout": ParagraphStyle(
            "EyeGuardCallout", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=9.4,
            leading=13.6, textColor=NAVY, backColor=PALE, borderColor=TEAL,
            borderWidth=0.7, borderPadding=8, spaceBefore=4, spaceAfter=9,
        ),
        "source": ParagraphStyle(
            "EyeGuardSource", parent=base["BodyText"], fontName="Helvetica", fontSize=8.2,
            leading=11.5, textColor=MUTED, leftIndent=10, firstLineIndent=-8, spaceAfter=4,
        ),
        "center": ParagraphStyle(
            "EyeGuardCenter", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10,
            leading=14, alignment=TA_CENTER, textColor=TEAL, spaceAfter=10,
        ),
    }


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), style)


def bullet(text: str, styles: dict) -> Paragraph:
    return paragraph(f"- {text}", styles["bullet"])


def link_paragraph(label: str, url: str, styles: dict) -> Paragraph:
    safe_url = escape(url, quote=True)
    safe_label = escape(label)
    return Paragraph(
        f'- <link href="{safe_url}" color="#168C86">{safe_label}</link>',
        styles["source"],
    )


def build_manual(output_path: Path = OUTPUT_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    story = [
        Spacer(1, 0.38 * inch),
        paragraph("EyeGuard AI", styles["title"]),
        paragraph("User guide and screen-care tips", styles["subtitle"]),
        paragraph(
            "A practical guide to the survey estimate, live blink test, habit diary, and break timer.",
            styles["body"],
        ),
        paragraph(
            "Educational project only. EyeGuard AI does not diagnose eye conditions or replace an eye examination.",
            styles["callout"],
        ),
        paragraph("1. Getting started", styles["heading"]),
        paragraph("Open the EyeGuard app in your browser after the project is running on your computer.", styles["body"]),
        bullet("Survey estimate: enter broad habit categories to see an estimate of the project's exploratory symptom score.", styles),
        bullet("Live blink test: opt in to the camera, press Start in the camera widget, and then begin the calibrated test.", styles),
        bullet("Habit diary: add a daily entry. Download its CSV if you want to keep it after the app session ends.", styles),
        bullet("Break timer: choose a focus or break interval and start the countdown that fits your routine.", styles),
        paragraph("2. Live blink test", styles["heading"]),
        paragraph(
            "The test waits for a visible face, uses about 5 seconds to calibrate eye landmarks, and then counts blinks during a 60-second reading passage. Sit comfortably, keep your face centered, use even front lighting, and read at a natural pace.",
            styles["body"],
        ),
        bullet("The result is an estimated blink count per minute for that reading task and session only.", styles),
        bullet("Tracking coverage describes how often the face was visible to the detector. It is not medical confidence.", styles),
        bullet("If tracking is limited, adjust lighting and camera position, keep both eyes visible, and repeat only if you want to.", styles),
        PageBreak(),
        paragraph("Using your results and data", styles["heading"]),
        paragraph("3. Survey score and model", styles["subheading"]),
        paragraph(
            "The survey score adds five self-reported symptom answers coded Never=0, Sometimes=1, Often=2, Always=3. The total ranges from 0 to 15 and was created for this project; it is not a validated clinical scale. The model's grouped validation error was about 2.40 points on that scale, only a modest improvement over a mean-only baseline. Do not interpret the estimate as a diagnosis or a personal medical risk category.",
            styles["body"],
        ),
        paragraph("4. Habit diary and trends", styles["subheading"]),
        paragraph(
            "Diary entries are kept in the current app session. Export the CSV to save a copy on your device. In a later session, import that CSV to continue the chart. The charts summarize self-reported entries and do not establish cause and effect.",
            styles["body"],
        ),
        paragraph("5. Optional paired-data export", styles["subheading"]),
        paragraph(
            "Adults can choose to create a CSV row pairing a blink result with broad habit categories and symptom answers. This is opt-in, requires a separate consent checkbox, and is not uploaded by EyeGuard. The app does not collect names or save camera frames. Save and share the exported file only if you choose to participate; new records require appropriate consent and review before research use.",
            styles["body"],
        ),
        paragraph("6. Camera and privacy", styles["subheading"]),
        bullet("Camera access begins only after you opt in and start the camera widget.", styles),
        bullet("Frames are processed by the app's Python server for landmark tracking and are not recorded or saved by EyeGuard.", styles),
        bullet("When run on localhost, the Python server is on your computer. A hosted app receives the live camera stream; use only a trusted, secure deployment.", styles),
        bullet("Diary and paired-data entries stay in session memory until exported. Avoid adding identifying information.", styles),
        paragraph("Quick troubleshooting", styles["subheading"]),
        bullet("No camera preview: start the camera widget, allow browser camera access, and use the local app address.", styles),
        bullet("Weak tracking: add even front lighting, move closer, center your face, and keep both eyes visible.", styles),
        bullet("Model download fails: check the app computer's internet access, then restart the app and try again.", styles),
        bullet("Need to stop camera use: press Stop in the camera widget or uncheck the camera-consent box.", styles),
        paragraph("Before sharing an optional export", styles["subheading"]),
        bullet("Review the CSV contents and remove the file if you no longer want to keep it.", styles),
        bullet("The app does not transmit exports. Only share a file if you have chosen to contribute and your project has the right consent process.", styles),
        PageBreak(),
        paragraph("Everyday screen-care tips", styles["heading"]),
        paragraph(
            "These general comfort suggestions are not a treatment plan. Choose what works for you and stop an activity if it worsens discomfort.",
            styles["body"],
        ),
    ]

    for section_title, tips in CARE_SECTIONS:
        story.append(paragraph(section_title, styles["subheading"]))
        story.extend(bullet(tip, styles) for tip in tips)

    story.append(paragraph("When to get help", styles["heading"]))
    story.extend(bullet(item, styles) for item in URGENT_GUIDANCE)
    story.append(paragraph("References", styles["heading"]))
    story.append(paragraph("The health tips are based on general patient guidance. Blink tracking follows a published facial-landmark approach; it is not a clinical test.", styles["body"]))
    for label, url in CARE_SOURCES:
        story.append(link_paragraph(label, url, styles))

    doc = ManualDocTemplate(str(output_path))
    doc.build(story)
    return output_path


if __name__ == "__main__":
    print(f"Created: {build_manual()}")
