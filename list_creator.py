import tkinter as tk
from tkinter import Toplevel, PhotoImage, OptionMenu, StringVar, messagebox, Spinbox
import sqlite3


class ListCreatorPage(tk.Frame):
    """A gyártási terv(ek) létrehozására szolgáló oldal."""

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # A termékek mezőinek tárolására szolgáló lista inicializálása
        self.product_entries = []

        # Az adatbázis kapcsolat
        self.conn = sqlite3.connect('cliptimizer.db')
        self.cursor = self.conn.cursor()

        # Adat lekérése a products táblából
        self.cursor.execute("SELECT name FROM products")
        self.product_names = [row[0] for row in self.cursor.fetchall()]

        # A cím
        label = tk.Label(self, text="TERVEK LÉTREHOZÁSA", bg='white', font=('Helvetica', 20, 'bold'), padx=20, pady=20)
        label.pack(anchor=tk.N)

        # Ezen az oldalon található képek
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

    def load_plans(self):
        """Tervek betöltése az adatbázisból és panelek megjelenítése."""
        self.cursor.execute("SELECT DISTINCT plan_name FROM plans")
        plans = self.cursor.fetchall()

        # Minden tervhez létrehozunk egy panelt
        for plan in plans:
            self.add_plan_panel(plan[0])

    def create_new_plan(self):
        """Egy terv létrehozása: Új ablak és adatbázis kapcsolódás."""
        new_window = Toplevel(self)
        new_window.title("Terv")
        new_window.geometry("1920x1080")

        # Cím az új ablakban
        label = tk.Label(new_window, text="Terv létrehozása", font=('Helvetica', 14))
        label.pack(pady=20)

        # Input mező a terv nevéhez
        plan_name_entry = tk.Entry(new_window)
        plan_name_entry.pack(pady=10)

        # Frame a termékeknek és az új termék gombnak
        product_frame = tk.Frame(new_window)
        product_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # Kezdő termék hozzáadása
        self.add_product_field(product_frame)

        # Az új termék hozzáadása gomb
        add_product_button = tk.Button(new_window, image=self.add_icon, bg='white', bd=0,
                                       command=lambda: self.add_product_field(product_frame))
        add_product_button.pack(pady=10)

        # Frame a mentés gombnak
        button_frame = tk.Frame(new_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Mentés gomb
        tk.Button(button_frame, text="Mentés", command=lambda: self.save_plan(new_window, plan_name_entry.get())).pack(
            pady=10)

    def add_product_field(self, window):
        """Új termék és mennyiség mezők hozzáadása."""
        product_frame = tk.Frame(window)
        product_frame.pack(pady=10)

        # Legördülő menü a termék nevével
        selected_product = StringVar(window)
        selected_product.set(self.product_names[0])
        product_menu = OptionMenu(product_frame, selected_product, *self.product_names)
        product_menu.pack(side=tk.LEFT, padx=10)

        # Spinbox mennyiség mező
        amount_entry = Spinbox(product_frame, from_=1, to=1000, width=5)
        amount_entry.pack(side=tk.LEFT, padx=10)

        # Hozzáadjuk a termék menü és mennyiség mezőt a listához
        self.product_entries.append((selected_product, amount_entry))

    def save_plan(self, window, plan_name):
        """Terv mentése az összes termékkel és mennyiséggel."""
        if plan_name and self.product_entries:
            for selected_product, amount_entry in self.product_entries:
                try:
                    product_name = selected_product.get()

                    # Mennyiség mező létezik-e és érvényes-e?
                    try:
                        amount_str = amount_entry.get()
                    except Exception as e:
                        messagebox.showerror("Hiba", f"Nem sikerült elérni a mennyiség mezőt: {e}")
                        return

                    # Mennyiség mező nem üres-e és egy számot tartalmaz-e?
                    if not amount_str.isdigit():
                        messagebox.showerror("Hiba", "A mennyiség mezőbe számot kell írni.")
                        return

                    amount = int(amount_str)

                    # Product ID lekérése a név alapján
                    self.cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
                    product_id = self.cursor.fetchone()[0]

                    # Adatok mentése az adatbázisba
                    self.cursor.execute(
                        "INSERT INTO plans (plan_name, product_ID, amount, start_time, end_time, hangers_needed) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (plan_name, product_id, amount, '', '', None))
                    self.conn.commit()

                except Exception as e:
                    messagebox.showerror("Hiba", f"Hiba történt a terv mentésekor: {e}")
                    return

            # Zárjuk be az új terv ablakot csak akkor, ha sikeres volt a mentés
            window.destroy()

            # Terv hozzáadása a listához
            self.add_plan_panel(plan_name)

    def add_plan_panel(self, plan_name):
        """Panel hozzáadása a tervhez."""
        panel = tk.Frame(self.plan_container, bg='lightgrey', bd=2, relief='solid')
        panel.pack(pady=5, padx=10, fill=tk.X)

        # Terv neve
        plan_label = tk.Label(panel, text=f"{plan_name}", bg='lightgrey', font=('Helvetica', 12))
        plan_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Terv megnézése
        view_button = tk.Button(panel, image=self.eye_icon, bg='lightgrey', bd=0,
                                command=lambda: self.view_plan(plan_name))
        view_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Terv törlése
        delete_button = tk.Button(panel, image=self.trash_icon, bg='lightgrey', bd=0,
                                  command=lambda: self.confirm_delete(plan_name))
        delete_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def view_plan(self, plan_name):
        """Terv megjelenítése egy új ablakban."""
        new_window = Toplevel(self)
        new_window.title(f"Terv: {plan_name}")
        new_window.geometry("1920x1080")

        label = tk.Label(new_window, text=f"Terv neve: {plan_name}", font=('Helvetica', 14))
        label.pack(pady=10)

        # A termékek megjelenítése a tervhez
        self.cursor.execute("SELECT product_ID, amount FROM plans WHERE plan_name = ?", (plan_name,))
        products = self.cursor.fetchall()

        for product_id, amount in products:
            self.cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
            product_name = self.cursor.fetchone()[0]
            product_label = tk.Label(new_window, text=f"Termék: {product_name} - Mennyiség: {amount}",
                                     font=('Helvetica', 12))
            product_label.pack(pady=5)

    def confirm_delete(self, plan_name):
        """Terv törlésének megerősítése és törlése."""
        if messagebox.askyesno("Törlés megerősítése", f"Biztos törölni szeretné ezt a tervet : "
                                                      f"'{plan_name}'?"):
            self.delete_plan(plan_name)

    def delete_plan(self, plan_name):
        """Terv törlése az adatbázisból és a panelből."""
        self.cursor.execute("DELETE FROM plans WHERE plan_name = ?", (plan_name,))
        self.conn.commit()

        # Frissítjük a felhasználói felületet
        for widget in self.plan_container.winfo_children():
            if isinstance(widget, tk.Frame):
                if widget.winfo_children()[0].cget("text") == plan_name:
                    widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")
    app = ListCreatorPage(root)
    app.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
