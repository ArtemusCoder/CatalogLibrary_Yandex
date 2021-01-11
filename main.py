import csv
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QDialog, QLabel
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.con = sqlite3.connect("books_db.sqlite")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Каталог библиотеки')
        self.comboBox.addItem('Название')
        self.comboBox.addItem('Автор')
        self.searchbtn.clicked.connect(self.search)
        self.listWidget.itemClicked.connect(self.clicked)

    def search(self):
        self.listWidget.clear()
        cur = self.con.cursor()
        find_by = str(self.comboBox.currentText())
        input = self.line_input.text()
        if bool(input):
            if find_by == 'Название':
                res = cur.execute("""SELECT books.name FROM books WHERE name LIKE '{}%'""".format(input)).fetchall()
            if find_by == 'Автор':
                res = cur.execute(
                    """SELECT books.name FROM books INNER JOIN Author ON Author.id = books.author_id WHERE Author.author like '{}%'""".format(
                        input)).fetchall()
            print(res)
            if bool(res):
                for elem in res:
                    print(elem[0])
                    self.listWidget.addItem(elem[0])

    def clicked(self, item):
        cur = self.con.cursor()
        data = cur.execute("""SELECT books.name, Author.author, books.year, books.genre_id, books.image FROM books INNER JOIN Author ON Author.id = books.author_id WHERE name = ?""", (item.text(),))
        for elem in data:
            name, author, year, genre_id, image = elem
        print(genre_id)
        res = cur.execute("""SELECT genre FROM Genre WHERE id = ?""", (genre_id, )).fetchone()
        genre = res[0]
        d = QDialog()
        d.setWindowTitle("Информация о книге")
        pixmap = QPixmap()
        pixmap.loadFromData(image, 'jpg')
        imagelabel = QLabel(d)
        imagelabel.move(175, 20)
        imagelabel.resize(150, 300)
        pixmap = pixmap.scaled(150, 300, Qt.KeepAspectRatio)
        imagelabel.setPixmap(pixmap)
        label1 = QLabel(d)
        label1.setText('Название')
        label1.move(200, 320)
        label1.setStyleSheet('font: 18px bold;')
        label2 = QLabel(d)
        label2.setText(name)
        label2.move(200, 350)
        label3 = QLabel(d)
        label3.setText('Автор')
        label3.move(200, 380)
        label4 = QLabel(d)
        label4.setText(author)
        label4.move(200, 410)
        label5 = QLabel(d)
        label5.setText('Год выпуска')
        label5.move(200, 440)
        label6 = QLabel(d)
        label6.setText(str(year))
        label6.move(200, 470)
        label7 = QLabel(d)
        label7.setText('Жанр')
        label7.move(200, 500)
        label8 = QLabel(d)
        label8.setText(genre)
        label8.move(200, 530)
        label3.setStyleSheet('font: 18px bold;')
        label5.setStyleSheet('font: 18px bold;')
        label7.setStyleSheet('font: 18px bold;')
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
