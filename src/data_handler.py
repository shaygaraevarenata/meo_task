import json
import os
from datetime import datetime

class DataHandler:
    def __init__(self, data_file='data/trainings.json'):
        self.data_file = data_file
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Создаёт директорию для данных, если её нет"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def load_trainings(self):
        """Загружает тренировки из JSON-файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка загрузки данных: {e}")
            return []

    def save_trainings(self, trainings):
        """Сохраняет тренировки в JSON-файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(trainings, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка сохранения данных: {e}")

    def validate_date_format(self, date_str):
        """Проверяет формат даты (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_duration(self, duration_str):
        """Проверяет, что длительность — положительное число"""
        try:
            duration = float(duration_str)
            return duration > 0
        except ValueError:
            return False
