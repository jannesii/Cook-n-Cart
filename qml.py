# qml.py

from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl, QObject
from PySide6.QtQml import QQmlComponent
from PySide6.QtWidgets import QWidget, QVBoxLayout


class NormalTextField(QWidget):
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
            height: 40
            color: "transparent"
            radius: 5

            TextField {{
                id: {self.text_field_id}
                objectName: "{self.text_field_id}"  // Set the objectName so findChild() can locate this element
                anchors.fill: parent
                font.pixelSize: 16
                placeholderText: " {placeholder_text}"
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

    def get_text(self):
        # Retrieve the QML root object
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            # Use the dynamic id to find the TextField
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                return text_field.property("text")
        return ""

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
            radius: 5

            TextField {{
                id: {self.text_field_id}
                objectName: "{self.text_field_id}"  // Set the objectName so findChild() can locate this element
                anchors.fill: parent
                font.pixelSize: 16
                placeholderText: " {placeholder_text}"
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

    def get_text(self):
        # Retrieve the QML root object
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            # Use the dynamic id to find the TextField
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                return text_field.property("text")
        return ""

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
            radius: 5

            // Signal to propagate text changes.
            signal textChanged(string newText)

            TextField {{
                id: {self.text_field_id}
                objectName: "{self.text_field_id}"  // So findChild() can locate it if needed.
                anchors.fill: parent
                font.pixelSize: 16
                placeholderText: " {placeholder_text}"
                onTextChanged: root.textChanged(text)
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

    def get_text(self):
        # Retrieve the QML root object and then the TextField by its id.
        root_obj = self.quick_widget.rootObject()
        if root_obj is not None:
            text_field = root_obj.findChild(QObject, self.text_field_id)
            if text_field is not None:
                return text_field.property("text")
        return ""

    def get_root_object(self):
        return self.quick_widget.rootObject()


class ScrollViewWidget(QWidget):
    def __init__(self, list_model_name="myListModel", parent=None):
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
            height: 200

            // Signal emitted when an item is clicked. Sends the productId.
            signal itemClicked(var productId)

            ListView {{
                id: listView
                anchors.fill: parent
                model: {self.list_model_name}
                delegate: Item {{
                    width: listView.width   // Use ListView's width instead of parent's width.
                    height: 50

                    Rectangle {{
                        id: itemRect
                        width: parent.width 
                        height: 45
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

    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

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
            height: 400
            color: "transparent"

            ListView {
                id: tagListView
                anchors.fill: parent
                spacing: 10                    // Add this line to set vertical spacing
                model: tagModel
                delegate: Rectangle {
                    id: delegateRect
                    width: tagListView.width   // Screen-wide
                    height: 45                 // Increase height for a larger touch target
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
                        onClicked: { model.checked = !model.checked }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Helper function to add a tag into the model.
            function addTag(text, checked) {
                tagModel.append({"text": text, "checked": checked});
            }

            // Helper function to clear all tags from the model.
            function clearTags() {
                while(tagModel.count > 0) {
                    tagModel.remove(0);
                }
            }

            // Helper function to return an array of selected tag texts.
            function getSelectedTags() {
                var result = [];
                for(var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    if(item.checked)
                        result.push(item.text);
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

    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

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


class ProductSelectorWidgetPage1(QWidget):

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
                spacing: 10                    // Add this line to set vertical spacing
                model: tagModel
                delegate: Rectangle {
                    id: delegateRect
                    width: tagListView.width   // Screen-wide
                    height: 45                 // Increase height for a larger touch target
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
                        onClicked: { model.checked = !model.checked }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Helper function to add a tag into the model.
            function addTag(text, id, checked) {
                tagModel.append({"text": text, "id": id, "checked": checked});
            }

            // Helper function to clear all tags from the model.
            function clearTags() {
                while(tagModel.count > 0) {
                    tagModel.remove(0);
                }
            }

            // Helper function to return an array of selected tag texts.
            function getSelectedTags() {
                var result = [];
                for(var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    if(item.checked)
                        result.push(item.id);
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

    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

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
                    height: 60
                    radius: 10
                    color: "#00B0F0"
                    border.width: 1
                    border.color: "gray"

                    Row {
                        anchors.fill: parent
                        anchors.margins: 5
                        spacing: 10

                        Text {
                            id: tagLabel
                            text: model.text
                            font.pixelSize: 16
                            font.bold: true
                            color: "black"
                            verticalAlignment: Text.AlignVCenter
                        }

                        TextField {
                            id: qtyField
                            text: model.qty.toString()
                            width: 40
                            inputMethodHints: Qt.ImhDigitsOnly
                            onEditingFinished: {
                                // Update the model via setProperty to ensure proper ListModel update.
                                tagListView.model.setProperty(delegateIndex, "qty", parseInt(text) || 1)
                            }
                        }

                        ComboBox {
                            id: unitCombo
                            model: ["kpl", "kg", "l"]

                            // Delay the initialization until after the delegate is fully set up.
                            Timer {
                                interval: 0   // triggers as soon as possible after construction
                                running: true
                                repeat: false
                                onTriggered: {
                                    unitCombo.currentIndex = model.unit === "kpl" ? 0 :
                                                (model.unit === "kg" ? 1 :
                                                (model.unit === "l" ? 2 : 0))
                                }
                            }

                            // Use onActivated with an explicit function signature to avoid parameter injection issues.
                            onActivated: function(activatedIndex) {
                                // Use the stored delegateIndex rather than the potentially shadowed "index"
                                tagListView.model.setProperty(delegateIndex, "unit", currentText)
                                console.log("Updated unit for delegate index", delegateIndex, "to", currentText)
                            }
                        }
                    }
                }
            }

            ListModel {
                id: tagModel
            }

            // Helper function to add a tag into the model.
            // The id defaults to the text value if not provided.
            function addTag(name, id, qty, unit) {
                tagModel.append({"text": name, "id": id, "qty": qty, "unit": unit});
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
                for(var i = 0; i < tagModel.count; i++) {
                    var item = tagModel.get(i);
                    
                    result.push({"id": item.id, "qty": item.qty, "unit": item.unit, "name": item.text});
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

    def get_root_object(self) -> QObject:
        """Returns the root QML object for further interactions."""
        return self.quick_widget.rootObject()

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
