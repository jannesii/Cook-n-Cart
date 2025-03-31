# tuotteet_page.py

import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QStackedWidget,
    QFrame, QLineEdit, QCompleter, QFormLayout,
    QMessageBox
)
from PySide6.QtCore import Qt, QStringListModel

from root_controllers import ProductController as PC
from root_controllers import ShoppingListController as SLC
from root_controllers import RecipeController as RC
from widgets_product_detail_widget import ProductDetailWidget
from qml import NormalTextField, MainSearchTextField, ScrollViewWidget, ComboBoxWidget

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()


class TuotteetPage(QWidget):
    """
    Tuotteet-näkymä:
      - Yläpalkki: 'Tuotteet' -otsikko vasemmalla, 'Hae tuotetta' ja 'Uusi tuote' -napit oikealla
      - Keskialue: QML ScrollViewWidget displaying a list of products
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.products_dict = {}
        self.update_products_dict()

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.page_list = None
        self.page_add_form = None
        self.page_detail = None

        # Start with the list page
        self.setLayout(main_layout)
        main_layout.addWidget(self.stacked, 1)
        self.back_to_list()

    def _create_list_layout(self):
        layout = QVBoxLayout()
        # -- Top Bar --
        top_bar_layout = QHBoxLayout()
        self.title_label = QLabel("Tuotteet")
        self.title_label.setObjectName("top_bar_title_label")
        top_bar_search_layout = QHBoxLayout()
        self.search_bar = MainSearchTextField(
            text_field_id="top_bar_search_bar",
            placeholder_text="Hae tuotetta..."
        )
        self.new_button = QPushButton("Uusi tuote")
        self.new_button.clicked.connect(self.display_add_product)

        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_search_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_button)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")

        layout.addWidget(top_bar_frame, 0)
        layout.addLayout(top_bar_search_layout)

        # -- QML Scrollable List --
        self.scroll_area = ScrollViewWidget(list_model_name="tuotteet_list")
        layout.addWidget(self.scroll_area, 1)

        # Connect the search bar's textChanged signal to filter_products.
        self.search_bar.get_root_object().textChanged.connect(self.filter_products)
        # Connect the QML signal for item clicks.
        self.scroll_area.connect_item_clicked(self.handle_item_click)

        # Initially populate the list.
        self.populate_product_list()

        return layout

    def populate_product_list(self, filter_text=""):
        """
        Clear and repopulate the QML ListModel in the ScrollViewWidget
        with product names, optionally filtering by filter_text.
        """
        self.scroll_area.clear_items()

        # Sort products by name (case-insensitive)
        sorted_products = sorted(
            self.products_dict.values(),
            key=lambda p: p.name.lower()
        )

        for product in sorted_products:
            # Only add product if filter_text is empty or is found in the product name.
            if filter_text == "" or filter_text in product.name.lower():
                self.scroll_area.add_item(product.name, product.id)

    def filter_products(self, newText):
        """
        Called when the search bar text changes.
        Filters the product list to only include items that contain the search text.
        """
        search_text = newText.lower().strip()
        # Repopulate the list with the filtered products.
        self.populate_product_list(filter_text=search_text)

    def handle_item_click(self, product_id):
        """
        Handle the click event for a product item in the list.
        """
        print(f"Product clicked: {product_id}")
        product = ProductController.get_product_by_id(product_id)
        if product:
            self.show_product_details(product)

    def _create_add_form_layout(self):
        layout = QVBoxLayout()
        form = QFormLayout()
        self.name_edit = NormalTextField(
            text_field_id="name_edit", placeholder_text="Syötä nimi..."
        )
        self.unit_edit = ComboBoxWidget()
        
        self.price_edit = NormalTextField(
            text_field_id="price_edit", placeholder_text="Syötä hinta..."
        )
        self.category_edit = NormalTextField(
            text_field_id="category_edit", placeholder_text="Syötä kategoria..."
        )

        # Fetch and set up categories if needed
        all_categories = ProductController.get_all_categories()
        unique_categories = sorted(set(all_categories))
        categories_completer = QCompleter(unique_categories)
        categories_completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.category_edit.setCompleter(categories_completer)

        form.addRow("Nimi:", self.name_edit)
        form.addRow("Yksikkö:", self.unit_edit)
        form.addRow("Hinta:", self.price_edit)
        form.addRow("Kategoria:", self.category_edit)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Tallenna tuote")
        save_btn.clicked.connect(self._save_new_product)
        back_btn = QPushButton("Takaisin")
        back_btn.setObjectName("gray_button")
        back_btn.clicked.connect(self.back_to_list)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(back_btn)
        layout.addLayout(btn_layout)
        layout.addStretch()
        return layout

    def _save_new_product(self):
        name = self.name_edit.get_text().strip()
        desc = self.unit_edit.get_unit().strip()
        price_str = self.price_edit.get_text().strip().replace(",", ".")
        cat = self.category_edit.get_text().strip()

        if not name or not desc or not price_str:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please provide a value for Name, Description, and Price."
            )
            return

        try:
            price = float(price_str)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Price",
                "Please enter a valid numeric value for Price."
            )
            return

        print(f"Adding product: {name}, {desc}, {price}, {cat}")
        ProductController.add_product(
            name=name,
            unit=desc,
            price_per_unit=price,
            category=cat
        )

        self.update_products_dict()
        self.populate_product_list()
        self._update_category_completer()
        self.back_to_list()

    def _update_category_completer(self):
        all_categories = ProductController.get_all_categories()
        unique_categories = sorted(set(all_categories))
        # self.category_edit.completer().setModel(QStringListModel(unique_categories))

    def update_products_dict(self):
        self.products_dict = ProductController.get_all_products()

    def filter_products(self, newText):
        search_text = newText.lower().strip()
        self.populate_product_list(filter_text=search_text)

    def display_add_product(self):
        self.page_add_form = QWidget()
        self.page_add_form.setLayout(self._create_add_form_layout())
        self.stacked.addWidget(self.page_add_form)
        self.stacked.setCurrentWidget(self.page_add_form)

    def show_product_details(self, product):
        self.page_detail = ProductDetailWidget()
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        self.stacked.addWidget(self.page_detail)
        self.page_detail.set_product(product)
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        self.page_detail.remove_btn.clicked.connect(lambda: self.remove_product(product))
        self.stacked.setCurrentWidget(self.page_detail)

    def back_to_list(self):
        self.rm_page_add()
        self.rm_page_detail()
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())
        self.stacked.addWidget(self.page_list)
        self.stacked.setCurrentWidget(self.page_list)

    def rm_page_add(self):
        if self.page_add_form:
            print("Removing page_add_form")
            self.stacked.removeWidget(self.page_add_form)
            self.page_add_form.deleteLater()
            self.page_add_form = None

    def rm_page_detail(self):
        if self.page_detail:
            print("Removing page_detail")
            self.stacked.removeWidget(self.page_detail)
            self.page_detail.deleteLater()
            self.page_detail = None

    def rm_page_list(self):
        if self.page_list:
            print("Removing page_list")
            self.stacked.removeWidget(self.page_list)
            self.page_list.deleteLater()
            self.page_list = None

    def remove_product(self, product):
        ProductController.delete_product(product.id)
        self.update_products_dict()
        self.populate_product_list()
        self.back_to_list()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
