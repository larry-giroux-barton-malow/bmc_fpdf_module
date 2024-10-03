
import os
from pathlib import Path

from bmcFPDF import bmcFPDF

pdf = bmcFPDF()
inputJsonFolder = os.path.realpath("C:\Users\mkoski2\OneDrive - Barton Malow\Quality Observations\Quality Observations Reports\json\qo_summary_pdf_src")
outputPdfFolder = "C:\Users\mkoski2\OneDrive - Barton Malow\AI Reports\Raw Reports"

for f in os.listdir(inputJsonFolder):
    fileName = f.replace(".json","")+".pdf"
    print(fileName)

    # filePath = os.path.join(outputPdfFolder,fileName)
    # pdf.qoSummaryReport(filePath)