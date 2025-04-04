# add_shoplist_widget.py

import functools
import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PySide6.QtCore import Signal, Qt
from widgets_add_products_widget import AddProductsWidget
from root_controllers import ProductController as PC
from qml import NormalTextField

from error_handler import catch_errors_ui


class AddShoplistWidget(QWidget):
    """
    Widget for creating a new shopping list with a title and optional items.
    """
    shoplist_created = Signal(
        int)  # Emits the ID of the newly created shopping list

    @catch_errors_ui
    def __init__(self, shoplist_controller=None, product_controller=None, parent=None):
        super().__init__(parent)
        self.shoplist_controller = shoplist_controller
        self.product_controller = product_controller
        self.selected_products = []  # Store selected products from AddProductsWidget

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.title_input = NormalTextField(
            placeholder_text="Ostoslistan nimi...", text_field_id="shoplist_title_input")
        layout.addWidget(self.title_input)
        # Create a label to show error messages for the title input.
        self.title_label = QLabel()
        layout.addWidget(self.title_label)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.create_btn = QPushButton("Luo ostoslista")
        self.create_btn.clicked.connect(self._create_shoplist)
        buttons_layout.addWidget(self.create_btn)

        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setObjectName("gray_button")
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    @catch_errors_ui
    def _handle_finished_add_products(self, selected_products):
        """Handles the selection of products from AddProductsWidget."""
        self.selected_products = []
        for product_data in selected_products:
            product_id = product_data.get("id")
            quantity = product_data.get("quantity", 1)
            # Ensure product_id is valid.
            if not product_id:
                print(
                    "ERROR: Missing product ID in selected product data:", product_data)
                continue
            # Fetch full product details from the database.
            product = self.product_controller.get_product_by_id(product_id)
            if not product:
                print(
                    f"ERROR: Product with ID {product_id} not found in database.")
                continue  # Skip if product is not found.
            # Append correctly structured data.
            self.selected_products.append({
                "product": product,
                "quantity": quantity,
                "unit": product_data.get("unit", "kpl")  # Default unit.
            })

    @catch_errors_ui
    def _create_shoplist(self):
        """Create a new shopping list and emit its ID."""
        title = self.title_input.get_text().strip()
        if not title:
            self.title_label.setText("Ostoslistan nimi: (Ei voi olla tyhjä!)")
            self.title_label.setStyleSheet("color: red;")
            return

        # Create the shopping list with selected products.
        try:
            shopping_list = self.shoplist_controller.add_shopping_list(
                title=title, items=self.selected_products)
        except ValueError as e:
            print(f"Error creating shopping list: {e}")
            return

        # Emit the ID of the created shopping list.
        self.shoplist_created.emit(shopping_list.id)

        # Reset the form.
        self.selected_products = []
