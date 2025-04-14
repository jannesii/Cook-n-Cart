# File: ostoslistat_page.py

import functools
import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QFrame, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from widgets_add_shoplist_widget import AddShoplistWidget
from widgets_shoplist_detail_widget import ShoplistDetailWidget
from root_controllers import ProductController, ShoppingListController
from qml import MainSearchTextField, ScrollViewWidget
from error_handler import catch_errors_ui, show_error_toast

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class OstolistatPage(QWidget):
    """
    Ostoslistat Page:
      - QStackedWidget with three pages:
         Page 0: Shopping list overview with a top bar (title, search bar, and "Luo uusi ostoslista" button)
                 and a scrollable list of shopping lists.
         Page 1: Add shopping list view (AddShoplistWidget).
         Page 2: Detail view (ShoplistDetailWidget).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.shoplist_controller = ShoppingListController()
        self.product_controller = ProductController()
        self.shopping_lists = {}
        self.update_shopping_lists()

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()

        # Page 0: List view
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())
        self.stacked.addWidget(self.page_list)

        # Page 1: Add shopping list view
        self.page_add_shoplist = None

        # Page 2: Detail view
        self.page_detail = None

        main_layout.addWidget(self.stacked, 1)
        self.setLayout(main_layout)
        self.stacked.setCurrentWidget(self.page_list)

    def _create_list_layout(self):
        layout = QVBoxLayout()

        # Top bar: title, search bar, and "Luo uusi ostoslista" button
        top_bar_layout = QHBoxLayout()
        self.title_label = QLabel("Ostoslistat")
        self.title_label.setObjectName("top_bar_title_label")

        top_bar_search_layout = QHBoxLayout()
        self.search_bar = MainSearchTextField(
            text_field_id="search_bar", placeholder_text="Hae ostoslistoja", parent=self)
        self.search_bar.get_root_object().textChanged.connect(self.filter_shopping_lists)

        self.new_btn = QPushButton("Luo uusi ostoslista")
        self.new_btn.setObjectName("top_bar_new_button")
        self.new_btn.clicked.connect(self.open_add_shoplist_page)

        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_search_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_btn)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")
        layout.addWidget(top_bar_frame)
        layout.addLayout(top_bar_search_layout)

        # Scroll area containing the shopping list buttons
        self.scroll_area = ScrollViewWidget(
            list_model_name="shopping_list", height=70)
        self.scroll_area.connect_item_clicked(self.display_shoplist_detail)
        layout.addWidget(self.scroll_area, 1)

        self.populate_shopping_list()
        return layout

    @catch_errors_ui
    def update_shopping_lists(self):
        """Fetch all shopping lists from the controller."""
        self.shopping_lists = self.shoplist_controller.get_all_shopping_lists()

    @catch_errors_ui
    def populate_shopping_list(self, filter_text=""):
        """Populate the scroll area with a button for each shopping list."""
        # Clear the scroll area before populating it again.
        self.scroll_area.clear_items()
        for shoplist_id, shoplist in self.shopping_lists.items():
            # Count how many items are purchased.
            purchased_count = self.shoplist_controller.get_purchased_count(
                shoplist_id)
            total_items = len(
                self.shoplist_controller.get_items_by_shopping_list_id(shoplist_id))
            # Create text showing purchased/total.
            text = f"{shoplist.title}\n{purchased_count}/{total_items}"
            if filter_text == "" or filter_text in shoplist.title.lower():
                self.scroll_area.add_item(text, shoplist_id)

    @catch_errors_ui
    def filter_shopping_lists(self, text):
        search_text = text.lower().strip()
        self.populate_shopping_list(filter_text=search_text)

    @catch_errors_ui
    def open_add_shoplist_page(self):
        self.page_add_shoplist = AddShoplistWidget(
            shoplist_controller=self.shoplist_controller,
            product_controller=self.product_controller,
            parent=self
        )
        self.page_add_shoplist.shoplist_created.connect(
            self.on_shoplist_created)
        self.page_add_shoplist.cancel_btn.clicked.connect(self.back_to_list)
        self.stacked.addWidget(self.page_add_shoplist)
        self.stacked.setCurrentWidget(self.page_add_shoplist)
        self.window().hide_buttons()

    @catch_errors_ui
    def display_shoplist_detail(self, shoplist_id):
        shoplist = self.shoplist_controller.get_shopping_list_by_id(
            shoplist_id)
        self.page_detail = ShoplistDetailWidget(parent=self)
        self.page_detail.set_shopping_list(shoplist)
        # When finished (e.g. after deletion or when user clicks back), return to list view.
        self.page_detail.finished.connect(self.back_to_list)
        self.stacked.addWidget(self.page_detail)
        self.stacked.setCurrentWidget(self.page_detail)
        self.window().hide_buttons()

    @catch_errors_ui
    def back_to_list(self):
        self.rm_add_shoplist_widget()
        self.rm_shoplist_detail_widget()
        self.update_shopping_lists()
        self.populate_shopping_list()
        self.stacked.setCurrentWidget(self.page_list)
        self.window().show_buttons()

    @catch_errors_ui
    def on_shoplist_created(self, shoplist_id):
        show_error_toast(self, "Ostoslista luotu onnistuneesti.", pos="top", background_color="green", text_color="black")
        self.back_to_list()

    @catch_errors_ui
    def rm_page_list(self):
        if self.page_list:
            print("Removing page_list")
            self.stacked.removeWidget(self.page_list)
            self.page_list.deleteLater()
            del self.page_list
            self.page_list = None

    @catch_errors_ui
    def rm_add_shoplist_widget(self):
        if self.page_add_shoplist:
            print("Removing page_add_shoplist")
            self.stacked.removeWidget(self.page_add_shoplist)
            self.page_add_shoplist.deleteLater()
            del self.page_add_shoplist
            self.page_add_shoplist = None

    @catch_errors_ui
    def rm_shoplist_detail_widget(self):
        if self.page_detail:
            print("Removing page_detail")
            self.stacked.removeWidget(self.page_detail)
            self.page_detail.deleteLater()
            del self.page_detail
            self.page_detail = None
