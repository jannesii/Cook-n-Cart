import sys
import json

with open('utils/config.json') as f:
    data = json.load(f)
    currency = data['settings']['currency']

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Qt, Signal


from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC
from models import ShoppingList, ShoppingListItem

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

class ShoplistDetailWidget(QWidget):
    """
    Widget that displays the details of a shopping list and allows managing its products.
    """
    finished = Signal()  # Signal to indicate when the user finishes interacting with this widget.

    def __init__(self, parent=None):
        super().__init__(parent)

        self.shoppinglist = None  # Initially set to None

        # Layout
        self.layout = QVBoxLayout(self)

        # Shoplist title
        self.shoplist_label = QLabel("Shopping List Details")
        self.shoplist_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.shoplist_label)

        # Product list
        self.product_list = QListWidget()
        self.layout.addWidget(self.product_list)

        # Add product button
        self.add_product_btn = QPushButton("Lisää tuote")
        self.add_product_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        self.add_product_btn.clicked.connect(self._open_add_products_widget)
        self.layout.addWidget(self.add_product_btn)

        # Back button
        self.back_btn = QPushButton("Takaisin")
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        self.back_btn.clicked.connect(self._go_back)
        self.layout.addWidget(self.back_btn)

        self.setLayout(self.layout)

    def set_shopping_list(self, shopping_list: ShoppingList):
        """Sets the shopping list to display in the widget."""
        self.shoppinglist = shopping_list
        self._refresh_product_list()

    def _refresh_product_list(self):
        """Refresh the displayed product list."""
        if not self.shoppinglist:
            return  # Do nothing if no shopping list is set
        
        self.product_list.clear()
        shopping_list_items = ShoppingListController.get_items_by_shopping_list_id(self.shoppinglist.id)
        
        for item in shopping_list_items:
            product = ProductController.get_all_products().get(item.product_id)
            if product:
                item_text = f"{product.name} - {item.quantity} {product.unit}"
                list_item = QListWidgetItem(item_text)
                list_item.setData(Qt.UserRole, item)
                self.product_list.addItem(list_item)

    def _open_add_products_widget(self):
        """Open AddProductsWidget to select new products."""
        print("Lisää tuotteita - functionality is not yet implemented.")

    def _go_back(self):
        """Emit a signal to go back to the previous view."""
        self.finished.emit()