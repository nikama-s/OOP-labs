import tkinter as tk
from tkinter import ttk, messagebox

class EditConnectionsWindow:
    def __init__(self, root, ClassManager, render_callback):
        self.root = root
        self.class_manager = ClassManager
        self.render_callback = render_callback
        self.conn_window = None
        self.create_connection_window = None
        self.create_window()

    def create_window(self):
        self.conn_window = tk.Toplevel(self.root)
        self.conn_window.title("Manage Connections")
        self.conn_window.geometry("400x400")

        notebook = ttk.Notebook(self.conn_window)
        notebook.pack(fill="both", expand=True)

        for conn_type in ["Inheritance", "Compositions", "Aggregations", "Dependencies", "Associations", "Realizations"]:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=conn_type)

            listbox = tk.Listbox(frame)
            listbox.pack(fill="both", expand=True, padx=10, pady=10)
            self.populate_connection_list(listbox, conn_type)

            button_frame = ttk.Frame(frame)
            button_frame.pack(pady=10)

            ttk.Button(button_frame, text="Delete",command=lambda lb=listbox, ct=conn_type: self.handle_delete_connection(lb, ct)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Create",command=lambda ct=conn_type: self.handle_create_connection(ct)).pack(side="left", padx=5)

    def populate_connection_list(self, listbox, connection_type):
        listbox.delete(0, tk.END)
        for class_name, details in self.class_manager.get_classes().items():
            for conn in details[self.class_manager.connection_keys[connection_type]]:
                if connection_type == "Inheritance":
                    listbox.insert(tk.END, f"{class_name} -> {conn}")
                else:
                    listbox.insert(tk.END, f"{conn} -> {class_name}")

    def handle_delete_connection(self, listbox, connection_type):
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a connection to delete.")
            self.conn_window.focus()
            return

        connection = listbox.get(selected[0])
        if connection_type == "Inheritance":
            source, target = connection.split(" -> ")
        else:
            target, source = connection.split(" -> ")

        try:
            self.class_manager.classes_data[source][self.class_manager.connection_keys[connection_type]].remove(target)
            listbox.delete(selected)
            self.render_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete connection: {e}")

    def handle_create_connection(self, connection_type):
        if self.create_connection_window and self.create_connection_window.winfo_exists():
            self.create_connection_window.lift()
            return

        self.create_connection_window = tk.Toplevel(self.conn_window)
        self.create_connection_window.title(f"Create {connection_type}")
        self.create_connection_window.geometry("350x200")

        ttk.Label(self.create_connection_window, text=f"Create a '{connection_type}' connection:", font=("Helvetica", 10, "bold")).pack(pady=10)

        connection_frame = ttk.Frame(self.create_connection_window)
        connection_frame.pack(pady=10)

        source_var = tk.StringVar()
        source_combobox = ttk.Combobox(connection_frame, textvariable=source_var, values=list(self.class_manager.get_classes().keys()), state="readonly", width=15)
        source_combobox.grid(row=0, column=0, padx=5)

        ttk.Label(connection_frame, text="->", font=("Helvetica", 12)).grid(row=0, column=1, padx=5)

        target_var = tk.StringVar()
        target_combobox = ttk.Combobox(connection_frame, textvariable=target_var, values=list(self.class_manager.get_classes().keys()), state="readonly", width=15)
        target_combobox.grid(row=0, column=2, padx=5)

        def save_connection():
            source = source_var.get()
            target = target_var.get()

            if not source or not target:
                messagebox.showerror("Error", "Both classes must be selected.")
                self.create_connection_window.focus()
                return
            if source == target:
                messagebox.showerror("Error", "The two classes cannot be the same.")
                self.create_connection_window.focus()
                return

            try:
                if connection_type == "Inheritance":
                    self.class_manager.classes_data[source][self.class_manager.connection_keys[connection_type]].append(target)
                else:
                    self.class_manager.classes_data[target][self.class_manager.connection_keys[connection_type]].append(source)
                self.create_connection_window.destroy()
                self.conn_window.focus()
                self.render_callback()

                self.update_connection_list(connection_type)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create connection: {e}")

        ttk.Button(self.create_connection_window, text="Save", command=save_connection).pack(pady=10)

    def update_connection_list(self, connection_type):
        notebook = self._find_notebook()
        if notebook:
            listbox = self._find_listbox_by_tab_text(notebook, connection_type)
            if listbox:
                self.populate_connection_list(listbox, connection_type)

    def _find_notebook(self):
        for child in self.conn_window.winfo_children():
            if isinstance(child, ttk.Notebook):
                return child
        return None

    def _find_listbox_by_tab_text(self, notebook, connection_type):
        for i, tab in enumerate(notebook.winfo_children()):
            if notebook.tab(i, "text") == connection_type:
                listbox = tab.winfo_children()[0] if tab.winfo_children() else None
                return listbox
        return None