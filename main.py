import tkinter as tk
from tkinter import PhotoImage, messagebox
import pystray
from PIL import Image
import add
import contact
import database
import delete
import edit
import home
import active_list_creator
import login
import plan_creator
import search


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Kezdetben a felhasználó nincs bejelentkezve
        self.logged_in = False

        # Az alapvető dolgok
        self.geometry('1920x1080')
        self.title('Cliptimizer')
        self.iconbitmap('images/cliptimizer.ico')
        self.configure(bg='black')
        self.tray_icon_image = Image.open('images/cliptimizer.png')
        self.tray_icon = pystray.Icon("name", self.tray_icon_image, "Cliptimizer", self.create_tray_menu())
        self.tray_icon.run_detached()

        # Az osztály attribútumainak inicializálása
        self.login_page = None
        self.home_image = None
        self.contact_image = None
        self.database_image = None
        self.search_image = None
        self.plan_creator_image = None
        self.add_image = None
        self.delete_image = None
        self.edit_image = None
        self.active_list_creator_image = None
        self.sign_out_image = None
        self.quit_image = None
        self.home_button = None
        self.contact_button = None
        self.database_button = None
        self.search_button = None
        self.add_button = None
        self.edit_button = None
        self.delete_button = None
        self.plan_creator_button = None
        self.active_list_creator_button = None
        self.sign_out_button = None
        self.quit_button = None
        self.menu_bar_panel = None
        self.pages_container = None
        self.current_page = None

        # Bejelentkezési ablak
        self.show_login()

    def create_tray_menu(self):
        """Tálcaikon menüje."""
        menu = pystray.Menu(
            pystray.MenuItem("Megnyitás", self.tray_show),
            pystray.MenuItem("Kilépés", self.tray_quit)
        )
        return menu

    def tray_show(self):
        """Az alkalmazás megjelenítése a tálcaikonról."""
        self.deiconify()

    def tray_quit(self):
        """Az alkalmazás bezárása a tálcaikonról."""
        self.tray_icon.stop()
        self.quit()

    def init_ui(self):
        """A felhasználói felület inicializálása (menu bar, ikonok, gombok, container, elrendezések)."""
        # A menu bar
        self.menu_bar_panel = tk.Frame(self, bg='white', width=80)
        self.menu_bar_panel.pack(side=tk.LEFT, fill=tk.Y, pady=4, padx=5)

        # A bal oldalt található ikonok
        self.home_image = PhotoImage(file='images/home_resized.png')
        self.contact_image = PhotoImage(file='images/envelope_resized.png')
        self.database_image = PhotoImage(file='images/database_resized.png')
        self.search_image = PhotoImage(file='images/search_resized.png')
        self.plan_creator_image = PhotoImage(file='images/plan-strategy_resized.png')
        self.add_image = PhotoImage(file='images/add_resized.png')
        self.delete_image = PhotoImage(file='images/delete_resized.png')
        self.edit_image = PhotoImage(file='images/edit_resized.png')
        self.active_list_creator_image = PhotoImage(file='images/list_resized.png')
        self.sign_out_image = PhotoImage(file='images/sign-out-alt_resized.png')
        self.quit_image = PhotoImage(file='images/power_resized.png')

        # Az ikonok, amik lényegében gombok is
        self.home_button = tk.Button(self.menu_bar_panel, image=self.home_image, bg='white', bd=0,
                                     command=self.show_home)
        self.home_button.pack(pady=(10, 10))

        self.active_list_creator_button = tk.Button(self.menu_bar_panel, image=self.active_list_creator_image,
                                                    bg='white',
                                                    bd=0,
                                                    command=self.show_active_list_creator)
        self.active_list_creator_button.pack(pady=(10, 10))

        self.plan_creator_button = tk.Button(self.menu_bar_panel, image=self.plan_creator_image, bg='white', bd=0,
                                             command=self.show_plan_creator)
        self.plan_creator_button.pack(pady=(10, 10))

        self.database_button = tk.Button(self.menu_bar_panel, image=self.database_image, bg='white', bd=0,
                                         command=self.show_database)
        self.database_button.pack(pady=(10, 10))

        self.search_button = tk.Button(self.menu_bar_panel, image=self.search_image, bg='white', bd=0,
                                       command=self.search_database)
        self.search_button.pack(pady=(10, 10))

        self.add_button = tk.Button(self.menu_bar_panel, image=self.add_image, bg='white', bd=0,
                                    command=self.add_database)
        self.add_button.pack(pady=(10, 10))

        self.edit_button = tk.Button(self.menu_bar_panel, image=self.edit_image, bg='white', bd=0,
                                     command=self.edit_database)
        self.edit_button.pack(pady=(10, 10))

        self.delete_button = tk.Button(self.menu_bar_panel, image=self.delete_image, bg='white', bd=0,
                                       command=self.delete_database)
        self.delete_button.pack(pady=(10, 10))

        self.contact_button = tk.Button(self.menu_bar_panel, image=self.contact_image, bg='white', bd=0,
                                        command=self.show_contact)
        self.contact_button.pack(pady=(10, 10))

        self.sign_out_button = tk.Button(self.menu_bar_panel, image=self.sign_out_image, bg='white', bd=0,
                                         command=self.logout_application)
        self.sign_out_button.pack(pady=(10, 10))

        self.quit_button = tk.Button(self.menu_bar_panel, image=self.quit_image, bg='white', bd=0,
                                     command=self.quit_application)
        self.quit_button.pack(pady=(10, 10))

        # A container létrehozása más tartalmak megjelenítésére
        self.pages_container = tk.Frame(self, bg='white')
        self.pages_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Az alapértelmezett ablak
        self.current_page = None
        self.show_home()

    def show_home(self):
        """A HomePage mutatása (első ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = home.HomePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_active_list_creator(self):
        """A ListCreatorPage mutatása (második ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = active_list_creator.ListCreatorPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_database(self):
        """A DatabasePage mutatása (harmadik ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = database.DatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def search_database(self):
        """A SearchDatabasePage mutatása (negyedik ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = search.SearchDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def add_database(self):
        """Az AddDatabasePage mutatása (ötödik ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = add.AddDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def edit_database(self):
        """Az EditDatabasePage mutatása (hatodik ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = edit.EditDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def delete_database(self):
        """A DeleteDatabasePage mutatása (hetedik ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = delete.DeleteDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_plan_creator(self):
        """A PlanCreatorPage mutatása (nyolcadik ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = plan_creator.PlanCreatorPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_contact(self):
        """A ContactPage mutatása (utolsó ablak)."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = contact.ContactPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def logout_application(self):
        """Felhasználó kijelentkezése."""
        confirm = messagebox.askyesno("Kijelentkezés", "Biztos kijelentkezel?")
        if confirm:
            self.logged_in = False
            if self.menu_bar_panel:
                self.menu_bar_panel.pack_forget()
            if self.pages_container:
                self.pages_container.pack_forget()
            self.show_login()

    def show_login(self):
        """A LoginPage mutatása (program előtti bejelentkezésre szolgáló ablak)."""
        self.login_page = login.LoginPage(self, self)
        self.login_page.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self):
        """Sikeres bejelentkezés kezelése."""
        self.logged_in = True
        self.login_page.pack_forget()
        self.init_ui()
        self.show_home()

    def quit_application(self):
        """Kilépés előtti megerősítés és a program biztonságos leállítása."""
        if messagebox.askyesno("Kilépés", "Biztosan ki akarsz lépni?"):
            if hasattr(self, 'tray_icon'):
                self.tray_icon.stop()
            self.quit()
            self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
