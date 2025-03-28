from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl, QObject
from PySide6.QtQml import QQmlComponent
from PySide6.QtWidgets import QWidget, QVBoxLayout

class QmlTextFieldWidget(QWidget):
    def __init__(self, text_field_id="mobileTextField", parent=None):
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

            TextField {{
                id: {self.text_field_id}
                objectName: "{self.text_field_id}"  // Set the objectName so findChild() can locate this element
                anchors.fill: parent
                font.pixelSize: 16
                placeholderText: "Enter value..."
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
