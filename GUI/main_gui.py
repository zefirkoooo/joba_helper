import os
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QProgressBar, QTimer
)
from GUI.func_gui import save_api_key
from voice_questions.voice_func import capture_audio_from_output, list_output_devices, get_audio_level

CONFIG_FILE = "config.py"
API_KEY = ""

if os.path.exists(CONFIG_FILE):
    try:
        from config import OPENAI_API_KEY
        API_KEY = OPENAI_API_KEY
    except ImportError:
        API_KEY = ""

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Приложение с выбором устройства и API-ключом")
        self.setGeometry(100, 100, 400, 450)

        self.label = QLabel("Выберите устройство вывода звука", self)
        self.device_combo = QComboBox(self)
        self.populate_audio_devices()

        self.api_button = QPushButton("Вставить API ключ OpenAI", self)
        self.api_button.clicked.connect(self.show_api_key_input)

        self.api_input = QLineEdit(self)
        self.api_input.setPlaceholderText("Введите API ключ")
        self.api_input.setText(API_KEY)
        self.api_input.hide()

        self.save_checkbox = QCheckBox("Сохранить API ключ", self)
        self.save_checkbox.hide()

        self.save_api_button = QPushButton("Сохранить", self)
        self.save_api_button.hide()
        self.save_api_button.clicked.connect(self.on_save_api_key)

        self.volume_bar = QProgressBar(self)
        self.volume_bar.setMinimum(0)
        self.volume_bar.setMaximum(100)

        self.listen_button = QPushButton("Распознать звук", self)
        self.listen_button.clicked.connect(self.handle_system_audio)

        self.text_output = QLabel("Распознанный текст появится здесь", self)

        self.audio_timer = QTimer(self)
        self.audio_timer.timeout.connect(self.update_audio_level)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.device_combo)
        layout.addWidget(self.api_button)
        layout.addWidget(self.api_input)
        layout.addWidget(self.save_checkbox)
        layout.addWidget(self.save_api_button)
        layout.addWidget(QLabel("🔊 Уровень звука:"))
        layout.addWidget(self.volume_bar)
        layout.addWidget(self.listen_button)
        layout.addWidget(self.text_output)

        self.setLayout(layout)

    def populate_audio_devices(self):
        """Заполняет список аудиоустройств вывода"""
        self.device_combo.addItems(list_output_devices().values())

    def show_api_key_input(self):
        """Показывает поле для ввода API ключа"""
        self.api_input.show()
        self.save_checkbox.show()
        self.save_api_button.show()

    def on_save_api_key(self):
        """Сохраняет API ключ"""
        save_api_key(self.api_input.text(), self.save_checkbox.isChecked(), self)

    def update_audio_level(self):
        """Обновляет уровень громкости"""
        selected_device_name = self.device_combo.currentText()
        devices = list_output_devices()
        selected_device_index = next((i for i, name in devices.items() if name == selected_device_name), None)

        if selected_device_index is not None:
            level = get_audio_level(selected_device_index)
            self.volume_bar.setValue(level)

    def handle_system_audio(self):
        """Запускает распознавание звука"""
        selected_device_name = self.device_combo.currentText()
        devices = list_output_devices()
        selected_device_index = next((i for i, name in devices.items() if name == selected_device_name), None)

        if selected_device_index is not None:
            self.audio_timer.start(100)
            text = capture_audio_from_output(selected_device_index)
            self.audio_timer.stop()
            self.text_output.setText(text)
