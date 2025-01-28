# recipe_detail_widget.py

import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton,

)
from PySide6.QtCore import Qt, QStringListModel
from datetime import datetime

from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()




class RecipeDetailWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.recipe = None  # We'll store the current recipe here

        self.layout = QVBoxLayout(self)

        # placeholders
        self.name_label = QLabel()
        self.instructions_label = QLabel()
        self.tags_label = QLabel()
        self.ingredients_label = QLabel()
        self.created_at_label = QLabel()
        self.updated_at_label = QLabel()

        # Let text wrap
        for lbl in [
            self.name_label, self.instructions_label,
            self.tags_label, self.ingredients_label,
            self.created_at_label, self.updated_at_label
        ]:
            lbl.setWordWrap(True)
            self.layout.addWidget(lbl)

        # "Back" button
        self.back_btn = QPushButton("Takaisin")
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #009ACD;
            }}
        """)

        # This button will be wired up in ReseptitPage to switch pages
        self.layout.addWidget(self.back_btn, alignment=Qt.AlignRight)

    def set_recipe(self, recipe):
        """
        Update the labels to show the selected recipe details.
        """
        self.recipe = recipe
        if recipe:
            self.name_label.setText(f"<b>Nimi:</b> {recipe.name}")
            self.instructions_label.setText(
                f"<b>Valmistusohje:</b> {recipe.instructions}")
            self.tags_label.setText(f"<b>Tagit:</b> {recipe.tags}")
            self.ingredients_label.setText(
                f"<b>Ainesosat:</b> {recipe.ingredients}")
            self.created_at_label.setText(
                f"<b>Luotu:</b> {self.format_datetime_or_string(recipe.created_at)}")
            self.updated_at_label.setText(
                f"<b>Päivitetty:</b> {self.format_datetime_or_string(recipe.updated_at)}")
        else:
            # Clear fields if no recipe
            self.name_label.setText("")
            self.instructions_label.setText("")
            self.tags_label.setText("")
            self.ingredients_label.setText("")
            self.created_at_label.setText("")
            self.updated_at_label.setText("")
            
    def format_datetime_or_string(value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, str):
            # Optionally parse or just return the raw string
            return value
        else:
            return "N/A"


