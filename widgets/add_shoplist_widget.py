from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Signal, Qt


class AddShoplistWidget(QWidget):
    """
    Widget for creating a new shopping list with a title and optional items.
    """
    shoplist_created = Signal(int)  # Emits the ID of the newly created shopping list

    def __init__(self, shoplist_controller, product_controller, parent=None):
        super().__init__(parent)
        self.shoplist_controller = shoplist_controller
        self.product_controller = product_controller

        self.layout = QVBoxLayout(self)

        # Title input
        self.title_label = QLabel("Ostoslistan nimi:")
        self.layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.layout.addWidget(self.title_input)

        # Product selection (optional)
        self.product_list_label = QLabel("Valitse tuotteita (valinnainen):")
        self.layout.addWidget(self.product_list_label)

        self.product_list = QListWidget()
        self.layout.addWidget(self.product_list)

        # Populate product list from the database
        self._populate_product_list()

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Create button
        self.create_btn = QPushButton("Luo ostoslista")
        self.create_btn.clicked.connect(self._create_shoplist)
        buttons_layout.addWidget(self.create_btn)

        # Cancel button
        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setObjectName("gray_button")
        buttons_layout.addWidget(self.cancel_btn)

        self.layout.addLayout(buttons_layout)

    def _populate_product_list(self):
        """Fetch and populate products into the list."""
        products = self.product_controller.get_all_products()
        for product_id, product in products.items():
            item_text = f"{product.name} ({product.unit}) - {product.category}"
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.UserRole, {"product_id": product_id, "product": product})
            list_item.setCheckState(Qt.Unchecked)  # Allow users to select products
            self.product_list.addItem(list_item)

    def _create_shoplist(self):
        """Create a new shopping list and emit its ID."""
        title = self.title_input.text().strip()
    
        # Validate the title is not empty
        if not title:
            self.title_label.setText("Ostoslistan nimi: (Ei voi olla tyhjä!)")
            self.title_label.setStyleSheet("color: red;")
            return

    # Gather selected products
        selected_products = []
        for i in range(self.product_list.count()):
            item = self.product_list.item(i)
            if item.checkState() == Qt.Checked:
                product_data = item.data(Qt.UserRole)
            
            # Ensure product_data is valid
                if not product_data or "product_id" not in product_data:
                    continue  # Skip invalid items
            
                product = self.product_controller.get_product_by_id(product_data["product_id"])
                if not product:
                    continue  # Skip if product is not found
            
                selected_products.append({"product": product, "quantity": 1})  # Default quantity

    # Create the shopping list
        try:
            shopping_list = self.shoplist_controller.add_shopping_list(title=title, items=selected_products)
        except ValueError as e:
            # Handle invalid data errors from add_shopping_list
            print(f"Error creating shopping list: {e}")
            return

    # Emit the ID of the created shopping list
        self.shoplist_created.emit(shopping_list.id)

    # Reset the form
        self.title_input.clear()
        for i in range(self.product_list.count()):
            self.product_list.item(i).setCheckState(Qt.Unchecked)

