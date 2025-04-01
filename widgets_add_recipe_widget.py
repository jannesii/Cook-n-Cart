from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QCompleter
)
from PySide6.QtCore import Qt, Signal, QTimer

from widgets_add_tags_widget import AddTagsWidget
from widgets_add_products_widget import AddProductsWidget
from qml import NormalTextField, TallTextField, WarningDialog

TURKOOSI = "#00B0F0"
HARMAA = "#808080"


class AddRecipeWidget(QWidget):
    """
    Widget for adding or editing a recipe. It contains:
      - Name and instructions fields.
      - A button to add products (using AddProductsWidget).
      - A button to select tags (which opens AddTagsWidget).
      - Save and Cancel buttons.
      
    Internally, it uses a QStackedWidget with:
      Page 0: The recipe form.
      Page 1: The products selection widget.
      Page 2: The tags selection widget.
      
    To edit an existing recipe, call set_recipe(recipe) before showing the widget.
    """

    # Signal emitted after the recipe is saved (added or updated)
    recipe_saved = Signal(object)

    def __init__(self, recipe_controller, product_controller, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        self.product_controller = product_controller

        # Store selected products and tags
        self.selected_products = []
        self.selected_tags = []

        # current_recipe is None when adding a new recipe;
        # if set, then the widget is in edit mode.
        self.current_recipe = None

        # QStackedWidget settings:
        # Page 0: recipe form
        # Page 1: product selection (AddProductsWidget)
        # Page 2: tag selection (AddTagsWidget)
        self.stacked = QStackedWidget(self)

        # Page 0: Recipe form
        self.form_page = QWidget()
        self.form_page.setLayout(self._create_form_layout())
        self.stacked.addWidget(self.form_page)  # index 0

        # Pages for products and tags will be created as needed.
        self.products_page = None
        self.tags_page = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self._open_form_page()

    def _create_form_layout(self):
        layout = QVBoxLayout()

        # 1) Name
        name_label = QLabel("Nimi:")
        self.name_edit = NormalTextField(
            text_field_id="name_edit",
            placeholder_text="Syötä reseptin nimi"
        )
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # 2) Instructions
        instructions_label = QLabel("Valmistusohjeet:")
        self.instructions_edit = TallTextField(
            text_field_id="instructions_edit",
            placeholder_text="Syötä valmistusohjeet"
        )
        layout.addWidget(instructions_label)
        layout.addWidget(self.instructions_edit)

        # 3) Tags selection: show current tags and a button to edit them.
        tags_label = QLabel("Tagit:")
        self.tags_display_label = QLabel()
        if self.selected_tags:
            self.tags_display_label.setText(", ".join(self.selected_tags))
        else:
            self.tags_display_label.setText("Ei valittuja tageja")
        self.select_tags_btn = QPushButton("Valitse tageja")
        self.select_tags_btn.clicked.connect(self._open_tags_page)
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_display_label)
        layout.addWidget(self.select_tags_btn)

        # 4) Products selection: button opens product selection widget.
        self.add_products_btn = QPushButton("+ Lisää tuotteita")
        self.add_products_btn.clicked.connect(self._open_products_page)
        layout.addWidget(self.add_products_btn)

        # 5) Save and Cancel buttons
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Tallenna resepti")
        self.save_btn.clicked.connect(self._save_recipe)
        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setObjectName("gray_button")
        self.cancel_btn.clicked.connect(self._cancel_recipe)
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)

        layout.addStretch()
        return layout

    def _open_form_page(self):
        """Switch to the form (Page 0)."""
        self.stacked.setCurrentIndex(0)

    def _open_products_page(self):
        """Opens the products selection widget."""
        self.products_page = AddProductsWidget(
            parent=self, selected_products=self.selected_products
        )
        self.products_page.finished.connect(self.on_products_selected)
        self.stacked.addWidget(self.products_page)  # index 1
        self.stacked.setCurrentWidget(self.products_page)

    def _open_tags_page(self):
        """Opens the tags selection widget."""
        self.tags_page = AddTagsWidget(
            recipe_controller=self.recipe_controller,
            selected_tags=self.selected_tags,
            parent=self
        )
        self.tags_page.finished.connect(self.on_tags_selected)
        self.stacked.addWidget(self.tags_page)  # index 2
        self.stacked.setCurrentWidget(self.tags_page)

    def on_products_selected(self, selected_products):
        if selected_products:
            print(f"Selected products: {selected_products}")
            self.selected_products = selected_products
        else:
            print("Ei valittuja tuotteita")
            self.selected_products = []
        self._open_form_page()

    def on_tags_selected(self, selected_tags):
        if selected_tags:
            self.selected_tags = selected_tags
            print(f"Selected tags: {selected_tags}")
            self.tags_display_label.setText(", ".join(selected_tags))
        else:
            print("Ei valittuja tageja")
            self.tags_display_label.setText("Ei valittuja tageja")
        self._open_form_page()

    def set_recipe(self, recipe):
        """
        Puts the widget into edit mode by prepopulating the fields with the given recipe.
        Also sets self.current_recipe so that _save_recipe() updates rather than adds.
        """
        self.current_recipe = recipe
        # Prepopulate text fields with the recipe data.
        self.name_edit.set_text(recipe.name)
        self.instructions_edit.set_text(recipe.instructions)
        # Assume recipe.tags is a comma-separated string.
        if recipe.tags:
            tags_list = [tag.strip() for tag in recipe.tags.split(",") if tag.strip()]
        else:
            tags_list = []
        self.selected_tags = tags_list
        self.tags_display_label.setText(", ".join(tags_list))
        # For ingredients/products, you might want to prepopulate self.selected_products.
        # This depends on your data structure; here we assume each ingredient contains
        # at least 'product_id', 'quantity', and 'unit'.
        self.selected_products = []
        for ingredient in recipe.ingredients:
            self.selected_products.append({
                "id": ingredient.product_id,
                "quantity": ingredient.quantity,
                "unit": ingredient.unit
            })

    def _save_recipe(self):
        name = self.name_edit.get_text().strip()
        instructions = self.instructions_edit.get_text().strip()
        tags = ", ".join(self.selected_tags)

        if not name:
            self._show_error("Reseptin nimi on pakollinen.")
            return
        if not instructions:
            self._show_error("Valmistusohjeet ovat pakolliset.")
            return

        # Validate selected products
        for p in self.selected_products:
            try:
                quantity = float(p.get("quantity", 0))
            except ValueError:
                self._show_error("Ainesosan määrä ei ole kelvollinen luku.")
                return
            if quantity <= 0:
                self._show_error(f"Ainesosan määrä tuotteelle '{p.get('name', '')}' täytyy olla suurempi kuin 0.")
                return
            if not p.get("unit"):
                self._show_error("Valitse ainesosalle yksikkö.")
                return

        # Prepare ingredients list from selected products
        ingredients = []
        for p in self.selected_products:
            if isinstance(p, dict):
                product_id = p.get("id")
                quantity = p.get("quantity", 1.0)
                unit = p.get("unit", "")
            else:
                product_id = p.id
                quantity = getattr(p, "quantity", 1.0)
                unit = getattr(p, "unit", "")
            ingredients.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit": unit
            })

        try:
            if self.current_recipe is not None:
                # Update the existing recipe
                updated_recipe = self.recipe_controller.update_recipe(
                    recipe_id=self.current_recipe.id,
                    name=name,
                    instructions=instructions,
                    tags=tags,
                    ingredients=ingredients
                )
                recipe = updated_recipe
            else:
                # Add a new recipe
                recipe = self.recipe_controller.add_recipe(
                    name=name,
                    instructions=instructions,
                    tags=tags,
                    ingredients=ingredients
                )
        except Exception as e:
            self._show_error(f"Reseptin tallennus epäonnistui: {e}")
            return

        self.recipe_saved.emit(recipe)
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _cancel_recipe(self):
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _show_error(self, message):
        warning = WarningDialog(f"Virhe: {message}", self)
        warning.show()
