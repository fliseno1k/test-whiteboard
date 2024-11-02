import sys
from PySide6.QtWidgets import QApplication
from widgets.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
