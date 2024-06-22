import tkinter as tk


class DatabasePage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        label = tk.Label(self, text="A  jelenlegi adatok az adatbázisban", bg='white',
                         font=('Arial', 20, 'bold'), padx=20, pady=20)
        label.pack(expand=True)

        label.pack(anchor=tk.CENTER)
