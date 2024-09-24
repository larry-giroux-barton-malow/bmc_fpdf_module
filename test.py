from fpdf import FPDF
from bmcFPDF import bmcFPDF

#pull json data from file once
#feed information into corect methods


pdf = bmcFPDF()
pdf.load_file("example.json")
pdf.set_date("period_description")
pdf.set_title("QO Summary Test")
pdf.set_author('Quality Team')
pdf.report("Project Quality Observation Summary","Project Name:", "test description")
pdf.descriptionText("desc.txt")
pdf.rygTable("data_quality","data_quality_reasoning","r")
pdf.output('QOTestReport.pdf')