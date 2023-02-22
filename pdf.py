from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from datetime import datetime
import pandas as pd

outfile = "resultado.pdf"

modelo = PdfReader("Modelo_Receta_Villegas.pdf", decompress = False).pages[0]
modelo_obj = pagexobj(modelo)

canvas = Canvas(outfile)

xobj_name = makerl(canvas, modelo_obj)
canvas.doForm(xobj_name)

y_top = 675
y_bottom = 655

x_left = 135
x_right = 405

# Leer .csv
df = pd.read_csv('Antecedentes Adulto.csv')

# Select specific row.
row = df.iloc[1]

# Extract values from row + col
nombre = row['Nombre']
apellidos =  row['Apellidos']
run = row['RUT o N° Pasaporte']
direccion = row['Número de Teléfono']
edad = row['Edad']

##START DATA ENTRY
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nombre_apellido = nombre + ' ' + apellidos
canvas.drawString(x_left, y_top, nombre_apellido)

canvas.drawString(x_right, y_top, run)

canvas.drawString(x_left, y_bottom, str(direccion))

canvas.drawString(x_right, y_bottom, str(edad))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##END DATA ENTRY

canvas.save()