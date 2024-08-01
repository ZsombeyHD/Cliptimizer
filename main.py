import tkinter as tk
from tkinter import PhotoImage

import pystray
from PIL import Image

import add
import contact
import database
import delete
import edit
import home
import list_creator
import login
import robot
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
        self.robot_image = None
        self.add_image = None
        self.delete_image = None
        self.edit_image = None
        self.list_creator_image = None
        self.home_button = None
        self.contact_button = None
        self.database_button = None
        self.search_button = None
        self.add_button = None
        self.edit_button = None
        self.delete_button = None
        self.robot_button = None
        self.list_creator_button = None
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
        menu_bar_panel = tk.Frame(self, bg='white', width=80)
        menu_bar_panel.pack(side=tk.LEFT, fill=tk.Y, pady=4, padx=5)

        # A bal oldalt található ikonok
        self.home_image = PhotoImage(file='images/home_resized.png')
        self.contact_image = PhotoImage(file='images/envelope_resized.png')
        self.database_image = PhotoImage(file='images/database_resized.png')
        self.search_image = PhotoImage(file='images/search_resized.png')
        self.robot_image = PhotoImage(file='images/robot_resized.png')
        self.add_image = PhotoImage(file='images/add_resized.png')
        self.delete_image = PhotoImage(file='images/delete_resized.png')
        self.edit_image = PhotoImage(file='images/edit_resized.png')
        self.list_creator_image = PhotoImage(file='images/list_resized.png')

        # Az ikonok, amik lényegében gombok is
        self.home_button = tk.Button(menu_bar_panel, image=self.home_image, bg='white', bd=0,
                                     command=self.show_home)
        self.home_button.pack(pady=(10, 10))

        self.list_creator_button = tk.Button(menu_bar_panel, image=self.list_creator_image, bg='white', bd=0,
                                             command=self.show_list_creator)
        self.list_creator_button.pack(pady=(10, 10))

        self.database_button = tk.Button(menu_bar_panel, image=self.database_image, bg='white', bd=0,
                                         command=self.show_database)
        self.database_button.pack(pady=(10, 10))

        self.search_button = tk.Button(menu_bar_panel, image=self.search_image, bg='white', bd=0,
                                       command=self.search_database)
        self.search_button.pack(pady=(10, 10))

        self.add_button = tk.Button(menu_bar_panel, image=self.add_image, bg='white', bd=0,
                                    command=self.add_database)
        self.add_button.pack(pady=(10, 10))

        self.edit_button = tk.Button(menu_bar_panel, image=self.edit_image, bg='white', bd=0,
                                     command=self.edit_database)
        self.edit_button.pack(pady=(10, 10))

        self.delete_button = tk.Button(menu_bar_panel, image=self.delete_image, bg='white', bd=0,
                                       command=self.delete_database)
        self.delete_button.pack(pady=(10, 10))

        self.robot_button = tk.Button(menu_bar_panel, image=self.robot_image, bg='white', bd=0,
                                      command=self.show_robot)
        self.robot_button.pack(pady=(10, 10))

        self.contact_button = tk.Button(menu_bar_panel, image=self.contact_image, bg='white', bd=0,
                                        command=self.show_contact)
        self.contact_button.pack(pady=(10, 10))

        # A container létrehozása más tartalmak megjelenítésére
        self.pages_container = tk.Frame(self, bg='white')
        self.pages_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Az alapértelmezett ablak
        self.current_page = None
        self.show_home()

    def show_home(self):
        """A HomePage mutatása (első ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
        HomePage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = home.HomePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_list_creator(self):
        """A ListCreatorPage mutatása (második ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
        ListCreatorPage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén
        visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = list_creator.ListCreatorPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_database(self):
        """A DatabasePage mutatása (harmadik ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
         DatabasePage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = database.DatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def search_database(self):
        """A SearchDatabassePage mutatása (negyedik ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
        SearchDatabasePage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén
        visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = search.SearchDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def add_database(self):
        """Az AddDatabasePage mutatása (ötödik ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
        AddDatabasePage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén
        visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = add.AddDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def edit_database(self):
        """Az EditDatabasePage mutatása (hatodik ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
        EditDatabasePage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén
        visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = edit.EditDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def delete_database(self):
        """A DeleteDatabasePage mutatása (hetedik ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
        DeleteDatabasePage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén
        visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = delete.DeleteDatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_robot(self):
        """A RobotPage mutatása (nyolcadik ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
         RobotPage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = robot.RobotPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_contact(self):
        """A ContactPage mutatása (utolsó ablak). Oldal megjelenítése, esetleges jelenlegi oldal elrejtése,
         ContactPage objektum létrehozás és containerben megjelenítés. Sikertelen bejelentkezés esetén visszatérés."""
        if not self.logged_in:
            return
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = contact.ContactPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_login(self):
        """A LoginPage mutatása (program előtti bejelentkezésre szolgáló ablak). Itt nincs container,
        hiszen a LoginPage nem függ tőle."""
        self.login_page = login.LoginPage(self, self)
        self.login_page.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self):
        """Sikeres bejelentkezés kezelése."""
        self.logged_in = True
        self.login_page.pack_forget()
        self.init_ui()
        self.show_home()


# A main.py fájl közvetlen elindítása
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
