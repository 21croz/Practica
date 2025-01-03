import tkinter as tk
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import filedialog, ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

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

""""
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Certidumbre')
        WINDOW_WIDTH = 1300
        WINDOW_HEIGHT = 880
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)

        self.menu_bar = tk.Menu(root)
        self.menu_file = tk.Menu(menu_bar, tearoff = 0)
        self.menu_file.add_command(label = 'Open File', command = open_file)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Exit', command = root.quit)
        self.menu_bar.add_cascade(label = 'File', menu = menu_file)
        self.root.config(menu = menu_bar)
"""

def open_file():
    """
    Abre un archivo excel.
    """
    global df
    global options
    global original_df

    file_path = filedialog.askopenfilename(title = 'Open File')
    if file_path:
        original_df = pd.read_csv(file_path)
        df = pd.read_csv(file_path)
        options = list(df)
    
    reset_combobox()
    messagebox.showinfo("SUCCESS", "File loaded successfully")
    button_graph_footprint.config(state='disabled')

def reset_combobox():
    """
    Crea nuevamente los cuadros para seleccionar las variables
    de los encabezados del archivo.
    """
    global combobox_x
    global combobox_y
    global combobox_z
    global combobox_cu

    combobox_x.destroy()
    combobox_y.destroy()
    combobox_z.destroy()
    combobox_cu.destroy()

    combobox_x = ttk.Combobox(frame_x, values = options, state='readonly', width = 10)
    combobox_x.pack(side='left')

    combobox_y = ttk.Combobox(frame_y, values = options, state='readonly', width = 10)
    combobox_y.pack(side='left')

    combobox_z = ttk.Combobox(frame_z, values = options, state='readonly', width = 10)
    combobox_z.pack(side='left')

    combobox_cu = ttk.Combobox(frame_cu, values = options, state='readonly', width = 10)
    combobox_cu.pack(side='left')

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

def graph_3d():
    """
    Crea un gráfico en 3 dimensiones usando las
    columnas x, y, z, ley del archivo importado,
    además. Hecho mediante el paquete
    matplotlib.
    """
    global frame_graph

    filter_value()

    for widget in frame_graph.winfo_children():
        widget.destroy()

    x_data = df.loc[:, combobox_x.get()].tolist()
    y_data = df.loc[:, combobox_y.get()].tolist()
    z_data = df.loc[:, combobox_z.get()].tolist()
    cu_data = df.loc[:, combobox_cu.get()].tolist()

    fig = Figure(figsize=(10, 4), dpi = 100)
    ax = fig.add_subplot(111, projection = '3d')

    ax.scatter(x_data, y_data, z_data, c = cu_data, cmap = 'RdYlBu', marker = 'o', s = 50)
    ax.set_title('Block model')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')

    canvas_3dgraph = FigureCanvasTkAgg(fig, master = frame_graph)
    canvas_3dgraph.draw()
    canvas_3dgraph.get_tk_widget().pack(fill = 'both', expand = True)

def graph_footp():
    """
    Crea el grafico en 2D del footprint.
    """
    for widget in frame_graph.winfo_children():
        widget.destroy()
    
    filter_value()

    x_data = df.loc[:, combobox_x.get()].tolist()
    y_data = df.loc[:, combobox_y.get()].tolist()
    value_data = df['valor']

    fig = Figure(figsize=(10,4), dpi = 100)
    ax = fig.add_subplot(111)
    ax.scatter(x_data, y_data, marker = 'o')
    ax.set_title('Footprint')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.legend()

    canvas_footprint_graph = FigureCanvasTkAgg(fig, master = frame_graph)
    canvas_footprint_graph.draw()
    canvas_footprint_graph.get_tk_widget().pack(fill = 'both', expand=True)

def filter_value():
    """
    Filtra los bloques con un valor 'antes_max' igual a 1,
    es decir, los que serán económicamente rentables de
    extraer.
    """
    global df
    global original_df

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

def files_number():
    """
    Esta función entrega el número de archivos que se crearán en las
    iteraciones. El cálculo se hace en base al largo de los intervalos
    que se elijan para los parámetros (precio, costo mina, costo
    planta, etc.)
    """
    global df
    global combobox_x
    global combobox_y
    global combobox_z
    global combobox_cu

    price_lower = float(entry_price_lower.get())
    price_upper = float(entry_price_upper.get())
    price_step = float(entry_price_step.get())
    minecost_lower = float(entry_minecost_lower.get())
    minecost_upper = float(entry_minecost_upper.get())
    minecost_step = float(entry_minecost_step.get())
    plantcost_lower = float(entry_plantcost_lower.get())
    plantcost_upper = float(entry_plantcost_upper.get())
    plantcost_step = float(entry_plantcost_step.get())
    discount_lower = float(entry_discountrate_lower.get())
    discount_upper = float(entry_discountrate_upper.get())
    discount_step = float(entry_discountrate_step.get())
    recovery_lower = float(entry_recovery_lower.get())
    recovery_upper = float(entry_recovery_upper.get())
    recovery_step = float(entry_recovery_step.get())
    sell_low = float(entry_sellingcost_lower.get())
    sell_upper = float(entry_sellingcost_upper.get())
    sell_step = float(entry_sellingcost_step.get())

    price_range = np.arange(price_lower, price_upper + price_step, price_step)
    mine_cost_range = np.arange(minecost_lower, minecost_upper + minecost_step, minecost_step)
    plant_cost_range = np.arange(plantcost_lower, plantcost_upper + plantcost_step, plantcost_step)
    discount_rate_range = np.arange(discount_lower, discount_upper + discount_step, discount_step)
    recovery_range = np.arange(recovery_lower, recovery_upper + recovery_step, recovery_step)
    sell_cost_range = np.arange(sell_low, sell_upper + sell_step, sell_step)

    return length_product([
        price_range,
        mine_cost_range,
        plant_cost_range,
        discount_rate_range,
        recovery_range,
        sell_cost_range
    ])

def iterations():
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

    global df
    global combobox_x
    global combobox_y
    global combobox_z
    global combobox_cu
    global iterations_path
    global cases_folder

    price_lower = float(entry_price_lower.get())
    price_upper = float(entry_price_upper.get())
    price_step = float(entry_price_step.get())
    minecost_lower = float(entry_minecost_lower.get())
    minecost_upper = float(entry_minecost_upper.get())
    minecost_step = float(entry_minecost_step.get())
    plantcost_lower = float(entry_plantcost_lower.get())
    plantcost_upper = float(entry_plantcost_upper.get())
    plantcost_step = float(entry_plantcost_step.get())
    discount_lower = float(entry_discountrate_lower.get())
    discount_upper = float(entry_discountrate_upper.get())
    discount_step = float(entry_discountrate_step.get())
    recovery_lower = float(entry_recovery_lower.get())
    recovery_upper = float(entry_recovery_upper.get())
    recovery_step = float(entry_recovery_step.get())
    sell_low = float(entry_sellingcost_lower.get())
    sell_upper = float(entry_sellingcost_upper.get())
    sell_step = float(entry_sellingcost_step.get())

    price_range = np.arange(price_lower, price_upper + price_step, price_step)
    mine_cost_range = np.arange(minecost_lower, minecost_upper + minecost_step, minecost_step)
    plant_cost_range = np.arange(plantcost_lower, plantcost_upper + plantcost_step, plantcost_step)
    discount_rate_range = np.arange(discount_lower, discount_upper + discount_step, discount_step)
    recovery_range = np.arange(recovery_lower, recovery_upper + recovery_step, recovery_step)
    sell_cost_range = np.arange(sell_low, sell_upper + sell_step, sell_step)

    iterations_number = length_product([
        price_range,
        mine_cost_range,
        plant_cost_range,
        discount_rate_range,
        recovery_range,
        sell_cost_range
    ])

    progress_bar['maximum'] = iterations_number

    progress_index = 1
    sc = 1
    for sell_cost in sell_cost_range:
        r = 1
        for rec in recovery_range:
            d = 1
            for i in discount_rate_range:
                pco = 1
                for pc in plant_cost_range:
                    mco = 1
                    for mc in mine_cost_range:
                        pr = 1
                        for price in price_range:
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

                            if sell_cost == min(sell_cost_range) and rec == max(recovery_range) and i == min(discount_rate_range) and pc == min(plant_cost_range) and mc == min(mine_cost_range) and price == max(price_range):
                                worst_mid_best_case(df_saved, f"{cases_folder}/BEST.csv")
                            elif sell_cost == max(sell_cost_range) and rec == min(recovery_range) and i == max(discount_rate_range) and pc == max(plant_cost_range) and mc == max(mine_cost_range) and price == min(price_range):
                                worst_mid_best_case(df_saved, f"{cases_folder}/WORST.csv")
                            elif sell_cost == list_percentage(sell_cost_range, 75) and rec == list_percentage(recovery_range, 25) and i == list_percentage(discount_rate_range, 25) and pc == list_percentage(plant_cost_range, 75) and mc == list_percentage(mine_cost_range, 75) and price == list_percentage(price_range, 25):
                                worst_mid_best_case(df_saved, f"{cases_folder}/MIDCASE25.csv")
                            elif sell_cost == list_percentage(sell_cost_range, 50) and rec == list_percentage(recovery_range, 50) and i == list_percentage(discount_rate_range, 50) and pc == list_percentage(plant_cost_range, 50) and mc == list_percentage(mine_cost_range, 50) and price == list_percentage(price_range, 50):
                                worst_mid_best_case(df_saved, f"{cases_folder}/MIDCASE50.csv")
                            elif sell_cost == list_percentage(sell_cost_range, 25) and rec == list_percentage(recovery_range, 75) and i == list_percentage(discount_rate_range, 75) and pc == list_percentage(plant_cost_range, 25) and mc == list_percentage(mine_cost_range, 25) and price == list_percentage(price_range, 75):
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
    
    finish_iterations()
    
def finish_iterations():
    """
    Deifne los parámetros que cambiarán luego de terminar
    de iterar.
    """
    messagebox.showinfo("SUCCESS", "Iterations completed")
    progress_bar['value'] = 0
    percentage.set("0.00 %")
    button_iterations.config(state='normal')
    button_graph_footprint.config(state = 'normal')

def clear_files(path):
    """
    Esta función verifica si la carpeta 'iteraciones' contiene archivos, en caso de
    tener los elimina para luego almacenar las nuevas iteraciones.
    """
    files = os.listdir(path)

    if files:
        for folder_file in files:
            file_path = os.path.join(path, folder_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    path2 = f"{path}/cases"
    
    if not os.path.exists(path2):
        os.makedirs(path2)

    files = os.listdir(path)

    if files:
        for folder_file in files:
            file_path = os.path.join(path2, folder_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def save_csv(df, file_name):
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

def verify_iterations():
    """
    Luego de presionar el boton para realizar las iteraciones, se crea un mensaje que advierte
    al usuario sobre la cantidad de archivo y su tamaño total en el disco.
    """
    file_number = files_number()
    answer = messagebox.askokcancel("Confirm", f"Se crearán {file_number+3} archivos. ({round(((file_number+3)*1000/1024)/1024, 2)} Gb).")
    if answer:
        button_iterations.config(state='disabled')
        path = select_iterations_path()
        iterations()

def select_iterations_path():
    """
    Define la carpeta en donde se guardarán las
    iteraciones.
    """
    global cases_folder
    global iterations_path
    
    iterations_path = filedialog.askdirectory(title = "Folder to save iterations")
    cases_folder = os.path.join(iterations_path, "cases")
    clear_files(iterations_path)
    clear_files(cases_folder)

def worst_mid_best_case(df, file_name):
    global cases_folder
    
    if not os.path.exists(cases_folder):
        os.makedirs(cases_folder)
    df.to_csv(file_name, index = False)

def footprint_button():
    """
    Función ligada al botón "Graph", establece las funciones que
    se ejecutarán tras presionar el botón.
    """
    footprint_graph_window()

def build_graph_footprint():
    """
    Creación del gráfico del footprint teniendo en cuenta la cota
    seleccionada en el cuadro desplegable.
    """
    dataframes_modified = []
    z_height_footprint = combobox_cota_z.get()
    for df in dataframes_study_cases:
        dataframes_modified.append(df[df['z'] == int(z_height_footprint)])

    plt.figure()
    plt.scatter(dataframes_modified[0]['x'].tolist(), dataframes_modified[0]['y'].tolist(), s=250, color='#00ff00', label="Best Case")  # BEST CASE
    plt.scatter(dataframes_modified[3]['x'].tolist(), dataframes_modified[3]['y'].tolist(), s=200, color='#40bf00', label="Q75 Case")  # MID 75 CASE
    plt.scatter(dataframes_modified[2]['x'].tolist(), dataframes_modified[2]['y'].tolist(), s=150, color='#808000', label="Q50 Case")  # MID 50 CASE
    plt.scatter(dataframes_modified[1]['x'].tolist(), dataframes_modified[1]['y'].tolist(), s=100, color='#bf4000', label="Q25 Case")  # MID 25 CASE
    plt.scatter(dataframes_modified[4]['x'].tolist(), dataframes_modified[4]['y'].tolist(), s=50, color='#ff0000', label="Worst Case")  # WORST CASE
    plt.title("Footprint Graph")
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

def footprint_graph_window():
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
    boton_graficar = tk.Button(frame_new_window_z_height, text = 'Graficar', font = ('Arial', 20), command = build_graph_footprint)
    boton_graficar.pack(pady=10)

def graph_filtered_footprint():
    return


root = tk.Tk()
root.title('Certidumbre')
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 880
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(False, False)

menu_bar = tk.Menu(root)
menu_file = tk.Menu(menu_bar, tearoff = 0)
menu_file.add_command(label = 'Open File', command = open_file)
menu_file.add_separator()
menu_file.add_command(label = 'Exit', command = root.quit)
menu_bar.add_cascade(label = 'File', menu = menu_file)
menu_graph = tk.Menu(menu_bar, tearoff = 0)
menu_graph.add_command(label = 'Graph Footprint', command = graph_filtered_footprint)
menu_bar.add_cascade(label = 'Graph', menu = menu_graph)
root.config(menu = menu_bar)

# Creación de los dos frames principales de la interfaz.
# El de la izquierda (1/4 de la ventana), donde están los
# parámetros para graficar y hacer el análisis de sensibilidad.
# Y el de la derecha, donde se crean los gráficos del modelo
# de bloques y el gráfico del footprint.
frame_sensitivity = tk.Frame(root, bg = COLORFRAME1, width=WINDOW_WIDTH // 4)
frame_sensitivity.pack(side='left', fill='both')
frame_graph = tk.Frame(root, bg = COLORFRAME2, width=WINDOW_WIDTH*3 // 4)
frame_graph.pack(side='left', fill='both')

frame_xyzcu = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_xyzcu.pack()
frame_x = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_x.pack(pady = 3)
frame_y = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_y.pack(pady = 3)
frame_z = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_z.pack(pady = 3)
frame_cu = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_cu.pack(pady = 3)

label_x = tk.Label(frame_x, text='X coordinate', **label_style).pack(side='left')
combobox_x = ttk.Combobox(frame_x, values = options, state='readonly', width = 10, justify = 'center')
combobox_x.pack(side='left')

label_y = tk.Label(frame_y, text='Y coordinate', **label_style).pack(side='left')
combobox_y = ttk.Combobox(frame_y, values = options, state='readonly', width = 10, justify = 'center')
combobox_y.pack(side='left')

label_z = tk.Label(frame_z, text='Z coordinate', **label_style).pack(side='left')
combobox_z = ttk.Combobox(frame_z, values = options, state='readonly', width = 10, justify = 'center')
combobox_z.pack(side='left')

label_cu = tk.Label(frame_cu, text='Metal grade', **label_style).pack(side='left')
combobox_cu = ttk.Combobox(frame_cu, values = options, state='readonly', width = 10, justify = 'center')
combobox_cu.pack(side='left')

frame_graph_buttons = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_graph_buttons.pack()
frame_button_3d_graph = tk.Frame(frame_graph_buttons, **button_frame_style)
frame_button_3d_graph.pack(padx = 10, pady = 15, side = 'left')
button_3d_graph = tk.Button(frame_button_3d_graph, text='3D Graph', command=graph_3d, **button_style)
button_3d_graph.pack()
frame_button_2d_graph = tk.Frame(frame_graph_buttons, **button_frame_style)
frame_button_2d_graph.pack(padx = 10, pady = 15, side='left')
button_2d_graph = tk.Button(frame_button_2d_graph, text='Footprint graph', command=graph_footp, **button_style)
button_2d_graph.pack()

frame_price_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_price_general.pack(pady = 10)
label_price = tk.Label(frame_price_general, text = 'Price (usd/lb)', **label_style).pack()
frame_price = tk.Frame(frame_price_general, bg = COLORFRAME1)
frame_price.pack()
frame_price_lower = tk.Frame(frame_price, bg = COLORFRAME1)
frame_price_lower.pack(padx = 10, side='left')
label_price_lower = tk.Label(frame_price_lower, text = 'Min', bg=COLORFRAME1, fg = '#ffffff').pack()
entry_price_lower = tk.Entry(frame_price_lower, **entry_style)
entry_price_lower.pack()
frame_price_upper = tk.Frame(frame_price, bg = COLORFRAME1)
frame_price_upper.pack(padx = 10, side='left')
label_price_upper = tk.Label(frame_price_upper, text = 'Max', bg=COLORFRAME1, fg = '#ffffff').pack()
entry_price_upper = tk.Entry(frame_price_upper, **entry_style)
entry_price_upper.pack()
frame_price_step = tk.Frame(frame_price, bg = COLORFRAME1)
frame_price_step.pack(padx = 10, side='left')
label_price_step = tk.Label(frame_price_step, text = 'Step', bg=COLORFRAME1, fg = '#ffffff').pack()
entry_price_step = tk.Entry(frame_price_step, **entry_style)
entry_price_step.pack()

frame_minecost_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_minecost_general.pack(pady = 10)
label_mine_cost = tk.Label(frame_minecost_general, text = 'Mine cost (usd/t)', **label_style).pack()
frame_minecost = tk.Frame(frame_minecost_general, bg = COLORFRAME1)
frame_minecost.pack()
frame_minecost_lower = tk.Frame(frame_minecost, bg = COLORFRAME1)
frame_minecost_lower.pack(padx = 10, side='left')
label_minecost_lower = tk.Label(frame_minecost_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_minecost_lower = tk.Entry(frame_minecost_lower, **entry_style)
entry_minecost_lower.pack()
frame_minecost_upper = tk.Frame(frame_minecost, bg = COLORFRAME1)
frame_minecost_upper.pack(padx = 10, side='left')
label_minecost_upper = tk.Label(frame_minecost_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_minecost_upper = tk.Entry(frame_minecost_upper, **entry_style)
entry_minecost_upper.pack()
frame_minecost_step = tk.Frame(frame_minecost, bg = COLORFRAME1)
frame_minecost_step.pack(padx = 10, side='left')
label_minecost_step = tk.Label(frame_minecost_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_minecost_step = tk.Entry(frame_minecost_step, **entry_style)
entry_minecost_step.pack()

frame_plantcost_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_plantcost_general.pack(pady = 10)
label_plant_cost = tk.Label(frame_plantcost_general, text = 'Plant cost (usd/t)', **label_style).pack()
frame_plantcost = tk.Frame(frame_plantcost_general, bg = COLORFRAME1)
frame_plantcost.pack()
frame_plantcost_lower = tk.Frame(frame_plantcost, bg = COLORFRAME1)
frame_plantcost_lower.pack(padx = 10, side='left')
label_plantcost_lower = tk.Label(frame_plantcost_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_plantcost_lower = tk.Entry(frame_plantcost_lower, **entry_style)
entry_plantcost_lower.pack()
frame_plantcost_upper = tk.Frame(frame_plantcost, bg = COLORFRAME1)
frame_plantcost_upper.pack(padx = 10, side='left')
label_plantcost_upper = tk.Label(frame_plantcost_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_plantcost_upper = tk.Entry(frame_plantcost_upper, **entry_style)
entry_plantcost_upper.pack()
frame_plantcost_step = tk.Frame(frame_plantcost, bg = COLORFRAME1)
frame_plantcost_step.pack(padx = 10, side='left')
label_plantcost_step = tk.Label(frame_plantcost_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_plantcost_step = tk.Entry(frame_plantcost_step, **entry_style)
entry_plantcost_step.pack()

frame_discountrate_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_discountrate_general.pack(pady = 10)
label_discount_rate = tk.Label(frame_discountrate_general, text = 'Discount rate (%)', **label_style).pack()
frame_discountrate = tk.Frame(frame_discountrate_general, bg = COLORFRAME1)
frame_discountrate.pack()
frame_discountrate_lower = tk.Frame(frame_discountrate, bg = COLORFRAME1)
frame_discountrate_lower.pack(padx = 10, side='left')
label_discountrate_lower = tk.Label(frame_discountrate_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_discountrate_lower = tk.Entry(frame_discountrate_lower, **entry_style)
entry_discountrate_lower.pack()
frame_discountrate_upper = tk.Frame(frame_discountrate, bg = COLORFRAME1)
frame_discountrate_upper.pack(padx = 10, side='left')
label_discountrate_upper = tk.Label(frame_discountrate_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_discountrate_upper = tk.Entry(frame_discountrate_upper, **entry_style)
entry_discountrate_upper.pack()
frame_discountrate_step = tk.Frame(frame_discountrate, bg = COLORFRAME1)
frame_discountrate_step.pack(padx = 10, side='left')
label_discountrate_step = tk.Label(frame_discountrate_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_discountrate_step = tk.Entry(frame_discountrate_step, **entry_style)
entry_discountrate_step.pack()

frame_recovery_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_recovery_general.pack(pady = 10)
label_recovery = tk.Label(frame_recovery_general, text = 'Recovery (%)', **label_style).pack()
frame_recovery = tk.Frame(frame_recovery_general, bg = COLORFRAME1)
frame_recovery.pack()
frame_recovery_lower = tk.Frame(frame_recovery, bg = COLORFRAME1)
frame_recovery_lower.pack(padx = 10, side='left')
label_recovery_lower = tk.Label(frame_recovery_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_recovery_lower = tk.Entry(frame_recovery_lower, **entry_style)
entry_recovery_lower.pack()
frame_recovery_upper = tk.Frame(frame_recovery, bg = COLORFRAME1)
frame_recovery_upper.pack(padx = 10, side='left')
label_recovery_upper = tk.Label(frame_recovery_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_recovery_upper = tk.Entry(frame_recovery_upper, **entry_style)
entry_recovery_upper.pack()
frame_recovery_step = tk.Frame(frame_recovery, bg = COLORFRAME1)
frame_recovery_step.pack(padx = 10, side='left')
label_recovery_step = tk.Label(frame_recovery_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_recovery_step = tk.Entry(frame_recovery_step, **entry_style)
entry_recovery_step.pack()

frame_selling_cost_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_selling_cost_general.pack(pady = 10)
label_selling_cost = tk.Label(frame_selling_cost_general, text = 'Selling cost (usd/lb)', **label_style).pack()
frame_selling_cost = tk.Frame(frame_selling_cost_general, bg = COLORFRAME1)
frame_selling_cost.pack()
frame_selling_cost_lower = tk.Frame(frame_selling_cost, bg = COLORFRAME1)
frame_selling_cost_lower.pack(padx = 10, side='left')
label_selling_cost_lower = tk.Label(frame_selling_cost_lower, text = 'Min', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_sellingcost_lower = tk.Entry(frame_selling_cost_lower, **entry_style)
entry_sellingcost_lower.pack()
frame_selling_cost_upper = tk.Frame(frame_selling_cost, bg = COLORFRAME1)
frame_selling_cost_upper.pack(padx = 10, side='left')
label_selling_cost_upper = tk.Label(frame_selling_cost_upper, text = 'Max', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_sellingcost_upper = tk.Entry(frame_selling_cost_upper, **entry_style)
entry_sellingcost_upper.pack()
frame_selling_cost_step = tk.Frame(frame_selling_cost, bg = COLORFRAME1)
frame_selling_cost_step.pack(padx = 10, side='left')
label_selling_cost_step = tk.Label(frame_selling_cost_step, text = 'Step', bg = COLORFRAME1, fg = '#ffffff').pack()
entry_sellingcost_step = tk.Entry(frame_selling_cost_step, **entry_style)
entry_sellingcost_step.pack()

frame_iterations = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_iterations.pack()
frame_button_iterations = tk.Frame(frame_iterations, **button_frame_style)
frame_button_iterations.pack(pady=15)
button_iterations = tk.Button(frame_button_iterations, text = 'Iterate', command = verify_iterations, **button_style)
button_iterations.pack()
progress_bar = ttk.Progressbar(frame_iterations, orient='horizontal', length = 200)
progress_bar.pack()

percentage = tk.StringVar()
label_percentage = tk.Label(frame_iterations, textvariable=percentage, bg=COLORFRAME1, fg='#ffffff', font=('Courier New', 10))
label_percentage.pack(pady = 2)
percentage.set("0.00 %")

frame_graph_footprint = tk.Frame(frame_sensitivity, **button_frame_style)
frame_graph_footprint.pack(pady = 15)
button_graph_footprint = tk.Button(frame_graph_footprint, text = 'Graph', state='disabled', command = footprint_button, **button_style)
button_graph_footprint.pack()

root.mainloop()