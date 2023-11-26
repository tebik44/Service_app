import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from database.db import Model
import login


class ProfileEmployeer(QMainWindow):
    def __init__(self, email):
        super(ProfileEmployeer, self).__init__()
        uic.loadUi('Windows/employeer_table.ui', self)
        self.tableView = self.findChild(QtWidgets.QTableView, 'tableView')
        self.table_model = QStandardItemModel()
        self.tableView.setModel(self.table_model)

        conn = Model().conn
        cur = conn.cursor()
        cur.execute("""
            select id_requst, c.first_name, Description, DeadLine, status
            from Requests r
                join Clients c on r.id_client = c.id_client
                join Employees e on r.id_employee = e.id_employee
            where e.email = ?
        """, (email,))
        data = cur.fetchall()
        cur.execute("PRAGMA table_info(Requests)")
        column_data = cur.fetchall()
        self.load_data(data, column_data)

        self.pushButton.clicked.connect(self.exit)

    def load_data(self, data, column_data):
        column_data = [item[1] for item in column_data]
        column_data.remove('id_employee')
        self.table_model.setHorizontalHeaderLabels(column_data)

        for index_row, data_row in enumerate(data):
            for index_column, data_column in enumerate(column_data):
                item = QStandardItem(str(data_row[index_column]))
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                self.table_model.setItem(index_row, index_column, item)


    def exit(self):
        self.log = login.Login()
        self.log.show()
        self.hide()