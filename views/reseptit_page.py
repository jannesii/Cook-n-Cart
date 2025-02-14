# reseptit_page.py

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


TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

class ReseptitPage(QWidget):
    """
    Reseptit-sivu:
      - QStackedWidget with:
         Page 0: "Reseptilista" with "Hae reseptejä" and "Uusi resepti" at the top
         Page 1: Detailed recipe view (RecipeDetailWidget)
         Page 2: Add recipe view (AddRecipeWidget)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.recipes_dict = {}
        self.update_recipes_dict()

        main_layout = QVBoxLayout(self)

        # Create the QStackedWidget
        self.stacked = QStackedWidget()

        # Page 0 (list view)
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1 (detail view)
        self.page_detail = RecipeDetailWidget()
        # Hook the "Back" button in RecipeDetailWidget
        self.page_detail.back_btn.clicked.connect(self.back_to_list)
        # Connect the edit signal from the detail widget:
        self.page_detail.edit_recipe_requested.connect(self.open_edit_recipe)

        # Page 2 (add recipe view)
        self.page_add_recipe = AddRecipeWidget(
            recipe_controller=RecipeController,
            product_controller=ProductController,
            parent=self
        )
        # Connect signals from AddRecipeWidget to handle post-addition actions
        self.page_add_recipe.recipe_added.connect(self.on_recipe_added)
        self.page_add_recipe.cancel_btn.clicked.connect(self.back_to_list)

        # Add all pages to the QStackedWidget
        self.stacked.addWidget(self.page_list)         # index 0
        self.stacked.addWidget(self.page_detail)         # index 1
        self.stacked.addWidget(self.page_add_recipe)       # index 2

        # Start with the list page
        self.stacked.setCurrentIndex(0)

        main_layout.addWidget(self.stacked, 1)
        self.setLayout(main_layout)

    def _create_list_layout(self):
        """
        Creates and returns the layout for the "list" page (page_list).
        """
        layout = QVBoxLayout()

        # -- Yläpalkki (Top Bar) --
        top_bar_layout = QHBoxLayout()

        # Title Label
        self.title_label = QLabel("Reseptit")
        self.title_label.setObjectName("top_bar_title_label")

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae reseptejä")
        self.search_bar.textChanged.connect(self.filter_recipes)

        # New Recipe Button
        self.new_btn = QPushButton("Uusi resepti")
        self.new_btn.clicked.connect(self.open_add_recipe_page)

        # Styling for Search Bar
        self.search_bar.setObjectName("top_bar_search_bar")


        # Styling for New Recipe Button
        self.new_btn.setObjectName("top_bar_new_button")


        # Assemble Top Bar Layout
        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_btn)

        # Frame for Top Bar
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setObjectName("top_bar_frame")


        layout.addWidget(top_bar_frame, 0)

        # -- Scroll Area for Recipes --
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1)

        # Populate the recipe list
        self.populate_recipe_list()

        return layout

    def update_recipes_dict(self):
        """
        Fetch all recipes from the RecipeController and update the local dictionary.
        """
        self.recipes_dict = RecipeController.get_all_recipes()

    def populate_recipe_list(self):
        # Clear the current layout properly
        self.clear_layout(self.scroll_layout)
        
        # Sort recipes by name (case-insensitive)
        sorted_recipes = sorted(
            self.recipes_dict.values(),
            key=lambda r: r.name.lower()
        )

        # Add recipes to the layout
        for recipe in sorted_recipes:
            btn = QPushButton(f"{recipe.name}")
            btn.setObjectName("main_list_button")
            btn.clicked.connect(lambda checked=False, r=recipe: self.display_recipe_detail(r))
            self.scroll_layout.addWidget(btn)

        # Add stretch at the end
        self.scroll_layout.addStretch()


    def display_recipe_detail(self, recipe):
        """
        Fills in the detail page with the given recipe and switches the stacked widget.
        """
        self.page_detail.set_recipe(recipe)
        # Switch to page index 1 (detail view)
        self.stacked.setCurrentIndex(1)

    def open_add_recipe_page(self):
        """
        Opens the add recipe page and ensures the form is reset.
        """
        self.page_add_recipe.setFieldsToDefaults()
        self.stacked.setCurrentIndex(2)
    
    # In reseptit_page.py (inside the ReseptitPage class)

    def open_edit_recipe(self, recipe):
        self.page_add_recipe.setFieldsToRecipe(recipe)
        # Use QTimer.singleShot(0, ...) so that the UI can finish processing before switching pages.
        QTimer.singleShot(0, lambda: self.stacked.setCurrentIndex(2))


    def back_to_list(self):
        """
        Switches back to the recipe list page and refreshes the list.
        """
        self.update_recipes_dict()
        self.populate_recipe_list()
        self.stacked.setCurrentIndex(0)

    def on_recipe_added(self, recipe):
        """
        Slot that gets called when a new recipe is added.
        """
        # Refresh the recipe list to include the new recipe
        self.back_to_list()

    def filter_recipes(self, text):
        search_text = text.lower()
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i).widget()
            if item is None:
                continue  # Skip layout items without a widget (like stretches)
            if search_text in item.text().lower():
                item.show()
            else:
                item.hide()



    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
