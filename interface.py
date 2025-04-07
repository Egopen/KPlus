import fitz  # PyMuPDF
import re
from transformers import BertModel, BertTokenizer, BertPreTrainedModel, BertConfig
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
import pandas as pd

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DualBert(BertPreTrainedModel):
    def __init__(self, config, num_classes):
        super().__init__(config)
        self.bert = BertModel(config)
        self.classifier = nn.Linear(config.hidden_size, num_classes)
        self.regressor = nn.Linear(config.hidden_size, 1)
        self.init_weights()
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.bert(input_ids, attention_mask)
        pooled_output = outputs.pooler_output
        
        logits = self.classifier(pooled_output)
        risk_score = self.regressor(pooled_output).squeeze(-1)
        
        return logits, risk_score

def pdf_to_sentences(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    formatted_text = []
    
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: (block[1], block[0]))
        
        prev_bottom = None
        prev_text = ""
        for block in blocks:
            text = block[4].strip()
            if not text:
                continue
                
            # Пропускаем отдельные цифры
            if text.isdigit() and len(text) == 1:
                continue
                
            # Если текст начинается с номера пункта (например, "3.4.13."), 
            # объединяем его с предыдущим блоком, если он был коротким (возможно, это таб)
            if re.match(r'^\d+\.\d+\.\d+\.$', text) and prev_text and len(prev_text) < 20:
                formatted_text[-1] = formatted_text[-1] + " " + text
                prev_text = text
                continue
                
            block_type = "normal"
            if block[1] < 50:
                block_type = "header"
            elif any(char.isdigit() for char in text.split()[0]) and len(text.split()[0]) < 5:
                block_type = "numbered"
            elif text.upper() == text and len(text.split()) < 5:
                block_type = "section_header"
                
            if prev_bottom is not None and block[1] - prev_bottom > 20:
                formatted_text.append("")
                
            if block_type == "header":
                formatted_text.append(f"===== {text} =====")
            elif block_type == "section_header":
                formatted_text.append(f"\n{text}\n")
            elif block_type == "numbered":
                formatted_text.append(text)
            else:
                formatted_text.append(text)
                
            prev_bottom = block[3]
            prev_text = text
    
    # Постобработка: объединяем строки, где номер пункта отделен от текста
    processed_text = []
    i = 0
    while i < len(formatted_text):
        line = formatted_text[i]
        if i < len(formatted_text) - 1 and re.match(r'^\d+\.\d+\.\d+\.$', line.strip()):
            next_line = formatted_text[i+1]
            processed_text.append(line + " " + next_line)
            i += 2
        else:
            processed_text.append(line)
            i += 1
    
    # Дополнительная обработка для объединения разделенных пунктов
    final_text = []
    current_block = []
    for line in processed_text:
        line = line.strip()
        if not line:
            if current_block:
                final_text.append(" ".join(current_block))
                current_block = []
        else:
            # Если строка начинается с номера пункта (например, "3.4.13."), это новый блок
            if re.match(r'^\d+\.\d+\.\d+\.', line) or re.match(r'^\d+\.\d+\.', line) or re.match(r'^\d+\.', line):
                if current_block:
                    final_text.append(" ".join(current_block))
                current_block = [line]
            else:
                current_block.append(line)
    
    if current_block:
        final_text.append(" ".join(current_block))
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(final_text))

def text_processing(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'(\d)\s+(?=\d)', r'\1', text)
    return text

def test(model, tokenizer, text):
    input = tokenizer(text, max_length=256, padding=True, truncation=True, 
                    return_tensors="pt", return_token_type_ids=False).to(device)
    logits, pred = model(**input)
    return logits, pred

def get_risk_color(risk_value):
    """Возвращает класс цвета в зависимости от уровня риска"""
    if risk_value < 0.2:
        return "risk-1"   # Очень низкий риск
    elif 0.2 <= risk_value < 0.4:
        return "risk-2"   # Низкий риск
    elif 0.4 <= risk_value < 0.5:
        return "risk-3"   # Умеренный риск
    elif 0.5 <= risk_value < 0.6:
        return "risk-4"   # Повышенный риск
    elif 0.6 <= risk_value < 0.7:
        return "risk-5"   # Высокий риск
    elif 0.7 <= risk_value < 0.8:
        return "risk-6"   # Очень высокий риск
    else:
        return "risk-7"   # Критический риск

def is_new_paragraph(line, prev_line):
    """Определяет, начинается ли новый абзац"""
    if not prev_line:
        return True
    # Если строка начинается с цифры и точки (например, "8.2."), это новый абзац
    if re.match(r'^\d+\.\d+\.', line.strip()) or re.match(r'^\d+\.', line.strip()):
        return True
    # Если предыдущая строка заканчивается точкой, а текущая начинается с заглавной буквы
    if prev_line.strip().endswith('.') and line.strip() and line.strip()[0].isupper():
        return True
    return False

def test_on_file(model, tokenizer, label_encoder, lines, output_file):
    results = []
    html = [
        '''<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Анализ рисков договора</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6;
                    margin: 40px auto;
                    max-width: 1000px;
                    padding: 0 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .highlight { 
                    padding: 10px; 
                    border-radius: 4px; 
                    margin: 10px 0;
                    display: block;
                    border-left: 4px solid;
                }
                /* Градация цветов от зелёного к красному */
                .risk-1 { background: #e6f7e6; border-color: #2ecc71; } /* Очень низкий */
                .risk-2 { background: #d4edda; border-color: #27ae60; } /* Низкий */
                .risk-3 { background: #fff3cd; border-color: #f39c12; } /* Умеренный */
                .risk-4 { background: #ffe0b2; border-color: #e67e22; } /* Повышенный */
                .risk-5 { background: #f8d7da; border-color: #e74c3c; } /* Высокий */
                .risk-6 { background: #f5c6cb; border-color: #c0392b; } /* Очень высокий */
                .risk-7 { background: #f1b0b7; border-color: #a93226; } /* Критический */
                
                pre {
                    white-space: pre-wrap;
                    font-family: inherit;
                    margin: 0;
                    padding: 0;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 0.9em;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                    font-weight: bold;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                h1 {
                    color: #333;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #444;
                    margin-top: 30px;
                }
                .risk-legend {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin: 20px 0;
                }
                .legend-item {
                    display: flex;
                    align-items: center;
                    margin-right: 15px;
                }
                .legend-color {
                    width: 20px;
                    height: 20px;
                    margin-right: 5px;
                    border-radius: 3px;
                    border-left: 3px solid;
                }
            </style>
        </head>
        <body>
        <div class="container">
        <h1>Анализ рисков договора</h1>
        <div class="risk-legend">
            <div class="legend-item"><div class="legend-color risk-1"></div>Очень низкий (0-0.2)</div>
            <div class="legend-item"><div class="legend-color risk-2"></div>Низкий (0.2-0.4)</div>
            <div class="legend-item"><div class="legend-color risk-3"></div>Умеренный (0.4-0.5)</div>
            <div class="legend-item"><div class="legend-color risk-4"></div>Повышенный (0.5-0.6)</div>
            <div class="legend-item"><div class="legend-color risk-5"></div>Высокий (0.6-0.7)</div>
            <div class="legend-item"><div class="legend-color risk-6"></div>Очень высокий (0.7-0.8)</div>
            <div class="legend-item"><div class="legend-color risk-7"></div>Критический (0.8-1.0)</div>
        </div>
        '''
    ]

    current_block = []
    prev_line = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_block:
                block_text = " ".join(current_block)
                out, pred = test(model, tokenizer, block_text)
                pred_label_id = torch.argmax(out, dim=1).item()
                label = label_encoder.inverse_transform([pred_label_id])[0]
                risk_value = pred.item()
                
                if label != "neutral":
                    results.append({
                        'Текст': block_text,
                        'Класс': label,
                        'Уровень риска': risk_value,
                        'Цвет': get_risk_color(risk_value)
                    })
                
                color_class = get_risk_color(risk_value) if label not in ["neutral", "no_risk"] else ""
                highlighted = f'<div class="highlight {color_class}"><pre>{block_text}</pre></div>' if color_class else f'<pre>{block_text}</pre>'
                html.append(highlighted)
            
            current_block = []
            prev_line = ""
        else:
            if is_new_paragraph(line, prev_line) and current_block:
                # Обрабатываем текущий блок перед началом нового
                block_text = " ".join(current_block)
                out, pred = test(model, tokenizer, block_text)
                pred_label_id = torch.argmax(out, dim=1).item()
                label = label_encoder.inverse_transform([pred_label_id])[0]
                risk_value = pred.item()
                
                if label != "neutral":
                    results.append({
                        'Текст': block_text,
                        'Класс': label,
                        'Уровень риска': risk_value,
                        'Цвет': get_risk_color(risk_value)
                    })
                
                color_class = get_risk_color(risk_value) if label not in ["neutral", "no_risk"] else ""
                highlighted = f'<div class="highlight {color_class}"><pre>{block_text}</pre></div>' if color_class else f'<pre>{block_text}</pre>'
                html.append(highlighted)
                
                current_block = []
            
            current_block.append(line)
            prev_line = line

    # Обработка последнего блока
    if current_block:
        block_text = " ".join(current_block)
        out, pred = test(model, tokenizer, block_text)
        pred_label_id = torch.argmax(out, dim=1).item()
        label = label_encoder.inverse_transform([pred_label_id])[0]
        risk_value = pred.item()
        
        if label != "neutral":
            results.append({
                'Текст': block_text,
                'Класс': label,
                'Уровень риска': risk_value,
            })
        
        color_class = get_risk_color(risk_value) if label not in ["neutral", "no_risk"] else ""
        highlighted = f'<div class="highlight {color_class}"><pre>{block_text}</pre></div>' if color_class else f'<pre>{block_text}</pre>'
        html.append(highlighted)

    # Сортировка по уровню риска (от высокого к низкому)
    results.sort(key=lambda x: x['Уровень риска'], reverse=True)

    # Добавляем таблицу с результатами
    html.append('<h2>Детальный анализ рисков</h2>')
    html.append('<table><tr><th>Уровень риска</th><th>Оценка</th><th>Класс</th><th>Текст</th></tr>')
    
    for result in results:
        risk_value = f"{result['Уровень риска']:.2f}"
        risk_level = ""
        if result['Уровень риска'] < 0.2:
            risk_level = "Очень низкий"
        elif 0.2 <= result['Уровень риска'] < 0.4:
            risk_level = "Низкий"
        elif 0.4 <= result['Уровень риска'] < 0.5:
            risk_level = "Умеренный"
        elif 0.5 <= result['Уровень риска'] < 0.6:
            risk_level = "Повышенный"
        elif 0.6 <= result['Уровень риска'] < 0.7:
            risk_level = "Высокий"
        elif 0.7 <= result['Уровень риска'] < 0.8:
            risk_level = "Очень высокий"
        else:
            risk_level = "Критический"
        
        html.append(
            f'<td>{risk_value}</td>'
            f'<td>{risk_level}</td>'
            f'<td>{result["Класс"]}</td>'
            f'<td><pre>{result["Текст"]}</pre></td>'
            f'</tr>'
        )
    
    html.append('</table></div></body></html>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

def main():
    pdf_to_sentences("doc.pdf", "output1.txt")
    
    lines = []
    with open("output1.txt", 'r', encoding="utf-8") as file:
        for line in file.readlines():
            lines.append(line.replace('\n', ''))
    
    model_id = "DeepPavlov/rubert-base-cased"
    dataset = pd.read_csv("data1.csv")
    unique_classes = dataset["label"].unique()

    tokenizer = BertTokenizer.from_pretrained(model_id)
    config = BertConfig.from_pretrained(model_id)
    model = DualBert(config=config, num_classes=len(unique_classes)).to(device)

    model.load_state_dict(torch.load("best_model.pth", map_location=device))
    model.eval()

    label_encoder = LabelEncoder()
    label_encoder.fit(unique_classes)
    
    test_on_file(model, tokenizer, label_encoder, lines, "result.html")

if __name__ == "__main__":
    main()