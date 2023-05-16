from flask import Flask, send_file
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

app = Flask(__name__)

@app.get("/")
def root():
    return {
        'hola':'hola',
    }

@app.get("/generar-codigo/<texto>")
def generar_codigo_barras(texto):
    # Crear el objeto de código de barras
    codigo_barras = Code128(texto, writer=ImageWriter())

    # Generar la imagen del código de barras en memoria
    buffer = BytesIO()
    codigo_barras.write(buffer)
    buffer.seek(0)
    img = ImageReader(buffer)
    #obtener ancho y alto de la imagen
    img_w, img_h = img.getSize()

    #crear pdf
    w, h = A4
    pdf = canvas.Canvas('pdf/' + texto + ".pdf",  pagesize=A4)

    #Insertar data al pdf
    center_img_w = (w-img_w)/2
    pdf.drawImage(img, center_img_w, h - img_h)
    pdf.showPage()
    pdf.save()

    PATH = 'pdf/' + str(texto) + '.pdf'

    # Enviar la imagen como respuesta al usuario
    return send_file(PATH)

if __name__ == "__main__":
    app.run()
