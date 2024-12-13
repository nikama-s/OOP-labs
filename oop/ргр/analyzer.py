import os
import ast

class ClassAnalyzer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def analyze_python_files(folder_path):
        classes = {}
        python_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(folder_path)
            for file in files if file.endswith(".py")
        ]
        for file_path in python_files:
            file_classes = ClassAnalyzer.analyze_file(file_path)
            classes.update(file_classes)
        return classes

    @staticmethod
    def analyze_file(file_path):
        classes = {}
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        tree = ast.parse(file_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name, class_details = ClassAnalyzer.analyze_class(node)
                classes[class_name] = class_details
        return classes

    @staticmethod
    def analyze_class(node):
        class_name = node.name
        bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
        attributes, methods, compositions, aggregations = ClassAnalyzer.extract_class_contents(node.body)
        return class_name, {
            "inheritance": bases,
            "attributes": sorted(attributes),
            "methods": methods,
            "compositions": sorted(compositions),
            "aggregations": sorted(aggregations),
            "dependencies": [],
            "associations": [],
            "realizations": [],
        }

    @staticmethod
    def extract_class_contents(body):
        attributes = set()
        methods = []
        compositions = set()
        aggregations = set()
        for body_item in body:
            if isinstance(body_item, ast.FunctionDef):
                methods.append(body_item.name)
                attr, comp, agg = ClassAnalyzer.extract_self_attributes(body_item)
                attributes.update(attr)
                compositions.update(comp)
                aggregations.update(agg)
            elif isinstance(body_item, ast.Assign):
                attributes.update(ClassAnalyzer.extract_class_attributes(body_item))
        return attributes, methods, compositions, aggregations

    @staticmethod
    def extract_self_attributes(func_node):
        attributes, compositions, aggregations = set(), set(), set()
        for stmt in ast.walk(func_node):
            if ClassAnalyzer.is_self_attribute_assignment(stmt):
                attributes.add(stmt.targets[0].attr)
                ClassAnalyzer.classify_assignment(stmt.value, compositions, aggregations)
        return attributes, compositions, aggregations

    @staticmethod
    def is_self_attribute_assignment(node):
        return (
                isinstance(node, ast.Assign) and
                isinstance(node.targets[0], ast.Attribute) and
                isinstance(node.targets[0].value, ast.Name) and
                node.targets[0].value.id == "self"
        )

    @staticmethod
    def classify_assignment(value, compositions, aggregations):
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and not ClassAnalyzer.is_builtin_function(value.func.id):
            compositions.add(value.func.id)
        elif isinstance(value, ast.Name) and not value.id.islower():
            aggregations.add(value.id)

    @staticmethod
    def is_builtin_function(func_name):
        builtins = {
            "sorted", "list", "set", "dict", "tuple", "len", "range", "int", "float", "str",
            "bool", "sum", "max", "min", "map", "filter", "zip", "enumerate", "open"
        }
        return func_name in builtins

    @staticmethod
    def extract_class_attributes(assign_node):
        return {target.id for target in assign_node.targets if isinstance(target, ast.Name)}