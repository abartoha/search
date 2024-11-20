import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget
from elasticsearch import Elasticsearch

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()

        # Connect to Elasticsearch
        self.es = Elasticsearch()

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
        res = self.es.search(index="your_index_name", q=query)

        self.result_list.clear()
        for hit in res['hits']['hits']:
            self.result_list.addItem(hit['_source']['title'])  # Assuming 'title' is a field in your JSON data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())