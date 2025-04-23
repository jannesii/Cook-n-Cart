# File: views_asetukset_page.py --------------------------------------------------------------------

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt

from root_controllers import ProductController as PC
from root_controllers import ShoppingListController as SLC
from root_controllers import RecipeController as RC
from root_controllers import ErrorController
from error_handler import catch_errors_ui
from qml import ScrollableLabel

TURKOOSI = "#00B0F0"
HARMAA = "#808080"
CONFIG_FILE = "cookncart/utils/config.json"

# Create controller instances.
RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()


class AsetuksetPage(QWidget):
    """
    Asetukset-sivu:
      - Yläpalkki: "Asetukset" -otsikko
      - Keskialue: Käyttää QStackedWidget:iä mahdollistamaan
        useiden widget-sivujen lisäämisen, esimerkkinä ensimmäinen sivu sisältää
        "Lue virheloki" -napin.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.error_controller = ErrorController()

        self.error_log = None
        self.update_error_log()  # Now references the class method

        # Main layout for the page.
        main_layout = QVBoxLayout(self)
        self.error_log_page = None

        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Asetukset")
        label.setObjectName("top_bar_title_label")
        self.back_button = QPushButton("Takaisin")
        self.back_button.setObjectName("top_bar_new_button")
        self.back_button.clicked.connect(self.display_main_page)

        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.back_button)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")
        top_bar_frame.setFixedHeight(50)
        main_layout.addWidget(top_bar_frame, 0)

        # -- Keskialue: Stacked Widget Setup --
        self.stacked_widget = QStackedWidget()

        # Create the initial page with the "Lue virheloki" button.
        self.initial_page = QWidget()
        initial_layout = QVBoxLayout(self.initial_page)
        read_error_log_button = QPushButton("Lue virheloki")
        read_error_log_button.setObjectName("main_list_button")
        read_error_log_button.clicked.connect(self.display_error_log)
        initial_layout.addWidget(read_error_log_button)
        initial_layout.addStretch()  # Adds spacing if desired.

        self.stacked_widget.addWidget(self.initial_page)
        main_layout.addWidget(self.stacked_widget, 1)
        self.display_main_page()

    @catch_errors_ui
    def update_error_log(self):
        """
        Update the instance's error_log attribute by retrieving error logs as a single string.
        """
        self.error_log = self.error_controller.get_all_error_logs_as_one_string(
            sort_order="ASC")

    @catch_errors_ui
    def init_error_log(self):
        """
        Initialize a layout containing a scrollable error log label.
        """
        layout = QVBoxLayout()
        error_log_label = ScrollableLabel(
            parent=self, placeholder_text="Ei virhelokiviestejä.")

        self.update_error_log()
        error_log_label.set_text(self.error_log)

        layout.addWidget(error_log_label)

        return layout

    @catch_errors_ui
    def display_error_log(self):
        """
        Display the error log in the stacked widget.
        """
        self.window().hide_buttons()

        self.error_log_page = QWidget()
        self.back_button.show()
        self.error_log_page.setLayout(self.init_error_log())

        self.stacked_widget.addWidget(self.error_log_page)
        self.stacked_widget.setCurrentWidget(self.error_log_page)

    @catch_errors_ui
    def display_main_page(self):
        """
        Return to the main page of the application.
        """
        self.window().show_buttons()

        self.back_button.hide()
        self.stacked_widget.setCurrentWidget(self.initial_page)

        if self.error_log_page is not None:
            self.stacked_widget.removeWidget(self.error_log_page)
            self.error_log_page.deleteLater()
            self.error_log_page = None
