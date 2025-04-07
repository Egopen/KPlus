from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys

app = FastAPI()

# Разрешаем запросы с localhost:3000 (ваш сайт)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем только запросы с этого источника
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.get("/open_form/")
async def open_form():
    try:
        # Запускаем Python скрипт с формой через subprocess
        subprocess.Popen([sys.executable, 'form.py'])  # Запускаем form.py
        return {"message": "Форма успешно открыта!"}  # Успешный ответ
    except Exception as e:
        return {"error": str(e)}  # Обработка ошибок, если что-то пошло не так
