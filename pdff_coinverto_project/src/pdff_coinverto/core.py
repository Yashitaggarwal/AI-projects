import os
from pathlib import Path
from PIL import Image
from fpdf import FPDF
import sys

# Try importing docx2pdf
try:
    from docx2pdf import convert as docx_convert
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

class PdfConverter:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir

    def convert(self, file_path: str) -> str:
        """
        Convert a single file to PDF.
        Returns the path to the generated PDF.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        output_filename = path.stem + ".pdf"
        
        if self.output_dir:
             out_path = Path(self.output_dir) / output_filename
        else:
             out_path = path.parent / output_filename

        output_file = str(out_path)

        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            self._convert_image(path, output_file)
        elif ext in ['.txt', '.md', '.log', '.py', '.js', '.json']:
            self._convert_text(path, output_file)
        elif ext == '.docx':
            self._convert_docx(path, output_file)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        return output_file

    def _convert_image(self, path: Path, output_file: str):
        image = Image.open(path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output_file)

    def _convert_text(self, path: Path, output_file: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
             with open(path, 'r', encoding='latin-1') as f:
                text = f.read()

        # Simple text wrapping handling by FPDF
        # sanitize text for latin1 if needed or just use utf8 compatible font instructions
        # FPDF standard font doesn't support full UTF-8, but we'll try basic.
        # For better support, we'd need a unicode font. 
        # We will replace unsupported chars to avoid crashes.
        
        # A simple way to handle multi_cell
        pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))
        pdf.output(output_file)

    def _convert_docx(self, path: Path, output_file: str):
        if not HAS_DOCX:
            raise ImportError("docx2pdf is not installed or available.")
        # docx2pdf output handling
        # It handles output path automatically if provided
        docx_convert(str(path), output_file)

