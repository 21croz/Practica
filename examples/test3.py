import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


def abrir_carpeta():
    path = filedialog.askdirectory(title = "Abrir carpeta")
    verificar_creacion_archivos(path)

def verificar_creacion_archivos(path):
    answer = messagebox.askokcancel("Confirmar", "Se creará 1 archivo")
    if answer:
        crear_archivo(path)

def crear_archivo(path):
    directorio = Path(path)
    nombre_archivo = "Holamundo.txt"

    ruta_completa = directorio / nombre_archivo
    with ruta_completa.open("w") as archivo:
        archivo.write("Hola mundo\n")


root = tk.Tk()
root.geometry("200x200")
root.configure(bg = '#1a1a1a')

button_border = tk.Frame(root,
                        highlightbackground="#37d3ff",
                        highlightcolor="#37d3ff",
                        highlightthickness=4,
                        bd=0)
button_border.pack(pady = 50)

button = tk.Button(button_border, text = 'Botón',
                   command = abrir_carpeta,
                   bg = '#3c93c9',
                   fg = '#ffffff',
                   font = ('Arial', 15),
                   width = 10,
                   cursor = 'hand2',
                   border = 0)
button.pack()

root.mainloop()