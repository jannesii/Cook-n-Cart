# ostoslistat_page.py

from PySide6.QtWidgets import (
    QWidget,QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, 
)

from controllers import ProductController as PC
from controllers import ShoppingListController as SLC
from controllers import RecipeController as RC


TURKOOSI = "#00B0F0"
HARMAA = "#808080"

RecipeController = RC()
ProductController = PC()
ShoppingListController = SLC()

class OstolistatPage(QWidget):
    """
    Ostolistat-sivu:
      - Yläpalkki: "Ostoslistat" -otsikko vasemmalla, "Uusi ostolista" -nappi oikealla
      - Keskialue: esim. "Ruokaostokset 0/16", "Motonet 0/5", "Biltema 0/11" -napit
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # -- Yläpalkki --
        top_bar_layout = QHBoxLayout()
        label = QLabel("Ostoslistat")
        label.setStyleSheet("font-weight: bold; font-size: 18px;")

        # Esimerkin "Uusi ostolista" -nappi
        new_list_btn = QPushButton("Uusi ostolista")
        new_list_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TURKOOSI};
                color: black;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }}
        """)

        top_bar_layout.addWidget(label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(new_list_btn)

        # Värjätään yläpalkin tausta harmaaksi asettamalla QFrame
        top_bar_frame = QFrame()
        top_bar_frame.setLayout(top_bar_layout)
        top_bar_frame.setStyleSheet(
            f"background-color: {HARMAA}; border-radius: 10px;")

        main_layout.addWidget(top_bar_frame, 0)  # yläpalkki

        # -- Scrollattava keskialue, jos listoja on paljon --
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Esimerkkilistat
        shopping_lists = [
            "Ruokaostokset \n0/16",
            "Motonet \n0/5",
            "Biltema \n0/11"
        ]

        for item in shopping_lists:
            btn = QPushButton(item)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TURKOOSI};
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left; /* Teksti vasemmalle */
                }}
            """)
            scroll_layout.addWidget(btn)

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area, 1)


