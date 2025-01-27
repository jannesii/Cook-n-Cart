# add_recipe_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QCompleter, QMessageBox
)
from PySide6.QtCore import Qt, Signal

# Define your color constants
TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class AddRecipeWidget(QWidget):
    """
    Widget to add a new recipe. Includes:
      - name, instructions, tags fields
      - a button to open AddProductsWidget
      - Save and Cancel buttons
    Uses an internal QStackedWidget:
      Page 0: The main 'new recipe' form
      Page 1: The AddProductsWidget
    """

    # Define a signal that emits the newly added recipe
    recipe_added = Signal(object)

    def __init__(self, recipe_controller, product_controller, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        self.product_controller = product_controller

        # Keep track of selected products / ingredients
        self.selected_products = []

        # Set up the QStackedWidget to hold:
        #  - Page 0: "Recipe form"
        #  - Page 1: "AddProductsWidget"
        self.stacked = QStackedWidget(self)

        # Create page 0 (the recipe form)
        self.form_page = QWidget()
        self.form_page.setLayout(self._create_form_layout())

        # Create page 1 (the AddProductsWidget), define it after the form
        from add_products_widget import AddProductsWidget  # Ensure this import works correctly
        self.products_page = AddProductsWidget(
            product_controller=self.product_controller,
            parent=self
        )
        # Hook up "finished" signal from AddProductsWidget
        self.products_page.finished.connect(self.on_products_selected)

        # Add pages to the QStackedWidget
        self.stacked.addWidget(self.form_page)      # index 0
        self.stacked.addWidget(self.products_page)  # index 1

        # Set the layout for AddRecipeWidget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)

        self.setLayout(layout)

    def _create_form_layout(self):
        """
        Builds and returns the layout for the 'Add New Recipe' form (page 0).
        """
        layout = QVBoxLayout()

        # 1) Name
        name_label = QLabel("Nimi:")
        self.name_edit = QLineEdit()

        # 2) Instructions
        instructions_label = QLabel("Valmistusohjeet:")
        self.instructions_edit = QTextEdit()

        # 3) Tags (with an optional QCompleter)
        tags_label = QLabel("Tagit (pilkulla eroteltuna):")
        self.tags_edit = QLineEdit()

        # Fetch all tags and ensure uniqueness
        all_tags = self.recipe_controller.get_all_tags()
        unique_tags = sorted({tag for tag in all_tags if tag})  # Excludes None and empty strings
        tags_completer = QCompleter(unique_tags)
        tags_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.tags_edit.setCompleter(tags_completer)

        # 4) Add products button
        self.add_products_btn = QPushButton("+ Lisää tuotteita")
        self.add_products_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                margin-top: 8px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: #009ACD;
            }}
        """)
        self.add_products_btn.clicked.connect(self._open_products_page)

        # 5) Save and Cancel buttons
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Tallenna resepti")
        self.save_btn.setStyleSheet(
            f"background-color: {TURKOOSI}; color: black; font-weight: bold; padding: 5px 10px; border-radius: 5px;"
        )
        self.save_btn.clicked.connect(self._save_recipe)

        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setStyleSheet(
            f"background-color: {HARMAA}; color: black; font-weight: bold; padding: 5px 10px; border-radius: 5px;"
        )
        self.cancel_btn.clicked.connect(self._cancel_add_recipe)

        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)

        # Add widgets to the layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(instructions_label)
        layout.addWidget(self.instructions_edit)
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_edit)

        layout.addWidget(self.add_products_btn)
        layout.addLayout(buttons_layout)

        # Add stretch for spacing
        layout.addStretch()
        return layout

    def _open_products_page(self):
        """
        Switch from the form (page 0) to the AddProductsWidget (page 1).
        """
        # Pass the current selected products to the AddProductsWidget
        self.products_page.set_selected_products(self.selected_products)

        self.stacked.setCurrentIndex(1)

    def on_products_selected(self, selected_products):
        """
        Callback when AddProductsWidget finishes.
        `selected_products` is a list of Product objects.
        """
        self.selected_products = selected_products
        self.stacked.setCurrentIndex(0)

    def _save_recipe(self):
        """
        Gather data from the form, call recipe_controller.add_recipe(...) 
        and then emit the `recipe_added` signal.
        """
        name = self.name_edit.text().strip()
        instructions = self.instructions_edit.toPlainText().strip()
        tags = self.tags_edit.text().strip()

        # Validate mandatory fields
        if not name:
            self._show_error("Reseptin nimi on pakollinen.")
            return
        if not instructions:
            self._show_error("Valmistusohjeet ovat pakolliset.")
            return

        # Convert self.selected_products into the ingredients list structure
        ingredients = []
        for p in self.selected_products:
            # Ensure 'quantity' matches the RecipeIngredient field
            ingredients.append({
                "product_id": p.id,
                "quantity": 1.0  # Default quantity; consider adding a field to specify
                # "unit": "pcs"  # Removed as it's not part of RecipeIngredient
            })

        # Add the recipe using the controller
        try:
            new_recipe = self.recipe_controller.add_recipe(
                name=name,
                instructions=instructions,
                tags=tags,
                ingredients=ingredients
            )
        except Exception as e:
            self._show_error(f"Reseptin tallennus epäonnistui: {e}")
            return

        # Emit the recipe_added signal with the new recipe
        self.recipe_added.emit(new_recipe)

        # Clear fields after saving
        self._clear_fields()

        # Optionally, navigate back to the recipe list
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _cancel_add_recipe(self):
        """
        Handle the Cancel button click. Emit a signal or perform necessary actions.
        """
        # Optionally, emit a signal or notify the parent to switch views
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _clear_fields(self):
        """
        Clears all input fields and resets selected products.
        """
        self.name_edit.clear()
        self.instructions_edit.clear()
        self.tags_edit.clear()
        self.selected_products = []

    def _show_error(self, message):
        """
        Displays an error message to the user.
        Implemented using a QMessageBox.
        """
        QMessageBox.warning(self, "Virhe", message)

    def setFieldsToDefaults(self):
        """
        Resets the input fields to their default state.
        """
        self._clear_fields()
