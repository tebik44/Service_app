import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from database.db import Model
from login import Login


class ProfileClient(QMainWindow):
    def __init__(self, email):
        super(ProfileClient, self).__init__()
        uic.loadUi('Windows/create_request.ui', self)
        self.setWindowTitle('Создать заявку')
        self.email = email
        self.load_masters()


        self.pushButton.clicked.connect(self.add_new_request)
        self.pushButton_2.clicked.connect(self.exit)
        self.pushButton_3.clicked.connect(self.review)

    def review(self):
        conn = Model().conn
        cur = conn.cursor()
        cur.execute("select id_client from Clients where email = ?", (self.email,))
        id_client = cur.fetchone()
        self.rev = ShowReview(id_client=id_client[0], email=self.email)
        self.rev.show()
        self.hide()
    @staticmethod
    def find_key_by_value(dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None
    def add_new_request(self):
        conn = Model().conn
        cur = conn.cursor()

        employeer_comboBox_text = self.comboBox.currentText()
        employeer = self.find_key_by_value(self.employeer_data, employeer_comboBox_text)
        problem = self.lineEdit.text()
        dead_line = self.dateEdit.text()
        cur.execute("select id_client from Clients where email = ?", (self.email,))
        id_client = cur.fetchone()
        try:
            cur.execute("""
                INSERT INTO Requests (id_client, id_employee, Description, Deadline, status)
                VALUES (?,?,?,?,?)
            """, (id_client[0], employeer, problem, dead_line, 'Выполняется'))
            conn.commit()
            QMessageBox.information(self, 'Успех', 'Обращение успешно создано, ожидайте', QMessageBox.Ok)
            self.exit()
        except conn.Error as er:
            QMessageBox.information(self, 'Провал', 'Ошибка создания обращения, проверьте правильность данных', QMessageBox.Ok)


    def load_masters(self):
        conn = Model().conn
        cur = conn.cursor()
        cur.execute("""select id_employee, last_name, ratting, experience
            from Employees""")
        data = cur.fetchall()
        self.employeer_data = {item[0]: f"{item[1]} рейтинг: {item[2]} стаж: {item[3]} лет" for item in data}


        employeer_values = [f"{item[1]} рейтинг: {item[2]} стаж: {item[3]} лет" for item in data]

        self.comboBox.addItems(employeer_values)

    def exit(self):
        self.log = Login()
        self.log.show()
        self.hide()


class ShowReview(QMainWindow):
    def __init__(self, id_client, email):
        super(ShowReview, self).__init__()
        uic.loadUi('Windows/employeer_table.ui', self)
        self.setWindowTitle('Ваши заявки')
        self.id_client = id_client
        self.email = email
        self.tableView = self.findChild(QtWidgets.QTableView, 'tableView')
        self.table_model = QStandardItemModel()
        self.tableView.setModel(self.table_model)

        conn = Model().conn
        cur = conn.cursor()
        cur.execute("""
                    select id_requst, c.first_name, e.first_name, Description, DeadLine, status
                    from Requests r
                        join Clients c on r.id_client = c.id_client
                        join Employees e on r.id_employee = e.id_employee
                    where r.id_client = ? and r.status = 'Выполняется';
                """, (id_client,))
        data = cur.fetchall()
        cur.execute("PRAGMA table_info(Requests)")
        column_data = cur.fetchall()
        self.load_data(data, column_data)

        self.pushButton.clicked.connect(self.exit)
        self.tableView.doubleClicked.connect(self.add_review)

    def add_review(self, index):
        row = index.row()
        desciption = self.table_model.item(row, 3).text()
        id_request = self.table_model.item(row, 0).text()
        self.review = AddReview(id_client=self.id_client, email=self.email,
                                description=desciption, id_request=id_request)
        self.review.show()
        self.hide()

    def load_data(self, data, column_data):
        column_data = [item[1] for item in column_data]
        self.table_model.setHorizontalHeaderLabels(column_data)

        for index_row, data_row in enumerate(data):
            for index_column, data_column in enumerate(column_data):
                item = QStandardItem(str(data_row[index_column]))
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                self.table_model.setItem(index_row, index_column, item)

    def exit(self):
        self.back = ProfileClient(email=self.email)
        self.back.show()
        self.hide()


class AddReview(QMainWindow):
    def __init__(self, id_client, email, description, id_request):
        super(AddReview, self).__init__()
        uic.loadUi('Windows/add_review.ui', self)
        self.id_request = id_request
        self.id_client = id_client
        self.email = email
        self.label_2.setText(f'Тема обращения - {description}')
        self.setWindowTitle('Оставить отзыв')

        self.pushButton.clicked.connect(self.add_review_to_db)

    def add_review_to_db(self):
        review = self.textEdit.toPlainText()
        if review == '':
            QMessageBox.information(self, 'Провал', 'Пожалуйста напишите что-нибудь', QMessageBox.Ok)
        else:
            conn = Model().conn
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO Reviews (id_client, content)
                    VALUES (?,?)
                """, (self.id_client, review))
                cur.execute("""
                    UPDATE Requests
                    SET status = ?
                    WHERE id_requst = ?
                """, ('Оценено', self.id_request))
                conn.commit()
                QMessageBox.information(self, 'Успех', 'Спасибо за оценку', QMessageBox.Ok)
                self.exit()
            except conn.Error as er:
                QMessageBox.information(self, 'Провал', f'Ошибка вставки отзыва: {er}', QMessageBox.Ok)



    def exit(self):
        self.review_data = ShowReview(id_client=self.id_client, email=self.email)
        self.review_data.show()
        self.hide()


