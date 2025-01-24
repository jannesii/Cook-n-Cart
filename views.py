import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QComboBox, QFrame
)
from PySide6.QtCore import Qt
import controllers
import models
from typing import Dict

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

class OstolistatPage(QWidget):
    """
    Ostolistat-sivu:
      - Yläpalkki: "Ostoslistat" -otsikko vasemmalla, "Uusi ostolista" -nappi oikealla
      - Keskialue: esim. "Ruokaostokset 0/16", "Motonet 0/5", "Biltema 0/11" -napit
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Ostoslistat")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        # Esimerkin "Uusi ostolista" -nappi
        new_list_btn = QPushButton("Uusi ostolista")
        new_list_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }}
        """)
        
        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(new_list_btn)
        
        # Värjätään yläpalkin tausta harmaaksi asettamalla QFrame
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(f"background-color: {HARMAA};")
        
        main_layout.addWidget(top_bar_frame, 0)  # yläpalkki
        
        # -- Scrollattava keskialue, jos listoja on paljon --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Esimerkkilistat
        shopping_lists = [
            "Ruokaostokset \n0/16",
            "Motonet \n0/5",
            "Biltema \n0/11"
        ]
        
        for item in shopping_lists:
            btn = QPushButton(item)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left; /* Teksti vasemmalle */
                }}
            """)
            scroll_layout.addWidget(btn)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area, 1)


class ReseptitPage(QWidget):
    """
    Reseptit-sivu:
      - Yläpalkki: "Reseptit" -otsikko vasemmalla, "Hae reseptejä" ja "Uusi resepti" -napit oikealla
      - Keskialue: isoja nappeja, esim. "Karjalanpaisti", "Pasta bolognese", "Tikka masala"
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        
        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Reseptit")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        search_btn = QPushButton("Hae reseptejä")
        new_btn = QPushButton("Uusi resepti")
        
        # Voit halutessasi säätää esim. samaa tyyliä kuin ostolistasivulla
        search_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }}
        """)
        
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }}
        """)
        
        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(search_btn)
        top_bar_layout.addWidget(new_btn)
        
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(f"background-color: {HARMAA};")
        
        main_layout.addWidget(top_bar_frame, 0)
        
        # -- Scrollattava keskialue (reseptien lista) --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        recipes = [
            "Karjalanpaisti",
            "Pasta bolognese",
            "Tikka masala"
        ]
        
        for recipe in recipes:
            btn = QPushButton(recipe)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }}
            """)
            scroll_layout.addWidget(btn)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area, 1)


class ProductsPage(QWidget):
    """
    Tuotteet-näkymä:
      - Yläpalkki: 'Tuotteet' -otsikko vasemmalla, 'Hae tuotetta' ja 'Uusi tuote' -napit oikealla
      - Keskialue: Scrollattava lista tuotteista
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        
        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        
        self.title_label = QLabel("Tuotteet")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        self.search_button = QPushButton("Hae tuotetta")
        self.new_button = QPushButton("Uusi tuote")
        
        self.search_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }}
        """)
        self.new_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }}
        """)
        
        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_button)
        top_bar_layout.addWidget(self.new_button)
        
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(f"background-color: {HARMAA};")
        
        main_layout.addWidget(top_bar_frame, 0)
        
        # -- Scrollattava lista keskellä --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        
        
        products = self.get_product_dict()
        
        for product in products:
            btn = QPushButton(product)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }}
            """)
            scroll_layout.addWidget(btn)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area, 1)

        ## Tuotteiden haku databasesta.
    def get_product_dict(self):
        tuotteet = controllers.ProductController().get_all_products()
        # Create a dictionary with id as the key
        self.products_dict: Dict[int, models.Product] = {product.id: product for product in tuotteet}
        return self.products_dict


class AsetuksetPage(QWidget):
    """
    Asetukset-sivu:
      - Yläpalkki: "Asetukset" -otsikko
      - Keskialue: 2 "nappiriviä" (tai kehyksiä), joihin on sijoitettu Label + ComboBox:
          1) "Valuutta" - '€'
          2) "Painon yksikkö" - 'kg/l'
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        
        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Asetukset")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")
        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(f"background-color: {HARMAA};")
        
        main_layout.addWidget(top_bar_frame, 0)
        
        # -- Keskialue --
        # Tehdään kaksi "riviä", joissa vasemmalla label ja oikealla ComboBox,
        # ja koko rivi on kehystetty kuin nappi (pyöristetty, turkoosi).
        
        # 1) Valuutta
        currency_frame = QFrame()
        currency_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TURKOOSI};
                border-radius: 10px;
            }}
        """)
        currency_layout = QHBoxLayout(currency_frame)
        
        currency_label = QLabel("Valuutta")
        currency_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        
        self.currency_combo = QComboBox()
        # Täytetään muutama valuutta esimerkin vuoksi
        self.currency_combo.addItems(["€", "$", "£", "¥"])
        self.currency_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                padding: 2px;
            }
        """)
        
        currency_layout.addWidget(currency_label)
        currency_layout.addStretch()
        currency_layout.addWidget(self.currency_combo)
        
        # 2) Painon yksikkö
        weight_frame = QFrame()
        weight_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TURKOOSI};
                border-radius: 10px;
            }}
        """)
        weight_layout = QHBoxLayout(weight_frame)
        
        weight_label = QLabel("Painon yksikkö")
        weight_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        
        self.weight_combo = QComboBox()
        self.weight_combo.addItems(["kg/l", "lb", "oz"])
        self.weight_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                padding: 2px;
            }
        """)
        
        weight_layout.addWidget(weight_label)
        weight_layout.addStretch()
        weight_layout.addWidget(self.weight_combo)
        
        # Lisätään kehykset pystylayoutiin
        content_layout = QVBoxLayout()
        content_layout.addWidget(currency_frame)
        content_layout.addWidget(weight_frame)
        content_layout.addStretch()
        
        main_layout.addLayout(content_layout, 1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Esimerkkisovellus")
        self.setMinimumSize(400, 600)

        # Pääwidget QMainWindowille
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Päälayout (pystysuunta): yläosassa sivut (QStackedWidget), alaosassa navigointipalkki
        main_layout = QVBoxLayout(central_widget)

        # --- QStackedWidget - sivut ---
        self.stacked_widget = QStackedWidget()
        
        self.ostolistat_page = OstolistatPage()
        self.reseptit_page = ReseptitPage()
        self.products_page = ProductsPage()
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
        self.btn_ostolistat.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_reseptit.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_tuotteet.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_asetukset.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        # Voit halutessasi säätää alapalkin tyylin
        for btn in [self.btn_ostolistat, self.btn_reseptit, self.btn_tuotteet, self.btn_asetukset]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {HARMAA};
                    color: black;
                    font-weight: bold;
                    border: none;
                    padding: 8px;
                }}
                QPushButton:pressed {{
                    background-color: #707070; /* tummempi harmaa klikatessa */
                }}
            """)

        bottom_bar_layout.addWidget(self.btn_ostolistat)
        bottom_bar_layout.addWidget(self.btn_reseptit)
        bottom_bar_layout.addWidget(self.btn_tuotteet)
        bottom_bar_layout.addWidget(self.btn_asetukset)

        main_layout.addLayout(bottom_bar_layout)

        # Asetetaan oletussivuksi Ostolistat (index 0)
        self.stacked_widget.setCurrentIndex(0)