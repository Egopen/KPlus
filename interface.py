import fitz  # PyMuPDF
import re
from transformers import BertModel, BertTokenizer, BertPreTrainedModel, BertConfig
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Архитектура модели, выдающей label, class и risk_score
class TripleBert(BertPreTrainedModel):
    def __init__(self, config, num_classes_label, num_classes_class):
        super().__init__(config)
        self.bert = BertModel(config)
        
        # Голова для label
        self.classifier_label = nn.Sequential(
            nn.Linear(config.hidden_size, 300),
            nn.Linear(300, num_classes_label)
        )
        
        # Голова для class
        self.classifier_class = nn.Sequential(
            nn.Linear(config.hidden_size, 300),
            nn.Dropout(0.2),
            nn.Linear(300, num_classes_class)
        )
        
        # Регрессор для risk_score
        self.regressor = nn.Sequential(
            nn.Linear(config.hidden_size, 300),
            nn.Dropout(0.2),
            nn.Linear(300, 1)
        )
        
        self.init_weights()
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.bert(input_ids, attention_mask)
        pooled_output = outputs.pooler_output
        
        logits_label = self.classifier_label(pooled_output)
        logits_class = self.classifier_class(pooled_output)
        risk_score = self.regressor(pooled_output).squeeze(-1)
        
        return logits_label, logits_class, risk_score


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
            # Если текст выглядит как номер пункта (например, "3.4.13."),
            # объединяем его с предыдущим коротким блоком
            if re.match(r"^\d+\.\d+\.\d+\.$", text) and prev_text and len(prev_text) < 20:
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

    processed_text = []
    i = 0
    while i < len(formatted_text):
        line = formatted_text[i]
        if i < len(formatted_text) - 1 and re.match(r"^\d+\.\d+\.\d+\.$", line.strip()):
            next_line = formatted_text[i + 1]
            processed_text.append(line + " " + next_line)
            i += 2
        else:
            processed_text.append(line)
            i += 1

    final_text = []
    current_block = []
    for line in processed_text:
        line = line.strip()
        if not line:
            if current_block:
                final_text.append(" ".join(current_block))
                current_block = []
        else:
            if re.match(r"^\d+\.", line) or re.search(r"ПРЕДМЕТ ДОГОВОРА", line, re.IGNORECASE):
                if current_block:
                    final_text.append(" ".join(current_block))
                current_block = [line]
            else:
                current_block.append(line)
    if current_block:
        final_text.append(" ".join(current_block))

    intro_index = None
    for idx, block in enumerate(final_text):
        if re.search(r"^(1\.)", block) or re.search(r"ПРЕДМЕТ ДОГОВОРА", block, re.IGNORECASE):
            intro_index = idx
            break
    if intro_index is not None:
        final_text = final_text[intro_index:]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(final_text))


def text_processing(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"(\d)\s+(?=\d)", r"\1", text)
    return text


# Функция test возвращает все три выхода модели
def test(model, tokenizer, text):
    inp = tokenizer(
        text,
        max_length=256,
        padding=True,
        truncation=True,
        return_tensors="pt",
        return_token_type_ids=False,
    ).to(device)
    logits_label, logits_class, risk_score = model(**inp)
    return logits_label, logits_class, risk_score


# Функция для выбора цвета оформления по риск‑классу (из classifier_class)
def get_risk_color_by_class(risk_class):
    mapping = {
        "Умеренный": "risk-umerennyy",
        "Повышенный": "risk-povyshennyy",
        "Высокий": "risk-vysokiy",
        "Очень высокий": "risk-ochen-vysokiy",
        "Критический": "risk-kriticheskiy"
    }
    return mapping.get(risk_class, "risk-umerennyy")


def get_risk_label_by_class(risk_class):
    return risk_class


# Функция, возвращающая нижнюю и верхнюю границу для данной риск‑категории
def get_bounds_for_category(risk_category):
    if risk_category == "Умеренный":
        return 0, 49
    elif risk_category == "Повышенный":
        return 50, 59
    elif risk_category == "Высокий":
        return 60, 69
    elif risk_category == "Очень высокий":
        return 70, 79
    elif risk_category == "Критический":
        return 80, 100
    else:
        return 0, 100


# Новая функция: обрезаем (clamp) вероятность в пределах диапазона для выбранной категории
def get_clamped_probability(probability, risk_category):
    lower, upper = get_bounds_for_category(risk_category)
    # Если вероятность ниже нижней границы – возвращаем нижнюю
    # Если выше верхней – возвращаем верхнюю
    return max(lower, min(probability, upper))


def is_new_paragraph(line, prev_line):
    if not prev_line:
        return True
    if re.match(r"^\d+\.", line.strip()):
        return True
    if prev_line.strip().endswith(".") and line.strip() and line.strip()[0].isupper():
        return True
    return False


def generate_local_chart(risk_categories, risk_counts):
    bg_colors = ["#FFE29A", "#FFC371", "#FCA1A3", "#FA8A8E", "#D2696D"]
    edge_colors = ["#EDAA09", "#E68A25", "#E6534B", "#D03E39", "#A52923"]
    counts = [risk_counts[cat] for cat in risk_categories]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        risk_categories,
        counts,
        color=bg_colors,
        edgecolor=edge_colors,
        linewidth=1.5,
        alpha=0.9,
    )
    ax.set_title("Распределение рисков по категориям", fontsize=10)
    ax.set_xlabel("Категории риска", fontsize=8)
    ax.set_ylabel("Количество", fontsize=8)
    ax.set_ylim(0, max(counts) + 1)
    plt.subplots_adjust(bottom=0.25)
    ax.tick_params(axis="x", labelsize=7)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=7,
        )
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64


def test_on_file(model, tokenizer, label_encoder, class_encoder, lines, output_file):
    results = []          # Для таблицы: Вероятность, Риск, Лейбл, Текст, окончательная (обрезанная) вероятность
    contract_blocks = []  # Для полного текста договора

    current_block = []
    prev_line = ""
    for line in lines:
        line = line.strip()
        if not line:
            if current_block:
                block_text = " ".join(current_block)
                logits_label, logits_class, risk_score = test(model, tokenizer, block_text)
                pred_label_id = torch.argmax(logits_label, dim=1).item()
                pred_label = label_encoder.inverse_transform([pred_label_id])[0]
                if pred_label.lower() != "neutral":
                    pred_class_id = torch.argmax(logits_class, dim=1).item()
                    risk_class = class_encoder.inverse_transform([pred_class_id])[0]
                    css_class = get_risk_color_by_class(risk_class)
                    highlighted = f'<div class="highlight {css_class}"><pre>{block_text}</pre></div>'
                    probability = risk_score.item() * 100
                    # Обрезаем вероятность так, чтобы она попадала в указанный диапазон для категории
                    final_probability = get_clamped_probability(probability, risk_class)
                    results.append({
                        "Текст": block_text,
                        "Риск": risk_class,
                        "Вероятность": probability,
                        "Лейбл": pred_label,
                        "Окончательная вероятность": final_probability
                    })
                else:
                    highlighted = f"<pre>{block_text}</pre>"
                contract_blocks.append(highlighted)
            current_block = []
            prev_line = ""
        else:
            if is_new_paragraph(line, prev_line) and current_block:
                block_text = " ".join(current_block)
                logits_label, logits_class, risk_score = test(model, tokenizer, block_text)
                pred_label_id = torch.argmax(logits_label, dim=1).item()
                pred_label = label_encoder.inverse_transform([pred_label_id])[0]
                if pred_label.lower() != "neutral":
                    pred_class_id = torch.argmax(logits_class, dim=1).item()
                    risk_class = class_encoder.inverse_transform([pred_class_id])[0]
                    css_class = get_risk_color_by_class(risk_class)
                    highlighted = f'<div class="highlight {css_class}"><pre>{block_text}</pre></div>'
                    probability = risk_score.item() * 100
                    final_probability = get_clamped_probability(probability, risk_class)
                    results.append({
                        "Текст": block_text,
                        "Риск": risk_class,
                        "Вероятность": probability,
                        "Лейбл": pred_label,
                        "Окончательная вероятность": final_probability
                    })
                else:
                    highlighted = f"<pre>{block_text}</pre>"
                contract_blocks.append(highlighted)
                current_block = []
            current_block.append(line)
            prev_line = line
    if current_block:
        block_text = " ".join(current_block)
        logits_label, logits_class, risk_score = test(model, tokenizer, block_text)
        pred_label_id = torch.argmax(logits_label, dim=1).item()
        pred_label = label_encoder.inverse_transform([pred_label_id])[0]
        if pred_label.lower() != "neutral":
            pred_class_id = torch.argmax(logits_class, dim=1).item()
            risk_class = class_encoder.inverse_transform([pred_class_id])[0]
            css_class = get_risk_color_by_class(risk_class)
            highlighted = f'<div class="highlight {css_class}"><pre>{block_text}</pre></div>'
            probability = risk_score.item() * 100
            final_probability = get_clamped_probability(probability, risk_class)
            results.append({
                "Текст": block_text,
                "Риск": risk_class,
                "Вероятность": probability,
                "Лейбл": pred_label,
                "Окончательная вероятность": final_probability
            })
        else:
            highlighted = f"<pre>{block_text}</pre>"
        contract_blocks.append(highlighted)

    # Определяем порядок категорий риска для сортировки
    risk_order = {"Критический": 5, "Очень высокий": 4, "Высокий": 3, "Повышенный": 2, "Умеренный": 1}
    # Сортируем результаты сначала по порядку категории, затем по окончательной вероятности (убывание)
    results = sorted(results, key=lambda r: (risk_order.get(r["Риск"], 0), r["Окончательная вероятность"]), reverse=True)

    # Подсчет распределения по категориям
    risk_categories = ["Умеренный", "Повышенный", "Высокий", "Очень высокий", "Критический"]
    risk_counts = {cat: 0 for cat in risk_categories}
    for r in results:
        risk_cat = r["Риск"]
        if risk_cat in risk_counts:
            risk_counts[risk_cat] += 1

    summary_text = "Договор хороший." if risk_counts["Критический"] == 0 else "Договор не является хорошим из-за наличия критических рисков."

    img_base64 = generate_local_chart(risk_categories, risk_counts)
    chart_html = f'<div id="chart"><img src="data:image/png;base64,{img_base64}" alt="Распределение рисков"></div>'

    # Добавляем диапазоны риска в легенду
    risk_legend_html = """
    <div class="risk-legend">
        <div class="legend-item"><div class="legend-color risk-umerennyy"></div>Умеренный (0-49%)</div>
        <div class="legend-item"><div class="legend-color risk-povyshennyy"></div>Повышенный (50–59%)</div>
        <div class="legend-item"><div class="legend-color risk-vysokiy"></div>Высокий (60–69%)</div>
        <div class="legend-item"><div class="legend-color risk-ochen-vysokiy"></div>Очень высокий (70–79%)</div>
        <div class="legend-item"><div class="legend-color risk-kriticheskiy"></div>Критический (80–100%)</div>
    </div>
    """

    summary_html = f"""
    <div id="summary">
      <body>Внимание! Данный продукт является оценочным и не предполагает профессиональной консультации. Принимайте окончательные решения на свой риск.</body>
      <h2>Общий анализ рисков</h2>
      {risk_legend_html}
      <p>Распределение рисков по категориям:</p>
      <ul>
        <li>Умеренный: {risk_counts["Умеренный"]}</li>
        <li>Повышенный: {risk_counts["Повышенный"]}</li>
        <li>Высокий: {risk_counts["Высокий"]}</li>
        <li>Очень высокий: {risk_counts["Очень высокий"]}</li>
        <li>Критический: {risk_counts["Критический"]}</li>
      </ul>
      <p><strong>Итоговый вывод:</strong> {summary_text}</p>
      {chart_html}
    </div>
    """

    html_out = []
    html_out.append(
        """<!DOCTYPE html>
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
      .risk-umerennyy { background: #FFE29A; border-color: #EDAA09; }
      .risk-povyshennyy { background: #FFC371; border-color: #E68A25; }
      .risk-vysokiy { background: #FCA1A3; border-color: #E6534B; }
      .risk-ochen-vysokiy { background: #FA8A8E; border-color: #D03E39; }
      .risk-kriticheskiy { background: #D2696D; border-color: #A52923; }
      pre { white-space: pre-wrap; font-family: inherit; margin: 0; padding: 0; }
      table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.9em; }
      th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
      th { background-color: #f2f2f2; font-weight: bold; }
      tr:nth-child(even) { background-color: #f9f9f9; }
      h1 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px; }
      h2 { color: #444; margin-top: 30px; }
      .risk-legend { display: flex; flex-wrap: wrap; gap: 45px; margin: 20px 0; white-space: nowrap; }
      .legend-item { display: inline-block; width: 140px; text-align: center; font-size: 0.9em; }
      .legend-color { width: 20px; height: 20px; margin: 0 auto 5px; border-radius: 3px; border: 3px solid; }
      .legend-color.risk-umerennyy { background: #FFE29A; border-color: #EDAA09; }
      .legend-color.risk-povyshennyy { background: #FFC371; border-color: #E68A25; }
      .legend-color.risk-vysokiy { background: #FCA1A3; border-color: #E6534B; }
      .legend-color.risk-ochen-vysokiy { background: #FA8A8E; border-color: #D03E39; }
      .legend-color.risk-kriticheskiy { background: #D2696D; border-color: #A52923; }
  </style>
</head>
<body>
<div class="container">
<h1>Анализ рисков договора</h1>
"""
    )
    html_out.append(summary_html)
    html_out.append("<h2>Текст договора</h2>")
    html_out.extend(contract_blocks)
    html_out.append("<h2>Детальный анализ рисков</h2>")
    html_out.append("<table><tr><th>Вероятность (%)</th><th>Категория риска</th><th>Лейбл</th><th>Текст</th></tr>")
    for r in results:
        probability = int(r["Окончательная вероятность"])
        risk_cat = r["Риск"]
        css_class = get_risk_color_by_class(risk_cat)
        label_text = r["Лейбл"]
        html_out.append(
            f"<tr><td>{probability}%</td>"
            f'<td class="table-risk {css_class}">{risk_cat}</td>'
            f"<td>{label_text}</td>"
            f'<td><pre>{r["Текст"]}</pre></td></tr>'
        )
    html_out.append("</table></div></body></html>")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_out))


def main():
    pdf_to_sentences("doc.pdf", "output1.txt")
    lines = []
    with open("output1.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            clean_line = line.replace("\n", "").strip()
            if clean_line:
                lines.append(clean_line)
    model_id = "DeepPavlov/rubert-base-cased"
    dataset = pd.read_csv("data1.csv")
    label_encoder = LabelEncoder()
    label_encoder.fit(dataset["label"].unique())
    class_encoder = LabelEncoder()
    class_encoder.fit(dataset["class"].unique())
    
    tokenizer = BertTokenizer.from_pretrained(model_id)
    config = BertConfig.from_pretrained(model_id)
    num_classes_label = len(dataset["label"].unique())
    num_classes_class = len(dataset["class"].unique())
    model = TripleBert(config=config, num_classes_label=num_classes_label, num_classes_class=num_classes_class).to(device)
    model.load_state_dict(torch.load("best_model.pth", map_location=device))
    model.eval()
    test_on_file(model, tokenizer, label_encoder, class_encoder, lines, "result.html")


if __name__ == "__main__":
    main()
