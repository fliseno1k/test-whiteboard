import sys
import signal
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow


def handle_sigterm(signum, frame):
    QApplication.quit()


signal.signal(signal.SIGINT, handle_sigterm)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        QApplication.quit()


if __name__ == "__main__":
    main()
