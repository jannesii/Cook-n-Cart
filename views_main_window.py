# main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QStackedWidget
)
from views_ostoslistat_page import OstolistatPage
from views_reseptit_page import ReseptitPage
from views_tuotteet_page import TuotteetPage
from views_asetukset_page import AsetuksetPage


TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cook and Cart")
        self.setMinimumSize(400, 600)

        # Pääwidget QMainWindowille
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Päälayout (pystysuunta): yläosassa sivut (QStackedWidget), alaosassa navigointipalkki
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- QStackedWidget - sivut ---
        self.stacked_widget = QStackedWidget()

        self.ostolistat_page = OstolistatPage()
        self.reseptit_page = ReseptitPage()
        self.products_page = TuotteetPage()
        self.asetukset_page = AsetuksetPage()

        self.stacked_widget.addWidget(self.ostolistat_page)  # index 0
        self.stacked_widget.addWidget(self.reseptit_page)    # index 1
        self.stacked_widget.addWidget(self.products_page)    # index 2
        self.stacked_widget.addWidget(self.asetukset_page)   # index 3

        main_layout.addWidget(self.stacked_widget, stretch=1)

        # --- Alapalkin layout ---
        bottom_bar_layout = QHBoxLayout()

        self.btn_ostolistat = QPushButton("Ostolistat")
        self.btn_reseptit = QPushButton("Reseptit")
        self.btn_tuotteet = QPushButton("Tuotteet")
        self.btn_asetukset = QPushButton("Asetukset")

        # Kytketään napit vaihtamaan QStackedWidgetin sivua
        self.btn_ostolistat.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(0))
        self.btn_reseptit.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(1))
        self.btn_tuotteet.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(2))
        self.btn_asetukset.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(3))

        # Voit halutessasi säätää alapalkin tyylin
        for btn in [self.btn_ostolistat, self.btn_reseptit, self.btn_tuotteet, self.btn_asetukset]:
            btn.setObjectName("gray_button")

        bottom_bar_layout.addWidget(self.btn_ostolistat)
        bottom_bar_layout.addWidget(self.btn_reseptit)
        bottom_bar_layout.addWidget(self.btn_tuotteet)
        bottom_bar_layout.addWidget(self.btn_asetukset)

        main_layout.addLayout(bottom_bar_layout)

        # Asetetaan oletussivuksi Ostolistat (index 0)
        self.stacked_widget.setCurrentIndex(0)
