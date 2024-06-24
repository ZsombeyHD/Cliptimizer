import tkinter as tk
import sqlite3


class AddDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # Címke
        label = tk.Label(self, text="Új adat hozzáadása", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        # Név mező
        name_label = tk.Label(self, text="Név:", bg='white', font=('Helvetica', 14))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=('Helvetica', 14))
        self.name_entry.pack(pady=5)

        # Email mező
        email_label = tk.Label(self, text="Email:", bg='white', font=('Helvetica', 14))
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=('Helvetica', 14))
        self.email_entry.pack(pady=5)

        # Hozzáadás gomb
        add_button = tk.Button(self, text="Hozzáadás", font=('Helvetica', 14), command=self.add_data)
        add_button.pack(pady=20)

        # Adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def add_data(self):
        # Adatok begyűjtése a mezőkből
        name = self.name_entry.get()
        email = self.email_entry.get()

        # Adatok hozzáadása az adatbázishoz
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()

        # Beviteli mezők ürítése
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        # Adatok frissítése más ablakokban
        self.update_pages()

    def update_pages(self):
        # Frissítés más ablakokban
        for widget in self.master.master.pages_container.winfo_children():
            if hasattr(widget, 'display_data'):
                widget.display_data()

    # Destruktor, ha létezik
    def __del__(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')

    # Az AddDatabasePage
    add_page = AddDatabasePage(root)
    add_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
