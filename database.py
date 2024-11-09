import tkinter as tk
import sqlite3


class DatabasePage(tk.Frame):
    """A jelenlegi adatok mutatására szolgáló oldal. Bármilyen hozzáadás, módosítás, törlés esetén frissítődik."""

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A cím
        label = tk.Label(self, text="JELENLEGI ADATOK", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

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
        self.display_data()

    def display_data(self):
        """Az adatbázis kapcsolat nyitása, lekérdezése, feldolgozása, szépítése, korábbi adatok törlése."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        for row in rows:
            frame = tk.Frame(self.scrollable_frame, bg='white', bd=1, relief='solid')
            frame.pack(pady=5, padx=10, fill=tk.X)

            attributes = [
                f"ID: {row[0]}",
                f"Név: {row[1]}",
                f"Szín: {row[2]}",
                f"Klipsz típusa: {row[3]}",
                f"Függesztékre felrakható: {row[4]} db",
                f"Függesztékenként ciklusidő: {row[5]}",
                f"Anyagszükséglet / alkatrész (g): {row[7]}"
            ]

            for attr in attributes:
                label = tk.Label(frame, text=attr, font=('Helvetica', 10), bg='white')
                label.pack(side=tk.LEFT, padx=5, pady=5)

    def __del__(self):
        """Destruktor, ha van nyitott kapcsolat."""
        if self.conn:
            self.conn.close()


# A database.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('database.py')

    database_page = DatabasePage(root)
    database_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
