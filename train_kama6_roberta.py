# -*- coding: utf-8 -*-
"""
KAMA AI 6.0 - PyTorch / HuggingFace RoBERTa Fine-Tuning Pipeline
Base Model: dbmdz/bert-base-turkish-128k-uncased (BERTurk / Turkish RoBERTa)
Origin Edge Deep Neural Architecture
"""

import os
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import List, Dict, Any

# ── 1. SAMPLE / BENCHMARK TURKISH DATASET ──────────────────────────────
DATASET_SAMPLES = [
    # TEMIZ (Clean)
    {"text": "Merhaba, projenin son durumunu öğrenebilir miyim?", "label": 0},
    {"text": "Yarın saat 14:00'te toplantı yapalım.", "label": 0},
    {"text": "Harika bir çalışma olmuş, ellerinize sağlık.", "label": 0},
    {"text": "Siparişiniz kargoya verildi, takip numarası iletilmiştir.", "label": 0},
    {"text": "Eksik belgeleri en kısa sürede tamamlayıp göndereceğim.", "label": 0},
    {"text": "Kamu kurumlarıyla ilgili süreç tamamlandı.", "label": 0},
    
    # HAFIF_ARGO (Slang)
    {"text": "Lan oğlum boş yapma işine bak.", "label": 1},
    {"text": "Ulan ne adamsın ya güldürdün beni.", "label": 1},
    {"text": "Bırak bu kolpa işleri dümenci seni.", "label": 1},
    {"text": "Lavuk yine ortalığı karıştırmış.", "label": 1},
    
    # HAKARET (Insult)
    {"text": "Sen tam bir gerizekalısın hiçbir şey bilmiyorsun.", "label": 2},
    {"text": "Aptal herif projeyi batırdın.", "label": 2},
    {"text": "Şerefsiz ve karaktersiz bir insansın.", "label": 2},
    {"text": "Rezil herif utanmadan buraya gelmiş.", "label": 2},
    
    # KUFUR (Profanity)
    {"text": "Siktir git buradan bir daha yazma.", "label": 3},
    {"text": "Senin yapacağın işi sikeyim amk.", "label": 3},
    {"text": "Yarrak kafalı sus artık.", "label": 3},
    {"text": "Orospu çocuğu seni.", "label": 3},
    
    # TEHDIT (Threat)
    {"text": "Seni bulup geberteceğim bekle sen.", "label": 4},
    {"text": "Evini basıp hayatını karartırım.", "label": 4},
    {"text": "Seni yaşatmam bu mahallede.", "label": 4},
    
    # SIBER_ZORBALIK (Cyberbullying)
    {"text": "Sen bir hiçsin, kimse seni sevmiyor git kendini öldür.", "label": 5},
    {"text": "Rezil edeceğim seni bütün okula yayacağım.", "label": 5},
    {"text": "Ezik herif ağla şimdi kudur.", "label": 5},
    
    # COCUK_RISKI (Child Safety / Grooming)
    {"text": "Ev adresini ve telefon numaranı ver gizli konuşalım.", "label": 6},
    {"text": "Kendini çek fotoğraf at aramızda kalsın kimseye söyleme.", "label": 6},
    {"text": "Hangi okuldasın çıkışta parkta buluşalım mı?", "label": 6}
]

CLASS_NAMES = ["TEMIZ", "HAFIF_ARGO", "HAKARET", "KUFUR", "TEHDIT", "SIBER_ZORBALIK", "COCUK_RISKI"]

class KamaDataset(Dataset):
    def __init__(self, data: List[Dict[str, Any]], tokenizer, max_length: int = 128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        encoding = self.tokenizer(
            item["text"],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(item["label"], dtype=torch.long)
        }

def train_kama_model(
    model_name: str = "dbmdz/bert-base-turkish-128k-uncased",
    output_dir: str = "./kama_v6_checkpoint",
    epochs: int = 4,
    batch_size: int = 8,
    lr: float = 2e-5
):
    """Fine-tunes Turkish RoBERTa model with PyTorch & HuggingFace."""
    print(f"🚀 [KAMA AI 6.0] RoBERTa Fine-Tuning Başlatılıyor...")
    print(f"📦 Model: {model_name} | Sınıf Sayısı: {len(CLASS_NAMES)}")
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
    except ImportError:
        print("⚠️ transformers ve torch kütüphaneleri gerekli: pip install transformers torch")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"⚡ Çalışma Cihazı: {device}")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(CLASS_NAMES))
    model.to(device)

    dataset = KamaDataset(DATASET_SAMPLES, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for batch in dataloader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = loss_fn(outputs.logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"  [Epoch {epoch+1}/{epochs}] Ortalama Kayıp (Loss): {avg_loss:.4f}")

    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"✅ Model başarıyla kaydedildi: {output_dir}")

if __name__ == "__main__":
    print("KAMA AI 6.0 RoBERTa Training Module Ready.")
