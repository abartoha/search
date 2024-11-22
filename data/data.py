import json
from PyQt5.QtWidgets import QMessageBox

def load_data(file_path, parent=None):
    """
    Load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        parent (QWidget, optional): Parent widget for error dialogs.

    Returns:
        list: The loaded data or an empty list if an error occurred.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        QMessageBox.critical(parent, "Error", f"File not found: {file_path}")
    except json.JSONDecodeError:
        QMessageBox.critical(parent, "Error", f"Invalid JSON in file: {file_path}")
    return []
