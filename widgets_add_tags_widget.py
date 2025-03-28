# File: widgets_add_tags_widget.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal
from qml import TagSelectorWidget  # Import the new TagSelectorWidget from qml.py

class AddTagsWidget(QWidget):
    finished = Signal(list)  # Emits a list of selected tags

    def __init__(self, recipe_controller, selected_tags=None, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        # Get all tags from the controller (unique and sorted)
        self.all_tags = sorted(set(self.recipe_controller.get_all_tags()))
        # Use provided selected_tags if any; otherwise, start empty.
        self.selected_tags = selected_tags if selected_tags is not None else []

        layout = QVBoxLayout(self)

        # Create an instance of TagSelectorWidget.
        self.tag_selector = TagSelectorWidget()
        layout.addWidget(self.tag_selector)

        # Button row for OK and Cancel.
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Peruuta")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Connect the buttons.
        self.ok_btn.clicked.connect(self._finish_selection)
        self.cancel_btn.clicked.connect(self._cancel_selection)

        # Populate the tag selector with tags.
        self.populate_tags()

    def populate_tags(self):
        """
        Populate the QML model in TagSelectorWidget with all tags.
        Pre-check tags that are already selected.
        """
        root_obj = self.tag_selector.get_root_object()
        if root_obj is not None:
            # Clear any existing tags from the QML model.
            root_obj.clearTags()
            # Add each tag from all_tags.
            for tag in self.all_tags:
                is_checked = tag in self.selected_tags
                root_obj.addTag(tag, is_checked)
        else:
            print("TagSelectorWidget root object not found.")

    def _finish_selection(self):
        """
        Retrieve the selected tags from the QML model, update stored selection,
        and emit the finished signal.
        """
        root_obj = self.tag_selector.get_root_object()
        if root_obj is not None:
            js_value = root_obj.getSelectedTags()
            # Convert the QJSValue to a native Python list.
            selected = js_value.toVariant()
            self.selected_tags = selected  # Update stored selection.
            self.finished.emit(selected)
            print(f"Selected tags: {selected}")
        else:
            self.finished.emit([])

    def _cancel_selection(self):
        """
        Retrieve the current selection on cancel and emit it.
        """
        root_obj = self.tag_selector.get_root_object()
        if root_obj is not None:
            selected = root_obj.getSelectedTags().toVariant()
            self.selected_tags = selected  # Update stored selection.
            print(f"Cancelled selection, tags: {selected}")
            self.finished.emit(selected)
        else:
            self.finished.emit([])
