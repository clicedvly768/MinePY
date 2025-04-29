from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog,
    QMessageBox, QSlider, QSpinBox
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, db, username):
        super().__init__()
        self.db = db
        self.username = username
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle(f'Minecraft Launcher - {self.username}')
        self.setMinimumSize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Приветствие
        self.greeting_label = QLabel(f'Добро пожаловать, {self.username}!')
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.greeting_label)

        # Настройки Java
        java_group = QWidget()
        java_layout = QHBoxLayout(java_group)

        java_label = QLabel('Путь к Java:')
        self.java_path_input = QLineEdit()
        self.java_path_input.setPlaceholderText('Автоматическое определение')
        
        java_browse_btn = QPushButton('Обзор...')
        java_browse_btn.clicked.connect(self.browse_java_path)

        java_layout.addWidget(java_label)
        java_layout.addWidget(self.java_path_input)
        java_layout.addWidget(java_browse_btn)

        layout.addWidget(java_group)

        # Выделение памяти
        memory_group = QWidget()
        memory_layout = QHBoxLayout(memory_group)

        memory_label = QLabel('Память (MB):')
        
        self.memory_slider = QSlider(Qt.Horizontal)
        self.memory_slider.setRange(1024, 8192)
        self.memory_slider.setSingleStep(256)
        self.memory_slider.setTickInterval(256)
        self.memory_slider.setTickPosition(QSlider.TicksBelow)
        
        self.memory_spinbox = QSpinBox()
        self.memory_spinbox.setRange(1024, 8192)
        self.memory_spinbox.setSingleStep(256)
        
        self.memory_slider.valueChanged.connect(self.memory_spinbox.setValue)
        self.memory_spinbox.valueChanged.connect(self.memory_slider.setValue)

        memory_layout.addWidget(memory_label)
        memory_layout.addWidget(self.memory_slider)
        memory_layout.addWidget(self.memory_spinbox)

        layout.addWidget(memory_group)

        # Разрешение экрана
        resolution_group = QWidget()
        resolution_layout = QHBoxLayout(resolution_group)

        resolution_label = QLabel('Разрешение:')
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            '800x600',
            '1024x768',
            '1280x720',
            '1366x768',
            '1600x900',
            '1920x1080',
            'Полный экран'
        ])

        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)

        layout.addWidget(resolution_group)

        # Кнопки
        buttons_group = QWidget()
        buttons_layout = QHBoxLayout(buttons_group)

        self.save_btn = QPushButton('Сохранить настройки')
        self.save_btn.clicked.connect(self.save_settings)

        self.play_btn = QPushButton('Играть!')
        self.play_btn.setStyleSheet('font-size: 16px;')
        self.play_btn.clicked.connect(self.launch_game)

        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.play_btn)

        layout.addWidget(buttons_group)

        layout.addStretch()

    def browse_java_path(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Выберите исполняемый файл Java',
            '',
            'Java Executable (java java.exe)'
        )
        
        if path:
            self.java_path_input.setText(path)

    def load_settings(self):
        settings = self.db.get_user_settings(self.username)
        if settings:
            self.java_path_input.setText(settings.get('java_path', ''))
            self.memory_slider.setValue(settings.get('memory_alloc', 2048))
            resolution = settings.get('resolution', '1024x768')
            
            index = self.resolution_combo.findText(resolution)
            if index >= 0:
                self.resolution_combo.setCurrentIndex(index)

    def save_settings(self):
        settings = {
            'java_path': self.java_path_input.text(),
            'memory_alloc': self.memory_slider.value(),
            'resolution': self.resolution_combo.currentText()
        }
        
        if self.db.update_user_settings(self.username, settings):
            QMessageBox.information(self, 'Успех', 'Настройки сохранены!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось сохранить настройки')

    def launch_game(self):
        # Здесь должна быть логика запуска Minecraft
        QMessageBox.information(
            self,
            'Запуск игры',
            'Игра запускается...\n\n' +
            f'Java: {self.java_path_input.text() or "по умолчанию"}\n' +
            f'Память: {self.memory_slider.value()} MB\n' +
            f'Разрешение: {self.resolution_combo.currentText()}'
        )
        
        # В реальном лаунчере здесь будет вызов Minecraft с указанными параметрами
        # Например, через subprocess