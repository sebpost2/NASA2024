import tkinter as tk
import ttkbootstrap as ttk

def create_gui():
    global root
    root = ttk.Window(themename="darkly")
    root.title("Galactic Games")
    root.geometry("1000x700")

    # Prueba diferentes fuentes
    fonts = ["Arial", "Helvetica", "Courier New", "Times New Roman", "Verdana", "Comic Sans MS", "Impact"]
    for font in fonts:
        title_label = ttk.Label(root, text="Galactic Games", font=(font, 50), foreground="#663399", background="#000033")
        title_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
