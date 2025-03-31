# File: edit_product_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QStackedWidget
)
from PySide6.QtCore import Signal, Qt
from root_controllers import ProductController
from qml import NormalTextField

class EditProductWidget(QWidget):
    # Signal to emit the updated product after saving.
    product_updated = Signal(object)
    # Signal to indicate that editing was cancelled.
    edit_cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_controller = ProductController()
        self.product = None  # Will store the product being edited

        # Create a stacked widget to hold the main form and the unit selector.
        self.stacked = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked)
        self.setLayout(main_layout)

        # Create the main form page.
        self.form_page = QWidget()
        self._init_form_ui()
        self.stacked.addWidget(self.form_page)  # index 0

        # Placeholder for unit selector page.
        self.unit_selector = None

    def _init_form_ui(self):
        """Initializes the main form UI inside self.form_page."""
        layout = QVBoxLayout(self.form_page)

        title = QLabel("Muokkaa tuotetta")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Product Name using NormalTextField.
        name_label = QLabel("Nimi:")
        self.name_edit = NormalTextField(
            text_field_id="name_edit",
            placeholder_text="Syötä nimi..."
        )
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # Unit: Instead of a plain text field, we use a QPushButton to trigger the unit selector.
        unit_label = QLabel("Yksikkö:")
        self.unit_btn = QPushButton("Valitse yksikkö")
        # Optionally, style the button so it looks like an input field.
        self.unit_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 3px;
                padding: 4px 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
            }
        """)
        self.unit_btn.clicked.connect(self._show_unit_selector)
        layout.addWidget(unit_label)
        layout.addWidget(self.unit_btn)

        # Price per unit using NormalTextField.
        price_label = QLabel("Hinta per yksikkö:")
        self.price_edit = NormalTextField(
            text_field_id="price_edit",
            placeholder_text="Syötä hinta..."
        )
        layout.addWidget(price_label)
        layout.addWidget(self.price_edit)

        # Category using NormalTextField.
        category_label = QLabel("Kategoria:")
        self.category_edit = NormalTextField(
            text_field_id="category_edit",
            placeholder_text="Syötä kategoria..."
        )
        layout.addWidget(category_label)
        layout.addWidget(self.category_edit)

        # Buttons for Save and Cancel.
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Tallenna muutokset")
        self.cancel_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        # Connect signals.
        self.save_btn.clicked.connect(self._save_product)
        self.cancel_btn.clicked.connect(self._cancel_edit)

    def _show_unit_selector(self):
        """Creates and shows the unit selector page."""
        self.unit_selector = QWidget()
        self.unit_selector.setLayout(self._create_unit_selector_layout())
        self.stacked.addWidget(self.unit_selector)
        self.stacked.setCurrentWidget(self.unit_selector)

    def _create_unit_selector_layout(self):
        """Creates a vertical layout with buttons for each unit option."""
        layout = QVBoxLayout()
        units = ["kpl", "mg", "g", "kg", "ml", "dl", "l"]
        for unit in units:
            button = QPushButton(unit)
            # When a unit is clicked, call _select_unit.
            button.clicked.connect(lambda checked, u=unit: self._select_unit(u))
            layout.addWidget(button)
        return layout

    def _select_unit(self, unit):
        """Updates the unit button text with the selected unit and returns to the main form."""
        self.unit_btn.setText(unit)
        # Switch back to the main form page.
        self.stacked.setCurrentWidget(self.form_page)
        # Clean up the unit selector page.
        if self.unit_selector:
            self.stacked.removeWidget(self.unit_selector)
            self.unit_selector.deleteLater()
            self.unit_selector = None

    def set_product(self, product):
        """Prepopulate the widget with the product details to edit."""
        self.product = product
        if product:
            self.name_edit.set_text(product.name)
            self.unit_btn.setText(product.unit)
            self.price_edit.set_text(str(product.price_per_unit))
            self.category_edit.set_text(product.category)

    def _save_product(self):
        """Gather data, validate, update the product, and emit product_updated."""
        name = self.name_edit.get_text().strip()
        unit = self.unit_btn.text().strip()
        price_str = self.price_edit.get_text().strip()
        category = self.category_edit.get_text().strip()

        if not name:
            QMessageBox.warning(self, "Virhe", "Tuotteen nimi on pakollinen.")
            return

        try:
            price = float(price_str)
        except ValueError:
            QMessageBox.warning(self, "Virhe", "Hinnan tulee olla numero.")
            return

        try:
            updated_product = self.product_controller.update_product(
                product_id=self.product.id,
                name=name,
                price_per_unit=price,
                category=category
            )
            self.product_updated.emit(updated_product)
        except Exception as e:
            QMessageBox.warning(self, "Virhe", f"Tuotteen päivitys epäonnistui: {e}")

    def _cancel_edit(self):
        """Emits the edit_cancelled signal."""
        self.edit_cancelled.emit()
