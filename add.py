import tkinter as tk
import sqlite3


class AddDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A mezők és hozzáadás gomb
        label = tk.Label(self, text="ÚJ ADAT HOZZÁADÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        name_label = tk.Label(self, text="Név:", bg='white', font=('Helvetica', 14))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=('Helvetica', 14))
        self.name_entry.pack(pady=5)

        email_label = tk.Label(self, text="Email:", bg='white', font=('Helvetica', 14))
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=('Helvetica', 14))
        self.email_entry.pack(pady=5)

        add_button = tk.Button(self, text="Hozzáadás", font=('Helvetica', 14), command=self.add_data)
        add_button.pack(pady=20)

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def add_data(self):
        """Adatok begyűjtése, hozzáadása, beviteli mezők ürítése, frissítés a többi ablakban is."""
        name = self.name_entry.get()
        email = self.email_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()

        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        self.update_pages()

    def update_pages(self):
        """Frissítés más ablakokban."""
        for widget in self.master.master.pages_container.winfo_children():
            if hasattr(widget, 'display_data'):
                widget.display_data()

    def __del__(self):
        """Destruktor."""
        if self.conn:
            self.conn.close()


# Az add.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('add.py')

    # Az AddDatabasePage
    add_page = AddDatabasePage(root)
    add_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
