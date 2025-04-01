# File: shoplist_detail_widget.py
import sys
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QLabel, QStackedWidget,
    QDialog
)
from PySide6.QtCore import Qt, Signal
from root_controllers import ProductController as PC
from root_controllers import ShoppingListController as SLC
from root_models import ShoppingList, ShoppingListItem
from widgets_add_products_widget import AddProductsWidget
from widgets_import_recipe_widget import ImportRecipeWidget
from qml import WarningDialog

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

        self.pc = PC()

        # Page 0: Detail view
        self.detail_page = QWidget()
        self.detail_page.setLayout(self._create_detail_layout())
        self.stacked_widget.addWidget(self.detail_page)

        # Page 1: Add products view
        self.add_products_widget = None

        # Page 2: New ImportRecipeWidget
        self.import_recipe_widget = None

        self.stacked_widget.setCurrentWidget(
            self.detail_page)  # Start with the detail page
        self.setLayout(self.layout)

    def _create_detail_layout(self):
        layout = QVBoxLayout()
        # Title for the shopping list
        self.shoplist_label = QLabel("Shopping List Details")
        self.shoplist_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.shoplist_label)

        # List of products already in the shopping list
        self.product_list = QListWidget()
        # Connect itemChanged signal so that toggling the checkbox updates the purchase status.
        self.product_list.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self.product_list)

        # Lisää uusi QLabel kokonaishinnan näyttämiseen
        self.total_cost_label = QLabel("Kokonaishinta: 0 €")
        self.total_cost_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_cost_label)

        # --- New Button: Import from Recipe ---
        self.import_from_recipe_btn = QPushButton("Tuo tuotteet reseptiltä")
        self.import_from_recipe_btn.clicked.connect(
            self._open_import_recipe_page)
        layout.addWidget(self.import_from_recipe_btn)

        # Existing button for manually adding a product
        self.add_product_btn = QPushButton("Lisää tuote")
        self.add_product_btn.clicked.connect(self._open_add_products_widget)
        layout.addWidget(self.add_product_btn)

        # Delete and Back buttons
        self.delete_btn = QPushButton("Poista ostoslista")
        self.delete_btn.setObjectName("delete_button")
        self.delete_btn.clicked.connect(self._delete_shoplist)
        layout.addWidget(self.delete_btn)

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
        """Refreshes the shopping list's product list and updates the total cost,
        converting quantities when needed and excluding purchased items."""
        if not self.shoppinglist:
            return

        self.product_list.clear()
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(
            self.shoppinglist.id)

        total_cost = 0  # Will hold the cost for unpurchased items

        # Block signals during list update
        self.product_list.blockSignals(True)

        # User’s preferred units from ShoppingListController
        user_weight_unit = self.shoplist_controller.weight_unit.lower()
        user_volume_unit = self.shoplist_controller.volume_unit.lower()

        for item in shopping_list_items:
            product = self.pc.get_all_products().get(item.product_id)
            if product:
                prod_unit = product.unit.lower()
                # Determine the quantity to use for price calculation.
                # For "kpl", no conversion is needed.
                if prod_unit == "kpl":
                    converted_quantity = item.quantity
                # For weight-based products
                    print("Conversion:", item.quantity, converted_quantity)
                elif prod_unit in ["kg", "g", "lb", "oz"]:
                    # Get conversion factors from the conversion service's weight table.
                    factor_user = 1
                    factor_product = 1
                    # Convert the quantity entered in the user's preferred weight unit to the product's unit.
                    converted_quantity = item.quantity * \
                        (factor_user / factor_product)
                    print("Conversion:", prod_unit, factor_user,
                          factor_product, item.quantity, converted_quantity)
                # For volume-based products
                elif prod_unit in ["l", "ml", "fl oz", "gal"]:
                    factor_user = 1
                    factor_product = 1
                    converted_quantity = item.quantity * \
                        (factor_user / factor_product)
                    print("Conversion:", prod_unit, factor_user,
                          factor_product, item.quantity, converted_quantity)
                else:
                    # If the unit is unknown, fall back to the raw quantity
                    converted_quantity = item.quantity

                # Calculate the cost for this item.
                # If the item is marked as purchased, skip adding its cost.
                total_price = product.price_per_unit * converted_quantity
                print(total_price, product.price_per_unit, converted_quantity)
                if not item.is_purchased:
                    total_cost += total_price

                # Create a display text for this product.
                purchased_prefix = "[Ostettu] " if item.is_purchased else ""
                # Optionally, you could show the converted quantity with the product's unit.
                display_text = (f"{purchased_prefix}{product.name} - {item.quantity} {user_weight_unit if prod_unit in ['kg','g','lb','oz'] else (user_volume_unit if prod_unit in ['l','ml','fl oz','gal'] else product.unit)} "
                                f"- {self.pc.get_price_with_currency(total_price)}")
                list_item = QListWidgetItem(display_text)
                list_item.setData(Qt.UserRole, item)
                list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
                list_item.setCheckState(
                    Qt.Checked if item.is_purchased else Qt.Unchecked)

                self.product_list.addItem(list_item)

        self.product_list.blockSignals(False)  # Re-enable signals

        # Convert the total cost to a currency string and update the label.
        total_cost_with_currency = self.pc.get_price_with_currency(total_cost)
        self.total_cost_label.setText(
            f"Kokonaishinta: {total_cost_with_currency}")

    # Lasketaan ja päivitetään ostoslistan kokonaishinta
        total_cost_with_currency = self.pc.get_price_with_currency(total_cost)
        self.total_cost_label.setText(
            f"Kokonaishinta: {total_cost_with_currency}")

    def _on_item_changed(self, list_item: QListWidgetItem):
        """
        Called when a list item's check state changes.
        Updates the corresponding shopping list item’s is_purchased status in the database,
        updates the item display, and recalculates the total cost.
        """
        shopping_list_item = list_item.data(Qt.UserRole)
        new_state = list_item.checkState() == Qt.Checked
        if shopping_list_item.is_purchased != new_state:
            shopping_list_item.is_purchased = new_state
            # Update the shopping list item in the repository.
            self.shoplist_controller.repo.update_shopping_list_items(
                [shopping_list_item])

            # Update the display text for this list item.
            product = self.pc.get_all_products().get(shopping_list_item.product_id)
            if product:
                purchased_prefix = "[Ostettu] " if new_state else ""
                # For display, you might keep the original quantity/unit or the user’s preferred unit.
                list_item.setText(
                    f"{purchased_prefix}{product.name} - {shopping_list_item.quantity} {product.unit} - {product.price_per_unit:.2f}")

            # Recalculate and update the total cost label.
            self._update_total_cost_label()

    def _update_total_cost_label(self):
        """
        Recalculates the total cost for the shopping list by iterating through all items,
        converting quantities when needed, and excluding items marked as purchased.
        """
        if not self.shoppinglist:
            return

        total_cost = 0.0
        # Get a ProductController instance and its conversion service.
        cs = self.pc.conversion_service  # ConversionService instance

        # Get the user's preferred weight/volume units.
        user_weight_unit = self.shoplist_controller.weight_unit.lower()
        user_volume_unit = self.shoplist_controller.volume_unit.lower()

        # Fetch current items for this shopping list.
        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(
            self.shoppinglist.id)

        for item in shopping_list_items:
            product = self.pc.get_all_products().get(item.product_id)
            if product:
                prod_unit = product.unit.lower()
                # If product unit is "kpl", no conversion is needed.
                if prod_unit == "kpl":
                    converted_quantity = item.quantity
                # Weight-based products: convert using weight factors.
                elif prod_unit in ["kg", "g", "lb", "oz"]:
                    factor_user = 1
                    factor_product = 1
                    converted_quantity = item.quantity * \
                        (factor_user / factor_product)
                # Volume-based products: convert using volume factors.
                elif prod_unit in ["l", "ml", "fl oz", "gal"]:
                    factor_user = 1
                    factor_product = 1
                    converted_quantity = item.quantity * \
                        (factor_user / factor_product)
                else:
                    converted_quantity = item.quantity

                total_price = product.price_per_unit * converted_quantity
                # Only add items that are not purchased.
                if not item.is_purchased:
                    total_cost += total_price

        # Convert total cost into a currency string.
        total_cost_with_currency = self.pc.get_price_with_currency(total_cost)
        self.total_cost_label.setText(
            f"Kokonaishinta: {total_cost_with_currency}")



    def _open_add_products_widget(self):
        if not self.shoppinglist:
            return

        self.add_products_widget = AddProductsWidget(PC(), self)
        self.add_products_widget.finished.connect(
            self._handle_finished_add_products)

        shopping_list_items = self.shoplist_controller.repo.get_items_by_shopping_list_id(
            self.shoppinglist.id)
        selected_products = []

        for item in shopping_list_items:
            product = PC().get_all_products().get(item.product_id)
            if product:
                selected_products.append({
                    "id": product.id,
                    "quantity": item.quantity,
                    # KPL jos yksikköä ei ole.
                    "unit": item.unit if hasattr(item, "unit") else "kpl"
                })

        self.stacked_widget.addWidget(self.add_products_widget)
        self.add_products_widget.set_selected_products(selected_products)
        self.stacked_widget.setCurrentWidget(self.add_products_widget)

    def _open_import_recipe_page(self):
        # Switch to the import recipe page (index 2)
        self.import_recipe_widget = ImportRecipeWidget(self)
        self.import_recipe_widget.importCompleted.connect(
            self._handle_import_completed)
        self.import_recipe_widget.cancelImport.connect(
            self._handle_import_cancel)
        self.stacked_widget.addWidget(self.import_recipe_widget)

        self.stacked_widget.setCurrentWidget(self.import_recipe_widget)

    def _handle_import_completed(self, selected_products):
        # Add the imported products to the shopping list (using your existing merge/update logic)
        self._add_selected_products(selected_products)
        # Return to the detail view after import
        self.stacked_widget.setCurrentWidget(self.detail_page)
        self.clear_memory()


    def _handle_import_cancel(self):
        # If cancelled, return to the detail view
        self.stacked_widget.setCurrentWidget(self.detail_page)
        self.clear_memory()
        
    def _handle_finished_add_products(self, selected_products):
        self._add_selected_products(selected_products)
        self.stacked_widget.setCurrentWidget(self.detail_page)
        self.clear_memory()
        
    def clear_memory(self):
        if self.import_recipe_widget:
            print("Removing import_recipe_widget")
            self.stacked_widget.removeWidget(self.import_recipe_widget)
            self.import_recipe_widget.deleteLater()
            del self.import_recipe_widget
            self.import_recipe_widget = None

        if self.add_products_widget:
            print("Removing add_products_widget")
            self.stacked_widget.removeWidget(self.add_products_widget)
            self.add_products_widget.deleteLater()
            del self.add_products_widget
            self.add_products_widget = None

    # Käyttää repo metodeja controllerin kautta, mutta controlleriin pitää lisätä nämä metodit.

    def _add_selected_products(self, selected_products):
        if not self.shoppinglist:
            print("No shopping list is set.")
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
            for item_id in removed_items:
                self.shoplist_controller.repo.delete_shopping_list_item(
                    item_id)

        if updated_items:
            self.shoplist_controller.repo.update_shopping_list_items(
                updated_items)

        if new_items:
            self.shoplist_controller.repo.add_shopping_list_items(
                self.shoppinglist.id, new_items)

        self._refresh_product_list()

    def _delete_shoplist(self):
        if not self.shoppinglist:
            return
        try:
            self.shoplist_controller.delete_shopping_list_by_id(
                self.shoppinglist.id)
            self._show_message(
                "Ostoslista on poistettu onnistuneesti.")
            self.finished.emit()
        except Exception as e:
            self._show_error(f"Ostoslistan poistaminen epäonnistui: {str(e)}")

    def _go_back(self):
        self.finished.emit()

    def _show_error(self, message):
        warning = WarningDialog(f"Virhe: {message}", self)
        warning.show()
        
    def _show_message(self, message):
        msg = WarningDialog(f"Viesti: {message}", self)
        msg.show()
