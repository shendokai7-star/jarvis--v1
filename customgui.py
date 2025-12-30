import tkinter as tk
from PIL import Image, ImageTk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("1322x851")

        self.label = tk.Label(self, bg="black")
        self.label.place(x=-60, y=-40, width=1381, height=911)

        self.label_2 = tk.Label(self, bg="black", fg="black", bd=3, relief="solid")
        self.label_2.place(x=0, y=0, width=1322, height=851)

        self.gif_image = Image.open("guifile/00b6c716490c3ec6fe4c9bef2b595f43.gif")
        self.gif_image = self.gif_image.resize((1091, 801), Image.ANTIALIAS)
        self.gif_photo = ImageTk.PhotoImage(self.gif_image)
        self.gif = tk.Label(self, image=self.gif_photo, bd=1, relief="solid")
        self.gif.place(x=160, y=20)

        self.terminal = tk.Text(self, bg="black", fg="white", font=("Open Sans", 10))
        self.terminal.place(x=40, y=570, width=381, height=221)

        self.time2023 = tk.Text(self, bg="black", fg="white", font=("MS Shell Dlg 2", 25))
        self.time2023.place(x=1010, y=760, width=291, height=81)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
