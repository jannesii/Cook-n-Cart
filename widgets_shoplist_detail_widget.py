# File: shoplist_detail_widget.py

import functools
import logging
import sys
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QLabel, QStackedWidget,
    QGridLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from root_controllers import ProductController as PC
from root_controllers import ShoppingListController as SLC
from root_models import ShoppingList, ShoppingListItem
from widgets_add_products_widget import AddProductsWidget
from widgets_import_recipe_widget import ImportRecipeWidget
from qml import ShoplistWidget

from error_handler import catch_errors_ui, show_error_toast, ask_confirmation

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class ShoplistDetailWidget(QWidget):
    """
    Widget that displays the details of a shopping list and allows managing its products.
    A new "Poista ostoslista" button has been added to delete the shopping list.
    """
    finished = Signal()  # Emitted when the user finishes interacting with this widget.

    @catch_errors_ui
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.shoplist_controller = SLC()
        self.pc = PC()
        self.shoppinglist = None  # Current shopping list
        self.layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Page 0: Detail view
        self.detail_page = QWidget()
        self.detail_page.setLayout(self._create_detail_layout())
        self.stacked_widget.addWidget(self.detail_page)

        # Page 1: Add products view
        self.add_products_widget = None

        # Page 2: Import recipe widget
        self.import_recipe_widget = None

        self.stacked_widget.setCurrentWidget(
            self.detail_page)  # Start with the detail page
        self.setLayout(self.layout)

    @catch_errors_ui
    def _create_detail_layout(self):
        layout = QVBoxLayout()
        # List of products already in the shopping list
        self.product_list = ShoplistWidget(parent=self)
        # Title for the shopping list
        self.top_bar_layout = QHBoxLayout()
        self.shoplist_label = QLabel("Shopping List Details")
        self.set_all_checked_button = QPushButton("Merkitse kaikki ostetuksi")
        self.set_all_checked_button.clicked.connect(self.product_list.set_all_checked)
        
        self.top_bar_layout.addWidget(self.shoplist_label)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.set_all_checked_button)
        layout.addLayout(self.top_bar_layout)

        # Connect itemClicked signal so that toggling the checkbox updates the purchase status.
        self.product_list.connect_item_clicked(self._on_item_clicked)
        layout.addWidget(self.product_list)

        # Label to show total cost.
        self.total_cost_label = QLabel("Kokonaishinta: 0 €")
        self.total_cost_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_cost_label)

        button_layout = QGridLayout()
        # --- Import from Recipe Button ---
        self.import_from_recipe_btn = QPushButton("Tuo tuotteet reseptiltä")
        self.import_from_recipe_btn.clicked.connect(
            self._open_import_recipe_page)
        button_layout.addWidget(self.import_from_recipe_btn, 0, 0)

        # --- Add/Remove Product Button ---
        self.add_product_btn = QPushButton("Lisää/poista tuote")
        self.add_product_btn.clicked.connect(self._open_add_products_widget)
        button_layout.addWidget(self.add_product_btn, 0, 1)

        # --- Delete and Back Buttons ---
        self.delete_btn = QPushButton("Poista ostoslista")
        self.delete_btn.setObjectName("delete_button")
        self.delete_btn.clicked.connect(self._delete_shoplist)
        button_layout.addWidget(self.delete_btn, 1, 0)

        self.back_btn = QPushButton("Takaisin")
        self.back_btn.clicked.connect(self._go_back)
        button_layout.addWidget(self.back_btn, 1, 1)

        layout.addLayout(button_layout)
        return layout

    @catch_errors_ui
    def set_shopping_list(self, shopping_list: ShoppingList):
        """Sets the current shopping list and refreshes the product list."""
        self.shoppinglist = shopping_list
        self.shoplist_label.setText(shopping_list.title)
        self._refresh_product_list()

    @catch_errors_ui
    def _refresh_product_list(self):
        """Refreshes the shopping list's product list and updates the total cost,
        converting quantities when needed and excluding purchased items."""
        if not self.shoppinglist:
            return

        self.product_list.clear_tags()
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(
            self.shoppinglist.id)

        total_cost = 0  # Cost for unpurchased items

        for item in shopping_list_items:
            product = self.pc.get_all_products().get(item.product_id)
            if product:
                # Determine product_price based on the unit
                if product.unit == "kpl":
                    product_price = product.price_per_unit * item.quantity
                elif product.unit == "kg":
                    product_price = product.price_per_unit * item.quantity
                elif product.unit == "g":
                    product_price = product.price_per_unit * \
                        (item.quantity / 1000.0)
                elif product.unit == "mg":
                    product_price = product.price_per_unit * \
                        (item.quantity / 1000000.0)
                elif product.unit == "l":
                    product_price = product.price_per_unit * item.quantity
                elif product.unit == "dl":
                    product_price = product.price_per_unit * \
                        (item.quantity / 10.0)
                elif product.unit == "ml":
                    product_price = product.price_per_unit * \
                        (item.quantity / 1000.0)
                else:
                    product_price = 0  # Or handle unknown units appropriately

                if not item.is_purchased:
                    total_cost += product_price
                checked = True if item.is_purchased == 1 else False
                self.add_tag(text=product.name, checked=checked, id=item.id,
                             quantity=item.quantity, unit=product.unit, price=product_price)
        self._update_total_cost_label(total_cost)

    @catch_errors_ui
    def add_tag(self, text="", id=0, checked=False, quantity=0, unit="", price=0):
        """
        Adds a product to the shopping list.
        This method is called when a new product is added to the list.
        """
        self.product_list.get_root_object().addTag(
            text, id, checked, quantity, unit, price)
        self.product_list.update()

    @catch_errors_ui
    def _update_total_cost_label(self, total_cost=0):
        """
        Updates the total cost label with the formatted total cost.
        """
        self.total_cost_label.setText(f"Kokonaishinta: {total_cost:.2f}€")

    @catch_errors_ui
    def _on_item_clicked(self, item_id, checked, total_cost):
        """Handles the click event on a shopping list item.
        Updates the purchase status of the item in the database."""
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(
            self.shoppinglist.id)
        print(
            f"Item clicked: {item_id}, Checked: {checked}, Total Cost: {total_cost}")
        for item in shopping_list_items:
            if item.id == item_id:
                item.is_purchased = checked
                break
        self.shoplist_controller.update_purchased_status(item_id, not checked)
        self.shoplist_controller.update_total_sum(
            self.shoppinglist.id, total_cost)
        self._update_total_cost_label(total_cost)
        self.parent.populate_shopping_list()

    @catch_errors_ui
    def get_selected_products(self):
        """Returns a list of selected products from the shopping list."""
        if not self.shoppinglist:
            return []
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(
            self.shoppinglist.id)
        selected_products = []
        for item in shopping_list_items:
            product = self.pc.get_all_products().get(item.product_id)
            if product:
                selected_products.append({
                    "id": product.id,
                    "quantity": item.quantity,
                    "unit": item.unit if hasattr(item, "unit") else "kpl"
                })
        return selected_products

    @catch_errors_ui
    def _open_add_products_widget(self):
        if not self.shoppinglist:
            return
        selected_products = self.get_selected_products()
        self.add_products_widget = AddProductsWidget(
            parent=self, selected_products=selected_products)
        self.add_products_widget.finished.connect(
            self._handle_finished_add_products)
        self.stacked_widget.addWidget(self.add_products_widget)
        self.stacked_widget.setCurrentWidget(self.add_products_widget)

    @catch_errors_ui
    def _open_import_recipe_page(self):
        # Switch to the import recipe page.
        self.import_recipe_widget = ImportRecipeWidget(
            self, selected_products=self.get_selected_products())
        self.import_recipe_widget.importCompleted.connect(
            self._handle_import_completed)
        self.import_recipe_widget.cancelImport.connect(
            self._handle_import_cancel)
        self.stacked_widget.addWidget(self.import_recipe_widget)
        self.stacked_widget.setCurrentWidget(self.import_recipe_widget)

    @catch_errors_ui
    def _handle_import_completed(self, selected_products):
        # Add the imported products to the shopping list.
        self._add_selected_products(selected_products)
        # Return to the detail view after import.
        self.stacked_widget.setCurrentWidget(self.detail_page)
        self.clear_memory()

    @catch_errors_ui
    def _handle_import_cancel(self):
        # If cancelled, return to the detail view.
        self.stacked_widget.setCurrentWidget(self.detail_page)
        self.clear_memory()

    @catch_errors_ui
    def _handle_finished_add_products(self, selected_products):
        self._add_selected_products(selected_products)
        self.stacked_widget.setCurrentWidget(self.detail_page)
        self.clear_memory()

    @catch_errors_ui
    def clear_memory(self):
        if self.import_recipe_widget:
            print("Removing import_recipe_widget")
            self.stacked_widget.removeWidget(self.import_recipe_widget)
            self.import_recipe_widget.deleteLater()
            self.import_recipe_widget = None
        if self.add_products_widget:
            print("Removing add_products_widget")
            self.stacked_widget.removeWidget(self.add_products_widget)
            self.add_products_widget.deleteLater()
            self.add_products_widget = None

    @catch_errors_ui
    def _add_selected_products(self, selected_products):
        if not self.shoppinglist:
            print("No shopping list is set.")
            return
        if not selected_products:
            print("No products selected.")
            return
        existing_items = self.shoplist_controller.get_items_by_shopping_list_id(
            self.shoppinglist.id)
        existing_items_dict = {
            item.product_id: item for item in existing_items}
        new_items = []
        updated_items = []
        removed_items = []
        selected_product_ids = {product["id"] for product in selected_products}
        for product_data in selected_products:
            product_id = product_data["id"]
            quantity = product_data.get("quantity", 1)
            unit = product_data.get("unit")

            if unit is not None:
                self.pc.update_product(product_id=product_id, unit=unit)

            if product_id in existing_items_dict:
                existing_item = existing_items_dict[product_id]
                if existing_item.quantity != quantity:
                    existing_item.quantity = quantity
                    updated_items.append(existing_item)
            else:
                item = ShoppingListItem(
                    id=0,
                    shopping_list_id=self.shoppinglist.id,
                    product_id=product_id,
                    quantity=quantity,
                    is_purchased=False,
                    created_at=None,
                    updated_at=None
                )
                new_items.append(item)
        for product_id, existing_item in existing_items_dict.items():
            if product_id not in selected_product_ids:
                removed_items.append(existing_item.id)
        if removed_items:
            print(f"Removing items: {removed_items}")
            for item_id in removed_items:
                self.shoplist_controller.repo.delete_shopping_list_item(
                    item_id)
        if updated_items:
            print(f"Updating items: {updated_items}")
            self.shoplist_controller.repo.update_shopping_list_items(
                updated_items)
        if new_items:
            print(f"Adding new items: {new_items}")
            self.shoplist_controller.repo.add_shopping_list_items(
                self.shoppinglist.id, new_items)
        self._refresh_product_list()

    @catch_errors_ui
    def _delete_shoplist(self):
        if not self.shoppinglist:
            return

        confirm = ask_confirmation(
            self, pos="mid", yes_text="Poista", no_text="Peruuta")
        if confirm:
            self.shoplist_controller.delete_shopping_list_by_id(
                self.shoppinglist.id)
            show_error_toast(self.parent, "Ostoslista poistettu onnistuneesti.",
                             pos="top", background_color="green", text_color="black")
            self.finished.emit()

    @catch_errors_ui
    def _go_back(self):
        self.finished.emit()
