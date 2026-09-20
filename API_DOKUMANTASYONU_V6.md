# 🛡️ KAMA AI 6.0 - Bilişsel Zeka ve Güvenlik Platformu

> **Mimari:** Açık Kaynak Türkçe RoBERTa (`dbmdz/bert-base-turkish-128k-uncased`) + KAMA 6.0 Hybrid Cognitive Shield  
> **Geliştirici:** Origin Edge Deep Neural Architecture  
> **Sürüm:** 6.0.0 (Ultra Cognitive & Shield)  
> **Lisans:** MIT License  

---

## 🚀 KAMA AI 6.0 İle Eklenen Yenilikler

### 1. 🔤 Filtre Atlama & Karakter Sansürü Kalkanı (Leetspeak / Evasion Resolver)
- Kullanıcıların kelime arasına nokta, alt çizgi, boşluk veya benzeri karakterler koyarak filtreleri atlatma girişimlerini engeller.
- Homoglif (Cyrillic / Greek harf benzerleri) ve sayısal yer değiştirmeleri otomatik çözer:
  - `@.m.k` ➔ `amk`
  - `s.i.k` ➔ `sik`
  - `0.r.0.s.p.u` ➔ `orospu`
  - `s!k!k` ➔ `sikik`
  - `p 1 c` ➔ `pic`

### 2. 👶 Çocuk Güvenliği & Siber Zorbalık Tespiti (EdgeMail Çocuk Kalkanı)
- Minor grooming (çocuklardan gizli bilgi, adres, telefon veya fotoğraf isteme) tespit katmanı (`COCUK_RISKI`).
- Akran ve siber zorbalık tespit katmanı (`SIBER_ZORBALIK`).

### 3. 🎭 AI Diplomat v2 (4 Farklı Ton)
- **KURUMSAL:** Profesyonel iş dili ve saygılı üslup.
- **ARKADAS_CANLISI:** Empatik, sıcak ve samimi ton.
- **YAPICI:** Çözüm odaklı ve yapıcı öneri dili.
- **SAKINLESTIRICI:** Stres düşürücü ve arabulucu sakin ton.

### 4. 🧠 RoBERTa PyTorch Fine-Tuning Pipeline
- `train_kama6_roberta.py` ile `dbmdz/bert-base-turkish-128k-uncased` temelinde özel Türkçe veri setiyle model ağırlık eğitimi ve ONNX dışa aktarım desteği.

### 5. 🔌 Çoklu SDK ve Bot Entegrasyonları
- **Python SDK (`kama_sdk.py`):** `KamaAI.analyze()`, `KamaAI.rewrite_diplomat()`, `KamaAI.mask_pii()`
- **Node.js SDK (`kama_sdk.js`):** Discord.js ve Telegram botları için hazır `createDiscordMiddleware` desteği.

---

## 📡 API Endpointleri (v6)

### `POST /api/v6/analyze`
Metni deobfuscation, duygu/toksisite, KVKK ve çocuk güvenliği açılarından tam kapsamlı analiz eder.

#### Örnek İstek:
```json
{
  "metin": "Sen tam bir gerizekalısın @.m.k"
}
```

#### Örnek Yanıt:
```json
{
  "sinif": "KUFUR",
  "toksisite_skoru": 0.95,
  "guvenilirlik": 0.96,
  "deobfuscated_metin": "sen tam bir gerizekalisin amk",
  "tespit_edilen_kategoriler": ["HAKARET", "KUFUR"],
  "dikkat_haritasi": [
    {"token": "Sen", "attention_weight": 0.05, "is_flagged": false},
    {"token": "tam", "attention_weight": 0.02, "is_flagged": false},
    {"token": "bir", "attention_weight": 0.05, "is_flagged": false},
    {"token": "gerizekalısın", "attention_weight": 0.95, "is_flagged": true},
    {"token": "@.m.k", "attention_weight": 0.95, "is_flagged": true}
  ],
  "diplomat_onerileri": {
    "kurumsal": "Saygılarımla iletmek isterim ki; Sen bu konuda farklı bir yaklaşım sergileyen birisin.",
    "arkadas_canlisi": "Selamlar! Konuyu birlikte tatlılıkla çözebiliriz 😊",
    "yapici": "Gelişime açık bir öneri olarak: süreci daha verimli kılalım.",
    "sakinlestirici": "Anlıyorum, bu durum stresli hissettirmiş olabilir, sakin kalarak çözelim."
  },
  "cocuk_icin_guvenli_mi": false
}
```

---

## 💻 Kullanım Örnekleri

### Python ile Kullanım:
```python
from kama_sdk import KamaAI

kama = KamaAI(api_url="https://ai.oedge.xyz")
sonuc = kama.analyze("s.i.k.i.k herif")
print(sonuc["sinif"]) # KUFUR
```

### Discord Bot Moderasyonu (Node.js):
```javascript
const { Client, GatewayIntentBits } = require('discord.js');
const { KamaAI } = require('./kama_sdk');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const kama = new KamaAI();

client.on('messageCreate', kama.createDiscordMiddleware({ autoDelete: true, warnUser: true }));
client.login('DISCORD_TOKEN');
```
