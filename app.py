# app.py
import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow

def load_stylesheet(app, path=r"utils\\styles.qss"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            qss = f.read()
        # Replace placeholder tokens with actual values.
        qss = qss.replace("%%TURKOOSI%%", "#00B0F0")
        qss = qss.replace("%%TURKOOSI_HOVER%%", "#009ACD")
        qss = qss.replace("%%HARMAA%%", "#808080")
        qss = qss.replace("%%HARMAA_HOVER%%", "#535353")
        app.setStyleSheet(qss)
    except Exception as e:
        print(f"Unable to load stylesheet: {e}")

def main():
    app = QApplication(sys.argv)
    load_stylesheet(app, r"utils\\styles.qss")  # Jos tiedosto sijaitsee utils-kansiossa
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
