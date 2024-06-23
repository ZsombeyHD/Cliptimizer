import tkinter as tk
import sqlite3


class SearchDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # Felső címke a kereső oldal tetején
        label = tk.Label(self, text="Adat keresése", bg='white', font=('Arial', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        # Kereső mező és gomb elhelyezése
        self.search_entry = tk.Entry(self, font=('Arial', 14))
        self.search_entry.pack(pady=10)

        search_button = tk.Button(self, text="Keresés", command=self.search_data)
        search_button.pack(pady=10)

        # Vászon és görgetősáv
        self.canvas = tk.Canvas(self, bg='white')
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def search_data(self):
        # Meghívódik a Keresés gombra kattintva
        search_term = self.search_entry.get()

        # Törli a korábbi keresési eredményeket
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Keresés
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR email LIKE ?",
                       (f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()

        # Eredmények megjelenítése
        for row in rows:
            frame = tk.Frame(self.scrollable_frame, bg='black', bd=1)
            frame.pack(pady=5, padx=10, fill=tk.X)

            id_label = tk.Label(frame, text=f"ID: {row[0]}", bg='white', font=('Arial', 12))
            id_label.pack(side=tk.LEFT, padx=5, pady=5)

            name_label = tk.Label(frame, text=f"Name: {row[1]}", bg='white', font=('Arial', 12))
            name_label.pack(side=tk.LEFT, padx=5, pady=5)

            email_label = tk.Label(frame, text=f"Email: {row[2]}", bg='white', font=('Arial', 12))
            email_label.pack(side=tk.LEFT, padx=5, pady=5)

    # Destruktor, ha létezik
    def __del__(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')

    # SearchDatabasePage létrehozása és megjelenítése
    search_page = SearchDatabasePage(root)
    search_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
