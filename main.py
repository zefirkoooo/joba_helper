import sys
from PyQt6.QtWidgets import QApplication
from GUI.main_gui import SimpleApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())