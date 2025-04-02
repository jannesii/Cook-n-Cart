# File: widgets_add_tags_widget.py

import functools
import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog,
    QStackedWidget, QLabel, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from qml import TagSelectorWidget, MainSearchTextField, NormalTextField, WarningDialog
from root_controllers import ProductController

from error_handler import catch_errors_ui


class AddTagsWidget(QWidget):
    finished = Signal(list)  # Emits a list of selected tags

    @catch_errors_ui
    def __init__(self, recipe_controller, selected_tags=None, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        # Get all tags from the controller (unique and sorted)
        self.all_tags = sorted(set(self.recipe_controller.get_all_tags()))
        # Use provided selected_tags if any; otherwise, start empty.
        self.selected_tags = selected_tags if selected_tags is not None else []

        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.main_page = None
        self.add_tag_page = None

        self.setLayout(main_layout)
        main_layout.addWidget(self.stacked, 1)
        self._show_select_tags_page()

    @catch_errors_ui
    def _select_tags_layout(self):
        layout = QVBoxLayout()

        # -- Search Bar --
        top_bar_search_layout = QHBoxLayout()
        self.search_bar = MainSearchTextField(
            text_field_id="top_bar_search_bar",
            placeholder_text="Hae tageja..."
        )
        # Connect the search bar's textChanged signal to filter_products.
        self.search_bar.get_root_object().textChanged.connect(self.filter_products)
        top_bar_search_layout.addWidget(self.search_bar)
        layout.addLayout(top_bar_search_layout)

        # Create an instance of TagSelectorWidget.
        self.tag_selector = TagSelectorWidget()
        layout.addWidget(self.tag_selector)

        # Bottom bar: new tag button + OK/Cancel buttons.
        bottom_bar_layout = QVBoxLayout()
        self.add_tag_btn = QPushButton("Lisää uusi tagi")
        self.add_tag_btn.setObjectName("add_tag_button")
        # Connect the new tag button to our new functionality.
        self.add_tag_btn.clicked.connect(self._show_add_tag_page)
        bottom_bar_layout.addWidget(self.add_tag_btn)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        bottom_bar_layout.addLayout(btn_layout)
        layout.addLayout(bottom_bar_layout)

        # Connect the OK and Cancel buttons.
        self.ok_btn.clicked.connect(self._finish_selection)
        self.cancel_btn.clicked.connect(self._cancel_selection)

        # Populate the tag selector with tags.
        self.populate_tags()

        return layout

    @catch_errors_ui
    def _add_new_tag_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.new_tag_text_field = NormalTextField(
            text_field_id="new_tag_text_field",
            placeholder_text="Syötä uusi tagi..."
        )
        layout.addWidget(self.new_tag_text_field)
        self.description_label = QLabel(
            "Tagi on reseptin kategorisointia varten. Tagi voi olla esim. \"Kasvis\" tai \"Gluteeniton\"."
        )
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        btn_layout = QHBoxLayout()
        self.add_tag_btn = QPushButton("Lisää tagi")
        self.cancel_add_tag_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.add_tag_btn)
        btn_layout.addWidget(self.cancel_add_tag_btn)
        layout.addLayout(btn_layout)

        self.add_tag_btn.clicked.connect(self._add_tag)
        self.cancel_add_tag_btn.clicked.connect(self._show_select_tags_page)

        return layout

    @catch_errors_ui
    def _add_tag(self):
        new_tag = self.new_tag_text_field.get_text().strip()
        if not new_tag:
            # Inform the user that the tag cannot be empty.
            warning = WarningDialog("Tagi ei voi olla tyhjä.", self)
            warning.show()
            return  # Stop processing if the tag is empty
        if new_tag not in self.all_tags:
            self.all_tags.append(new_tag)
            self.all_tags.sort()
        if new_tag not in self.selected_tags:
            self.selected_tags.append(new_tag)
        self.populate_tags()
        self._show_select_tags_page()

    @catch_errors_ui
    def _show_select_tags_page(self):
        if self.main_page is None:
            self.main_page = QWidget()
            self.main_page.setLayout(self._select_tags_layout())
            self.stacked.addWidget(self.main_page)
        self.stacked.setCurrentWidget(self.main_page)

    @catch_errors_ui
    def _show_add_tag_page(self):
        if self.add_tag_page is None:
            self.add_tag_page = QWidget()
            self.add_tag_page.setLayout(self._add_new_tag_layout())
            self.stacked.addWidget(self.add_tag_page)
        self.stacked.setCurrentWidget(self.add_tag_page)

    @catch_errors_ui
    def populate_tags(self, filter_text=""):
        """
        Populate the QML model in TagSelectorWidget with all tags.
        Pre-check tags that are already selected.
        """
        root_obj = self.tag_selector.get_root_object()
        if root_obj is not None:
            # Clear any existing tags from the QML model.
            root_obj.clearTags()
            # Add each tag from all_tags.
            for tag in self.all_tags:
                is_checked = tag in self.selected_tags
                if filter_text == "" or filter_text in tag.lower():
                    root_obj.addTag(tag, is_checked)
        else:
            print("TagSelectorWidget root object not found.")

    @catch_errors_ui
    def filter_products(self, newText):
        """
        Called when the search bar text changes.
        Filters the tag list to only include items that contain the search text.
        """
        search_text = newText.lower().strip()
        self.populate_tags(filter_text=search_text)

    @catch_errors_ui
    def _finish_selection(self):
        """
        Retrieve the selected tags from the QML model, update stored selection,
        and emit the finished signal.
        """
        root_obj = self.tag_selector.get_root_object()
        if root_obj is not None:
            js_value = root_obj.getSelectedTags()
            # Convert the QJSValue to a native Python list.
            selected = js_value.toVariant()
            self.selected_tags = selected
            self.finished.emit(selected)
        else:
            self.finished.emit([])

    @catch_errors_ui
    def _cancel_selection(self):
        """
        Retrieve the current selection on cancel and emit it.
        """
        root_obj = self.tag_selector.get_root_object()
        if root_obj is not None:
            selected = root_obj.getSelectedTags().toVariant()
            self.selected_tags = selected
            print(f"Cancelled selection, tags: {selected}")
            self.finished.emit(selected)
        else:
            self.finished.emit([])
