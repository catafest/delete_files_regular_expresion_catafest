from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QLineEdit, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Dicționarul cu conținut pentru dropdown
        self.tooltip_dict = {
            '^test*\\.py$': "fișierele care încep cu 'test' și se termină cu extensia: '.py'",
            '^test*\\.txt$': "fișierele care încep cu 'test' și se termină cu extensia: '.txt'",
            '^0{3}[A-Za-z0-9]*\\.tmp$': "fișiere de tip '000...*' și se termină cu extensia: '.tmp' generate de tool backup NOD32"
        }

        # Creează un QComboBox
        self.dropdown = QComboBox()
        for key, description in self.tooltip_dict.items():
            combined_text = f"{key} - {description}"
            self.dropdown.addItem(combined_text)

        # Adaugă un label informativ
        self.label_RE = QLabel("Expresie regulată căutare nume fișier:")
        self.regex_edit = QLineEdit()
        self.regex_edit.setCompleter(self.dropdown.completer())

        # Conectează semnalul QCompleter.activated la metoda show_tooltip
        self.dropdown.activated.connect(self.show_tooltip)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_RE)
        layout.addWidget(self.regex_edit)
        layout.addWidget(self.dropdown)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_tooltip(self, index):
        selected_text = self.dropdown.itemText(index)
        key, _ = selected_text.split(" - ", 1)
        self.regex_edit.setText(key)
        tooltip_text = self.tooltip_dict.get(key, "")
        self.regex_edit.setToolTip(tooltip_text)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
