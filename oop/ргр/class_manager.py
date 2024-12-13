from tkinter import messagebox, filedialog
import json


class ClassManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.classes_data = {}
            self.connection_keys = {
                "Inheritance": "inheritance",
                "Compositions": "compositions",
                "Aggregations": "aggregations",
                "Dependencies": "dependencies",
                "Associations": "associations",
                "Realizations": "realizations",
            }


    def add_class(self, name, attributes=None, methods=None, parents=None):
        if name in self.classes_data:
            raise ValueError(f"Class '{name}' already exists.")
        self.classes_data[name] = {
            "inheritance": parents or [],
            "attributes": attributes or [],
            "methods": methods or [],
            "compositions": [],
            "aggregations": [],
            "dependencies": [],
            "associations": [],
            "realizations": [],
        }

    def delete_class(self, name):
        if name in self.classes_data:
            del self.classes_data[name]
            self._remove_references_to_class(name)

    def edit_class(self, name, original_name, attributes=None, methods=None, parents=None, compositions=None, aggregations=None):
        if name != original_name:
            self.classes_data[name] = self.classes_data.pop(original_name)
            self._update_references(original_name, name)
        self.classes_data[name]["attributes"] = attributes
        self.classes_data[name]["methods"] = methods

    def get_classes(self):
        return self.classes_data

    def _remove_references_to_class(self, class_name):
        for cls, details in self.classes_data.items():
            for relation in ["inheritance", "compositions", "aggregations", "dependencies", "associations", "realizations"]:
                details[relation] = [item for item in details[relation] if item != class_name]

    def _update_references(self, old_name, new_name):
        for cls, details in self.classes_data.items():
            for relation in ["inheritance", "compositions", "aggregations", "dependencies", "associations", "realizations"]:
                details[relation] = [new_name if item == old_name else item for item in details[relation]]

    def save_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "w") as json_file:
                json.dump(self.classes_data, json_file, indent=4)
            messagebox.showinfo("Success", f"Classes data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save classes data: {e}")

    def open_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "r") as json_file:
                loaded_data = json.load(json_file)
            self.classes_data = loaded_data
            messagebox.showinfo("Success", f"Classes data loaded from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open classes data: {e}")