import sys
import os
import re

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget,QFrame,QCompleter,QListView
from PyQt6.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QFileDialog, QLineEdit,QVBoxLayout,QLabel,QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt,QSize

import searchFiles

# NOTA:
# VERIFICA INTOTDEAUNA LISTA DE FISIERE INAINTE DE STERGEREA DE PE HDD
# Am pastrat avertizarea aceasta :
# SyntaxWarning: invalid escape sequence '\.'  template_list = ['^test.*\.py$', '^test.*\.txt$'] 
# Codul sursa nu este testat 100% 
# Am gasit neconcordante la unele expresii regulate si selectii de dropdown buton 
# Ar fi trebuit să folosim dublul caracter de escape \\ pentru a reprezenta un singur caracter \ pentru a nu avea aceasta avertizare
# insa nu ar mai fi afisata corect expresia regulata si nu sunt sigur ca ar functiona in toate cazurile mai complexe

class FileListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("clean and delete")
        # Se creează un QFrame pentru bara de titlu
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(1080)  # Setează înălțimea dorită
        clean_delete_icon_path = QIcon("icon_clean_delete_re.svg")
        self.setWindowIcon(clean_delete_icon_path)
        self.setGeometry(100, 100, 1280, 860)
        
        # Se creează o listă de șabloane (poți înlocui cu propriile șabloane)
        template_list = ['^test*\.py$', '^test*\.txt$']
        # Creează dicționarul pentru asocieri între șabloane și texte de tooltip
        self.tooltip_dict = {
            '^test*\.py$': "fișierele care încep cu 'test' și se termină cu extensia: '.py'",
            '^test*\.txt$': "fișierele care încep cu 'test' și se termină cu extensia: '.txt'",
            '^0{3}[A-Za-z0-9]*\.tmp$':"fisiere de tip '000...*' și se termină cu extensia: '.tmp' generate de tool backup NOD32 "
        }
        # Creează un QComboBox
        self.dropdown = QComboBox()
        for key, description in self.tooltip_dict.items():
            combined_text = f"{key} - {description}"
            self.dropdown.addItem(combined_text)

        # Creează un QCompleter cu lista de șabloane
        completer = QCompleter(template_list, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
  

        # Se creează un QVBoxLayout pentru zona de afișare (stânga)
        self.file_list = QListWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.file_list)
        # Se creează un QHBoxLayout pentru butoane (dreapta)
        self.folder_button = QPushButton("Selectează Folder")
        self.folder_button.clicked.connect(self.select_folder)
        folder_select = QIcon("folder-svgrepo-com.svg")
        self.folder_button.setIcon(folder_select)

        self.system_button = QPushButton("Selectează curățare sistem")
        self.system_button.clicked.connect(self.system_clean)

        # Label informativ cale folder
        self.label_folder = QLabel("Cale folder in care se cauta : ")

        self.folder_path_edit = QLineEdit()
        # Creează un QListView personalizat pentru a afișa sugestiile
        custom_list_view = QListView()
        completer.setPopup(custom_list_view)

        # Label informativ expresie tip RE
        self.label_RE = QLabel("Expresie regulata cautare nume fisier : ")
        # Label informativ expresie tip RE
        self.label_NOTA1 = QLabel("ATENTIE: Verifica fisierele din lista INAINTE DE STERGERE!")
        self.label_NOTA2 = QLabel("AM gasit neconcordante la mai multe selectii - buton dropdown cu RE txt")
        self.label_NOTA3 = QLabel("NU a gasit fisierele la un singur folder fara recursivitate")
        self.label_NOTA4 = QLabel("Codul sursa rulat nu este testat 100% ")
        # Creează un QLineEdit și asociază QCompleter-ul
        self.regex_edit = QLineEdit()
        self.regex_edit.setCompleter(self.dropdown.completer())

        # Conectează semnalul QCompleter.activated la metoda show_tooltip
        self.dropdown.activated.connect(self.show_tooltip)

        self.load_files_button = QPushButton("Încarcă Fișiere")
        self.load_files_button.clicked.connect(self.load_files)

        self.clear_list_button = QPushButton("Șterge fișierele din listă!")
        self.clear_list_button.clicked.connect(self.clear_list)
        icon_attention = QIcon("attention.svg")
        self.clear_list_button.setIcon(icon_attention)

        self.delete_selected_button = QPushButton("ȘTERGE !!! Fișierele de pe HDD!")
        # Setează geometria (poziție și dimensiune) butonului
        self.delete_selected_button.setIconSize(QSize(32, 32))
        self.delete_selected_button.clicked.connect(self.delete_selected_files)
        icon_delete = QIcon("delete.svg")
        self.delete_selected_button.setIcon(icon_delete)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.folder_button)
        right_layout.addWidget(self.system_button)
        right_layout.addWidget(self.label_folder)
        right_layout.addWidget(self.folder_path_edit)
        right_layout.addWidget(self.label_RE)
        right_layout.addWidget(self.label_NOTA1)
        right_layout.addWidget(self.label_NOTA2)
        right_layout.addWidget(self.label_NOTA3)
        right_layout.addWidget(self.label_NOTA4)
        right_layout.addWidget(self.regex_edit)
        right_layout.addWidget(self.dropdown)
        right_layout.addWidget(self.load_files_button)
        right_layout.addWidget(self.delete_selected_button)
        right_layout.addWidget(self.clear_list_button)

        # Creează un QHBoxLayout pentru a combina cele două layout-uri
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 4)  # 80% pentru zona de afișare
        main_layout.addLayout(right_layout, 1)  # 20% pentru butoane

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Selectează Folder")
        if folder_path:
            self.folder_path_edit.setText(folder_path)
    def system_clean(self):
        # deschide fisier csv si citeste paths pentru curatare
        #system_folders_path = csv_item
        pass

    def load_files(self):
        folder_path = self.folder_path_edit.text()
        regex_pattern = self.regex_edit.text()
        self.file_list.clear()
        self.add_files_recursive(folder_path, regex_pattern)

    def add_files_recursive(self, directory, regex_pattern):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if re.match(regex_pattern, file):
                    item = QListWidgetItem(os.path.join(root, file))
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Checked)  # Setează opțiunea de check la Checked
                    self.file_list.addItem(item)

    def delete_selected_files(self):
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                file_path = item.text()
                os.remove(file_path)
        self.load_files()

    def clear_list(self):
        self.file_list.clear()

    def show_tooltip(self, index):
        selected_text = self.dropdown.itemText(index)
        key, _ = selected_text.split(" - ", 1)
        self.regex_edit.setText(key)
        tooltip_text = self.tooltip_dict.get(key, "")
        self.regex_edit.setToolTip(tooltip_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    searcher = searchFiles.FileSearcher(".*\.txt") 
    window = FileListApp()
    window.show()
    sys.exit(app.exec())
