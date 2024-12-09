import tkinter as tk
import sqlite3
from tkinter import StringVar, OptionMenu


class AddDatabasePage(tk.Frame):
    """A termékek hozzáadására szolgáló oldal."""

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A mezők és hozzáadás gomb
        label = tk.Label(self, text="ÚJ TERMÉK HOZZÁADÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20,
                         pady=20)
        label.pack(anchor=tk.N)

        name_label = tk.Label(self, text="Termék neve:", bg='white', font=('Helvetica', 14))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=('Helvetica', 14))
        self.name_entry.pack(pady=5)

        color_label = tk.Label(self, text="Termék színe:", bg='white', font=('Helvetica', 14))
        color_label.pack(pady=5)
        self.color_var = StringVar(self)
        self.color_var.set("DIS576")  # Alapértelmezett szín
        color_menu = OptionMenu(self, self.color_var, "DIS576", "DIS519", "DIS377", "DIS520", "DIS376",
                                "DIS522", "DIS1198")
        color_menu.pack(pady=5)

        clip_type_label = tk.Label(self, text="Klipsz típusa:", bg='white', font=('Helvetica', 14))
        clip_type_label.pack(pady=5)
        self.clip_type_entry = tk.Entry(self, font=('Helvetica', 14))
        self.clip_type_entry.pack(pady=5)

        items_per_hanger_label = tk.Label(self, text="Függesztékre felrakható alkatrészek száma:", bg='white',
                                          font=('Helvetica', 14))
        items_per_hanger_label.pack(pady=5)
        self.items_per_hanger_entry = tk.Entry(self, font=('Helvetica', 14))
        self.items_per_hanger_entry.pack(pady=5)

        cycle_time_label = tk.Label(self, text="Teljes ciklusidő (másodperc):", bg='white', font=('Helvetica', 14))
        cycle_time_label.pack(pady=5)
        self.cycle_time_entry = tk.Entry(self, font=('Helvetica', 14))
        self.cycle_time_entry.pack(pady=5)

        material_per_part_label = tk.Label(self, text="Vegyes anyagszükséglet / alkatrész (g):", bg='white',
                                           font=('Helvetica', 14))
        material_per_part_label.pack(pady=5)
        self.material_per_part_entry = tk.Entry(self, font=('Helvetica', 14))
        self.material_per_part_entry.pack(pady=5)

        add_button = tk.Button(self, text="Hozzáadás", font=('Helvetica', 14), command=self.add_data)
        add_button.pack(pady=20)

        # Adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def add_data(self):
        """Adatok begyűjtése, hozzáadása a products táblához."""
        name = self.name_entry.get()
        color = self.color_var.get()
        clip_type = self.clip_type_entry.get()
        items_per_hanger = self.items_per_hanger_entry.get()
        cycle_time = self.cycle_time_entry.get()
        material_per_part = self.material_per_part_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO products (name, color, clip_type, items_per_hanger, total_cycle_time, 
        material_per_part) VALUES (?, ?, ?, ?, ?, ?)""", (name, color, clip_type, items_per_hanger,
                                                          cycle_time, material_per_part))
        self.conn.commit()

        # Beviteli mezők ürítése
        self.name_entry.delete(0, tk.END)
        self.clip_type_entry.delete(0, tk.END)
        self.items_per_hanger_entry.delete(0, tk.END)
        self.cycle_time_entry.delete(0, tk.END)
        self.material_per_part_entry.delete(0, tk.END)

        self.update_pages()

    def update_pages(self):
        """Frissítés más ablakokban."""
        for widget in self.master.master.pages_container.winfo_children():
            if hasattr(widget, 'display_data'):
                widget.display_data()

    def __del__(self):
        """Destruktor, ha van nyitott kapcsolat."""
        if self.conn:
            self.conn.close()


# Az add.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('add.py')

    add_page = AddDatabasePage(root)
    add_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
