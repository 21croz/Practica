import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df1 = None
df2 = None
df3 = None

def crear_grafico():
    global df1
    global df2
    global df3
    
    df1_mod = df1
    df2_mod = df2
    df3_mod = df3
    cota_z = combobox_cota_z.get()
    df1_mod = df1_mod[df1_mod['z'] == int(cota_z)]
    df2_mod = df2_mod[df2_mod['z'] == int(cota_z)]
    df3_mod = df3_mod[df3_mod['z'] == int(cota_z)]

    for widget in frame_grafico.winfo_children():
        widget.destroy()

    fig = plt.figure(figsize=(6, 6))

    plt.scatter(df1_mod['x'].tolist(), df1_mod['y'].tolist(), s=200, color='blue', label="Set 1")  # Puntos grandes
    plt.scatter(df2_mod['x'].tolist(), df2_mod['y'].tolist(), s=100, color='green', label="Set 2")  # Puntos medianos
    plt.scatter(df3_mod['x'].tolist(), df3_mod['y'].tolist(), s=50, color='red', label="Set 3")  # Puntos pequeños

    plt.title("Tres conjuntos de datos con diferentes tamaños de puntos")
    plt.legend()

    plt.xlabel("X")
    plt.ylabel("Y")

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack()

def leer_filtrar_df():
    global df1
    global df2
    global df3

    df1 = pd.read_csv(r'Practica\code\iterations\cases\BEST.csv', sep = ',')
    df2 = pd.read_csv(r'Practica\code\iterations\cases\WORST.csv', sep = ',')
    df3 = pd.read_csv(r'Practica\code\iterations\cases\MIDCASE.csv', sep = ',')

    df1 = df1[df1['antes_max'] == 1]
    df2 = df2[df2['antes_max'] == 1]
    df3 = df3[df3['antes_max'] == 1]

root = tk.Tk()
root.title('Footprint')
root.geometry('800x800')

leer_filtrar_df()

options = sorted(list(set(df1['z'].tolist() + df2['z'].tolist() + df3['z'].tolist())))

frame_cota_z = tk.Frame(root)
frame_cota_z.pack()
frame_grafico = tk.Frame(root)
frame_grafico.pack()
label_cota_z = tk.Label(frame_cota_z, text='X coordinate').pack()
combobox_cota_z = ttk.Combobox(frame_cota_z, values = options, state='readonly', width = 10, justify='center')
combobox_cota_z.pack()
boton_graficar = tk.Button(frame_cota_z, text = 'Graficar', command = crear_grafico)
boton_graficar.pack(pady=10)

root.mainloop()