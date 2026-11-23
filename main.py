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

        self.Addbtn.clicked.connect(self.add_form)
        self.editbtn.clicked.connect(self.edit_form)

    def load_table(self):
        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()
            res = cur.execute("SELECT * FROM main_tabel").fetchall()

        self.tableWidget.setRowCount(len(res))
        for i, row in enumerate(res):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def edit_form(self):
        self.curr_id_edit = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
        dialog = QDialog(self)
        uic.loadUi('addEditCoffeeForm.ui', dialog)

        with sqlite3.connect("coffee.sqlite") as con:
            cur = con.cursor()
            row = cur.execute(
                "SELECT * FROM main_tabel WHERE id = ?", (self.curr_id_edit,)
            ).fetchone()

        if row:
            dialog.lineEdit.setText(str(row[0]))
            dialog.lineEdit_2.setText(str(row[1]))
            dialog.lineEdit_3.setText(str(row[2]))
            dialog.lineEdit_4.setText(str(row[3]))
            dialog.lineEdit_5.setText(str(row[4]))
            dialog.lineEdit_6.setText(str(row[5]))
            dialog.lineEdit_7.setText(str(row[6]))

        def save():
            cur_id = dialog.lineEdit.text()
            cur_name = dialog.lineEdit_2.text()
            cur_roast = dialog.lineEdit_3.text()
            cur_ground = dialog.lineEdit_4.text()
            cur_desc = dialog.lineEdit_5.text()
            cur_price = dialog.lineEdit_6.text()
            cur_volume = dialog.lineEdit_7.text()

            with sqlite3.connect("coffee.sqlite") as con:
                cur = con.cursor()
                cur.execute("""
                    UPDATE main_tabel SET
                        id = ?, Название сорта = ?, Степень обжарки = ?,
                                        Молотый/в зернах = ?, Описание вкуса = ?, Цена = ?, Обьем упаковки = ? 
                    WHERE id = ?
                """, (cur_id, cur_name, cur_roast, cur_ground,
                      cur_desc, cur_price, cur_volume, self.curr_id_edit))
                con.commit()

            dialog.accept()
            self.load_table()

        dialog.pushButton.clicked.connect(save)
        dialog.exec()

    def add_form(self):
        dialog = QDialog(self)
        uic.loadUi('addEditCoffeeForm.ui', dialog)

        def save():
            cur_id = dialog.lineEdit.text()
            cur_name = dialog.lineEdit_2.text()
            cur_roast = dialog.lineEdit_3.text()
            cur_ground = dialog.lineEdit_4.text()
            cur_desc = dialog.lineEdit_5.text()
            cur_price = dialog.lineEdit_6.text()
            cur_volume = dialog.lineEdit_7.text()

            with sqlite3.connect("coffee.sqlite") as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO main_tabel
                    (id, Название сорта, Степень обжарки, Молотый/в зернах, 
                                    Описание вкуса, Цена, Обьем упаковки) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (cur_id, cur_name, cur_roast, cur_ground,
                      cur_desc, cur_price, cur_volume))
                con.commit()

            dialog.accept()
            self.load_table()

        dialog.pushButton.clicked.connect(save)

        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())
