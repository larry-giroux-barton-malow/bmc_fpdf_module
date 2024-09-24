from fpdf import FPDF
from bmcFPDF import bmcFPDF

pdf = bmcFPDF()
pdf.set_title("QO Summary Test")
pdf.set_author('Quality Team')
pdf.report("Project Quality Observation Summary","Project Name:"," September 24, 2024", "test description")
pdf.descriptionText("desc.txt")
pdf.output('QOTestReport.pdf')