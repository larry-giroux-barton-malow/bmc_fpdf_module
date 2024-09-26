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
pdf.set_date("Period Description")
pdf.report("Project Quality Observation Summary","Project Name:", "test description")

#Add description section
pdf.descriptionText("desc.txt")

#Add RYG table (Risk Level)
#Do RYG logic
h1 = "Risk Level"
h2 = "Risk Level Reasoning"
c = None
riskLevel = pdf.data[h1]
riskLevel = riskLevel.lower().strip()
if riskLevel == "low":
    c = "green"
elif riskLevel == "medium":
    c = "yellow"
else:
    c = "red"

#Add table
pdf.rygTable(h1,h2,c)

#Add RYG table (Data Quality)
#Do RYG logic
h1 = "Data Quality"
h2 = "Data Quality Reasoning"
c = None
dataQuality = pdf.data[h1]
dataQuality = dataQuality.lower().strip()
if dataQuality == "high":
    c = "green"
elif dataQuality == "medium":
    c = "yellow"
else:
    c = "red"
pdf.rygTable(h1,h2,c)

#Add Highlighted Observation
#Do RYG logic
pdf.QoHighlight()

#Output document
pdf.output('QOTestReport.pdf')