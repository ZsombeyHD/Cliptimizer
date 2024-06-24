import tkinter as tk


# Ez egy beépített AI assistant lesz. Nem találtam még egy jó ingyenes lehetőséget,
# de ha sokat dob a szakdolgozaton, akkor jobban utána nézek.


class RobotPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        label = tk.Label(self, text="AI ASSZISZTENS : KÉRDEZZ BÁRMIT!", bg='white', font=('Helvetica', 20, 'bold'),
                         padx=20, pady=20)
        label.pack(anchor=tk.N)


# A robot.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('robot.py')

    # A RobotPage
    home_page = RobotPage(root)
    home_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
