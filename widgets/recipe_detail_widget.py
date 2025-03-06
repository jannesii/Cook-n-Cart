# recipe_detail_widget.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from controllers import ProductController as PC  # Ensure this import exists

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

class RecipeDetailWidget(QWidget):
    # New signal that sends the current recipe object.
    edit_recipe_requested = Signal(object)
    delete_recipe_requested = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_controller = PC()
        self.recipe = None  # Store the current recipe

        self.layout = QVBoxLayout(self)

        # Define labels for each field:
        self.name_label = QLabel()
        self.instructions_label = QLabel()
        self.tags_label = QLabel()
        self.ingredients_Titlelabel = QLabel("<b>Ainesosat:</b>")
        self.ingredients_label = QLabel()
        #self.created_at_label = QLabel()
        self.updated_at_label = QLabel()

        # Allow text to wrap:
        for lbl in [self.name_label, self.instructions_label,
                    self.tags_label, self.ingredients_Titlelabel,
                    self.ingredients_label, self.updated_at_label]:
            lbl.setWordWrap(True)
            self.layout.addWidget(lbl)

        # Buttons layout:
        button_layout = QVBoxLayout()
        # Horizontal layout for Edit/Delete
        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Muokkaa reseptiä")
        self.delete_btn = QPushButton("Poista resepti")
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        button_layout.addLayout(btn_layout)
        # Back button
        self.back_btn = QPushButton("Takaisin")
        button_layout.addWidget(self.back_btn, alignment=Qt.AlignRight)
        self.layout.addLayout(button_layout)

        # Connect the edit button to a local slot that emits our signal
        self.edit_btn.clicked.connect(self.on_edit_clicked)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        
    def on_edit_clicked(self):
        if self.recipe:
            self.edit_recipe_requested.emit(self.recipe)
            
    def on_delete_clicked(self):
        if self.recipe:
            self.delete_recipe_requested.emit(self.recipe)

    def set_recipe(self, recipe):
        """Update the widget fields with the given recipe details."""
        self.recipe = recipe
        if recipe:
            self.name_label.setText(f"<b>Nimi:</b> {recipe.name}")
            instructions_formatted = recipe.instructions.replace("\n", "<br>")
            self.instructions_label.setText(f"<b>Valmistusohje:</b><br>{instructions_formatted}")
            self.tags_label.setText(f"<b>Tagit:</b> {recipe.tags}")
            
            ingredients_text = ""
            for ingredient in recipe.ingredients:
                product = self.product_controller.get_product_by_id(ingredient.product_id)
                product_name = product.name if product else f"Product {ingredient.product_id}"
                # Format quantity to remove unnecessary decimals
                quantity_str = f"{ingredient.quantity:g}"
                ingredients_text += f"{product_name}: {quantity_str} {ingredient.unit}<br>"
            self.ingredients_label.setText(ingredients_text)
            
            #self.created_at_label.setText(f"<b>Luotu:</b> {recipe.created_at}")
            self.updated_at_label.setText(f"<b>Päivitetty:</b> {recipe.updated_at}")
        else:
            self.name_label.setText("")
            self.instructions_label.setText("")
            self.tags_label.setText("")
            self.ingredients_label.setText("")
            #self.created_at_label.setText("")
            self.updated_at_label.setText("")
