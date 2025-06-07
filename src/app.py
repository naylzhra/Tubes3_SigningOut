from gui.components.main_window import MainWindow
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MainWindow()
    app.resizable(False, False)
    app.mainloop()