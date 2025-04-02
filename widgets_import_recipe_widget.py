# import_recipe_widget.py

import functools
import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from root_controllers import RecipeController, ProductController
from qml import WarningDialog, ScrollViewWidget, MainSearchTextField, IngredientSelectorWidget

from error_handler import catch_errors_ui


class ImportRecipeWidget(QWidget):
    # Signal emitted with a list of selected product dictionaries (each with id, quantity, unit)
    importCompleted = Signal(list)
    # Signal emitted when the user cancels the import action
    cancelImport = Signal()

    @catch_errors_ui
    def __init__(self, parent=None, selected_products=[]):
        super().__init__(parent)
        # Create controller instances (or receive them as parameters)
        self.recipe_controller = RecipeController()
        self.product_controller = ProductController()
        self.selected_recipe = None
        self.selected_products = selected_products
        self._init_ui()

    @catch_errors_ui
    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        # A QStackedWidget to handle two pages: recipe selection and ingredient selection.
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)
        # Page 0: Recipe selection page
        self.page_recipes = QWidget()
        self._init_recipe_selection_page()
        self.stacked.addWidget(self.page_recipes)
        # Page 1: Ingredient selection page
        self.page_ingredients = QWidget()
        self._init_ingredient_selection_page()
        self.stacked.addWidget(self.page_ingredients)
        self.setLayout(main_layout)

    @catch_errors_ui
    def _init_recipe_selection_page(self):
        layout = QVBoxLayout(self.page_recipes)
        # Top bar: title and search field
        top_bar = QHBoxLayout()
        title = QLabel("Valitse resepti")
        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar_search_layout = QHBoxLayout()
        self.search_edit = MainSearchTextField(
            text_field_id="recipe_search_bar", placeholder_text="Hae reseptejä...", parent=self
        )
        top_bar_search_layout.addWidget(self.search_edit)
        layout.addLayout(top_bar)
        layout.addLayout(top_bar_search_layout)
        # Recipe list
        self.recipe_list_widget = ScrollViewWidget(
            parent=self, main_height=300)
        layout.addWidget(self.recipe_list_widget)
        # Populate the list of recipes
        self._populate_recipe_list()
        # Connect search for filtering recipes
        self.search_edit.get_root_object().textChanged.connect(self._filter_recipes)
        # When a recipe is clicked, go to the ingredient selection page
        self.recipe_list_widget.connect_item_clicked(self._on_recipe_selected)
        # Cancel button at the bottom
        btn_layout = QHBoxLayout()
        self.cancel_btn_recipes = QPushButton("Peruuta")
        self.cancel_btn_recipes.clicked.connect(self._on_cancel)
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn_recipes)
        layout.addLayout(btn_layout)

    @catch_errors_ui
    def _populate_recipe_list(self, filter_text=""):
        self.recipe_list_widget.clear_items()
        # Assuming a dict {id: recipe}
        recipes = self.recipe_controller.get_all_recipes()
        # Sort recipes by name (case-insensitive)
        sorted_recipes = sorted(recipes.values(), key=lambda r: r.name.lower())
        for recipe in sorted_recipes:
            if filter_text == "" or filter_text in recipe.name.lower():
                self.recipe_list_widget.add_item(recipe.name, recipe.id)

    @catch_errors_ui
    def _filter_recipes(self, text):
        text = text.lower().strip()
        self._populate_recipe_list(filter_text=text)

    @catch_errors_ui
    def _on_recipe_selected(self, id):
        recipe = self.recipe_controller.get_recipe_by_id(id)
        if recipe:
            self.selected_recipe = recipe
            self._populate_ingredient_list(recipe)
            self.stacked.setCurrentIndex(1)

    @catch_errors_ui
    def _init_ingredient_selection_page(self):
        layout = QVBoxLayout(self.page_ingredients)
        # Top bar: title and "Select All" button
        top_bar = QHBoxLayout()
        self.ing_title_label = QLabel("Valitse ainesosat")
        top_bar.addWidget(self.ing_title_label)
        top_bar.addStretch()
        self.select_all_btn = QPushButton("Valitse kaikki")
        self.select_all_btn.clicked.connect(self._on_select_all)
        top_bar.addWidget(self.select_all_btn)
        layout.addLayout(top_bar)
        # Ingredient list with checkboxes
        self.ingredient_list_widget = IngredientSelectorWidget(parent=self)
        layout.addWidget(self.ingredient_list_widget)
        # Bottom buttons: Cancel and Import
        btn_layout = QHBoxLayout()
        self.cancel_btn_ingredients = QPushButton("Peruuta")
        self.cancel_btn_ingredients.clicked.connect(
            self._on_cancel_ingredients)
        btn_layout.addWidget(self.cancel_btn_ingredients)
        btn_layout.addStretch()
        self.import_btn = QPushButton("Tuo ostoslistaan")
        self.import_btn.clicked.connect(self._on_import)
        btn_layout.addWidget(self.import_btn)
        layout.addLayout(btn_layout)

    @catch_errors_ui
    def _populate_ingredient_list(self, recipe):
        self.ingredient_list_widget.clear_tags()
        # For each ingredient in the selected recipe, add a checkable list item.
        for ing in recipe.ingredients:
            # Use product controller to fetch product name.
            product = self.product_controller.get_product_by_id(ing.product_id)
            product_name = product.name if product else f"Tuote {ing.product_id}"
            text = f"{product_name}: {ing.quantity} {ing.unit}"
            self.ingredient_list_widget.get_root_object().addTag(
                text, False, ing.quantity, ing.unit, ing.product_id)

    @catch_errors_ui
    def _on_select_all(self):
        self.ingredient_list_widget.check_all_tags()

    @catch_errors_ui
    def _on_cancel_ingredients(self):
        # Go back to the recipe selection page.
        self.stacked.setCurrentIndex(0)

    @catch_errors_ui
    def _on_import(self):
        selected_products = self.ingredient_list_widget.get_selected_tags().toVariant()
        for product in selected_products:
            self.selected_products.append(product)
        if selected_products:
            self.importCompleted.emit(self.selected_products)
        else:
            self._show_error("Et ole valinnut yhtään ainesosaa.")

    @catch_errors_ui
    def _on_cancel(self):
        self.cancelImport.emit()

    @catch_errors_ui
    def _show_error(self, message):
        warning = WarningDialog(f"Virhe: {message}", self)
        warning.show()
