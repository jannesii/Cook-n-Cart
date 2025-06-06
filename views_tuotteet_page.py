# File: views_tuotteet_page.py --------------------------------------------------------------------

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame
)

from root_controllers import ProductController as PC
from widgets_product_detail_widget import ProductDetailWidget
from widgets_product_form_widget import ProductFormWidget
from qml import MainSearchTextField, ScrollViewWidget
from error_handler import catch_errors_ui, show_error_toast

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class TuotteetPage(QWidget):
    """
    Tuotteet-näkymä:
      - Yläpalkki: 'Tuotteet' -otsikko vasemmalla, 'Hae tuotetta' ja 'Uusi tuote' -napit oikealla
      - Keskialue: QML ScrollViewWidget displaying a list of products
    """

    @catch_errors_ui
    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_controller = PC()

        self.products_dict = {}
        self.update_products_dict()

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.page_list = None
        self.page_add_form = None
        self.page_detail = None
        self.unit_selector = None
        self.category_selector = None

        # Start with the list page
        self.setLayout(main_layout)
        main_layout.addWidget(self.stacked, 1)
        self.back_to_list()

    @catch_errors_ui
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

    @catch_errors_ui
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
            if filter_text == "" or filter_text in product.name.lower():
                self.scroll_area.add_item(product.name, product.id)

    @catch_errors_ui
    def filter_products(self, newText):
        """
        Called when the search bar text changes.
        Filters the product list to only include items that contain the search text.
        """
        search_text = newText.lower().strip()
        self.populate_product_list(filter_text=search_text)

    @catch_errors_ui
    def handle_item_click(self, product_id):
        """
        Handle the click event for a product item in the list.
        """
        print(f"Product clicked: {product_id}")
        product = self.product_controller.get_product_by_id(product_id)
        if product:
            self.show_product_details(product)

    @catch_errors_ui
    def update_products_dict(self):
        self.products_dict = self.product_controller.get_all_products()

    @catch_errors_ui
    def display_add_product(self):
        if not self.page_add_form:
            self.page_add_form = ProductFormWidget(
                self.product_controller, parent=self)
            self.stacked.addWidget(self.page_add_form)
            self.page_add_form.canceled.connect(self.back_to_list)
            self.page_add_form.finished.connect(self.on_product_added)
        self.stacked.setCurrentWidget(self.page_add_form)
        self.window().hide_buttons()

    @catch_errors_ui
    def on_product_added(self, product):
        show_error_toast(self, "Tuote luotu onnistuneesti.",
                         pos="top", background_color="green", text_color="black")
        self.update_products_dict()
        self.populate_product_list()
        self.back_to_list()

    @catch_errors_ui
    def show_product_details(self, product):
        self.page_detail = ProductDetailWidget()
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        self.stacked.addWidget(self.page_detail)
        self.page_detail.set_product(product)
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        self.page_detail.remove_btn.clicked.connect(
            lambda checked: self.remove_product(product))
        self.stacked.setCurrentWidget(self.page_detail)
        self.window().hide_buttons()

    @catch_errors_ui
    def back_to_list(self):
        self.rm_page_add()
        self.rm_page_detail()
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())
        self.stacked.addWidget(self.page_list)
        self.stacked.setCurrentWidget(self.page_list)
        self.window().show_buttons()

    @catch_errors_ui
    def rm_page_add(self):
        if self.page_add_form:
            print("Removing page_add_form")
            self.stacked.removeWidget(self.page_add_form)
            self.page_add_form.deleteLater()
            self.page_add_form = None

    @catch_errors_ui
    def rm_page_detail(self):
        if self.page_detail:
            print("Removing page_detail")
            self.stacked.removeWidget(self.page_detail)
            self.page_detail.deleteLater()
            self.page_detail = None

    @catch_errors_ui
    def rm_page_list(self):
        if self.page_list:
            print("Removing page_list")
            self.stacked.removeWidget(self.page_list)
            self.page_list.deleteLater()
            self.page_list = None

    @catch_errors_ui
    def remove_product(self, product):
        self.product_controller.delete_product(product.id)
        self.update_products_dict()
        self.populate_product_list()
        self.back_to_list()

    @catch_errors_ui
    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
