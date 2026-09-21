# 🛡️ KAMA AI 1.0 — Foundation Production Model

[![Version](https://img.shields.io/badge/version-1.0.0--GA-emerald.svg)](https://github.com/kefy266/kama-ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-indigo.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688.svg)](https://fastapi.tiangolo.com)

**KAMA AI 1.0**, Türkçeye özel eğitilmiş açık kaynaklı **RoBERTa Transformer mimarisi** ve bilişsel güvenlik kalkanını bir araya getiren yeni nesil yapay zeka denetim, siber güvenlik ve içerik moderasyon platformudur.

KAMA AI artık beta sürecinden çıkmış olup **1.0.0 General Availability (GA)** kararlı sürümündedir.

---

## ⚡ Temel Yetenekler & Özellikler

- **🛡️ 7 Sınıflı Derin Toksisite Tespiti:**
  1. `TEMIZ` (Güvenli & Temiz İçerik)
  2. `HAFIF_ARGO` (Sokak Dili & Hafif Argo)
  3. `HAKARET` (Aşağılama & Kişilik Haklarına Saldırı)
  4. `KUFUR` (Doğrudan Küfür & Ağır Argo)
  5. `TEHDIT` (Fiziksel / Psikolojik Şiddet & Tehdit)
  6. `SIBER_ZORBALIK` (Siber Zorbalık & İtibar Suikastı)
  7. `COCUK_RISKI` (Çocuk İstismarı & Şüpheli İletişim Koruması)

- **🔤 Leetspeak & Evasion Resolver (Sansür Atlatma Çözücü):**
  - Noktalı, boşluklu veya sembollü filtre atlatma taktiklerini anında deşifre eder (`s.i.k.i.k`, `@.m.k`, `0.r.0.s.p.u`).
  - Kiril/Grekçe harf ikamelerini (homoglyphs) ve aşırı harf tekrarlarını otomatik olarak çözer.

- **🔒 KVKK & PII Veri Maskeleme Motoru:**
  - TCKN, Telefon Numarası, Kredi Kartı, IBAN, E-posta ve IP adreslerini otomatik olarak tespit edip sansürler.

- **🕊️ 4 Tonlu AI Diplomat (Yeniden Yazıcı):**
  - Toksik veya kaba ifadeleri 4 farklı profesyonel üsluba çevirir:
    - *Kurumsal (Corporate)*
    - *Yapıcı (Constructive)*
    - *Sakin (Calm)*
    - *Diplomatik (Diplomatic)*

- **🎯 Token Düzeyinde Attention Heatmap (Açıklanabilir Yapay Zeka):**
  - Modelin hangi kelimelere odaklandığını gösteren dikkat ağırlıkları.

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
git clone https://github.com/kefy266/kama-ai.git
cd kama-ai
pip install -r requirements.txt
```

### 2. Sunucuyu Başlatma
```bash
python app.py
# veya
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Arayüz ve test stüdyosuna erişim: **`http://localhost:8000`**  
Swagger API Dokümantasyonu: **`http://localhost:8000/docs`**

---

## 📡 API Kullanımı

### Metin Analizi (`POST /v1/analyze`)
```bash
curl -X POST "http://localhost:8000/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Burada s.i.k.i.k laflar edenler var @mk"}'
```

**Örnek Yanıt:**
```json
{
  "durum": "KUFUR",
  "sinif_id": 3,
  "kategori": "KUFUR",
  "guven_skoru": 0.94,
  "guvenlik_durumu": "TEHLIKELI",
  "toksik_mi": true,
  "onemli_kelimeler": ["sikik", "amk"],
  "tum_skorlar": {
    "TEMIZ": 0.06,
    "HAFIF_ARGO": 0.0,
    "HAKARET": 0.0,
    "KUFUR": 0.94,
    "TEHDIT": 0.0,
    "SIBER_ZORBALIK": 0.0,
    "COCUK_RISKI": 0.0
  },
  "diplomat": {
    "kurumsal": "Konuyla ilgili değerlendirmem şudur: Burada uygunsuz ifade laflar edenler var uygunsuz ifade. Profesyonel standartlar çerçevesinde ilerleyelim."
  },
  "pii": {
    "original": "Burada s.i.k.i.k laflar edenler var @mk",
    "masked": "Burada s.i.k.i.k laflar edenler var @mk",
    "detected_types": []
  },
  "latency_ms": 1.2
}
```

---

## 📦 SDK Kullanımı

### Python SDK (`kama_sdk.py`)
```python
from kama_sdk import KamaAI

kama = KamaAI(base_url="http://localhost:8000")

# Tekli analiz
res = kama.analyze("Projenin yeni sürümü harika olmuş!")
print(res["durum"]) # "TEMIZ"

# KVKK Maskeleme
pii = kama.mask_pii("Telefonum 0532 123 45 67, TCKN 12345678901")
print(pii["masked"]) # "Telefonum 05** *** ** 67, TCKN 123******01"
```

### JavaScript / Node.js SDK (`kama_sdk.js`)
```javascript
const KamaAI = require('./kama_sdk');
const kama = KamaAI.createClient({ baseUrl: 'http://localhost:8000' });

async function check() {
  const res = await kama.analyze('Test mesajı');
  console.log(res.durum, res.guven_skoru);
}
check();
```

---

## 🧪 Testleri Çalıştırma
```bash
python test_kama1_engine.py
```

---

## 📄 Lisans
Bu proje **MIT Lisansı** altında açık kaynaklı olarak yayınlanmıştır. Origin Edge ekosisteminin bir parçasıdır.
