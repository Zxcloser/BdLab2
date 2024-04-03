import sys
from PyQt6 import QtGui, QtCore,  QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import MySQLdb as mdb
from mainwindow import Ui_MainWindow


conn = mdb.connect(host="localhost", user="root", password="", database="var1_tar2")
def get_data():
    cursor = conn.cursor()
    cursor.execute("select * from genres")
    res = cursor.fetchall()
    return res
def get_books(id):
    cursor = conn.cursor()
    cursor.execute(f"select name, price from Books where genre_id = {id};")
    res = cursor.fetchall()
    return res
class Show_books(QMainWindow):
    def __init__(self, books):
        super(Show_books, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        height = 10
        for i in books:
            lb = QtWidgets.QLabel(self)
            lb.setGeometry(QtCore.QRect(30, height, 180, 150))
            lb.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lb.setObjectName(f"label_{i[0]}")

            lb_t = QtWidgets.QLabel(self)
            lb_t.setGeometry(QtCore.QRect(110, height, 210, 150))
            lb_t.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lb_t.setText(f"{i[0]}\n ")
            lb_t.setObjectName(f"label_text_{i[0]}")
            lb_t.adjustSize()
            height += 30

class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        def add():
            cursor = conn.cursor()
            cursor.execute(f"call addToBasket({int(self.edit_1.text())},{int(self.edit_1.text())},{int(self.edit_3.text())});")
            conn.commit()
        self.lb_1 = QtWidgets.QLabel(self)
        self.lb_1.setGeometry(QtCore.QRect(10, 100, 100, 20))
        self.lb_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_1.setText("Введите номер книги")
        self.lb_1.adjustSize()

        self.edit_1 = QtWidgets.QLineEdit(self)#Я так делал поэтом уи спин бокс использовал
        self.edit_1.setGeometry(QtCore.QRect(160, 100, 200, 20))
        self.edit_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.lb_2 = QtWidgets.QLabel(self)
        self.lb_2.setGeometry(QtCore.QRect(10, 140, 100, 20))
        self.lb_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_2.setText("Введите номер сессии")
        self.lb_2.adjustSize()

        self.edit_2 = QtWidgets.QLineEdit(self)
        self.edit_2.setGeometry(QtCore.QRect(160, 140, 200, 20))
        self.edit_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.lb_3 = QtWidgets.QLabel(self)
        self.lb_3.setGeometry(QtCore.QRect(10, 180, 100, 20))
        self.lb_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_3.setText("Введите количество книг")
        self.lb_3.adjustSize()

        self.edit_3 = QtWidgets.QLineEdit(self)
        self.edit_3.setGeometry(QtCore.QRect(160, 180, 200, 20))
        self.edit_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.finalize = QtWidgets.QPushButton(self)
        self.finalize.setGeometry(QtCore.QRect(160, 220, 150, 65))
        self.finalize.setText("Добавить в корзину")
        self.finalize.clicked.connect(add)
        print("И не здесь")

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        books = []
        def checky_check():
            print(books)
            book = Show_books(books)
            self.book_window = book
            book.show()
            for k in range(len(checkboxes)):
                checkboxes[k].setChecked(False)
            books.clear()
        def add_books(j):
            if j not in books:
                books.append(j)
        def add_dialog():
            dial = Dialog()
            self.Dialog = dial
            dial.show()

        res_data = get_data()
        height = 10
        checkboxes = []
        for i in res_data:
            lb = QtWidgets.QLabel(self)
            lb.setGeometry(QtCore.QRect(30, height, 180, 150))
            lb.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lb.setObjectName(f"label_{i[1]}")

            lb_t = QtWidgets.QLabel(self)
            lb_t.setGeometry(QtCore.QRect(110, height, 210, 150))
            lb_t.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lb_t.setText(f"{i[1]}\n ")
            lb_t.setObjectName(f"label_text_{i[1]}")
            lb_t.adjustSize()
            height += 30
            books_data = get_books(i[0])
            for j in books_data:
                ch = QtWidgets.QCheckBox(self)
                ch.stateChanged.connect(lambda state, j=j: add_books(j))
                ch.setGeometry(QtCore.QRect(160, height-65, 180, 150))
                ch.setObjectName(f"label_{j[0]}")
                checkboxes.append(ch)

                lb_t = QtWidgets.QLabel(self)
                lb_t.setGeometry(QtCore.QRect(210, height, 210, 150))
                lb_t.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                lb_t.setText(f"{j[0]}\n ")
                lb_t.setObjectName(f"label_text_{j[0]}")
                lb_t.adjustSize()

                lb_t = QtWidgets.QLabel(self)
                lb_t.setGeometry(QtCore.QRect(420, height, 210, 150))
                lb_t.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                lb_t.setText(f"{j[1]}\n ")
                lb_t.setObjectName(f"label_text_{j[1]}")
                lb_t.adjustSize()

                height += 30
            height += 120
        add = QtWidgets.QPushButton(self)
        add.setGeometry(QtCore.QRect(250, height, 150, 65))
        add.setText("Добавить")
        add.clicked.connect(add_dialog)
        check= QtWidgets.QPushButton(self)
        check.setGeometry(QtCore.QRect(400, height, 150, 65))
        check.setText("Посмотреть")
        check.clicked.connect(checky_check)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec())