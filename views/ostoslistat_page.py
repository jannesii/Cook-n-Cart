# ostoslistat_page.py

import sys
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QFrame, QLineEdit, QListWidgetItem
)
from widgets.add_shoplist_widget import AddShoplistWidget
from widgets.shoplist_detail_widget import ShoplistDetailWidget

from controllers import ProductController
from controllers import ShoppingListController


TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class OstolistatPage(QWidget):
    """
    Ostoslistat Page:
    - StackedWidget with:
      - Page 0: Shopping list overview with a search bar and "Create New List" button.
      - Page 1: AddShoplistWidget to create a new shopping list.
      - Page 2: ShoplistDetailWidget to display details of a selected shopping list.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Controllers
        self.shoplist_controller = ShoppingListController()
        self.product_controller = ProductController()

        # Shopping lists dictionary
        self.shopping_lists = {}
        self.update_shopping_lists()

        # Main layout
        main_layout = QVBoxLayout(self)

        # Stacked widget
        self.stacked = QStackedWidget()

        # Page 0 (list view)
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1 (add shopping list view)
        self.page_add_shoplist = AddShoplistWidget(
            shoplist_controller=self.shoplist_controller,
            product_controller=self.product_controller,
            parent=self
        )
        self.page_add_shoplist.shoplist_created.connect(self.on_shoplist_created)
        self.page_add_shoplist.cancel_btn.clicked.connect(self.back_to_list)

        # Page 2 (detail view)
        self.page_detail = ShoplistDetailWidget()

        self.page_detail.back_btn.clicked.connect(self.back_to_list)

        # Add pages to the stacked widget
        self.stacked.addWidget(self.page_list)         # index 0
        self.stacked.addWidget(self.page_add_shoplist) # index 1
        self.stacked.addWidget(self.page_detail)       # index 2

        # Default to the shopping list view
        self.stacked.setCurrentIndex(0)

        # Add the stacked widget to the main layout
        main_layout.addWidget(self.stacked, 1)

    def _create_list_layout(self):
        """
        Creates the layout for the shopping list overview (Page 0).
        """
        layout = QVBoxLayout()

        # -- Top Bar --
        top_bar_layout = QHBoxLayout()

        # Title Label
        self.title_label = QLabel("Ostoslistat")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae ostoslistoja")
        self.search_bar.textChanged.connect(self.filter_shopping_lists)

        # Create New List Button
        self.new_btn = QPushButton("Luo uusi ostoslista")
        self.new_btn.clicked.connect(self.open_add_shoplist_page)

        # Styling
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        self.new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: #009ACD;
            }}
        """)

        # Assemble Top Bar
        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_btn)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;"
        )

        layout.addWidget(top_bar_frame, 0)

        # -- Scroll Area for Shopping Lists --
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1)

        # Populate shopping lists
        self.populate_shopping_list()

        return layout

    def update_shopping_lists(self):
        """
        Fetch all shopping lists from the controller and update the dictionary.
        """
        self.shopping_lists = self.shoplist_controller.get_all_shopping_lists()

    def populate_shopping_list(self):
        """
        Populate the scroll area with buttons for each shopping list.
        """
        # Clear the current layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add shopping lists to the layout
        for shoplist_id, shoplist in self.shopping_lists.items():
            btn = QPushButton(f"{shoplist.title} - {len(shoplist.items)} tuotetta")
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
                QPushButton:hover {{
                    background-color: #009ACD;
                }}
            """)
            # Connect the button to display the shopping list detail
            btn.clicked.connect(lambda checked=False, id=shoplist_id: self.display_shoplist_detail(id))
            self.scroll_layout.addWidget(btn)

        self.scroll_layout.addStretch()

    def display_shoplist_detail(self, shoplist_id):
        """
        Fill in the detail page with the given shopping list and switch to detail view.
        """
        shoplist = self.shoplist_controller.get_shopping_list_by_id(shoplist_id)
        self.page_detail.set_shoplist(shoplist)
        self.stacked.setCurrentIndex(2)

    def open_add_shoplist_page(self):
        """
        Opens the add shopping list page.
        """
        self.page_add_shoplist.setFieldsToDefaults()
        self.stacked.setCurrentIndex(1)

    def back_to_list(self):
        """
        Switch back to the shopping list overview and refresh the data.
        """
        self.update_shopping_lists()
        self.populate_shopping_list()
        self.stacked.setCurrentIndex(0)

    def on_shoplist_created(self):
        """
        Handle the creation of a new shopping list.
        """
        self.back_to_list()

    def filter_shopping_lists(self, text):
        """
        Filter the shopping list buttons based on search input.
        """
        search_text = text.lower()
        for i in range(self.scroll_layout.count() - 1):  # Exclude the stretch
            item = self.scroll_layout.itemAt(i).widget()
            if search_text in item.text().lower():
                item.show()
            else:
                item.hide()
