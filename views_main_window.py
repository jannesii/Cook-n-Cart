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



        self.ostolistat_page = None
        self.reseptit_page = None
        self.products_page = None
        self.asetukset_page = None

        main_layout.addWidget(self.stacked_widget, stretch=1)

        # --- Alapalkin layout ---
        bottom_bar_layout = QHBoxLayout()

        self.btn_ostolistat = QPushButton("Ostolistat")
        self.btn_reseptit = QPushButton("Reseptit")
        self.btn_tuotteet = QPushButton("Tuotteet")
        self.btn_asetukset = QPushButton("Asetukset")

        # Kytketään napit vaihtamaan QStackedWidgetin sivua

        self.btn_ostolistat.clicked.connect(
            lambda checked: self.open_ostolistat())
        self.btn_reseptit.clicked.connect(
            lambda checked: self.open_reseptit())
        self.btn_tuotteet.clicked.connect(
            lambda checked: self.open_tuotteet())
        self.btn_asetukset.clicked.connect(
            lambda checked: self.open_asetukset())

        # Voit halutessasi säätää alapalkin tyylin
        for btn in [self.btn_ostolistat, self.btn_reseptit, self.btn_tuotteet, self.btn_asetukset]:
            btn.setObjectName("gray_button")

        bottom_bar_layout.addWidget(self.btn_ostolistat)
        bottom_bar_layout.addWidget(self.btn_reseptit)
        bottom_bar_layout.addWidget(self.btn_tuotteet)
        bottom_bar_layout.addWidget(self.btn_asetukset)

        main_layout.addLayout(bottom_bar_layout)

        # Asetetaan oletussivuksi Ostolistat (index 0)
        self.open_ostolistat()

    def open_ostolistat(self):
        #self.clearMemory()
        self.ostolistat_page = OstolistatPage()
        self.stacked_widget.addWidget(self.ostolistat_page)  # index 0
        self.stacked_widget.setCurrentWidget(self.ostolistat_page)

    def open_reseptit(self):
        #self.clearMemory()
        self.reseptit_page = ReseptitPage()
        self.stacked_widget.addWidget(self.reseptit_page)    # index 1
        self.stacked_widget.setCurrentWidget(self.reseptit_page)

    def open_tuotteet(self):
        #self.clearMemory()
        self.products_page = TuotteetPage()
        self.stacked_widget.addWidget(self.products_page)    # index 2
        self.stacked_widget.setCurrentWidget(self.products_page)

    def open_asetukset(self):
        #self.clearMemory()
        self.asetukset_page = AsetuksetPage()
        self.stacked_widget.addWidget(self.asetukset_page)   # index 3
        self.stacked_widget.setCurrentWidget(self.asetukset_page)

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
            
            
            