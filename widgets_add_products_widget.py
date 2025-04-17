# File: widgets_add_products_widget.py --------------------------------------------------------------------

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QComboBox, QCheckBox,
    QStackedWidget, QMessageBox
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Signal, Qt, QTimer
from time import sleep
from qml import (
    ProductSelectorWidgetPage1, MainSearchTextField, ProductSelectorWidgetPage2
)
from root_controllers import ProductController as PC
from root_controllers import ShoppingListController as SLC
from root_controllers import RecipeController as RC

import functools
import logging

from error_handler import catch_errors_ui, show_error_toast

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class AddProductsWidget(QWidget):
    finished = Signal(list)

    @catch_errors_ui
    def __init__(self, parent=None, selected_products=[]):
        super().__init__(parent)
        self.product_controller = PC()
        self.selected_products = selected_products
        self.all_products = self.product_controller.get_all_products()

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.page1 = None
        self.page2 = None

        # Page 1
        self.flag = False
        self.page1 = QWidget()
        self.page1.setLayout(self.create_page1_layout())
        self.stacked.addWidget(self.page1)

        self.setLayout(main_layout)
        main_layout.addWidget(self.stacked, 1)
        self.stacked.setCurrentIndex(0)

    @catch_errors_ui
    def create_page1_layout(self):
        layout = QVBoxLayout()

        # -- Search Bar --
        top_bar_search_layout = QHBoxLayout()
        self.search_bar = MainSearchTextField(
            text_field_id="top_bar_search_bar",
            placeholder_text="Hae tuotetta..."
        )
        # Connect the search bar's textChanged signal to filter_products.
        self.search_bar.get_root_object().textChanged.connect(self.filter_products)
        top_bar_search_layout.addWidget(self.search_bar)
        layout.addLayout(top_bar_search_layout)

        # -- QML Scrollable List --
        self.scroll_area = ProductSelectorWidgetPage1(
            list_model_name="tuotteet_list"
        )
        # Connect the QML signal for item clicks if needed.
        # self.scroll_area.connect_item_clicked(self.handle_item_click)
        layout.addWidget(self.scroll_area, 1)

        # -- Buttons --
        button_layout = QHBoxLayout()
        self.next_button = QPushButton("Seuraava")
        button_layout.addWidget(self.next_button)
        self.cancel_button = QPushButton("Peruuta")
        self.cancel_button.setObjectName("gray_button")
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.next_button.clicked.connect(self.handle_next)
        self.cancel_button.clicked.connect(self.handle_cancel)

        # Initially populate the list.
        self.populate_product_list(self.scroll_area, self.all_products)
        return layout

    @catch_errors_ui
    def create_page2_layout(self, products):
        layout = QVBoxLayout()

        # -- QML Scrollable List --
        self.scroll_area2 = ProductSelectorWidgetPage2(
            list_model_name="tuotteet_list"
        )
        layout.addWidget(self.scroll_area2, 1)

        # -- Buttons --
        button_layout = QHBoxLayout()
        self.finish_button = QPushButton("Valmis")
        button_layout.addWidget(self.finish_button)
        self.back_button = QPushButton("Takaisin")
        self.back_button.setObjectName("gray_button")
        button_layout.addWidget(self.back_button)
        layout.addLayout(button_layout)

        self.finish_button.clicked.connect(self.handle_finish)
        self.back_button.clicked.connect(self.handle_back)

        # Initially populate the list.
        self.populate_product_list2(self.scroll_area2, products)
        return layout
    
    @catch_errors_ui
    def handle_back(self):
        """
        Handle the back button click event.
        """
        print("Back button clicked")
        self.stacked.setCurrentIndex(0)
        self.clearMemory(rem_page1=False)

    @catch_errors_ui
    def handle_cancel(self):
        """
        Handle the cancel button click event.
        """
        print("Cancel button clicked")
        self.finished.emit(self.selected_products)
        self.clearMemory()

    @catch_errors_ui
    def handle_next(self):
        """
        Handle the next button click event.
        """
        print("Next button clicked")
        root_obj = self.scroll_area.get_root_object()
        if root_obj is not None:
            js_value = root_obj.getSelectedTags()
            # Convert the QJSValue to a native Python list.
            selected = js_value.toVariant()
            print("selected products in handle_next:", selected)
            self.selected_products = selected
            
            if self.selected_products:
                self.page2 = QWidget()
                self.page2.setLayout(self.create_page2_layout(selected))
                self.stacked.addWidget(self.page2)
                self.stacked.setCurrentIndex(1)
            else:
                self.finished.emit(self.selected_products)
                self.clearMemory()

    @catch_errors_ui
    def handle_finish(self):
        """
        Handle the finish button click event.
        """
        print("Finish button clicked")
        root_obj = self.scroll_area2.get_root_object()
        if root_obj is not None:
            js_value = root_obj.getSelectedTags()
            products = js_value.toVariant()
        else:
            products = []

        new_selection = []
        for product in products:
            try:
                quantity = float(product["qty"])
                if quantity <= 0:
                    show_error_toast(self, message="Invalid quantity.\nQuantity must be positive.", lines=2)
                    return  # Stop if invalid
            except ValueError:
                show_error_toast(self, message="Invalid input.\nPlease enter a valid number.", lines=2)
                return
            new_selection.append({
                "id": product["id"],
                "quantity": quantity,
                "unit": product["unit"],
            })
            print(f"Product ID: {product['id']}, Quantity: {quantity}, Unit: {product['unit']}")
            
        self.finished.emit(new_selection)
        self.clearMemory()

    @catch_errors_ui
    def populate_product_list(self, target, products, filter_text=""):
        """
        Clear and repopulate the QML ListModel in the ScrollViewWidget
        with product names, optionally filtering by filter_text.
        Always include items that are already selected.
        """
        root_obj = target.get_root_object()
        if root_obj is not None:
            js_value = root_obj.getSelectedTags()
            # Convert the QJSValue to a native Python list.
            selected = js_value.toVariant()
            
            for item in selected:
                self.selected_products.append({
                    "id": item["id"],
                    "quantity": item["quantity"],
                    "unit": item["unit"]
                })
           
            root_obj.clearTags()
            # Sort products by name (case-insensitive)
            sorted_products = sorted(
                products.values(),
                key=lambda p: p.name.lower()
            )
            for product in sorted_products:
                # Check if the product is already selected.
                is_selected = any(item['id'] == product.id for item in self.selected_products)
                
                # Only add the product if it matches the filter text,
                # or if it has already been selected.
                if filter_text == "" or filter_text in product.name.lower() or is_selected:
                    if is_selected:
                        is_checked = True
                        # Get the previously stored quantity and unit.
                        selected_item = next(
                            (item for item in self.selected_products if item['id'] == product.id), None)
                        if selected_item:
                            quantity = selected_item['quantity']
                            unit = selected_item['unit']
                        else:
                            quantity = 1
                            unit = "kpl"
                    else:
                        is_checked = False
                        quantity = 1
                        unit = "kpl"

                    root_obj.addTag(product.name, product.id, is_checked, quantity, unit)
                    root_obj.reorderSelected()


    @catch_errors_ui
    def populate_product_list2(self, target, products, filter_text=""):
        """
        Clear and repopulate the QML ListModel in the ScrollViewWidget
        with product names, optionally filtering by filter_text.
        """
        root_obj = target.get_root_object()
        if root_obj is not None:
            root_obj.clearTags()
            for p in products:
                product = self.product_controller.get_product_by_id(p["id"])
                root_obj.addTag(product.name, p["id"], p["quantity"], p["unit"])

    @catch_errors_ui
    def filter_products(self, newText):
        """
        Called when the search bar text changes.
        Filters the product list to only include items that contain the search text.
        """
        search_text = newText.lower().strip()
        self.populate_product_list(
            filter_text=search_text, target=self.scroll_area, products=self.all_products)

    @catch_errors_ui
    def handle_item_click(self, product_id):
        """
        Handle the click event for a product item in the list.
        """
        print(f"Product clicked: {product_id}")

    @catch_errors_ui
    def clearMemory(self, rem_page1=True, rem_page2=True):
        """
        Clear the memory of the widget.
        """
        if self.page1 and rem_page1:
            print("Removing add_products page1")
            self.stacked.removeWidget(self.page1)
            self.page1.deleteLater()
            self.page1 = None
        if self.page2 and rem_page2:
            print("Removing add_products page2")
            self.stacked.removeWidget(self.page2)
            self.page2.deleteLater()
            self.page2 = None
