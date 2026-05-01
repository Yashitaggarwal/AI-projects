# PdffCoinverto & PdfItDown

**PdffCoinverto** is a powerful Python library to convert almost any file format (Images, Text, Word) into PDF.
**PdfItDown** is an MCP server built on top of PdffCoinverto to expose this functionality to AI agents.

## Installation

```bash
pip install .
```

## Usage

### Library

```python
from pdff_coinverto import PdfConverter

converter = PdfConverter()
pdf_path = converter.convert("path/to/file.docx")
print(f"PDF created at: {pdf_path}")
```

### MCP Server

Run the server:

```bash
pdfitdown
# or
python -m pdff_coinverto_project.server.server
```

## Supported Formats

- Images (.png, .jpg, etc.)
- Text (.txt, .md, .log, code files)
- Word (.docx) - Requires Microsoft Word on Windows
