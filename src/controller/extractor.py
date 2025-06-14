from __future__ import annotations

from pathlib import Path
from typing import Final
import re

try:
    import fitz  # PyMuPDF - butuh pip install PyMuPDF
except ImportError:
    print("Warning: PyMuPDF not installed. PDF extraction will not work.")
    print("Install with: pip install PyMuPDF")
    fitz = None

_SPACES: Final = re.compile(r"\s+")

def _read_pdf(pdf_path: str | Path) -> str:
    if fitz is None:
        raise ImportError("PyMuPDF not installed. Cannot extract PDF content.")
    
    try:
        doc = fitz.open(pdf_path)
        text_content = "\n".join([page.get_text("text") for page in doc])
        doc.close()
        return text_content
    except Exception as e:
        raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")

def extract_cv_content_direct(pdf_path: str | Path, use_regex: bool = False) -> str:
    try:
        raw = _read_pdf(pdf_path)
        
        if use_regex:
            cleaned_lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
            return "\n".join(cleaned_lines)
        else:
            return _SPACES.sub(" ", raw).strip().lower()
            
    except Exception as e:
        print(f"Error extracting content from {pdf_path}: {e}")
        return f"Error extracting PDF content: {str(e)}"

# # Driver
# if __name__ == "__main__":
#     print("PDF Extractor Test")
    
#     test_paths = [
#         "data/ACCOUNTANT/10554236.pdf",
#         "data/DEVELOPER/sample_cv.pdf"
#     ]
    
#     for pdf_path in test_paths:
#         if Path(pdf_path).exists():
#             print(f"\nTesting with: {pdf_path}")
            
#             try:
#                 # Test regex extraction
#                 regex_file = extract_regex_text(pdf_path)
#                 print(f"Regex text saved to: {regex_file}")
                
#                 # Test plain extraction
#                 plain_file = extract_plain_text(pdf_path)
#                 print(f"Plain text saved to: {plain_file}")
                
#                 # Test direct extraction
#                 direct_content = extract_cv_content_direct(pdf_path, use_regex=False)
#                 print(f"Direct extraction: {len(direct_content)} characters")
#                 print(f"Sample: {direct_content[:100]}...")
                
#             except Exception as e:
#                 print(f"Error processing {pdf_path}: {e}")
#         else:
#             print(f"File not found: {pdf_path}")