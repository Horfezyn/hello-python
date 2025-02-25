import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

# Configuration
CSV_FILE = "participants.csv"  
TEMPLATE_PDF = "template.pdf"  
OUTPUT_FOLDER = "certificates/"

# Create output folder if it does not exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def adjust_font_size(name):
    """Dynamically adjusts font size based on name length."""
    length = len(name)
    if length <= 15:
        return 48  # Large font for short names
    elif length <= 25:
        return 40  # Medium font
    elif length <= 35:
        return 32  # Small font
    else:
        return 24  # Very small font

def generate_certificate(participant_name):
    """Generates a certificate in PDF format based on the template."""
    
    output_pdf = f"{OUTPUT_FOLDER}certificate_{participant_name.replace(' ', '_')}.pdf"
    
    reader = PdfReader(TEMPLATE_PDF)
    writer = PdfWriter()
    page = reader.pages[0]  # Use the first page of the template

    temp_pdf = f"{OUTPUT_FOLDER}temp.pdf"
    c = canvas.Canvas(temp_pdf, pagesize=letter)

    font_size = adjust_font_size(participant_name)
    c.setFont("Helvetica-Bold", font_size)
    c.setFillColorRGB(0, 0, 0)  

    x_pos = 300  
    y_pos = 400  
    c.drawCentredString(x_pos, y_pos, participant_name)

    c.save()

    with open(temp_pdf, "rb") as temp_f:
        overlay_reader = PdfReader(temp_f)
        overlay_page = overlay_reader.pages[0]
        page.merge_page(overlay_page)  
    
    writer.add_page(page)
    with open(output_pdf, "wb") as output_f:
        writer.write(output_f)

    os.remove(temp_pdf)

    print(f"✅ Certificate generated: {output_pdf}")

# Read names from CSV file
df = pd.read_csv(CSV_FILE)

# Generate certificates for each participant
for name in df["Name"]:
    generate_certificate(name)

print("🎉 All certificates have been generated.")
