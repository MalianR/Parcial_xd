import PyPDF2
from tkinter import filedialog
import tkinter as tk

def recortar_pdf(archivo_entrada, pagina_inicio, pagina_fin, archivo_salida):
    with open(archivo_entrada, 'rb') as entrada:
        lector = PyPDF2.PdfFileReader(entrada)
        escritor = PyPDF2.PdfFileWriter()
        
        for num_pagina in range(pagina_inicio - 1, pagina_fin):
            escritor.addPage(lector.getPage(num_pagina))
        
        with open(archivo_salida, 'wb') as salida:
            escritor.write(salida)

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename()
    return archivo

def seleccionar_directorio():
    root = tk.Tk()
    root.withdraw()
    directorio = filedialog.askdirectory()
    return directorio

def main():
    # Solicitar al usuario que seleccione el archivo PDF
    archivo_entrada = seleccionar_archivo()

    # Solicitar al usuario que ingrese el rango de páginas
    pagina_inicio = int(input("Ingresa el número de página inicial: "))
    pagina_fin = int(input("Ingresa el número de página final: "))

    # Solicitar al usuario que seleccione la ubicación de salida
    directorio_salida = seleccionar_directorio()
    archivo_salida = directorio_salida + "/recorte.pdf"

    # Recortar el PDF
    recortar_pdf(archivo_entrada, pagina_inicio, pagina_fin, archivo_salida)
    print(f"El PDF recortado ha sido guardado en: {archivo_salida}")

if __name__ == "__main__":
    main()
