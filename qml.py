# qml.py

from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl, QObject
from PySide6.QtQml import QQmlComponent
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QTimer
import functools
import logging
from error_handler import catch_errors


class NormalTextField(QWidget):
    @catch_errors
    def __init__(self, text_field_id="mobileTextField", placeholder_text="Enter value...", parent=None, width=200):
        super().__init__(parent)
        self.text_field_id = text_field_id

        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        # Inline QML with a dynamic TextField id
        qml_code = f'''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {{
            id: root
            width: {width}
            height: 40
            color: "transparent"
            radius: 3
            border.width: 1
            border.color: "gray"

            TextField {{
                id: {self.text_field_id}
                objectName: "{self.text_field_id}"  // Set the objectName so findChild() can locate this element
                anchors.fill: parent
                font.pixelSize: 16
                placeholderText: " {placeholder_text}"
                background: Rectangle {{ color: "transparent" }}  // Override default background
            }}
        }}
        '''
        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        item = component.create()
        self.quick_widget.setContent(QUrl(), component, item)

    @catch_errors
    def get_text(self):
        # Retrieve the QML root object
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            # Use the dynamic id to find the TextField
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                return text_field.property("text")
        return ""

    @catch_errors
    def set_text(self, text: str):
        """
        Set the text of the QML TextField by finding the object and updating its property.
        """
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                text_field.setProperty("text", text)


class TallTextField(QWidget):
    @catch_errors
    def __init__(self, text_field_id="mobileTextField", placeholder_text="Enter value...", parent=None):
        super().__init__(parent)
        self.text_field_id = text_field_id

        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        # Inline QML with a dynamic TextField id
        qml_code = f'''
import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {{
    id: root
    width: 200
    height: 200
    color: "transparent"
    radius: 3
    border.width: 1
    border.color: "gray"

    TextArea {{
        id: {self.text_field_id}
        objectName: "{self.text_field_id}"  // Allows findChild() to locate this element
        anchors.fill: parent
        font.pixelSize: 16
        placeholderText: " {placeholder_text}"
        wrapMode: Text.WordWrap  // Enable wrapping/newline input

    }}
}}

        '''
        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        item = component.create()
        self.quick_widget.setContent(QUrl(), component, item)

    @catch_errors
    def get_text(self):
        # Retrieve the QML root object
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            # Use the dynamic id to find the TextField
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                return text_field.property("text")
        return ""

    @catch_errors
    def set_text(self, text: str):
        """
        Set the text of the QML TextField by finding the object and updating its property.
        """
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                text_field.setProperty("text", text)


class MainSearchTextField(QWidget):
    @catch_errors
    def __init__(self, text_field_id="mobileTextField", placeholder_text="Enter value...", parent=None):
        super().__init__(parent)
        self.text_field_id = text_field_id

        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        # Inline QML with a dynamic TextField id and a textChanged signal.
        qml_code = f'''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {{
            id: root
            width: 140
            height: 40
            color: "transparent"
            radius: 3
            border.width: 1
            border.color: "gray"

            // Signal to propagate text changes.
            signal textChanged(string newText)

            TextField {{
                id: {self.text_field_id}
                objectName: "{self.text_field_id}"  // So findChild() can locate it if needed.
                anchors.fill: parent
                font.pixelSize: 16
                placeholderText: " {placeholder_text}"
                onTextChanged: root.textChanged(text)
                background: Rectangle {{ color: "transparent" }}  // Override default background
            }}
        }}
        '''
        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        item = component.create()
        self.quick_widget.setContent(QUrl(), component, item)

    @catch_errors
    def get_text(self):
        # Retrieve the QML root object and then the TextField by its id.
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                return text_field.property("text")
        return ""

    @catch_errors
    def get_root_object(self):
        return self.quick_widget.rootObject()


class ScrollViewWidget(QWidget):
    @catch_errors
    def __init__(self, list_model_name="myListModel", parent=None, height=50, main_height=200):
        super().__init__(parent)
        self.list_model_name = list_model_name  # dynamic objectName for ListModel
        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        # Inline QML code for a ScrollView with a ListView and a dynamic ListModel.
        # It defines:
        # - A delegate that displays a clickable Rectangle (with text) and stores itemId.
        # - A signal "itemClicked" that is emitted when an item is clicked.
        # - Helper functions "addItem" and "clearItems" to manage the model.
        qml_code = f'''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        ScrollView {{
            id: scrollView
            width: 350
            height: {main_height}

            // Signal emitted when an item is clicked. Sends the productId.
            signal itemClicked(var productId)

            ListView {{
                id: listView
                anchors.fill: parent
                model: {self.list_model_name}
                delegate: Item {{
                    width: listView.width   // Use ListView's width instead of parent's width.
                    height: {height}

                    Rectangle {{
                        id: itemRect
                        width: parent.width 
                        height: {height-5}
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        radius: 8
                        color: "#00B0F0"

                        Text {{
                            id: itemText
                            text: model.text
                            anchors {{
                                left: parent.left
                                right: parent.right
                                top: parent.top
                                bottom: parent.bottom
                                leftMargin: 16
                                rightMargin: 16
                                topMargin: 10
                                bottomMargin: 10
                            }}
                            color: "black"
                            font.bold: true
                            font.pixelSize: 16
                        }}

                        MouseArea {{
                            anchors.fill: parent
                            onClicked: {{
                                scrollView.itemClicked(model.productId)
                            }}
                        }}
                    }}
                }}
            }}

            ListModel {{
                id: {self.list_model_name}
                objectName: "{self.list_model_name}"
            }}

            // QML helper function to add an item to the ListModel.
            function addItem(text, productId) {{
                {self.list_model_name}.append({{"text": text, "productId": productId}});
            }}

            // QML helper function to clear all items from the ListModel.
            function clearItems() {{
                while({self.list_model_name}.count > 0) {{
                    {self.list_model_name}.remove(0);
                }}
            }}
        }}
        '''

        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        item = component.create()
        self.quick_widget.setContent(QUrl(), component, item)

    @catch_errors
    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

    @catch_errors
    def add_item(self, text: str, item_id):
        """
        Adds an item with the given text and item_id to the QML ListModel
        by calling the QML function 'addItem'.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.addItem(text, item_id)
            except Exception as e:
                print("Error calling addItem:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def clear_items(self):
        """
        Clears all items from the QML ListModel by calling the QML function 'clearItems'.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.clearItems()
            except Exception as e:
                print("Error calling clearItems:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def connect_item_clicked(self, slot):
        """
        Connects a Python slot to the QML 'itemClicked' signal.
        The slot should accept one argument, the itemId.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            root_obj.itemClicked.connect(slot)
        else:
            print("Root object not found.")
            raise RuntimeError("Root object not found.")


class TagSelectorWidget(QWidget):
    """
    A QML-based widget that displays a scrollable list of tags with checkboxes.
    Provides helper functions to populate the model, clear tags, and retrieve selected tags.
    """
    @catch_errors
    def __init__(self, parent=None, main_height=350):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        qml_code = '''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {
            id: root
            width: 300
            height: 350
            color: "transparent"

            ListView {
                id: tagListView
                anchors.fill: parent
                spacing: 5  // Vertical spacing between delegates
                model: tagModel
                delegate: Rectangle {
                    id: delegateRect
                    width: tagListView.width   // Screen-wide
                    height: 30                 // Touch target size
                    radius: 10
                    color: model.checked ? "#00B0F0" : "#ffffff"
                    border.width: 1
                    border.color: "gray"

                    Text {
                        id: tagText
                        text: model.text
                        anchors.centerIn: parent
                        font.pixelSize: 16
                        color: model.checked ? "white" : "black"
                        font.bold: true
                    }

                    // The entire delegate acts as a button.
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            model.checked = !model.checked
                            reorderSelected()
                        }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Helper function to add a tag into the model.
            function addTag(text, checked) {
                // Ensure that roles are defined by providing safe defaults.
                var safeText = text !== undefined ? text : ""
                var safeChecked = checked !== undefined ? checked : false
                tagModel.append({"text": safeText, "checked": safeChecked})
            }

            // Helper function to clear all tags from the model.
            function clearTags() {
                while (tagModel.count > 0) {
                    tagModel.remove(0)
                }
            }

            // Helper function to return an array of selected tag texts.
            function getSelectedTags() {
                var result = []
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i)
                    if (item.checked)
                        result.push(item.text)
                }
                return result
            }

            // Function to reorder the model so that all selected tags are at the top.
            function reorderSelected() {
                var selectedItems = []
                var unselectedItems = []
                // Split items into selected and unselected while ensuring defined roles.
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i)
                    var fixedItem = {
                        "text": item.text !== undefined ? item.text : "",
                        "checked": item.checked !== undefined ? item.checked : false
                    }
                    if (fixedItem.checked)
                        selectedItems.push(fixedItem)
                    else
                        unselectedItems.push(fixedItem)
                }
                // Clear the model.
                while (tagModel.count > 0) {
                    tagModel.remove(0)
                }
                // Append selected items first.
                for (var i = 0; i < selectedItems.length; i++) {
                    tagModel.append(selectedItems[i])
                }
                // Append the unselected items.
                for (var i = 0; i < unselectedItems.length; i++) {
                    tagModel.append(unselectedItems[i])
                }
            }

            // New function to mark all tags as checked.
            function checkAllTags() {
                for (var i = 0; i < tagModel.count; i++) {
                    tagModel.setProperty(i, "checked", true)
                }
                reorderSelected()
            }

            // A timer to reorder the model after initial population.
            Timer {
                id: reorderTimer
                interval: 10   // Adjust delay as needed
                running: false
                repeat: false
                onTriggered: {
                    reorderSelected()
                }
            }

            Component.onCompleted: {
                reorderTimer.start()
            }
        }

        '''

        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        qml_item = component.create()
        self.quick_widget.setContent(QUrl(), component, qml_item)

    @catch_errors
    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

    @catch_errors
    def add_tag(self, text: str, checked: bool = False):
        """
        Adds a tag with the given text and checked state to the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.addTag(text, checked)
            except Exception as e:
                print("Error calling addTag:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def clear_tags(self):
        """
        Clears all tags from the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.clearTags()
            except Exception as e:
                print("Error calling clearTags:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def get_selected_tags(self):
        """
        Retrieves an array of tag texts that are checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                return root_obj.getSelectedTags()
            except Exception as e:
                print("Error calling getSelectedTags:", e)
        else:
            print("Root object not found.")
        return []

    @catch_errors
    def check_all_tags(self):
        """
        Marks all tags as checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.checkAllTags()
            except Exception as e:
                print("Error calling checkAllTags:", e)
        else:
            print("Root object not found.")


class IngredientSelectorWidget(QWidget):
    """
    A QML-based widget that displays a scrollable list of tags with checkboxes.
    Provides helper functions to populate the model, clear tags, and retrieve selected tags.
    """
    @catch_errors
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        qml_code = '''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {
            id: root
            width: 300
            height: 350
            color: "transparent"

            ListView {
                id: tagListView
                anchors.fill: parent
                spacing: 5  // Vertical spacing between delegates
                model: tagModel
                delegate: Rectangle {
                    id: delegateRect
                    width: tagListView.width   // Screen-wide
                    height: 30                 // Touch target size
                    radius: 10
                    color: model.checked ? "#00B0F0" : "#ffffff"
                    border.width: 1
                    border.color: "gray"

                    Text {
                        id: tagText
                        text: model.text
                        anchors.centerIn: parent
                        font.pixelSize: 16
                        color: model.checked ? "white" : "black"
                        font.bold: true
                    }

                    // The entire delegate acts as a button.
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            model.checked = !model.checked
                            reorderSelected()
                        }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Helper function to add a tag into the model.
            function addTag(text, checked, quantity, unit, id) {
                // Ensure that roles are defined by providing safe defaults.
                var safeText = text !== undefined ? text : ""
                var safeChecked = checked !== undefined ? checked : false
                var safeQuantity = quantity !== undefined ? quantity : 0
                var safeUnit = unit !== undefined ? unit : ""
                var safeId = id !== undefined ? id : ""
                //console.log("Adding tag:", safeChecked, safeQuantity, safeUnit, safeId)
                tagModel.append({
                    "text": safeText,
                    "checked": safeChecked,
                    "quantity": safeQuantity,
                    "unit": safeUnit,
                    "id": safeId
                })
            }

            // Helper function to clear all tags from the model.
            function clearTags() {
                while (tagModel.count > 0) {
                    tagModel.remove(0)
                }
            }

            // Helper function to return an array of selected tag details.
            function getSelectedTags() {
                var result = []
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i)
                    if (item.checked) {
                        //console.log("Exporting item:", item.id, item.quantity, item.unit)
                        result.push({
                            "id": item.id,
                            "quantity": item.quantity,
                            "unit": item.unit
                        })
                    }
                }
                return result
            }

            // Function to reorder the model so that all selected tags are at the top.
            function reorderSelected() {
                var selectedItems = []
                var unselectedItems = []
                // Split items into selected and unselected while ensuring defined roles.
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i)
                    var fixedItem = {
                        "text": item.text !== undefined ? item.text : "",
                        "checked": item.checked !== undefined ? item.checked : false,
                        "quantity": item.quantity !== undefined ? item.quantity : 0,
                        "unit": item.unit !== undefined ? item.unit : "",
                        "id": item.id !== undefined ? item.id : ""
                    }
                    if (fixedItem.checked) {
                        selectedItems.push(fixedItem)
                    } else {
                        unselectedItems.push(fixedItem)
                    }
                }
                // Clear the model.
                while (tagModel.count > 0) {
                    tagModel.remove(0)
                }
                // Append selected items first.
                for (var i = 0; i < selectedItems.length; i++) {
                    tagModel.append(selectedItems[i])
                }
                // Append the unselected items.
                for (var i = 0; i < unselectedItems.length; i++) {
                    tagModel.append(unselectedItems[i])
                }
            }

            // New function to mark all tags as checked.
            function checkAllTags() {
                for (var i = 0; i < tagModel.count; i++) {
                    tagModel.setProperty(i, "checked", true)
                }
                reorderSelected()
            }

            // A timer to reorder the model after initial population.
            Timer {
                id: reorderTimer
                interval: 10   // Adjust delay as needed
                running: false
                repeat: false
                onTriggered: {
                    reorderSelected()
                }
            }

            Component.onCompleted: {
                reorderTimer.start()
            }
        }

        '''

        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        qml_item = component.create()
        self.quick_widget.setContent(QUrl(), component, qml_item)

    @catch_errors
    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

    @catch_errors
    def add_tag(self, text: str, checked: bool = False):
        """
        Adds a tag with the given text and checked state to the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.addTag(text, checked)
            except Exception as e:
                print("Error calling addTag:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def clear_tags(self):
        """
        Clears all tags from the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.clearTags()
            except Exception as e:
                print("Error calling clearTags:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def get_selected_tags(self):
        """
        Retrieves an array of tag texts that are checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                return root_obj.getSelectedTags()
            except Exception as e:
                print("Error calling getSelectedTags:", e)
        else:
            print("Root object not found.")
        return []

    @catch_errors
    def check_all_tags(self):
        """
        Marks all tags as checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.checkAllTags()
            except Exception as e:
                print("Error calling checkAllTags:", e)
        else:
            print("Root object not found.")


class ProductSelectorWidgetPage1(QWidget):
    @catch_errors
    def __init__(self, list_model_name="myListModel", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        qml_code = '''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {
            id: root
            width: 300
            height: 400
            color: "transparent"

            ListView {
                id: tagListView
                anchors.fill: parent
                spacing: 5                    // Vertical spacing between delegates
                model: tagModel
                delegate: Rectangle {
                    id: delegateRect
                    width: tagListView.width   // Screen-wide
                    height: 30                 // Increased height for a larger touch target
                    radius: 10
                    color: model.checked ? "#00B0F0" : "#ffffff"
                    border.width: 1
                    border.color: "gray"

                    Text {
                        id: tagText
                        text: model.text 
                        anchors.centerIn: parent
                        font.pixelSize: 16
                        color: model.checked ? "white" : "black"
                        font.bold: true
                    }

                    // The entire delegate acts as a button.
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            // Toggle the checked state.
                            model.checked = !model.checked;
                            // Reorder the entire model so that all selected items appear on top.
                            reorderSelected();
                        }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Function to reorder the model so that selected items are at the top.
            function reorderSelected() {
                var selectedItems = [];
                var unselectedItems = [];
                // Loop over each item in the model.
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    // Ensure each role has a default value.
                    var fixedItem = {
                        "text": item.text !== undefined ? item.text : "",
                        "id": item.id !== undefined ? item.id : 0,
                        "checked": item.checked !== undefined ? item.checked : false,
                        "qty": item.qty !== undefined ? item.qty : 0,
                        "unit": item.unit !== undefined ? item.unit : ""
                    };
                    if (fixedItem.checked) {
                        selectedItems.push(fixedItem);
                    } else {
                        unselectedItems.push(fixedItem);
                    }
                }
                // Clear the model.
                while (tagModel.count > 0) {
                    tagModel.remove(0);
                }
                // Append selected items first.
                for (var i = 0; i < selectedItems.length; i++) {
                    tagModel.append(selectedItems[i]);
                }
                // Append unselected items.
                for (var i = 0; i < unselectedItems.length; i++) {
                    tagModel.append(unselectedItems[i]);
                }
            }

            // Timer to call reorderSelected after the model is initially populated.
            Timer {
                id: reorderTimer
                interval: 10  // Adjust delay if necessary
                running: false
                repeat: false
                onTriggered: {
                    reorderSelected();
                }
            }

            Component.onCompleted: {
                // Start the timer so that the model is fully populated before reordering.
                reorderTimer.start();
            }

            // Helper function to add a tag into the model.
            function addTag(text, id, checked, qty, unit) {
                tagModel.append({
                    "text": text !== undefined ? text : "",
                    "id": id !== undefined ? id : 0,
                    "checked": checked !== undefined ? checked : false,
                    "qty": qty !== undefined ? qty : 0,
                    "unit": unit !== undefined ? unit : ""
                });
            }
            
            // Helper function to clear all tags from the model.
            function clearTags() {
                while(tagModel.count > 0) {
                    tagModel.remove(0);
                }
            }

            // Helper function to return an array of selected tag IDs.
            function getSelectedTags() {
                var result = [];
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    if (item.checked)
                        result.push({"id": item.id, "quantity": item.qty, "unit": item.unit});
                }
                return result;
            }
        }

        '''

        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        qml_item = component.create()
        self.quick_widget.setContent(QUrl(), component, qml_item)

    @catch_errors
    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

    @catch_errors
    def add_tag(self, text: str, checked: bool = False):
        """
        Adds a tag with the given text and checked state to the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.addTag(text, checked)
            except Exception as e:
                print("Error calling addTag:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def clear_tags(self):
        """
        Clears all tags from the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.clearTags()
            except Exception as e:
                print("Error calling clearTags:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def get_selected_tags(self):
        """
        Retrieves an array of tag texts that are checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                return root_obj.getSelectedTags()
            except Exception as e:
                print("Error calling getSelectedTags:", e)
        else:
            print("Root object not found.")
        return []


class ProductSelectorWidgetPage2(QWidget):
    @catch_errors
    def __init__(self, list_model_name="myListModel", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        qml_code = '''
        import QtQuick 2.15
        import QtQuick.Controls 2.15
        import QtQuick.Layouts 1.15

        Rectangle {
            id: root
            width: 300
            height: 400
            color: "transparent"

            ListView {
                id: tagListView
                anchors.fill: parent
                spacing: 10
                model: tagModel

                delegate: Rectangle {
                    id: delegateRect
                    property int delegateIndex: index  // capture the model index at creation time
                    width: tagListView.width
                    height: 80   // increased height to accommodate two rows
                    radius: 10
                    color: "#00B0F0"
                    border.width: 1
                    border.color: "gray"

                    Column {
                        anchors.fill: parent
                        anchors.margins: 5
                        spacing: 5

                        // First row: display the tag text.
                        Row {
                            Text {
                                id: tagLabel
                                text: model.text       // direct role access
                                font.pixelSize: 16
                                font.bold: true
                                color: "black"
                                verticalAlignment: Text.AlignVCenter
                            }
                        }

                        // Second row: display the TextField and ComboBox.
                        Row {
                            spacing: 10

                            TextField {
                                id: qtyField
                                text: qty.toString()  // using the qty role directly
                                width: 40
                                height: 30
                                inputMethodHints: Qt.ImhDigitsOnly
                                onEditingFinished: {
                                    tagListView.model.setProperty(delegateIndex, "qty", parseInt(text) || 1)
                                }
                            }
                            /*
                            Text {
                                id: tagUnitLabel
                                text: unit       // using the unit role directly
                                font.pixelSize: 16
                                font.bold: false
                                color: "black"
                                verticalAlignment: Text.AlignVCenter
                            }
                            */
                            ComboBox {
                                id: unitCombo
                                // Use a property alias to fall back to "kpl" if unit is empty
                                property string initialUnit: unit !== "" ? unit : "kpl"
                                model: root.getUnitOptions(initialUnit)
                                Component.onCompleted: {
                                    var options = root.getUnitOptions(initialUnit)
                                    var idx = options.indexOf(initialUnit)
                                    currentIndex = idx >= 0 ? idx : 0
                                }
                                onActivated: {
                                    tagListView.model.setProperty(delegateIndex, "unit", currentText)
                                    console.log("Updated unit for delegate index", delegateIndex, "to", currentText)
                                }
                            }
                        }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Helper function to add a tag into the model.
            // If no valid unit is provided, defaults to "kpl".
            function addTag(name, id, qty, unit) {
                console.log("Adding tag:", name, id, qty, unit)
                tagModel.append({
                    "text": name,
                    "id": id,
                    "qty": qty,
                    "unit": unit && unit !== "" ? unit : "kpl"
                });
            }

            // Helper function to clear all tags from the model.
            function clearTags() {
                while (tagModel.count > 0) {
                    tagModel.remove(0);
                }
            }

            // Function to return an array of selected tag objects,
            // which now reflects the unit currently selected in the ComboBox.
            function getSelectedTags() {
                var result = [];
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    result.push({
                        "id": item.id,
                        "qty": item.qty,
                        "unit": item.unit,
                        "name": item.text
                    });
                }
                return result;
            }

            // Function that returns a list of unit options based on the provided unit.
            function getUnitOptions(unit) {
                if (!unit || unit === "") {
                    return ["kpl"];
                }
                if (unit === "kg" || unit === "g" || unit === "mg") {
                    return ["kg", "g", "mg"];
                } else if (unit === "l" || unit === "dl" || unit === "ml") {
                    return ["l", "dl", "ml"];
                } else if (unit === "kpl") {
                    return ["kpl", "l", "dl", "ml", "kg", "g", "mg"];
                }
                // Fallback: return the unit itself.
                return [unit];
            }
        }
        '''

        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        qml_item = component.create()
        self.quick_widget.setContent(QUrl(), component, qml_item)

    @catch_errors
    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

    @catch_errors
    def add_tag(self, text: str, checked: bool = False):
        """
        Adds a tag with the given text and checked state to the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.addTag(text, checked)
            except Exception as e:
                print("Error calling addTag:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def clear_tags(self):
        """
        Clears all tags from the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.clearTags()
            except Exception as e:
                print("Error calling clearTags:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def get_selected_tags(self):
        """
        Retrieves an array of tag IDs that are checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                return root_obj.getSelectedTags()
            except Exception as e:
                print("Error calling getSelectedTags:", e)
        else:
            print("Root object not found.")
        return []


class ShoplistWidget(QWidget):
    @catch_errors
    def __init__(self, list_model_name="myListModel", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        qml_code = '''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {
            id: root
            width: 300
            height: 400
            color: "transparent"
            
            signal itemClicked(var id, var checked, var price)

            ListView {
                id: tagListView
                anchors.fill: parent
                spacing: 5                    // Vertical spacing between delegates
                model: tagModel
                delegate: Rectangle {
                    id: delegateRect
                    width: tagListView.width   // Full width
                    height: 30                 // Increased height for a larger touch target
                    radius: 10
                    // When checked, use gray; when unchecked, use #00B0F0.
                    color: model.checked ? "#d3d3d3" : "#00B0F0"
                    border.width: 1
                    border.color: "gray"

                    Text {
                        id: tagText
                        // Use rich text formatting to allow strike-through.
                        textFormat: Text.RichText
                        // If checked, wrap text with <s> tags to cross it out.
                        text: model.checked ? "<s>" + model.text + " - " + model.qty + " " + model.unit + " - " + model.price.toFixed(2) + "€</s>" : model.text + " - " + model.qty + " " + model.unit + " - " + model.price.toFixed(2) + "€"
                        anchors.centerIn: parent
                        font.pixelSize: 16
                        // Use gray text when checked; otherwise, white text.
                        color: model.checked ? "gray" : "white"
                        font.bold: true
                    }

                    // The entire delegate acts as a button.
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            // Toggle the checked state.
                            model.checked = !model.checked;
                            // Emit the itemClicked signal with the price of the clicked item.
                            itemClicked(model.id, !model.checked, getTotalCost());
                            // Reorder the entire model.
                            reorderSelected();
                        }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Function to reorder the model so that selected items appear at the bottom.
            function reorderSelected() {
                var selectedItems = [];
                var unselectedItems = [];
                // Loop over each item in the model.
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    // Ensure each property has a default value.
                    var fixedItem = {
                        "text": item.text !== undefined ? item.text : "",
                        "id": item.id !== undefined ? item.id : 0,
                        "checked": item.checked !== undefined ? item.checked : false,
                        "qty": item.qty !== undefined ? item.qty : 0,
                        "unit": item.unit !== undefined ? item.unit : "",
                        "price": item.price !== undefined ? item.price : 0.0  // Include the price property
                    };
                    if (fixedItem.checked) {
                        selectedItems.push(fixedItem);
                    } else {
                        unselectedItems.push(fixedItem);
                    }
                }
                // Clear the model.
                while (tagModel.count > 0) {
                    tagModel.remove(0);
                }
                // Append unselected items first.
                for (var i = 0; i < unselectedItems.length; i++) {
                    tagModel.append(unselectedItems[i]);
                }
                // Append selected items next.
                for (var i = 0; i < selectedItems.length; i++) {
                    tagModel.append(selectedItems[i]);
                }
            }


            // Timer to call reorderSelected after the model is initially populated.
            Timer {
                id: reorderTimer
                interval: 10  // Adjust delay if necessary
                running: false
                repeat: false
                onTriggered: {
                    reorderSelected();
                }
            }

            Component.onCompleted: {
                // Start the timer so that the model is fully populated before reordering.
                reorderTimer.start();
            }

            // Helper function to add a tag into the model.
            function addTag(text, id, checked, qty, unit, price) {
                tagModel.append({
                    "text": text !== undefined ? text : "",
                    "id": id !== undefined ? id : 0,
                    "checked": checked !== undefined ? checked : false,
                    "qty": qty !== undefined ? qty : 0,
                    "unit": unit !== undefined ? unit : "",
                    "price": price !== undefined ? price : 0.0  // Added price property
                });
            }
            
            // Helper function to clear all tags from the model.
            function clearTags() {
                while(tagModel.count > 0) {
                    tagModel.remove(0);
                }
            }

            // Helper function to return an array of selected tag IDs.
            function getSelectedTags() {
                var result = [];
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    if (item.checked)
                        result.push({"id": item.id, "qty": item.qty, "unit": item.unit});
                }
                return result;
            }
            
            function getTotalCost() {
                var total = 0;
                for (var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    if (!item.checked) {
                        total += item.price * item.qty;
                    }
                }
                return total;
            }
            
            function setAllChecked() {
                for (var i = 0; i < tagModel.count; i++) {
                    tagModel.setProperty(i, "checked", true);
                }
                // Optionally, reorder the items if needed.
                reorderSelected();
            }
        }
        '''

        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        qml_item = component.create()
        self.quick_widget.setContent(QUrl(), component, qml_item)

    @catch_errors
    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

    @catch_errors
    def add_tag(self, text: str, checked: bool = False):
        """
        Adds a tag with the given text and checked state to the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.addTag(text, checked)
            except Exception as e:
                print("Error calling addTag:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def clear_tags(self):
        """
        Clears all tags from the QML ListModel.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.clearTags()
            except Exception as e:
                print("Error calling clearTags:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def get_selected_tags(self):
        """
        Retrieves an array of tag texts that are checked.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                return root_obj.getSelectedTags()
            except Exception as e:
                print("Error calling getSelectedTags:", e)
        else:
            print("Root object not found.")
        return []
    
    @catch_errors
    def set_all_checked(self):
        """
        Sets all tag items in the QML ListModel to the checked state.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            try:
                root_obj.setAllChecked()
            except Exception as e:
                print("Error calling setAllChecked:", e)
        else:
            print("Root object not found.")

    @catch_errors
    def connect_item_clicked(self, slot):
        """
        Connects a Python slot to the QML 'itemClicked' signal.
        The slot should accept one argument, the itemId.
        """
        root_obj = self.get_root_object()
        if root_obj is not None:
            root_obj.itemClicked.connect(slot)
        else:
            print("Root object not found.")
            raise RuntimeError("Root object not found.")


class ScrollableLabel(QWidget):
    @catch_errors
    def __init__(self, label_id="scrollableLabel", placeholder_text="No text set", parent=None, width=300, height=300):
        super().__init__(parent)
        self.label_id = label_id

        layout = QVBoxLayout(self)
        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.quick_widget)
        self.setLayout(layout)

        # Revised QML:
        # The TextArea is placed inside a ScrollView.
        # We set the ScrollView to fill the Rectangle.
        # The TextArea sets its width to parent.width instead of anchoring completely.
        qml_code = f'''
        import QtQuick 2.15
        import QtQuick.Controls 2.15

        Rectangle {{
            id: root
            width: {width}
            height: {height}
            color: "transparent"
            radius: 3
            border.width: 1
            border.color: "gray"

            ScrollView {{
                anchors.fill: parent

                TextArea {{
                    id: {self.label_id}
                    objectName: "{self.label_id}"  // Enables findChild() by this name
                    width: parent.width
                    font.pixelSize: 16
                    text: "{placeholder_text}"
                    wrapMode: TextArea.Wrap  // Enable word wrapping
                    readOnly: true         // Prevent editing while allowing selection and copy
                    selectByMouse: true    // Allows text selection (works with touch on phones)
                    background: Rectangle {{ color: "transparent" }}  // Custom background if desired
                }}
            }}
        }}
        '''
        component = QQmlComponent(self.quick_widget.engine())
        component.setData(qml_code.encode('utf-8'), QUrl())
        if component.status() != QQmlComponent.Status.Ready:
            for error in component.errors():
                print("QML Error:", error.toString())
        item = component.create()
        self.quick_widget.setContent(QUrl(), component, item)

    @catch_errors
    def get_text(self):
        # Retrieve the QML root object and then the TextArea.
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            text_area = root_obj.findChild(QObject, self.label_id)
            if text_area is not None:
                return text_area.property("text")
        return ""

    @catch_errors
    def set_text(self, text: str):
        """
        Update the text in the read-only scrollable label.
        """
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            text_area = root_obj.findChild(QObject, self.label_id)
            if text_area is not None:
                text_area.setProperty("text", text)
