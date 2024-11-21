import json
from fuzzywuzzy import fuzz
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QListWidget, QVBoxLayout, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtWidgets

def search_json(data, query, selected_genres):
    results = []
    for item in data:
        if (
            fuzz.partial_ratio(query.lower(), item['title'].lower()) >= 70
            or any(fuzz.partial_ratio(query.lower(), tag.lower()) >= 70 for tag in item['genre'])
        ):
            if all(genre in item['genre'] for genre in selected_genres):
                results.append(item)
    return results

class CheckableComboBox(QtWidgets.QComboBox):
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
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def get_checked_items(self):
        checked_items = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.Checked:
                checked_items.append(item.text())
        return checked_items

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search App")
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

        # Extract unique genres from the data
        self.genres = sorted(set(genre for item in self.data for genre in item['genre']))

        # Create UI elements
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter search query")
        self.search_button = QPushButton("Search")
        self.result_list = QListWidget()

        # Create genre filter combobox
        self.genre_combobox = CheckableComboBox()
        self.genre_combobox.addItem("All Genres")  # Default item
        for genre in self.genres:
            self.genre_combobox.add_item(genre)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.genre_combobox)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_list)
        self.setLayout(layout)

        # Connect signals
        self.search_button.clicked.connect(self.search)
        self.result_list.itemDoubleClicked.connect(self.show_details)

    def search(self):
        query = self.search_box.text()
        selected_genres = self.genre_combobox.get_checked_items()

        if "All Genres" in selected_genres:
            selected_genres = []  # Ignore genre filtering if "All Genres" is selected

        results = search_json(self.data, query, selected_genres)
        self.result_list.clear()

        for result in results:
            item = QListWidgetItem(result['title'])
            self.result_list.addItem(item)

    def show_details(self):
        selected_item = self.result_list.currentItem()
        if selected_item:
            item_text = selected_item.text()
            for result in self.data:
                if result['title'] == item_text:
                    QMessageBox.information(
                        self, "Details", 
                        f"Title: {result['title']}\n"
                        f"Date: {result['date']}\n"
                        f"Download Links: {', '.join(result['download_links'])}\n"
                        f"Genres: {', '.join(result['genre'])}\n"
                        f"Features: {', '.join(result['features'])}"
                    )
                    break

if __name__ == '__main__':
    app = QApplication([])
    window = SearchApp()
    window.show()
    app.exec_()
