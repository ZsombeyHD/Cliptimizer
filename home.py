import tkinter as tk


class HomePage(tk.Frame):
    """Ez az alapértelmezett úgymond főoldal bejelentkezés után."""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')
        self.pack(fill=tk.BOTH, expand=True)

        # Top frame a nagy szöveg és a kép számára
        top_frame = tk.Frame(self, bg='white')
        top_frame.pack(expand=True, pady=(100, 20))

        # A kép
        self.clip_image = tk.PhotoImage(file='images/cliptimizer.png')
        image_label = tk.Label(top_frame, image=self.clip_image, bg='white')
        image_label.pack(side=tk.TOP, padx=20, pady=10)

        # Cím és alsó szöveg
        title_label = tk.Label(top_frame, text="CLIPTIMIZER", bg='white', font=('Helvetica', 50, 'bold'))
        title_label.pack(expand=True)

        subtitle_label = tk.Label(top_frame, text="NP Hungária festőüzemének gyártástervezője", bg='white',
                                  font=('Helvetica', 20), padx=20, pady=10)
        subtitle_label.pack(pady=(10, 0))


# A home.py közvetlen elindítása
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title('home.py')

    # A HomePage
    home_page = HomePage(root)
    home_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
