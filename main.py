import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
import sqlite3


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'состояние', 'вкус', 'цена', 'объем'])
        self.loaddata()
        self.button_main.clicked.connect(self.edit)
        self.download.clicked.connect(self.loaddata)

    def edit(self):
        self.ex = Win2()
        self.ex.show()

    def loaddata(self):
        con = sqlite3.connect('coffee.db')
        cur = con.cursor()
        sqlquest = "SELECT * FROM coffee1"
        inf = cur.execute(sqlquest)
        res = cur.fetchall()
        self.table.setRowCount(len(res))
        tablerow = 0
        for row in res:
            for i in range(len(row)):
                self.table.setItem(tablerow, i, QTableWidgetItem(str(row[i])))
            tablerow += 1
        con.close()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.repaint()


class Win2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.button.clicked.connect(self.save_edit)

    def save_edit(self):
        id = self.line1.text()
        sort = self.line2.text()
        roast = self.line3.text()
        condition = self.line4.text()
        taste = self.line5.text()
        cost = self.line6.text()
        volume = self.line7.text()
        here = False
        if id:
            db = sqlite3.connect('coffee.db')
            cur = db.cursor()
            for ids in cur.execute("SELECT ID FROM coffee1"):
                if ids[0] == int(id):
                    here = True
            if here:
                if sort:
                    db.execute("UPDATE coffee1 SET сорт = ? WHERE ID = ?", (sort, id))
                if roast:
                    db.execute("UPDATE coffee1 SET обжарка = ? WHERE ID = ?", (roast, id))
                if condition:
                    db.execute("UPDATE coffee1 SET молотыйзерна = ? WHERE ID = ?", (condition, id))
                if taste:
                    db.execute("UPDATE coffee1 SET вкус = ? WHERE ID = ?", (taste, id))
                if int(cost) > 0:
                    db.execute("UPDATE coffee1 SET цена = ? WHERE ID = ?", (cost, id))
                if int(volume) > 0:
                    db.execute("UPDATE coffee1 SET объем = ? WHERE ID = ?", (volume, id))
            else:
                if sort and roast and condition and taste and int(cost) > 0 and int(volume) > 0:
                    db.execute("""INSERT INTO coffee1(ID,цена,объем) VALUES (?, ?, ?)""", (id, cost, volume))
                    db.execute("UPDATE coffee1 SET сорт = ? WHERE ID = ?", (sort, id))
                    db.execute("UPDATE coffee1 SET обжарка = ? WHERE ID = ?", (roast, id))
                    db.execute("UPDATE coffee1 SET молотыйзерна = ? WHERE ID = ?", (condition, id))
                    db.execute("UPDATE coffee1 SET вкус = ? WHERE ID = ?", (taste, id))
            db.commit()
            db.close()
        self.closed()

    def closed(self):
        self.close()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
