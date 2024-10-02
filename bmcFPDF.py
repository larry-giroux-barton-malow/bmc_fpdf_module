# TODO: 
# Add all high level objects to __init__ and data load methods
# Change all self.data calls to self.aiResponse.get()
# Update second table of Highlighted QO
# 
# BUG:
# none identified

from fpdf import FPDF
from fpdf import Align
import json

class bmcFPDF(FPDF):

    #Initialize values and add fonts
    def __init__(self):
        super().__init__()
        self.title = None
        self.subtitle = None
        self.date = None
        self.description = None
        self.error = None
        self.reportName = None
        self.aiResponse = {}
        self.aiHighlight = None
        self.observations = {}
        self.highlightedObs = None

        #add BM fonts
        self.add_font("Factoria Black","", "fonts\\Factoria-Black.ttf",uni=True)
        self.add_font("Factoria Demi","", "fonts\\Factoria-Demi.ttf",uni=True)
        self.add_font("URW DIN","", "fonts\\urwdin-regular.ttf",uni=True)
        self.add_font("URW DIN Bold","", "fonts\\urwdin-bold.ttf",uni=True)
        self.add_font("URW DIN BoldItalic","", "fonts\\urwdin-bolditalic.ttf",uni=True)
        self.add_font("URW DIN Italic","", "fonts\\urwdin-italic.ttf",uni=True)

    #Method used to load data, takes relative path
    def load_file(self, path = None):
        try:
            with open(path,"r") as f:
                data = json.loads(f.read())
                self.error = data.get("error","ERROR, Error not found")
                self.reportName = data.get("report_name","ERROR, Report Name not found")
                self.aiResponse = data.get("ai_response_frame",{'error':'data not found'})
                self.aiHighlight = data.get("ai_highlight","ERROR, AI Highlight not found")
                self.observations = data.get("observations:",{'error':'observations not found'})
                self.highlightedObs = self.observations.get(self.aiHighlight)
        except Exception as e:
            self.description = str(e)

    #Method used to set date field for report
    def set_date(self,arg = None):
        self.date = self.aiResponse.get(arg,"ERROR, Date not found")

    #Define the Header for each page
    def header(self):
        # Factoria Black regular 12
        self.set_font('Factoria Black', '', 12)
        # Colors of text
        self.set_color()

        # Title
        self.cell(self.get_string_width(self.title), 5, self.title, 0, 1, 'L')

        # URW DIN regular 12
        self.set_font('URW DIN', '', 12)

        # Subtitle
        self.cell(self.get_string_width(self.subtitle), 5, self.subtitle, 0, 1, 'L')

        self.ln(2)

        # Date
        self.set_font('URW DIN Bold', '', 12)
        self.cell(w=self.get_string_width("DATE:   "), h=5, text="DATE:", border=0, align='L')
        self.set_font('URW DIN', '', 12)
        self.cell(w=self.get_string_width(self.date), h=5, text=self.date, border=0, align='L')
        self.ln()

        #BMC Logo
        self.image("Barton-Malow-Company-Linear-Logo-Full-Color.jpg",160,10,30,0,"JPG")

        # Line break
        self.ln(4)

    #Define the Footer for each page
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        
        # Set color of Text
        self.set_color()
        
        #Add report type to bottom corner
        self.set_font('URW DIN Bold', '', 10)
        self.cell(0, 10, 'NOTE: This Report is Generated Using AI', 0, 0, 'L')

        # Page number
        self.set_font('URW DIN', '', 10)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, 'R')

    #Method used to add the description section to a report
    def descriptionText(self,fileName=None):
        desc = "This is a report generated by the Quality Team"
        if fileName != None:
            try:
                with open(fileName,'r') as f:
                    desc = f.read()
            except Exception as e:
                desc = fileName

        self.set_color()
        self.set_font('URW DIN Bold', '', 12)
        self.cell(self.get_string_width("Description:"), 8, "Description:", 0, 1, 'L')

        self.set_font('URW DIN', '', 10)
        self.multi_cell(w=0,h=None,text=desc)
        self.ln(5)

    #Method to set consistent Header styling
    def setTableHeaderStyle(self):
        self.set_color("rebar","fill")
        self.set_color()
        self.set_color("blue","draw")
        self.set_font("URW DIN Bold","",10)

    #Method to set consistent Body styling
    def setTableBodyStyle(self):
        self.set_color()
        self.set_color("blue","draw")
        self.set_font("URW DIN","",10)

    #Method to create a 2x2 table with a ryg value in column 1 row 2 (not completed)
    def rygTable(self,k1,k11,k2,k22,ryg):
        # output headers (k1, and k2)
        self.setTableHeaderStyle()
        self.cell(w=30, h=6, text=k1, border=1, align='C', fill=True)
        self.cell(w=0, h=6, text=k2, border=1, align='C', fill=True)
        self.ln()

        self.setTableBodyStyle()
        top = self.y
        self.x=40
        ReasoningCell = self.multi_cell(0, None, self.aiResponse.get(k22, "ERROR, Reasoning not found"), 1, 'L',padding=2,output='HEIGHT')

        self.y = top
        self.x=10
        self.set_color(ryg,"fill")
        self.set_color("black","text")
        self.set_font("URW DIN Bold",'',10)
        self.cell(30, ReasoningCell, self.aiResponse.get(k11, "ERROR, Data not found"), 1, 0,'C',True)
        
        self.ln()
        self.ln(5)

    #Method to create the QO Highlight Content
    def QoHighlight(self):
        #Section Header
        self.set_font("Urw Din Bold",'',12)
        self.set_color()
        self.cell(text="Quality Observation Highlighted:")
        self.ln(6)

        #1st Table Header
        self.setTableHeaderStyle()
        top = self.y
        headerH=self.multi_cell(w=30,h=None,text="Highlighted Observation",border=1,align='C',fill=True,padding=2,output='HEIGHT')
        self.y = top
        self.cell(w=130,h=headerH,text="Reasoning",border=1,align='C',fill=True)
        self.y = top
        self.multi_cell(w=30,h=None,text="Highlight Pool Size",border=1,align='C',fill=True,padding=2)

        #1st Table Body
        self.setTableBodyStyle()
        top=self.y
        self.x=40
        bodyH=self.multi_cell(w=130,h=None,text=self.aiResponse.get("highlight_reasoning","ERROR, Highlight Reasoning not found"),border=1,align='C',fill=False,padding=2,output='Height')
        self.y=top
        self.x=10
        self.cell(w=30,h=bodyH,text=self.aiResponse.get("highlighted_observation", "ERROR, Highlighted Observation not found"),border=1,align='C',fill=False,link=self.aiResponse.get("highlight_link"))
        self.y=top
        self.x=170
        poolSize=self.aiResponse.get("highlight_pool_size", "ERROR, Highlight Pool Size not found")
        poolSize = str(poolSize)
        self.cell(w=30,h=bodyH,text=poolSize,border=1,align='C',fill=False)
        self.ln()
        self.ln(5)

        #2nd Table Header
        #Date, Type, Categorey, Location, Description
        self.setTableHeaderStyle()
        top=self.y
        self.x=10
        self.cell(w=30,h=10,text="Date",border=1,align='C',fill=True)
        self.cell(w=30,h=10,text="Type",border=1,align='C',fill=True)
        self.cell(w=30,h=10,text="Category",border=1,align='C',fill=True)
        self.cell(w=30,h=10,text="Location",border=1,align='C',fill=True)
        self.cell(w=70,h=10,text="Description",border=1,align='C',fill=True)
        self.ln()

        #2nd Table Body
        self.setTableBodyStyle()
        top=self.y
        height1=self.multi_cell(w=30,h=None,text=self.highlightedObs.get("Date/Time","ERROR, Date/Time not found"),border=0,align='C',fill=False,padding=2,output='Height')
        self.y=top
        height2=self.multi_cell(w=30,h=None,text=self.highlightedObs.get("Obs Type","ERROR, Obs Type not found"),border=0,align='C',fill=False,padding=2,output='Height',dry_run=True)
        if height2>height1: height1=height2
        self.setTableBodyStyle()
        self.y=top
        self.x=70
        height2=self.multi_cell(w=30,h=None,text=self.highlightedObs.get("Category","ERROR, Category not found"),border=0,align='C',fill=False,padding=2,output='Height')
        if height2>height1: height1=height2
        self.y=top
        height2=self.multi_cell(w=30,h=None,text=self.highlightedObs.get("Location","ERROR, Location not found"),border=0,align='C',fill=False,padding=2,output='Height')
        if height2>height1: height1=height2
        self.y=top
        height2=self.multi_cell(w=70,h=None,text=self.highlightedObs.get("Description","ERROR, Description not found"),border=0,align='C',fill=False,padding=2,output='Height')
        if height2>height1: height1=height2
        self.y=top
        self.x=10
        self.cell(w=30,h=height1,border=1)
        obsType = self.highlightedObs.get("Obs Type")
        if obsType.lower().strip() == "positive":
            self.set_color("green","fill")
        else:
            self.set_color("red","fill")
        self.set_color("black","text")
        self.set_font("URW DIN Bold",'',10)
        self.cell(w=30,h=height1,border=1,fill=1)
        self.x=40
        self.multi_cell(w=30,h=None,text=self.highlightedObs.get("Obs Type","ERROR, Observation Type not found"),border=0,align='C',fill=False,padding=2,output='Height')
        self.y=top
        self.cell(w=30,h=height1,border=1)
        self.cell(w=30,h=height1,border=1)
        self.cell(w=70,h=height1,border=1)
        self.ln()
        self.ln(5)

        #Highlighted QO Image
        imageTopY=self.y
        imageHeight= 277 - imageTopY
        
        imageURL = self.highlightedObs.get("image_url")
        self.image(name=imageURL,h=imageHeight,x=Align.C)
        # self.cell(190,10,"cell 1",1)

    #Method to creat the summary section
    def QoSummary(self):
        #Section Header
        self.set_font("Urw Din Bold",'',12)
        self.set_color()
        self.cell(text="Report Summary:")
        self.ln()
        self.ln(1)
        self.set_font("Urw Din",'',10)
        self.multi_cell(w=0,text=self.aiResponse.get("period_summary", "ERROR, Period Summary not found"))
        self.ln(3)

    #Method to create Observations section
    def QoSection(self,obsID):

        #Get data out
        obsID = str(obsID)
        obs=self.observations.get(obsID)
        obsDate = obs.get("Date/Time")
        obsType = obs.get("Obs Type")
        obsCat = obs.get("Category")
        obsSev = obs.get("Severity")
        if obsType.lower().strip() == "positive": obsSev = "N/A"
        obsDesc = obs.get("Description")
        obsStat = obs.get("Status")
        obsImg = obs.get("image_url")

        self.set_color()
        self.set_font('URW DIN Bold', '', 12)
        self.cell(w=self.get_string_width("Quality Observation: "),h=None,text="Quality Observation: ")
        self.set_font('URW DIN', '', 12)
        self.cell(w=self.get_string_width(obs.get("Obs ID")),h=None,text=obs.get("Obs ID"),link=obs.get("link"))
        self.ln()
        self.ln(2)

        #Table Headers Row 1
        self.setTableHeaderStyle()
        self.cell(w=30, h=5, text="Date",border=1, fill=1, align='C')
        self.cell(w=30, h=5, text="Type",border=1, fill=1, align='C')
        self.cell(w=30, h=5, text="Severity",border=1, fill=1, align='C')
        self.cell(w=100, h=5, text="Image", border=1, fill=1, align='C')
        self.ln()
        top=self.y

        #Table Body Row 1
        self.x=100
        self.image(name=obsImg,w=100,h=95,keep_aspect_ratio=True)
        self.y=top
        self.cell(w=100,h=95,border=1)
        
        self.setTableBodyStyle()
        self.y=top
        self.x=10
        height1=self.multi_cell(w=30,h=None,text=obsDate,border=0,align='C',fill=False,padding=2,output='Height',max_line_height=10)
        self.y=top
        height2=self.multi_cell(w=30,h=None,text=obsType,border=0,align='C',fill=False,padding=2,output='Height',dry_run=True)
        if height2>height1: height1=height2
        self.setTableBodyStyle()
        self.y=top
        self.x=70
        height2=self.multi_cell(w=30,h=None,text=obsSev,border=0,align='C',fill=False,padding=2,output='Height',max_line_height=10)
        if height2>height1: height1=height2
        self.y=top
        self.x=10
        self.cell(w=30,h=10,border=1)
        if obsType.lower().strip() == "positive":
            self.set_color("green","fill")
        else:
            self.set_color("red","fill")
        self.set_color("black","text")
        self.set_font("URW DIN Bold",'',10)
        self.cell(w=30,h=10,border=1,fill=1)
        self.x=40
        self.multi_cell(w=30,h=None,text=obsType,border=0,align='C',fill=False,padding=2,output='Height', max_line_height=10)
        self.y=top
        self.cell(w=30,h=10,border=1)
        self.ln()

        #Table Headers Row 2
        self.setTableHeaderStyle()
        self.cell(w=60, h=5, text="Category",border=1,fill=1,align='C')
        self.cell(w=30, h=5, text="Status",border=1,fill=1,align='C')
        self.ln()

        #Table Body Row 2
        self.setTableBodyStyle()
        top=self.y
        height1=self.multi_cell(w=60,h=None,text=obsCat,border=0,align='C',fill=False,padding=2,output='Height', max_line_height=10)
        self.y=top
        height2=self.multi_cell(w=30,h=None,text=obsStat,border=0,align='C',fill=False,padding=2,output='Height', max_line_height=10)
        if height2>height1: height1=height2
        self.y=top
        self.x=10
        self.cell(w=60,h=10,border=1)
        self.cell(w=30,h=10,border=1)
        self.ln()

        #Table Headers Row 3
        self.setTableHeaderStyle()
        self.cell(w=90, h=5, text="Description",border=1,fill=1,align='C')
        self.ln()

        #Table Body Row 3
        self.setTableBodyStyle()
        top=self.y
        heightDesc=self.multi_cell(w=90,h=None,text=obsDesc,border=0,align='C',fill=False,padding=2,output='Height')
        self.y=top
        self.x=10
        self.cell(w=90,h=65,border=1)
        
        self.ln()
        self.ln(5)

    #Use this method to set the color from defined list, 
    #use "text" for text, "fill" for backround of cells, and "draw" for borders
    #Default is blue text
    def set_color(self,color = "blue", type = "text"):
        c = [0,0,0]
        if isinstance(color,str):
            color = color.lower().strip()
            if color in ["barton blue", "blue"]:
                c = [0,38,58]
            elif color in ["malow orange", "orange"]:
                c = [227,82,5]
            elif color in ["steel blue", "steel"]:
                c = [79,117,139]
            elif color in ["craftsman blue", "craft"]:
                c = [40,76,96]
            elif color in ["rebar grey", "rebar"]:
                c = [165,186,201]
            elif color in ["slate blue","slate"]:
                c = [122,151,171]
            elif color in ["red","r"]:
                c = [255,0,0]
            elif color in ["yel","yellow","y"]:
                c = [255,255,0]
            elif color in ["green","grn","g"]:
                c = [0,255,0]
            elif color in ["white", "w"]:
                c = [255,255,255]
        if isinstance(type,str):
            type = type.lower().strip()
            if type == "fill":
                self.set_fill_color(c[0],c[1],c[2])
                return
            if type == "draw":
                self.set_draw_color(c[0],c[1],c[2])
                return
        self.set_text_color(c[0],c[1],c[2])

    #Create report and define the title, subtitle, and description
    def report(self, title, subtitle, description):
        self.title = title.strip() if isinstance(title, str) else "ERROR, title not found!"
        self.subtitle = subtitle.strip() if isinstance(subtitle, str) else "ERROR, subtitle not found!"
        self.date = self.date.strip() if isinstance(self.date, str) else "ERROR, date not found!"
        self.description = description.strip() if isinstance(description, str) else "ERROR, description not found!"
        self.add_page()

    #One method for a QO Summary
    def qoSummaryReport(self,fileName):
        #Load JSON file 
        self.load_file(fileName)

        #Set document properties
        self.set_author('BMC Quality')

        #Create document and add first page
        self.set_date("period_description")
        self.report("Project Quality Observation Summary","Project Name: "+self.reportName, "test description")

        #Add description section
        self.descriptionText("desc.txt")

        #Add summary
        self.QoSummary()

        #Add RYG table (Risk Level)
        #Do RYG logic
        h1 = "Risk Level"
        h11 = "risk_level"
        h2 = "Risk Level Reasoning"
        h22 = "risk_level_reasoning"
        c = None
        riskLevel = self.aiResponse.get(h11,"ERROR, Risk Level not found")
        riskLevel = riskLevel.lower().strip()
        if riskLevel == "low":
            c = "green"
        elif riskLevel == "medium":
            c = "yellow"
        else:
            c = "red"

        #Add table
        self.rygTable(h1,h11,h2,h22,c)

        #Add RYG table (Data Quality)
        #Do RYG logic
        h1 = "Data Quality"
        h11 = "data_quality"
        h2 = "Data Quality Reasoning"
        h22 = "data_quality_reasoning"
        c = None
        dataQuality = self.aiResponse.get(h11, "ERROR, Data Quality not found")
        dataQuality = dataQuality.lower().strip()
        if dataQuality == "high":
            c = "green"
        elif dataQuality == "medium":
            c = "yellow"
        else:
            c = "red"
        self.rygTable(h1,h11,h2,h22,c)

        #Add Highlighted Observation
        self.QoHighlight()

        #Add All observations
        obsCount=0
        for k in self.observations:
            if obsCount %2 == 0: self.add_page()
            self.QoSection(k)
            obsCount+=1
            
