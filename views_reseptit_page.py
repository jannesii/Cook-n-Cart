# File: reseptit_page.py

import functools
import logging
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QFrame, QLineEdit, QMessageBox
)
from PySide6.QtCore import QTimer
from root_controllers import ProductController as PC
from root_controllers import ShoppingListController as SLC
from root_controllers import RecipeController as RC
from widgets_add_recipe_widget import AddRecipeWidget
from widgets_recipe_detail_widget import RecipeDetailWidget
from qml import MainSearchTextField, ScrollViewWidget
from error_handler import catch_errors_ui

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()


class ReseptitPage(QWidget):
    """
    Reseptit-sivu:
      - QStackedWidget with four pages:
         Page 0: Recipe list view with search and a "Uusi resepti" button.
         Page 1: Recipe detail view (RecipeDetailWidget).
         Page 2: Add recipe view (AddRecipeWidget).
         Page 3: Edit recipe view (EditRecipeWidget) – a separate widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.recipes_dict = {}
        self.update_recipes_dict()

        main_layout = QVBoxLayout(self)

        # Create the QStackedWidget
        self.stacked = QStackedWidget()

        # Page 0: List view
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        self.page_detail = None
        self.page_add_recipe = None
        self.page_edit_recipe = None

        # Add pages to the stacked widget
        self.stacked.addWidget(self.page_list)         # index 0

        # Set default page to recipe list
        self.stacked.setCurrentWidget(self.page_list)
        main_layout.addWidget(self.stacked, 1)
        self.setLayout(main_layout)

    @catch_errors_ui
    def _create_list_layout(self):
        """
        Creates the layout for the recipe list view (Page 0).
        """
        layout = QVBoxLayout()

        # Top bar: Title, search bar, and new recipe button
        top_bar_layout = QHBoxLayout()
        self.title_label = QLabel("Reseptit")
        self.title_label.setObjectName("top_bar_title_label")

        top_bar_search_layout = QHBoxLayout()
        self.search_bar = MainSearchTextField(
            text_field_id="top_bar_search_bar", placeholder_text="Hae reseptejä")
        top_bar_search_layout.addWidget(self.search_bar)

        self.new_btn = QPushButton("Uusi resepti")
        self.new_btn.setObjectName("top_bar_new_button")
        self.new_btn.clicked.connect(self.open_add_recipe_page)

        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.new_btn)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")
        layout.addWidget(top_bar_frame, 0)
        layout.addLayout(top_bar_search_layout)

        # Scroll area for the recipe list
        self.scroll_area = ScrollViewWidget(list_model_name="recipe_list")
        layout.addWidget(self.scroll_area, 1)

        # Connect the search bar's textChanged signal to filter_recipes.
        self.search_bar.get_root_object().textChanged.connect(self.filter_recipes)
        # Connect the QML signal for item clicks.
        self.scroll_area.connect_item_clicked(self.handle_item_click)

        self.populate_recipe_list()
        return layout

    @catch_errors_ui
    def handle_delete_recipe(self, recipe):
        # Delete the recipe using the controller
        RecipeController.delete_recipe(recipe.id)
        print("Recipe deleted successfully.")
        self.back_to_list()  # Return to the recipe list view

    @catch_errors_ui
    def update_recipes_dict(self):
        """
        Fetches all recipes from the RecipeController and updates the local dictionary.
        """
        self.recipes_dict = RecipeController.get_all_recipes()

    @catch_errors_ui
    def populate_recipe_list(self, filter_text=""):
        # Clear current layout
        self.scroll_area.clear_items()
        # Sort recipes by name (case-insensitive)
        sorted_recipes = sorted(
            self.recipes_dict.values(),
            key=lambda r: r.name.lower()
        )
        for recipe in sorted_recipes:
            if filter_text == "" or filter_text in recipe.name.lower():
                self.scroll_area.add_item(recipe.name, recipe.id)

    @catch_errors_ui
    def display_recipe_detail(self, recipe):
        """
        Loads the recipe into the detail view and switches to it.
        """
        self.page_detail = RecipeDetailWidget()
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        self.page_detail.edit_recipe_requested.connect(self.open_edit_recipe)
        self.page_detail.delete_recipe_requested.connect(
            self.handle_delete_recipe)
        self.stacked.addWidget(self.page_detail)         # index 1
        self.page_detail.set_recipe(recipe)
        self.stacked.setCurrentWidget(self.page_detail)
        self.parent.hide_buttons()

    @catch_errors_ui
    def back_to_recipe_detail(self):
        # Switch back to the recipe detail view (index 1)
        self.stacked.setCurrentWidget(self.page_detail)

    @catch_errors_ui
    def open_add_recipe_page(self):
        """
        Opens the add recipe view and resets its fields.
        """
        self.page_add_recipe = AddRecipeWidget(
            recipe_controller=RecipeController,
            product_controller=ProductController,
            parent=self
        )
        self.page_add_recipe.recipe_saved.connect(self.on_recipe_added)
        self.page_add_recipe.cancel_btn.clicked.connect(self.back_to_list)
        self.stacked.addWidget(self.page_add_recipe)       # index 2
        self.stacked.setCurrentWidget(self.page_add_recipe)
        self.parent.hide_buttons()

    @catch_errors_ui
    def open_edit_recipe(self, recipe):
        """
        Opens the edit recipe view with the selected recipe prepopulated.
        """
        self.page_edit_recipe = AddRecipeWidget(
            recipe_controller=RecipeController,
            product_controller=ProductController,
            parent=self
        )
        self.page_edit_recipe.recipe_saved.connect(self.on_recipe_updated)
        self.page_edit_recipe.cancel_btn.clicked.connect(
            self.back_to_recipe_detail)
        self.stacked.addWidget(self.page_edit_recipe)      # index 3
        self.page_edit_recipe.set_recipe(recipe)
        self.stacked.setCurrentWidget(self.page_edit_recipe)
        self.parent.hide_buttons()

    @catch_errors_ui
    def back_to_list(self):
        """
        Returns to the recipe list view and refreshes the list.
        """
        self.update_recipes_dict()
        self.populate_recipe_list()
        self.stacked.setCurrentWidget(self.page_list)
        self.parent.show_buttons()

        # Remove the detail and add recipe pages from the stack
        if self.page_detail:
            print("Removing page_detail")
            self.stacked.removeWidget(self.page_detail)
            self.page_detail.deleteLater()
            del self.page_detail
            self.page_detail = None

        if self.page_add_recipe:
            print("Removing page_add_recipe")
            self.stacked.removeWidget(self.page_add_recipe)
            self.page_add_recipe.deleteLater()
            del self.page_add_recipe
            self.page_add_recipe = None

        if self.page_edit_recipe:
            print("Removing page_edit_recipe")
            self.stacked.removeWidget(self.page_edit_recipe)
            self.page_edit_recipe.deleteLater()
            del self.page_edit_recipe
            self.page_edit_recipe = None

    @catch_errors_ui
    def on_recipe_added(self, recipe):
        self.back_to_list()

    @catch_errors_ui
    def on_recipe_updated(self, recipe):
        self.back_to_list()

    @catch_errors_ui
    def filter_recipes(self, newtext):
        search_text = newtext.lower().strip()
        self.populate_recipe_list(filter_text=search_text)

    @catch_errors_ui
    def handle_item_click(self, recipe_id):
        # Fetch the recipe details using the ID.
        recipe = RecipeController.get_recipe_by_id(recipe_id)
        if recipe:
            self.display_recipe_detail(recipe)

    @catch_errors_ui
    def clear_layout(self, layout):
        """
        Recursively clears all items from a layout.
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
