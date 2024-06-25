import tkinter as tk
import sqlite3


class EditDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A mezők és módosítás gomb
        label = tk.Label(self, text="ADAT MÓDOSÍTÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        id_label = tk.Label(self, text="ID:", bg='white', font=('Helvetica', 14))
        id_label.pack(pady=5)
        self.id_entry = tk.Entry(self, font=('Helvetica', 14))
        self.id_entry.pack(pady=5)

        name_label = tk.Label(self, text="Új név:", bg='white', font=('Helvetica', 14))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=('Helvetica', 14))
        self.name_entry.pack(pady=5)

        email_label = tk.Label(self, text="Új email:", bg='white', font=('Helvetica', 14))
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=('Helvetica', 14))
        self.email_entry.pack(pady=5)

        edit_button = tk.Button(self, text="Módosítás", font=('Helvetica', 14), command=self.edit_data)
        edit_button.pack(pady=20)

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def edit_data(self):
        """Adatok begyűjtése, módosítása ID alapján, beviteli mezők ürítése, frissítése a többi ablakban is."""
        id_value = self.id_entry.get()
        new_name = self.name_entry.get()
        new_email = self.email_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("UPDATE contacts SET name=?, email=? WHERE id=?", (new_name, new_email, id_value))
        self.conn.commit()

        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

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
