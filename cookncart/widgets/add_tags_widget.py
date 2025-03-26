# File: add_tags_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QStackedWidget
)
from PySide6.QtCore import Signal, Qt

TURKOOSI = "#00B0F0"
HARMAA = "#808080"

class AddTagsWidget(QWidget):
    finished = Signal(list)  # Emittaa valittujen tagien listan (merkkijonoina)

    def __init__(self, recipe_controller, parent=None):
        super().__init__(parent)
        self.recipe_controller = recipe_controller
        self.selected_tags = []  # Lista valituista tageista
        # Haetaan kaikki tagit ja varmistetaan uniikkius
        self.all_tags = sorted(set(self.recipe_controller.get_all_tags()))
        
        self.outer_layout = QVBoxLayout(self)
        # QStackedWidget: 
        # - Page 0: olemassa olevien tagien valinta
        # - Page 1: uuden tagin lisäämislomake
        self.stacked = QStackedWidget()
        
        # Page 0: Tagien valinta
        self.page_list = QWidget()
        self.page_list.setLayout(self._create_list_layout())
        # Page 1: Uuden tagin lisääminen
        self.page_add = QWidget()
        self.page_add.setLayout(self._create_add_form_layout())
        
        self.stacked.addWidget(self.page_list)  # index 0
        self.stacked.addWidget(self.page_add)   # index 1
        self.stacked.setCurrentIndex(0)
        
        self.outer_layout.addWidget(self.stacked)
        self.setLayout(self.outer_layout)
    
    def _create_list_layout(self):
        layout = QVBoxLayout()
        
        # Hakukenttä tageille
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Hae tageja")
        self.search_bar.textChanged.connect(self._filter_tag_list)
        layout.addWidget(self.search_bar)
        
        # Lista, jossa tagit näytetään: jokainen on checkable
        self.tag_list_widget = QListWidget()
        layout.addWidget(self.tag_list_widget)
        self._refresh_tag_list()
        
        # Nappirivi: "Lisää uusi tagi", OK ja Peruuta
        btn_layout = QHBoxLayout()
        self.add_new_btn = QPushButton("Lisää uusi tagi")
        self.add_new_btn.clicked.connect(self._open_add_tag_page)
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self._finish_selection)
        self.cancel_btn = QPushButton("Peruuta")
        self.cancel_btn.clicked.connect(self._cancel_selection)
        btn_layout.addWidget(self.add_new_btn)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        return layout
    
    def _create_add_form_layout(self):
        layout = QVBoxLayout()
        
        # Yksinkertainen kenttä uuden tagin syöttämistä varten
        self.new_tag_edit = QLineEdit()
        self.new_tag_edit.setPlaceholderText("Anna uusi tagi")
        layout.addWidget(self.new_tag_edit)
        
        # Nappi uuden tagin tallentamiseen ja takaisin listaan
        btn_layout = QHBoxLayout()
        self.save_new_tag_btn = QPushButton("Tallenna")
        self.save_new_tag_btn.clicked.connect(self._save_new_tag)
        self.back_btn = QPushButton("Takaisin")
        self.back_btn.clicked.connect(self._back_to_list_page)
        btn_layout.addWidget(self.save_new_tag_btn)
        btn_layout.addWidget(self.back_btn)
        layout.addLayout(btn_layout)
        
        return layout
    
    def _refresh_tag_list(self, filtered_tags=None):
        self.tag_list_widget.clear()
        # Näytetään joko kaikki tagit tai suodatetut
        tags_to_show = filtered_tags if filtered_tags is not None else self.all_tags
        for tag in tags_to_show:
            item = QListWidgetItem(tag)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if tag in self.selected_tags:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.tag_list_widget.addItem(item)
        self.tag_list_widget.sortItems(Qt.AscendingOrder)
    
    def _filter_tag_list(self):
        query = self.search_bar.text().strip().lower()
        if not query:
            self._refresh_tag_list()
            return
        filtered = [tag for tag in self.all_tags if query in tag.lower()]
        self._refresh_tag_list(filtered_tags=filtered)
    
    def _open_add_tag_page(self):
        self.stacked.setCurrentIndex(1)
    
    def _back_to_list_page(self):
        self.stacked.setCurrentIndex(0)
    
    def _save_new_tag(self):
        new_tag = self.new_tag_edit.text().strip()
        if new_tag and new_tag not in self.all_tags:
            self.all_tags.append(new_tag)
            self.all_tags = sorted(set(self.all_tags))
            # Voidaan valita automaattisesti myös uusi tagi
            self.selected_tags.append(new_tag)
        self.new_tag_edit.clear()
        self._back_to_list_page()
        self._refresh_tag_list()
    
    def _finish_selection(self):
        self.selected_tags = []
        for i in range(self.tag_list_widget.count()):
            item = self.tag_list_widget.item(i)
            if item.checkState() == Qt.Checked:
                self.selected_tags.append(item.text())
        self.finished.emit(self.selected_tags)
    
    def _cancel_selection(self):
        self.finished.emit(self.selected_tags)
