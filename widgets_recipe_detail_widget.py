# File: recipe_detail_widget.py --------------------------------------------------------------------

import functools
import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from root_controllers import RecipeController, ProductController

from error_handler import catch_errors_ui, show_error_toast

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class RecipeDetailWidget(QWidget):
    # Define signals for edit and deletion.
    edit_recipe_requested = Signal(object)
    delete_recipe_requested = Signal(object)

    @catch_errors_ui
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recipe_controller = RecipeController()
        self.product_controller = ProductController()
        self.recipe = None  # Currently displayed recipe

        # Use a QStackedWidget to hold the detail view (and optionally other pages)
        self.stacked = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked)
        self.setLayout(main_layout)

        # --- Detail Page ---
        self.detail_page = QWidget()
        detail_layout = QVBoxLayout(self.detail_page)
        self.name_label = QLabel()
        self.instructions_label = QLabel()
        self.tags_label = QLabel()
        self.ingredients_label = QLabel()
        for lbl in [self.name_label, self.instructions_label,
                    self.tags_label, self.ingredients_label]:
            lbl.setWordWrap(True)
            detail_layout.addWidget(lbl)

        # Buttons: Edit, Delete, Back
        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Muokkaa reseptiä")
        self.delete_btn = QPushButton("Poista resepti")
        self.delete_btn.setObjectName("delete_button")
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        self.back_btn = QPushButton("Takaisin")
        btn_layout.addWidget(self.back_btn)
        detail_layout.addLayout(btn_layout)
        self.stacked.addWidget(self.detail_page)  # index 0

        # --- Signal Connections ---
        self.edit_btn.clicked.connect(self.switch_to_edit_view)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        # (Assume back_btn is handled by the parent view.)

    @catch_errors_ui
    def set_recipe(self, recipe):
        """Prepopulates the detail view with the recipe data."""
        self.recipe = recipe
        if recipe:
            self.name_label.setText(f"<b>Nimi:</b> {recipe.name}")
            instructions_formatted = recipe.instructions.replace("\n", "<br>")
            self.instructions_label.setText(
                f"<b>Ohjeet:</b><br>{instructions_formatted}")
            self.tags_label.setText(f"<b>Tagit:</b> {recipe.tags}")
            ingredients_text = ""
            for ingredient in recipe.ingredients:
                product = self.product_controller.get_product_by_id(
                    ingredient.product_id)
                product_name = product.name if product else f"Tuote {ingredient.product_id}"
                quantity_str = f"{ingredient.quantity:g}"
                ingredients_text += f"{product_name}: {quantity_str} {ingredient.unit}<br>"
            self.ingredients_label.setText(ingredients_text)
        else:
            self.name_label.setText("Reseptiä ei löytynyt")
            self.instructions_label.clear()
            self.tags_label.clear()
            self.ingredients_label.clear()

    @catch_errors_ui
    def switch_to_edit_view(self):
        """
        Emits the edit_recipe_requested signal with the current recipe.
        The parent view should have connected this signal and will then open the edit view.
        """
        if self.recipe:
            self.edit_recipe_requested.emit(self.recipe)
        else:
            self._show_error("Ei reseptiä muokattavaksi.")

    @catch_errors_ui
    def on_delete_clicked(self):
        """Emits the delete_recipe_requested signal with the current recipe."""
        if self.recipe:
            self.delete_recipe_requested.emit(self.recipe)

    @catch_errors_ui
    def _show_error(self, message):
        show_error_toast(self, message, pos="top")
