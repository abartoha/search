from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


class SettingsDialog(QDialog):
    def __init__(self, app=None, parent=None):
        super().__init__(parent)
        self.app = app  # Store the app reference if needed
        self.setWindowTitle("Settings")

        # Layout
        layout = QVBoxLayout(self)

        # Theme Selection
        theme_label = QLabel("Choose Theme:", self)
        self.theme_combo_box = QComboBox(self)
        self.theme_combo_box.addItems(["Light", "Dark"])  # Add themes to the combobox

        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo_box)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
