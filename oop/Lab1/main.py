import tkinter as tk
from module1 import Module1
from module2 import Module2
from tkinter import Menu


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.create_menu()

        self.label = tk.Label(self.root, text="", font=("Arial", 14))
        self.label.pack(pady=20)

    def create_menu(self):
        menu_bar = Menu(self.root)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Робота1", command=self. handle_robota1)
        file_menu.add_separator()
        file_menu.add_command(label="Робота2", command=self.handle_robota2)

        menu_bar.add_cascade(label="Меню", menu=file_menu)
        self.root.config(menu=menu_bar)

    def  handle_robota1(self):
        self.root.withdraw()

        dialog = Module1(self.root)
        self.root.wait_window(dialog)

        result = dialog.result

        self.root.deiconify()
        self.label.config(text=result)

    def handle_robota2(self):
        self.root.withdraw()

        dialog = Module2(self.root)
        self.root.wait_window(dialog)

        result = dialog.result

        self.root.deiconify()
        self.label.config(text=result)


if __name__ == "__main__":
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()


