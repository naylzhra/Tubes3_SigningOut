from __future__ import annotations

from pathlib import Path
from typing import Final
import fitz # butuh pip install PyMuPDF
import re

_SPACES: Final = re.compile(r"\s+")


def _read_pdf(pdf_path: str | Path) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])


def extract_regex_text(pdf_path: str | Path) -> str: #returnnya tu path
    raw = _read_pdf(pdf_path)
    cleaned_lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    final = "\n".join(cleaned_lines)

    pdf_path = Path(pdf_path)
    out_dir = pdf_path.parent / "regex"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / (pdf_path.stem + ".txt")
    out_file.write_text(final, encoding="utf-8")

    return out_file


def extract_plain_text(pdf_path: str | Path) -> str: #returnnya tu path
    raw = _read_pdf(pdf_path)
    collapsed = _SPACES.sub(" ", raw).strip().lower()

    pdf_path = Path(pdf_path)
    out_dir = pdf_path.parent / "plain"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / (pdf_path.stem + ".txt")
    out_file.write_text(collapsed, encoding="utf-8")

    return out_file

# kalo mau pake di file lain gini contohnya:
# from extractor import extract_regex_text, extract_plain_text

# pdf1 = "data/ACCOUNTANT/10554236.pdf"
# pdf2 = "data/ACCOUNTANT/10674770.pdf"
# regex_blob1 = extract_regex_text(pdf1)
# plain_blob1 = extract_plain_text(pdf1)
# regex_blob2 = extract_regex_text(pdf2)
# plain_blob2 = extract_plain_text(pdf2)
