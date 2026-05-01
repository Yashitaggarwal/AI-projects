from pdff_coinverto import PdfConverter
from PIL import Image
import os

def test_conversion():
    # Create dummy files
    if not os.path.exists("test_files"):
        os.makedirs("test_files")
    
    # Text
    with open("test_files/test.txt", "w") as f:
        f.write("Hello, World! This is a test PDF conversion.")
    
    # Image
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save('test_files/test.png')
    
    converter = PdfConverter(output_dir="test_files")
    
    print("Converting test.txt...")
    pdf_txt = converter.convert("test_files/test.txt")
    print(f"Created: {pdf_txt}")
    
    print("Converting test.png...")
    pdf_img = converter.convert("test_files/test.png")
    print(f"Created: {pdf_img}")

    assert os.path.exists(pdf_txt)
    assert os.path.exists(pdf_img)
    print("Verification Successful!")

if __name__ == "__main__":
    test_conversion()
