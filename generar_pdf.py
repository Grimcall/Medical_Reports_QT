from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from dateutil import parser
import textwrap
import pytz
import pandas as pd

class GeneradorPDF:
    def __init__(self, df, row_n, recetas = None):
        self.df : pd.DataFrame = df

        #Getting font ready for later use.
        pdfmetrics.registerFont(TTFont('Garamond', 'EBGaramond-Regular.ttf'))
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        style.fontName = "Garamond"

        #Read model pdf.
        modelo = PdfReader("Modelo_Receta_Villegas_1.pdf", decompress = False).pages[0]
        modelo_obj = pagexobj(modelo)

        #Select specific row.
        row = self.df.iloc[row_n]

        #Extract values from row[col]
        fecha = row['Timestamp']
        nombre = row['Nombre']
        apellidos =  row['Apellidos']
        run = row['RUT o N° Pasaporte']
        direccion = row['Número de Teléfono']
        edad = row['Edad']
        nombre_apellido = nombre + ' ' + apellidos

        #Name outfile after date + patient name and surname.             
        dt = parser.parse(fecha)
        chile_tz = pytz.timezone("Etc/GMT-3")
        dt = dt.astimezone(chile_tz)
        new_date = dt.strftime("%Y-%m-%d")

        outfile = new_date + "_" + nombre + apellidos + ".pdf"

        canvas = Canvas(outfile)

        xobj_name = makerl(canvas, modelo_obj)
        canvas.doForm(xobj_name)

        y_top = 675
        y_bottom = 655
        x_left = 135
        x_right = 405

        ##START DATA WRITE
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        ##Filling patient data.
        canvas.drawString(x_left, y_top, nombre_apellido)

        canvas.drawString(x_right, y_top, run)

        canvas.drawString(x_left, y_bottom, str(direccion))

        canvas.drawString(x_right, y_bottom, str(edad))

        ##Writing signature.
        signature = ImageReader('firma.png')
        signature_width, signature_height = signature.getSize()
        canvas.drawImage(
            signature, 
            width = signature_width/1.3, 
            height = signature_height/1.3, 
            x = 310, 
            y = 132, 
            mask = "auto")
        
        ##Writing recipe.

        #Dummy string to test text wrapping.
        #Splits lines based on '\n' and string width.
        '''
        recetas = """-1. El paciente sufre de escoliosis multiple. 
        \n0. Tambien sufre de dolor emocional.
        \n1.
        \n2.
        \n3.
        \n4.
        \n5.
        \n6.
        \n7.
        \n8.
        \n9.
        \n10."""
        '''
        if recetas:
            canvas.setFont("Garamond", 20) #Font type, font size.
            lines = recetas.split('\n') #Split on \n
            formatted_lines = [] #List of str.

            for line in lines:
                formatted_lines.extend(textwrap.wrap(line, width = 45)) # 50

            formatted_lines = formatted_lines[:12] #Max lines. Set to [:] for inf lines.
            canvas.drawString(x_left-10, 592, formatted_lines[0])
            for n, l in enumerate(formatted_lines[1:], 1):
                canvas.drawString(x_left-75, 592 - (n*32), l)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ##END DATA WRITE

        canvas.save()


#Dummy data for testing.
"""data = {'Timestamp': ['2022-02-22 12:00:00', '2022-02-22 12:30:00'],
        'Nombre': ['Juan', 'María'],
        'Apellidos': ['Pérez', 'García'],
        'RUT o N° Pasaporte': ['12345678-9', 'ABC123456'],
        'Número de Teléfono': ['+56 9 12345678', '+56 9 87654321'],
        'Edad': [30, 25]}

dataframe = pd.DataFrame(data)
pdf = GeneradorPDF(dataframe, 0)
"""