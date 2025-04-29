from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt

class AuthWindow(QWidget):
    def __init__(self, db, on_auth_success):
        super().__init__()
        self.db = db
        self.on_auth_success = on_auth_success
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Minecraft Launcher - Авторизация')
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        self.title_label = QLabel('Minecraft Launcher')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)

        self.username_label = QLabel('Имя пользователя:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите ваш никнейм')
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.remember_check = QCheckBox('Запомнить меня')
        layout.addWidget(self.remember_check)

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Регистрация')
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return

        if self.db.check_user(username, password):
            self.on_auth_success(username)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверное имя пользователя или пароль')

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return

        if self.db.add_user(username, password):
            QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким именем уже существует')




