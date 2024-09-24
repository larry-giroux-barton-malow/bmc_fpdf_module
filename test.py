from bmcFPDF import bmcFPDF

pdf = bmcFPDF()
pdf.set_title("QO Summary Test")
pdf.set_author('MoneyPenny')
pdf.report("Test Report","Test Subtitle"," September 9, 2024", "test description")
pdf.output('QOTestReport.pdf', 'F')