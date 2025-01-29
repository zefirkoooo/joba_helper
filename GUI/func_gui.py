import os
from PyQt6.QtWidgets import QMessageBox

CONFIG_FILE = "config.py"

def save_api_key(api_key, should_save, parent_window):
    """
    Сохраняет API ключ в config.py.

    :param api_key: Введенный API-ключ (str)
    :param should_save: Флаг сохранения (bool)
    :param parent_window: Окно, в котором вызывается функция (для отображения сообщений)
    """
    api_key = api_key.strip()

    if not api_key:
        QMessageBox.warning(parent_window, "Ошибка", "API ключ не может быть пустым!")
        return

    if should_save:
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(f'OPENAI_API_KEY = "{api_key}"\n')
            QMessageBox.information(parent_window, "Успех", "API ключ сохранён!")
        except Exception as e:
            QMessageBox.critical(parent_window, "Ошибка", f"Ошибка сохранения ключа: {e}")
    else:
        QMessageBox.information(parent_window, "Инфо", "Ключ не сохранён, но будет использован в сессии.")
