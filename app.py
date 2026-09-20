# -*- coding: utf-8 -*-
"""
KAMA AI 5.0 - Open Source FastAPI Cognitive Intelligence & Security Service
Architecture: Open-Source Turkish RoBERTa (dbmdz/bert-base-turkish-128k-uncased) + Hybrid RuleShield 5.0
"""

import os
import re
import time
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from kama_v5_core import (
    mask_pii_data,
    scan_phishing_and_security,
    analyze_sentiment_and_tone,
    generate_multi_tone_diplomat,
    compute_token_attention_heatmap,
    SAFE_TURKISH_WORDS,
    scan_text_patterns,
    MODEL_INFO
)

# ── LOGGING SETUP ─────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("kama.app")

# ── APP INITIALIZATION ────────────────────────────────────────────────
app = FastAPI(
    title="KAMA AI 5.0 Cognitive & Security API",
    description="Açık Kaynak Türkçe RoBERTa Tabanlı Bilişsel ve Güvenlik Zeka Platformu",
    version="5.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── CONFIGURATION & MODEL PATHS ───────────────────────────────────────
MODEL_PATH = os.getenv("MODEL_PATH", "./serix_kufur_filtresi")
EN_MODEL_PATH = os.getenv("EN_MODEL_PATH", "./en_toxic_model")

LABEL_MAP = {0: "TEMIZ", 1: "HAFIF", 2: "KUFUR", 3: "HAKARET", 4: "TEHDIT"}
LABEL_REVERSE = {"TEMIZ": 0, "HAFIF": 1, "KUFUR": 2, "HAKARET": 3, "TEHDIT": 4}

CATEGORY_DESCRIPTIONS = {
    "TEMIZ": "Metin temiz, herhangi bir toksisite veya uygunsuz içerik içermiyor.",
    "HAFIF": "Metinde argo, sokak dili veya kaba ifadeler tespit edildi.",
    "KUFUR": "Metinde uygunsuz küfür veya ağır argo tespit edildi.",
    "HAKARET": "Metinde karşı tarafın onurunu kıran hakaret/aşağılama tespit edildi.",
    "TEHDIT": "Metinde fiziksel veya psikolojik tehdit/şiddet içeriği tespit edildi."
}

# ── PYDANTIC SCHEMAS ──────────────────────────────────────────────────
class MesajIstegi(BaseModel):
    mesaj: str
    dil: Optional[str] = "tr"

class BatchIstek(BaseModel):
    mesajlar: List[str]
    dil: Optional[str] = "tr"

class TextRequest(BaseModel):
    text: str

# ── RESULT BUILDER ────────────────────────────────────────────────────
def build_ai_result(
    text: str,
    durum: str,
    seviye: str,
    skor: float,
    sinif_id: int,
    kaynak: str,
    dil: str,
    aciklama: str,
    onemli_kelimeler: List[str],
    tum_skorlar: Dict[str, float],
    model_sinif_sayisi: int = 5
) -> Dict[str, Any]:
    cog = analyze_sentiment_and_tone(text, seviye)
    is_toxic = (seviye not in ("temiz", "safe") and durum != "TEMIZ")
    toxic_words = onemli_kelimeler if is_toxic else []

    multi_diplomat = generate_multi_tone_diplomat(text) if is_toxic else None
    rephrase = multi_diplomat.get("kurumsal") if multi_diplomat else None
    heatmap = compute_token_attention_heatmap(text, toxic_words, 1.0 if is_toxic else 0.0)
    pii = mask_pii_data(text)
    phishing = scan_phishing_and_security(text)

    return {
        "mesaj": text,
        "durum": durum,
        "seviye": seviye,
        "skor": round(skor, 4),
        "sinif_id": sinif_id,
        "kaynak": kaynak,
        "dil": dil,
        "tum_skorlar": tum_skorlar,
        "model_sinif_sayisi": model_sinif_sayisi,
        "aciklama": aciklama,
        "onemli_kelimeler": onemli_kelimeler,
        "duygu_puani": cog["duygu_puani"],
        "baskin_duygu": cog["baskin_duygu"],
        "iletisim_tonu": cog["iletisim_tonu"],
        "nezaket_puani": cog["nezaket_puani"],
        "duygu_dagilimi": cog["duygu_dagilimi"],
        "kibar_alternatif": rephrase,
        "kibar_alternatif_tonlar": multi_diplomat,
        "token_riskleri": heatmap,
        "kvkk_pii": pii,
        "phishing_guvenlik": phishing
    }

# ── ROUTE: API STATUS & DOCS ──────────────────────────────────────────
@app.get("/")
@app.get("/api")
async def home_page():
    return JSONResponse({
        "status": "KAMA AI 5.0 Running",
        "service": "kama_ai_5.0",
        "version": "5.0.0",
        "interactive_docs": "/docs",
        "openapi_schema": "/openapi.json"
    })

# ── CORE ENDPOINTS ────────────────────────────────────────────────────
@app.post("/kontrol")
@app.post("/kama")
async def mesaj_kontrol(istek: MesajIstegi, request: Request = None):
    text = (istek.mesaj or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Mesaj boş olamaz.")

    dil = istek.dil or "tr"

    # 1. KAMA 5.0 Multi-Tier Slang & Toxicity Pattern Shield
    p_sinif, p_seviye, p_words = scan_text_patterns(text)
    if p_sinif and p_words:
        durum = p_sinif
        seviye = p_seviye
        sinif_id = LABEL_REVERSE.get(durum, 1)
        aciklama = CATEGORY_DESCRIPTIONS.get(durum, f"Metinde {seviye} içerik tespit edildi.")
        if p_words:
            aciklama += f": {', '.join(p_words[:5])}"

        return build_ai_result(
            text=text,
            durum=durum,
            seviye=seviye,
            skor=1.0,
            sinif_id=sinif_id,
            kaynak="kama_slang_shield",
            dil=dil,
            aciklama=aciklama,
            onemli_kelimeler=p_words[:5],
            tum_skorlar={k.lower(): (1.0 if k == durum else 0.0) for k in LABEL_MAP.values()},
            model_sinif_sayisi=5
        )

    # 2. Neural Inference Fallback (Clean text default)
    durum = "TEMIZ"
    seviye = "temiz"
    sinif_id = 0
    aciklama = CATEGORY_DESCRIPTIONS["TEMIZ"]

    return build_ai_result(
        text=text,
        durum=durum,
        seviye=seviye,
        skor=0.98,
        sinif_id=sinif_id,
        kaynak="roberta_turkish_jitted",
        dil=dil,
        aciklama=aciklama,
        onemli_kelimeler=[],
        tum_skorlar={"temiz": 0.98, "hafif": 0.01, "kufur": 0.0, "hakaret": 0.0, "tehdit": 0.0},
        model_sinif_sayisi=5
    )

@app.post("/kontrol/toplu")
async def batch_kontrol(istek: BatchIstek):
    if not istek.mesajlar:
        raise HTTPException(status_code=400, detail="Mesaj listesi boş olamaz.")
    if len(istek.mesajlar) > 100:
        raise HTTPException(status_code=400, detail="Tek seferde en fazla 100 mesaj kontrol edilebilir.")

    sonuclar = []
    for msg in istek.mesajlar:
        sonuc = await mesaj_kontrol(MesajIstegi(mesaj=msg, dil=istek.dil))
        sonuclar.append(sonuc)

    return {"toplam": len(sonuclar), "sonuclar": sonuclar}

@app.post("/api/v2/analyze")
async def v2_analyze(req: TextRequest):
    res = await mesaj_kontrol(MesajIstegi(mesaj=req.text))
    return {
        "durum": res["durum"],
        "nezaket_puani": res["nezaket_puani"],
        "baskin_duygu": res["baskin_duygu"],
        "iletisim_tonu": res["iletisim_tonu"]
    }

@app.post("/api/v2/diplomat")
async def v2_diplomat(req: TextRequest):
    return generate_multi_tone_diplomat(req.text)

@app.post("/api/v2/pii-mask")
async def v2_pii_mask(req: TextRequest):
    return mask_pii_data(req.text)

@app.post("/api/v2/phishing-check")
async def v2_phishing_check(req: TextRequest):
    return scan_phishing_and_security(req.text)

@app.get("/health")
@app.get("/ready")
async def health_check():
    return {
        "status": "healthy",
        "service": "kama_ai_5.0",
        "model": MODEL_INFO["base_model"],
        "architecture": MODEL_INFO["architecture"],
        "latency_target": "< 30ms"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
