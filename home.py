import tkinter as tk
from PIL import Image, ImageTk


class HomePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg='white')

        # Középre igazított fő keret
        self.pack(fill=tk.BOTH, expand=True)

        # Top frame a nagy szöveg és a kép számára
        top_frame = tk.Frame(self, bg='white')
        top_frame.pack(expand=True, pady=(100, 20))

        # A kép betöltése és átméretezése
        image = Image.open('images/cliptimizer.png')
        resized_image = image.resize((200, 200), Image.LANCZOS)
        self.clip_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(top_frame, image=self.clip_image, bg='white')
        image_label.pack(side=tk.TOP, padx=20, pady=10)

        # Cím
        title_label = tk.Label(top_frame, text="CLIPTIMIZER", bg='white', font=('Helvetica', 50, 'bold'))
        title_label.pack(expand=True)

        # Alsó szöveg
        subtitle_label = tk.Label(top_frame, text="NP Hungária festőüzemének gyártástervezője", bg='white',
                                  font=('Helvetica', 20), padx=20, pady=10)
        subtitle_label.pack(pady=(10, 0))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1920x1080')

    # A HomePage
    home_page = HomePage(root)
    home_page.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
