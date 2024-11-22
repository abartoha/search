from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class ProgressIndicator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processing...")
        self.setModal(True)
        self.setFixedSize(300, 100)

        # Layout
        layout = QVBoxLayout(self)
        self.label = QLabel("Please wait...", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Indeterminate mode

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

    def start(self):
        self.show()

    def stop(self):
        self.hide()
