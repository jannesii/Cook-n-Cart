# main_window.py

import functools
import logging
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt

from views_ostoslistat_page import OstolistatPage
from views_reseptit_page import ReseptitPage
from views_tuotteet_page import TuotteetPage
from views_asetukset_page import AsetuksetPage
from error_handler import catch_errors_ui

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Cook and Cart")
        self.setMinimumSize(400, 600)

        # Main widget for the QMainWindow.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout: a QStackedWidget for pages and a bottom navigation bar.
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # QStackedWidget for the pages.
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, stretch=1)

        # Bottom navigation bar.
        bottom_bar_layout = QHBoxLayout()

        self.btn_ostolistat = QPushButton("Ostolistat")
        self.btn_reseptit = QPushButton("Reseptit")
        self.btn_tuotteet = QPushButton("Tuotteet")
        self.btn_asetukset = QPushButton("Asetukset")

        # Connect buttons to methods (wrapped with error handling).
        self.btn_ostolistat.clicked.connect(
            lambda checked: self.open_ostolistat())
        self.btn_reseptit.clicked.connect(lambda checked: self.open_reseptit())
        self.btn_tuotteet.clicked.connect(lambda checked: self.open_tuotteet())
        self.btn_asetukset.clicked.connect(
            lambda checked: self.open_asetukset())

        # Set style names.
        for btn in [self.btn_ostolistat, self.btn_reseptit, self.btn_tuotteet, self.btn_asetukset]:
            btn.setObjectName("gray_button")

        bottom_bar_layout.addWidget(self.btn_ostolistat)
        bottom_bar_layout.addWidget(self.btn_reseptit)
        bottom_bar_layout.addWidget(self.btn_tuotteet)
        bottom_bar_layout.addWidget(self.btn_asetukset)
        main_layout.addLayout(bottom_bar_layout)

        # Set default page.
        self.open_ostolistat()

    @catch_errors_ui
    def hide_buttons(self):
        """Hide the navigation bar buttons."""
        self.btn_ostolistat.hide()
        self.btn_reseptit.hide()
        self.btn_tuotteet.hide()
        self.btn_asetukset.hide()

    @catch_errors_ui
    def show_buttons(self):
        """Show the navigation bar buttons."""
        self.btn_ostolistat.show()
        self.btn_reseptit.show()
        self.btn_tuotteet.show()
        self.btn_asetukset.show()

    @catch_errors_ui
    def open_ostolistat(self):
        self.ostolistat_page = OstolistatPage(parent=self)
        self.stacked_widget.addWidget(self.ostolistat_page)  # index 0
        self.stacked_widget.setCurrentWidget(self.ostolistat_page)

    @catch_errors_ui
    def open_reseptit(self):
        self.reseptit_page = ReseptitPage(parent=self)
        self.stacked_widget.addWidget(self.reseptit_page)    # index 1
        self.stacked_widget.setCurrentWidget(self.reseptit_page)

    @catch_errors_ui
    def open_tuotteet(self):
        self.products_page = TuotteetPage(parent=self)
        self.stacked_widget.addWidget(self.products_page)    # index 2
        self.stacked_widget.setCurrentWidget(self.products_page)

    @catch_errors_ui
    def open_asetukset(self):
        self.asetukset_page = AsetuksetPage(parent=self)
        self.stacked_widget.addWidget(self.asetukset_page)   # index 3
        self.stacked_widget.setCurrentWidget(self.asetukset_page)

    @catch_errors_ui
    def clearMemory(self):
        if self.ostolistat_page:
            print("Removing ostolistat_page")
            self.stacked_widget.removeWidget(self.ostolistat_page)
            self.ostolistat_page.deleteLater()
            del self.ostolistat_page
            self.ostolistat_page = None
        if self.reseptit_page:
            print("Removing reseptit_page")
            self.stacked_widget.removeWidget(self.reseptit_page)
            self.reseptit_page.deleteLater()
            del self.reseptit_page
            self.reseptit_page = None
        if self.products_page:
            print("Removing products_page")
            self.stacked_widget.removeWidget(self.products_page)
            self.products_page.deleteLater()
            del self.products_page
            self.products_page = None
        if self.asetukset_page:
            print("Removing asetukset_page")
            self.stacked_widget.removeWidget(self.asetukset_page)
            self.asetukset_page.deleteLater()
            del self.asetukset_page
            self.asetukset_page = None
    
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Back, Qt.Key_Escape):
            # Tell Qt to “ignore” this, so it does NOT trigger the exit toast
            event.ignore()
            print("Back or Escape key pressed, ignoring event.")
            return
        # Otherwise, proceed with normal behavior
        print("Key pressed:", event.key())
        super().keyPressEvent(event)

