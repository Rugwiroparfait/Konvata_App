from pdf2docx import Converter
from docx import Document
from reportlab.pdfgen import canvas

def pdf_to_docx(input_file, output_file):
    cv = Converter(input_file)
    cv.convert(output_file)
    cv.close()

def docx_to_pdf(input_file, output_file):
    doc = Document(input_file)
    pdf = canvas.Canvas(output_file)
    for para in doc.paragraphs:
        pdf.drawString(50, 800, para.text)
    pdf.save()
