# File: edit_recipe_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QListWidget, QListWidgetItem, QTextEdit
)
from PySide6.QtCore import Signal
from root_controllers import RecipeController, ProductController

class EditRecipeWidget(QWidget):
    # Signal that emits the updated recipe object after saving
    recipe_updated = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recipe = None
        self.recipe_controller = RecipeController()
        self.product_controller = ProductController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Recipe Name as QLineEdit
        self.name_edit = QLineEdit()
        layout.addWidget(QLabel("Nimi:"))
        layout.addWidget(self.name_edit)

        # Recipe Instructions as QTextEdit (supports newlines)
        self.instructions_edit = QTextEdit()
        self.instructions_edit.setMinimumHeight(100)
        layout.addWidget(QLabel("Ohjeet:"))
        layout.addWidget(self.instructions_edit)

        # Tags – allow editing directly
        self.tags_edit = QLineEdit()
        layout.addWidget(QLabel("Tagit (pilkulla eroteltuna):"))
        layout.addWidget(self.tags_edit)

        # Ingredients list – each row will have product name (left-aligned)
        # and quantity/unit widgets (right-aligned)
        layout.addWidget(QLabel("Ainesosat:"))
        self.ingredients_list = QListWidget()
        layout.addWidget(self.ingredients_list)

        # Save and Cancel buttons
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Tallenna muutokset")
        self.cancel_btn = QPushButton("Peruuta")
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)

        self.save_btn.clicked.connect(self._save_recipe)

    def set_recipe(self, recipe):
        """Prepopulate the widget with the recipe to edit."""
        self.recipe = recipe
        self.name_edit.setText(recipe.name)
        self.instructions_edit.setPlainText(recipe.instructions)
        self.tags_edit.setText(recipe.tags)
        self._populate_ingredients(recipe.ingredients)

    def _populate_ingredients(self, ingredients):
        """Create a list entry for each ingredient with editable quantity and unit."""
        self.ingredients_list.clear()
        for ingredient in ingredients:
            # Create a container widget for this ingredient row
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(5, 5, 5, 5)
            row_layout.setSpacing(10)
            
            # Label for product name (aligned left)
            product = self.product_controller.get_product_by_id(ingredient.product_id)
            product_name = product.name if product else f"Tuote {ingredient.product_id}"
            product_label = QLabel(product_name)
            product_label.setStyleSheet("font-weight: bold;")
            row_layout.addWidget(product_label)
            
            # Add a stretch so that the remaining widgets are pushed to the right
            row_layout.addStretch()
            
            # Quantity label and edit (aligned right)
            qty_label = QLabel("Qty:")
            row_layout.addWidget(qty_label)
            
            qty_edit = QLineEdit(str(ingredient.quantity))
            qty_edit.setFixedWidth(50)
            row_layout.addWidget(qty_edit)
            
            # Unit dropdown (aligned right)
            unit_combo = QComboBox()
            unit_combo.addItems(["kpl", "g", "kg", "ml", "l", "oz", "lb"])
            index = unit_combo.findText(ingredient.unit)
            if index != -1:
                unit_combo.setCurrentIndex(index)
            row_layout.addWidget(unit_combo)
            
            # Add a subtle bottom border for a modern look
            row_widget.setStyleSheet("border-bottom: 1px solid #ccc;")
            
            # Store references in the widget for later retrieval
            row_widget.qty_edit = qty_edit
            row_widget.unit_combo = unit_combo
            row_widget.ingredient = ingredient  # original ingredient object
            
            list_item = QListWidgetItem()
            list_item.setSizeHint(row_widget.sizeHint())
            self.ingredients_list.addItem(list_item)
            self.ingredients_list.setItemWidget(list_item, row_widget)

    def _save_recipe(self):
        # Gather updated values
        name = self.name_edit.text().strip()
        instructions = self.instructions_edit.toPlainText().strip()
        tags = self.tags_edit.text().strip()

        updated_ingredients = []
        for i in range(self.ingredients_list.count()):
            item = self.ingredients_list.item(i)
            row_widget = self.ingredients_list.itemWidget(item)
            if row_widget:
                try:
                    quantity = float(row_widget.qty_edit.text())
                except ValueError:
                    # Use the old quantity if conversion fails
                    quantity = row_widget.ingredient.quantity
                unit = row_widget.unit_combo.currentText()
                updated_ingredients.append({
                    "product_id": row_widget.ingredient.product_id,
                    "quantity": quantity,
                    "unit": unit
                })

        # Use the recipe controller to update the recipe
        try:
            updated_recipe = self.recipe_controller.update_recipe(
                recipe_id=self.recipe.id,
                name=name,
                instructions=instructions,
                tags=tags,
                ingredients=updated_ingredients
            )
            self.recipe_updated.emit(updated_recipe)
        except Exception as e:
            # Optionally, display an error message to the user
            print(f"Error updating recipe: {e}")
