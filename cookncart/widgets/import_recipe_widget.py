# import_recipe_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from cookncart.controllers import RecipeController, ProductController

class ImportRecipeWidget(QWidget):
    # Signal emitted with a list of selected product dictionaries (each with id, quantity, unit)
    importCompleted = Signal(list)
    # Signal emitted when the user cancels the import action
    cancelImport = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create controller instances (or receive them as parameters)
        self.recipe_controller = RecipeController()
        self.product_controller = ProductController()
        self.selected_recipe = None

        self._init_ui()

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

    def _init_recipe_selection_page(self):
        layout = QVBoxLayout(self.page_recipes)
        # Top bar: title and search field
        top_bar = QHBoxLayout()
        title = QLabel("Valitse resepti")
        top_bar.addWidget(title)
        top_bar.addStretch()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Hae reseptejä")
        top_bar.addWidget(self.search_edit)
        layout.addLayout(top_bar)

        # Recipe list
        self.recipe_list_widget = QListWidget()
        layout.addWidget(self.recipe_list_widget)

        # Populate the list of recipes
        self._populate_recipe_list()

        # Connect search for filtering recipes
        self.search_edit.textChanged.connect(self._filter_recipes)
        # When a recipe is double-clicked, go to the ingredient selection page
        self.recipe_list_widget.clicked.connect(self._on_recipe_selected)

        # Cancel button at the bottom
        btn_layout = QHBoxLayout()
        self.cancel_btn_recipes = QPushButton("Peruuta")
        self.cancel_btn_recipes.clicked.connect(self._on_cancel)
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn_recipes)
        layout.addLayout(btn_layout)

    def _populate_recipe_list(self):
        self.recipe_list_widget.clear()
        recipes = self.recipe_controller.get_all_recipes()  # Assuming a dict {id: recipe}
        # Sort recipes by name (case-insensitive)
        sorted_recipes = sorted(recipes.values(), key=lambda r: r.name.lower())
        for recipe in sorted_recipes:
            item = QListWidgetItem(recipe.name)
            item.setData(Qt.UserRole, recipe)
            self.recipe_list_widget.addItem(item)

    def _filter_recipes(self, text):
        text = text.lower()
        for i in range(self.recipe_list_widget.count()):
            item = self.recipe_list_widget.item(i)
            recipe_name = item.text().lower()
            item.setHidden(text not in recipe_name)

    def _on_recipe_selected(self, item):
        recipe = item.data(Qt.UserRole)
        if recipe:
            self.selected_recipe = recipe
            self._populate_ingredient_list(recipe)
            self.stacked.setCurrentIndex(1)

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
        self.ingredient_list_widget = QListWidget()
        layout.addWidget(self.ingredient_list_widget)

        # Bottom buttons: Cancel and Import
        btn_layout = QHBoxLayout()
        self.cancel_btn_ingredients = QPushButton("Peruuta")
        self.cancel_btn_ingredients.clicked.connect(self._on_cancel_ingredients)
        btn_layout.addWidget(self.cancel_btn_ingredients)
        btn_layout.addStretch()
        self.import_btn = QPushButton("Tuo ostoslistaan")
        self.import_btn.clicked.connect(self._on_import)
        btn_layout.addWidget(self.import_btn)
        layout.addLayout(btn_layout)

    def _populate_ingredient_list(self, recipe):
        self.ingredient_list_widget.clear()
        # For each ingredient in the selected recipe, add a checkable list item.
        for ing in recipe.ingredients:
            # Use product controller to fetch product name
            product = self.product_controller.get_product_by_id(ing.product_id)
            product_name = product.name if product else f"Tuote {ing.product_id}"
            text = f"{product_name}: {ing.quantity} {ing.unit}"
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            # Store the ingredient data in the item
            item.setData(Qt.UserRole, ing)
            self.ingredient_list_widget.addItem(item)

    def _on_select_all(self):
        for i in range(self.ingredient_list_widget.count()):
            item = self.ingredient_list_widget.item(i)
            item.setCheckState(Qt.Checked)

    def _on_cancel_ingredients(self):
        # Go back to the recipe selection page
        self.stacked.setCurrentIndex(0)

    def _on_import(self):
        selected_products = []
        for i in range(self.ingredient_list_widget.count()):
            item = self.ingredient_list_widget.item(i)
            if item.checkState() == Qt.Checked:
                ing = item.data(Qt.UserRole)
                selected_products.append({
                    "id": ing.product_id,
                    "quantity": ing.quantity,
                    "unit": ing.unit
                })
        if selected_products:
            self.importCompleted.emit(selected_products)
        else:
            QMessageBox.warning(self, "Huom", "Et ole valinnut yhtään ainesosaa.")

    def _on_cancel(self):
        self.cancelImport.emit()
