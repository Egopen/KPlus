import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import interface
import pandas as pd
from transformers import BertTokenizer, BertConfig
import torch
from sklearn.preprocessing import LabelEncoder

app = FastAPI(title="Contract Risk Analysis API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация модели и энкодеров при старте приложения
@app.on_event("startup")
async def startup_event():
    # Загрузка данных и создание энкодеров для label и class
    interface.model_id = "DeepPavlov/rubert-base-cased"
    interface.dataset = pd.read_csv("data1.csv")
    labels = interface.dataset["label"].unique()
    classes = interface.dataset["class"].unique()

    interface.label_encoder = LabelEncoder()
    interface.label_encoder.fit(labels)
    interface.class_encoder = LabelEncoder()
    interface.class_encoder.fit(classes)

    # Инициализация токенизатора и модели
    interface.tokenizer = BertTokenizer.from_pretrained(interface.model_id)
    interface.config = BertConfig.from_pretrained(interface.model_id)
    interface.model = interface.TripleBert(
        config=interface.config,
        num_classes_label=len(labels),
        num_classes_class=len(classes)
    ).to(interface.device)

    # Загрузка весов и перевод модели в режим evaluation
    interface.model.load_state_dict(
        torch.load("best_model.pth", map_location=interface.device)
    )
    interface.model.eval()

# Endpoint для анализа PDF договора и возврата HTML отчета
@app.post("/api/analyze", response_class=HTMLResponse)
async def analyze_contract(file: UploadFile = File(...)):
    # Генерация временных файлов
    temp_pdf = f"temp_{uuid.uuid4()}.pdf"
    temp_txt = f"temp_{uuid.uuid4()}.txt"
    temp_html = f"result_{uuid.uuid4()}.html"

    try:
        # Сохраняем загруженный PDF
        with open(temp_pdf, "wb") as f:
            f.write(await file.read())

        # Преобразуем PDF в текстовые блоки
        interface.pdf_to_sentences(temp_pdf, temp_txt)

        # Читаем непустые строки из txt
        with open(temp_txt, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Генерируем HTML отчет с использованием класс-энкодера
        interface.test_on_file(
            model=interface.model,
            tokenizer=interface.tokenizer,
            label_encoder=interface.label_encoder,
            class_encoder=interface.class_encoder,
            lines=lines,
            output_file=temp_html
        )

        # Проверяем существование отчета
        if not os.path.exists(temp_html):
            raise HTTPException(status_code=500, detail="Report file was not generated")

        # Читаем и возвращаем HTML
        with open(temp_html, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Очищаем временные файлы PDF и TXT
        for path in (temp_pdf, temp_txt):
            if os.path.exists(path):
                os.remove(path)

        return HTMLResponse(content=html_content)

    except Exception as e:
        # При ошибке удаляем все временные файлы
        for path in (temp_pdf, temp_txt, temp_html):
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
