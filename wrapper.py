import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import interface  # ваш оригинальный код

app = FastAPI(title="Contract Risk Analysis API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация модели (вызовет ваш оригинальный код из interface.py)
@app.on_event("startup")
async def startup_event():
    # Инициализируем модель так же, как в вашем main()
    interface.model_id = "DeepPavlov/rubert-base-cased"
    interface.dataset = pd.read_csv("data1.csv")
    interface.unique_classes = interface.dataset["label"].unique()

    interface.tokenizer = BertTokenizer.from_pretrained(interface.model_id)
    interface.config = BertConfig.from_pretrained(interface.model_id)
    interface.model = interface.DualBert(
        config=interface.config, 
        num_classes=len(interface.unique_classes)
    ).to(interface.device)

    interface.model.load_state_dict(torch.load("best_model.pth", map_location=interface.device))
    interface.model.eval()

    interface.label_encoder = LabelEncoder()
    interface.label_encoder.fit(interface.unique_classes)

@app.post("/api/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    """Endpoint для анализа PDF"""
    try:
        # Создаем временные файлы
        temp_pdf = f"temp_{uuid.uuid4()}.pdf"
        temp_txt = f"temp_{uuid.uuid4()}.txt"
        result_html = f"result_{uuid.uuid4()}.html"

        # Сохраняем PDF
        with open(temp_pdf, "wb") as f:
            f.write(await file.read())

        # Вызываем ваши оригинальные функции
        interface.pdf_to_sentences(temp_pdf, temp_txt)
        
        with open(temp_txt, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # Используем вашу оригинальную функцию для генерации отчета
        interface.test_on_file(
            model=interface.model,
            tokenizer=interface.tokenizer,
            label_encoder=interface.label_encoder,
            lines=lines,
            output_file=result_html
        )

        return FileResponse(
            result_html,
            media_type="text/html",
            headers={"Content-Disposition": "inline; filename=report.html"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Удаляем временные файлы
        for f in [temp_pdf, temp_txt, result_html]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)