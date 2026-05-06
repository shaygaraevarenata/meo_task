import tkinter as tk
from tkinter import ttk, messagebox
from data_handler import DataHandler
from datetime import datetime

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x600")

        self.data_handler = DataHandler()
        self.trainings = self.data_handler.load_trainings()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Фрейм для формы ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поля формы
        ttk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.type_entry = ttk.Combobox(input_frame, values=[
            "Кардио", "Силовая", "Йога", "Плавание", "Бег", "Велоспорт"
        ])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Длительность (часы):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        add_button = ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация")
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Тип:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filter_type = ttk.Combobox(filter_frame, values=["Все"] + [
            "Кардио", "Силовая", "Йога", "Плавание", "Бег", "Велоспорт"
        ])
        self.filter_type.set("Все")
        self.filter_type.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата с:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.filter_date_from = ttk.Entry(filter_frame)
        self.filter_date_from.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="по:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.filter_date_to = ttk.Entry(filter_frame)
        self.filter_date_to.grid(row=0, column=5, padx=5, pady=5)

        filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_button.grid(row=0, column=6, padx=5, pady=5)

        clear_filter_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.clear_filter)
        clear_filter_button.grid(row=0, column=7, padx=5, pady=5)

        # Таблица для отображения данных
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Дата", "Тип", "Длительность (ч)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.data_handler.validate_date_format(date):
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
            return

        if not self.data_handler.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть
