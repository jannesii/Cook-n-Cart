# error_handler.py

# File: error_handler.py

from typing import Literal
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



def show_error_toast(parent, message, pos: Literal["bot", "mid", "top"] = "bot", duration=3000):
    """
    Display a toast message indicating an error.

    Parameters:
        parent: The parent widget.
        message: The error message to display.
        pos (Literal["bot", "mid", "top"]): Position for the toast.
            "bot" - Bottom of the parent widget (default)
            "mid" - Middle of the parent widget
            "top" - Top of the parent widget
        duration: Duration (in milliseconds) for which the toast is displayed.
    """
    toast = QLabel(parent)
    toast.setText(message)
    toast.setStyleSheet("""
        background-color: red;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    """)
    toast.setAlignment(Qt.AlignCenter)
    toast.setAttribute(Qt.WA_TransparentForMouseEvents)
    toast.resize(int(parent.width() * 0.8), 40)
    
    if pos == "bot":
        height_bot = parent.height() - toast.height() - 20
        toast.move((parent.width() - toast.width()) // 2, height_bot)
    elif pos == "mid":
        height_mid = (parent.height() - toast.height()) // 2
        toast.move((parent.width() - toast.width()) // 2, height_mid)
    else:
        height_top = 20
        toast.move((parent.width() - toast.width()) // 2, height_top)
    toast.show()
    
    QTimer.singleShot(duration, toast.deleteLater)