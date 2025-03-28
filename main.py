import sys
import os
from PySide6.QtWidgets import QApplication
from views_main_window import MainWindow

def load_stylesheet(app, qss):
    print("Loading stylesheet...")
    try:
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
    
    # Check if the 'utils' directory exists, create if it doesn't.
    
    utils_dir = "utils"
    
    if not os.path.exists(utils_dir):
        print("Creating utils dir.")
        os.makedirs(utils_dir)
    
    # Check if the config file exists, and create it if missing.
    config_path = os.path.join(utils_dir, "config.json")
    
    if not os.path.exists(config_path):
        print("Creating config.json")
        default_config = '''{
            "settings": {
                "currency": "\\u20ac",
                "weight_unit": "kg",
                "volume_unit": "l"
            }
        }'''
        try:
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write(default_config)
        except Exception as e:
            print(f"Unable to write config file: {e}")
    
    default_styles = """
        /* style.qss */

        /* General settings for all widgets */
        QWidget {
            background-color: #f0f0f0;
            font-family: "Segoe UI", sans-serif;
        }

        QLineEdit, QListWidget {
            color: black;
        }

        QListView::indicator:unchecked {
            border: 1px solid #808080;
            border-radius: 4px;
        }

        /* Uniform style for buttons */
        QPushButton {
            background-color: %%TURKOOSI%%;
            color: black;
            font-weight: bold;
            border: none;
            padding: 8px;
            border-radius: 5px;
        }

        QPushButton:hover {
            background-color: %%TURKOOSI_HOVER%%;
        }

        QPushButton:pressed {
            background-color: #707070;
        }

        QPushButton#main_list_button {
            background-color: %%TURKOOSI%%;
            color: black;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
            text-align: left;
        }

        QPushButton:hover#main_list_button {
            background-color: #009ACD;
        }

        QPushButton:pressed#main_list_button {
            background-color: #707070;
        }

        QPushButton#gray_button {
            background-color: %%HARMAA%%;
            color: black;
            font-weight: bold;
            border: none;
            padding: 8px;
            border-radius: 5px;
        }

        QPushButton:hover#gray_button {
            background-color: %%HARMAA_HOVER%%;
        }

        QPushButton:pressed#gray_button {
            background-color: %%TURKOOSI%%;
        }

        QPushButton#delete_button {
            background-color: red;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px;
        }

        QPushButton:hover#delete_button {
            background-color: crimson;
        }

        QPushButton:pressed#delete_button {
            background-color: darkred;
        }

        /* Example label style */
        QLabel {
            color: #333333;
            font-size: 16px;
        }

        QLabel#top_bar_title_label {
            color: #333333;
            background-color: %%HARMAA%%;
            font-weight: bold;
            font-size: 18px;
        }

        QLineEdit#top_bar_search_bar {
            background-color: %%TURKOOSI%%;
            color: black;
            font-weight: bold;
            border-radius: 5px;
            padding: 8px;
        }

        QFrame#top_bar_frame {
            background-color: %%HARMAA%%;
            border-radius: 10px;
        }

        QFrame#asetukset_frame {
            background-color: %%TURKOOSI%%;
            border-radius: 10px;
        }

        QLabel#asetukset_label {
            background-color: %%TURKOOSI%%;
            color: black;
            font-size: 16px;
            font-weight: bold;
        }

        QComboBox#asetukset_combobox {
            color: black;
            font-size: 14px;
            font-weight: bold;
            padding: 2px;
            border-radius: 5px;
        }

        QComboBox#asetukset_combobox QAbstractItemView {
            color: black;
        }

        .warningLabel {
            color: red;
            font-weight: bold;
        }
    """
    load_stylesheet(app, default_styles)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
