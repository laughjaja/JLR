import fitz # PyMuPDF
import os

pdf_path = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/Company Profile JLR PNG Builders LTD.pdf"
output_dir = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/extracted_images/refined"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)
for page_index in range(len(doc)):
    page = doc[page_index]
    image_list = page.get_images(full=True)
    
    print(f"Found {len(image_list)} images on page {page_index + 1}")
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        image_name = f"page{page_index+1}_img{img_index+1}.{image_ext}"
        image_path = os.path.join(output_dir, image_name)
        
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved: {image_name}")

doc.close()
print("Extraction complete.")
