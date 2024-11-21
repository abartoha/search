import json
from fuzzywuzzy import fuzz
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QSizePolicy, QMessageBox
THRES = 90
def search_json(data, query):
    results = []
    for item in data:
        if fuzz.partial_ratio(query.lower(), item['title'].lower()) >= THRES or \
           any(fuzz.partial_ratio(query.lower(), tag.lower()) >= THRES for tag in item['genre']):
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
        self.result_list.itemDoubleClicked.connect(self.show_details)

    def search(self):
        query = self.search_box.text()
        results = search_json(self.data, query)

        self.result_list.clear()
        for result in results:
            self.result_list.addItem(result['title'])

    def show_details(self):
        selected_item = self.result_list.currentItem()
        if selected_item:
            item_text = selected_item.text()
            for result in self.data:
                infos = ""
                for text in result['features']:
                    infos += text + "\n"
                if result['title'] == item_text:
                    # Display details in a message box
                    QMessageBox.information(self, "Details", f"Title: {result['title']}\n"
                                                                 f"Release Date: {result['date']}\n"
                                                                 f"Release Date: {result['genre']}\n"
                                                                 f"Download Links: {infos}\n"
                                                                 # Add other fields as needed
                                                                 )
                    break

if __name__ == '__main__':
    app = QApplication([])
    window = SearchApp()
    window.show()
    app.exec_()