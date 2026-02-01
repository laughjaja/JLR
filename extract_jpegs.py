import re
import os

def extract_jpegs(pdf_path, output_dir):
    with open(pdf_path, 'rb') as f:
        data = f.read()

    # JPEG markers: \xff\xd8 ... \xff\xd9
    start_marker = b'\xff\xd8'
    end_marker = b'\xff\xd9'
    
    start = 0
    count = 0
    while True:
        start = data.find(start_marker, start)
        if start == -1:
            break
        end = data.find(end_marker, start)
        if end == -1:
            break
        
        end += 2
        jpeg_data = data[start:end]
        
        # Only save if it looks like a real image (size threshold)
        if len(jpeg_data) > 5000:
            count += 1
            output_path = os.path.join(output_dir, f"extracted_{count}.jpg")
            with open(output_path, 'wb') as out:
                out.write(jpeg_data)
            print(f"Extracted: {output_path}")
        
        start = end

if __name__ == "__main__":
    pdf_path = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/Company Profile JLR PNG Builders LTD.pdf"
    output_dir = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/extracted_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    extract_jpegs(pdf_path, output_dir)
