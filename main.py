import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt6 import uic
import sqlite3


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.curr_id_edit = 0

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

        self.pushButton.clicked.connect(self.create_new)

    def load_table(self):
        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()
            res = cur.execute("SELECT * FROM main_tabel").fetchall()

        self.tableWidget.setRowCount(len(res))
        for i, row in enumerate(res):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


    def create_new(self):
        if self.tableWidget.currentRow() != -1:
            self.curr_id_edit = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
            self.edit_form()
        else:
            self.add_form()

    def edit_form(self):
        dialog = QDialog(self)
        uic.loadUi('addEditCoffeeForm.ui', dialog)

        lineEdit = dialog.lineEdit.text()
        lineEdit_2 = dialog.lineEdit_2.text()
        lineEdit_3 = dialog.lineEdit_3.text()
        lineEdit_4 = dialog.lineEdit_4.text()
        lineEdit_5 = dialog.lineEdit_5.text()
        lineEdit_6 = dialog.lineEdit_6.text()
        lineEdit_7 = dialog.lineEdit_7.text()

        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()

            cur.execute("""
                                    UPDATE main_tabel SET
                                        id = ?, Название сорта = ?, Степень обжарки = ?,
                                        Молотый/в зернах = ?, Описание вкуса = ?, Цена = ?, Обьем упаковки = ? 
                                    WHERE id = ?
                                """, (lineEdit, lineEdit_2, lineEdit_3, lineEdit_4, lineEdit_5, lineEdit_6, lineEdit_7,
                                      self.curr_id_edit))
            con.commit()

        dialog.accept()
        self.load_table()

        dialog.pushButton.clicked.connect(self.save)

    def add_form(self):
        dialog = QDialog(self)
        uic.loadUi('addEditCoffeeForm.ui', dialog)

        lineEdit = dialog.lineEdit.text()
        lineEdit_2 = dialog.lineEdit_2.text()
        lineEdit_3 = dialog.lineEdit_3.text()
        lineEdit_4 = dialog.lineEdit_4.text()
        lineEdit_5 = dialog.lineEdit_5.text()
        lineEdit_6 = dialog.lineEdit_6.text()
        lineEdit_7 = dialog.lineEdit_7.text()

        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()
            cur.execute("""
                                    INSERT INTO main_tabel
                                    (id, Название сорта, Степень обжарки, Молотый/в зернах, 
                                    Описание вкуса, Цена, Обьем упаковки)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (lineEdit, lineEdit_2, lineEdit_3, lineEdit_4,
                                      lineEdit_5, lineEdit_6, lineEdit_7))

        dialog.accept()


        dialog.pushButton.clicked.connect(self.save)


    def save(self):
        self.load_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())
