import tkinter as tk


class RobotPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # Ez egy beépített AI assistant lesz. Nem találtam még egy jó ingyenes lehetőséget,
        # de ha sokat dob a szakdolgozaton, akkor jobban utána nézek.
