# add_shoplist_widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Signal

from widgets_add_products_widget import AddProductsWidget
from root_controllers import ProductController as PC

class AddShoplistWidget(QWidget):
    """
    Widget for creating a new shopping list with a title and optional items.
    """
    shoplist_created = Signal(int)  # Emits the ID of the newly created shopping list

    def __init__(self, shoplist_controller, product_controller, parent=None):
        super().__init__(parent)
        self.shoplist_controller = shoplist_controller
        self.product_controller = product_controller
        self.selected_products = []  # Store selected products from AddProductsWidget

        self.layout = QVBoxLayout(self)

        # Title input
        self.title_label = QLabel("Ostoslistan nimi:")
        self.layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.layout.addWidget(self.title_input)

        # Product selection widget
        self.product_selection_label = QLabel("Valitse tuotteita (valinnainen):")
        self.layout.addWidget(self.product_selection_label)

        self.add_products_widget = AddProductsWidget(self.product_controller, self)
        self.add_products_widget.finished.connect(self._handle_finished_add_products)
        self.layout.addWidget(self.add_products_widget)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.create_btn = QPushButton("Luo ostoslista")
        self.create_btn.clicked.connect(self._create_shoplist)
        buttons_layout.addWidget(self.create_btn)

        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setObjectName("gray_button")
        buttons_layout.addWidget(self.cancel_btn)

        self.layout.addLayout(buttons_layout)

    def _handle_finished_add_products(self, selected_products):
        """Handles the selection of products from AddProductsWidget."""

        self.selected_products = []
        
        for product_data in selected_products:
            product_id = product_data.get("id")
            quantity = product_data.get("quantity", 1)  
            
            # Ensure product_id is valid
            if not product_id:
                print("ERROR: Missing product ID in selected product data:", product_data)
                continue
            
            # Fetch full product details from the database
            product = self.product_controller.get_product_by_id(product_id)
            if not product:
                print(f"ERROR: Product with ID {product_id} not found in database.")
                continue  # Skip if product is not found
            
            # Append correctly structured data
            self.selected_products.append({
                "product": product,  
                "quantity": quantity,  
                "unit": product_data.get("unit", "kpl")  # Default unit
            })


    def _create_shoplist(self):
        """Create a new shopping list and emit its ID."""
        title = self.title_input.text().strip()

        if not title:
            self.title_label.setText("Ostoslistan nimi: (Ei voi olla tyhjä!)")
            self.title_label.setStyleSheet("color: red;")
            return

        # Create the shopping list with selected products
        try:
            shopping_list = self.shoplist_controller.add_shopping_list(title=title, items=self.selected_products)
        except ValueError as e:
            print(f"Error creating shopping list: {e}")
            return

        # Emit the ID of the created shopping list
        self.shoplist_created.emit(shopping_list.id)

        # Reset the form
        self.title_input.clear()
        self.selected_products = []
        self.add_products_widget.set_selected_products([])  # Reset selection in widget
