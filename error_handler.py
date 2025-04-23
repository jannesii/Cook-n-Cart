# File: error_handler.py --------------------------------------------------------------------

from typing import Literal
import functools
import traceback
import logging
from PySide6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, QEventLoop

_error_controller_instance = None


def get_error_controller():
    """Lazily import and return the global ErrorController instance."""
    global _error_controller_instance
    if _error_controller_instance is None:
        from root_controllers import ErrorController
        _error_controller_instance = ErrorController()
    return _error_controller_instance


def catch_errors_ui(func):
    """
    Decorator that logs the error, shows a toast error message (if a QApplication exists),
    logs the error to the database via ErrorController, and then re-raises the exception.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            print(f"Error in {func.__name__}: {e}")

            # Use the lazy getter to retrieve the controller.
            get_error_controller().log_error(
                error_message=str(e),
                tb=traceback.format_exc(),
                func_name=func.__name__,
            )

            # Check if a QApplication exists.
            app = QApplication.instance()
            if app is not None:
                # Attempt to determine a parent widget from the first argument.
                if args and hasattr(args[0], "width") and hasattr(args[0], "height"):
                    parent = args[0]
                else:
                    parent = app.activeWindow()

                if parent is not None:
                    show_error_toast(
                        parent,
                        message="An unexpected error occurred.\nPlease check the logs for more details.",
                        pos="top",
                        lines=2
                    )
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
            get_error_controller().log_error(
                error_message=str(e),
                tb=traceback.format_exc(),
                func_name=func.__name__,
            )
            print(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


def show_error_toast(
    parent,
    message: str = "An unexpected error occurred.",
    pos: Literal["bot", "mid", "top"] = "top",
    duration: int = 3000,
    background_color: str = "red",
    text_color: str = "white",
    lines: int = 1
):
    """
    Display a toast message indicating an error.

    Parameters:
        parent: The parent widget.
        message: The error message to display.
        pos (Literal["bot", "mid", "top"]): Position for the toast.
        duration: Duration (in milliseconds) for which the toast is displayed.
        background_color: Background color of the toast.
        text_color: Text color of the toast.
        lines: Number of lines in the message (for height calculation).
    """
    toast = QLabel(parent)
    toast.setText(message)
    toast.setStyleSheet(f"""
        background-color: {background_color};
        color: {text_color};
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    """)
    toast.setAlignment(Qt.AlignCenter)
    toast.setAttribute(Qt.WA_TransparentForMouseEvents)
    toast.resize(int(parent.width() * 0.8), 40 * lines)

    # Create and configure the drop shadow effect.
    shadow = QGraphicsDropShadowEffect(toast)
    shadow.setBlurRadius(15)
    shadow.setOffset(3, 3)
    shadow.setColor(Qt.black)
    toast.setGraphicsEffect(shadow)

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


def ask_confirmation(
    parent,
    message: str = "Oletko varma?",
    pos: Literal["bot", "mid", "top"] = "mid",
    yes_text: str = "Kyllä",
    no_text: str = "Ei",
) -> bool:
    """
    Display a confirmation overlay with two buttons ("Kyllä" and "Ei")
    over the parent widget. Returns True if "Kyllä" is clicked, False if "Ei".
    """
    container = QWidget(parent)
    container.setStyleSheet("background: transparent;")
    container.setGeometry(0, 0, parent.width(), parent.height())
    container.show()
    container.raise_()

    confirmation = QWidget(container)
    confirmation.setStyleSheet("""
        background-color: lightgray;
        border-radius: 5px;
    """)

    shadow = QGraphicsDropShadowEffect(confirmation)
    shadow.setBlurRadius(15)
    shadow.setOffset(3, 3)
    shadow.setColor(Qt.black)
    confirmation.setGraphicsEffect(shadow)

    conf_layout = QVBoxLayout(confirmation)
    conf_layout.setContentsMargins(10, 10, 10, 10)

    label = QLabel(message, confirmation)
    label.setStyleSheet("color: black; font-weight: bold;")
    label.setAlignment(Qt.AlignCenter)
    conf_layout.addWidget(label)

    button_layout = QHBoxLayout()
    btn_yes = QPushButton(yes_text, confirmation)
    btn_yes.setStyleSheet("background-color: red; color: white;")
    btn_no = QPushButton(no_text, confirmation)
    btn_no.setStyleSheet("background-color: white; color: black;")
    button_layout.addWidget(btn_yes)
    button_layout.addWidget(btn_no)
    conf_layout.addLayout(button_layout)

    confirmation.resize(int(parent.width() * 0.8), 100)

    if pos == "bot":
        y = parent.height() - confirmation.height() - 20
    elif pos == "mid":
        y = (parent.height() - confirmation.height()) // 2
    else:
        y = 20
    confirmation.move((parent.width() - confirmation.width()) // 2, y)
    confirmation.show()

    loop = QEventLoop()
    result = None

    def on_yes():
        nonlocal result
        result = True
        loop.quit()

    def on_no():
        nonlocal result
        result = False
        loop.quit()

    btn_yes.clicked.connect(on_yes)
    btn_no.clicked.connect(on_no)

    loop.exec()

    container.deleteLater()
    return result
