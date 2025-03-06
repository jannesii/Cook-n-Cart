# File: reseptit_page.py

import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QFrame, QLineEdit
)
from PySide6.QtCore import QTimer

from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC
from widgets.add_recipe_widget import AddRecipeWidget
from widgets.recipe_detail_widget import RecipeDetailWidget
from widgets.edit_recipe_widget import EditRecipeWidget  # New dedicated edit widget

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

        self.recipes_dict = {}
        self.update_recipes_dict()

        main_layout = QVBoxLayout(self)

        # Create the QStackedWidget
        self.stacked = QStackedWidget()

        # Page 0: List view
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1: Detail view
        self.page_detail = RecipeDetailWidget()
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        # When the edit button is clicked in the detail view,
        # emit a signal with the current recipe.
        self.page_detail.edit_recipe_requested.connect(self.open_edit_recipe)
        self.page_detail.delete_recipe_requested.connect(self.handle_delete_recipe)

        # Page 2: Add recipe view (for creating new recipes)
        self.page_add_recipe = AddRecipeWidget(
            recipe_controller=RecipeController,
            product_controller=ProductController,
            parent=self
        )
        self.page_add_recipe.recipe_added.connect(self.on_recipe_added)
        self.page_add_recipe.cancel_btn.clicked.connect(self.back_to_list)

        # Page 3: Edit recipe view (separate widget for editing)
        self.page_edit_recipe = EditRecipeWidget(parent=self)
        self.page_edit_recipe.recipe_updated.connect(self.on_recipe_updated)
        self.page_edit_recipe.cancel_btn.clicked.connect(self.back_to_recipe_detail)
        # (Optionally, connect a cancel button in EditRecipeWidget to back_to_list)

        # Add pages to the stacked widget
        self.stacked.addWidget(self.page_list)         # index 0
        self.stacked.addWidget(self.page_detail)         # index 1
        self.stacked.addWidget(self.page_add_recipe)       # index 2
        self.stacked.addWidget(self.page_edit_recipe)      # index 3

        # Set default page to recipe list
        self.stacked.setCurrentIndex(0)
        main_layout.addWidget(self.stacked, 1)
        self.setLayout(main_layout)

    def _create_list_layout(self):
        """
        Creates the layout for the recipe list view (Page 0).
        """
        layout = QVBoxLayout()

        # Top bar: Title, search bar, and new recipe button
        top_bar_layout = QHBoxLayout()
        self.title_label = QLabel("Reseptit")
        self.title_label.setObjectName("top_bar_title_label")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae reseptejä")
        self.search_bar.textChanged.connect(self.filter_recipes)
        self.search_bar.setObjectName("top_bar_search_bar")

        self.new_btn = QPushButton("Uusi resepti")
        self.new_btn.setObjectName("top_bar_new_button")
        self.new_btn.clicked.connect(self.open_add_recipe_page)

        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_btn)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")
        layout.addWidget(top_bar_frame, 0)

        # Scroll area for the recipe list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1)

        self.populate_recipe_list()
        return layout

    def handle_delete_recipe(self, recipe):
        try:
            # Delete the recipe using the controller
            RecipeController.delete_recipe(recipe.id)
            # Optionally, show a confirmation message to the user.
            print("Recipe deleted successfully.")
            self.back_to_list()  # Return to the recipe list view
        except Exception as e:
            print(f"Error deleting recipe: {e}")


    def update_recipes_dict(self):
        """
        Fetches all recipes from the RecipeController and updates the local dictionary.
        """
        self.recipes_dict = RecipeController.get_all_recipes()

    def populate_recipe_list(self):
        # Clear current layout
        self.clear_layout(self.scroll_layout)
        # Sort recipes by name (case-insensitive)
        sorted_recipes = sorted(
            self.recipes_dict.values(),
            key=lambda r: r.name.lower()
        )
        for recipe in sorted_recipes:
            btn = QPushButton(f"{recipe.name}")
            btn.setObjectName("main_list_button")
            # Store the recipe object for later filtering
            btn.recipe = recipe
            # When clicked, display the recipe detail view
            btn.clicked.connect(lambda checked=False, r=recipe: self.display_recipe_detail(r))
            self.scroll_layout.addWidget(btn)
        self.scroll_layout.addStretch()


    def display_recipe_detail(self, recipe):
        """
        Loads the recipe into the detail view and switches to it.
        """
        self.page_detail.set_recipe(recipe)
        self.stacked.setCurrentIndex(1)
    
    def back_to_recipe_detail(self):
        # Switch back to the recipe detail view (index 1)
        self.stacked.setCurrentIndex(1)

    def open_add_recipe_page(self):
        """
        Opens the add recipe view and resets its fields.
        """
        self.page_add_recipe.setFieldsToDefaults()
        self.stacked.setCurrentIndex(2)

    def open_edit_recipe(self, recipe):
        """
        Opens the edit recipe view with the selected recipe prepopulated.
        """
        self.page_edit_recipe.set_recipe(recipe)
        self.stacked.setCurrentIndex(3)

    def back_to_list(self):
        """
        Returns to the recipe list view and refreshes the list.
        """
        self.update_recipes_dict()
        self.populate_recipe_list()
        self.stacked.setCurrentIndex(0)

    def on_recipe_added(self, recipe):
        """
        Called when a new recipe is added.
        """
        self.back_to_list()

    def on_recipe_updated(self, recipe):
        """
        Called when an edited recipe is updated.
        """
        self.back_to_list()

    def filter_recipes(self, text):
        search_text = text.lower()
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is None:
                continue
            # If the recipe attribute is present, check name and tags.
            recipe = getattr(widget, "recipe", None)
            if recipe:
                name_match = search_text in recipe.name.lower()
                tags_match = search_text in recipe.tags.lower() if recipe.tags else False
                if name_match or tags_match:
                    widget.show()
                else:
                    widget.hide()
            else:
                # Fallback: check the widget text (if for some reason recipe is not set)
                if search_text in widget.text().lower():
                    widget.show()
                else:
                    widget.hide()


    def clear_layout(self, layout):
        """
        Recursively clears all items from a layout.
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
