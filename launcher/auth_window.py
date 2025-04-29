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
        self.setWindowTitle('Minecraft Launcher - �����������')
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        self.title_label = QLabel('Minecraft Launcher')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(self.title_label)

        self.username_label = QLabel('��� ������������:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('������� ��� �������')
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('������:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('������� ������')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.remember_check = QCheckBox('��������� ����')
        layout.addWidget(self.remember_check)

        self.login_button = QPushButton('�����')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('�����������')
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, '������', '��������� ��� ����!')
            return

        if self.db.check_user(username, password):
            self.on_auth_success(username)
        else:
            QMessageBox.warning(self, '������', '�������� ��� ������������ ��� ������')

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, '������', '��������� ��� ����!')
            return

        if self.db.add_user(username, password):
            QMessageBox.information(self, '�����', '����������� ������ �������!')
        else:
            QMessageBox.warning(self, '������', '������������ � ����� ������ ��� ����������')




