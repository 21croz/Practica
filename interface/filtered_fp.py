import tkinter as tk
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, ttk, messagebox


class ScatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráficos de Dispersión Configurables")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Función para cerrar la aplicación:
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.menu_bar = tk.Menu(root)
        self.menu_file = tk.Menu(self.menu_bar, tearoff = 0)
        self.menu_file.add_command(label = 'Open Folder', command = self.select_folder)
        self.menu_file.add_separator()
        self.menu_file.add_command(label = 'Exit', command = root.quit)
        self.menu_bar.add_cascade(label = 'File', menu = self.menu_file)
        self.root.config(menu = self.menu_bar)

        self.dataframes = []
        self.colors = ['red', 'blue', 'green', 'orange', 'purple']
        self.sizes = [250, 200, 150, 100, 50]

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.frame_combobox = tk.Frame(self.control_frame)
        self.frame_combobox.pack(pady = 15)

        self.frame_checkbuttons = tk.Frame(self.control_frame)
        self.frame_checkbuttons.pack(pady = 15)

        self.frame_graph_button = tk.Frame(self.control_frame)
        self.frame_graph_button.pack(pady = 5)

        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)


    def select_folder(self):
        folder_path = filedialog.askdirectory()
        
        if not folder_path:
            return
        
        try:
            csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

            for file in csv_files:
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                self.dataframes.append(df[df['antes_max'] == 1])
        except Exception as e:
            messagebox.showerror("Error", f"An error has occured: {e}")
        
        self.options = sorted(list(set(self.dataframes[0]['z'].tolist() + self.dataframes[1]['z'].tolist() + self.dataframes[2]['z'].tolist() + self.dataframes[3]['z'].tolist() + self.dataframes[4]['z'].tolist())))
        
        self.create_widgets()
    

    def create_widgets(self):
        self.label_cota = tk.Label(self.frame_combobox, text = "Cota Z", justify = 'center')
        self.label_cota.pack()

        self.combobox_cota = ttk.Combobox(self.frame_combobox, values = self.options, state = 'readonly', width = 10, justify = 'center')
        self.combobox_cota.pack()

        self.checkbuttons_state = [tk.BooleanVar(value = True) for _ in range(5)]
        self.graph_labels = ['Best case', 'Mid case (25%)', 'Mid case (50%)', 'Mid case (75%)', 'Worst case']

        for i, label in enumerate(self.graph_labels):
            chk = ttk.Checkbutton(self.frame_checkbuttons, text = label, variable = self.checkbuttons_state[i])
            chk.pack(anchor = tk.W)
        
        self.button_graph = tk.Button(self.frame_graph_button, text = 'Graph', command = self.create_graph)
        self.button_graph.pack()


    def create_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        self.dataframes_mod = []
        for df in self.dataframes:
            self.dataframes_mod.append(df[df['z'] == int(self.combobox_cota.get())])

        self.dataframes_x = [df['x'].tolist() for df in self.dataframes_mod]
        self.dataframes_y = [df['y'].tolist() for df in self.dataframes_mod]

        self.fig, self.ax = plt.subplots(figsize = (6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.update_graph()
    

    def update_graph(self):
        self.ax.clear()

        for i, show in enumerate(self.checkbuttons_state):
            if show.get():
                self.ax.scatter(
                    self.dataframes_x[i], self.dataframes_y[i],
                    label = self.graph_labels[i],
                    c = self.colors[i],
                    s = self.sizes[i])
        
        self.ax.set_title("Footprint")
        self.ax.legend()
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_axis_off()
        self.canvas.draw()


    def on_closing(self):
        self.root.quit()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ScatterApp(root)
    root.mainloop()