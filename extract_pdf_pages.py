import Quartz
import os
from Cocoa import NSURL, NSData, NSBitmapImageRep, NSPNGFileType

def extract_images_from_pdf(pdf_path, output_dir):
    url = NSURL.fileURLWithPath_(pdf_path)
    pdf = Quartz.PDFDocument.alloc().initWithURL_(url)
    if not pdf:
        print(f"Failed to load PDF: {pdf_path}")
        return

    for i in range(pdf.pageCount()):
        page = pdf.pageAtIndex_(i)
        # This gets the whole page as an image, which is a good way to see the content
        page_rect = page.boundsForBox_(Quartz.kPDFDisplayBoxMediaBox)
        
        # Create an image from the page
        image = Quartz.NSImage.alloc().initWithSize_(page_rect.size)
        image.lockFocus()
        context = Quartz.NSGraphicsContext.currentContext().graphicsPort()
        page.drawWithBox_(Quartz.kPDFDisplayBoxMediaBox)
        image.unlockFocus()
        
        bitmap = NSBitmapImageRep.alloc().initWithData_(image.TIFFRepresentation())
        png_data = bitmap.representationUsingType_properties_(NSPNGFileType, None)
        
        output_path = os.path.join(output_dir, f"page_{i+1}.png")
        png_data.writeToFile_atomically_(output_path, True)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    pdf_path = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/Company Profile JLR PNG Builders LTD.pdf"
    output_dir = "/Users/TTTG/Documents/Private_Trunk/Desktop_Backups/Desktop - Ja/808 Project/JLR/extracted_images"
    extract_images_from_pdf(pdf_path, output_dir)
