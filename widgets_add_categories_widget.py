# File: widgets_add_categories_widget.py --------------------------------------------------------------------

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel
)
from PySide6.QtCore import Signal, Qt
from qml import TagSelectorWidget, MainSearchTextField, NormalTextField
from root_controllers import ProductController
from error_handler import catch_errors_ui, show_error_toast


class AddCategoriesWidget(QWidget):
    finished = Signal(list)  # Emits a list of selected categories

    @catch_errors_ui
    def __init__(self, selected_categories=None, parent=None):
        super().__init__(parent)
        self.product_controller = ProductController()
        # Get all categories from the controller (unique and sorted)
        self.all_categories = sorted(
            set(self.product_controller.get_all_categories()))
        # Use provided selected_categories if any; otherwise, start empty.
        self.selected_categories = selected_categories if selected_categories is not None else []

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.main_page = None
        self.add_category_page = None

        self.setLayout(main_layout)
        main_layout.addWidget(self.stacked, 1)
        self._show_select_categories_page()

    @catch_errors_ui
    def _select_categories_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # -- Search Bar --
        top_bar_search_layout = QHBoxLayout()
        self.search_bar = MainSearchTextField(
            text_field_id="top_bar_search_bar",
            placeholder_text="Hae kategorioita..."
        )
        # Connect the search bar's textChanged signal to filter_products.
        self.search_bar.get_root_object().textChanged.connect(self.filter_products)
        top_bar_search_layout.addWidget(self.search_bar)
        layout.addLayout(top_bar_search_layout)

        # Create an instance of TagSelectorWidget (re-used for categories).
        self.category_selector = TagSelectorWidget()
        layout.addWidget(self.category_selector)

        # Bottom bar: new category button + OK/Cancel buttons.
        bottom_bar_layout = QVBoxLayout()
        self.add_category_btn = QPushButton("Lisää uusi kategoria")
        self.add_category_btn.setObjectName("add_category_button")
        # Connect the new category button to our new functionality.
        self.add_category_btn.clicked.connect(self._show_add_category_page)
        bottom_bar_layout.addWidget(self.add_category_btn)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        bottom_bar_layout.addLayout(btn_layout)
        bottom_bar_layout.setAlignment(Qt.AlignBottom)
        layout.addLayout(bottom_bar_layout)

        # Connect the OK and Cancel buttons.
        self.ok_btn.clicked.connect(self._finish_selection)
        self.cancel_btn.clicked.connect(self._cancel_selection)

        # Populate the category selector with categories.
        self.populate_categories()

        return layout

    @catch_errors_ui
    def _add_new_category_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.new_category_text_field = NormalTextField(
            text_field_id="new_category_text_field",
            placeholder_text="Syötä uusi kategoria..."
        )
        layout.addWidget(self.new_category_text_field)
        self.description_label = QLabel(
            "Kategoria on tuotteen ryhmittelyä varten. Kategoria voi olla esim. \"Elektroniikka\" tai \"Vaatteet\"."
        )
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        btn_layout = QHBoxLayout()
        self.add_category_btn = QPushButton("Lisää kategoria")
        self.cancel_add_category_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.add_category_btn)
        btn_layout.addWidget(self.cancel_add_category_btn)
        layout.addLayout(btn_layout)

        self.add_category_btn.clicked.connect(self._add_category)
        self.cancel_add_category_btn.clicked.connect(
            self._show_select_categories_page)

        return layout

    @catch_errors_ui
    def _add_category(self):
        new_category = self.new_category_text_field.get_text().strip()
        if not new_category:
            show_error_toast(self, "Kategoria ei voi olla tyhjä.", pos="top")
            return  # Stop processing if the category is empty
        if new_category not in self.all_categories:
            self.all_categories.append(new_category)
            self.all_categories.sort()
        if new_category not in self.selected_categories:
            self.selected_categories.append(new_category)
        self.populate_categories()
        self._show_select_categories_page()

    @catch_errors_ui
    def _show_select_categories_page(self):
        if self.main_page is None:
            self.main_page = QWidget()
            self.main_page.setLayout(self._select_categories_layout())
            self.stacked.addWidget(self.main_page)
        self.stacked.setCurrentWidget(self.main_page)

    @catch_errors_ui
    def _show_add_category_page(self):
        if self.add_category_page is None:
            self.add_category_page = QWidget()
            self.add_category_page.setLayout(self._add_new_category_layout())
            self.stacked.addWidget(self.add_category_page)
        self.stacked.setCurrentWidget(self.add_category_page)

    @catch_errors_ui
    def populate_categories(self, filter_text=""):
        """
        Populate the QML model in TagSelectorWidget with all categories.
        Pre-check categories that are already selected.
        """
        root_obj = self.category_selector.get_root_object()
        if root_obj is not None:
            # Retrieve the current selected categories from QML.
            js_value = root_obj.getSelectedTags()
            selected = js_value.toVariant()  # should be a list of category strings
            self.selected_categories = selected[:]  # update our internal list

            root_obj.clearTags()
            # Add each category from all_categories.
            for category in self.all_categories:
                is_checked = category in self.selected_categories
                if filter_text == "" or filter_text in category.lower() or is_checked:
                    root_obj.addTag(category, is_checked)
                    root_obj.reorderSelected()
        else:
            print("CategorySelectorWidget root object not found.")

    @catch_errors_ui
    def filter_products(self, newText):
        """
        Called when the search bar text changes.
        Filters the category list to only include items that contain the search text.
        """
        search_text = newText.lower().strip()
        self.populate_categories(filter_text=search_text)

    @catch_errors_ui
    def _finish_selection(self):
        """
        Retrieve the selected categories from the QML model, update stored selection,
        and emit the finished signal.
        """
        root_obj = self.category_selector.get_root_object()
        if root_obj is not None:
            js_value = root_obj.getSelectedTags()
            # Convert the QJSValue to a native Python list.
            selected = js_value.toVariant()
            self.selected_categories = selected
            self.finished.emit(selected)
        else:
            self.finished.emit([])

    @catch_errors_ui
    def _cancel_selection(self):
        """
        Retrieve the current selection on cancel and emit it.
        """
        root_obj = self.category_selector.get_root_object()
        if root_obj is not None:
            selected = root_obj.getSelectedTags().toVariant()
            self.selected_categories = selected
            print(f"Cancelled selection, categories: {selected}")
            self.finished.emit(selected)
        else:
            self.finished.emit([])
