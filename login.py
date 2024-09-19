import tkinter as tk
from tkinter import messagebox
import sqlite3


class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg='white')

        label = tk.Label(self, text="BEJELENTKEZÉS", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        # A mezők és bejelentkezés gomb
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

        # A jelszóváltoztatás gomb
        change_password_button = tk.Button(self, text="Jelszóváltoztatás", font=('Helvetica', 14),
                                           command=self.open_change_password_window)
        change_password_button.pack(pady=10)

        # Kilépés gomb
        exit_button = tk.Button(self, text="Kilépés", font=('Helvetica', 14), command=self.exit_application)
        exit_button.pack(pady=10)

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

        if user:
            self.app.on_login_success()
        else:
            messagebox.showerror("Error", "Hibás felhasználónév vagy jelszó!")

    def open_change_password_window(self):
        """Jelszóváltoztatási ablak megnyitása."""
        change_window = tk.Toplevel(self)
        change_window.title("Jelszóváltoztatás")
        change_window.geometry("1920x1080")

        # Felhasználónév megadása
        tk.Label(change_window, text="Felhasználónév:", font=('Helvetica', 14)).pack(pady=10)
        username_entry = tk.Entry(change_window, font=('Helvetica', 14))
        username_entry.pack(pady=10)

        # Régi jelszó megadása
        tk.Label(change_window, text="Régi jelszó:", font=('Helvetica', 14)).pack(pady=10)
        old_password_entry = tk.Entry(change_window, font=('Helvetica', 14), show='*')
        old_password_entry.pack(pady=10)

        # Új jelszó megadása
        tk.Label(change_window, text="Új jelszó:", font=('Helvetica', 14)).pack(pady=10)
        new_password_entry = tk.Entry(change_window, font=('Helvetica', 14), show='*')
        new_password_entry.pack(pady=10)

        # Új jelszó megerősítése
        tk.Label(change_window, text="Új jelszó megerősítése:", font=('Helvetica', 14)).pack(pady=10)
        confirm_password_entry = tk.Entry(change_window, font=('Helvetica', 14), show='*')
        confirm_password_entry.pack(pady=10)

        # A mentés gomb
        tk.Button(change_window, text="Mentés", font=('Helvetica', 14),
                  command=lambda: self.change_password(username_entry.get(), old_password_entry.get(),
                                                       new_password_entry.get(), confirm_password_entry.get(),
                                                       change_window)).pack(pady=20)

    def change_password(self, username, old_password, new_password, confirm_password, window):
        """Jelszó frissítése az adatbázisban."""
        # Ellenőrizzük a felhasználónevet és a régi jelszót
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, old_password))
        user = cursor.fetchone()

        if not user:
            messagebox.showerror("Hiba", "A megadott felhasználónév vagy régi jelszó helytelen.")
            return

        # Új jelszó és megerősítése
        if new_password != confirm_password:
            messagebox.showerror("Hiba", "Az új jelszavak nem egyeznek.")
            return

        # Jelszó hosszának ellenőrzése
        if len(new_password) < 8:
            messagebox.showerror("Hiba", "A jelszónak legalább 8 karakter hosszúnak kell lennie.")
            return

        # Jelszó frissítése az adatbázisban
        cursor.execute("UPDATE admin SET password=? WHERE username=?", (new_password, username))
        self.conn.commit()

        messagebox.showinfo("Siker", "Jelszó sikeresen megváltoztatva!")
        window.destroy()

    def exit_application(self):
        """Az alkalmazás bezárása."""
        self.app.withdraw()
        self.app.quit()
        self.app.destroy()

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
