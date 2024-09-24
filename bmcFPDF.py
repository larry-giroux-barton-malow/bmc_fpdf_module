from fpdf import FPDF
import json


class bmcFPDF(FPDF):

    def __init__(self):
        super().__init__()
        self.title = None
        self.subtitle = None
        self.date = None
        self.description = None

        #add BM fonts
        self.add_font("Factoria Black","", "fonts\\Factoria-Black.ttf",uni=True)
        self.add_font("Factoria Demi","", "fonts\\Factoria-Demi.ttf",uni=True)
        self.add_font("URW DIN","", "fonts\\urwdin-regular.ttf",uni=True)
        self.add_font("URW DIN Bold","", "fonts\\urwdin-bold.ttf",uni=True)
        self.add_font("URW DIN BoldItalic","", "fonts\\urwdin-bolditalic.ttf",uni=True)
        self.add_font("URW DIN Italic","", "fonts\\urwdin-italic.ttf",uni=True)

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

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

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

    def rygTable(self,file_name):
        with open(file_name,'r') as f:
            data = json.load(f)
        with self.table() as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)


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
        if isinstance(type,str):
            type = type.lower().strip()
            if type == "fill":
                self.set_fill_color(c[0],c[1],c[2])
                return
            if type == "draw":
                self.set_draw_color(c[0],c[1],c[2])
                return
        self.set_text_color(c[0],c[1],c[2])

    def report(self, title, subtitle, date, description):
        self.title = title.strip() if isinstance(title, str) else "ERROR, title not found!"
        self.subtitle = subtitle.strip() if isinstance(subtitle, str) else "ERROR, subtitle not found!"
        self.date = date.strip() if isinstance(date, str) else "ERROR, date not found!"
        self.description = description.strip() if isinstance(description, str) else "ERROR, description not found!"
        self.add_page()

