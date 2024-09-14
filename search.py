import tkinter as tk
import sqlite3


class SearchDatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        label = tk.Label(self, text="TERMÉK KERESÉSE", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        # A kereső mező és gomb
        self.search_entry = tk.Entry(self, font=('Helvetica', 14))
        self.search_entry.pack(pady=10)

        search_button = tk.Button(self, text="Keresés", font=('Helvetica', 14), command=self.search_data)
        search_button.pack(pady=10)

        # A canvas és scrollbar
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

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def search_data(self):
        """Keresés gomb után meghívódik; Korábbi kereséseket töröl, keres, keresési eredményeket mutat."""
        search_term = self.search_entry.get()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ? OR color LIKE ? OR clip_type LIKE ?",
                       (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()

        for row in rows:
            frame = tk.Frame(self.scrollable_frame, bg='black', bd=1)
            frame.pack(pady=5, padx=10, fill=tk.X)

            id_label = tk.Label(frame, text=f"ID: {row[0]}", bg='white', font=('Helvetica', 12))
            id_label.pack(side=tk.LEFT, padx=5, pady=5)

            name_label = tk.Label(frame, text=f"Név: {row[1]}", bg='white', font=('Helvetica', 12))
            name_label.pack(side=tk.LEFT, padx=5, pady=5)

            color_label = tk.Label(frame, text=f"Szín: {row[2]}", bg='white', font=('Helvetica', 12))
            color_label.pack(side=tk.LEFT, padx=5, pady=5)

            clip_type_label = tk.Label(frame, text=f"Klipsz típusa: {row[3]}", bg='white', font=('Helvetica', 12))
            clip_type_label.pack(side=tk.LEFT, padx=5, pady=5)

            items_per_hanger_label = tk.Label(frame, text=f"Függesztékre felrakható alkatrészek száma: {row[4]}",
                                              bg='white', font=('Helvetica', 12))
            items_per_hanger_label.pack(side=tk.LEFT, padx=5, pady=5)

            cycle_time_label = tk.Label(frame, text=f"Teljes ciklus ideje (sec): {row[5]}", bg='white', font=('Helvetica', 12))
            cycle_time_label.pack(side=tk.LEFT, padx=5, pady=5)

    def __del__(self):
        """Destruktor, ha van nyitott kapcsolat."""
        if self.conn:
            self.conn.close()


# A search.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('search.py')

    # A SearchDatabasePage
    search_page = SearchDatabasePage(root)
    search_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
