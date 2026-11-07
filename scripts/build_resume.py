"""Build an ATS-friendly single-column resume (PDF + DOCX) from a content JSON file.

Usage: python scripts/build_resume.py content.json out.pdf out.docx

The PDF is built directly with reportlab (selectable text, no LibreOffice needed).
Page 1 is rendered to page1.png next to the DOCX for a visual check.
See examples/content.example.json for the schema.
"""
import json
import os
import sys
from xml.sax.saxutils import escape as e

import docx
import pymupdf
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Inches, Pt
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, HRFlowable, Paragraph, SimpleDocTemplate, Spacer

content_path, pdf_path, docx_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(content_path) as f:
    C = json.load(f)

NAME, CONTACT, SUMMARY, SKILLS = C["name"], C["contact"], C["summary"], C["skills"]
EXP, EDU, ADDL = C["experience"], C["education"], C["additional"]
FS = C.get("font_size", 10)

# --- PDF ---
base = ParagraphStyle("b", fontName="Helvetica", fontSize=FS, leading=FS * 1.14)
name = ParagraphStyle("n", parent=base, fontName="Helvetica-Bold", fontSize=15, leading=18, alignment=TA_CENTER)
ctr = ParagraphStyle("c", parent=base, alignment=TA_CENTER)
head = ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=11, leading=13, spaceBefore=4, spaceAfter=1)
bul = ParagraphStyle("bl", parent=base, leftIndent=12, bulletIndent=2)
W = letter[0] - 1.0 * inch


def line(left, right, bold=True):
    """One line with left text and a right-aligned date, no tables."""
    class L(Flowable):
        def wrap(self, aw, ah):
            return (aw, FS * 1.3)

        def draw(self):
            c = self.canv
            c.setFont("Helvetica-Bold" if bold else "Helvetica", FS)
            c.drawString(0, 3, left)
            c.setFont("Helvetica", FS)
            c.drawRightString(W, 3, right)
    return L()


s = [Paragraph(e(NAME), name), Paragraph(e(CONTACT), ctr)]


def H(t):
    s.extend([Paragraph(t, head), HRFlowable(width="100%", thickness=0.6, spaceAfter=3)])


H("SUMMARY")
s.append(Paragraph(e(SUMMARY), base))
H("SKILLS")
s.append(Paragraph(e(SKILLS), base))
H("EXPERIENCE")
for i, job in enumerate(EXP):
    if i:
        s.append(Spacer(1, 2))
    s.append(line(job["title"], job["dates"]))
    for b in job["bullets"]:
        s.append(Paragraph(e(b), bul, bulletText="•"))
H("EDUCATION")
for ed in EDU:
    s.append(line(ed["school"], ed["location"]))
    s.append(line(ed["degree"], ed["dates"], bold=False))
H("ADDITIONAL")
for a in ADDL:
    s.append(Paragraph(e(a), bul, bulletText="•"))

doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                        topMargin=0.4 * inch, bottomMargin=0.4 * inch, title=f"{NAME} - Resume", author=NAME)
doc.build(s)

# --- DOCX ---
d = docx.Document()
st = d.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(FS)
for sec in d.sections:
    sec.left_margin = sec.right_margin = Inches(0.6)
    sec.top_margin = sec.bottom_margin = Inches(0.5)


def P(text="", bold=False, size=None, center=False, style=None):
    p = d.add_paragraph(style=style)
    r = p.add_run(text)
    r.bold = bold
    if size:
        r.font.size = Pt(size)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    return p


def TL(left, right, bold=True):
    p = d.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.3), WD_TAB_ALIGNMENT.RIGHT)
    a = p.add_run(left)
    a.bold = bold
    p.add_run("\t" + right)
    p.paragraph_format.space_after = Pt(0)


P(NAME, True, 15, True)
P(CONTACT, center=True)
for title, body in (("SUMMARY", SUMMARY), ("SKILLS", SKILLS)):
    P(title, True, 11)
    P(body)
P("EXPERIENCE", True, 11)
for job in EXP:
    TL(job["title"], job["dates"])
    for b in job["bullets"]:
        P(b, style="List Bullet")
P("EDUCATION", True, 11)
for ed in EDU:
    TL(ed["school"], ed["location"])
    TL(ed["degree"], ed["dates"], False)
P("ADDITIONAL", True, 11)
for a in ADDL:
    P(a, style="List Bullet")
d.save(docx_path)

# --- Visual check ---
x = pymupdf.open(pdf_path)
print("pages", x.page_count)
x[0].get_pixmap(dpi=110).save(os.path.join(os.path.dirname(os.path.abspath(docx_path)), "page1.png"))
