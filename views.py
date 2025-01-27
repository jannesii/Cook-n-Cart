import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QStackedWidget, QComboBox, QFrame, QDialog, QLineEdit, QCompleter, QFormLayout
)
from PySide6.QtCore import Qt, QStringListModel
from datetime import datetime

from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC
from models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem
from add_recipe_widget import AddRecipeWidget
from typing import Dict

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()


def format_datetime_or_string(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, str):
        # Optionally parse or just return the raw string
        return value
    else:
        return "N/A"


class OstolistatPage(QWidget):
    """
    Ostolistat-sivu:
      - Yläpalkki: "Ostoslistat" -otsikko vasemmalla, "Uusi ostolista" -nappi oikealla
      - Keskialue: esim. "Ruokaostokset 0/16", "Motonet 0/5", "Biltema 0/11" -napit
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Ostoslistat")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")

        # Esimerkin "Uusi ostolista" -nappi
        new_list_btn = QPushButton("Uusi ostolista")
        new_list_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
        """)

        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(new_list_btn)

        # Värjätään yläpalkin tausta harmaaksi asettamalla QFrame
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;")

        main_layout.addWidget(top_bar_frame, 0)  # yläpalkki

        # -- Scrollattava keskialue, jos listoja on paljon --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Esimerkkilistat
        shopping_lists = [
            "Ruokaostokset \n0/16",
            "Motonet \n0/5",
            "Biltema \n0/11"
        ]

        for item in shopping_lists:
            btn = QPushButton(item)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left; /* Teksti vasemmalle */
                }}
            """)
            scroll_layout.addWidget(btn)

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area, 1)


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
                f"<b>Luotu:</b> {format_datetime_or_string(recipe.created_at)}")
            self.updated_at_label.setText(
                f"<b>Päivitetty:</b> {format_datetime_or_string(recipe.updated_at)}")
        else:
            # Clear fields if no recipe
            self.name_label.setText("")
            self.instructions_label.setText("")
            self.tags_label.setText("")
            self.ingredients_label.setText("")
            self.created_at_label.setText("")
            self.updated_at_label.setText("")


class ReseptitPage(QWidget):
    """
    Reseptit-sivu:
      - QStackedWidget with:
         Page 0: "Reseptilista" with "Hae reseptejä" and "Uusi resepti" at the top
         Page 1: Detailed recipe view (RecipeDetailWidget)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.recipes_dict = {}

        # Main layout for the entire ReseptitPage
        main_layout = QVBoxLayout(self)

        # Create the QStackedWidget
        self.stacked = QStackedWidget()

        # Page 0 (list view)
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1 (detail view)
        self.page_detail = RecipeDetailWidget()

        # Hook the "Back" button
        self.page_detail.back_btn.clicked.connect(self.back_to_list)

        self.page_add_recipe = AddRecipeWidget(
            recipe_controller=RecipeController,
            product_controller=ProductController,
            parent=self
        )
        self.page_add_recipe.cancel_btn.clicked.connect(self.back_to_list)

        # Add both pages to the QStackedWidget
        self.stacked.addWidget(self.page_list)   # index 0
        self.stacked.addWidget(self.page_detail)  # index 1
        self.stacked.addWidget(self.page_add_recipe)  # index 2

        # Start with the list page
        self.stacked.setCurrentIndex(0)

        main_layout.addWidget(self.stacked, 1)

    def _create_list_layout(self):
        """
        Creates and returns the layout for the "list" page (page_list).
        """
        layout = QVBoxLayout()

        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Reseptit")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")

        search_btn = QPushButton("Hae reseptejä")
        new_btn = QPushButton("Uusi resepti")
        new_btn.clicked.connect(self.open_add_recipe_page)

        search_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: #009ACD;
            }}
        """)

        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: #009ACD;
            }}
        """)

        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(search_btn)
        top_bar_layout.addWidget(new_btn)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;")

        layout.addWidget(top_bar_frame, 0)

        # -- Scroll area for recipes --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.update_recipes_dict()

        for recipe_id, recipe in self.recipes_dict.items():
            btn = QPushButton(f"{recipe_id}: {recipe.name}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #009ACD;
                }}
            """)
            # Instead of QDialog, we’ll show the details page:
            btn.clicked.connect(lambda checked=False,
                                r=recipe: self.display_recipe_detail(r))
            scroll_layout.addWidget(btn)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)

        layout.addWidget(scroll_area, 1)

        return layout

    def update_recipes_dict(self):
        self.recipes_dict = RecipeController.get_all_recipes()

    def display_recipe_detail(self, recipe: Recipe):
        """
        Fills in the detail page with the given recipe and switches the stacked widget.
        """
        self.page_detail.set_recipe(recipe)
        # Switch to page index 1 (detail view)
        self.stacked.setCurrentIndex(1)

    def open_add_recipe_page(self):
        # Make sure the add-recipe form is cleared or set to default
        self.page_add_recipe.setFieldsToDefaults()
        # Switch the stacked widget to index 2
        self.stacked.setCurrentIndex(2)

    def back_to_list(self):
        """
        Switches back to the recipe list page.
        """
        self.stacked.setCurrentIndex(0)


class ProductsPage(QWidget):
    """
    Tuotteet-näkymä:
      - Yläpalkki: 'Tuotteet' -otsikko vasemmalla, 'Hae tuotetta' ja 'Uusi tuote' -napit oikealla
      - Keskialue: Scrollattava lista tuotteista
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.products_dict = {}
        self.update_products_dict()

        main_layout = QVBoxLayout(self)

        self.stacked = QStackedWidget()

        # Page 0 (list view)
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())

        # Page 1 (add product view)
        self.page_add_form = QWidget()
        self.page_add_form.setLayout(self._create_add_form_layout())

        self.stacked.addWidget(self.page_list)      # index 0
        self.stacked.addWidget(self.page_add_form)  # index 1

        # Start with the list page
        self.stacked.setCurrentIndex(0)

        main_layout.addWidget(self.stacked, 1)

    def _create_list_layout(self):
        layout = QVBoxLayout()
        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()

        self.title_label = QLabel("Tuotteet")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae tuotetta")
        self.search_bar.textChanged.connect(self.filter_products)

        self.new_button = QPushButton("Uusi tuote")
        self.new_button.clicked.connect(self.display_add_product)

        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        self.new_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
        """)

        top_bar_layout.addWidget(self.title_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_bar)
        top_bar_layout.addWidget(self.new_button)

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;"
        )

        layout.addWidget(top_bar_frame, 0)

        # -- Scrollattava lista keskellä --
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area, 1)

        self.populate_product_list()

        return layout

    def _create_add_form_layout(self):
        layout = QVBoxLayout()

        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.category_edit = QLineEdit()

        # Fetch all categories and ensure uniqueness
        all_categories = ProductController.get_all_categories()
        unique_categories = sorted(set(all_categories))  # Ensures unique and sorted categories

        categories_completer = QCompleter(unique_categories)
        categories_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.category_edit.setCompleter(categories_completer)

        form.addRow("Nimi:", self.name_edit)
        form.addRow("Yksikkö:", self.desc_edit)
        form.addRow("Hinta:", self.price_edit)
        form.addRow("Kategoria:", self.category_edit)

        layout.addLayout(form)

        # Save/Cancel
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("Tallenna tuote")
        save_btn.setStyleSheet(
            f"background-color: {TURKOOSI}; font-weight: bold;"
        )
        save_btn.clicked.connect(self._save_new_product)

        back_btn = QPushButton("Takaisin")
        back_btn.setStyleSheet(
            f"background-color: {HARMAA}; font-weight: bold;"
        )
        back_btn.clicked.connect(self._back_to_product_list)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(back_btn)

        layout.addLayout(btn_layout)

        layout.addStretch()
        return layout

    def _save_new_product(self):
        """
        Call product_controller.add_product(...) with data from the form,
        then go back to product list page and refresh.
        """
        name = self.name_edit.text().strip()
        desc = self.desc_edit.text().strip()
        price_str = self.price_edit.text().strip().replace(",", ".")
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            price = 0.0  # Default to 0.0 or handle the error as needed
            # Optionally, you can show an error message here

        cat = self.category_edit.text().strip()

        # Add the new product using the ProductController
        ProductController.add_product(
            name=name,
            unit=desc,
            price_per_unit=price,
            category=cat
        )

        # Update the products dictionary and refresh the product list
        self.update_products_dict()
        self.populate_product_list()

        # Update the category completer with unique categories
        self._update_category_completer()

        # Clear fields
        self.name_edit.clear()
        self.desc_edit.clear()
        self.price_edit.clear()
        self.category_edit.clear()

        # Go back to page 0 and refresh the product list
        self._back_to_product_list()

    def _update_category_completer(self):
        """
        Refresh the category completer to include any new unique categories.
        """
        all_categories = ProductController.get_all_categories()
        unique_categories = sorted(set(all_categories))
        self.category_edit.completer().setModel(QStringListModel(unique_categories))

    def _back_to_product_list(self):
        """
        Switch from add form (page 1) back to list (page 0).
        """
        self.stacked.setCurrentIndex(0)

    def display_add_product(self):
        self.stacked.setCurrentIndex(1)

    def update_products_dict(self):
        """
        Fetch all products from the ProductController and update the local dictionary.
        """
        self.products_dict = ProductController.get_all_products()

    def populate_product_list(self):
        """
        Populate the scroll area with buttons representing each product.
        """
        # Clear the current layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Sort products by name (case-insensitive)
        sorted_products = sorted(
            self.products_dict.values(),
            key=lambda p: p.name.lower()
        )

        # Add products to the layout
        for product in sorted_products:
            btn = QPushButton(f"{product.name}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }}
            """)
            # Optionally, connect the button to a detailed view or action
            # btn.clicked.connect(lambda checked, p=product: self.view_product_details(p))
            self.scroll_layout.addWidget(btn)

        self.scroll_layout.addStretch()

    def filter_products(self):
        """
        Filter the product buttons based on the search text.
        """
        search_text = self.search_bar.text().lower()
        for i in range(self.scroll_layout.count() - 1):  # Exclude the stretch
            item = self.scroll_layout.itemAt(i).widget()
            if search_text in item.text().lower():
                item.show()
            else:
                item.hide()

class AsetuksetPage(QWidget):
    """
    Asetukset-sivu:
      - Yläpalkki: "Asetukset" -otsikko
      - Keskialue: 2 "nappiriviä" (tai kehyksiä), joihin on sijoitettu Label + ComboBox:
          1) "Valuutta" - '€'
          2) "Painon yksikkö" - 'kg/l'
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Asetukset")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")
        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()

        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;")

        main_layout.addWidget(top_bar_frame, 0)

        # -- Keskialue --
        # Tehdään kaksi "riviä", joissa vasemmalla label ja oikealla ComboBox,
        # ja koko rivi on kehystetty kuin nappi (pyöristetty, turkoosi).

        # 1) Valuutta
        currency_frame = QFrame()
        currency_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TURKOOSI};
                border-radius: 10px;
            }}
        """)
        currency_layout = QHBoxLayout(currency_frame)

        currency_label = QLabel("Valuutta")
        currency_label.setStyleSheet(
            "color: black; font-size: 16px; font-weight: bold;")

        self.currency_combo = QComboBox()
        # Täytetään muutama valuutta esimerkin vuoksi
        self.currency_combo.addItems(["€", "$", "£", "¥"])
        self.currency_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                padding: 2px;
            }
        """)

        currency_layout.addWidget(currency_label)
        currency_layout.addStretch()
        currency_layout.addWidget(self.currency_combo)

        # 2) Painon yksikkö
        weight_frame = QFrame()
        weight_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TURKOOSI};
                border-radius: 10px;
            }}
        """)
        weight_layout = QHBoxLayout(weight_frame)

        weight_label = QLabel("Painon yksikkö")
        weight_label.setStyleSheet(
            "color: black; font-size: 16px; font-weight: bold;")

        self.weight_combo = QComboBox()
        self.weight_combo.addItems(["kg/l", "lb", "oz"])
        self.weight_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                padding: 2px;
            }
        """)

        weight_layout.addWidget(weight_label)
        weight_layout.addStretch()
        weight_layout.addWidget(self.weight_combo)

        # Lisätään kehykset pystylayoutiin
        content_layout = QVBoxLayout()
        content_layout.addWidget(currency_frame)
        content_layout.addWidget(weight_frame)
        content_layout.addStretch()

        main_layout.addLayout(content_layout, 1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Esimerkkisovellus")
        self.setMinimumSize(400, 600)

        # Pääwidget QMainWindowille
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Päälayout (pystysuunta): yläosassa sivut (QStackedWidget), alaosassa navigointipalkki
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- QStackedWidget - sivut ---
        self.stacked_widget = QStackedWidget()

        self.ostolistat_page = OstolistatPage()
        self.reseptit_page = ReseptitPage()
        self.products_page = ProductsPage()
        self.asetukset_page = AsetuksetPage()

        self.stacked_widget.addWidget(self.ostolistat_page)  # index 0
        self.stacked_widget.addWidget(self.reseptit_page)    # index 1
        self.stacked_widget.addWidget(self.products_page)    # index 2
        self.stacked_widget.addWidget(self.asetukset_page)   # index 3

        main_layout.addWidget(self.stacked_widget, stretch=1)

        # --- Alapalkin layout ---
        bottom_bar_layout = QHBoxLayout()

        self.btn_ostolistat = QPushButton("Ostolistat")
        self.btn_reseptit = QPushButton("Reseptit")
        self.btn_tuotteet = QPushButton("Tuotteet")
        self.btn_asetukset = QPushButton("Asetukset")

        # Kytketään napit vaihtamaan QStackedWidgetin sivua
        self.btn_ostolistat.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(0))
        self.btn_reseptit.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(1))
        self.btn_tuotteet.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(2))
        self.btn_asetukset.clicked.connect(
            lambda checked: self.stacked_widget.setCurrentIndex(3))

        # Voit halutessasi säätää alapalkin tyylin
        for btn in [self.btn_ostolistat, self.btn_reseptit, self.btn_tuotteet, self.btn_asetukset]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {HARMAA};
                    color: black;
                    font-weight: bold;
                    border: none;
                    padding: 8px;
                    border-radius: 5px;
                }}
                QPushButton:pressed {{
                    background-color: #707070; /* tummempi harmaa klikatessa */
                }}
            """)

        bottom_bar_layout.addWidget(self.btn_ostolistat)
        bottom_bar_layout.addWidget(self.btn_reseptit)
        bottom_bar_layout.addWidget(self.btn_tuotteet)
        bottom_bar_layout.addWidget(self.btn_asetukset)

        main_layout.addLayout(bottom_bar_layout)

        # Asetetaan oletussivuksi Ostolistat (index 0)
        self.stacked_widget.setCurrentIndex(0)
