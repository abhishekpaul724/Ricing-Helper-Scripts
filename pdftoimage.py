import fitz  # PyMuPDF
import os

pdf_path = input("Enter the pdf path: ")
output_folder = "pdf_images"
os.makedirs(output_folder, exist_ok=True)

doc = fitz.open(pdf_path)

# 600 DPI = zoom factor (dpi / 72)
zoom = 600 / 72  # 72 is default PDF dpi
mat = fitz.Matrix(zoom, zoom)

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=mat)
    pix.save(os.path.join(output_folder, f"page_{page_num+1:03d}.png"))

print(f"Conversion complete! Images saved in '{output_folder}'")
