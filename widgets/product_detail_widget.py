# product_detal_widget.py

import sys
import json
with open('utils/config.json') as f:
    data = json.load(f)
    currency = data['settings']['currency']

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton,

)
from PySide6.QtCore import Qt, QStringListModel
from datetime import datetime
from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC
from models import Product

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

class ProductDetailWidget (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.product = None  # We'll store the current product here

        self.layout = QVBoxLayout(self)

        # placeholders
        self.name_label = QLabel()
        self.price_label = QLabel()
        self.category_label = QLabel()
        self.tags_label = QLabel()
        self.created_at_label = QLabel()
        self.updated_at_label = QLabel()

        # Let text wrap
        for lbl in [
            self.name_label,self.price_label, self.category_label, self.tags_label,
            self.created_at_label, self.updated_at_label
        ]:
            lbl.setWordWrap(True)
            self.layout.addWidget(lbl)

        # "Back" button
        self.back_btn = QPushButton("Takaisin")
        self.layout.addWidget(self.back_btn)

        # "Remove" button
        self.remove_btn = QPushButton("Poista tuote")
        self.remove_btn.setObjectName("delete_button")
        self.layout.addWidget(self.remove_btn)

        self.setLayout(self.layout)

    def set_product(self, product):
        
        currency = data['settings']['currency']
        if currency == '$':
            multiplier = 1.18
        else:
            multiplier = 1

        self.product = product
        if product:
            self.name_label.setText(f"Nimi: {product.name}")
            self.price_label.setText(f"Hinta: {product.price_per_unit * multiplier} {currency}")
            self.category_label.setText(f"Kategoria: {product.category}")
            self.tags_label.setText(f"unit: {product.unit}")
            self.created_at_label.setText(f"Luotu: {product.created_at}")
            self.updated_at_label.setText(f"Päivitetty: {product.updated_at}")
        else:
            self.product = None
            self.name_label.setText("Tuotetta ei löytynyt")
            self.tags_label.setText("")
            self.created_at_label.setText("")
            self.updated_at_label.setText("")

