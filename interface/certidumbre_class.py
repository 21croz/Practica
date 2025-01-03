import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import filedialog, ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 880        
original_df = None
df = None
options = []
options_footprint = []
z_height_footprint = None
dataframes_study_cases = []
iterations_path = None
cases_folder = None
COLORFRAME1 = '#404040'
COLORFRAME2 = '#4f4f4f'
label_style = {
    'bg': COLORFRAME1,
    'fg': '#ffffff',
    'font': ('Arial', 12)
}
button_style = {
    'bg': '#ffad33',
    'fg': '#000000',
    'width': 16,
    'font': ('Arial', 11),
    'border': 0,
    'cursor': 'hand2'
}
entry_style = {
    'width': 5,
    'justify': 'center'
}
button_frame_style = {
    'highlightbackground': "#e68a00",
    'highlightcolor': "#e68a00",
    'highlightthickness': 3,
    'bd': 0
}


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Certidumbre')
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)

        self.menu_bar = tk.Menu(root)
        self.menu_file = tk.Menu(self.menu_bar, tearoff = 0)
        self.menu_file.add_command(label = 'Open File', command = self.open_file)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Exit', command = root.quit)
        self.menu_bar.add_cascade(label = 'File', menu = self.menu_file)
        self.root.config(menu = self.menu_bar)

        self.create_widgets()


    def create_widgets(self):
        self.frame_sensitivity = tk.Frame(root, bg = COLORFRAME1, width=WINDOW_WIDTH // 4)
        self.frame_sensitivity.pack(side='left', fill='both')
        self.frame_graph = tk.Frame(root, bg = COLORFRAME2, width=WINDOW_WIDTH*3 // 4)
        self.frame_graph.pack(side='left', fill='both')

        self.frame_xyzcu = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_xyzcu.pack()
        self.frame_x = tk.Frame(self.frame_xyzcu, bg = COLORFRAME1)
        self.frame_x.pack(pady = 3)
        self.frame_y = tk.Frame(self.frame_xyzcu, bg = COLORFRAME1)
        self.frame_y.pack(pady = 3)
        self.frame_z = tk.Frame(self.frame_xyzcu, bg = COLORFRAME1)
        self.frame_z.pack(pady = 3)
        self.frame_cu = tk.Frame(self.frame_xyzcu, bg = COLORFRAME1)
        self.frame_cu.pack(pady = 3)

        self.label_x = tk.Label(self.frame_x, text='X coordinate', **label_style).pack(side='left')
        self.combobox_x = ttk.Combobox(self.frame_x, values = options, state='readonly', width = 10, justify = 'center')
        self.combobox_x.pack(side='left')

        self.label_y = tk.Label(self.frame_y, text='Y coordinate', **label_style).pack(side='left')
        self.combobox_y = ttk.Combobox(self.frame_y, values = options, state='readonly', width = 10, justify = 'center')
        self.combobox_y.pack(side='left')

        self.label_z = tk.Label(self.frame_z, text='Z coordinate', **label_style).pack(side='left')
        self.combobox_z = ttk.Combobox(self.frame_z, values = options, state='readonly', width = 10, justify = 'center')
        self.combobox_z.pack(side='left')

        self.label_cu = tk.Label(self.frame_cu, text='Metal grade', **label_style).pack(side='left')
        self.combobox_cu = ttk.Combobox(self.frame_cu, values = options, state='readonly', width = 10, justify = 'center')
        self.combobox_cu.pack(side='left')

        self.frame_graph_buttons = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_graph_buttons.pack()
        self.frame_button_3d_graph = tk.Frame(self.frame_graph_buttons, **button_frame_style)
        self.frame_button_3d_graph.pack(padx = 10, pady = 15, side = 'left')
        self.button_3d_graph = tk.Button(self.frame_button_3d_graph, text='3D Graph', command = self.graph_3d, **button_style)
        self.button_3d_graph.pack()
        self.frame_button_2d_graph = tk.Frame(self.frame_graph_buttons, **button_frame_style)
        self.frame_button_2d_graph.pack(padx = 10, pady = 15, side='left')
        self.button_2d_graph = tk.Button(self.frame_button_2d_graph, text='Footprint graph', command = self.graph_footp, **button_style)
        self.button_2d_graph.pack()

        self.frame_price_general = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_price_general.pack(pady = 10)
        self.label_price = tk.Label(self.frame_price_general, text = 'Price (usd/lb)', **label_style).pack()
        self.frame_price = tk.Frame(self.frame_price_general, bg = COLORFRAME1)
        self.frame_price.pack()
        self.frame_price_lower = tk.Frame(self.frame_price, bg = COLORFRAME1)
        self.frame_price_lower.pack(padx = 10, side='left')
        self.label_price_lower = tk.Label(self.frame_price_lower, text = 'Min', bg=COLORFRAME1, fg = '#ffffff').pack()
        self.entry_price_lower = tk.Entry(self.frame_price_lower, **entry_style)
        self.entry_price_lower.pack()
        self.frame_price_upper = tk.Frame(self.frame_price, bg = COLORFRAME1)
        self.frame_price_upper.pack(padx = 10, side='left')
        self.label_price_upper = tk.Label(self.frame_price_upper, text = 'Max', bg=COLORFRAME1, fg = '#ffffff').pack()
        self.entry_price_upper = tk.Entry(self.frame_price_upper, **entry_style)
        self.entry_price_upper.pack()
        self.frame_price_step = tk.Frame(self.frame_price, bg = COLORFRAME1)
        self.frame_price_step.pack(padx = 10, side='left')
        self.label_price_step = tk.Label(self.frame_price_step, text = 'Step', bg=COLORFRAME1, fg = '#ffffff').pack()
        self.entry_price_step = tk.Entry(self.frame_price_step, **entry_style)
        self.entry_price_step.pack()

        self.frame_minecost_general = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_minecost_general.pack(pady = 10)
        self.label_mine_cost = tk.Label(self.frame_minecost_general, text = 'Mine cost (usd/t)', **label_style).pack()
        self.frame_minecost = tk.Frame(self.frame_minecost_general, bg = COLORFRAME1)
        self.frame_minecost.pack()
        self.frame_minecost_lower = tk.Frame(self.frame_minecost, bg = COLORFRAME1)
        self.frame_minecost_lower.pack(padx = 10, side='left')
        self.label_minecost_lower = tk.Label(self.frame_minecost_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_minecost_lower = tk.Entry(self.frame_minecost_lower, **entry_style)
        self.entry_minecost_lower.pack()
        self.frame_minecost_upper = tk.Frame(self.frame_minecost, bg = COLORFRAME1)
        self.frame_minecost_upper.pack(padx = 10, side='left')
        self.label_minecost_upper = tk.Label(self.frame_minecost_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_minecost_upper = tk.Entry(self.frame_minecost_upper, **entry_style)
        self.entry_minecost_upper.pack()
        self.frame_minecost_step = tk.Frame(self.frame_minecost, bg = COLORFRAME1)
        self.frame_minecost_step.pack(padx = 10, side='left')
        self.label_minecost_step = tk.Label(self.frame_minecost_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_minecost_step = tk.Entry(self.frame_minecost_step, **entry_style)
        self.entry_minecost_step.pack()

        self.frame_plantcost_general = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_plantcost_general.pack(pady = 10)
        self.label_plant_cost = tk.Label(self.frame_plantcost_general, text = 'Plant cost (usd/t)', **label_style).pack()
        self.frame_plantcost = tk.Frame(self.frame_plantcost_general, bg = COLORFRAME1)
        self.frame_plantcost.pack()
        self.frame_plantcost_lower = tk.Frame(self.frame_plantcost, bg = COLORFRAME1)
        self.frame_plantcost_lower.pack(padx = 10, side='left')
        self.label_plantcost_lower = tk.Label(self.frame_plantcost_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_plantcost_lower = tk.Entry(self.frame_plantcost_lower, **entry_style)
        self.entry_plantcost_lower.pack()
        self.frame_plantcost_upper = tk.Frame(self.frame_plantcost, bg = COLORFRAME1)
        self.frame_plantcost_upper.pack(padx = 10, side='left')
        self.label_plantcost_upper = tk.Label(self.frame_plantcost_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_plantcost_upper = tk.Entry(self.frame_plantcost_upper, **entry_style)
        self.entry_plantcost_upper.pack()
        self.frame_plantcost_step = tk.Frame(self.frame_plantcost, bg = COLORFRAME1)
        self.frame_plantcost_step.pack(padx = 10, side='left')
        self.label_plantcost_step = tk.Label(self.frame_plantcost_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_plantcost_step = tk.Entry(self.frame_plantcost_step, **entry_style)
        self.entry_plantcost_step.pack()

        self.frame_discountrate_general = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_discountrate_general.pack(pady = 10)
        self.label_discount_rate = tk.Label(self.frame_discountrate_general, text = 'Discount rate (%)', **label_style).pack()
        self.frame_discountrate = tk.Frame(self.frame_discountrate_general, bg = COLORFRAME1)
        self.frame_discountrate.pack()
        self.frame_discountrate_lower = tk.Frame(self.frame_discountrate, bg = COLORFRAME1)
        self.frame_discountrate_lower.pack(padx = 10, side='left')
        self.label_discountrate_lower = tk.Label(self.frame_discountrate_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_discountrate_lower = tk.Entry(self.frame_discountrate_lower, **entry_style)
        self.entry_discountrate_lower.pack()
        self.frame_discountrate_upper = tk.Frame(self.frame_discountrate, bg = COLORFRAME1)
        self.frame_discountrate_upper.pack(padx = 10, side='left')
        self.label_discountrate_upper = tk.Label(self.frame_discountrate_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_discountrate_upper = tk.Entry(self.frame_discountrate_upper, **entry_style)
        self.entry_discountrate_upper.pack()
        self.frame_discountrate_step = tk.Frame(self.frame_discountrate, bg = COLORFRAME1)
        self.frame_discountrate_step.pack(padx = 10, side='left')
        self.label_discountrate_step = tk.Label(self.frame_discountrate_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_discountrate_step = tk.Entry(self.frame_discountrate_step, **entry_style)
        self.entry_discountrate_step.pack()

        self.frame_recovery_general = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_recovery_general.pack(pady = 10)
        self.label_recovery = tk.Label(self.frame_recovery_general, text = 'Recovery (%)', **label_style).pack()
        self.frame_recovery = tk.Frame(self.frame_recovery_general, bg = COLORFRAME1)
        self.frame_recovery.pack()
        self.frame_recovery_lower = tk.Frame(self.frame_recovery, bg = COLORFRAME1)
        self.frame_recovery_lower.pack(padx = 10, side='left')
        self.label_recovery_lower = tk.Label(self.frame_recovery_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_recovery_lower = tk.Entry(self.frame_recovery_lower, **entry_style)
        self.entry_recovery_lower.pack()
        self.frame_recovery_upper = tk.Frame(self.frame_recovery, bg = COLORFRAME1)
        self.frame_recovery_upper.pack(padx = 10, side='left')
        self.label_recovery_upper = tk.Label(self.frame_recovery_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_recovery_upper = tk.Entry(self.frame_recovery_upper, **entry_style)
        self.entry_recovery_upper.pack()
        self.frame_recovery_step = tk.Frame(self.frame_recovery, bg = COLORFRAME1)
        self.frame_recovery_step.pack(padx = 10, side='left')
        self.label_recovery_step = tk.Label(self.frame_recovery_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_recovery_step = tk.Entry(self.frame_recovery_step, **entry_style)
        self.entry_recovery_step.pack()

        self.frame_selling_cost_general = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_selling_cost_general.pack(pady = 10)
        self.label_selling_cost = tk.Label(self.frame_selling_cost_general, text = 'Selling cost (usd/lb)', **label_style).pack()
        self.frame_selling_cost = tk.Frame(self.frame_selling_cost_general, bg = COLORFRAME1)
        self.frame_selling_cost.pack()
        self.frame_selling_cost_lower = tk.Frame(self.frame_selling_cost, bg = COLORFRAME1)
        self.frame_selling_cost_lower.pack(padx = 10, side='left')
        self.label_selling_cost_lower = tk.Label(self.frame_selling_cost_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_sellingcost_lower = tk.Entry(self.frame_selling_cost_lower, **entry_style)
        self.entry_sellingcost_lower.pack()
        self.frame_selling_cost_upper = tk.Frame(self.frame_selling_cost, bg = COLORFRAME1)
        self.frame_selling_cost_upper.pack(padx = 10, side='left')
        self.label_selling_cost_upper = tk.Label(self.frame_selling_cost_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_sellingcost_upper = tk.Entry(self.frame_selling_cost_upper, **entry_style)
        self.entry_sellingcost_upper.pack()
        self.frame_selling_cost_step = tk.Frame(self.frame_selling_cost, bg = COLORFRAME1)
        self.frame_selling_cost_step.pack(padx = 10, side='left')
        self.label_selling_cost_step = tk.Label(self.frame_selling_cost_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
        self.entry_sellingcost_step = tk.Entry(self.frame_selling_cost_step, **entry_style)
        self.entry_sellingcost_step.pack()

        self.frame_iterations = tk.Frame(self.frame_sensitivity, bg = COLORFRAME1)
        self.frame_iterations.pack()
        self.frame_button_iterations = tk.Frame(self.frame_iterations, **button_frame_style)
        self.frame_button_iterations.pack(pady=15)
        self.button_iterations = tk.Button(self.frame_button_iterations, text = 'Iterate', command = self.verify_iterations, **button_style)
        self.button_iterations.pack()
        self.progress_bar = ttk.Progressbar(self.frame_iterations, orient='horizontal', length = 200)
        self.progress_bar.pack()

        percentage = tk.StringVar()
        self.label_percentage = tk.Label(self.frame_iterations, textvariable=percentage, bg=COLORFRAME1, fg='#ffffff', font=('Courier New', 10))
        self.label_percentage.pack(pady = 2)
        percentage.set("0.00 %")

        self.frame_graph_footprint = tk.Frame(self.frame_sensitivity, **button_frame_style)
        self.frame_graph_footprint.pack(pady = 15)
        self.button_graph_footprint = tk.Button(self.frame_graph_footprint, text = 'Graph', state='disabled', command = self.footprint_button, **button_style)
        self.button_graph_footprint.pack()


    def open_file(self):
        """
        Abre un archivo excel.
        """
        file_path = filedialog.askopenfilename(title = 'Open File')
        if file_path:
            self.original_df = pd.read_csv(file_path)
            self.df = pd.read_csv(file_path)
            self.options = list(self.df)
        
        self.reset_combobox()
        messagebox.showinfo("SUCCESS", "File loaded successfully")
        self.button_graph_footprint.config(state='disabled')


    def reset_combobox(self):
        """
        Crea nuevamente los cuadros para seleccionar las variables
        de los encabezados del archivo.
        """
        self.combobox_x.destroy()
        self.combobox_y.destroy()
        self.combobox_z.destroy()
        self.combobox_cu.destroy()

        self.combobox_x = ttk.Combobox(self.frame_x, values = options, state='readonly', width = 10)
        self.combobox_x.pack(side='left')

        self.combobox_y = ttk.Combobox(self.frame_y, values = options, state='readonly', width = 10)
        self.combobox_y.pack(side='left')

        self.combobox_z = ttk.Combobox(self.frame_z, values = options, state='readonly', width = 10)
        self.combobox_z.pack(side='left')

        self.combobox_cu = ttk.Combobox(self.frame_cu, values = options, state='readonly', width = 10)
        self.combobox_cu.pack(side='left')


    def list_percentage(lst: list, num: int):
        """
        Esta funcion calcula el elemento en una posición dada por el numero
        'num', el cual corresponderá a un porcentaje. Si 'num' es 25, la
        función entregará el numero justo en el primer cuarto de los
        elementos. Si 'num' es 0, entregará el primer elemento. Si 'num' es
        100, entregará el último elemento.\n
        Parámetros:\n
        * lst: Lista cualquiera.\n
        * num: Porcentaje (num)%
        """
        if len(lst) == 0:
            return
        
        if num not in [100, 0]:
            return lst[len(lst)*num // 100]
        elif num == 0:
            return lst[0]
        elif num == 100:
            return lst[len(lst)-1]


    def mid_list(lst: list):
        """
        Esta función encuentra el termino del medio en una lista de dimensión n.\n
        * Si n es impar, se encuentra el valor central.
        * Si n es par, se encuentra el valor izquierdo del centro.\n
        Se usa para encontrar el mid_case a la hora de hacer las iteraciones.
        """
        length = len(lst)

        if length % 2 != 0:
            middle_index = length//2
            return lst[middle_index]
        
        first_middle_index = length // 2 - 1
        return lst[first_middle_index]


    def graph_3d(self):
        """
        Crea un gráfico en 3 dimensiones usando las
        columnas x, y, z, ley del archivo importado,
        además. Hecho mediante el paquete
        matplotlib.
        """
        self.filter_value()

        for widget in self.frame_graph.winfo_children():
            widget.destroy()

        self.x_data = df.loc[:, combobox_x.get()].tolist()
        self.y_data = df.loc[:, combobox_y.get()].tolist()
        self.z_data = df.loc[:, combobox_z.get()].tolist()
        self.cu_data = df.loc[:, combobox_cu.get()].tolist()

        self.fig = Figure(figsize=(10, 4), dpi = 100)
        self.ax = self.fig.add_subplot(111, projection = '3d')

        self.ax.scatter(self.x_data, self.y_data, self.z_data, c = self.cu_data, cmap = 'RdYlBu', marker = 'o', s = 50)
        self.ax.set_title('Block model')
        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.set_zlabel('Z Axis')

        self.canvas_3dgraph = FigureCanvasTkAgg(self.fig, master = self.frame_graph)
        self.canvas_3dgraph.draw()
        self.canvas_3dgraph.get_tk_widget().pack(fill = 'both', expand = True)


    def graph_footp(self):
        """
        Crea el grafico en 2D del footprint.
        """
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
        
        self.filter_value()

        self.x_data = df.loc[:, combobox_x.get()].tolist()
        self.y_data = df.loc[:, combobox_y.get()].tolist()
        self.value_data = df['valor']

        self.fig = Figure(figsize=(10,4), dpi = 100)
        self.ax = self.fig.add_subplot(111)
        self.ax.scatter(self.x_data, self.y_data, marker = 'o')
        self.ax.set_title('Footprint')
        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.legend()

        self.canvas_footprint_graph = FigureCanvasTkAgg(self.fig, master = self.frame_graph)
        self.canvas_footprint_graph.draw()
        self.canvas_footprint_graph.get_tk_widget().pack(fill = 'both', expand=True)


    def filter_value(self):
        """
        Filtra los bloques con un valor 'antes_max' igual a 1,
        es decir, los que serán económicamente rentables de
        extraer.
        """
        df = df.loc[df['antes_max'] > 0]


    def length_product(lista: list):
            """
            Función de ayuda para la barra de progreso.\n
            Calcula la cantidad de archivos que creará la funcion
            iterations(), en base a eso, se define después el
            incremento de la barra de progreso.
            """
            total_length = 1
            for item in lista:
                total_length = total_length*len(item)
            return total_length


    def files_number(self):
        """
        Esta función entrega el número de archivos que se crearán en las
        iteraciones. El cálculo se hace en base al largo de los intervalos
        que se elijan para los parámetros (precio, costo mina, costo
        planta, etc.)
        """
        self.price_lower = float(self.entry_price_lower.get())
        self.price_upper = float(self.entry_price_upper.get())
        self.price_step = float(self.entry_price_step.get())
        self.minecost_lower = float(self.entry_minecost_lower.get())
        self.minecost_upper = float(self.entry_minecost_upper.get())
        self.minecost_step = float(self.entry_minecost_step.get())
        self.plantcost_lower = float(self.entry_plantcost_lower.get())
        self.plantcost_upper = float(self.entry_plantcost_upper.get())
        self.plantcost_step = float(self.entry_plantcost_step.get())
        self.discount_lower = float(self.entry_discountrate_lower.get())
        self.discount_upper = float(self.entry_discountrate_upper.get())
        self.discount_step = float(self.entry_discountrate_step.get())
        self.recovery_lower = float(self.entry_recovery_lower.get())
        self.recovery_upper = float(self.entry_recovery_upper.get())
        self.recovery_step = float(self.entry_recovery_step.get())
        self.sell_low = float(self.entry_sellingcost_lower.get())
        self.sell_upper = float(self.entry_sellingcost_upper.get())
        self.sell_step = float(self.entry_sellingcost_step.get())

        self.price_range = np.arange(self.price_lower, self.price_upper + self.price_step, self.price_step)
        self.mine_cost_range = np.arange(self.minecost_lower, self.minecost_upper + self.minecost_step, self.minecost_step)
        self.plant_cost_range = np.arange(self.plantcost_lower, self.plantcost_upper + self.plantcost_step, self.plantcost_step)
        self.discount_rate_range = np.arange(self.discount_lower, self.discount_upper + self.discount_step, self.discount_step)
        self.recovery_range = np.arange(self.recovery_lower, self.recovery_upper + self.recovery_step, self.recovery_step)
        self.sell_cost_range = np.arange(self.sell_low, self.sell_upper + self.sell_step, self.sell_step)

        return self.length_product([
            self.price_range,
            self.mine_cost_range,
            self.plant_cost_range,
            self.discount_rate_range,
            self.recovery_range,
            self.sell_cost_range
        ])


    def iterations(self):
        """
        Realiza iteraciones dentro de un intervalo, variando
        el precio del cobre, costo de mina, costo de planta,
        tasa de descuento, recuperación y costo de refinación
        y venta.
        Los archivos creados tienen los campos:
        * x: Coordenada x.
        * y: Coordenada y.
        * z: Coordenada z.
        * ley: Porcentaje de cobre de cada bloque
        * antes_max: 
        * periodo: Año en el que se extraerá el bloque
        * valor: Ingreso que se obtendrá al vender el bloque en el instante 0.
        * VAN: Ingreso descontado tras extraer el bloque

        Luego de definir los archivos, llama a la función save_csv().
        """
        self.price_lower = float(self.entry_price_lower.get())
        self.price_upper = float(self.entry_price_upper.get())
        self.price_step = float(self.entry_price_step.get())
        self.minecost_lower = float(self.entry_minecost_lower.get())
        self.minecost_upper = float(self.entry_minecost_upper.get())
        self.minecost_step = float(self.entry_minecost_step.get())
        self.plantcost_lower = float(self.entry_plantcost_lower.get())
        self.plantcost_upper = float(self.entry_plantcost_upper.get())
        self.plantcost_step = float(self.entry_plantcost_step.get())
        self.discount_lower = float(self.entry_discountrate_lower.get())
        self.discount_upper = float(self.entry_discountrate_upper.get())
        self.discount_step = float(self.entry_discountrate_step.get())
        self.recovery_lower = float(self.entry_recovery_lower.get())
        self.recovery_upper = float(self.entry_recovery_upper.get())
        self.recovery_step = float(self.entry_recovery_step.get())
        self.sell_low = float(self.entry_sellingcost_lower.get())
        self.sell_upper = float(self.entry_sellingcost_upper.get())
        self.sell_step = float(self.entry_sellingcost_step.get())

        self.price_range = np.arange(self.price_lower, self.price_upper + self.price_step, self.price_step)
        self.mine_cost_range = np.arange(self.minecost_lower, self.minecost_upper + self.minecost_step, self.minecost_step)
        self.plant_cost_range = np.arange(self.plantcost_lower, self.plantcost_upper + self.plantcost_step, self.plantcost_step)
        self.discount_rate_range = np.arange(self.discount_lower, self.discount_upper + self.discount_step, self.discount_step)
        self.recovery_range = np.arange(self.recovery_lower, self.recovery_upper + self.recovery_step, self.recovery_step)
        self.sell_cost_range = np.arange(self.sell_low, self.sell_upper + self.sell_step, self.sell_step)

        iterations_number = self.length_product([
            self.price_range,
            self.mine_cost_range,
            self.plant_cost_range,
            self.discount_rate_range,
            self.recovery_range,
            self.sell_cost_range
        ])

        self.progress_bar['maximum'] = iterations_number

        progress_index = 1
        sc = 1
        for sell_cost in self.sell_cost_range:
            r = 1
            for rec in self.recovery_range:
                d = 1
                for i in self.discount_rate_range:
                    pco = 1
                    for pc in self.plant_cost_range:
                        mco = 1
                        for mc in self.mine_cost_range:
                            pr = 1
                            for price in self.price_range:
                                data_saved = {
                                    'x': df[combobox_x.get()],
                                    'y': df[combobox_y.get()],
                                    'z': df[combobox_z.get()],
                                    'ley': df[combobox_cu.get()],
                                    'antes_max': df['antes_max'],
                                    'periodo': df['Period']
                                }
                                df_saved = pd.DataFrame(data_saved)
                                # EL VOLUMEN DEL BLOQUE ES 10X10X10, SE ASUME DENSIDAD DE 2.7
                                df_saved['valor'] = calculate_block_value(price, sell_cost, 1000*2.7, rec, df_saved['ley'], mc, pc)
                                df_saved['valor_descontado'] = df_saved['valor']/((1 + i/100)**df_saved['periodo'])

                                iterations_operations(df_saved)

                                csv_name = f"pr{pr}mc{mco}pc{pco}d{d}r{r}sc{sc}.csv"

                                if sell_cost == min(self.sell_cost_range) and rec == max(self.recovery_range) and i == min(self.discount_rate_range) and pc == min(self.plant_cost_range) and mc == min(self.mine_cost_range) and price == max(self.price_range):
                                    worst_mid_best_case(df_saved, f"{cases_folder}/BEST.csv")
                                elif sell_cost == max(self.sell_cost_range) and rec == min(self.recovery_range) and i == max(self.discount_rate_range) and pc == max(self.plant_cost_range) and mc == max(self.mine_cost_range) and price == min(self.price_range):
                                    worst_mid_best_case(df_saved, f"{cases_folder}/WORST.csv")
                                elif sell_cost == list_percentage(self.sell_cost_range, 75) and rec == list_percentage(self.recovery_range, 25) and i == list_percentage(self.discount_rate_range, 25) and pc == list_percentage(self.plant_cost_range, 75) and mc == list_percentage(self.mine_cost_range, 75) and price == list_percentage(self.price_range, 25):
                                    worst_mid_best_case(df_saved, f"{cases_folder}/MIDCASE25.csv")
                                elif sell_cost == list_percentage(self.sell_cost_range, 50) and rec == list_percentage(self.recovery_range, 50) and i == list_percentage(self.discount_rate_range, 50) and pc == list_percentage(self.plant_cost_range, 50) and mc == list_percentage(self.mine_cost_range, 50) and price == list_percentage(self.price_range, 50):
                                    worst_mid_best_case(df_saved, f"{cases_folder}/MIDCASE50.csv")
                                elif sell_cost == list_percentage(self.sell_cost_range, 25) and rec == list_percentage(self.recovery_range, 75) and i == list_percentage(self.discount_rate_range, 75) and pc == list_percentage(self.plant_cost_range, 25) and mc == list_percentage(self.mine_cost_range, 25) and price == list_percentage(self.price_range, 75):
                                    worst_mid_best_case(df_saved, f"{cases_folder}/MIDCASE75.csv")
                                else:
                                    save_csv(df_saved, f"{iterations_path}/{csv_name}")
                                progress_bar['value'] = progress_index
                                percentage.set(f"{(progress_index/iterations_number)*100:.2f} %")
                                root.update_idletasks()
                                progress_index += 1
                                pr += 1
                            mco += 1
                        pco += 1
                    d += 1
                r += 1
            sc += 1
        
        self.finish_iterations()


    def finish_iterations(self):
        """
        Deifne los parámetros que cambiarán luego de terminar
        de iterar.
        """
        self.progress_bar['value'] = 0
        self.percentage.set("0.00 %")
        self.button_iterations.config(state='normal')
        self.button_graph_footprint.config(state = 'normal')


    def clear_files(path):
        """
        Esta función verifica si la carpeta 'iteraciones' contiene archivos, en caso de
        tener los elimina para luego almacenar las nuevas iteraciones.
        """
        self.files = os.listdir(path)

        if self.files:
            for folder_file in self.files:
                file_path = os.path.join(path, folder_file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        self.path2 = f"{path}/cases"
        
        if not os.path.exists(self.path2):
            os.makedirs(self.path2)

        self.files = os.listdir(path)

        if self.files:
            for folder_file in self.files:
                file_path = os.path.join(self.path2, folder_file)
                if os.path.isfile(file_path):
                    os.remove(file_path)


    def save_csv(self, df, file_name):
        """
        Guarda los archivos hechos en las iteraciones
        """
        df.to_csv(file_name, index = False)


    def group_columns(df):
        """
        Esta función crea un diccionario de dataframes con cada fila del dataframe inicial.
        Los dataframes creados tienen las mismas coordenadas x e y, de este modo se
        puede realizar un análisis sobre cada columna (distinta cota o eje z). 
        """
        columns_filter = df.groupby(['x', 'y'])
        column_dataframes = {group: group_df for group, group_df in columns_filter}
        return column_dataframes


    def calculate_block_value(price:float, selling_cost:float, tonnage:float, recovery:int, grade:float, mine_cost:float, plant_cost:float):
        """
        Esta función calcula el beneficio que se obtendrá tras extraer un bloque
        """
        income = (price - selling_cost)*tonnage*(recovery/100)*(grade/100)*2204.63
        outcome = (mine_cost + plant_cost)*tonnage
        return income - outcome


    def iterations_operations(df_saved):
        """
        Esta funcion establece las operaciones que se harán en cada iteración sobre el dataframe.
        * Verifica si el valor de un bloque es positivo o negativo, si es positivo, escribe un 1 en
        la columna 'antes_max'
        """
        df_saved['antes_max'] = (df_saved['valor'] > 0).astype(int)


    def verify_iterations(self):
        """
        Luego de presionar el boton para realizar las iteraciones, se crea un mensaje que advierte
        al usuario sobre la cantidad de archivo y su tamaño total en el disco.
        """
        file_number = self.files_number()
        answer = messagebox.askokcancel("Confirm", f"Se crearán {file_number+3} archivos. ({round(((file_number+3)*1000/1024)/1024, 2)} Gb).")
        if answer:
            self.button_iterations.config(state='disabled')
            path = self.select_iterations_path()
            self.iterations()


    def select_iterations_path(self):
        """
        Define la carpeta en donde se guardarán las
        iteraciones.
        """
        self.iterations_path = filedialog.askdirectory(title = "Folder to save iterations")
        cases_folder = os.path.join(iterations_path, "cases")
        self.clear_files(iterations_path)
        self.clear_files(cases_folder)


    def worst_mid_best_case(self, df, file_name):
        global cases_folder
        
        if not os.path.exists(cases_folder):
            os.makedirs(cases_folder)
        df.to_csv(file_name, index = False)


    def footprint_button(self):
        """
        Función ligada al botón "Graph", establece las funciones que
        se ejecutarán tras presionar el botón.
        """
        self.footprint_graph_window()


    def build_graph_footprint(self):
        """
        Creación del gráfico del footprint teniendo en cuenta la cota
        seleccionada en el cuadro desplegable.
        """
        dataframes_modified = []
        z_height_footprint = combobox_cota_z.get()
        for df in dataframes_study_cases:
            dataframes_modified.append(df[df['z'] == int(z_height_footprint)])

        self.plt.figure()
        self.plt.scatter(dataframes_modified[0]['x'].tolist(), dataframes_modified[0]['y'].tolist(), s=250, color='#00ff00', label="Best Case")  # BEST CASE
        self.plt.scatter(dataframes_modified[3]['x'].tolist(), dataframes_modified[3]['y'].tolist(), s=200, color='#40bf00', label="Q75 Case")  # MID 75 CASE
        self.plt.scatter(dataframes_modified[2]['x'].tolist(), dataframes_modified[2]['y'].tolist(), s=150, color='#808000', label="Q50 Case")  # MID 50 CASE
        self.plt.scatter(dataframes_modified[1]['x'].tolist(), dataframes_modified[1]['y'].tolist(), s=100, color='#bf4000', label="Q25 Case")  # MID 25 CASE
        self.plt.scatter(dataframes_modified[4]['x'].tolist(), dataframes_modified[4]['y'].tolist(), s=50, color='#ff0000', label="Worst Case")  # WORST CASE
        self.plt.title("Footprint Graph")
        self.plt.legend()
        self.plt.xlabel("X")
        self.plt.ylabel("Y")
        self.plt.grid(True)
        self.plt.show()


    def footprint_graph_window(self):
        """
        Crea la ventana nueva al presionar el botón 'Graph'.
        """
        def read_dataframes():
            """
            Lee los archivos .csv (Best Case, Worst Case y cuartiles 25 50 y 75).
            """
            for file in os.listdir(cases_folder):
                full_path = os.path.join(cases_folder, file)
                if os.path.isfile(full_path):
                    df = pd.read_csv(full_path, sep=',')
                    dataframes_study_cases.append(df[df['antes_max'] == 1])

        def set_options_combobox():
            """
            Configura las opciones del texto desplegable
            """
            for df in dataframes_study_cases:
                for element in df['z']:
                    if element not in options_footprint:
                        options_footprint.append(element)
        
        footprint_window = tk.Toplevel(root)
        footprint_window.title('Footprint Graph')
        footprint_window.geometry('300x200')

        read_dataframes()
        set_options_combobox()

        frame_new_window_z_height = tk.Frame(footprint_window)
        frame_new_window_z_height.pack()
        frame_new_window_graph = tk.Frame(footprint_window)
        frame_new_window_graph.pack()
        label_new_window_z_height = tk.Label(frame_new_window_z_height, text = 'Z Coordniates', font = ('Arial', 20))
        label_new_window_z_height.pack()

        global combobox_cota_z
        combobox_cota_z = ttk.Combobox(frame_new_window_z_height, values = options_footprint, state='readonly', font = ('Arial', 20), width = 10, justify='center')
        combobox_cota_z.pack()
        boton_graficar = tk.Button(frame_new_window_z_height, text = 'Graficar', font = ('Arial', 20), command = self.build_graph_footprint)
        boton_graficar.pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()