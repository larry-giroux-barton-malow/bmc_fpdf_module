from bmcFPDF import bmcFPDF

pdf = bmcFPDF()

#Create Report
pdf.APIReport()

# take in a dictonary
# set dictonary values to appropriate pdf values

# Output Report
pdf.output('APITestReport.pdf')

# byteOut = pdf.output()
# print(byteOut)