import sys
import os
import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget
from PyQt6.QtWidgets import QCheckBox, QListWidgetItem, QHBoxLayout, QFileDialog, QLineEdit
from PyQt6.QtCore import Qt

class FileListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Listare Fișiere")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        self.folder_button = QPushButton("Selectează Folder")
        self.folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.folder_button)

        self.folder_path_edit = QLineEdit()
        self.layout.addWidget(self.folder_path_edit)

        self.regex_edit = QLineEdit()
        self.layout.addWidget(self.regex_edit)

        self.load_files_button = QPushButton("Încarcă Fișiere")
        self.load_files_button.clicked.connect(self.load_files)
        self.layout.addWidget(self.load_files_button)

        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        self.delete_selected_button = QPushButton("Șterge Fișiere Selectate")
        self.delete_selected_button.clicked.connect(self.delete_selected_files)
        self.layout.addWidget(self.delete_selected_button)

        self.clear_list_button = QPushButton("Șterge Listă")
        self.clear_list_button.clicked.connect(self.clear_list)
        self.layout.addWidget(self.clear_list_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Selectează Folder")
        if folder_path:
            self.folder_path_edit.setText(folder_path)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileListApp()
    window.show()
    sys.exit(app.exec())
