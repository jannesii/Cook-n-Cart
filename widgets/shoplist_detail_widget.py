import sys
import json

with open('utils/config.json') as f:
    data = json.load(f)
    currency = data['settings']['currency']

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, QStackedWidget
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

from widgets.add_products_widget import AddProductsWidget

class ShoplistDetailWidget(QWidget):
    """
    Widget that displays the details of a shopping list and allows managing its products.
    """
    finished = Signal()  # Signal to indicate when the user finishes interacting with this widget.

    def __init__(self, parent=None):
        super().__init__(parent)

        self.shoppinglist = None  # Initially set to None

        # Main layout
        self.layout = QVBoxLayout(self)

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Page 0: Shoplist Detail Page
        self.detail_page = QWidget()
        self.detail_page.setLayout(self._create_detail_layout())
        self.stacked_widget.addWidget(self.detail_page)

        # Page 1: Add Products Page
        self.add_products_widget = AddProductsWidget(ProductController, self)
        self.add_products_widget.finished.connect(self._handle_finished_add_products)
        self.stacked_widget.addWidget(self.add_products_widget)

        # Start with the detail page
        self.stacked_widget.setCurrentIndex(0)

    def _create_detail_layout(self):
        """Creates the layout for the shopping list detail page."""
        layout = QVBoxLayout()

        # Shoplist title
        self.shoplist_label = QLabel("Shopping List Details")
        self.shoplist_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.shoplist_label)

        # Product list
        self.product_list = QListWidget()
        layout.addWidget(self.product_list)

        # Add product button
        self.add_product_btn = QPushButton("Lisää tuote")
        self.add_product_btn.clicked.connect(self._open_add_products_widget)
        layout.addWidget(self.add_product_btn)

        # Back button
        self.back_btn = QPushButton("Takaisin")
        self.back_btn.clicked.connect(self._go_back)
        layout.addWidget(self.back_btn)

        return layout

    def set_shopping_list(self, shopping_list: ShoppingList):
        """Sets the shopping list to display in the widget."""
        self.shoppinglist = shopping_list
        self._refresh_product_list()

    def _refresh_product_list(self):
        """Refresh the displayed product list."""
        if not self.shoppinglist:
            return  # Do nothing if no shopping list is set
        
        self.product_list.clear()
        shopping_list_items = ShoppingListController.repo.get_items_by_shopping_list_id(self.shoppinglist.id)
        
        for item in shopping_list_items:
            product = ProductController.get_all_products().get(item.product_id)
            if product:
                item_text = f"{product.name} - {item.quantity} {product.unit} - {product.price_per_unit:.2f} {currency}"
                list_item = QListWidgetItem(item_text)
                list_item.setData(Qt.UserRole, item)
                self.product_list.addItem(list_item)

    def _open_add_products_widget(self):
        """Switch to the AddProductsWidget within the stacked widget."""
        # Get selected products for the current shopping list
        shopping_list_items = ShoppingListController.repo.get_items_by_shopping_list_id(self.shoppinglist.id)
        selected_products = [
            ProductController.get_all_products().get(item.product_id)
            for item in shopping_list_items
        ]
        selected_products = [prod for prod in selected_products if prod is not None]

        # Set the selected products in the AddProductsWidget
        self.add_products_widget.set_selected_products(selected_products)

        # Switch to AddProductsWidget
        self.stacked_widget.setCurrentIndex(1)

    def _handle_finished_add_products(self, selected_products):
        """Handle the finished signal from AddProductsWidget."""
        # Add the selected products to the shopping list
        self._add_selected_products(selected_products)

        # Switch back to the detail page
        self.stacked_widget.setCurrentIndex(0)

    def _add_selected_products(self, selected_products):
        """Add the selected products to the shopping list."""
        if not self.shoppinglist:
            print("No shopping list is set.")
            return

        # Create ShoppingListItem instances for each selected product
        shopping_list_items = []
        for product in selected_products:
            # Avoid adding duplicates
            existing_items = ShoppingListController.repo.get_items_by_shopping_list_id(self.shoppinglist.id)
            existing_product_ids = {item.product_id for item in existing_items}

            if product.id not in existing_product_ids:
                # Populate only required fields; database will handle the rest
                item = ShoppingListItem(
                    id=0,  # Leave as None for the database to auto-generate
                    shopping_list_id=self.shoppinglist.id,
                    product_id=product.id,
                    quantity=1,  # Default quantity (adjustable)
                    is_purchased=False,
                    created_at=None,  # Leave as None for database to auto-generate
                    updated_at=None   # Leave as None for database to auto-generate
                )
                shopping_list_items.append(item)

        # Add items to the shopping list via the controller
        ShoppingListController.repo.add_shopping_list_items(self.shoppinglist.id, shopping_list_items)

        # Refresh the product list in the UI
        self._refresh_product_list()


    def _go_back(self):
        """Emit a signal to go back to the previous view."""
        self.finished.emit()
