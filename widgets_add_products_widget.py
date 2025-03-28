# widgets_add_products_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QComboBox, QCheckBox,
    QMessageBox, QStackedWidget
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Signal, Qt, QTimer

from qml import ProductSelectorWidget, MainSearchTextField, ProductSelectorWidgetPage2
from root_controllers import ProductController as PC

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class AddProductsWidget(QWidget):
    finished = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_controller = PC()
        self.selected_products = []
        self.all_products = self.product_controller.get_all_products()

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()

        # Page 1
        self.page1 = QWidget()
        self.page1.setLayout(self.create_page1_layout())

        self.setLayout(main_layout)
        main_layout.addWidget(self.stacked, 1)
        self.stacked.addWidget(self.page1)

        self.stacked.setCurrentIndex(0)

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
        self.scroll_area = ProductSelectorWidget(list_model_name="tuotteet_list")
        # Connect the QML signal for item clicks.
        #self.scroll_area.connect_item_clicked(self.handle_item_click)
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
        self.populate_product_list(self.scroll_area,self.all_products)

        return layout
    
    def create_page2_layout(self, products):
        layout = QVBoxLayout()


        # -- QML Scrollable List --
        self.scroll_area2 = ProductSelectorWidgetPage2(list_model_name="tuotteet_list")
        # Connect the QML signal for item clicks.
        #self.scroll_area.connect_item_clicked(self.handle_item_click)
        layout.addWidget(self.scroll_area2, 1)

        # -- Buttons --
        button_layout = QHBoxLayout()
        self.finish_button = QPushButton("Valmis")
        button_layout.addWidget(self.finish_button)
        
        self.cancel_button = QPushButton("Peruuta")
        self.cancel_button.setObjectName("gray_button")
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.finish_button.clicked.connect(self.handle_finish)
        self.cancel_button.clicked.connect(self.handle_cancel)

        # Initially populate the list.
        self.populate_product_list2(self.scroll_area2, products)

        return layout

    def handle_cancel(self):
        """
        Handle the cancel button click event.
        """
        print("Cancel button clicked")
        self.finished.emit([])

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
            self.selected_products = selected
            print(f"Selected products: {selected}")
            products = []
            for id in selected:
                products.append(self.product_controller.get_product_by_id(id))
            self.page2 = QWidget()
            self.page2.setLayout(self.create_page2_layout(products))
            self.stacked.addWidget(self.page2)
            self.stacked.setCurrentIndex(1)
    
    def handle_finish(self):
        """
        Handle the finish button click event.
        """
        print("Finish button clicked")

    def populate_product_list(self, target, products, filter_text=""):
        """
        Clear and repopulate the QML ListModel in the ScrollViewWidget
        with product names, optionally filtering by filter_text.
        """
        root_obj = target.get_root_object()
        if root_obj is not None:
            root_obj.clearTags()
            # Sort products by name (case-insensitive)
            sorted_products = sorted(
                products.values(),
                key=lambda p: p.name.lower()
            )

            for product in sorted_products:
                is_checked = product.id in self.selected_products
                # Only add product if filter_text is empty or is found in the product name.
                if filter_text == "" or filter_text in product.name.lower():
                    root_obj.addTag(product.name, product.id, is_checked)
                    
    def populate_product_list2(self, target, products, filter_text=""):
        """
        Clear and repopulate the QML ListModel in the ScrollViewWidget
        with product names, optionally filtering by filter_text.
        """
        root_obj = target.get_root_object()
        if root_obj is not None:
            root_obj.clearTags()
            # Sort products by name (case-insensitive)
        

            for product in products:
                is_checked = product.id in self.selected_products
                # Only add product if filter_text is empty or is found in the product name.
                if filter_text == "" or filter_text in product.name.lower():
                    root_obj.addTag(product.name, product.id, is_checked)

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
