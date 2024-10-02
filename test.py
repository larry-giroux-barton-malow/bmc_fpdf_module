from bmcFPDF import bmcFPDF

pdf = bmcFPDF()

#Create Report
pdf.qoSummaryReport("GM - Project A.json")

#Output Report
pdf.output('QOTestReport.pdf')