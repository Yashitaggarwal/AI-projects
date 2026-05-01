from fastmcp import FastMCP
from pdff_coinverto import PdfConverter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PdfItDown")

# Create an MCP server
mcp = FastMCP("PdfItDown")

@mcp.tool()
def convert_to_pdf(files: list[str]) -> list[str]:
    """
    Convert a list of files to PDF format.
    
    Args:
        files: List of absolute file paths to convert.
        
    Returns:
        List of paths to the generated PDF files.
    """
    converter = PdfConverter()
    results = []
    
    for file_path in files:
        try:
            logger.info(f"Converting file: {file_path}")
            pdf_path = converter.convert(file_path)
            results.append(pdf_path)
        except Exception as e:
            logger.error(f"Failed to convert {file_path}: {e}")
            # We continue processing other files even if one fails
            # But maybe we should report the error?
            # For now, let's append an error string or skip?
            # The tool signature says list[str], so maybe just return what we have?
            # Or formatted error string?
            # Let's return "Error: <msg>" only if critical, but user usually wants paths.
            results.append(f"Error converting {file_path}: {str(e)}")

    return results


def main():
    mcp.run()

if __name__ == "__main__":
    main()

