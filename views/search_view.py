from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget,
    QMessageBox, QMenuBar, QAction, QCompleter, QDialog
)
from PyQt5.QtCore import Qt
from views.components import CheckableComboBox, ProgressIndicator, SettingsDialog
from data.data import load_data
from utils.dialogs import show_error_dialog
from utils.search import search_json
import re


class SearchApp(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Fitgirl Offline and Better")
        self.resize(800, 600)

        # Load data
        try:
            self.data = load_data("data/data.json")
        except (FileNotFoundError, ValueError) as e:
            show_error_dialog(self, "Data Error", str(e))
            exit()

        self.genres = sorted(set(genre for item in self.data for genre in item.get("genre", [])))

        # UI Elements
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Enter search query (supports regex)")

        self.search_button = QPushButton("Search", self)
        self.result_list = QListWidget(self)
        self.genre_combobox = CheckableComboBox(self)

        for genre in self.genres:
            self.genre_combobox.add_item(genre)

        self.progress = ProgressIndicator(parent=self)

        # Autocomplete setup
        self.autocomplete = QCompleter([item["title"] for item in self.data], self)
        self.autocomplete.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_box.setCompleter(self.autocomplete)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_box)
        layout.addWidget(self.genre_combobox)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_list)
        self.setLayout(layout)

        # Menu
        self.menu_bar = QMenuBar(self)
        layout.setMenuBar(self.menu_bar)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.menu_bar.addAction(settings_action)

        # Signals
        self.search_button.clicked.connect(self.start_search)
        self.result_list.itemDoubleClicked.connect(self.show_details)

    def update_autocomplete(self):
        """Update autocomplete suggestions based on loaded data."""
        titles = [item["title"] for item in self.data]
        self.autocomplete.model().setStringList(titles)  # Fixed: Ensure the model is initialized correctly

    def start_search(self):
        """Start the search operation."""
        query = self.search_box.text()
        selected_genres = self.genre_combobox.get_checked_items()

        if not query.strip() and not selected_genres:
            show_error_dialog(self, "Search Error", "Please enter a query or select genres.")
            return

        self.progress.start()
        try:
            results = search_json(self.data, query, selected_genres)
        except re.error as e:
            self.progress.stop()
            show_error_dialog(self, "Regex Error", f"Invalid regular expression: {str(e)}")
            return

        self.progress.stop()

        self.result_list.clear()
        if not results:
            QMessageBox.information(self, "No Results", "No results found.")
            return

        for result in results:
            self.result_list.addItem(result["title"])

    def show_details(self, item):
        title = item.text()
        for entry in self.data:
            if entry["title"] == title:
                download_links = ", ".join(entry.get("download_links", []))  # Safely handle missing download links

                # Prepare the details message
                details_message = (
                    f"Title: {entry['title']}\n"
                    f"Date: {entry['date']}\n"
                    f"Genres: {', '.join(entry['genre'])}\n"
                )

                if download_links:
                    details_message += f"Download Links: {download_links}\n"  # Add download links to message
                else:
                    details_message += "Download Links: None available\n"  # Show message if no links are present

                # Display the details in a message box
                QMessageBox.information(self, "Details", details_message)
                break


    def open_settings(self):
        """Open the settings dialog."""
        dialog = SettingsDialog(app=self.app, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            theme = dialog.theme_combo_box.currentText()
            if theme == "Dark":
                self.app.setStyleSheet(open('styles/dark.qss', 'r').read())
            else:
                self.app.setStyleSheet(open('styles/light.qss', 'r').read())

