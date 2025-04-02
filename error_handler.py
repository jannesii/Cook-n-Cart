# error_handler.py

# File: error_handler.py

import functools
import logging
import sys
from PySide6.QtWidgets import QApplication, QMessageBox

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
