import fitz
import re
from transformers import BertModel, BertTokenizer, BertPreTrainedModel, BertConfig
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
import spacy

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
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text() + "\n"

    text = re.sub(r'(\w+)-(\r?\n)(\w+)', r'\1\3', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sentences))

def text_procesing(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'(\d)\s+(?=\d)', r'\1', text)
    return text

def test(model, tokenizer, text):
    input = tokenizer(text, max_length=256, padding=True, truncation=True, return_tensors="pt", return_token_type_ids=False).to(device)
    logits, pred = model(**input)
    return logits, pred

def test_on_file(model, tokenizer, label_encoder, lines, output_file):
    html = [
        '''<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Анализ рисков</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .highlight { padding: 2px 5px; border-radius: 3px; }
                .yellow { background: #fff3cd; }
                .orange { background: #ffe0b2; }
                .red { background: #f8d7da; }
                .green { background: #d4edda; }
            </style>
        </head>
        <body>
        '''
    ]

    for line in lines:
        if len(line) <= 5:
            continue
        out, pred = test(model, tokenizer, line)
        pred_label_id = torch.argmax(out, dim=1)
        pred_label_id.cpu()

        label = label_encoder.inverse_transform([pred_label_id.item()])[0]
        risk_value = pred.item()
        
        if label in ["neutral", "no_risk"]:
            html.append(f'<div>{line}</div>')
        # elif label == "no_risk":
        #     color_class = "green"
        #     highlighted = f'<span class="highlight {color_class}">{line}: {label}, {risk_value:.2f}</span>'
        #     html.append(f'<div>{highlighted}</div>')
        else:
            if risk_value < 0.6:
                color_class = "yellow"
            elif 0.6 <= risk_value <= 0.8:
                color_class = "orange"
            else:
                color_class = "red"
            
            highlighted = f'<span class="highlight {color_class}">{line}: {label}, {risk_value:.2f}</span>'
            html.append(f'<div>{highlighted}</div>')

    html.append('</body></html>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))


def main():
    pdf_to_sentences("doc2.pdf", "output2.txt")
    
    lines = []
    with open("output2.txt", 'r', encoding="utf-8") as file:
        for line in file.readlines():
            lines.append(text_procesing(line).replace('\n', ''))
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_id = "DeepPavlov/rubert-base-cased"

    unique_classes = ['legal_risk', 'no_risk', 'financial_risk', 'operational_risk', 'penalty_risk', 'procedural_risk', 'neutral']

    num_labels = len(unique_classes)

    tokenizer = BertTokenizer.from_pretrained(model_id)
    config = BertConfig.from_pretrained(model_id, num_labels=num_labels)
    model = DualBert.from_pretrained(model_id, config=config, num_classes=num_labels).to(device)
    
    label_encoder = LabelEncoder()
    label_encoder.fit(unique_classes)
    
    model.load_state_dict(torch.load('best_model.pth'))
    
    test_on_file(model, tokenizer, label_encoder, lines, "result2.html")


if __name__ == "__main__":
    main()