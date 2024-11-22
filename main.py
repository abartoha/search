import json
import re
from fuzzywuzzy import fuzz
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,
    QListWidget, QVBoxLayout, QMessageBox, QListWidgetItem,
    QDialog, QComboBox, QDialogButtonBox, QLabel, QMenuBar, QMenu,
    QProgressDialog, QCompleter
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QIcon


def search_json(data, query, selected_genres, use_regex=False):
    """Search JSON data with support for regex and genre filtering."""
    results = []
    try:
        for item in data:
            title_match = False

            # Regular expression search
            if use_regex:
                try:
                    if re.search(query, item['title'], re.IGNORECASE):
                        title_match = True
                except re.error:
                    raise ValueError("Invalid regular expression.")
            # Fuzzy matching
            elif fuzz.partial_ratio(query.lower(), item['title'].lower()) >= 70:
                title_match = True

            # Apply genre filtering
            if title_match and all(genre in item['genre'] for genre in selected_genres):
                results.append(item)
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred during the search: {e}")
    return results


class CheckableComboBox(QtWidgets.QComboBox):
    """Custom ComboBox with checkable items for multi-selection."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QtGui.QStandardItemModel(self))
        self.view().pressed.connect(self.handle_item_pressed)

    def add_item(self, text):
        item = QtGui.QStandardItem(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Unchecked)
        self.model().appendRow(item)

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)

    def get_checked_items(self):
        return [
            self.model().item(i).text()
            for i in range(self.model().rowCount())
            if self.model().item(i).checkState() == Qt.Checked
        ]


class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Search App")
        self.resize(600, 400)

        # Load JSON data
        try:
            with open('data.json', 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "data.json not found.")
            exit()
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Invalid JSON data in data.json.")
            exit()

        # Extract unique genres and titles for autocomplete
        self.genres = sorted(set(genre for item in self.data for genre in item['genre']))
        self.titles = [item['title'] for item in self.data]

        # UI elements
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter search query")
        self.search_button = QPushButton("Search")
        self.result_list = QListWidget()

        # Autocomplete for search box
        completer = QCompleter(self.titles, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_box.setCompleter(completer)

        # Genre filter combobox
        self.genre_combobox = CheckableComboBox()
        self.genre_combobox.add_item("All Genres")
        for genre in self.genres:
            self.genre_combobox.add_item(genre)

        # Regex checkbox
        self.use_regex_checkbox = QtWidgets.QCheckBox("Use Regular Expression")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.genre_combobox)
        layout.addWidget(self.use_regex_checkbox)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_list)
        self.setLayout(layout)

        # Connect signals
        self.search_button.clicked.connect(self.search)
        self.result_list.itemDoubleClicked.connect(self.show_details)

    def search(self):
        query = self.search_box.text()
        selected_genres = self.genre_combobox.get_checked_items()
        use_regex = self.use_regex_checkbox.isChecked()

        if "All Genres" in selected_genres:
            selected_genres = []

        # Progress dialog
        progress_dialog = QProgressDialog("Searching...", "Cancel", 0, 0, self)
        progress_dialog.setWindowTitle("Please Wait")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Perform search
        results = search_json(self.data, query, selected_genres, use_regex)

        progress_dialog.close()

        # Display results
        self.result_list.clear()
        if results:
            for result in results:
                self.result_list.addItem(QListWidgetItem(result['title']))
        else:
            QMessageBox.information(self, "No Results", "No results found for your query.")

    def show_details(self):
        selected_item = self.result_list.currentItem()
        if selected_item:
            item_text = selected_item.text()
            for result in self.data:
                if result['title'] == item_text:
                    QMessageBox.information(
                        self, "Details",
                        f"Title: {result['title']}\n"
                        f"Date: {result.get('date', 'N/A')}\n"
                        f"Genres: {', '.join(result['genre'])}\n"
                        f"Features: {', '.join(result.get('features', []))}"
                    )
                    break


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.ico'))
    window = SearchApp()
    window.show()
    app.exec_()
