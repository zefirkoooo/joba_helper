from PyQt6.QtWidgets import QApplication
from GUI.main_gui import SimpleApp
import sys

app = QApplication(sys.argv)
window = SimpleApp()
window.show()
sys.exit(app.exec())
