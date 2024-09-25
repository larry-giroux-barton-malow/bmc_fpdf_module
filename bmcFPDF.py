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
        self.set_color("blue","text")

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
        self.ln(10)

    #Define the Footer for each page
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        
        # Set color of Text
        self.set_color("blue","text")
        
        #Add report type to bottom corner
        self.set_font('URW DIN Bold', '', 10)
        self.cell(0, 10, 'NOTE: This Report is Generated Using AI', 0, 0, 'L')

        # Page number
        self.set_font('URW DIN', '', 10)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'R')

    #Method used to add the description section to a report
    def descriptionText(self,file_name):
        desc = "Error, file not read"
        try:
            with open(file_name,'r') as f:
                desc = f.read()
        except Exception as e:
            desc = "ERROR: file not read. " + str(e)
            print(e)

        self.set_font('URW DIN Bold', '', 10)
        self.cell(self.get_string_width("Description:"), 8, "Description:", 0, 1, 'L')

        self.set_font('URW DIN', '', 10)
        self.multi_cell(0,0,desc)

    #Method to create a 2x2 table with a ryg value in column 1 row 2 (not completed)
    def rygTable(self,k1,k2,ryg):


        # output headers (k1, and k2)
        #     
        self.set_color(ryg,"fill")
        if ryg.lower()[0] in ["r","g"]:
            self.set_color("white","text")
        else:
            self.set_color("black","text")
        # output values (self.data[k1] and self.data[k2]) styling the first one with RYG and BOLD text 

        self.set_color("black","text")

    #Use this method to set the color from defined list, 
    # use "text" for text, "fill" for backround of cells, and "draw" for borders
    def set_color(self,color = "black", type = "text"):
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

