import tkinter as tk                                            # Importa la librería de interfaz gráfica.
import pandas as pd                                             # Importa la librería de manejo de datos.
import matplotlib.pyplot as plt                                 # Importa la librería de graficación.
import os                                                       # Importa la librería de manejo de archivos.
import numpy as np                                              # Importa la librería de cálculos y herramientas matemáticas.

from tkinter import ttk, filedialog, messagebox                 # Importa submódulos de la librería de interfaz gráfica.
from matplotlib.figure import Figure                            # Importa la clase Figure de la librería de graficación.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Importa la clase FigureCanvasTkAgg de la librería de graficación.
from math import floor                                          # Importa el paquete floor de la librería math, usado para los cálculos.
from itertools import product                                   # Importa el paquete product de la librería itertools, usado para las iteraciones.



class MainApp(tk.Tk):
    """Ventana principal de la aplicación"""

    WINDOW_HEIGHT = 850
    WINDOW_WIDTH = 1250
    BG_COLOR = '#2d3436'

    def __init__(self):
        """Constructor de la aplicación"""
        super().__init__()

        self.title('MainApp')
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.create_control_variables()

        self.create_menubar()
        self.widgets_create()
        self.widgets_layout()


    def create_control_variables(self):
        """Crea las variables de control de la ventana"""
        self.combo_values = []
        self.loaded_dataframe = None
        self.list_entries = []
        self.progressbar_percentage = tk.StringVar()
        self.number_of_files = 0
        self.iterations_done = False


    def create_menubar(self):
        """Crea la barra de menu"""
        self.menu_bar = tk.Menu(self)
        self.menu_file = tk.Menu(self.menu_bar, tearoff = 0)
        self.menu_file.add_command(label = 'Select File', command = self.select_file)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Exit', command = lambda: self.destroy())
        self.menu_bar.add_cascade(label = 'File', menu = self.menu_file)
        self.menu_graph = tk.Menu(self.menu_bar, tearoff = 0)
        self.menu_graph.add_command(label = 'Footprint Graph', command = self.open_footprint_window, state = 'normal')
        self.menu_bar.add_cascade(label = 'Graph', menu = self.menu_graph)
        self.config(menu = self.menu_bar)


    def widgets_create(self):
        """Crea los widgets de la ventana"""
        self.frame_control = tk.Frame(self, width = self.WINDOW_WIDTH//3, bg = self.BG_COLOR)
        self.frame_graph = tk.Frame(self, width = self.WINDOW_WIDTH*2//3, bg = '#636e72')


        self.frame_combo = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_combo_x = tk.Label(self.frame_combo, text = 'X Coordinate', bg = self.BG_COLOR, fg = 'white')
        self.label_combo_y = tk.Label(self.frame_combo, text = 'Y Coordinate', bg = self.BG_COLOR, fg = 'white')
        self.label_combo_z = tk.Label(self.frame_combo, text = 'Z Coordinate', bg = self.BG_COLOR, fg = 'white')
        self.label_combo_cu = tk.Label(self.frame_combo, text = 'Metal grade', bg = self.BG_COLOR, fg = 'white')
        self.combo_x = ttk.Combobox(self.frame_combo, values = self.combo_values, state = 'readonly', width = 10, justify = 'center')
        self.combo_y = ttk.Combobox(self.frame_combo, values = self.combo_values, state = 'readonly', width = 10, justify = 'center')
        self.combo_z = ttk.Combobox(self.frame_combo, values = self.combo_values, state = 'readonly', width = 10, justify = 'center')
        self.combo_cu = ttk.Combobox(self.frame_combo, values = self.combo_values, state = 'readonly', width = 10, justify = 'center')


        self.frame_graph_buttons = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.button_3d_graph = AppButton(self.frame_graph_buttons, text = '3D Graph', command = self.plot_columns_3d)
        self.button_footprint_graph = AppButton(self.frame_graph_buttons, text = 'Footprint Graph', command = self.plot_footprint)


        self.frame_price = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_price = tk.Label(self.frame_price, text = 'Price (usd/lb)', bg = self.BG_COLOR, fg = 'white')
        self.label_price_min = tk.Label(self.frame_price, text = 'Min', bg = self.BG_COLOR, fg = 'white')
        self.label_price_max = tk.Label(self.frame_price, text = 'Max', bg = self.BG_COLOR, fg = 'white')
        self.label_price_step = tk.Label(self.frame_price, text = 'Step', bg = self.BG_COLOR, fg = 'white')
        self.entry_price_min = tk.Entry(self.frame_price, width = 5)
        self.entry_price_max = tk.Entry(self.frame_price, width = 5)
        self.entry_price_step = tk.Entry(self.frame_price, width = 5)


        self.frame_minecost = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_minecost = tk.Label(self.frame_minecost, text = 'Mine cost (usd/ton)', bg = self.BG_COLOR, fg = 'white')
        self.label_minecost_min = tk.Label(self.frame_minecost, text = 'Min', bg = self.BG_COLOR, fg = 'white')
        self.label_minecost_max = tk.Label(self.frame_minecost, text = 'Max', bg = self.BG_COLOR, fg = 'white')
        self.label_minecost_step = tk.Label(self.frame_minecost, text = 'Step', bg = self.BG_COLOR, fg = 'white')
        self.entry_minecost_min = tk.Entry(self.frame_minecost, width = 5)
        self.entry_minecost_max = tk.Entry(self.frame_minecost, width = 5)
        self.entry_minecost_step = tk.Entry(self.frame_minecost, width = 5)


        self.frame_plantcost = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_plantcost = tk.Label(self.frame_plantcost, text = 'Plant cost (usd/ton)', bg = self.BG_COLOR, fg = 'white')
        self.label_plantcost_min = tk.Label(self.frame_plantcost, text = 'Min', bg = self.BG_COLOR, fg = 'white')
        self.label_plantcost_max = tk.Label(self.frame_plantcost, text = 'Max', bg = self.BG_COLOR, fg = 'white')
        self.label_plantcost_step = tk.Label(self.frame_plantcost, text = 'Step', bg = self.BG_COLOR, fg = 'white')
        self.entry_plantcost_min = tk.Entry(self.frame_plantcost, width = 5)
        self.entry_plantcost_max = tk.Entry(self.frame_plantcost, width = 5)
        self.entry_plantcost_step = tk.Entry(self.frame_plantcost, width = 5)


        self.frame_discountrate = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_discountrate = tk.Label(self.frame_discountrate, text = 'Discount rate (%)', bg = self.BG_COLOR, fg = 'white')
        self.label_discountrate_min = tk.Label(self.frame_discountrate, text = 'Min', bg = self.BG_COLOR, fg = 'white')
        self.label_discountrate_max = tk.Label(self.frame_discountrate, text = 'Max', bg = self.BG_COLOR, fg = 'white')
        self.label_discountrate_step = tk.Label(self.frame_discountrate, text = 'Step', bg = self.BG_COLOR, fg = 'white')
        self.entry_discountrate_min = tk.Entry(self.frame_discountrate, width = 5)
        self.entry_discountrate_max = tk.Entry(self.frame_discountrate, width = 5)
        self.entry_discountrate_step = tk.Entry(self.frame_discountrate, width = 5)


        self.frame_recovery = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_recovery = tk.Label(self.frame_recovery, text = 'Recovery (%)', bg = self.BG_COLOR, fg = 'white')
        self.label_recovery_min = tk.Label(self.frame_recovery, text = 'Min', bg = self.BG_COLOR, fg = 'white')
        self.label_recovery_max = tk.Label(self.frame_recovery, text = 'Max', bg = self.BG_COLOR, fg = 'white')
        self.label_recovery_step = tk.Label(self.frame_recovery, text = 'Step', bg = self.BG_COLOR, fg = 'white')
        self.entry_recovery_min = tk.Entry(self.frame_recovery, width = 5)
        self.entry_recovery_max = tk.Entry(self.frame_recovery, width = 5)
        self.entry_recovery_step = tk.Entry(self.frame_recovery, width = 5)


        self.frame_sellcost = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        self.label_sellcost = tk.Label(self.frame_sellcost, text = 'Selling cost (usd/ton)', bg = self.BG_COLOR, fg = 'white')
        self.label_sellcost_min = tk.Label(self.frame_sellcost, text = 'Min', bg = self.BG_COLOR, fg = 'white')
        self.label_sellcost_max = tk.Label(self.frame_sellcost, text = 'Max', bg = self.BG_COLOR, fg = 'white')
        self.label_sellcost_step = tk.Label(self.frame_sellcost, text = 'Step', bg = self.BG_COLOR, fg = 'white')
        self.entry_sellcost_min = tk.Entry(self.frame_sellcost, width = 5)
        self.entry_sellcost_max = tk.Entry(self.frame_sellcost, width = 5)
        self.entry_sellcost_step = tk.Entry(self.frame_sellcost, width = 5)

        
        self.button_iterate = AppButton(self.frame_control, text = 'Iterate', command = self.sensitivity_analysis)

        self.progressbar_iterations = ttk.Progressbar(self.frame_control, orient='horizontal', length = 200)
        self.label_progressbar_percentage = tk.Label(self.frame_control, textvariable = self.progressbar_percentage, font = ('Courier New', 8), bg = self.BG_COLOR, fg = 'white')

        self.progressbar_percentage.set("0.0 %")


    def widgets_layout(self):
        """Coloca los widgets en la ventana"""
        self.frame_control.pack(side='left', fill = 'both', expand=True)
        self.frame_graph.pack(side='left', fill = 'both', expand=True)


        self.frame_combo.pack(pady = 10, padx = 10)

        self.label_combo_x.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.label_combo_y.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.label_combo_z.grid(row = 2, column = 0, padx = 5, pady = 5)
        self.label_combo_cu.grid(row = 3, column = 0, padx = 5, pady = 5)
        self.combo_x.grid(row = 0, column = 1, pady = 5)
        self.combo_y.grid(row = 1, column = 1, pady = 5)
        self.combo_z.grid(row = 2, column = 1, pady = 5)
        self.combo_cu.grid(row = 3, column = 1, pady = 5)

        
        self.frame_graph_buttons.pack(pady = 10, padx = 10)

        self.button_3d_graph.grid(row = 0, column = 0, pady = 5, padx = 5)
        self.button_footprint_graph.grid(row = 0, column = 1, pady = 5, padx = 5)

        
        self.frame_price.pack(pady = 5, padx = 10)

        self.label_price.grid(columnspan = 3, row = 0, column = 0, pady = (10, 0), padx = 10)
        self.label_price_min.grid(row = 1, column = 0, padx = 10)
        self.label_price_max.grid(row = 1, column = 1, padx = 10)
        self.label_price_step.grid(row = 1, column = 2, padx = 10)
        self.entry_price_min.grid(row = 2, column = 0, padx = 10)
        self.entry_price_max.grid(row = 2, column = 1, padx = 10)
        self.entry_price_step.grid(row = 2, column = 2, padx = 10)


        self.frame_minecost.pack(pady = 5, padx = 10)

        self.label_minecost.grid(columnspan = 3, row = 0, column = 0, pady = (10, 0), padx = 10)
        self.label_minecost_min.grid(row = 1, column = 0, padx = 10)
        self.label_minecost_max.grid(row = 1, column = 1, padx = 10)
        self.label_minecost_step.grid(row = 1, column = 2, padx = 10)
        self.entry_minecost_min.grid(row = 2, column = 0, padx = 10)
        self.entry_minecost_max.grid(row = 2, column = 1, padx = 10)
        self.entry_minecost_step.grid(row = 2, column = 2, padx = 10)


        self.frame_plantcost.pack(pady = 5, padx = 10)

        self.label_plantcost.grid(columnspan = 3, row = 0, column = 0, pady = (10, 0), padx = 10)
        self.label_plantcost_min.grid(row = 1, column = 0, padx = 10)
        self.label_plantcost_max.grid(row = 1, column = 1, padx = 10)
        self.label_plantcost_step.grid(row = 1, column = 2, padx = 10)
        self.entry_plantcost_min.grid(row = 2, column = 0, padx = 10)
        self.entry_plantcost_max.grid(row = 2, column = 1, padx = 10)
        self.entry_plantcost_step.grid(row = 2, column = 2, padx = 10)


        self.frame_discountrate.pack(pady = 5, padx = 10)

        self.label_discountrate.grid(columnspan = 3, row = 0, column = 0, pady = (10, 0), padx = 10)
        self.label_discountrate_min.grid(row = 1, column = 0, padx = 10)
        self.label_discountrate_max.grid(row = 1, column = 1, padx = 10)
        self.label_discountrate_step.grid(row = 1, column = 2, padx = 10)
        self.entry_discountrate_min.grid(row = 2, column = 0, padx = 10)
        self.entry_discountrate_max.grid(row = 2, column = 1, padx = 10)
        self.entry_discountrate_step.grid(row = 2, column = 2, padx = 10)


        self.frame_recovery.pack(pady = 5, padx = 10)

        self.label_recovery.grid(columnspan = 3, row = 0, column = 0, pady = (10, 0), padx = 10)
        self.label_recovery_min.grid(row = 1, column = 0, padx = 10)
        self.label_recovery_max.grid(row = 1, column = 1, padx = 10)
        self.label_recovery_step.grid(row = 1, column = 2, padx = 10)
        self.entry_recovery_min.grid(row = 2, column = 0, padx = 10)
        self.entry_recovery_max.grid(row = 2, column = 1, padx = 10)
        self.entry_recovery_step.grid(row = 2, column = 2, padx = 10)


        self.frame_sellcost.pack(pady = 5, padx = 10)

        self.label_sellcost.grid(columnspan = 3, row = 0, column = 0, pady = (10, 0), padx = 10)
        self.label_sellcost_min.grid(row = 1, column = 0, padx = 10)
        self.label_sellcost_max.grid(row = 1, column = 1, padx = 10)
        self.label_sellcost_step.grid(row = 1, column = 2, padx = 10)
        self.entry_sellcost_min.grid(row = 2, column = 0, padx = 10)
        self.entry_sellcost_max.grid(row = 2, column = 1, padx = 10)
        self.entry_sellcost_step.grid(row = 2, column = 2, padx = 10)


        self.button_iterate.pack(pady = (45, 5), padx = 10)
        self.progressbar_iterations.pack(padx = 10)
        self.label_progressbar_percentage.pack(padx = 10)


    def list_entries_append(self):
        """Agrega las entradas a una lista para su posterior uso."""
        self.list_entries.append([])
        self.list_entries[0].append(float(self.entry_price_min.get()))
        self.list_entries[0].append(float(self.entry_price_max.get()))
        self.list_entries[0].append(float(self.entry_price_step.get()))

        self.list_entries.append([])
        self.list_entries[1].append(float(self.entry_minecost_min.get()))
        self.list_entries[1].append(float(self.entry_minecost_max.get()))
        self.list_entries[1].append(float(self.entry_minecost_step.get()))
        
        self.list_entries.append([])
        self.list_entries[2].append(float(self.entry_plantcost_min.get()))
        self.list_entries[2].append(float(self.entry_plantcost_max.get()))
        self.list_entries[2].append(float(self.entry_plantcost_step.get()))
        
        self.list_entries.append([])
        self.list_entries[3].append(float(self.entry_discountrate_min.get()))
        self.list_entries[3].append(float(self.entry_discountrate_max.get()))
        self.list_entries[3].append(float(self.entry_discountrate_step.get()))
        
        self.list_entries.append([])
        self.list_entries[4].append(float(self.entry_recovery_min.get()))
        self.list_entries[4].append(float(self.entry_recovery_max.get()))
        self.list_entries[4].append(float(self.entry_recovery_step.get()))
        
        self.list_entries.append([])
        self.list_entries[5].append(float(self.entry_sellcost_min.get()))
        self.list_entries[5].append(float(self.entry_sellcost_max.get()))
        self.list_entries[5].append(float(self.entry_sellcost_step.get()))


    def select_file(self):
        """Selecciona el archivo principal de datos que se usará para los cálculos."""
        file_path = filedialog.askopenfilename(title = 'Open File')
        if file_path:
            self.loaded_dataframe = pd.read_csv(file_path)
            self.combo_values = self.loaded_dataframe.columns.tolist()
            self.combo_x.config(values = self.combo_values)
            self.combo_y.config(values = self.combo_values)
            self.combo_z.config(values = self.combo_values)
            self.combo_cu.config(values = self.combo_values)

            messagebox.showinfo('Open File', 'File loaded successfully')


    def delete_graph(self):
        """Elimina el gráfico de la ventana."""
        for widget in self.frame_graph.winfo_children():
            widget.destroy()


    def plot_columns_3d(self):
        """Grafica las columnas de la base de datos en 3D."""

        self.delete_graph()

        ploted_dataframe = self.loaded_dataframe.copy()
        ploted_dataframe = ploted_dataframe.loc[ploted_dataframe['antes_max'] == 1]

        x_data = ploted_dataframe[self.combo_x.get()]
        y_data = ploted_dataframe[self.combo_y.get()]
        z_data = ploted_dataframe[self.combo_z.get()]
        cu_data = ploted_dataframe[self.combo_cu.get()]

        fig = Figure(figsize = (10, 4), dpi = 100)

        ax = fig.add_subplot(111, projection = '3d')

        ax.scatter(x_data, y_data, z_data, c = cu_data, cmap = 'viridis', marker = 'o', s = 50)
        ax.set_title('3D Graph')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')

        canvas_3d_graph = FigureCanvasTkAgg(fig, master = self.frame_graph)
        canvas_3d_graph.draw()
        canvas_3d_graph.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)


    def plot_footprint(self):
        """Grafica las columnas de la base de datos en un footprint."""
        
        self.delete_graph()

        plotted_dataframe = self.loaded_dataframe.copy()
        plotted_dataframe = plotted_dataframe.loc[plotted_dataframe['antes_max'] == 1]

        x_data = plotted_dataframe[self.combo_x.get()]
        y_data = plotted_dataframe[self.combo_y.get()]

        fig = Figure(figsize = (10, 4), dpi = 100)
        ax = fig.add_subplot(111)

        ax.scatter(x_data, y_data, c = 'blue', marker = 'o', s = 50)
        ax.set_title('Footprint Graph')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')

        canvas_footprint_graph = FigureCanvasTkAgg(fig, master = self.frame_graph)
        canvas_footprint_graph.draw()
        canvas_footprint_graph.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)


    def sensitivity_analysis(self):
        """Funcion principal de análisis de sensibilidad. Se usa el método de la certidumbre, 
        en donde se varían los parámetros de entrada para obtener un rango de resultados."""
        self.warning_message_iterations()


    def warning_message_iterations(self):
        """Muestra un mensaje de advertencia al usuario cuando se intenta cerrar la ventana durante el proceso de iteraciones."""
        file_number, files_size = self.iterations_result_files()
        self.number_of_files = file_number

        string_file_number = f'{file_number:,}'.replace(',', '.')
        if files_size < 1024:
            string_files_size = f'{files_size:,.2f}'.replace(',', '.')
            string_files_size += ' Gb'
        else:
            string_files_size = f'{(files_size/1024):,.2f}'.replace(',', '.')
            string_files_size += ' Tb'

        iterate_time = self.convert_time(file_number*305/5511)

        answer = messagebox.askyesno(
            'Warning',
            f'Iterations will be made.\n{string_file_number} files will be created ({string_files_size} aproximately).\nIt will take aproximately {iterate_time}')

        if answer:
            self.iterations()
        else:
            return
    

    def convert_time(self, time: int):
        """
        Funcion que transforma un tiempo en segundos a dias, horas, minutos, segundos.
        
        Inputs:
            * time: Tiempo en segundos.
        
        Outputs:
            * string_time: String que contiene el tiempo de la siguiente forma: [  ]d [  ]h [  ]m [  ]s
        
        Ejemplo de uso:
            >>> self.convert_time(90061)
            "1d 1h 1m 1s"

        """
        days = time // 86400
        time %= 86400
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        string_time_days = f'{int(days):,}'.replace(',', '.')
        string_time_hours = f'{int(hours):,}'.replace(',', '.')
        string_time_minutes = f'{int(minutes):,}'.replace(',', '.')
        string_time_seconds = f'{int(time):,}'.replace(',', '.')
        string_time = f'{string_time_days}d {string_time_hours}h {string_time_minutes}m {string_time_seconds}s'
        return string_time


    def iterations_result_files(self):
        """Entrega el número de archivos que se crearán al realizar las iteraciones, además de un aproximado del peso de la 
        carpeta que los contendrá."""
        self.list_entries = []
        self.list_entries_append()

        elements_in_range = []
        
        for elem in self.list_entries:
            elements_in_range.append(np.arange(elem[0], elem[1] + elem[2], elem[2]))

        total_length = len(elements_in_range[0])*len(elements_in_range[1])*len(elements_in_range[2])*len(elements_in_range[3])*len(elements_in_range[4])*len(elements_in_range[5])
        
        return total_length, ((total_length + 5)*1000/1024)/1024


    def iterations(self):
        """Proceso de iteraciones para el análisis de sensibilidad."""
        
        self.verify_folder()

        parameters_ranges = [
            np.arange(self.list_entries[0][0], self.list_entries[0][1] + self.list_entries[0][2], self.list_entries[0][2]),
            np.arange(self.list_entries[1][0], self.list_entries[1][1] + self.list_entries[1][2], self.list_entries[1][2]),
            np.arange(self.list_entries[2][0], self.list_entries[2][1] + self.list_entries[2][2], self.list_entries[2][2]),
            np.arange(self.list_entries[3][0], self.list_entries[3][1] + self.list_entries[3][2], self.list_entries[3][2]),
            np.arange(self.list_entries[4][0], self.list_entries[4][1] + self.list_entries[4][2], self.list_entries[4][2]),
            np.arange(self.list_entries[5][0], self.list_entries[5][1] + self.list_entries[5][2], self.list_entries[5][2])]

        combinations = self.create_combinations(parameters_ranges)

        self.progressbar_iterations['maximum'] = self.number_of_files
        progress_index = 1

        for price, m_cost, p_cost, discount, recov, sell_c in combinations:
            saved_data = {
                'x': self.loaded_dataframe[self.combo_x.get()],
                'y': self.loaded_dataframe[self.combo_y.get()],
                'z': self.loaded_dataframe[self.combo_z.get()],
                'grade': self.loaded_dataframe[self.combo_cu.get()],
                'period': self.loaded_dataframe['Period'],
                'antes_max': self.loaded_dataframe['antes_max']
            }
            df_saved = pd.DataFrame(saved_data)

            # El volumen del bloque es 10x10x10, se asume densidad de 2.7
            volume = 1000

            df_saved['value'] = self.calculate_block_value(price, sell_c, volume, 2.7, recov, df_saved['grade'], m_cost, p_cost)
            df_saved['disc_value'] = df_saved['value']/((1 + discount/100) ** df_saved['period'])
            df_saved['antes_max'] = (df_saved['value'] > 0).astype(int)

            file_name = f'p{price}mc{m_cost}pc{p_cost}d{discount}r{recov}sc{sell_c}.csv'

            case = self.set_study_case(parameters_ranges, price, m_cost, p_cost, discount, recov, sell_c)

            if case != '':
                self.save_file(df_saved, f'{case}.csv', normal = False)
                case = ''

            self.save_file(df_saved, file_name, normal = True)

            # Se actualiza la barra de progreso
            self.progressbar_iterations['value'] = progress_index
            self.progressbar_percentage.set(f'{(progress_index/self.number_of_files)*100:.1f} %')
            self.update_idletasks()
            progress_index += 1

        self.finish_iterate()


    def set_antes_max(self, df):
        """
        Esta funcion modifica la columna 'antes_max' del dataframe.
        * Se hace un filtro en cada elemento, se agrupan los que tienen igual coordenada (x, y), de esta forma se aisla cada columna.
        * Se realiza la suma acumulada del valor descontado en cada columna.
        * Se identifica el valor máximo del valor acumulado en cada columna.
        * Se asigna el valor de 1 a cada fila de la columna, desde la base hasta el valor máximo encontrado.
        """

        return


    def list_percentage(self, lst:list, perc:tuple|int):
        """
        Esta funcion retorna el elemento en la posición del porcentaje dado.
        Si se selecciona perc = 50, retornará el elemento en la mitad de la lista.
        Si se selecciona perc = 0, retornará el primer elemento.
        Si se selecciona perc = 100, retornará el último elemento.

        Inputs:
        * lst: Lista con los elementos.
        * perc: Porcentaje de la lista al cual se quiere retorar el elemento. Debe estar en el rango [0, 100]

        Outputs:
        * num: Elemento en la posición seleccionada.

        Ejemplo de uso:
        >>> self.list_percentage([1, 2, 3, 4, 5, 6, 7, 8, 9], 50)
        5
        >>> self.list_percentage([1, 2, 3, 4, 5, 6, 7, 8, 9], 100)
        9
        >>> self.list_percentage([1, 2, 3, 4, 5, 6, 7, 8, 9], 0)
        1
        """
        if isinstance(perc, tuple):
            values = []
            for num in perc:
                if not (0 <= num <= 100):
                    raise ValueError(f'perc, must be in interval [0, 100]')

                if len(lst) == 0:
                    values.append(0)
                
                if num == 100:
                    values.append(lst[-1])
                else:
                    values.append(lst[len(lst)*num // 100])
            
            return values
        
        elif isinstance(perc, int):
            if not (0 <= perc <= 100):
                raise ValueError(f'perc, must be in interval [0, 100]')

            if len(lst) == 0:
                return 0
            
            if perc == 100:
                return lst[-1]
            else:
                return lst[len(lst)*perc // 100]


    def set_study_case(self, parameters_range:list, price:float, mine_cost:float, plant_cost:float, discount:int, recovery:int, sell_cost:float):
        """
        Esta funcion ayuda a seleccionar la iteración con la que se está trabajando, si corresponde al Best Case, Worst Case, o casos intermedios
        
        Inputs:
        * parameters_range: Lista que en cada elemento posee una lista, estos elementos son el rango en el que se moverá cada uno de los parámetros.
        * price: Precio del metal.
        * mine_cost: Costo de minado del metal.
        * plant_cost: Costo de planta del metal.
        * discount: Tasa de descuento.
        * recovery: Recuperación de metal.
        * sell_cost: Costo de venta del metal.

        Outputs:
        * -> strings: ['best', 'worst', 'mid25', 'mid50', 'mid75']
        """
        
        # Lista con parámetros actuales:
        list_scenario = [price, mine_cost, plant_cost,
                         discount, recovery, sell_cost]
        
        # Recuperar minimos, maximos:
        min_price, max_price = parameters_range[0][0], parameters_range[0][-1]
        min_mine_cost, max_mine_cost = parameters_range[1][0], parameters_range[1][-1]
        min_plant_cost, max_plant_cost = parameters_range[2][0], parameters_range[2][-1]
        min_discount, max_discount = parameters_range[3][0], parameters_range[3][-1]
        min_recovery, max_recovery = parameters_range[4][0], parameters_range[4][-1]
        min_sell_cost, max_sell_cost = parameters_range[5][0], parameters_range[5][-1]

        # Recuperar casos intermedios:
        price_25, price_50, price_75 = self.list_percentage(parameters_range[0], (25, 50, 75))
        mine_cost_25, mine_cost_50, mine_cost_75 = self.list_percentage(parameters_range[1], (25, 50, 75))
        plant_cost_25, plant_cost_50, plant_cost_75 = self.list_percentage(parameters_range[2], (25, 50, 75))
        discount_25, discount_50, discount_75 = self.list_percentage(parameters_range[3], (25, 50, 75))
        recovery_25, recovery_50, recovery_75 = self.list_percentage(parameters_range[4], (25, 50, 75))
        sell_cost_25, sell_cost_50, sell_cost_75 = self.list_percentage(parameters_range[5], (25, 50, 75))

        # Listas con las definiciones de cada escenario:
        list_best = [max_price, min_mine_cost, min_plant_cost,
                    min_discount, max_recovery, min_sell_cost]
        
        list_worst = [min_price, max_mine_cost, max_plant_cost,
                      max_discount, min_recovery, max_sell_cost]
        
        list_midcase_25 = [price_25, mine_cost_25, plant_cost_25,
                           discount_25, recovery_25, sell_cost_25]

        list_midcase_50 = [price_50, mine_cost_50, plant_cost_50,
                           discount_50, recovery_50, sell_cost_50]

        list_midcase_75 = [price_75, mine_cost_75, plant_cost_75,
                           discount_75, recovery_75, sell_cost_75]
        
        # Evaluar cada escenario
        if list_scenario == list_best:
            return 'best'
        
        elif list_scenario == list_worst:
            return 'worst'
        
        elif list_scenario == list_midcase_25:
            return 'mid25'
        
        elif list_scenario == list_midcase_50:
            return 'mid50'

        elif list_scenario == list_midcase_75:
            return 'mid75'
        else:
            return ''


    def finish_iterate(self):
        """Esta función se ejecuta al terminar las iteraciones"""
        messagebox.showinfo('SUCCESS', 'Iterations completed')
        self.progressbar_iterations['value'] = 0
        self.progressbar_percentage.set('0.0 %')
        self.menu_graph.entryconfig(0, state = 'normal')
        self.iterations_done = True


    def verify_folder(self):
        """Esta funcion verifica que existan las carpetas donde guardar las iteraciones y los casos especiales.
        Si las carpetas no existen, las crea.
        Si las carpetas ya existen, llama a la funcion >>> self.clear_files() para limpiarla"""

        folder_name_iterations = 'Iterations'

        path = os.path.join('Practica', 'interface', 'data', folder_name_iterations)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            self.clear_files(path)
        
        folder_name_cases = 'Cases'
        
        path = os.path.join('Practica', 'interface', 'data', folder_name_cases)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            self.clear_files(path)        


    def clear_files(self, path: str):
        """Elimina los archivos dentro de una carpeta.
        
        Inputs:
        * path: Directorio de la carpeta a la cual se le quieren eliminar los archivos."""

        files = os.listdir(path)

        if files:
            for folder_file in files:
                file_path = os.path.join(path, folder_file)
                if os.path.isfile(file_path):
                    os.remove(file_path)


    def save_file(self, df, name:str, normal = True):
        """
        Esta función guarda los dataframes creados en la carpeta iterations y cases dentro de la carpeta data.
        
        Inputs:
        * name: Nombre que tendrá el archivo (debe contener la extensión)
        * normal: Define si el archivo se creará en la carpeta iterations o en la carpeta cases. True es para una
        iteración normal, False es para los casos de estudio (best case, worst case, mid case)

        Outputs:
        * Se crea un archivo dentro de una de las carpetas iterations o cases (dependiendo del parámetro normal).
        """
        if normal:
            path = os.path.join('Practica', 'interface', 'data', 'iterations')
            if not os.path.exists(path):
                os.makedirs(path)

            file_path = os.path.join(path, name)
            df.to_csv(file_path, index = False)
            return
        else:
            path = os.path.join('Practica', 'interface', 'data', 'cases')
            if not os.path.exists(path):
                os.makedirs(path)

            file_path = os.path.join(path, name)
            df.to_csv(file_path, index = False)
            return


    def calculate_block_value(self, price:int|float, sell_cost:int|float, volume:int|float, density:int|float, recovery:int, grade:int|float, mine_cost:int|float, plant_cost:int|float):
        """
        Esta funcion calcula el valor de un bloque dados los parámetros económicos.

        Inputs:
        * price: Precio del metal (usd/lb).
        * sell_cost: Precio de venta del metal (usd/lb).
        * volume: Volumen del bloque en el modelo de bloques (m3).
        * density: Densidad del material (t/m^3).
        * recovery: Recuperación de metal (%).
        * grade: Concentración de metal (%).
        * mine_cost: Costo de mina ($/t).
        * plant_cost: Costo de planta ($/t).

        Outputs:
        * income - outcome: Valor del bloque

        Ejemplo de uso:
            >>> self.calculate_block_value(4, 1, 1000, 2.7, 85, 1, 19, 22)
            41,088.78
        """
        income = (price - sell_cost)*volume*density*(recovery/100)*(grade/100)*2204.63
        outcome = (mine_cost + plant_cost)*volume*density
        return income - outcome


    def create_combinations(self, list_of_lists):
        """
        Crea combinaciones entre cada elemento de las listas que se ingresen.
        
        Inputs:
        lst: Cantidad cualquiera de listas.

        Output:
        Lista con combinaciones entre los elementos de las listas ingresadas.

        Ejemplo de uso:
            >>> self.create_combinations([1, 2], ["a", "b", "c"])
            [(1, "a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c")]
        """
        if not list_of_lists:
            return []
        return list(product(*list_of_lists))


    def open_footprint_window(self):
        """Abre la ventana de visualización del grafico de footprint con sus filtros."""
        FootprintWindow(self)


    def on_closing(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        self.quit()



class FootprintWindow(tk.Toplevel):
    """Ventana de visualización del gráfico de footprint con filtros"""
    
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 600
    BG_COLOR = '#2d3436'

    def __init__(self, parent):
        """Constructor de la ventana"""
        super().__init__(parent)
        self.title('Footprint Graph')
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.resizable(False, False)

        self.create_control_variables()
        
        self.create_widgets()
        self.layout_widgets()

        self.define_dataframes()
        self.define_heights()

        self.create_plot_window()
    
    
    def create_control_variables(self):
        """Esta funcion crea las variables de control de la ventana."""
        self.dataframes = []
        self.coordinates = []
        self.heights = []
        self.check_names = ['Best Case', 'Mid case (75%)', 'Mid case (50%)', 'Mid case (25%)', 'Worst case']
        self.graph_colors = ['#00b894', '#ffeaa7', '#0984e3', '#ff7675', '#636e72']
        self.graph_sizes = [375, 300, 225, 150, 75]


    def create_widgets(self):
        """Esta funcion crea los widgets que se verán en la ventana."""
        self.frame_control = tk.Frame(self, bg = self.BG_COLOR, width = self.WINDOW_WIDTH // 3)
        self.frame_graph = tk.Frame(self, bg = '#636e72', width = self.WINDOW_WIDTH * 2 // 3)

        self.label_level = tk.Label(self.frame_control, text = 'Height Z', bg = self.BG_COLOR, fg = 'white')
        self.combo_level = ttk.Combobox(self.frame_control, values = self.heights, state = 'readonly', width = 10)

        self.check_state = [tk.BooleanVar(value = False) for _ in range(5)]

        self.frame_check = tk.Frame(self.frame_control, bg = self.BG_COLOR)

        for i, label in enumerate(self.check_names):
            self.label = tk.Label(self.frame_check, text = label, bg = self.BG_COLOR, fg = 'white')
            self.label.grid(row = i, column = 0)
            self.checkbutton_filter = ttk.Checkbutton(self.frame_check, variable = self.check_state[i])
            self.checkbutton_filter.grid(row = i, column = 1, pady = 5)

        self.refresh_button = AppButton(self.frame_control, text = 'Refresh', command = self.update_plot)


    def layout_widgets(self):
        """Esta funcion coloca los widgets creados, en la ventana."""
        self.frame_control.pack(side = 'left', fill = 'both', expand = True)
        self.frame_graph.pack(side = 'left', fill = 'both', expand = True)

        self.label_level.pack(pady = (20, 5))
        self.combo_level.pack(pady = (5, 20))

        self.frame_check.pack(pady = (20, 10))

        self.refresh_button.pack(pady = 10)


    def define_dataframes(self):
        """Esta funcion importa los dataframes de la carpeta 'cases' en la variable >>> self.dataframes."""
        folder_path = os.path.join('Practica', 'interface', 'data', 'cases')
        try:
            csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

            for file in csv_files:
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                self.dataframes.append(df[df['antes_max'] == 1])

        except Exception as e:
            messagebox.showerror("Error", "An error has happened when trying to read files in 'cases'")


    def define_coordinates(self):
        """Esta funcion filtra las coordenadas de los dataframes de acuerdo con la coordenada Z que se
        ingrese en el menú desplegable, ubicado en la parte superior izquierda de la ventana"""
        for df in self.dataframes:
            self.coordinates.append(df[df['z'] == int(self.combo_level.get())])


    def define_heights(self):
        """Esta funcion define las alturas que se mostrarán en el menú desplegable."""
        list_heights = []
        for i in range(5):
            list_heights += self.dataframes[i]['z'].tolist()
        
        self.combo_level["values"] = (sorted(list(set(list_heights))))


    def create_plot_window(self):
        """Esta funcion crea la zona en donde se creará el gráfico."""
        self.fig, self.ax = plt.subplots(figsize = (6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_graph)
        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)


    def update_plot(self):
        """Esta funcion actualiza el gráfico de acuerdo a los filtros puestos por el usuario."""

        self.define_coordinates()        

        self.ax.clear()

        for i, show in enumerate(self.check_state):
            if show.get():
                self.ax.scatter(
                    self.coordinates[i]['x'].tolist(),
                    self.coordinates[i]['y'].tolist(),
                    label = self.check_names[i],
                    c = self.graph_colors[i],
                    s = self.graph_sizes[i]
                )
        
        self.ax.set_title('Footprint')
        self.ax.legend()
        self.ax.set_xlabel('X Coordinate')
        self.ax.set_xlabel('Y Coordinate')

        self.canvas.draw()



class AppButton(tk.Frame):
    """Botón personalizado usado dentro de la ventana principal"""
    def __init__(self, parent, text, command = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(
            highlightbackground = '#e84393',    # Color del borde del botón
            highlightthickness = 2,             # Grosor del borde al pasar el mouse
            bd = 0                              # Grosor del borde
            )

        button = tk.Button(
            self,
            text = text,                # Texto del botón
            bg = '#fd79a8',             # Color del botón
            fg = 'black',               # Color del texto del botón
            width = 16,                 # Ancho del botón
            border = 0,                 # Borde del botón
            cursor = 'hand2',           # Cursor al pasar el mouse
            command = command           # Función a ejecutar al hacer click
            )
        button.pack()



if __name__ == '__main__':
    app = MainApp()
    app.mainloop()