import sqlite3
import tkinter as tk


class DeleteDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A mezők és törlés gomb
        label = tk.Label(self, text="ADAT TÖRLÉSE", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        id_label = tk.Label(self, text="ID:", bg='white', font=('Helvetica', 14))
        id_label.pack(pady=5)
        self.id_entry = tk.Entry(self, font=('Helvetica', 14))
        self.id_entry.pack(pady=5)

        delete_button = tk.Button(self, text="Törlés", font=('Helvetica', 14), command=self.delete_data)
        delete_button.pack(pady=20)

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def delete_data(self):
        """Az adatok begyűjtése, törlése ID alapján, beviteli mezők ürítése, frissítése a többi ablakban is."""
        product_id = self.id_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

        self.id_entry.delete(0, tk.END)

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


# A delete.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('delete.py')

    # A DeleteDatabasePage
    delete_page = DeleteDatabasePage(root)
    delete_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
