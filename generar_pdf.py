from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from datetime import datetime
from dateutil import parser
import pytz
import pandas as pd

class GeneradorPDF:
    def __init__(self, df, row_n):
        self.df : pd.DataFrame = df

        #Outfile name must be data + patient name
        modelo = PdfReader("Modelo_Receta_Villegas_1.pdf", decompress = False).pages[0]
        modelo_obj = pagexobj(modelo)

        #Select specific row
        row = self.df.iloc[row_n]

        #Extract values from row[col]
        fecha = row['Timestamp']
        nombre = row['Nombre']
        apellidos =  row['Apellidos']
        run = row['RUT o N° Pasaporte']
        direccion = row['Número de Teléfono']
        edad = row['Edad']
        nombre_apellido = nombre + ' ' + apellidos

        #Name outfile after date             
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
        canvas.drawString(x_left, y_top, nombre_apellido)

        canvas.drawString(x_right, y_top, run)

        canvas.drawString(x_left, y_bottom, str(direccion))

        canvas.drawString(x_right, y_bottom, str(edad))

        #TODO: Recipe section.
        signature = ImageReader('firma.png')
        signature_width, signature_height = signature.getSize()
        canvas.drawImage(
            signature, 
            width = signature_width/1.3, 
            height = signature_height/1.3, 
            x = 310, 
            y = 132, 
            mask = "auto")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ##END DATA WRITE


        canvas.save()


data = {'Timestamp': ['2022-02-22 12:00:00', '2022-02-22 12:30:00'],
        'Nombre': ['Juan', 'María'],
        'Apellidos': ['Pérez', 'García'],
        'RUT o N° Pasaporte': ['12345678-9', 'ABC123456'],
        'Número de Teléfono': ['+56 9 12345678', '+56 9 87654321'],
        'Edad': [30, 25]}

dataframe = pd.DataFrame(data)
pdf = GeneradorPDF(dataframe, 0)