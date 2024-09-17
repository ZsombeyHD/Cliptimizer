import tkinter as tk
from tkinter import Toplevel, PhotoImage, OptionMenu, StringVar, messagebox
import sqlite3


class ListCreatorPage(tk.Frame):
    """A gyártási terv(ek) létrehozására szolgáló oldal."""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')
        self.cursor = self.conn.cursor()

        # Adat lekérése
        self.cursor.execute("SELECT name FROM contacts")
        self.contact_names = [row[0] for row in self.cursor.fetchall()]

        # A cím
        label = tk.Label(self, text="TERVEK LÉTREHOZÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        # Terv panelén található képek betöltése
        self.add_icon = PhotoImage(file='images/add_plan_resized.png')
        self.eye_icon = PhotoImage(file='images/eye_resized.png')
        self.trash_icon = PhotoImage(file='images/trash_resized.png')

        # Terv létrehozása gomb
        add_button = tk.Button(self, image=self.add_icon, bg='white', bd=0, command=self.create_new_plan)
        add_button.pack(anchor=tk.N, pady=20)

        # Panelek konténere (ahol a terveket megjelenítjük)
        self.plan_container = tk.Frame(self, bg='white')
        self.plan_container.pack(anchor=tk.N, pady=20)

        # Tervek betöltése
        self.load_plans()

    def create_new_plan(self):
        """Egy terv létrehozása : Új ablak és adatbázis kapcsolódás."""
        new_window = Toplevel(self)
        new_window.title("Terv")
        new_window.geometry("1920x1080")

        # Cím az új ablakban
        label = tk.Label(new_window, text="Terv létrehozása", font=('Helvetica', 14))
        label.pack(pady=20)

        # Input mező a terv nevéhez
        plan_name_entry = tk.Entry(new_window)
        plan_name_entry.pack(pady=10)

        # Legördülő menü a meglévő adatokból
        selected_contact = StringVar(new_window)
        selected_contact.set(self.contact_names[0])
        contact_menu = OptionMenu(new_window, selected_contact, *self.contact_names)
        contact_menu.pack(pady=10)

        # Mentés gomb
        tk.Button(new_window, text="Mentés",
                  command=lambda: self.save_plan(new_window, plan_name_entry.get(), selected_contact.get())).pack(
            pady=10)

    def save_plan(self, window, plan_name, contact_name):
        """Terv mentése és panel hozzáadása."""
        if plan_name and contact_name:
            # Zárjuk be az új terv ablakot
            window.destroy()

            # Adatok mentése az adatbázisba
            self.cursor.execute("INSERT INTO plans (plan_name, contact_name) VALUES (?, ?)",
                                (plan_name, contact_name))
            self.conn.commit()

            # Terv hozzáadása a listához
            self.add_plan_panel(plan_name, contact_name)

    def add_plan_panel(self, plan_name, contact_name):
        """Panel hozzáadása a tervhez."""
        panel = tk.Frame(self.plan_container, bg='lightgrey', bd=2, relief='solid')
        panel.pack(pady=5, padx=10, fill=tk.X)

        # Terv neve
        plan_label = tk.Label(panel, text=f"{plan_name}", bg='lightgrey', font=('Helvetica', 12))
        plan_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Terv megnézése
        view_button = tk.Button(panel, image=self.eye_icon, bg='lightgrey', bd=0,
                                command=lambda: self.view_plan(plan_name, contact_name))
        view_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Terv törlése
        delete_button = tk.Button(panel, image=self.trash_icon, bg='lightgrey', bd=0,
                                  command=lambda: self.confirm_delete(plan_name))
        delete_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def view_plan(self, plan_name, contact_name):
        """Terv megjelenítése egy új ablakban."""
        new_window = Toplevel(self)
        new_window.title(f"Terv: {plan_name}")
        new_window.geometry("1920x1080")

        label = tk.Label(new_window, text=f"Terv neve: {plan_name}", font=('Helvetica', 14))
        label.pack(pady=10)

        contact_label = tk.Label(new_window, text=f"Név: {contact_name}", font=('Helvetica', 12))
        contact_label.pack(pady=10)

    def confirm_delete(self, plan_name):
        """Terv törlésének megerősítése és törlése."""
        if messagebox.askyesno("Törlés megerősítése", f"Biztos törölni szeretné ezt a tervet : '{plan_name}'?"):
            self.delete_plan(plan_name)

    def delete_plan(self, plan_name):
        """Terv törlése az adatbázisból és a panelből."""
        self.cursor.execute("DELETE FROM plans WHERE plan_name = ?", (plan_name,))
        self.conn.commit()

        for widget in self.plan_container.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children()[0].cget("text") == plan_name:
                widget.destroy()
                break

    def load_plans(self):
        """A tervek betöltése az adatbázisból."""
        self.cursor.execute("SELECT plan_name, contact_name FROM plans")
        plans = self.cursor.fetchall()

        for plan_name, contact_name in plans:
            self.add_plan_panel(plan_name, contact_name)

    def __del__(self):
        """Destruktor, bezárjuk az adatbázis kapcsolatot."""
        if self.conn:
            self.conn.close()


# A list_creator.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('list_creator.py')

    contact_page = ListCreatorPage(root)
    contact_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
