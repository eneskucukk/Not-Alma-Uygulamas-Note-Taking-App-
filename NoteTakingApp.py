import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QListWidget
)
from PyQt5.QtCore import Qt

class NoteTakingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Not Alma Uygulaması")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Not başlığı girişi
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Not başlığını girin...")
        self.layout.addWidget(self.title_input)

        # Not içeriği girişi
        self.content_input = QTextEdit()
        self.layout.addWidget(self.content_input)

        # Notları listelemek için liste widget'ı
        self.notes_list = QListWidget()
        self.layout.addWidget(self.notes_list)

        # Kaydet ve Sil butonları
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_note)
        self.layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete_note)
        self.layout.addWidget(self.delete_button)

        # Notları yükle
        self.load_notes()

        # Liste öğesinin seçilmesi durumunda içeriği göster
        self.notes_list.itemClicked.connect(self.display_note)

    def save_note(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()

        if title and content:
            note = {"title": title, "content": content}
            notes = self.load_existing_notes()
            notes.append(note)
            with open("notes.json", "w") as file:
                json.dump(notes, file)
            self.notes_list.addItem(title)
            self.title_input.clear()
            self.content_input.clear()
        else:
            print("Lütfen hem başlık hem de içerik girin.")

    def load_notes(self):
        notes = self.load_existing_notes()
        for note in notes:
            self.notes_list.addItem(note["title"])

    def load_existing_notes(self):
        try:
            with open("notes.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def display_note(self, item):
        selected_note = item.text()
        notes = self.load_existing_notes()
        for note in notes:
            if note["title"] == selected_note:
                self.title_input.setText(note["title"])
                self.content_input.setPlainText(note["content"])

    def delete_note(self):
        selected_item = self.notes_list.currentItem()
        if selected_item:
            title_to_delete = selected_item.text()
            notes = self.load_existing_notes()
            notes = [note for note in notes if note["title"] != title_to_delete]
            with open("notes.json", "w") as file:
                json.dump(notes, file)
            self.notes_list.takeItem(self.notes_list.row(selected_item))
            self.title_input.clear()
            self.content_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteTakingApp()
    window.show()
    sys.exit(app.exec_())

