# File: add_products_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QFormLayout, QComboBox, QCheckBox, QMessageBox
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtCore import QStringListModel

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

class ProductItemWidget(QWidget):
    """
    Custom widget for displaying a product with:
      - a checkbox (showing the product name),
      - a quantity QLineEdit (with a double validator),
      - and a QComboBox for unit selection.
    """
    def __init__(self, product, selected=False, parent=None):
        super().__init__(parent)
        self.product = product
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Checkbox with product name
        self.checkbox = QCheckBox(product.name)
        self.checkbox.setChecked(selected)
        layout.addWidget(self.checkbox)
        layout.addStretch()
        
        # Label for quantity
        qty_label = QLabel("Qty:")
        layout.addWidget(qty_label)
        
        # Quantity input with validator (only positive numbers allowed)
        self.quantity_edit = QLineEdit("1.0")
        self.quantity_edit.setFixedWidth(50)
        validator = QDoubleValidator(0, 10000, 2, self)
        #self.quantity_edit.setValidator(validator)
        layout.addWidget(self.quantity_edit)
        
        # Unit selection drop-down
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["kpl", "g", "kg", "ml", "l", "oz", "lb"])
        layout.addWidget(self.unit_combo)
        
        self.setLayout(layout)

class AddProductsWidget(QWidget):
    """
    Widget for selecting products for a recipe.
    
    - The user can search products (with debounce).
    - The product list is sorted so that selected products always appear at the top.
    - When finished, a list of dictionaries is emitted; each dictionary contains
      'id', 'quantity', and 'unit' for a selected product.
    """
    finished = Signal(list)  # Emits a list of selected product dicts.

    def __init__(self, product_controller, parent=None):
        super().__init__(parent)
        self.product_controller = product_controller

        # Keep track of the products that have been selected (list of dicts)
        self.selected_products = []
        # Cache all products (assumed to be a dict keyed by product id)
        self.all_products = self.product_controller.get_all_products()
        
        self.outer_layout = QVBoxLayout(self)
        
        # --- Search Bar with Debounce ---
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae Tuotteita")
        self.outer_layout.addWidget(self.search_bar)
        
        # Setup a timer for debouncing search input (300 ms)
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(300)
        self.search_timer.setSingleShot(True)
        self.search_bar.textChanged.connect(lambda: self.search_timer.start())
        self.search_timer.timeout.connect(self._on_search_timeout)
        
        # --- Product List ---
        self.product_list = QListWidget()
        self.outer_layout.addWidget(self.product_list, 1)
        
        # --- Buttons at the bottom ---
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Lisää tuote (uusi)")
        add_btn.clicked.connect(self._open_add_product_form)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self._finish_selection)
        cancel_btn = QPushButton("Peruuta")
        cancel_btn.setObjectName("gray_button")
        cancel_btn.clicked.connect(self._cancel_selection)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        self.outer_layout.addLayout(btn_layout)
        
        self.setLayout(self.outer_layout)
        
        # Initially populate the product list.
        self._refresh_product_list()

    def _on_search_timeout(self):
        """Called when the search timer times out; updates the filter."""
        query = self.search_bar.text().strip().lower()
        if not query:
            self._refresh_product_list()
        else:
            filtered = [
                product for product in self.all_products.values()
                if query in product.name.lower()
            ]
            self._refresh_product_list(filtered_products=filtered)

    def _refresh_product_list(self, filtered_products=None):
        """Rebuilds the product list display.
        
        Selected products are sorted to appear at the top.
        """
        self.product_list.clear()
        products_to_show = filtered_products if filtered_products is not None else list(self.all_products.values())
        
        # Build a set of selected product IDs.
        selected_ids = {sp.get("id") for sp in self.selected_products}
        # Sort so that selected products come first, then alphabetically.
        sorted_products = sorted(
            products_to_show,
            key=lambda p: (0 if p.id in selected_ids else 1, p.name.lower())
        )
        
        for product in sorted_products:
            # Check if this product is already selected.
            selection = next((sp for sp in self.selected_products if sp.get("id") == product.id), None)
            selected = bool(selection)
            widget = ProductItemWidget(product, selected)
            if selection:
                # Prepopulate quantity and unit if already selected.
                widget.quantity_edit.setText(str(selection.get("quantity", 1.0)))
                current_unit = selection.get("unit", widget.unit_combo.itemText(0))
                index = widget.unit_combo.findText(current_unit)
                if index != -1:
                    widget.unit_combo.setCurrentIndex(index)
            item = QListWidgetItem(self.product_list)
            # Set the item's text to the product name (helps with sorting)
            item.setText(product.name)
            item.setSizeHint(widget.sizeHint())
            self.product_list.setItemWidget(item, widget)

    def _finish_selection(self):
        """Gathers all checked products and emits the finished signal with a list of dicts."""
        new_selection = []
        for index in range(self.product_list.count()):
            item = self.product_list.item(index)
            widget = self.product_list.itemWidget(item)
            if widget and widget.checkbox.isChecked():
                try:
                    quantity = float(widget.quantity_edit.text().strip())
                    if quantity <= 0:
                        QMessageBox.warning(
                            self,
                            "Invalid Quantity",
                            f"Quantity for product '{widget.product.name}' must be positive."
                        )
                        return  # Stop and do not proceed if invalid
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Invalid Input",
                        f"Please enter a valid number for the quantity of product '{widget.product.name}'."
                    )
                    return
                new_selection.append({
                    "id": widget.product.id,
                    "quantity": quantity,
                    "unit": widget.unit_combo.currentText()
                })
        self.finished.emit(new_selection)

    def _cancel_selection(self):
        """Emit the current selection if the user cancels."""
        self.finished.emit(self.selected_products)

    def set_selected_products(self, products_list):
        """Called by the parent widget (e.g. AddRecipeWidget) to prepopulate the selection."""
        self.selected_products = products_list[:]
        self._refresh_product_list()

    def _open_add_product_form(self):
        """Switches to an add-product form. (Implement as needed.)"""
        print("Add product functionality not implemented.")
