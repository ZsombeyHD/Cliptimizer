import tkinter as tk
from tkinter import PhotoImage
import home
import contact
import database


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry('1920x1080')
        self.title('Cliptimizer')
        self.iconbitmap('images/cliptimizer.ico')
        self.configure(bg='black')

        menu_bar_panel = tk.Frame(self, bg='white', width=80)
        menu_bar_panel.pack(side=tk.LEFT, fill=tk.Y, pady=4, padx=5)

        self.home_image = PhotoImage(file='images/home_resized.png')
        self.contact_image = PhotoImage(file='images/envelope_resized.png')
        self.database_image = PhotoImage(file='images/database_resized.png')

        home_button = tk.Button(menu_bar_panel, image=self.home_image, bg='white', bd=0, command=self.show_home)
        home_button.pack(pady=(10, 10))

        database_button = tk.Button(menu_bar_panel, image=self.database_image, bg='white', bd=0,
                                    command=self.show_database)
        database_button.pack(pady=(10, 10))

        contact_button = tk.Button(menu_bar_panel, image=self.contact_image, bg='white', bd=0,
                                   command=self.show_contact)
        contact_button.pack(pady=(10, 10))

        self.pages_container = tk.Frame(self, bg='white')
        self.pages_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.current_page = None
        self.show_home()

    def show_home(self):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = home.HomePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_contact(self):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = contact.ContactPage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_database(self):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = database.DatabasePage(self.pages_container)
        self.current_page.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
