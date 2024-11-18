
import os
from bmcFPDF import bmcFPDF

userHome            = os.path.expanduser('~')
inputJsonFolder     = os.path.normpath(os.path.join(userHome,"OneDrive - Barton Malow","Quality Observations","Quality Observations Reports","json","qo_summary_pdf_src"))
outputPdfFolder     = os.path.normpath(os.path.join(userHome,"OneDrive - Barton Malow","AI Reports","Raw Reports"))

for f in os.listdir(inputJsonFolder):

    pdf = bmcFPDF()
    inputFilePath = os.path.join(inputJsonFolder,f)
    print(inputFilePath)
    pdf.qoSummaryReport(inputFilePath)
    outputFileName = "Quality Observations Summary - "+f.replace(".json","")+".pdf"
    print(outputFileName)
    outputFilePath = os.path.join(outputPdfFolder,outputFileName)
    pdf.output(outputFilePath)