import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

# A fő ablak létrehozása
root = ThemedTk(theme="elegance")
root.title("CLIPTIMIZER")
root.geometry("1920x1080")
root.configure(bg='#696969')

# Kép betöltése és beállítása ikonként
icon_image = Image.open("images/cliptimizer.png")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

# Funkciók+
def quit_program():
    root.quit()

# Stílusok és betűtípusok beállítása
style = ttk.Style()
style.configure('Quit.TButton', font=('Helvetica', 12, 'bold'))

# A "kilépés" gomb
quit_button = ttk.Button(root, text="Kilépés", command=quit_program, style='Quit.TButton')
quit_button.pack(side=tk.BOTTOM, pady=30)

# A Tkinter event loop elindítása
root.mainloop()
