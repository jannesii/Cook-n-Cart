from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QCompleter, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

class AddRecipeWidget(QWidget):
    """
    Widget uuden reseptin lisäämistä varten. Sisältää:
      - Nimi, ohjeet kentät
      - Painikkeen tuotteiden lisäämiseen (käyttää AddProductsWidget)
      - Uuden tagien valinnan: nappi, joka avaa tagien valintasivun (AddTagsWidget)
      - Tallenna ja Peruuta napit
    Sisäisen QStackedWidgetin sivut:
      Page 0: Reseptilomake
      Page 1: Tuotteiden valinta (AddProductsWidget)
      Page 2: Tagien valinta (AddTagsWidget)
    """

    # Signaali, joka emittoidaan uuden reseptin tallennuksen jälkeen
    recipe_added = Signal(object)

    def __init__(self, recipe_controller, product_controller, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        self.product_controller = product_controller

        # Tallennetaan valitut tuotteet ja tagit
        self.selected_products = []
        self.selected_tags = []

        # QStackedWidget:n asetukset:
        # Page 0: reseptilomake
        # Page 1: tuotteiden valinta (olemassa oleva widget)
        # Page 2: tagien valinta (uusi widget)
        self.stacked = QStackedWidget(self)

        # Page 0: Reseptilomake
        self.form_page = QWidget()
        self.form_page.setLayout(self._create_form_layout())

        # Page 1: Tuotteiden valinta (oletetaan, että AddProductsWidget on jo toteutettu)
        from widgets.add_products_widget import AddProductsWidget
        self.products_page = AddProductsWidget(
            product_controller=self.product_controller,
            parent=self
        )
        self.products_page.finished.connect(self.on_products_selected)

        # Page 2: Tagien valinta
        from widgets.add_tags_widget import AddTagsWidget
        self.tags_page = AddTagsWidget(
            recipe_controller=self.recipe_controller,
            parent=self
        )
        self.tags_page.finished.connect(self.on_tags_selected)

        self.stacked.addWidget(self.form_page)      # index 0
        self.stacked.addWidget(self.products_page)    # index 1
        self.stacked.addWidget(self.tags_page)        # index 2

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)
        self.setLayout(layout)

    def _create_form_layout(self):
        """
        Luo lomakkeen ulkoasun uudelle reseptille (Page 0).
        """
        layout = QVBoxLayout()

        # 1) Nimi
        name_label = QLabel("Nimi:")
        self.name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # 2) Ohjeet
        instructions_label = QLabel("Valmistusohjeet:")
        self.instructions_edit = QTextEdit()
        layout.addWidget(instructions_label)
        layout.addWidget(self.instructions_edit)

        # 3) Tagien valinta: näytetään nykyiset tagit ja nappi niiden muokkaamiseen
        tags_label = QLabel("Tagit:")
        self.tags_display_label = QLabel("Ei valittuja tageja")
        self.select_tags_btn = QPushButton("Valitse tageja")
        self.select_tags_btn.clicked.connect(self._open_tags_page)
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_display_label)
        layout.addWidget(self.select_tags_btn)

        # 4) Tuotteiden lisäys: painike aukaisee tuotteiden valintasivun
        self.add_products_btn = QPushButton("+ Lisää tuotteita")
        self.add_products_btn.clicked.connect(self._open_products_page)
        layout.addWidget(self.add_products_btn)

        # 5) Tallenna ja Peruuta napit
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Tallenna resepti")
        self.save_btn.clicked.connect(self._save_recipe)
        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.setObjectName("gray_button")
        self.cancel_btn.clicked.connect(self._cancel_add_recipe)
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)

        layout.addStretch()
        return layout

    def _open_products_page(self):
        self.stacked.setCurrentIndex(1)

    def _open_tags_page(self):
        self.stacked.setCurrentIndex(2)

    def on_products_selected(self, selected_products):
        self.selected_products = selected_products
        self.stacked.setCurrentIndex(0)

    def on_tags_selected(self, selected_tags):
        self.selected_tags = selected_tags
        # Päivitetään lomakkeen näyttö:
        if selected_tags:
            self.tags_display_label.setText(", ".join(selected_tags))
        else:
            self.tags_display_label.setText("Ei valittuja tageja")
        self.stacked.setCurrentIndex(0)

    def setFieldsToRecipe(self, recipe):
        self.name_edit.setText(recipe.name)
        self.instructions_edit.setText(recipe.instructions)
        # Prepopulate tags: split by comma and trim spaces.
        self.selected_tags = [tag.strip() for tag in recipe.tags.split(",")] if recipe.tags else []
        self.tags_display_label.setText(recipe.tags if recipe.tags else "Ei valittuja tageja")
        # Prepopulate the product selection: build a list of dicts from recipe ingredients.
        self.selected_products = [
            {"id": ing.product_id, "quantity": ing.quantity, "unit": ing.unit}
            for ing in recipe.ingredients
        ]
        # Store the current recipe id for later update.
        self.current_recipe_id = recipe.id
        # Instead of immediately rebuilding the products list, schedule it to run as soon as the event loop is free.
        QTimer.singleShot(0, lambda: self.products_page.set_selected_products(self.selected_products))


    def _save_recipe(self):
        name = self.name_edit.text().strip()
        instructions = self.instructions_edit.toPlainText()
        tags = ", ".join(self.selected_tags)

        if not name:
            self._show_error("Reseptin nimi on pakollinen.")
            return
        if not instructions:
            self._show_error("Valmistusohjeet ovat pakolliset.")
            return

        for p in self.selected_products:
            try:
                quantity = float(p.get("quantity", 0))
            except ValueError:
                self._show_error("Ainesosan määrä ei ole kelvollinen luku.")
                return
            if quantity <= 0:
                self._show_error("Ainesosan määrä täytyy olla suurempi kuin 0.")
                return
            if not p.get("unit"):
                self._show_error("Valitse ainesosalle yksikkö.")
                return

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
            # If we're in edit mode (current_recipe_id is set), update the recipe.
            if hasattr(self, "current_recipe_id") and self.current_recipe_id:
                updated_recipe = self.recipe_controller.update_recipe(
                    recipe_id=self.current_recipe_id,
                    name=name,
                    instructions=instructions,
                    tags=tags,
                    ingredients=ingredients
                )
                new_recipe = updated_recipe
            else:
                # Otherwise, add as a new recipe.
                new_recipe = self.recipe_controller.add_recipe(
                    name=name,
                    instructions=instructions,
                    tags=tags,
                    ingredients=ingredients
                )
        except Exception as e:
            self._show_error(f"Reseptin tallennus epäonnistui: {e}")
            return

        self.recipe_added.emit(new_recipe)
        self._clear_fields()
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _cancel_add_recipe(self):
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _clear_fields(self):
        self.name_edit.clear()
        self.instructions_edit.clear()
        self.tags_display_label.setText("Ei valittuja tageja")
        self.selected_products = []
        self.selected_tags = []
        # Clear edit mode if present.
        if hasattr(self, "current_recipe_id"):
            del self.current_recipe_id

    def _show_error(self, message):
        QMessageBox.warning(self, "Virhe", message)

    def setFieldsToDefaults(self):
        self._clear_fields()