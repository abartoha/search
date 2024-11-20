import json
from fuzzywuzzy import fuzz
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QVBoxLayout

def search_json(data, query):
    results = []
    for item in data:
        for key, value in item.items():
            if isinstance(value, str):
                if fuzz.ratio(query.lower(), value.lower()) >= 70:  # Adjust threshold as needed
                    results.append(item)
                    break
            elif isinstance(value, dict):
                sub_results = search_json(value, query)
                if sub_results:
                    results.extend(sub_results)
    return results

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        # Load JSON data
        with open('data.json', 'r', encoding="utf-8") as f:
            self.data = json.load(f)

        # Create UI elements
        self.search_box = QLineEdit()
        self.search_button = QPushButton("Search")
        self.result_list = QListWidget()

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
            self.result_list.addItem(str(result))

if __name__ == '__main__':
    app = QApplication([])
    window = SearchApp()
    window.show()
    app.exec_()