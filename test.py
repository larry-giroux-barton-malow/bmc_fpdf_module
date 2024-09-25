from fpdf import FPDF
from bmcFPDF import bmcFPDF

#pull json data from file once
#feed information into corect methods


pdf = bmcFPDF()

#Load JSON file 
pdf.load_file("example.json")

#Set document properties
pdf.set_title("QO Summary Test")
pdf.set_author('Quality Team')

#Create document and add first page
pdf.set_date("period_description")
pdf.report("Project Quality Observation Summary","Project Name:", "test description")

#Add description section
pdf.descriptionText("desc.txt")

#Add RYG table (Risk Level)
#Do RYG logic
pdf.rygTable("data_quality","data_quality_reasoning","r")

#Add RYG table (Data Quality)
#Do RYG logic
pdf.rygTable("data_quality","data_quality_reasoning","r")

#Add Highlighted Observation
#Do RYG logic

#Output document
pdf.output('QOTestReport.pdf')