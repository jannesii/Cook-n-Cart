# asetukset_page.py

import sys
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QFrame, 
)

from cookncart.controllers import ProductController as PC
from cookncart.controllers import ShoppingListController as SLC
from cookncart.controllers import RecipeController as RC


TURKOOSI = "#00B0F0"
HARMAA = "#808080"
CONFIG_FILE = "cookncart/utils/config.json"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

class AsetuksetPage(QWidget):
    """
    Asetukset-sivu:
      - Yläpalkki: "Asetukset" -otsikko
      - Keskialue: 3 "nappiriviä" (tai kehyksiä), joihin on sijoitettu Label + ComboBox:
          1) "Valuutta" - '€'
          2) "Painon yksikkö" - 'kg'
          3) "Nestemäärän yksikkö" - 'l'
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Asetukset")
        label.setObjectName("top_bar_title_label")
        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")

        main_layout.addWidget(top_bar_frame, 0)

        # -- Keskialue --
        # Tehdään kolme "riviä", joissa vasemmalla label ja oikealla ComboBox,
        # ja koko rivi on kehystetty kuin nappi (pyöristetty, turkoosi).

        # 1) Valuutta
        def load_settings():
            """ Lataa asetukset config.json-tiedostosta. """
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                    return json.load(file).get("settings", {})
            except (FileNotFoundError, json.JSONDecodeError):
                return {"currency": "€", "weight_unit": "kg", "volume_unit": "l"}  # Oletusasetukset

        def save_settings():
            """ Tallentaa asetukset config.json-tiedostoon. """
            settings = {
                "settings": {
                    "currency": self.currency_combo.currentText(),
                    "weight_unit": self.weight_combo.currentText(),
                    "volume_unit": self.volume_combo.currentText()
                }
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4)

        self.settings = load_settings()

        currency_frame = QFrame()
        currency_frame.setObjectName("asetukset_frame")
        currency_layout = QHBoxLayout(currency_frame)

        currency_label = QLabel("Valuutta")
        currency_label.setObjectName("asetukset_label")

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["€", "$", "£"])
        self.currency_combo.setObjectName("asetukset_combobox")


        self.currency_combo.setCurrentText(self.settings.get("currency", "€"))
        self.currency_combo.currentTextChanged.connect(save_settings)

        currency_layout.addWidget(currency_label)
        currency_layout.addStretch()
        currency_layout.addWidget(self.currency_combo)

        # 2) Painon yksikkö
        weight_frame = QFrame()
        weight_frame.setObjectName("asetukset_frame")
        weight_layout = QHBoxLayout(weight_frame)

        weight_label = QLabel("Painon yksikkö")
        weight_label.setObjectName("asetukset_label")

        self.weight_combo = QComboBox()
        self.weight_combo.addItems(["kg", "g", "lb", "oz"])
        self.weight_combo.setObjectName("asetukset_combobox")

        self.weight_combo.setCurrentText(self.settings.get("weight_unit", "kg"))
        
        # Päivittää painoyksiköt järjestelmässä
        def update_weight_unit():
            save_settings()
            new_unit = self.weight_combo.currentText()
            ProductController.update_weight_unit(new_unit)
            ShoppingListController.update_weight_unit(new_unit)

        self.weight_combo.currentTextChanged.connect(update_weight_unit)

        weight_layout.addWidget(weight_label)
        weight_layout.addStretch()
        weight_layout.addWidget(self.weight_combo)

        # 3) Nestemäärän yksikkö
        volume_frame = QFrame()
        volume_frame.setObjectName("asetukset_frame")
        volume_layout = QHBoxLayout(volume_frame)

        volume_label = QLabel("Nestemäärän yksikkö")
        volume_label.setObjectName("asetukset_label")

        self.volume_combo = QComboBox()
        self.volume_combo.addItems(["l", "ml", "gallon", "fl oz"])
        self.volume_combo.setObjectName("asetukset_combobox")

        self.volume_combo.setCurrentText(self.settings.get("volume_unit", "l"))
        
        # Päivittää nesteyksiköt järjestelmässä
        def update_volume_unit():
            save_settings()
            new_unit = self.volume_combo.currentText()
            ProductController.update_volume_unit(new_unit)
            ShoppingListController.update_volume_unit(new_unit)

        self.volume_combo.currentTextChanged.connect(update_volume_unit)

        volume_layout.addWidget(volume_label)
        volume_layout.addStretch()
        volume_layout.addWidget(self.volume_combo)

        # Lisätään kehykset pystylayoutiin
        content_layout = QVBoxLayout()
        content_layout.addWidget(currency_frame)
        content_layout.addWidget(weight_frame)
        content_layout.addWidget(volume_frame)  # Lisää nesteyksikkö
        content_layout.addStretch()

        main_layout.addLayout(content_layout, 1)
