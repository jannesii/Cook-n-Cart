# File: widgets_product_form_widget.py --------------------------------------------------------------------

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QStackedWidget
)
from PySide6.QtCore import Qt, Signal

from widgets_add_categories_widget import AddCategoriesWidget
from qml import NormalTextField
from error_handler import catch_errors_ui, show_error_toast


class ProductFormWidget(QWidget):
    # Signals to let the parent know when the product is saved or canceled.
    finished = Signal(object)  # Emits the new/updated product.
    canceled = Signal()

    @catch_errors_ui
    def __init__(self, product_controller, product=None, parent=None):
        """
        Initialize the product form widget.

        Parameters:
            product_controller: Controller instance handling product operations.
            product: Optional product instance. If provided, the form will be populated for editing.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.product_controller = product_controller
        # None for adding new; existing product for editing.
        self.product = product
        self.parent_page = parent
        self.edit_mode = False  # Flag to indicate if we are in edit mode.

        # Create the main layout and a stacked widget
        main_layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()

        # Create the form UI only once.
        self.page_add_form = QWidget()
        # Call _init_ui() once and get the layout.
        form_layout = self._init_ui()
        self.page_add_form.setLayout(form_layout)
        self.stacked.addWidget(self.page_add_form)
        self.stacked.setCurrentWidget(self.page_add_form)
        main_layout.addWidget(self.stacked, 1)
        self.setLayout(main_layout)

        # If editing, then update fields.
        if self.product is not None:
            print(f"Editing product: {self.product.name}")
            self.edit_mode = True
            self._populate_fields()

    @catch_errors_ui
    def _init_ui(self):
        # Use a QFormLayout to keep labels and inputs nicely aligned
        form_layout = QFormLayout()

        # -- Nimi --
        nimi_label = QLabel("Nimi:")
        self.name_edit = NormalTextField(
            text_field_id="name_edit", placeholder_text="Syötä nimi..."
        )
        form_layout.addRow(nimi_label, self.name_edit)

        # -- Yksikkö --
        yksikko_label = QLabel("Yksikkö:")
        self.unit_edit = QPushButton("Valitse yksikkö")
        self.unit_edit.clicked.connect(self._show_unit_selector)
        self.unit_edit.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 3px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
            }
        """)
        form_layout.addRow(yksikko_label, self.unit_edit)

        # -- Hinta --
        hinta_label = QLabel("Hinta per yksikkö:")
        self.price_edit = NormalTextField(
            text_field_id="price_edit", placeholder_text="Syötä hinta..."
        )
        form_layout.addRow(hinta_label, self.price_edit)

        # -- Kategoria --
        kategoria_label = QLabel("Kategoria:")
        self.category_edit = QPushButton("Valitse kategoria")
        self.category_edit.clicked.connect(self._show_category_selector)
        self.category_edit.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 3px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
            }
        """)
        form_layout.addRow(kategoria_label, self.category_edit)

        # -- Buttons row --
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Tallenna tuote")
        save_btn.clicked.connect(self.finish)
        back_btn = QPushButton("Takaisin")
        back_btn.setObjectName("gray_button")
        back_btn.clicked.connect(self.cancel)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(back_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        main_layout.setAlignment(Qt.AlignCenter)

        return main_layout

    @catch_errors_ui
    def cancel(self):
        """Handle cancel action."""
        self.canceled.emit()

    @catch_errors_ui
    def finish(self):
        """Handle finish action."""
        if self.edit_mode:
            self._finish_edit()
        else:
            self._save_new_product()

    @catch_errors_ui
    def _populate_fields(self):
        if self.product is not None:
            print(f"Populating fields for product: {self.product.name}")
            self.name_edit.set_text(self.product.name)
            self.unit_edit.setText(self.product.unit)
            self.price_edit.set_text(str(self.product.price_per_unit))
            self.category_edit.setText(self.product.category)

    @catch_errors_ui
    def _show_form_page(self):
        if self.page_add_form is not None:
            self.stacked.setCurrentWidget(self.page_add_form)

    @catch_errors_ui
    def _show_category_selector(self):
        self.category_selector = AddCategoriesWidget()
        self.category_selector.finished.connect(self._on_category_selected)
        self.category_selector.cancel_btn.clicked.connect(self._show_form_page)
        self.stacked.addWidget(self.category_selector)
        self.stacked.setCurrentWidget(self.category_selector)

    @catch_errors_ui
    def _on_category_selected(self, categories):
        categories = ", ".join(
            categories) if categories else "Valitse kategoria"
        self.category_edit.setText(categories)
        if self.page_add_form is not None:
            self.stacked.setCurrentWidget(self.page_add_form)

    @catch_errors_ui
    def _show_unit_selector(self):
        self.unit_selector = QWidget()
        self.unit_selector.setLayout(self._create_unit_selector_layout())
        self.stacked.addWidget(self.unit_selector)
        self.stacked.setCurrentWidget(self.unit_selector)

    @catch_errors_ui
    def _select_unit(self, unit):
        self.unit_edit.setText(unit)
        if self.page_add_form is not None:
            self.stacked.setCurrentWidget(self.page_add_form)
        if self.unit_selector is not None:
            self.stacked.removeWidget(self.unit_selector)
            self.unit_selector.deleteLater()
            self.unit_selector = None

    @catch_errors_ui
    def _create_unit_selector_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        units = ["Kappaletavara (€/kpl)", "Painoperusteinen (€/kg)",
                 "Tilavuusperusteinen (€/l)",]
        for unit in units:
            button = QPushButton(unit)
            button.setFixedWidth(int(self.width() * 0.8))
            button.clicked.connect(lambda checked=True,
                                   u=unit: self._select_unit(u))
            layout.addWidget(button)
        return layout

    @catch_errors_ui
    def _finish_edit(self):
        name = self.name_edit.get_text().strip()
        unit = self.unit_edit.text().strip()
        price_str = self.price_edit.get_text().strip().replace(",", ".")
        cat = self.category_edit.text().strip()

        missing_fields = []
        if not name:
            missing_fields.append("Name")
            show_error_toast(self, "Nimi ei voi olla tyhjä!", pos="top")
            return

        if unit == "Valitse yksikkö" or unit == "Kappaletavara (€/kpl)":
            unit = "kpl"
        elif unit == "Painoperusteinen (€/kg)":
            unit = "kg"
        elif unit == "Tilavuusperusteinen (€/l)":
            unit = "l"

        if not price_str:
            price_str = "0.0"
        if cat == "Valitse kategoria":
            cat = "Muu"

        try:
            price = float(price_str)
        except ValueError:
            show_error_toast(
                self, "Virheellinen hinta!\nSyötä kelvollinen numeerinen arvo.", pos="top", lines=2
            )
            return

        updated_product = self.product_controller.update_product(
            product_id=self.product.id,
            name=name,
            price_per_unit=price,
            category=cat
        )

        print(f"Editing product: {name}, {unit}, {price}, {cat}")
        self.finished.emit(updated_product)

    @catch_errors_ui
    def _save_new_product(self):
        name = self.name_edit.get_text().strip()
        unit = self.unit_edit.text().strip()
        price_str = self.price_edit.get_text().strip().replace(",", ".")
        cat = self.category_edit.text().strip()

        missing_fields = []
        if not name:
            missing_fields.append("Name")
            show_error_toast(self, "Nimi ei voi olla tyhjä!", pos="top")
            return

        if unit == "Valitse yksikkö" or unit == "Kappaletavara (€/kpl)":
            unit = "kpl"
        elif unit == "Painoperusteinen (€/kg)":
            unit = "kg"
        elif unit == "Tilavuusperusteinen (€/l)":
            unit = "l"

        if not price_str:
            price_str = "0.0"
        if cat == "Valitse kategoria":
            cat = ""

        try:
            price = float(price_str)
        except ValueError:
            show_error_toast(
                self, "Virheellinen hinta!\nSyötä kelvollinen numeerinen arvo.", pos="top", lines=2
            )
            return

        print(f"Adding product: {name}, {unit}, {price}, {cat}")
        self.product_controller.add_product(
            name=name,
            unit=unit,
            price_per_unit=price,
            category=cat
        )

        self.finished.emit(self.product)
