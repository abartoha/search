from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QComboBox

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.view().pressed.connect(self.handle_item_pressed)

    def add_item(self, text):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Unchecked)
        self.model().appendRow(item)

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        item.setCheckState(Qt.Checked if item.checkState() == Qt.Unchecked else Qt.Unchecked)

    def get_checked_items(self):
        return [self.model().item(i).text() for i in range(self.model().rowCount())
                if self.model().item(i).checkState() == Qt.Checked]