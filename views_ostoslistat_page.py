# File: ostoslistat_page.py (Revised)
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QFrame, QLineEdit
)
from PySide6.QtCore import Qt
from widgets_add_shoplist_widget import AddShoplistWidget
from widgets_shoplist_detail_widget import ShoplistDetailWidget
from root_controllers import ProductController, ShoppingListController
from qml import MainSearchTextField

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
        # self.search_bar.setPlaceholderText("Hae ostoslistoja")
        # self.search_bar.textChanged.connect(self.filter_shopping_lists)
        # self.search_bar.setObjectName("top_bar_search_bar")

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
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1)

        self.populate_shopping_list()
        return layout

    def update_shopping_lists(self):
        """Fetch all shopping lists from the controller."""
        self.shopping_lists = self.shoplist_controller.get_all_shopping_lists()

    def populate_shopping_list(self):
        """Populate the scroll area with a button for each shopping list."""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        for shoplist_id, shoplist in self.shopping_lists.items():
            # Count how many items are purchased
            purchased_count = sum(
                1 for item in shoplist.items if item.is_purchased)
            total_items = len(shoplist.items)
            # Create text showing purchased/total
            btn_text = f"{shoplist.title}\n{purchased_count}/{total_items}"
            btn = QPushButton(btn_text)
            btn.setObjectName("main_list_button")
            btn.clicked.connect(
                lambda checked=False, id=shoplist_id: self.display_shoplist_detail(id))
            self.scroll_layout.addWidget(btn)
        self.scroll_layout.addStretch()

    def filter_shopping_lists(self, text):
        search_text = text.lower()
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(search_text in widget.text().lower())

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

    def display_shoplist_detail(self, shoplist_id):
        shoplist = self.shoplist_controller.get_shopping_list_by_id(
            shoplist_id)
        self.page_detail = ShoplistDetailWidget()
        self.page_detail.set_shopping_list(shoplist)
        # When finished (e.g. after deletion or when user clicks back), return to list view.
        self.page_detail.finished.connect(self.back_to_list)
        self.stacked.addWidget(self.page_detail)
        self.stacked.setCurrentWidget(self.page_detail)

    def back_to_list(self):
        self.rm_add_shoplist_widget()
        self.rm_shoplist_detail_widget()
        self.update_shopping_lists()
        self.populate_shopping_list()
        self.stacked.setCurrentWidget(self.page_list)

    def on_shoplist_created(self, shoplist_id):
        self.back_to_list()

    def rm_page_list(self):
        if self.page_list:
            print("Removing page_list")
            self.stacked.removeWidget(self.page_list)
            self.page_list.deleteLater()
            del self.page_list
            self.page_list = None

    def rm_add_shoplist_widget(self):
        if self.page_add_shoplist:
            print("Removing page_add_shoplist")
            self.stacked.removeWidget(self.page_add_shoplist)
            self.page_add_shoplist.deleteLater()
            del self.page_add_shoplist
            self.page_add_shoplist = None

    def rm_shoplist_detail_widget(self):
        if self.page_detail:
            print("Removing page_detail")
            self.stacked.removeWidget(self.page_detail)
            self.page_detail.deleteLater()
            del self.page_detail
            self.page_detail = None
