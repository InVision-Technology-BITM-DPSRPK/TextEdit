import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QShortcut, QKeySequence
from ui.window import Ui_MainWindow
from speech_lib.speech import speak
import enchant
import subprocess 
from PySide6.QtCore import QFile

def loadUiWidget(uifilename, parent=None):
    loader = QUiLoader()
    uifile = QFile(uifilename)
    uifile.open(QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui

def predict(word):
    d = enchant.Dict('en_US')
    return d.suggest(word)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.textBox.textChanged.connect(self.give_predictions)

        self.enter_text_sc = QShortcut(
            QKeySequence("Ctrl+Return"),
            self
        )

        self.read_predictions_sc = QShortcut(
            QKeySequence("Ctrl+Shift+Return"),
            self
        )

        self.read_last_word_sc = QShortcut(
            QKeySequence("Ctrl+Shift+/"),
            self
        )

        self.read_line_sc = QShortcut(
            QKeySequence("Ctrl+Alt+/"),
            self
        )

        self.copyall_sc = QShortcut(
            QKeySequence("Ctrl+Shift+C"),
            self
        )

        self.enter_text_sc.activated.connect(self.read_full)
        self.read_last_word_sc.activated.connect(self.read_last_word)
        self.read_line_sc.activated.connect(self.read_line)
        self.read_predictions_sc.activated.connect(self.read_predictions)
        self.copyall_sc.activated.connect(self.copyall)
    
    def read_full(self):
        tx = self.ui.textBox.toPlainText()
        speak(tx)

    def read_line(self):
        tx = self.ui.textBox.toPlainText()
        lines = tx.split("\n")
        speak(lines[-1])
    
    def read_last_word(self):
        tx = self.ui.textBox.toPlainText()
        ll = tx.split("\n")[-1]
        lw = ll.split(" ")[-1]
        speak(lw)

    def give_predictions(self):
        tx = self.ui.textBox.toPlainText()
        ll = tx.split("\n")[-1]
        lw = ll.split(" ")[-1]
        predictions = predict(lw)
        self.ui.suggestions.clear()
        self.ui.suggestions.addItems(predictions)
    
    def read_predictions(self):
        tx = self.ui.textBox.toPlainText()
        ll = tx.split("\n")[-1]
        lw = ll.split(" ")[-1]
        predictions = predict(lw)
        speak("Predictions are:")
        for item in predictions:
            speak(item)
    
    def copyall(self):
        tx = self.ui.textBox.toPlainText()
        cb = QApplication.clipboard()
        cb.clear()
        cb.setText(tx)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setFixedHeight(414)
    window.setFixedWidth(744)
    window.setWindowTitle("TexEd")
    window.show()

    sys.exit(app.exec())