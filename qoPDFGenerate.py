
import os
from pathlib import Path

from bmcFPDF import bmcFPDF

inputJsonFolder = r"C:\Users\mkoski2\OneDrive - Barton Malow\Quality Observations\Quality Observations Reports\json\qo_summary_pdf_src"
outputPdfFolder = r"C:\Users\mkoski2\OneDrive - Barton Malow\AI Reports\Raw Reports"

for f in os.listdir(inputJsonFolder):

    pdf = bmcFPDF()
    inputFilePath = os.path.join(inputJsonFolder,f)
    print(inputFilePath)
    pdf.qoSummaryReport(inputFilePath)
    outputFileName = f.replace(".json","")+".pdf"
    print(outputFileName)
    outputFilePath = os.path.join(outputPdfFolder,outputFileName)
    pdf.output(outputFilePath)