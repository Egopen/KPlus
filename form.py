import tkinter as tk
from tkinter import messagebox

# Вопросы с вариантами ответов и их коэффициентами
questions = {
    "Где будет располагаться ваш Клуб?": {
        "Торговый центр": 1.005,
        "Цокольный этаж жилого дома": 1.001,
        "Отдельное здание": 1.008,
        "Другое": 0.801
    },
    "Какая сеть?": {
        "Colizeum": 2.0,
        "F5": 1.2,
        "Кибертека": 1.5,
        "Другое": 0.7,
    },
    "Какой у вас бюджет?": {
        "До 1 млн руб.": 0.5,
        "1-3 млн руб.": 1.0,
        "3-5 млн руб.": 1.5,
        "Более 5 млн руб.": 2.0
    },
    "Расстояние до метро:": {
        "менее 500 метров": 1.08,
        "менее 1500 метров": 1.06,
        "менее 2500 метров": 1.03,
        "более 2500 метров": 1.001
    },
    "Конкуренты в радиусе 1 км:":{
        "Да": 0.001,
        "Нет": 0.009
    }
}

# Словарь для хранения выбора пользователя
selected_vars = {}

def calculate():
    total_score = 0
    for question, options in questions.items():
        selected_option = selected_vars[question].get()
        if not selected_option:
            messagebox.showwarning("Ошибка", f"Выберите вариант для вопроса: {question}")
            return
        total_score += options[selected_option]
    if total_score > 4:
        messagebox.showinfo("Результат", f"Высокий коэффициент: {total_score}")
        print(f"Высокий коэффициент: {total_score}")
    elif total_score < 2:
        messagebox.showinfo("Результат", f"Низкий коэффициент: {total_score}")
        print(f"Низкий коэффициент: {total_score}")

root = tk.Tk()
root.title("Опросник для клуба")

# Создание вопросов и вариантов ответов
for question, options in questions.items():
    label = tk.Label(root, text=question, font=("Arial", 12))
    label.pack(pady=5)
    
    selected_vars[question] = tk.StringVar(value="")
    
    for option in options:
        tk.Radiobutton(root, text=option, variable=selected_vars[question], value=option).pack(anchor="w")

# Кнопка расчета
tk.Button(root, text="Рассчитать", command=calculate).pack(pady=10)

root.mainloop()
