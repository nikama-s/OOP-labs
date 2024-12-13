import tkinter as tk
from tkinter import ttk


class TableWindow(tk.Toplevel):
    def __init__(self, parent, highlight_callback, not_highlight_callback, delete_row_callback, hide_table_window):
        super().__init__(parent)
        self.title("Таблиця об’єктів")
        self.geometry("600x200")
        self.hide_table_window = hide_table_window

        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.hide_table_window)

        self.highlight_callback = highlight_callback
        self.delete_row_callback = delete_row_callback
        self.not_highlight_callback = not_highlight_callback
        self.last_selected_item = None

        columns = ("Name", "x1", "y1", "x2", "y2")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self._setup_tree(columns)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<BackSpace>", self.delete_selected_row)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _setup_tree(self, columns):
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=50, width=100, stretch=True)

    def add_row(self, name, x1, y1, x2, y2):
        self.tree.insert("", "end", values=(name, x1, y1, x2, y2))

    def on_select(self, event):
        selected_items = self.tree.selection()
        if len(selected_items) < 1: return

        selected_item = selected_items[0]
        if selected_item == self.last_selected_item:
            self.deselect_item(selected_item)
        else:
            self.select_item(selected_item)

    def deselect_item(self, item):
        self.tree.selection_remove(item)
        self.last_selected_item = None
        self.not_highlight_callback()

    def select_item(self, item):
        values = self.tree.item(item, "values")
        self.highlight_callback(values)
        self.last_selected_item = item

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def remove_last_row(self):
        rows = self.tree.get_children()
        if rows:
            self.tree.delete(rows[-1])

    def delete_selected_row(self, event=None):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.delete_row_callback(values)
            self.tree.delete(selected_item[0])