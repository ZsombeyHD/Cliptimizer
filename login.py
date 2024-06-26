import tkinter as tk
from tkinter import messagebox
import sqlite3


class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg='white')

        # Felhasználónév és jelszó mezők
        label = tk.Label(self, text="BEJELENTKEZÉS", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        username_label = tk.Label(self, text="Felhasználónév:", bg='white', font=('Helvetica', 14))
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=('Helvetica', 14))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self, text="Jelszó:", bg='white', font=('Helvetica', 14))
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, font=('Helvetica', 14), show='*')
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Bejelentkezés", font=('Helvetica', 14), command=self.check_login)
        login_button.pack(pady=20)

        # A kép
        self.clip_image = tk.PhotoImage(file='images/cliptimizer.png')
        clip_label = tk.Label(self, image=self.clip_image, bg='white')
        clip_label.pack(pady=20)

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')

    def check_login(self):
        """Bejelentkezési adatok ellenőrzése."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if username == "cliptimizer_admin" and password == "cliptimizer":
            self.app.on_login_success()
        else:
            messagebox.showerror("Error", "Hibás felhasználónév, vagy jelszó!")

    def __del__(self):
        """Destruktor, ha van nyitott kapcsolat."""
        if self.conn:
            self.conn.close()


# A login.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('login.py')

    # A LoginPage
    login_page = LoginPage(root, None)
    login_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
