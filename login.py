import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import client
# from employeer import ProfileEmployeer
import employeer
from database.db import Model


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Windows/login.ui', self)
        self.setWindowTitle('Авторизация')
        self.label_2.hide()
        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')

        self.pushButton.clicked.connect(self.log)
        self.pushButton_2.clicked.connect(self.reg)

    def reg(self):
        self.ref = RegClient()
        self.ref.show()
        self.hide()

    def log(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.label_2.hide()
        conn = Model().conn
        cur = conn.cursor()
        cur.execute("""
            SELECT id_role, first_name, last_name, email
            FROM (
                SELECT id_role, first_name, last_name, email FROM Clients WHERE email = :login AND password = :password
                UNION
                SELECT id_role, first_name, last_name, email FROM Employees WHERE email = :login AND password = :password
            ) AS user_roles;
        """, {'password': password, 'login': login})
        respoune = cur.fetchone()
        if login == '' or password == '':
            self.label_2.setText('* Все поля должны быть заполнены')
            self.label_2.show()
            return
        elif respoune:
            if int(respoune[0]) == 2:
                QMessageBox.information(self, "Успех", f"Здравствуйте {respoune[1]} {respoune[2]},", QMessageBox.Ok)
                self.profile = client.ProfileClient(email=respoune[3])
                self.profile.show()
                self.hide()
            elif int(respoune[0]) == 1:
                QMessageBox.information(self, "Успех", f"Здравствуйте {respoune[1]} {respoune[2]},", QMessageBox.Ok)
                self.profile = employeer.ProfileEmployeer(email=respoune[3])
                self.profile.show()
                self.hide()

        else:
            self.label_2.setText("Пользователь не найден")
            self.label_2.show()


class RegClient(QMainWindow):
    def __init__(self):
        super(RegClient, self).__init__()
        uic.loadUi('Windows/reg.ui', self)
        self.setWindowTitle('Регистрация')

        self.comboBox.addItems(['М', 'Ж'])

        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.log)

    def reg(self):
        last_name = self.lineEdit.text()
        first_name = self.lineEdit_2.text()
        middle_name = self.lineEdit_3.text()
        phone_number = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        password = self.lineEdit_6.text()
        sex = self.comboBox.currentText()
        age = self.lineEdit_7.text()

        if not (last_name and first_name and middle_name and phone_number and email and password and sex and age):
            QMessageBox.information(self, 'Провал', 'Нужно заполнить все поля', QMessageBox.Ok)
        else:
            conn = Model().conn
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO Clients (last_name, first_name, middle_name, phone_number, email, password, sex, age, id_role)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (last_name, first_name, middle_name, phone_number, email, password, sex, age, 2))
                conn.commit()
                QMessageBox.information(self, 'Успех', 'Вы успешно зарегистриованы', QMessageBox.Ok)
                self.log()
            except conn.Error as er:
                QMessageBox.information(self, 'Провал', 'Ошибка вставки данных, проверьте корректность данных', QMessageBox.Ok)

    def log(self):
        self.lg = Login()
        self.lg.show()
        self.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    login = Login()
    login.show()

    sys.exit(app.exec_())