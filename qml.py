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
                placeholderText: "{placeholder_text}"
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
                placeholderText: "{placeholder_text}"
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
            width: 300
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
                        width: parent.width * 0.98
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
