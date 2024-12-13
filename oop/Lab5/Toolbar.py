import tkinter as tk
from Tooltip import ToolTip


class Toolbar(tk.Frame):
    def __init__(self, parent, set_shape_callback, button_data):
        super().__init__(parent, bd=1, relief=tk.RAISED)

        self.set_shape_callback = set_shape_callback
        self.active_button = None
        self.buttons = {}

        self.button_data = button_data

        self.create_toolbar()

    def create_toolbar(self):
        for shape_type, data in self.button_data.items():
            btn = tk.Button(
                self,
                image=data["image"],
                width=50,
                height=30,
                borderwidth=2
            )
            btn.config(command=lambda st=shape_type, b=btn: self.on_button_click(st, b))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            ToolTip(btn, data["tooltip"])
            self.buttons[shape_type] = btn


    def on_button_click(self, shape_type, button):
        if self.active_button != button:
            self.set_shape_callback(shape_type)
            self.update_button_state(button)

    def update_button_state(self, button):
        if self.active_button:
            self.active_button.config(bg="#f0f0f0", relief=tk.RAISED)
        self.active_button = button
        self.active_button.config(bg="#d8d8d8", relief=tk.SUNKEN)

    def update_from_menu(self, shape_type):
        button = self.buttons.get(shape_type)
        self.update_button_state(button)

    def reset_buttons(self):
        if self.active_button:
            self.active_button.config(bg="#f0f0f0", relief=tk.RAISED)
            self.active_button = None