# add_recipe_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QCompleter
)
from PySide6.QtCore import Qt, QStringListModel

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class AddRecipeWidget(QWidget):
    """
    Widget to add a new recipe. Includes:
      - name, instructions, tags fields
      - a button to open AddProductsWidget
      - a Save and Cancel button
    Uses an internal QStackedWidget:
      Page 0: The main 'new recipe' form
      Page 1: The AddProductsWidget
    """

    def __init__(self, recipe_controller, product_controller, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        self.product_controller = product_controller

        # Keep track of selected products / ingredients
        # (In a real app, store them as a list of {product_id, quantity, etc.})
        self.selected_products = []

        # Set up the QStackedWidget to hold:
        #  - Page 0: "Recipe form"
        #  - Page 1: "AddProductsWidget"
        self.stacked = QStackedWidget(self)

        # Create page 0 (the recipe form)
        self.form_page = QWidget()
        self.form_page.setLayout(self._create_form_layout())

        # Create page 1 (the AddProductsWidget), but define it *after* we have the form
        # We'll connect it so when user is done picking products, we come back to the form
        from add_products_widget import AddProductsWidget
        self.products_page = AddProductsWidget(
            product_controller=self.product_controller,
            parent=self
        )
        # Hook up "finished" signal from AddProductsWidget
        self.products_page.finished.connect(self.on_products_selected)

        self.stacked.addWidget(self.form_page)      # index 0
        self.stacked.addWidget(self.products_page)  # index 1

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)

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

        # If you want an autocomplete for tags:
        # e.g. ["vegan", "pasta", ...]
        all_tags = self.recipe_controller.get_all_tags()
        tags_completer = QCompleter(all_tags)
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
            }}
        """)
        self.add_products_btn.clicked.connect(self._open_products_page)

        # 5) Save and Cancel
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Tallenna resepti")
        self.save_btn.setStyleSheet(
            f"background-color: {TURKOOSI}; font-weight: bold;")
        self.save_btn.clicked.connect(self._save_recipe)

        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setStyleSheet(
            f"background-color: {HARMAA}; font-weight: bold;")


        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)

        # Add widgets to layout
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(instructions_label)
        layout.addWidget(self.instructions_edit)
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_edit)

        layout.addWidget(self.add_products_btn)
        layout.addLayout(buttons_layout)

        # Some spacing
        layout.addStretch()
        return layout

    def _open_products_page(self):
        """
        Switch from the form (page 0) to the AddProductsWidget (page 1).
        """
        # We can pass the current selected products to the AddProductsWidget if we want:
        self.products_page.set_selected_products(self.selected_products)

        self.stacked.setCurrentIndex(1)

    def on_products_selected(self, selected_products):
        """
        Callback when AddProductsWidget finishes.
        `selected_products` is whatever AddProductsWidget returns
        (e.g. list of (product_id, product_name, quantity)).
        """
        self.selected_products = selected_products
        self.stacked.setCurrentIndex(0)

    def _save_recipe(self):
        """
        Gather data from the form, call recipe_controller.add_recipe(...) 
        and then presumably go back to the main recipe list.
        """
        name = self.name_edit.text().strip()
        instructions = self.instructions_edit.toPlainText().strip()
        tags = self.tags_edit.text().strip()

        # Convert self.selected_products into the ingredients list structure
        # For example, we might do:
        # ingredients = [{"product_id": p.id, "amount": 1.0, "unit": "pcs"} for p in self.selected_products]
        # or whatever your code expects. We'll keep it simple:
        ingredients = []
        for p in self.selected_products:
            # p might be a Product object, or a dict. Adjust as needed.
            ingredients.append({
                "product_id": p.id,
                "amount": 1.0,
                "unit": "pcs"
            })

        self.recipe_controller.add_recipe(
            name=name,
            instructions=instructions,
            tags=tags,
            ingredients=ingredients
        )

        # Possibly clear fields if you want
        self._clear_fields()

        # Then go back to the recipe list. Usually you'd do:
        # self.parent().back_to_list() or emit a signal. For example:
        if hasattr(self.parent(), "back_to_list"):
            # If your ReseptitPage has a method like that.
            self.parent().back_to_list()


    def _clear_fields(self):
        self.name_edit.clear()
        self.instructions_edit.clear()
        self.tags_edit.clear()
        self.selected_products = []

    def setFieldsToDefaults(self):
        """
        You might call this before showing the page, if you want
        to ensure all fields start blank.
        """
        self._clear_fields()
