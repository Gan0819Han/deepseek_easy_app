import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import DeepseekWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DeepseekWindow()
    window.show()
    sys.exit(app.exec_())