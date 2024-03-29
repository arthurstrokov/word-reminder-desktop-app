from PyQt5 import QtWidgets

from service.abbyy_parse import get_duplicate
from service.file_handling import load_data, save_data, show_random_word
from ui.mydesign import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # connecting the clicked signal with btnClicked slot
        self.ui.pushButton.clicked.connect(self.btnClicked)
        self.ui.pushButton_2.clicked.connect(self.btnClicked_2)
        self.ui.pushButton_3.clicked.connect(self.btnClicked_3)

    def btnClicked(self):
        file_name = 'data/two_thousand_most_frequently_used_words.json'
        word = show_random_word(file_name)
        self.ui.label.setText(word)

    def btnClicked_2(self):
        file_name = 'data/unknown_words_en_ru.json'
        word = show_random_word(file_name)
        self.ui.label_2.setText(word)

    def btnClicked_3(self):
        check_here = load_data(
            'data/unknown_words_en_ru.json')
        word = self.ui.lineEdit.text()
        translated_word = get_duplicate(word, check_here)
        self.ui.label_4.setText(translated_word)
        save_data('data/unknown_words_en_ru.json', check_here)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    app.exec_()
