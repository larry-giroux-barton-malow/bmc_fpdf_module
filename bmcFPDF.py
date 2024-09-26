# TODO: Update the descriptionText method
# BUG: none identified 

from fpdf import FPDF
import json

class bmcFPDF(FPDF):

    #Initialize values and add fonts
    def __init__(self):
        super().__init__()
        self.title = None
        self.subtitle = None
        self.date = None
        self.description = None
        self.data = None

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
                self.data = json.loads(f.read())
        except Exception as e:
            self.description = str(e)

    #Method used to set data feild for report
    def set_date(self,arg = None):
        if arg in self.data: self.date = self.data[arg]

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

        self.ln(5)

        # Date
        self.set_font('URW DIN Bold', '', 10)
        self.cell(self.get_string_width("DATE"), 5, "DATE", 0, 1, 'L')
        self.set_font('URW DIN', '', 10)
        self.cell(self.get_string_width(self.date), 5, self.date, 0, 1, 'L')

        #BMC Logo
        self.image("Barton-Malow-Company-Linear-Logo-Full-Color.jpg",160,10,40,0,"JPG")

        # Line break
        self.ln(5)

    #Define the Footer for each page ( can I added page # of # ?)
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
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'R')

    #Method used to add the description section to a report
    #(Need to Update: The method can check if the arg is an existing file.
    # If it is, read the file, if not, dump the argument into the description box as raw text.)
    def descriptionText(self,file_name):
        desc = "Error, file not read"
        try:
            with open(file_name,'r') as f:
                desc = f.read()
        except Exception as e:
            desc = "ERROR: file not read. " + str(e)
            print(e)

        self.set_color()
        self.set_font('URW DIN Bold', '', 10)
        self.cell(self.get_string_width("Description:"), 8, "Description:", 0, 1, 'L')

        self.set_font('URW DIN', '', 10)
        self.multi_cell(0,0,desc)
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
    def rygTable(self,k1,k2,ryg):
        # output headers (k1, and k2)
        self.setTableHeaderStyle()
        self.cell(30, 10, k1, 1, 0, 'C',True)
        self.cell(0, 10, k2, 1, 0, 'C',True)
        self.ln()

        self.setTableBodyStyle()
        top = self.y
        self.x=40
        ReasoningCell = self.multi_cell(0, None, self.data[k2], 1, 'L',padding=2,output='HEIGHT')

        self.y = top
        self.x=10
        self.set_color(ryg,"fill")
        self.set_color("black","text")
        self.set_font("URW DIN Bold",'',10)
        self.cell(30, ReasoningCell, self.data[k1], 1, 0,'C',True)
        
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
        bodyH=self.multi_cell(w=130,h=None,text=self.data["Highlight Reasoning"],border=1,align='C',fill=False,padding=2,output='Height')
        self.y=top
        self.x=10
        self.cell(w=30,h=bodyH,text=self.data["Highlighted Observation"],border=1,align='C',fill=False,link=self.data["Link"])
        self.y=top
        self.x=170
        self.cell(w=30,h=bodyH,text=self.data["Highlight Pool Size"],border=1,align='C',fill=False)
        self.ln()
        self.ln(5)

        #2nd Table Header
        #Date, Type, Categorey, Location, Description
        self.setTableHeaderStyle()
        top=self.y
        self.x=10
        self.cell(w=30,h=10,text="Date",border=1,align='C',fill=True)
        self.cell(w=30,h=10,text="Type",border=1,align='C',fill=True)
        self.cell(w=30,h=10,text="Categorey",border=1,align='C',fill=True)
        self.cell(w=30,h=10,text="Location",border=1,align='C',fill=True)
        self.cell(w=70,h=10,text="Description",border=1,align='C',fill=True)
        self.ln()

        #2nd Table Body
        self.setTableBodyStyle()
        top=self.y
        height1=self.multi_cell(w=30,h=None,text=self.data["Highlighted Observation Date"],border=0,align='C',fill=False,padding=2,output='Height')
        self.y=top
        
        height2=self.multi_cell(w=30,h=None,text=self.data["Highlighted Observation Type"],border=0,align='C',fill=False,padding=2,output='Height',dry_run=True)
        if height2>height1: height1=height2
        
        self.setTableBodyStyle()
        self.y=top
        self.x=70
        height2=self.multi_cell(w=30,h=None,text=self.data["Highlighted Observation Category"],border=0,align='C',fill=False,padding=2,output='Height')
        if height2>height1: height1=height2
        self.y=top
        height2=self.multi_cell(w=30,h=None,text=self.data["Highlighted Observation Location"],border=0,align='C',fill=False,padding=2,output='Height')
        if height2>height1: height1=height2
        self.y=top
        height2=self.multi_cell(w=70,h=None,text=self.data["Highlighted Observation Description"],border=0,align='C',fill=False,padding=2,output='Height')
        if height2>height1: height1=height2
        self.y=top
        self.x=10
        self.cell(w=30,h=height1,border=1)

        obsType = self.data["Highlighted Observation Type"]
        if obsType.lower().strip() == "positive":
            self.set_color("green","fill")
        else:
            self.set_color("red","fill")
        self.set_color("black","text")
        self.set_font("URW DIN Bold",'',10)
        self.cell(w=30,h=height1,border=1,fill=1)
        self.x=40
        self.multi_cell(w=30,h=None,text=self.data["Highlighted Observation Type"],border=0,align='C',fill=False,padding=2,output='Height')
        self.y=top
        self.cell(w=30,h=height1,border=1)
        self.cell(w=30,h=height1,border=1)
        self.cell(w=70,h=height1,border=1)

        # self.cell(190,10,"cell 1",1)
        
        



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

