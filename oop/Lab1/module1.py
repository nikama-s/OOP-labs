import tkinter as tk
from tkinter import simpledialog, Toplevel

class Module1(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Введіть текст")
        self.geometry("400x200")
        self.label = tk.Label(self, text="Введіть текст:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(padx=20, pady=10)


        self.ok_button = tk.Button(self, text="Так", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.cancel_button = tk.Button(self, text="Відміна", command=self.on_cancel)
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.result = None

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.destroy()

