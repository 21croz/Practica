import tkinter as tk
import pandas as pd
from tkinter import filedialog, ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tkinter import ttk

df = None


def import_options():
    global df

    file_path = filedialog.askopenfilename(title = 'Open File', filetypes = [('Excel files', '*.csv', 'Text files', '*txt', 'All files', '*.*')])
    if file_path:
        df = pd.read_csv(file_path)
        display_data(df.head(20))
	
    open_file()

def open_file():
    global df
    file_path = filedialog.askopenfilename(title = 'Open File', filetypes = [('Excel files', '*.csv', 'Text files', '*txt', 'All files', '*.*')])
    if file_path:
        df = pd.read_csv(file_path)
        display_data(df.head(20))
        
        bajoTree()

def abrirExcel(): #importar base de datos como archivo excel
	global df
	file_path = filedialog.askopenfilename(title = 'Arbir Excel', filetypes = [('Excel files', '*.csv')])
	if file_path:
		df = pd.read_csv(file_path)
		display_data(df.head(20))

	bajoTree()

def abrirTexto(): #importar base de datos como archivo de texto
	global df
	file_path = filedialog.askopenfilename(title = 'Abrir archivo de texto', filetypes = [('Text files', '*.txt')])
	if file_path:
		df = pd.read_table(file_path, sep = '\t')
		display_data(df.head(20))

	bajoTree()

def display_data(df): #crear la visualización de la base de datos
	for item in tree.get_children():
		tree.delete(item)

	tree['column'] = list(df.columns)
	tree['show'] = 'headings'

	for column in tree['column']:
		tree.heading(column, text = column)
		tree.column(column, width = 50, anchor = 'center')

	for _, row in df.iterrows():
		tree.insert("", "end", values = list(row))

	root.geometry('800x500')

def bajoTree(): #widgets bajo la base de datos
	def toggle_entry():
		if checkvar.get():
			entryDens1.config(state = "normal")
			entryDens2.config(state = 'disabled')
		else:
			entryDens1.config(state = "disabled")
			entryDens2.config(state = 'normal')

	global entryX
	global entryY
	global entryZ
	global entryMin
	global entryTon
	global checkvar
	global entryDens1
	global entryDens2

	labX = tk.Label(frameX, text = 'Coordenada X')
	labX.pack(side = 'left')
	entryX = tk.Entry(frameX, width = 4, justify = 'center', validate = 'key', validatecommand = (validate_cmd, '%P'))
	entryX.pack(side = 'left')

	labY = tk.Label(frameY, text = 'Coordenada Y')
	labY.pack(side = 'left')
	entryY = tk.Entry(frameY, width = 4, justify = 'center', validate = 'key', validatecommand = (validate_cmd, '%P'))
	entryY.pack(side = 'left')

	labZ = tk.Label(frameZ, text = 'Coordenada Z')
	labZ.pack(side = 'left')
	entryZ = tk.Entry(frameZ, width = 4, justify = 'center', validate = 'key', validatecommand = (validate_cmd, '%P'))
	entryZ.pack(side = 'left')

	labMin = tk.Label(frameMin, text = 'Columna Mineral')
	labMin.pack(side = 'left')
	entryMin = tk.Entry(frameMin, width = 4, justify = 'center', validate = 'key', validatecommand = (validate_cmd, '%P'))
	entryMin.pack(side = 'left')

	checkvar = tk.BooleanVar(value = False)
	labDens1 = tk.Label(frameDens1, text = '¿Columna de densidad?')
	labDens1.pack(side = 'left')
	checkbox = ttk.Checkbutton(frameDens1, variable = checkvar, command = toggle_entry)
	checkbox.pack(side = 'left')

	labDens2 = tk.Label(frameDens2, text = 'Columna Densidad')
	labDens2.pack(side = 'left')
	entryDens1 = tk.Entry(frameDens2, width = 4, justify = 'center', validate = 'key', validatecommand = (validate_cmd, '%P'), state = "disabled")
	entryDens1.pack(side = 'left')
	
	labDens3 = tk.Label(frameDens3, text = 'Asumir Densidad')
	labDens3.pack(side = 'left')
	entryDens2 = tk.Entry(frameDens3, width = 4, justify = 'center', validate = 'key', validatecommand = (validate_cmd2, '%P'), state = "normal")
	entryDens2.pack(side = 'left')

	botonModelo = tk.Button(frame2, text = 'Generar modelo', font = ('Calibri', 13), command = grafico3d).pack(side = 'left', padx = 10, pady = 6)
	botonTongrad = tk.Button(frame2, text = 'Generar curva', font = ('Calibri', 13), command = tongrad).pack(side = 'left', padx = 10, pady = 6)

def grafico3d(): #mostrar grafico 3d
	x = int(entryX.get())
	y = int(entryY.get())
	z = int(entryZ.get())
	mineral = int(entryMin.get())

	colX = df.iloc[:, int(x) - 1].tolist()
	colY = df.iloc[:, int(y) - 1].tolist()
	colZ = df.iloc[:, int(z) - 1].tolist()
	colMin = df.iloc[:, int(mineral) - 1].tolist()

	fig = plt.figure()
	ax = fig.add_subplot(111, projection = '3d')

	colores = plt.cm.RdYlBu(colMin)

	scatter = ax.scatter(colX, colY, colZ, c = colMin, cmap = 'RdYlBu', marker = 'o', s = 50)

	cb = plt.colorbar(scatter, ax = ax, pad = 0.1)
	cb.set_label('Ley Cu')

	ax.set_title('Modelo de bloques')
	ax.set_xlabel('Eje x')
	ax.set_ylabel('Eje y')
	ax.set_zlabel('Eje z')

	plt.show()

def tongrad(): #crear y graficar la curva tonelaje ley
	global df

	def dividir_lista(lista, n):
		# Calcular el tamaño de cada subintervalo
		tamaño_subintervalo = len(lista) // n
		residuo = len(lista) % n
		
		primeros = []
		inicio = 0

		for i in range(n):
			# Calcular el tamaño del subintervalo, distribuyendo el residuo
			tamaño_actual = tamaño_subintervalo + (1 if i < residuo else 0)
			if tamaño_actual > 0:  # Asegurarse de no procesar sublistas vacías
				primeros.append(lista[inicio])
			inicio += tamaño_actual

		return primeros

	def promedio(lista):
		return(sum(lista)/len(lista))

	x = int(entryX.get())
	y = int(entryY.get())
	z = int(entryZ.get())
	mineral = int(entryMin.get())
	
	if entryDens1.get() != "":
		densidad = int(entryDens1)
	if entryDens2.get() != "":
		densidad = entryDens2.get()

	#extraer columnas del data frame
	colX = df.iloc[:, x-1].tolist()
	colY = df.iloc[:, y-1].tolist()
	colZ = df.iloc[:, z-1].tolist()
	colMin = df.iloc[:, mineral-1].tolist()
	if checkvar == False:
		colDens = df.iloc[:,densidad-1].tolist()
	else:
		colDens = [float(entryDens2.get())]*len(colX)

	#eliminar valores repetidos para calcular el tamaño del bloque
	colXnr = []
	colYnr = []
	colZnr = []
	[colXnr.append(val) for val in colX if val not in colXnr]
	[colYnr.append(val) for val in colY if val not in colYnr]
	[colZnr.append(val) for val in colZ if val not in colZnr]
	volumenBloque = (abs(sorted(colXnr)[1] - sorted(colXnr)[0]))*(abs(sorted(colYnr)[1] - sorted(colYnr)[0]))*(abs(sorted(colZnr)[1] - sorted(colZnr)[0]))

	#cálculo de la columna de tonelaje
	colTon = []
	for i in range(len(colDens)):
		colTon.append(volumenBloque*colDens[i])

	#ordenar de menor a mayor para hacer el gráfico tonelaje ley
	mineral, tonelaje = (list(t) for t in zip(*sorted(zip(colMin, colTon))))

	ejex = dividir_lista(mineral, 90)
	ejey1 = []
	ejey2 = []
	min_vec = []
	ton_vec = []

	for i in range(len(ejex)):
		for j in range(len(mineral)):
			if mineral[j] >= ejex[i]:
				min_vec.append(mineral[j])
				ton_vec.append(tonelaje[j])
		ejey1.append(sum(ton_vec)/1000000)
		ejey2.append(promedio(min_vec))
		ton_vec = []
		min_vec = []

	fig, ax1 = plt.subplots()

	ax1.plot(ejex, ejey1, 'b', label = 'Tonelaje')
	ax1.set_xlabel('Ley de corte')
	ax1.set_ylabel('Tonelaje [Mt]')
	ax1.tick_params(axis = 'y', labelcolor = 'b')

	ax2 = ax1.twinx()
	ax2.plot(ejex, ejey2, 'r-', label="Ley media")  # Gráfica en rojo
	ax2.set_ylabel("Ley media", color='r')
	ax2.set_ylim([0, max(ejey2)])
	ax2.tick_params(axis='y', labelcolor='r')

	plt.title('TONGRAD')
	plt.show()

def validate_digit(entry_text): #valida la entrada de texto para que solo acepte un dígito entero
    return entry_text.isdigit() and len(entry_text) == 1 or entry_text == ''

def validarDensidad(texto): #validar la entrada de texto para la densidad
	if texto == "":
		return True
	try:
		float(texto)
		return True
	except ValueError:
		return False


root = tk.Tk()
ANCHO = 800
LARGO = 500
root.geometry(f'{ANCHO}x{LARGO}')
root.title('Mindat')
root.resizable(False, False)

validate_cmd = root.register(validate_digit)
validate_cmd2 = root.register(validarDensidad)

menu_bar = tk.Menu(root)

menu_file = tk.Menu(menu_bar, tearoff=0)
menu_file.add_command(label="Open File", command=lambda: messagebox.showinfo("Abrir", "Abrir un archivo"))
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=menu_file)

root.config(menu = menu_bar)

botonExcel = tk.Button(root, text = 'Abrir archivo csv', font = ('Calibri', 13), command = abrirExcel).pack(pady = 10)
botonTexto = tk.Button(root, text = 'Abrir archivo texto', font = ('Calibri', 13), command = abrirTexto).pack(pady = 10)

frameTree = tk.Frame(root)
frameTree.pack(expand = True, fill = 'both', padx = 10, pady = 10)
scrollbar = ttk.Scrollbar(frameTree, orient = 'vertical')
scrollbar.pack(side = 'right', fill = 'y')
tree = ttk.Treeview(frameTree, yscrollcommand = scrollbar.set, height = 2)
tree.pack(side = 'left', expand = True, fill = 'both', pady = 10, padx = 10)
scrollbar.config(command = tree.yview)

frameEntries = tk.Frame(root)
frameEntries.pack(pady = 10)

frameX = tk.Frame(frameEntries)
frameX.pack(side = 'left', padx = 10)
frameY = tk.Frame(frameEntries)
frameY.pack(side = 'left', padx = 10)
frameZ = tk.Frame(frameEntries)
frameZ.pack(side = 'left', padx = 10)
frameMin = tk.Frame(frameEntries)
frameMin.pack(side = 'left', padx = 10)

frameDens1 = tk.Frame(root)
frameDens1.pack(pady = 5)

frameDens2 = tk.Frame(root)
frameDens2.pack(pady = 5)

frameDens3 = tk.Frame(root)
frameDens3.pack(pady = 5)

frame2 = tk.Frame(root)
frame2.pack(pady = 10)

root.mainloop()