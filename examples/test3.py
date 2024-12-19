import tkinter as tk

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
                   bg = '#3c93c9',
                   fg = '#ffffff',
                   font = ('Arial', 15),
                   width = 10,
                   cursor = 'hand2',
                   border = 0)
button.pack()

root.mainloop()