# tuotteet_page.py

import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QStackedWidget, 
    QFrame, QLineEdit, QCompleter, QFormLayout
)
from PySide6.QtCore import Qt, QStringListModel

from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC
from widgets.product_detail_widget import ProductDetailWidget

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

class TuotteetPage(QWidget):
    """
    Tuotteet-näkymä:
      - Yläpalkki: 'Tuotteet' -otsikko vasemmalla, 'Hae tuotetta' ja 'Uusi tuote' -napit oikealla
      - Keskialue: Scrollattava lista tuotteista
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.products_dict = {}
        self.update_products_dict()

        main_layout = QVBoxLayout(self)

        self.stacked = QStackedWidget()

        # Page 0 (list view)
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1 (add product view)
        self.page_add_form = QWidget()
        self.page_add_form.setLayout(self._create_add_form_layout())

        # page 2 (detail view)
        self.page_detail = ProductDetailWidget()
        #hook the "Back" button in ProductDetailWidget
        self.page_detail.back_btn.clicked.connect(self.back_to_list)

        self.stacked.addWidget(self.page_list)      # index 0
        self.stacked.addWidget(self.page_add_form)  # index 1
        self.stacked.addWidget(self.page_detail)    # index 2
        # Start with the list page
        self.stacked.setCurrentIndex(0)

        main_layout.addWidget(self.stacked, 1)

    def _create_list_layout(self):
        layout = QVBoxLayout()
        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()

        self.title_label = QLabel("Tuotteet")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae tuotetta")
        self.search_bar.textChanged.connect(self.filter_products)

        self.new_button = QPushButton("Uusi tuote")
        self.new_button.clicked.connect(self.display_add_product)

        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        self.new_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
        """)

        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_button)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;"
        )

        layout.addWidget(top_bar_frame, 0)

        # -- Scrollattava lista keskellä --
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1)

        self.populate_product_list()

        return layout

    def _create_add_form_layout(self):
        layout = QVBoxLayout()

        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.category_edit = QLineEdit()

        # Fetch all categories and ensure uniqueness
        all_categories = ProductController.get_all_categories()
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
            f"background-color: {TURKOOSI}; font-weight: bold;"
        )
        save_btn.clicked.connect(self._save_new_product)

        back_btn = QPushButton("Takaisin")
        back_btn.setStyleSheet(
            f"background-color: {HARMAA}; font-weight: bold;"
        )
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

        # Add the new product using the ProductController
        ProductController.add_product(
            name=name,
            unit=desc,
            price_per_unit=price,
            category=cat
        )

        # Update the products dictionary and refresh the product list
        self.update_products_dict()
        self.populate_product_list()

        # Update the category completer with unique categories
        self._update_category_completer()

        # Clear fields
        self.name_edit.clear()
        self.desc_edit.clear()
        self.price_edit.clear()
        self.category_edit.clear()

        # Go back to page 0 and refresh the product list
        self._back_to_product_list()

    def _update_category_completer(self):
        """
        Refresh the category completer to include any new unique categories.
        """
        all_categories = ProductController.get_all_categories()
        unique_categories = sorted(set(all_categories))
        self.category_edit.completer().setModel(QStringListModel(unique_categories))

    def _back_to_product_list(self):
        """
        Switch from add form (page 1) back to list (page 0).
        """
        self.stacked.setCurrentIndex(0)

    def display_add_product(self):
        self.stacked.setCurrentIndex(1)

    def update_products_dict(self):
        """
        Fetch all products from the ProductController and update the local dictionary.
        """
        self.products_dict = ProductController.get_all_products()

    def filter_products(self):
        """
        Filter the product buttons based on the search text.
        """
        search_text = self.search_bar.text().lower()
        for i in range(self.scroll_layout.count() - 1):  # Exclude the stretch
            item = self.scroll_layout.itemAt(i)
            widget = item.widget() if item else None
            if widget is not None:
                if search_text in widget.text().lower():
                    widget.show()
                else:
                    widget.hide()
            else:
                # Optionally, log or handle the unexpected None widget
                print(f"Warning: No widget found at index {i} during filtering.")

    def populate_product_list(self):
        """
        Populate the scroll area with buttons representing each product.
        """
        # Clear the current layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                # If the item is a layout or spacer, just remove it
                if item.layout():
                    self._clear_layout(item.layout())
        
        # Sort products by name (case-insensitive)
        sorted_products = sorted(
            self.products_dict.values(),
            key=lambda p: p.name.lower()
        )

        # Add products to the layout
        for product in sorted_products:
            btn = QPushButton(f"{product.name}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }}
            """)
            # Connect the button to a detailed view
            btn.clicked.connect(lambda checked, p=product: self.show_product_details(p))
            self.scroll_layout.addWidget(btn)
            # Optionally, connect the button to a detailed view or action
            # btn.clicked.connect(lambda checked, p=product: self.view_product_details(p))
            self.scroll_layout.addWidget(btn)

        # Ensure only one stretch is present
        self.scroll_layout.addStretch()

    def show_product_details(self, product):
        """
        Switch to the detail page and show the details of the given product.
        """
        self.page_detail.set_product(product)
        self.stacked.setCurrentIndex(2)

    def back_to_list(self):
        self.parent().setCurrentIndex(0)

    def _clear_layout(self, layout):
        """
        Recursively clear a layout.
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())


