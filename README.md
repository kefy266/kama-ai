# ⚡ KAMA AI 6.0 — Bilişsel ve Güvenlik Zeka Platformu

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![RoBERTa Turkish](https://img.shields.io/badge/Backbone-RoBERTa%20Turkish-00f5ff.svg)](https://huggingface.co/dbmdz/bert-base-turkish-128k-uncased)

**KAMA AI 6.0**, Açık Kaynak Türkçe RoBERTa (`dbmdz/bert-base-turkish-128k-uncased`) transformer mimarisi üzerine inşa edilmiş, karakter sansürü atlatma (leetspeak resolver), çocuk güvenliği ve siber zorbalık kalkanı, 4 tonlu yapay zeka diplomat dönüşümü, algoritmik KVKK veri maskelemesi ve e-posta oltalama (phishing) tespit sistemi içeren hibrit bir bilişsel yapay zeka motorudur.

---

## 🌟 KAMA AI 6.0 Temel Yetenekleri

1. **🧠 Derin RoBERTa Türkçe Sınıflandırma:**
   - 12 Transformer Bloğu, 128.000 Türkçe Vocab, 110M Parametre.
   - 7 Sınıf Bilişsel Analiz: `TEMIZ`, `HAFIF_ARGO`, `HAKARET`, `KUFUR`, `TEHDIT`, `SIBER_ZORBALIK`, `COCUK_RISKI`.
   - **Hard-Negative Whitelist:** *"kamu"*, *"eksik"*, *"psikoloji"*, *"klasik"*, *"amca"* gibi masum kelimelerde %100 sıfır yanlış pozitif.

2. **🛡️ Filtre Atlama & Leetspeak Çözücü (Evasion Resolver):**
   - Noktalı, boşluklu, tireli veya sembolik küfür atlatma hilelerini çözer (`@.m.k` ➔ `amk`, `s.i.k` ➔ `sik`, `0.r.0.s.p.u` ➔ `orospu`, `s!k!k` ➔ `sikik`).
   - Homoglif (Cyrillic / Greek benzer harf) deşifresi.

3. **👶 Çocuk Güvenliği & Siber Zorbalık Kalkanı:**
   - Minor grooming, gizli buluşma, kişisel bilgi (adres, telefon, okul) isteme girişimlerini tespit eder (`COCUK_RISKI`).
   - Akran zorbalığı ve dışlama kalıplarını analiz eder (`SIBER_ZORBALIK`).

4. **🤖 Gelişmiş AI Diplomat v2 (4 Ton):**
   - Sert veya kaba ifadeleri anlam kaybı olmadan **4 farklı tonda** dönüştürme:
     - 🏢 **Kurumsal:** Profesyonel iş dili ve resmi yazışmalar.
     - 🤝 **Arkadaş Canlısı:** Samimi, sıcak ve empatik üslup.
     - 💡 **Yapıcı:** Çözüm odaklı ve gelişim dili.
     - 🕊️ **Sakinleştirici:** Gerginliği yatıştıran arabulucu ton.

5. **🔒 Algoritmik KVKK / PII Veri Kalkanı:**
   - **T.C. Kimlik No:** 11 haneli kural ve Modulo-10 checksum doğrulaması.
   - **TR IBAN:** Modulo-97 format ve banka kod kontrolü.
   - **Kredi Kartı:** Luhn algoritması kontrollü tam doğrulama.
   - **Telefon & E-posta:** Regex ve sınır kontrollü otomatik maskeleme.

6. **🎣 EdgeMail Phishing & Güvenlik Kalkanı:**
   - Aciliyet ve panik tetikleyicileri (*"Hesabınız askıya alındı"*, *"24 saat içinde şifrenizi girin"*).
   - Şüpheli URL ve alan adı imza tespiti.

---

## 🚀 Hızlı Başlangıç (Quickstart)

### 1. Yerel Kurulum (Python)

```bash
# 1. Depoyu klonlayın
git clone https://github.com/kefy266/kama-ai-5.0.git
cd kama-ai-5.0

# 2. Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Sunucuyu başlatın
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📡 SDK ve Entegrasyonlar

### Python SDK (`kama_sdk.py`)
```python
from kama_sdk import KamaAI

kama = KamaAI(api_url="https://ai.oedge.xyz")

# Bilişsel Analiz
sonuc = kama.analyze("s.i.k.i.k herif @.m.k")
print(sonuc["sinif"]) # KUFUR
print(sonuc["toksisite_skoru"]) # 0.95

# AI Diplomat Dönüşümü
kibar = kama.rewrite_diplomat("Projeyi batırdın boş yapma", tone="KURUMSAL")
print(kibar["diplomatik_versiyon"])
```

### Node.js / Discord Bot Moderasyonu (`kama_sdk.js`)
```javascript
const { Client, GatewayIntentBits } = require('discord.js');
const { KamaAI } = require('./kama_sdk');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const kama = new KamaAI({ apiUrl: 'https://ai.oedge.xyz' });

// Mesajları otomatik denetleyen middleware
client.on('messageCreate', kama.createDiscordMiddleware({ autoDelete: true, warnUser: true }));
client.login(process.env.DISCORD_TOKEN);
```

---

## 🧠 RoBERTa Fine-Tuning Pipeline

Model ağırlıklarını kendi Türkçe veri setinizle eğitmek için:

```bash
python3 train_kama6_roberta.py
```

---

## 📄 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Origin Edge Deep Neural Architecture tarafından geliştirilmiştir.
