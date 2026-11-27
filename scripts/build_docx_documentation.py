"""Convert DOCUMENTATION.md into a beautifully styled, professional Word (.docx) document."""

from __future__ import annotations

import re
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MD_PATH = PROJECT_ROOT / "DOCUMENTATION.md"
DOCX_OUT_PATH = PROJECT_ROOT / "DOCUMENTATION.docx"
DOCX_OUT_DOCS = PROJECT_ROOT / "output" / "docs" / "AsthenoZero_Documentation.docx"

# Color Palette
HEX_DARK_NAVY = "0F172A"     # Headers / Major Titles
HEX_PRIMARY_BLUE = "1E3A8A"  # Heading 2
HEX_ACCENT_BLUE = "2563EB"   # Heading 3 / Highlights
HEX_BODY = "1E293B"          # Body text
HEX_MUTED = "64748B"         # Captions / Footers
HEX_BG_LIGHT = "F8FAFC"      # Alternate table row
HEX_BORDER = "CBD5E1"        # Table borders
HEX_CODE_BG = "F1F5F9"       # Code background

COLOR_DARK_NAVY = RGBColor(15, 23, 42)
COLOR_PRIMARY_BLUE = RGBColor(30, 58, 138)
COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)
COLOR_BODY = RGBColor(30, 41, 59)
COLOR_MUTED = RGBColor(100, 116, 139)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="{top}" w:type="dxa"/>'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'  <w:left w:w="{left}" w:type="dxa"/>'
        f'  <w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_cell_shading(cell, hex_color: str):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_table_borders(table, border_color="CBD5E1"):
    """Set clean subtle borders for an entire table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def format_inline_text(paragraph, text: str, default_font="Calibri", default_size=10.5, default_color=COLOR_BODY):
    """Parses basic markdown bold, italic, and code spans inside text."""
    # Pattern to match bold-italic, bold, italic, code, or plain text
    # e.g. **bold**, *italic*, `code`, and plain segments
    tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**') and len(token) >= 4:
            run = paragraph.add_run(token[2:-2])
            run.font.name = default_font
            run.font.size = Pt(default_size)
            run.font.bold = True
            run.font.color.rgb = default_color
        elif token.startswith('*') and token.endswith('*') and len(token) >= 2:
            run = paragraph.add_run(token[1:-1])
            run.font.name = default_font
            run.font.size = Pt(default_size)
            run.font.italic = True
            run.font.color.rgb = default_color
        elif token.startswith('`') and token.endswith('`') and len(token) >= 2:
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(default_size - 0.5)
            run.font.color.rgb = COLOR_PRIMARY_BLUE
        else:
            run = paragraph.add_run(token)
            run.font.name = default_font
            run.font.size = Pt(default_size)
            run.font.color.rgb = default_color


def build_docx():
    print(f"Reading markdown from: {MD_PATH}")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = docx.Document()

    # Configure Margins: 1 inch (72pt)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("AsthenoZero • Precision Ocular Ergonomics Suite v2.5")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED

        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        frun = fp.add_run("Lead Researcher: Akansha Kashyap  •  CONFIDENTIAL & INVESTIGATIONAL")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = COLOR_MUTED

    # Document Styles
    styles = doc.styles
    normal_style = styles["Normal"]
    normal_font = normal_style.font
    normal_font.name = "Calibri"
    normal_font.size = Pt(10.5)
    normal_font.color.rgb = COLOR_BODY

    # Process Lines
    lines = md_text.splitlines()
    idx = 0
    total_lines = len(lines)

    in_code_block = False
    code_lines = []
    code_lang = ""

    in_table = False
    table_lines = []

    # Title Banner
    # We detect the first H1 and H2
    title_text = "AsthenoZero: Precision Ocular Ergonomics & Digital Asthenopia Suite"
    subtitle_text = "Complete Technical, Clinical & Architectural Documentation"

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    t_run = p_title.add_run(title_text)
    t_run.font.name = "Calibri"
    t_run.font.size = Pt(22)
    t_run.font.bold = True
    t_run.font.color.rgb = COLOR_DARK_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    s_run = p_sub.add_run(subtitle_text)
    s_run.font.name = "Calibri"
    s_run.font.size = Pt(12.5)
    s_run.font.bold = True
    s_run.font.color.rgb = COLOR_ACCENT_BLUE

    # Metadata Card (Table Box)
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, border_color="E2E8F0")

    metadata_items = [
        ("Lead Author & Researcher:", "Akansha Kashyap"),
        ("LinkedIn Profile:", "https://www.linkedin.com/in/akansha-kashyap-b6a32b362"),
        ("System Classification:", "Digital Health / Software as a Medical Device (SaMD) Prototype"),
        ("Date of Release & Version:", "2026 • Release v2.5 Pro"),
        ("License & Copyright:", "Permissive Open-Source License © 2026 Akansha Kashyap"),
    ]

    col_widths = (Inches(2.2), Inches(4.3))
    for r_idx, (k, v) in enumerate(metadata_items):
        row = meta_table.rows[r_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width, cell_v.width = col_widths

        set_cell_margins(cell_k, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_v, top=60, bottom=60, left=100, right=100)

        set_cell_shading(cell_k, HEX_BG_LIGHT)
        set_cell_shading(cell_v, "FFFFFF")

        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_before = Pt(0)
        pk.paragraph_format.space_after = Pt(0)
        rk = pk.add_run(k)
        rk.font.name = "Calibri"
        rk.font.size = Pt(9.5)
        rk.font.bold = True
        rk.font.color.rgb = COLOR_PRIMARY_BLUE

        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_before = Pt(0)
        pv.paragraph_format.space_after = Pt(0)
        rv = pv.add_run(v)
        rv.font.name = "Calibri"
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = COLOR_BODY

    # Add space after metadata
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(8)
    p_sep.paragraph_format.space_after = Pt(8)

    # Skip initial lines in MD that contain title and metadata
    # We start reading from line 10
    start_line_idx = 0
    for i, line in enumerate(lines[:15]):
        if line.strip().startswith("## 1. Executive Summary"):
            start_line_idx = i
            break

    while idx < total_lines:
        if idx < start_line_idx:
            idx += 1
            continue

        raw_line = lines[idx]
        line = raw_line.strip()

        # Handle code blocks
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
                code_lines = []
                idx += 1
                continue
            else:
                in_code_block = False
                # Render accumulated code block
                block_text = "\n".join(code_lines)
                tbl_code = doc.add_table(rows=1, cols=1)
                tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(tbl_code, border_color="CBD5E1")
                c = tbl_code.cell(0, 0)
                c.width = Inches(6.5)
                set_cell_shading(c, HEX_CODE_BG)
                set_cell_margins(c, top=100, bottom=100, left=140, right=140)

                p_code = c.paragraphs[0]
                p_code.paragraph_format.space_before = Pt(0)
                p_code.paragraph_format.space_after = Pt(0)
                p_code.paragraph_format.line_spacing = 1.05

                r = p_code.add_run(block_text)
                r.font.name = "Consolas"
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_DARK_NAVY

                # Spacing paragraph
                sp = doc.add_paragraph()
                sp.paragraph_format.space_before = Pt(4)
                sp.paragraph_format.space_after = Pt(4)

                idx += 1
                continue

        if in_code_block:
            code_lines.append(raw_line)
            idx += 1
            continue

        # Handle Markdown Tables
        if "|" in line and (line.startswith("|") or line.endswith("|")):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
            idx += 1
            continue
        elif in_table:
            # End of table
            in_table = False
            # Parse table_lines
            rows_data = []
            for tl in table_lines:
                # Remove leading/trailing pipe
                content = tl.strip()
                if content.startswith("|"):
                    content = content[1:]
                if content.endswith("|"):
                    content = content[:-1]
                cells = [c.strip() for c in content.split("|")]
                # Skip divider row e.g. :--- | :---:
                if all(re.match(r"^:?-+:?$", c) for c in cells):
                    continue
                rows_data.append(cells)

            if rows_data:
                num_cols = max(len(r) for r in rows_data)
                tbl = doc.add_table(rows=len(rows_data), cols=num_cols)
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(tbl, border_color="CBD5E1")

                for r_i, r_data in enumerate(rows_data):
                    is_header = (r_i == 0)
                    for c_i in range(num_cols):
                        cell = tbl.cell(r_i, c_i)
                        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                        if is_header:
                            set_cell_shading(cell, HEX_PRIMARY_BLUE)
                        else:
                            bg = HEX_BG_LIGHT if r_i % 2 == 1 else "FFFFFF"
                            set_cell_shading(cell, bg)

                        cell_text = r_data[c_i] if c_i < len(r_data) else ""
                        p_cell = cell.paragraphs[0]
                        p_cell.paragraph_format.space_before = Pt(0)
                        p_cell.paragraph_format.space_after = Pt(0)

                        if is_header:
                            run = p_cell.add_run(cell_text)
                            run.font.name = "Calibri"
                            run.font.size = Pt(9.5)
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                        else:
                            format_inline_text(p_cell, cell_text, default_size=9.0)

                sp = doc.add_paragraph()
                sp.paragraph_format.space_before = Pt(4)
                sp.paragraph_format.space_after = Pt(4)

            table_lines = []
            # Do not continue, process the current line

        # Blank line
        if not line:
            idx += 1
            continue

        # Horizontal Rule
        if line in ["---", "***", "___"]:
            # Subtle divider
            p_hr = doc.add_paragraph()
            p_hr.paragraph_format.space_before = Pt(6)
            p_hr.paragraph_format.space_after = Pt(6)
            idx += 1
            continue

        # Headings
        if line.startswith("## "):
            h_text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = "Calibri"
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = COLOR_DARK_NAVY
            idx += 1
            continue

        if line.startswith("### "):
            h_text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(11)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = "Calibri"
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_PRIMARY_BLUE
            idx += 1
            continue

        if line.startswith("#### "):
            h_text = line[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(h_text)
            r.font.name = "Calibri"
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_ACCENT_BLUE
            idx += 1
            continue

        # Blockquote / Alert
        if line.startswith(">"):
            q_text = line[1:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(4)
            format_inline_text(p, q_text, default_color=COLOR_MUTED)
            idx += 1
            continue

        # Bullet List Items
        if re.match(r"^[-*+]\s+", line):
            b_text = re.sub(r"^[-*+]\s+", "", line)
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            format_inline_text(p, b_text)
            idx += 1
            continue

        # Nested Bullet List Items (indented with 2-4 spaces)
        if re.match(r"^\s{2,4}[-*+]\s+", raw_line):
            b_text = re.sub(r"^\s{2,4}[-*+]\s+", "", raw_line).strip()
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            format_inline_text(p, b_text)
            idx += 1
            continue

        # Numbered List Items
        if re.match(r"^\d+\.\s+", line):
            n_text = re.sub(r"^\d+\.\s+", "", line)
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            format_inline_text(p, n_text)
            idx += 1
            continue

        # Normal Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        format_inline_text(p, line)
        idx += 1

    # Ensure output directories exist
    DOCX_OUT_DOCS.parent.mkdir(parents=True, exist_ok=True)

    # Save to both locations
    print(f"Saving DOCX to: {DOCX_OUT_PATH}")
    doc.save(str(DOCX_OUT_PATH))

    print(f"Saving duplicate copy to: {DOCX_OUT_DOCS}")
    doc.save(str(DOCX_OUT_DOCS))

    print("Word Document Generation Complete!")


if __name__ == "__main__":
    build_docx()
