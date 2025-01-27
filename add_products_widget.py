# add_products_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QListWidget, QListWidgetItem,
    QStackedWidget, QFormLayout, QCompleter
)
from PySide6.QtCore import Signal, Qt, QStringListModel


TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class AddProductsWidget(QWidget):
    """
    A widget that lets the user:
      - search for products (with autocomplete),
      - see a list of all products, possibly select multiple,
      - add a new product,
      - click "OK" or "Cancel" to finish.

    We'll implement an inner QStackedWidget:
      Page 0: product list / selection
      Page 1: new product form

    Once finished, we emit `finished(selected_products)`.
    """
    finished = Signal(list)  # We will emit a list of selected products

    def __init__(self, product_controller, parent=None):
        super().__init__(parent)
        self.product_controller = product_controller

        # We'll keep track of selected products in a simple list
        # In a real app, you'd store the product IDs or a more robust structure
        self.selected_products = []

        # Store all products for filtering
        self.all_products = self.product_controller.get_all_products()

        # Outer layout
        self.outer_layout = QVBoxLayout(self)

        # Stacked widget: 2 pages
        self.stacked = QStackedWidget()

        # Page 0: The product list / selection
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1: The "Add new product" form
        self.page_add_form = QWidget()
        self.page_add_form.setLayout(self._create_add_form_layout())

        self.stacked.addWidget(self.page_list)       # index 0
        self.stacked.addWidget(self.page_add_form)   # index 1
        self.stacked.setCurrentIndex(0)

        self.outer_layout.addWidget(self.stacked)

    def _create_list_layout(self):
        layout = QVBoxLayout()

        # 1) Search bar without autocomplete
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae Tuotteita")
        self.search_bar.textChanged.connect(self._filter_product_list)  # Connect signal to filter method

        search_layout.addWidget(self.search_bar)

        layout.addLayout(search_layout)

        # 2) Scroll area or list widget to show all products
        self.product_list = QListWidget()
        layout.addWidget(self.product_list, 1)

        # Populate product_list
        self._refresh_product_list()

        # 3) Buttons: Add Product, OK, Cancel
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Lisää tuote (uusi)")
        add_btn.setStyleSheet(
            f"background-color: {TURKOOSI}; font-weight: bold;")
        add_btn.clicked.connect(self._open_add_product_form)

        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(
            f"background-color: {TURKOOSI}; font-weight: bold;")
        ok_btn.clicked.connect(self._finish_selection)

        cancel_btn = QPushButton("Peruuta")
        cancel_btn.setStyleSheet(
            f"background-color: {HARMAA}; font-weight: bold;")
        cancel_btn.clicked.connect(self._cancel_selection)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        return layout

    def _refresh_product_list(self, filtered_products=None):
        """
        Re-fetch all products from DB and show them in self.product_list.
        Optionally pre-check items the user previously selected.
        If filtered_products is provided, display only those.
        """
        self.product_list.clear()

        # Use filtered_products if provided, else use all_products
        products_to_show = filtered_products if filtered_products is not None else self.all_products.values()

        # We show them in a QListWidget with checkboxes:
        for product in products_to_show:
            item = QListWidgetItem(product.name)
            # store the actual Product object
            item.setData(Qt.UserRole, product)
            # Make the item checkable if you want multiple selection
            item.setCheckState(Qt.Unchecked)
            self.product_list.addItem(item)

        # Re-check items already in selected_products
        for i in range(self.product_list.count()):
            item = self.product_list.item(i)
            product_obj = item.data(Qt.UserRole)
            if product_obj in self.selected_products:
                item.setCheckState(Qt.Checked)

        self.product_list.sortItems(Qt.AscendingOrder)

    def _filter_product_list(self):
        """
        Filter the product list based on the search bar input.
        """
        query = self.search_bar.text().strip().lower()
        if not query:
            # If query is empty, show all products
            self._refresh_product_list()
            return

        # Filter products whose name contains the query (case-insensitive)
        filtered = [
            product for product in self.all_products.values()
            if query in product.name.lower()
        ]

        self._refresh_product_list(filtered_products=filtered)

    def _finish_selection(self):
        """
        Gather checked products from the list and emit `finished(...)`.
        """
        new_selection = []
        for i in range(self.product_list.count()):
            item = self.product_list.item(i)
            if item.checkState() == Qt.Checked:
                product_obj = item.data(Qt.UserRole)
                new_selection.append(product_obj)

        # Emit the combined selection
        self.finished.emit(new_selection)

    def _cancel_selection(self):
        """
        Emit the previously selected products (or empty) and close.
        """
        # Or you could emit an empty list to signal 'cancel'
        self.finished.emit(self.selected_products)

    def set_selected_products(self, products_list):
        """
        Called by AddRecipeWidget to set the initial selected products
        before we show the list.
        """
        self.selected_products = products_list[:]
        self._refresh_product_list()

    def _open_add_product_form(self):
        self.stacked.setCurrentIndex(1)

    def _create_add_form_layout(self):
        layout = QVBoxLayout()

        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.category_edit = QLineEdit()

        # Fetch all categories and ensure uniqueness
        all_categories = self.product_controller.get_all_categories()
        unique_categories = sorted(set(all_categories))  # Ensures unique and sorted categories

        categories_completer = QCompleter(unique_categories)
        categories_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.category_edit.setCompleter(categories_completer)

        form.addRow("Nimi:", self.name_edit)
        form.addRow("Yksikkö:", self.desc_edit)
        form.addRow("Hinta:", self.price_edit)
        form.addRow("Kategoria:", self.category_edit)

        layout.addLayout(form)

        # Save/Cancel
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("Tallenna tuote")
        save_btn.setStyleSheet(
            f"background-color: {TURKOOSI}; font-weight: bold;")
        save_btn.clicked.connect(self._save_new_product)

        back_btn = QPushButton("Takaisin")
        back_btn.setStyleSheet(
            f"background-color: {HARMAA}; font-weight: bold;")
        back_btn.clicked.connect(self._back_to_product_list)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(back_btn)

        layout.addLayout(btn_layout)

        layout.addStretch()
        return layout

    def _save_new_product(self):
        """
        Call product_controller.add_product(...) with data from the form,
        then go back to product list page and refresh.
        """
        name = self.name_edit.text().strip()
        desc = self.desc_edit.text().strip()
        price_str = self.price_edit.text().strip().replace(",", ".")
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            price = 0.0  # Default to 0.0 or handle the error as needed
            # Optionally, you can show an error message here

        cat = self.category_edit.text().strip()

        self.product_controller.add_product(
            name=name,
            unit=desc,
            price_per_unit=price,
            category=cat
        )

        # Update the all_products list
        self.all_products = self.product_controller.get_all_products()

        # Update the unique categories list
        all_categories = self.product_controller.get_all_categories()
        unique_categories = sorted(set(all_categories))
        self.category_edit.completer().setModel(QStringListModel(unique_categories))

        # Clear fields
        self.name_edit.clear()
        self.desc_edit.clear()
        self.price_edit.clear()
        self.category_edit.clear()

        # Go back to page 0 and refresh the product list
        self._back_to_product_list()
        self._filter_product_list()  # Apply current filter to include the new product if it matches

    def _back_to_product_list(self):
        """
        Switch from add form (page 1) back to list (page 0).
        """
        self.stacked.setCurrentIndex(0)
