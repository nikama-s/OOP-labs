import tkinter as tk
from tkinter import ttk, messagebox

class EditClassesWindow:
    def __init__(self, root, ClassManager, render_callback):
        self.root = root
        self.class_manager = ClassManager
        self.render_callback = render_callback
        self.edit_window = None
        self.editor_window = None
        self.listbox = None
        self.create_window()

    def create_window(self):
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Classes")
        self.edit_window.geometry("400x400")

        self.listbox = tk.Listbox(self.edit_window)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)
        for cls in self.class_manager.get_classes().keys():
            self.listbox.insert(tk.END, cls)

        button_frame = ttk.Frame(self.edit_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Edit", command=self.edit_class).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_class).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Create", command=self.create_class).pack(side="left", padx=5)

    def edit_class(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a class to edit.")
            self.edit_window.focus()
            return
        class_name = self.listbox.get(selected[0])
        self.open_class_editor(class_name, edit=True)

    def delete_class(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a class to delete.")
            self.edit_window.focus()
            return
        class_name = self.listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the class '{class_name}'?")
        if confirm:
            self.class_manager.delete_class(class_name)
            self.edit_window.focus()
            self.refresh_class_list()
            self.render_callback()

    def create_class(self):
        self.open_class_editor(None, edit=False)

    def open_class_editor(self, class_name=None, edit=False):
        if self.editor_window and self.editor_window.winfo_exists():
            self.editor_window.lift()  # Bring the existing window to the front
            return
        self.editor_window = tk.Toplevel(self.edit_window)
        self.editor_window.title(f"Edit Class: {class_name}" if edit else "Create Class")
        self.editor_window.geometry("400x500")

        ttk.Label(self.editor_window, text="Class Name:").pack(pady=5)
        name_entry = ttk.Entry(self.editor_window)
        name_entry.pack(pady=5)

        if edit and class_name:
            name_entry.insert(0, class_name)

        attr_frame, attr_entry, attr_listbox = self.create_list_section(self.editor_window, "Attributes")
        methods_frame, methods_entry, methods_listbox = self.create_list_section(self.editor_window, "Methods")
        class_data = self.class_manager.get_classes().get(class_name, {})

        if edit:
            for attr in class_data.get("attributes", []):
                attr_listbox.insert(tk.END, attr)
            for method in class_data.get("methods", []):
                methods_listbox.insert(tk.END, method)

        ttk.Button(self.editor_window, text="Save", command=lambda: self.save_class_changes(
            self.editor_window, name_entry, attr_listbox, methods_listbox, class_name, edit
        )).pack(pady=10)

    def create_list_section(self, parent, label):
        frame = ttk.Frame(parent)
        frame.pack(pady=5, fill="x")

        ttk.Label(frame, text=f"{label}:").pack(side="top", anchor="w")
        entry = ttk.Entry(frame)
        entry.pack(side="top", fill="x", padx=5)

        listbox = tk.Listbox(frame, height=5)
        listbox.pack(fill="both", expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)

        add_button = ttk.Button(
            btn_frame,
            text="Add",
            command=lambda: self.add_to_list(entry, listbox, label)
        )
        add_button.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=lambda: self.edit_in_list(entry, listbox, label, add_button)).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", command=lambda: self.delete_from_list(listbox, label)).pack(side="left", padx=5)

        return frame, entry, listbox

    def add_to_list(self, entry, listbox, label):
        item = entry.get().strip()
        if not item:
            messagebox.showerror("Error", f"{label} name cannot be empty.")
            return
        if item in listbox.get(0, tk.END):
            messagebox.showerror("Error", f"{label} '{item}' already exists.")
            return
        listbox.insert(tk.END, item)
        entry.delete(0, tk.END)

    def delete_from_list(self, listbox, label):
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", f"Please select a {label} to delete.")
            return
        listbox.delete(selected)

    def edit_in_list(self, entry, listbox, label, add_button):
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", f"Please select a {label} to edit.")
            return
        old_item = listbox.get(selected)
        entry.delete(0, tk.END)
        entry.insert(0, old_item)
        entry.focus_set()
        add_button.config(
            text="Update",
            command=lambda: self.save_edit(entry, listbox, selected, label, add_button)
        )

    def save_edit(self, entry, listbox, selected, label, add_button):
        new_item = entry.get().strip()
        if not new_item:
            messagebox.showerror("Error", f"{label} name cannot be empty.")
            return
        if new_item in listbox.get(0, tk.END) and new_item != listbox.get(selected):
            messagebox.showerror("Error", f"{label} '{new_item}' already exists.")
            return

        listbox.delete(selected)
        listbox.insert(selected, new_item)
        entry.delete(0, tk.END)

        add_button.config(
            text="Add",
            command=lambda: self.add_to_list(entry, listbox, label)
        )

    def save_class_changes(self, editor_window, name_entry, attr_listbox, methods_listbox, original_name, edit):
        new_name = name_entry.get().strip()
        class_data = self.class_manager.get_classes()
        if not new_name:
            messagebox.showerror("Error", "Class name cannot be empty.")
            editor_window.focus()
            return
        if new_name != original_name and new_name in class_data:
            messagebox.showerror("Error", f"Class '{new_name}' already exists.")
            editor_window.focus()
            return
        attributes = list(attr_listbox.get(0, tk.END))
        methods = list(methods_listbox.get(0, tk.END))

        if not edit:
            self.class_manager.add_class(new_name, attributes, methods)
        else:
            self.class_manager.edit_class(new_name, original_name, attributes, methods)

        editor_window.destroy()
        self.refresh_class_list()
        self.render_callback()
    def refresh_class_list(self):
        self.listbox.delete(0, tk.END)
        for cls in self.class_manager.get_classes().keys():
            self.listbox.insert(tk.END, cls)