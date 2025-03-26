# File: product_detail_widget.py
import sys
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget
)
from PySide6.QtCore import Qt
from cookncart.controllers import ProductController, ShoppingListController, RecipeController
from cookncart.models import Product

# Import the new edit product widget (make sure this file exists)
from cookncart.widgets.edit_product_widget import EditProductWidget

class ProductDetailWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Controllers
        self.product_controller = ProductController()
        self.shoplist_controller = ShoppingListController()

        # Currently displayed product
        self.product = None

        # Main layout and a stacked widget to hold the detail view and edit view
        self.main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget(self)
        self.main_layout.addWidget(self.stacked)

        # Page 0: Detail view
        self.detail_view = QWidget()
        self._init_detail_view()
        self.stacked.addWidget(self.detail_view)  # index 0

        # Page 1: Edit product view
        self.edit_view = EditProductWidget()
        self.edit_view.product_updated.connect(self._on_product_updated)
        self.edit_view.edit_cancelled.connect(self._on_edit_cancelled)
        self.stacked.addWidget(self.edit_view)  # index 1

        self.setLayout(self.main_layout)

    def _init_detail_view(self):
        """Initializes the product detail view."""
        layout = QVBoxLayout(self.detail_view)

        # Create labels for product information
        self.name_label = QLabel()
        self.price_label = QLabel()
        self.category_label = QLabel()
        self.unit_label = QLabel()
        self.created_at_label = QLabel()
        self.updated_at_label = QLabel()

        for lbl in [self.name_label, self.price_label, self.category_label,
                    self.unit_label, self.created_at_label, self.updated_at_label]:
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

        # Create a horizontal layout for action buttons: Edit and Delete
        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Muokkaa tuotetta")
        self.remove_btn = QPushButton("Poista tuote")
        self.remove_btn.setObjectName("delete_button")
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Back button
        self.back_btn = QPushButton("Takaisin")
        layout.addWidget(self.back_btn)

        # Connect the edit button to switch the stacked widget to the edit view
        self.edit_btn.clicked.connect(self._switch_to_edit_view)

    def set_product(self, product: Product):
        """Sets the product to display and updates the detail view."""
        self.product = product
        if product:
            currency_unit = self.product_controller.currency
            weight_unit = self.shoplist_controller.weight_unit
            volume_unit = self.shoplist_controller.volume_unit

            # Determine unit conversion
            if product.unit.lower() in ["kg", "g", "lb", "oz"]:
                converted_quantity = self.product_controller.convert_to_standard_unit(product.unit, 1)
                unit_display = f"{converted_quantity} {weight_unit}"
            elif product.unit.lower() in ["l", "ml", "fl oz", "gal"]:
                converted_quantity = self.product_controller.convert_to_standard_unit(product.unit, 1)
                unit_display = f"{converted_quantity} {volume_unit}"
            else:
                converted_quantity = 1
                unit_display = product.unit

            # Convert price based on standardized unit
            converted_price = product.price_per_unit * converted_quantity
            price_text = f"{converted_price:.2f} {currency_unit}"

            # Update detail view labels
            self.name_label.setText(f"Nimi: {product.name}")
            self.price_label.setText(f"Hinta: {self.product_controller.get_price_with_currency(product.price_per_unit)}")
            self.category_label.setText(f"Kategoria: {product.category}")
            self.unit_label.setText(f"Yksikkö: {unit_display}")
            self.created_at_label.setText(f"Luotu: {product.created_at}")
            self.updated_at_label.setText(f"Päivitetty: {product.updated_at}")
        else:
            self.name_label.setText("Tuotetta ei löytynyt")
            self.price_label.setText("")
            self.category_label.setText("")
            self.unit_label.setText("")
            self.created_at_label.setText("")
            self.updated_at_label.setText("")
        # Also update the edit view with current product data
        self.edit_view.set_product(product)
        # Ensure the detail view is shown
        self.stacked.setCurrentIndex(0)

    def _switch_to_edit_view(self):
        """Switches the stacked widget to display the edit product view."""
        self.stacked.setCurrentIndex(1)

    def _on_product_updated(self, updated_product):
        """Called when the product is updated via the edit widget."""
        self.set_product(updated_product)
        # Switch back to the detail view
        self.stacked.setCurrentIndex(0)

    def _on_edit_cancelled(self):
        """Called when editing is cancelled; returns to the detail view."""
        self.stacked.setCurrentIndex(0)
