import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic
import sqlite3


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM main_tabel').fetchall()
        print(res)
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена', 'Обьем упаковки'])
        self.tableWidget.setRowCount(len(res))

        for i, row_tuple in enumerate(res):
                for j, val in enumerate(row_tuple):
                    item = QTableWidgetItem(str(val))
                    self.tableWidget.setItem(i, j, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())