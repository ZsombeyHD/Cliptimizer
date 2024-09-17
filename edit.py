import tkinter as tk
import sqlite3


class EditDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A mezők és módosítás gomb
        label = tk.Label(self, text="ADAT MÓDOSÍTÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        info_label = tk.Label(self, text="ID MEGADÁSA KÖTELEZŐ! Minden adat változtatása OPCIONÁLIS! Csak a "
                                         "módosítani kívánt mezőket töltse ki!",
                              bg='white', font=('Helvetica', 12), fg='gray')
        info_label.pack(pady=5)

        id_label = tk.Label(self, text="ID:", bg='white', font=('Helvetica', 14))
        id_label.pack(pady=5)
        self.id_entry = tk.Entry(self, font=('Helvetica', 14))
        self.id_entry.pack(pady=5)

        name_label = tk.Label(self, text="Új név:", bg='white', font=('Helvetica', 14))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=('Helvetica', 14))
        self.name_entry.pack(pady=5)

        color_label = tk.Label(self, text="Új szín (DIS-kód):", bg='white', font=('Helvetica', 14))
        color_label.pack(pady=5)
        self.color_entry = tk.Entry(self, font=('Helvetica', 14))
        self.color_entry.pack(pady=5)

        items_label = tk.Label(self, text="Új alkatrészek száma függesztékenként:", bg='white', font=('Helvetica', 14))
        items_label.pack(pady=5)
        self.items_entry = tk.Entry(self, font=('Helvetica', 14))
        self.items_entry.pack(pady=5)

        clip_type_label = tk.Label(self, text="Új klipsz típus:", bg='white', font=('Helvetica', 14))
        clip_type_label.pack(pady=5)
        self.clip_type_entry = tk.Entry(self, font=('Helvetica', 14))
        self.clip_type_entry.pack(pady=5)

        cycle_time_label = tk.Label(self, text="Új ciklusidő (másodperc):", bg='white', font=('Helvetica', 14))
        cycle_time_label.pack(pady=5)
        self.cycle_time_entry = tk.Entry(self, font=('Helvetica', 14))
        self.cycle_time_entry.pack(pady=5)

        edit_button = tk.Button(self, text="Módosítás", font=('Helvetica', 14), command=self.edit_data)
        edit_button.pack(pady=20)

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def edit_data(self):
        """Adatok begyűjtése, módosítása ID alapján, beviteli mezők ürítése, frissítése a többi ablakban is."""
        id_value = self.id_entry.get()
        new_name = self.name_entry.get()
        new_color = self.color_entry.get()
        new_items = self.items_entry.get()
        new_clip_type = self.clip_type_entry.get()
        new_total_cycle_time = self.cycle_time_entry.get()

        cursor = self.conn.cursor()

        # Mivel opcionális minden adat változtatása, ellenőrizzük, hogy mi változott
        if new_name:
            cursor.execute("UPDATE products SET name=? WHERE id=?", (new_name, id_value))
        if new_color:
            cursor.execute("UPDATE products SET color=? WHERE id=?", (new_color, id_value))
        if new_items:
            cursor.execute("UPDATE products SET items_per_hanger=? WHERE id=?", (new_items, id_value))
        if new_clip_type:
            cursor.execute("UPDATE products SET clip_type=? WHERE id=?", (new_clip_type, id_value))
        if new_total_cycle_time:
            cursor.execute("UPDATE products SET total_cycle_time=? WHERE id=?", (new_total_cycle_time, id_value))

        self.conn.commit()

        # Bevitt adatok ürítése
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.items_entry.delete(0, tk.END)
        self.clip_type_entry.delete(0, tk.END)
        self.cycle_time_entry.delete(0, tk.END)

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


# Az edit.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('edit.py')

    # Az EditDatabasePage
    edit_page = EditDatabasePage(root)
    edit_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
