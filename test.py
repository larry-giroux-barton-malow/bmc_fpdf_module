from fpdf import FPDF
from bmcFPDF import bmcFPDF

#pull json data from file once
#feed information into corect methods


pdf = bmcFPDF()

#Create Report
pdf.qoSummaryReport("example.json")

#Output Report
pdf.output('QOTestReport.pdf')