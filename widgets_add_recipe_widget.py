# add_recipe_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QCompleter, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer

from widgets_add_tags_widget import AddTagsWidget
from widgets_add_products_widget import AddProductsWidget
from qml import NormalTextField, TallTextField, TagSelectorWidget

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
        self.stacked.addWidget(self.form_page)      # index 0

        # Page 1: Tuotteiden valinta (oletetaan, että AddProductsWidget on jo toteutettu)
        self.products_page = None

        # Page 2: Tagien valinta
        self.tags_page = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self._open_form_page()

    def _create_form_layout(self):
        layout = QVBoxLayout()

        # 1) Nimi
        name_label = QLabel("Nimi:")
        self.name_edit = NormalTextField(
            text_field_id="name_edit",
            placeholder_text="Syötä reseptin nimi"
        )
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # 2) Ohjeet
        instructions_label = QLabel("Valmistusohjeet:")
        self.instructions_edit = TallTextField(
            text_field_id="instructions_edit",
            placeholder_text="Syötä valmistusohjeet"
        )
        layout.addWidget(instructions_label)
        layout.addWidget(self.instructions_edit)

        # 3) Tagien valinta: näytetään nykyiset tagit ja nappi niiden muokkaamiseen
        tags_label = QLabel("Tagit:")
        self.tags_display_label = QLabel()
        # Use the stored selected tags to update the label.
        if self.selected_tags:
            self.tags_display_label.setText(", ".join(self.selected_tags))
        else:
            self.tags_display_label.setText("Ei valittuja tageja")
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


    def _open_form_page(self):
        """
        Aseta lomake näkyviin (Page 0).
        """

        self.stacked.setCurrentIndex(0)

    def _open_products_page(self):
        self.products_page = AddProductsWidget(
            parent=self, selected_products=self.selected_products
        )
        self.products_page.finished.connect(self.on_products_selected)
        self.stacked.addWidget(self.products_page)    # index 1
        self.stacked.setCurrentWidget(self.products_page)

    def _open_tags_page(self):
        self.tags_page = AddTagsWidget(
            recipe_controller=self.recipe_controller,
            selected_tags=self.selected_tags,  # Pass the current selected tags
            parent=self
        )
        self.tags_page.finished.connect(self.on_tags_selected)
        self.stacked.addWidget(self.tags_page)        # index 2
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
        # Päivitetään lomakkeen näyttö:
        if selected_tags:
            self.selected_tags = selected_tags
            print(f"Selected tags: {selected_tags}")
            self.tags_display_label.setText(", ".join(selected_tags))
        else:
            print("Ei valittuja tageja")
            self.tags_display_label.setText("Ei valittuja tageja")
        self._open_form_page()


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

        for p in self.selected_products:
            try:
                quantity = float(p.get("quantity", 0))
            except ValueError:
                self._show_error("Ainesosan määrä ei ole kelvollinen luku.")
                return
            if quantity <= 0:
                self._show_error(
                    "Ainesosan määrä täytyy olla suurempi kuin 0.")
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
        for i in ingredients:
            print(f"Ingredient: {i}")
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
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _cancel_add_recipe(self):
        if hasattr(self.parent(), "back_to_list"):
            self.parent().back_to_list()

    def _show_error(self, message):
        QMessageBox.warning(self, "Virhe", message)

    def clearMemory(self):
        if self.products_page:
            self.stacked.removeWidget(self.products_page)
            self.products_page.deleteLater()
            self.products_page = None
        if self.tags_page:
            self.stacked.removeWidget(self.tags_page)
            self.tags_page.deleteLater()
            self.tags_page = None