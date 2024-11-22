import sys
from PyQt5.QtWidgets import QApplication
from views.search_view import SearchApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles/light.qss", "r").read())
    window = SearchApp(app)
    window.show()
    sys.exit(app.exec_())
