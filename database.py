import tkinter as tk
import sqlite3


class DatabasePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

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

        self.conn = sqlite3.connect('cliptimizer.db')
        self.display_data()

    def display_data(self):
        """Az adatbázis kapcsolat nyitása, lekérdezése, feldolgozása, szépítése, korábbi adatok törlése"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()

        for row in rows:
            frame = tk.Frame(self.scrollable_frame, bg='black', bd=1)
            frame.pack(pady=5, padx=10, fill=tk.X)

            id_label = tk.Label(frame, text=f"ID: {row[0]}", bg='white', font=('Helvetica', 12))
            id_label.pack(side=tk.LEFT, padx=5, pady=5)

            name_label = tk.Label(frame, text=f"Name: {row[1]}", bg='white', font=('Helvetica', 12))
            name_label.pack(side=tk.LEFT, padx=5, pady=5)

            email_label = tk.Label(frame, text=f"Email: {row[2]}", bg='white', font=('Helvetica', 12))
            email_label.pack(side=tk.LEFT, padx=5, pady=5)

    def __del__(self):
        """Destruktor"""
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
