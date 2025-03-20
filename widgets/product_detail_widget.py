import sys
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from controllers import ProductController, ShoppingListController, RecipeController
from models import Product

class ProductDetailWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.product_controller = ProductController()
        self.shoplist_controller = ShoppingListController()
        self.product = None  # Tallennetaan valittu tuote

        self.layout = QVBoxLayout(self)

        # Tekstikentät tuotteen tietojen näyttämiseen
        self.name_label = QLabel()
        self.price_label = QLabel()
        self.category_label = QLabel()
        self.unit_label = QLabel()
        self.created_at_label = QLabel()
        self.updated_at_label = QLabel()

        # Sallitaan tekstin rivittyminen
        for lbl in [
            self.name_label, self.price_label, self.category_label, self.unit_label,
            self.created_at_label, self.updated_at_label
        ]:
            lbl.setWordWrap(True)
            self.layout.addWidget(lbl)

        # "Takaisin" -nappi
        self.back_btn = QPushButton("Takaisin")
        self.layout.addWidget(self.back_btn)

        # "Poista tuote" -nappi
        self.remove_btn = QPushButton("Poista tuote")
        self.remove_btn.setObjectName("delete_button")
        self.layout.addWidget(self.remove_btn)

        self.setLayout(self.layout)

    def set_product(self, product):
    
        self.product = product
        if product:
        # Haetaan käyttäjän asetuksista paino-, tilavuusyksikkö ja valuutta
            currency_unit = self.product_controller.currency
            weight_unit = self.shoplist_controller.weight_unit
            volume_unit = self.shoplist_controller.volume_unit

        # Määritetään oikea yksikkö tuotteelle ja muunnetaan määrä
            if product.unit.lower() in ["kg", "g", "lb", "oz"]:
                converted_quantity = self.product_controller.convert_to_standard_unit(product.unit, 1)  # 1 unit in standardized form
                unit_display = f"{converted_quantity} {weight_unit}"
            elif product.unit.lower() in ["l", "ml", "fl oz", "gal"]:
                converted_quantity = self.product_controller.convert_to_standard_unit(product.unit, 1)  # 1 yksikkö
                unit_display = f"{converted_quantity} {volume_unit}"
            else:
                converted_quantity = 1  # Oletusarvo, jos yksikköä ei tunnisteta
                unit_display = product.unit

        # Muunnetaan hinta oikeaan valuuttaan ja suhteutetaan määrään
            converted_price = product.price_per_unit * converted_quantity
            price_text = f"{converted_price:.2f} {currency_unit}"

        # Päivitetään käyttöliittymä
            self.name_label.setText(f"Nimi: {product.name}")
            self.price_label.setText(f"Hinta: {self.product_controller.get_price_with_currency(product.price_per_unit)}")
            self.category_label.setText(f"Kategoria: {product.category}")
            self.unit_label.setText(f"Yksikkö: {unit_display}")
            self.created_at_label.setText(f"Luotu: {product.created_at}")
            self.updated_at_label.setText(f"Päivitetty: {product.updated_at}")
        else:
            self.product = None
            self.name_label.setText("Tuotetta ei löytynyt")
            self.price_label.setText("")
            self.category_label.setText("")
            self.unit_label.setText("")
            self.created_at_label.setText("")
            self.updated_at_label.setText("")
