# error_handler.py

# File: error_handler.py

import functools
import logging
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QLabel
from PySide6.QtCore import Qt, QTimer

def catch_errors_ui(func):
    """
    Decorator that logs the error, shows an error dialog (if a QApplication exists),
    and then re-raises the exception.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            print(f"Error in {func.__name__}: {e}")
            if False: #QApplication.instance():
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("Error")
                # Avoid showing overly technical details to the user.
                msg_box.setText("An unexpected error occurred. Please try again later.")
                msg_box.exec()
            raise
    return wrapper

def catch_errors(func):
    """
    A simpler decorator that logs the error (with traceback) and then re-raises the exception.
    Use this when you do not want to show a user dialog.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            print(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt, QSysInfo

def show_error_toast(parent, message, duration=3000):
    if QSysInfo().productType() == 'android':
        # Use native Android toast via JNI
        from PySide6.QtCore import QAndroidJniObject
        # Get the Android application context
        context = QAndroidJniObject.callStaticObjectMethod(
            "android/app/ActivityThread",
            "currentApplication",
            "()Landroid/app/Application;"
        )
        # Create and show the native Toast (0 for short duration, 1 for long)
        QAndroidJniObject.callStaticMethod(
            "android/widget/Toast",
            "makeText",
            "(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;",
            context.object(),
            QAndroidJniObject.fromString(message).object(),
            0
        ).callMethod("show", "()V")
    else:
        # Create a custom QLabel-based toast for non-Android platforms
        toast = QLabel(parent)
        toast.setText(message)
        toast.setStyleSheet("""
            background-color: rgba(50, 50, 50, 0.8);
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        toast.setAlignment(Qt.AlignCenter)
        toast.setAttribute(Qt.WA_TransparentForMouseEvents)
        # Position and size the toast near the bottom of the parent widget
        toast.resize(int(parent.width() * 0.8), 40)
        toast.move((parent.width() - toast.width()) // 2, parent.height() - toast.height() - 20)
        toast.show()
        # Automatically remove the toast after the specified duration
        QTimer.singleShot(duration, toast.deleteLater)

