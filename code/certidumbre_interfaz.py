import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

original_df = None
df = None
options = []
COLORFRAME1 = '#ffd3d3'
COLORFRAME2 = '#ffffff'
label_style = {
    'bg': COLORFRAME1,
    'font': ('Arial', 12)
}
slider_style = {
    'bg': COLORFRAME1,
    'length': 180
}
button_style = {
    'bg': '#4a5cff',
    'fg': '#ffffff',
    'width': 15,
    'font': ('Courier New', 14),
    'border': 0,
    'cursor': 'hand2'
}


def open_file():
    """
    Abre un archivo excel
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

def reset_combobox():
    """
    Crea nuevamente los cuadros para seleccionar las variables de los encabezados del archivo
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

def graph_3d():
    """
    Crea un gráfico en 3 dimensiones usando las
    columnas x, y, z, ley del archivo importado,
    además. Hecho mediante el paquete
    matplotlib
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
    Crea el grafico en 2D del footprint
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
    global df
    global original_df

    df = df.loc[df['antes_max'] > 0]

def iterations():
    def length_product(list):
        total_length = 1
        for item in list:
            total_length = total_length*len(item)
        return total_length

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

    progress_bar['maximum'] = length_product([
        price_range,
        mine_cost_range,
        plant_cost_range,
        discount_rate_range,
        recovery_range,
        sell_cost_range
    ])

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
                            df_saved['valor'] = (price - sell_cost)*rec*df_saved['ley']*2204.63 - (mc - pc)
                            df_saved['VAN'] = df_saved['valor']/((1 + i)**df_saved['periodo'])

                            csv_name = f"pr{pr}mc{mco}pc{pco}d{d}r{r}sc{sc}.csv"

                            save_csv(df_saved, csv_name)
                            progress_bar['value'] = progress_index
                            root.update_idletasks()
                            progress_index += 1
                            pr += 1
                        mco += 1
                    pco += 1
                d += 1
            r += 1
        sc += 1
    progress_bar['value'] = 0

def save_csv(df, file_name):
    folder = "iteraciones"
    if not os.path.exists(folder):
        os.makedirs(folder)
    full_path = os.path.join(folder, file_name)
    df.to_csv(full_path, index = False)


root = tk.Tk()
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
root.resizable(False, False)

menu_bar = tk.Menu(root)
menu_file = tk.Menu(menu_bar, tearoff = 0)
menu_file.add_command(label = 'Open File', command = open_file)
menu_file.add_separator()
menu_file.add_command(label = 'Exit', command = root.quit)
menu_bar.add_cascade(label = 'File', menu = menu_file)
root.config(menu = menu_bar)

frame_sensitivity = tk.Frame(root, bg = COLORFRAME1, width=WINDOW_WIDTH // 4)
frame_sensitivity.pack(side='left', fill='both')
frame_graph = tk.Frame(root, bg = COLORFRAME2, width=WINDOW_WIDTH*3 // 4)
frame_graph.pack(side='left', fill='both')

frame_xyzcu = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_xyzcu.pack()
frame_x = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_x.pack()
frame_y = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_y.pack()
frame_z = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_z.pack()
frame_cu = tk.Frame(frame_xyzcu, bg = COLORFRAME1)
frame_cu.pack()

label_x = tk.Label(frame_x, text='X coordinate', **label_style).pack(side='left')
combobox_x = ttk.Combobox(frame_x, values = options, state='readonly', width = 10)
combobox_x.pack(side='left')

label_y = tk.Label(frame_y, text='Y coordinate', **label_style).pack(side='left')
combobox_y = ttk.Combobox(frame_y, values = options, state='readonly', width = 10)
combobox_y.pack(side='left')

label_z = tk.Label(frame_z, text='Z coordinate', **label_style).pack(side='left')
combobox_z = ttk.Combobox(frame_z, values = options, state='readonly', width = 10)
combobox_z.pack(side='left')

label_cu = tk.Label(frame_cu, text='Metal grade', **label_style).pack(side='left')
combobox_cu = ttk.Combobox(frame_cu, values = options, state='readonly', width = 10)
combobox_cu.pack(side='left')

frame_price_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_price_general.pack(pady = 10)
label_price = tk.Label(frame_price_general, text = 'Price (usd/lb)', **label_style).pack()
frame_price = tk.Frame(frame_price_general, bg = COLORFRAME1)
frame_price.pack()
frame_price_lower = tk.Frame(frame_price, bg = COLORFRAME1)
frame_price_lower.pack(padx = 10, side='left')
label_price_lower = tk.Label(frame_price_lower, text = 'Min', bg=COLORFRAME1).pack()
entry_price_lower = tk.Entry(frame_price_lower, width = 5)
entry_price_lower.pack()
frame_price_upper = tk.Frame(frame_price, bg = COLORFRAME1)
frame_price_upper.pack(padx = 10, side='left')
label_price_upper = tk.Label(frame_price_upper, text = 'Max', bg=COLORFRAME1).pack()
entry_price_upper = tk.Entry(frame_price_upper, width = 5)
entry_price_upper.pack()
frame_price_step = tk.Frame(frame_price, bg = COLORFRAME1)
frame_price_step.pack(padx = 10, side='left')
label_price_step = tk.Label(frame_price_step, text = 'Step', bg=COLORFRAME1).pack()
entry_price_step = tk.Entry(frame_price_step, width = 5)
entry_price_step.pack()

frame_minecost_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_minecost_general.pack(pady = 10)
label_mine_cost = tk.Label(frame_minecost_general, text = 'Mine cost (usd/t)', **label_style).pack()
frame_minecost = tk.Frame(frame_minecost_general, bg = COLORFRAME1)
frame_minecost.pack()
frame_minecost_lower = tk.Frame(frame_minecost, bg = COLORFRAME1)
frame_minecost_lower.pack(padx = 10, side='left')
label_minecost_lower = tk.Label(frame_minecost_lower, text = 'Min', bg = COLORFRAME1).pack()
entry_minecost_lower = tk.Entry(frame_minecost_lower, width = 5)
entry_minecost_lower.pack()
frame_minecost_upper = tk.Frame(frame_minecost, bg = COLORFRAME1)
frame_minecost_upper.pack(padx = 10, side='left')
label_minecost_upper = tk.Label(frame_minecost_upper, text = 'Max', bg = COLORFRAME1).pack()
entry_minecost_upper = tk.Entry(frame_minecost_upper, width = 5)
entry_minecost_upper.pack()
frame_minecost_step = tk.Frame(frame_minecost, bg = COLORFRAME1)
frame_minecost_step.pack(padx = 10, side='left')
label_minecost_step = tk.Label(frame_minecost_step, text = 'Step', bg = COLORFRAME1).pack()
entry_minecost_step = tk.Entry(frame_minecost_step, width = 5)
entry_minecost_step.pack()

frame_plantcost_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_plantcost_general.pack(pady = 10)
label_plant_cost = tk.Label(frame_plantcost_general, text = 'Plant cost (usd/t)', **label_style).pack()
frame_plantcost = tk.Frame(frame_plantcost_general, bg = COLORFRAME1)
frame_plantcost.pack()
frame_plantcost_lower = tk.Frame(frame_plantcost, bg = COLORFRAME1)
frame_plantcost_lower.pack(padx = 10, side='left')
label_plantcost_lower = tk.Label(frame_plantcost_lower, text = 'Min', bg = COLORFRAME1).pack()
entry_plantcost_lower = tk.Entry(frame_plantcost_lower, width = 5)
entry_plantcost_lower.pack()
frame_plantcost_upper = tk.Frame(frame_plantcost, bg = COLORFRAME1)
frame_plantcost_upper.pack(padx = 10, side='left')
label_plantcost_upper = tk.Label(frame_plantcost_upper, text = 'Max', bg = COLORFRAME1).pack()
entry_plantcost_upper = tk.Entry(frame_plantcost_upper, width = 5)
entry_plantcost_upper.pack()
frame_plantcost_step = tk.Frame(frame_plantcost, bg = COLORFRAME1)
frame_plantcost_step.pack(padx = 10, side='left')
label_plantcost_step = tk.Label(frame_plantcost_step, text = 'Step', bg = COLORFRAME1).pack()
entry_plantcost_step = tk.Entry(frame_plantcost_step, width = 5)
entry_plantcost_step.pack()

frame_discountrate_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_discountrate_general.pack(pady = 10)
label_discount_rate = tk.Label(frame_discountrate_general, text = 'Discount rate (%)', **label_style).pack()
frame_discountrate = tk.Frame(frame_discountrate_general, bg = COLORFRAME1)
frame_discountrate.pack()
frame_discountrate_lower = tk.Frame(frame_discountrate, bg = COLORFRAME1)
frame_discountrate_lower.pack(padx = 10, side='left')
label_discountrate_lower = tk.Label(frame_discountrate_lower, text = 'Min', bg = COLORFRAME1).pack()
entry_discountrate_lower = tk.Entry(frame_discountrate_lower, width = 5)
entry_discountrate_lower.pack()
frame_discountrate_upper = tk.Frame(frame_discountrate, bg = COLORFRAME1)
frame_discountrate_upper.pack(padx = 10, side='left')
label_discountrate_upper = tk.Label(frame_discountrate_upper, text = 'Max', bg = COLORFRAME1).pack()
entry_discountrate_upper = tk.Entry(frame_discountrate_upper, width = 5)
entry_discountrate_upper.pack()
frame_discountrate_step = tk.Frame(frame_discountrate, bg = COLORFRAME1)
frame_discountrate_step.pack(padx = 10, side='left')
label_discountrate_step = tk.Label(frame_discountrate_step, text = 'Step', bg = COLORFRAME1).pack()
entry_discountrate_step = tk.Entry(frame_discountrate_step, width = 5)
entry_discountrate_step.pack()

frame_recovery_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_recovery_general.pack(pady = 10)
label_recovery = tk.Label(frame_recovery_general, text = 'Recovery (%)', **label_style).pack()
frame_recovery = tk.Frame(frame_recovery_general, bg = COLORFRAME1)
frame_recovery.pack()
frame_recovery_lower = tk.Frame(frame_recovery, bg = COLORFRAME1)
frame_recovery_lower.pack(padx = 10, side='left')
label_recovery_lower = tk.Label(frame_recovery_lower, text = 'Min', bg = COLORFRAME1).pack()
entry_recovery_lower = tk.Entry(frame_recovery_lower, width = 5)
entry_recovery_lower.pack()
frame_recovery_upper = tk.Frame(frame_recovery, bg = COLORFRAME1)
frame_recovery_upper.pack(padx = 10, side='left')
label_recovery_upper = tk.Label(frame_recovery_upper, text = 'Max', bg = COLORFRAME1).pack()
entry_recovery_upper = tk.Entry(frame_recovery_upper, width = 5)
entry_recovery_upper.pack()
frame_recovery_step = tk.Frame(frame_recovery, bg = COLORFRAME1)
frame_recovery_step.pack(padx = 10, side='left')
label_recovery_step = tk.Label(frame_recovery_step, text = 'Step', bg = COLORFRAME1).pack()
entry_recovery_step = tk.Entry(frame_recovery_step, width = 5)
entry_recovery_step.pack()

frame_selling_cost_general = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_selling_cost_general.pack(pady = 10)
label_selling_cost = tk.Label(frame_selling_cost_general, text = 'Selling cost (usd/lb)', **label_style).pack()
frame_selling_cost = tk.Frame(frame_selling_cost_general, bg = COLORFRAME1)
frame_selling_cost.pack()
frame_selling_cost_lower = tk.Frame(frame_selling_cost, bg = COLORFRAME1)
frame_selling_cost_lower.pack(padx = 10, side='left')
label_selling_cost_lower = tk.Label(frame_selling_cost_lower, text = 'Min', bg = COLORFRAME1).pack()
entry_sellingcost_lower = tk.Entry(frame_selling_cost_lower, width = 5)
entry_sellingcost_lower.pack()
frame_selling_cost_upper = tk.Frame(frame_selling_cost, bg = COLORFRAME1)
frame_selling_cost_upper.pack(padx = 10, side='left')
label_selling_cost_upper = tk.Label(frame_selling_cost_upper, text = 'Max', bg = COLORFRAME1).pack()
entry_sellingcost_upper = tk.Entry(frame_selling_cost_upper, width = 5)
entry_sellingcost_upper.pack()
frame_selling_cost_step = tk.Frame(frame_selling_cost, bg = COLORFRAME1)
frame_selling_cost_step.pack(padx = 10, side='left')
label_selling_cost_step = tk.Label(frame_selling_cost_step, text = 'Step', bg = COLORFRAME1).pack()
entry_sellingcost_step = tk.Entry(frame_selling_cost_step, width = 5)
entry_sellingcost_step.pack()

frame_graph_buttons = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_graph_buttons.pack()
button_3d_graph = tk.Button(frame_graph_buttons, text='3D Graph', command=graph_3d, **button_style)
button_3d_graph.pack(padx = 10, pady = 15, side = 'left')
button_2d_graph = tk.Button(frame_graph_buttons, text='Footprint graph', command=graph_footp, **button_style)
button_2d_graph.pack(padx = 10, pady = 15, side='left')

frame_iterations = tk.Frame(frame_sensitivity, bg = COLORFRAME1)
frame_iterations.pack()
button_iterations = tk.Button(frame_iterations, text = 'Iterate', command = iterations, **button_style)
button_iterations.pack(pady=15)
progress_bar = ttk.Progressbar(frame_iterations, orient='horizontal', length = 200)
progress_bar.pack()

root.mainloop()