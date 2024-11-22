import sys
from PyQt5.QtWidgets import QApplication
from views.search_view import SearchApp
from PyQt5.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    app.setStyleSheet(open("styles/dark.qss", "r").read())
    window = SearchApp(app)
    window.show()
    sys.exit(app.exec_())
