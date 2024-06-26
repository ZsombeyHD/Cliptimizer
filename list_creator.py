import tkinter as tk


class ListCreatorPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A cím
        label = tk.Label(self, text="A TERV LÉTREHOZÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)
