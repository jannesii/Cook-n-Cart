# File: add_recipe_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QCompleter, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtCore import Signal

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
        # self.select_tags_btn.setObjectName("recipe_widget_btn")
        self.select_tags_btn.clicked.connect(self._open_tags_page)
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_display_label)
        layout.addWidget(self.select_tags_btn)

        # 4) Tuotteiden lisäys: painike aukaisee tuotteiden valintasivun
        self.add_products_btn = QPushButton("+ Lisää tuotteita")
        # self.add_products_btn.setObjectName("recipe_widget_btn")

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

    def _save_recipe(self):
        name = self.name_edit.text().strip()
        instructions = self.instructions_edit.toPlainText()
        # Tagit yhdistetään pilkulla erotelluksi merkkijonoksi
        tags = ", ".join(self.selected_tags)

        # Tarkistetaan, että pakolliset kentät on täytetty
        if not name:
            self._show_error("Reseptin nimi on pakollinen.")
            return
        if not instructions:
            self._show_error("Valmistusohjeet ovat pakolliset.")
            return

        # Muunnetaan valitut tuotteet reseptin ainesosiksi
        ingredients = []
        for p in self.selected_products:
            ingredients.append({
                "product_id": p.id,
                "quantity": 1.0  # Oletusmäärä; laajennettavissa tarvittaessa
            })

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

    def _show_error(self, message):
        QMessageBox.warning(self, "Virhe", message)

    def setFieldsToDefaults(self):
        self._clear_fields()
