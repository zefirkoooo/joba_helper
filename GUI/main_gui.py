import sys
import os
import sounddevice as sd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox
)
from GUI.func_gui import save_api_key

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

        # Настройка основного окна
        self.setWindowTitle("Приложение с выбором устройства и API-ключом")
        self.setGeometry(100, 100, 400, 400)

        # Метка и выбор устройства вывода звука
        self.label = QLabel("Выберите устройство вывода звука", self)
        self.device_combo = QComboBox(self)
        self.populate_audio_devices()

        # Кнопка для выбора устройства
        self.button = QPushButton("Показать выбранное устройство", self)
        self.button.clicked.connect(self.on_button_click)

        # Кнопка для ввода API ключа
        self.api_button = QPushButton("Вставить API ключ OpenAI", self)
        self.api_button.clicked.connect(self.show_api_key_input)

        # Поле ввода API ключа
        self.api_input = QLineEdit(self)
        self.api_input.setPlaceholderText("Введите API ключ")
        self.api_input.setText(API_KEY)  # Подгружаем сохраненный ключ
        self.api_input.hide()

        # Чекбокс "Сохранить ключ"
        self.save_checkbox = QCheckBox("Сохранить API ключ", self)
        self.save_checkbox.hide()

        # Кнопка "Сохранить API ключ"
        self.save_api_button = QPushButton("Сохранить", self)
        self.save_api_button.hide()
        self.save_api_button.clicked.connect(self.on_save_api_key)

        # Настройка компоновки
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.device_combo)
        layout.addWidget(self.button)
        layout.addWidget(self.api_button)
        layout.addWidget(self.api_input)
        layout.addWidget(self.save_checkbox)
        layout.addWidget(self.save_api_button)

        self.setLayout(layout)

    def populate_audio_devices(self):
        """Заполняет список аудиоустройств вывода"""
        self.devices = sd.query_devices()
        self.output_devices = [device for device in self.devices if device["max_output_channels"] > 0]

        for device in self.output_devices:
            self.device_combo.addItem(device["name"])

    def on_button_click(self):
        """Обработчик нажатия кнопки выбора устройства"""
        selected_device = self.device_combo.currentText()
        self.label.setText(f"Вы выбрали: {selected_device}")

    def show_api_key_input(self):
        """Показывает поле для ввода API ключа"""
        self.api_input.show()
        self.save_checkbox.show()
        self.save_api_button.show()

    def on_save_api_key(self):
        """Обработчик нажатия кнопки сохранения API ключа"""
        save_api_key(self.api_input.text(), self.save_checkbox.isChecked(), self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())
