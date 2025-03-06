# File: shoplist_detail_widget.py (Revised)
import sys
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QLabel, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from models import ShoppingList, ShoppingListItem
from widgets.add_products_widget import AddProductsWidget

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

class ShoplistDetailWidget(QWidget):
    """
    Widget that displays the details of a shopping list and allows managing its products.
    A new "Poista ostoslista" button has been added to delete the shopping list.
    """
    finished = Signal()  # Emitted when the user finishes interacting with this widget.
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shoplist_controller = SLC()
        self.shoppinglist = None  # Current shopping list
        self.layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Page 0: Detail view
        self.detail_page = QWidget()
        self.detail_page.setLayout(self._create_detail_layout())
        self.stacked_widget.addWidget(self.detail_page)
        
        # Page 1: Add products view
        self.add_products_widget = AddProductsWidget(PC(), self)
        self.add_products_widget.finished.connect(self._handle_finished_add_products)
        self.stacked_widget.addWidget(self.add_products_widget)
        
        self.stacked_widget.setCurrentIndex(0)
        self.setLayout(self.layout)
    
    def _create_detail_layout(self):
        layout = QVBoxLayout()
        # Title label for the shopping list
        self.shoplist_label = QLabel("Shopping List Details")
        self.shoplist_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.shoplist_label)
        # List widget to show products
        self.product_list = QListWidget()
        layout.addWidget(self.product_list)
        # Button to open add products view
        self.add_product_btn = QPushButton("Lisää tuote")
        self.add_product_btn.clicked.connect(self._open_add_products_widget)
        layout.addWidget(self.add_product_btn)
        # New Delete button for deleting the shopping list
        self.delete_btn = QPushButton("Poista ostoslista")
        self.delete_btn.setObjectName("delete_button")
        self.delete_btn.clicked.connect(self._delete_shoplist)
        layout.addWidget(self.delete_btn)
        # Back button to return to the main list
        self.back_btn = QPushButton("Takaisin")
        self.back_btn.clicked.connect(self._go_back)
        layout.addWidget(self.back_btn)
        return layout
    
    def set_shopping_list(self, shopping_list: ShoppingList):
        """Sets the current shopping list and refreshes the product list."""
        self.shoppinglist = shopping_list
        self.shoplist_label.setText(shopping_list.title)
        self._refresh_product_list()
    
    def _refresh_product_list(self):
        if not self.shoppinglist:
            return
        self.product_list.clear()
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(self.shoppinglist.id)
        for item in shopping_list_items:
            product = PC().get_all_products().get(item.product_id)
            if product:
                item_text = f"{product.name} - {item.quantity} {product.unit}"
                list_item = QListWidgetItem(item_text)
                list_item.setData(Qt.UserRole, item)
                self.product_list.addItem(list_item)
    
    def _open_add_products_widget(self):
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(self.shoppinglist.id)
        selected_products = [
            PC().get_all_products().get(item.product_id)
            for item in shopping_list_items if PC().get_all_products().get(item.product_id)
        ]
        self.add_products_widget.set_selected_products(selected_products)
        self.stacked_widget.setCurrentIndex(1)
    
    def _handle_finished_add_products(self, selected_products):
        self._add_selected_products(selected_products)
        self.stacked_widget.setCurrentIndex(0)
    
    def _add_selected_products(self, selected_products):
        if not self.shoppinglist:
            print("No shopping list is set.")
            return
        existing_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(self.shoppinglist.id)
        existing_ids = {item.product_id for item in existing_items}
        new_items = []
        for product in selected_products:
            if product.id not in existing_ids:
                item = ShoppingListItem(
                    id=0,
                    shopping_list_id=self.shoppinglist.id,
                    product_id=product.id,
                    quantity=1,
                    is_purchased=False,
                    created_at=None,
                    updated_at=None
                )
                new_items.append(item)
        if new_items:
            self.shoplist_controller.repo.add_shopping_list_items(self.shoppinglist.id, new_items)
        self._refresh_product_list()
    
    def _delete_shoplist(self):
        if not self.shoppinglist:
            return
        confirm = QMessageBox.question(
            self,
            "Vahvistus",
            "Haluatko varmasti poistaa tämän ostoslistan?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                self.shoplist_controller.delete_shopping_list_by_id(self.shoppinglist.id)
                QMessageBox.information(self, "Poistettu", "Ostoslista on poistettu onnistuneesti.")
                self.finished.emit()
            except Exception as e:
                QMessageBox.critical(self, "Virhe", f"Ostoslistan poistaminen epäonnistui: {str(e)}")
    
    def _go_back(self):
        self.finished.emit()
