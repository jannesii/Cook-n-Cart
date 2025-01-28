# asetukset_page.py

import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QFrame, 

)

from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC


TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

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
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;")

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
        currency_label.setStyleSheet(
            "color: black; font-size: 16px; font-weight: bold;")

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
        weight_label.setStyleSheet(
            "color: black; font-size: 16px; font-weight: bold;")

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


