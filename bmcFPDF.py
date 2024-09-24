from fpdf import FPDF


class bmcFPDF(FPDF):
    def header(self, title):
        # Arial bold 15
        self.set_font('Factoria Black', '', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_color("blue","text")
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
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

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

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