# File: edit_product_widget.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from root_controllers import ProductController
from qml import NormalTextField  # Use the QML based NormalTextField

class EditProductWidget(QWidget):
    # Signal to emit the updated product after saving.
    product_updated = Signal(object)
    # Signal to indicate that editing was cancelled.
    edit_cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_controller = ProductController()
        self.product = None  # Will store the product being edited
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Muokkaa tuotetta")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Product Name
        name_label = QLabel("Nimi:")
        self.name_edit = NormalTextField(
            text_field_id="name_edit",
            placeholder_text="Syötä nimi..."
        )
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

        # Unit
        unit_label = QLabel("Yksikkö:")
        self.unit_edit = NormalTextField(
            text_field_id="unit_edit",
            placeholder_text="Syötä yksikkö..."
        )
        layout.addWidget(unit_label)
        layout.addWidget(self.unit_edit)

        # Price per unit
        price_label = QLabel("Hinta per yksikkö:")
        self.price_edit = NormalTextField(
            text_field_id="price_edit",
            placeholder_text="Syötä hinta..."
        )
        layout.addWidget(price_label)
        layout.addWidget(self.price_edit)

        # Category
        category_label = QLabel("Kategoria:")
        self.category_edit = NormalTextField(
            text_field_id="category_edit",
            placeholder_text="Syötä kategoria..."
        )
        layout.addWidget(category_label)
        layout.addWidget(self.category_edit)

        # Buttons for Save and Cancel
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Tallenna muutokset")
        self.cancel_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Connect signals.
        self.save_btn.clicked.connect(self._save_product)
        self.cancel_btn.clicked.connect(self._cancel_edit)

    def set_product(self, product):
        """
        Prepopulate the widget with the product details to edit.
        """
        self.product = product
        if product:
            self.name_edit.set_text(product.name)
            self.unit_edit.set_text(product.unit)
            self.price_edit.set_text(str(product.price_per_unit))
            self.category_edit.set_text(product.category)

    def _save_product(self):
        """
        Gather data from the input fields, validate them,
        call the update method from ProductController, and emit product_updated.
        """
        name = self.name_edit.get_text().strip()
        unit = self.unit_edit.get_text().strip()
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
        """
        Handle cancellation of editing.
        """
        self.edit_cancelled.emit()
