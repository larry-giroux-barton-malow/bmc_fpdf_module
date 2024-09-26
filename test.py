from bmcFPDF import bmcFPDF

pdf = bmcFPDF()

#Create Report
pdf.qoSummaryReport("example.json")

#Output Report
pdf.output('QOTestReport.pdf')