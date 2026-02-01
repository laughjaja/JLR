import re
import os
import zlib

def extract_images(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(pdf_path, 'rb') as f:
        content = f.read()

    # Find image objects
    # This is a very simplified parser
    obj_pattern = re.compile(rb'(\d+ \d+ obj.*?endobj)', re.DOTALL)
    img_count = 0
    
    for match in obj_pattern.finditer(content):
        obj_data = match.group(1)
        if b'/Type /XObject' in obj_data and b'/Subtype /Image' in obj_data:
            # Extract stream
            stream_start = obj_data.find(b'stream')
            if stream_start == -1:
                continue
            stream_start += 6
            if obj_data[stream_start] == 10: # \n
                stream_start += 1
            elif obj_data[stream_start:stream_start+2] == b'\r\n':
                stream_start += 2
                
            stream_end = obj_data.find(b'endstream')
            if stream_end == -1:
                continue
            
            stream_data = obj_data[stream_start:stream_end].strip()
            
            # Identify filter
            img_type = "bin"
            if b'/Filter /DCTDecode' in obj_data:
                img_type = "jpg"
            elif b'/Filter /FlateDecode' in obj_data:
                try:
                    stream_data = zlib.decompress(stream_data)
                    img_type = "png" # We'll just save raw bytes and guess
                except:
                    continue
            
            img_count += 1
            output_path = os.path.join(output_dir, f"img_{img_count}.{img_type}")
            with open(output_path, 'wb') as out:
                out.write(stream_data)
            print(f"Extracted: {output_path}")

if __name__ == "__main__":
    pdf_path = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/Company Profile JLR PNG Builders LTD.pdf"
    output_dir = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/extracted_images/raw"
    extract_images(pdf_path, output_dir)
