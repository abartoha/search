import json
from fuzzywuzzy import fuzz
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QSizePolicy

def search_json(data, query):
    results = []
    for item in data:
        if fuzz.partial_ratio(query.lower(), item['title'].lower()) >= 70:
            results.append(item)
    return results

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        # Load JSON data
        try:
            with open('data.json', 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("Error: data.json not found.")
            exit()
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in data.json.")
            exit()

        # Create UI elements
        self.search_box = QLineEdit()
        self.search_button = QPushButton("Search")
        self.result_list = QListWidget()

        # Set initial window size and minimum size
        self.setFixedSize(600, 400)
        self.setMinimumSize(600, 400)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_list)
        self.setLayout(layout)

        # Connect button click to search function
        self.search_button.clicked.connect(self.search)

    def search(self):
        query = self.search_box.text()
        results = search_json(self.data, query)

        self.result_list.clear()
        for result in results:
            self.result_list.addItem(result['title'])

if __name__ == '__main__':
    app = QApplication([])
    window = SearchApp()
    window.show()
    app.exec_()