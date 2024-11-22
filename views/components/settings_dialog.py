from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 150)

        # Layout
        layout = QVBoxLayout(self)

        # Theme selection
        theme_label = QLabel("Choose Theme:", self)
        self.theme_combo_box = QComboBox(self)
        self.theme_combo_box.addItems(["Light", "Dark"])
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo_box)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_selected_theme(self):
        """Returns the selected theme."""
        return self.theme_combo_box.currentText()
