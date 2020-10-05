__version__ = "1.0"
__author__ = "Wizzy | Techcrest.com"

from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout
import sys

# List to hold the word dictionaries
word_bank = []
words = open("new_words.txt", 'r')
new_words = words.read()
new_wordz = new_words.split("\n")

# create a list from the file content
for word in new_wordz:
    if len(word) > 5:
        word_bank.append(word)


class PygameUi(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setting Application Window Properties
        self.setWindowTitle("Scrambler")
        self.setFixedSize(250, 230)
        self.setStyleSheet("background-color: purple")
        self.setWindowIcon(QtGui.QIcon("icon1.png"))
        self.status = self.statusBar()
        self.status.showMessage(f"Scrambler V{__version__} By: {__author__}")
        self.status.setStyleSheet("color: white; font-weight: bold;")
        self.setStatusBar(self.status)

        # Create and set Layout
        self.generalLayout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)

        # Widget Content
        self.heading = QLabel("<h1> WELCOME TO <br>WORD SCRAMBLER </h1>")
        self.heading.setStyleSheet("color: yellow; font-weight:bold; font-family: Arial")
        self.heading.setAlignment(Qt.AlignHCenter)
        self.generalLayout.addWidget(self.heading)
        # Buttons, Labels and other widgets
        self.btnLayout = QGridLayout()
        self.quitBtn = QPushButton(self)
        self.playBtn = QPushButton(self)
        self.playBtn.setText("Play Now")
        self.quitBtn.setText("Quit")
        self.playBtn.setStyleSheet("background-color: yellow; color: purple; margin-bottom: 30px; height:auto; font-weight: bold")
        self.quitBtn.setStyleSheet("background-color: red; color: white;height:auto; margin-bottom: 30px; font-weight: bold")
        self.btnLayout.addWidget(self.quitBtn, 0, 1)
        self.btnLayout.addWidget(self.playBtn, 0, 0)

        self.generalLayout.addLayout(self.btnLayout)
        # Initiate GameCtrl  class to use its methods
        self.ctrl = GameCtrl(self)
        self._connectSignals()

    def _connectSignals(self):
        self.playBtn.clicked.connect(self.ctrl.new_game)
        self.quitBtn.clicked.connect(self.ctrl.quit_game)


class PlayGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrambler")
        self.setFixedSize(250, 250)
        self.setStyleSheet("background-color: purple")
        self.setWindowIcon(QtGui.QIcon("icon1.png"))
        self.status = self.statusBar()
        self.status.showMessage(f"Scrambler V{__version__} By: {__author__}")
        self.status.setStyleSheet("color: white; font-weight: bold;")
        self.setStatusBar(self.status)

        # Create and set Layout
        self.generalLayout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)

        # Widget Content
        self.heading = QLabel("<h1> WORD SCRAMBLER </h1>")
        self.heading.setStyleSheet("color: yellow; font-weight:bold; font-family: Arial")
        self.heading.setAlignment(Qt.AlignHCenter)
        self.generalLayout.addWidget(self.heading)
        # Buttons, Labels and other widgets
        self.myLabel = QLabel()
        self.scrambled_word = self.get_scrambled_word()
        self.myLabel.setText(f"<h2 style='color: white; font-weight: bold; text-align: center;'>Unscramble the word <br><span style='color: yellow; font-weight: bold; '>({self.scrambled_word[0]})</span> </h2>")
        self.hint = QLabel(f"<p style='color:white; font-weight: bold'>Hint: {self.scrambled_word[1][0]}{int((len(self.scrambled_word[1])-2)) *'*'}{self.scrambled_word[1][-1]}</p>")
        self.userInput = QLineEdit()
        self.msg = QLabel()
        self.msg.setStyleSheet("color: orange; font-weight: bold; text-transform: upper-case")
        self.userInput.setStyleSheet("height: 35px; background-color: white; font-size: 18px; color:purple ")
        # Add the above widgets to generalLayout
        self.generalLayout.addWidget(self.myLabel)
        self.generalLayout.addWidget(self.hint)
        self.generalLayout.addWidget(self.userInput)
        self.generalLayout.addWidget(self.msg)

        # button layout section
        self.btnLayout = QGridLayout()
        self.okBtn = QPushButton("OK")
        self.mainBtn = QPushButton("End Game")
        self.okBtn.setStyleSheet("background-color: white; color: purple; margin-bottom:0px; height:auto; font-weight: bold")
        self.mainBtn.setStyleSheet("background-color: red; color: white;  height:auto; font-weight: bold")
        self.btnLayout.addWidget(self.okBtn, 0, 0)
        self.btnLayout.addWidget(self.mainBtn, 0, 1)
        self.generalLayout.addLayout(self.btnLayout)

        # call to signals
        self.mainBtn.clicked.connect(self.mainMenu)
        self.okBtn.clicked.connect(self.start_game)

        # GameCtrl Initialization
        self.ctrl = GameCtrl(self)

    def mainMenu(self):
        self.ctrl._ui.close()
        self.ctrl._ui = PygameUi()
        self.ctrl._ui.show()

    # This section controls the scrambled word generation
    def get_scrambled_word(self):
        import random
        random_word = random.choice(word_bank)
        random_word.upper()
        scrambled_word = "".join(random.sample(random_word, len(random_word)))
        return scrambled_word, random_word

    def start_game(self):
        import time

        def check_answer():
            random_word = self.scrambled_word[1]
            answer = self.userInput.text()

            if answer == random_word:
                self.msg.setText("Congratulations!! You're a Scramble Lord")
                self.userInput.setReadOnly(True)
                self.okBtn.setText("Play Again")
                self.mainBtn.setText("End Game")
                self.okBtn.clicked.connect(self.ctrl.new_game)
                self.mainBtn.clicked.connect(self.mainMenu)
            else:
                self.msg.setText(f"Incorrect, Please Try again")
                self.mainBtn.setText("New Word")
                self.mainBtn.clicked.connect(self.ctrl.new_game)

        check_answer()
        self.userInput.setText("")


class GameCtrl:
    def __init__(self, ui):
        self._ui = ui

    def new_game(self):
        self._ui.close()
        self._ui = PlayGame()
        self._ui.show()

    def quit_game(self):
        quit()


def main():
    app = QApplication(sys.argv)
    ui = PygameUi()
    ui.show()
    GameCtrl(ui=ui)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

