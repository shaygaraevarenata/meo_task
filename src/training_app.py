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
        self.filtered_trainings = self.trainings  # Для хранения отфильтрованных данных

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

        if not date or not training_type or not duration:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        if not self.data_handler.validate_date_format(date):
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
            return

        if not self.data_handler.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        try:
            # Создаём новую запись
            new_training = {
                "id": len(self.trainings) + 1,
                "date": date,
                "type": training_type,
                "duration": float(duration)
            }

            # Добавляем в список
            self.trainings.append(new_training)

            # Сохраняем в файл
            self.data_handler.save_trainings(self.trainings)

            # Обновляем таблицу
            self.refresh_table()

            # Очищаем поля ввода
            self.date_entry.delete(0, tk.END)
            self.type_entry.set("")
            self.duration_entry.delete(0, tk.END)

            messagebox.showinfo("Успех", "Тренировка добавлена успешно")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить тренировку: {e}")

    def apply_filter(self):
        """Применяет фильтры к данным"""
        filter_type = self.filter_type.get()
        date_from = self.filter_date_from.get()
        date_to = self.filter_date_to.get()

        filtered = []

        for training in self.trainings:
            # Проверка по типу тренировки
            type_match = (filter_type == "Все" or training["type"] == filter_type)

            # Проверка по дате
            date_match = True
            if date_from or date_to:
                training_date = datetime.strptime(training["date"], '%Y-%m-%d')
                if date_from:
                    from_date = datetime.strptime(date_from, '%Y-%m-%d')
                    date_match &= training_date >= from_date
                if date_to:
                    to_date = datetime.strptime(date_to, '%Y-%m-%d')
                    date_match &= training_date <= to_date

            if type_match and date_match:
                filtered.append(training)

        self.filtered_trainings = filtered
        self.refresh_table(filtered)

    def clear_filter(self):
        """Сбрасывает фильтры"""
        self.filter_type.set("Все")
        self.filter_date_from.delete(0, tk.END)
        self.filter_date_to.delete(0, tk.END)
        # Сбрасываем отфильтрованные данные к полному списку
        self.filtered_trainings = self.trainings
        self.refresh_table()

    def refresh_table(self, trainings=None):
        """Обновляет таблицу с данными"""
        # Очищаем текущую таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Определяем, какие данные отображать
        if trainings is None:
            trainings = self.filtered_trainings

        # Заполняем таблицу данными
        for training in trainings:
            self.tree.insert("", "end", values=(
                training["id"],
                training["date"],
                training["type"],
                f"{training['duration']:.2f}"  # Форматируем длительность до 2 знаков после запятой
            ))



def main():
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
