from PyQt5.QtWidgets import QMessageBox

def show_error_dialog(parent, title, message):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()
