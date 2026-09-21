# -*- coding: utf-8 -*-
"""
KAMA AI 1.0 - OFFICIAL FOUNDATION PRODUCTION SERVICE
FastAPI Cognitive Intelligence, Security Shield & NLP Engine
Release 1.0.0 General Availability
"""

import os
import time
import logging
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from kama_core import (
    analyze_content,
    mask_pii_data,
    generate_multi_tone_diplomat,
    MODEL_INFO
)

# ── LOGGING SETUP ─────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("kama.app")

# ── APP INITIALIZATION ────────────────────────────────────────────────
app = FastAPI(
    title="KAMA AI 1.0 Production API",
    description="Açık Kaynak Türkçe RoBERTa Tabanlı Bilişsel ve Güvenlik Zeka Platformu (v1.0 General Availability)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── PYDANTIC SCHEMAS ──────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    mesaj: Optional[str] = None
    dil: Optional[str] = "tr"

class BatchRequest(BaseModel):
    items: Optional[List[str]] = None
    mesajlar: Optional[List[str]] = None
    dil: Optional[str] = "tr"

class DiplomatRequest(BaseModel):
    text: str

class PIIRequest(BaseModel):
    text: str

# ── API ROUTES (V1 PRODUCTION) ────────────────────────────────────────

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "kama-ai",
        "version": "1.0.0",
        "model_status": "ready",
        "timestamp": time.time()
    }

@app.get("/v1/model-info")
def get_model_info():
    return MODEL_INFO

@app.post("/v1/analyze")
@app.post("/v1/denetle")
@app.post("/denetle")
@app.post("/analyze")
def api_analyze(req: AnalyzeRequest):
    content = req.text if req.text is not None else (req.mesaj or "")
    start_time = time.time()
    result = analyze_content(content)
    result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
    return result

@app.post("/v1/batch")
@app.post("/batch")
def api_batch(req: BatchRequest):
    items = req.items if req.items is not None else (req.mesajlar or [])
    if not items:
        return {"total": 0, "results": []}
    
    start_time = time.time()
    results = [analyze_content(t) for t in items]
    return {
        "total": len(results),
        "latency_ms": round((time.time() - start_time) * 1000, 2),
        "results": results
    }

@app.post("/v1/diplomat")
def api_diplomat(req: DiplomatRequest):
    if not req.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return {
        "original": req.text,
        "tones": generate_multi_tone_diplomat(req.text)
    }

@app.post("/v1/mask-pii")
def api_mask_pii(req: PIIRequest):
    return mask_pii_data(req.text)

# ── INTERACTIVE WEB DASHBOARD (STUDIO) ────────────────────────────────
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KAMA AI 1.0 — Production Intelligence & Security Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background: #030712;
      color: #f3f4f6;
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 60%),
        radial-gradient(circle at 100% 100%, rgba(16, 185, 129, 0.06) 0%, transparent 50%);
    }
    .glass {
      background: rgba(17, 24, 39, 0.7);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1.25rem;
    }
  </style>
</head>
<body class="min-h-screen p-4 md:p-8 flex flex-col items-center justify-start space-y-8">

  <header class="text-center max-w-2xl space-y-3">
    <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-mono font-bold">
      <span>🛡️ KAMA AI 1.0 Production Model (GA)</span>
    </div>
    <h1 class="text-3xl md:text-5xl font-black text-white tracking-tight">
      KAMA AI <span class="bg-gradient-to-r from-indigo-400 via-purple-300 to-emerald-400 bg-clip-text text-transparent">1.0</span> Studio
    </h1>
    <p class="text-xs md:text-sm text-slate-400">
      Açık Kaynak Türkçe RoBERTa Transformer Mimarisi, 7 Sınıflı Toksisite Tespiti, Sansür Çözücü ve KVKK PII Gizlilik Motoru.
    </p>
  </header>

  <main class="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 gap-6">

    <!-- Input Card -->
    <div class="glass p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <h2 class="font-bold text-white text-sm flex items-center gap-2">
          <span>✍️</span> Metin Denetleme & Analiz
        </h2>
        <span class="text-xs text-indigo-400 font-mono">v1.0 Live</span>
      </div>

      <textarea id="textInput" rows="5" class="w-full p-3.5 bg-slate-950 rounded-xl border border-slate-800 text-xs font-mono text-white focus:border-indigo-500 outline-none leading-relaxed" placeholder="Analiz edilecek Türkçe metni buraya yazın veya leetspeak deneyin (örn: s.i.k, @mk, 0rospu, vb.)..."></textarea>

      <div class="flex gap-2">
        <button onclick="runAnalysis()" class="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl transition-all shadow-lg shadow-indigo-600/20">
          🚀 KAMA 1.0 ile Analiz Et
        </button>
        <button onclick="fillSample()" class="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-xl border border-slate-700">
          Örnek Doldur
        </button>
      </div>

      <div class="pt-2">
        <div class="text-[11px] font-mono text-slate-400 mb-1">Desteklenen Sınıflar:</div>
        <div class="flex flex-wrap gap-1.5">
          <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-mono">TEMIZ</span>
          <span class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[10px] font-mono">HAFIF_ARGO</span>
          <span class="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 text-[10px] font-mono">HAKARET</span>
          <span class="px-2 py-0.5 rounded bg-red-500/10 text-red-400 text-[10px] font-mono">KUFUR</span>
          <span class="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 text-[10px] font-mono">TEHDIT</span>
          <span class="px-2 py-0.5 rounded bg-pink-500/10 text-pink-400 text-[10px] font-mono">SIBER_ZORBALIK</span>
          <span class="px-2 py-0.5 rounded bg-yellow-500/10 text-yellow-400 text-[10px] font-mono">COCUK_RISKI</span>
        </div>
      </div>
    </div>

    <!-- Output Result Card -->
    <div class="glass p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <h2 class="font-bold text-white text-sm flex items-center gap-2">
          <span>📊</span> Analiz Sonuçları
        </h2>
        <span id="durumBadge" class="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-slate-800 text-slate-400">Bekleniyor</span>
      </div>

      <div id="resultBox" class="space-y-3">
        <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
          <div class="text-[11px] text-slate-400 font-mono">Güven Skoru & Gecikme:</div>
          <div id="scoreVal" class="text-sm font-bold text-white font-mono mt-0.5">-</div>
        </div>

        <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
          <div class="text-[11px] text-slate-400 font-mono">Açıklama:</div>
          <div id="descVal" class="text-xs text-slate-300 mt-0.5">Analiz başlatılmadı.</div>
        </div>

        <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
          <div class="text-[11px] text-slate-400 font-mono">KVKK / PII Maskeleme:</div>
          <div id="piiVal" class="text-xs text-emerald-400 font-mono mt-0.5">-</div>
        </div>

        <div id="diplomatCard" class="p-3 bg-slate-950 rounded-xl border border-slate-800 hidden">
          <div class="text-[11px] text-indigo-400 font-mono">AI Diplomat (Kurumsal Yeniden Yazım):</div>
          <div id="diplomatVal" class="text-xs text-slate-300 mt-0.5 italic">-</div>
        </div>
      </div>
    </div>

  </main>

  <footer class="text-center text-xs text-slate-500 pt-8 pb-12">
    © 2026 Origin Edge & KAMA AI Foundation. MIT Lisanslı Açık Kaynak Platform.
  </footer>

  <script>
    const samples = [
      "Merhaba, proje dökümantasyonunu çok beğendim, emeğinize sağlık!",
      "Sen ne s.a.l.a.k bir adamsın, a.m.k senin gibi lavuğun",
      "TCKN: 12345678901 ve telefonum 0532 123 45 67, IBAN: TR12 3456 7890 1234 5678 9012 34",
      "Seni mahvedeceğim, gününü göreceksin evini bulurum!",
      "Kaç yaşındasın, annen evde mi yalnız mısın kameranı aç"
    ];
    let sampleIdx = 0;

    function fillSample() {
      document.getElementById('textInput').value = samples[sampleIdx % samples.length];
      sampleIdx++;
    }

    async function runAnalysis() {
      const txt = document.getElementById('textInput').value.trim();
      if (!txt) return;

      const badge = document.getElementById('durumBadge');
      badge.className = 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-indigo-500/20 text-indigo-400';
      badge.innerText = 'Analiz Ediliyor...';

      try {
        const res = await fetch('/v1/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: txt })
        });
        const data = await res.json();

        // Update badge
        if (data.durum === 'TEMIZ') {
          badge.className = 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400';
          badge.innerText = '🟢 TEMİZ';
        } else {
          badge.className = 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-rose-500/20 text-rose-400';
          badge.innerText = '🔴 ' + data.durum;
        }

        document.getElementById('scoreVal').innerText = `%${Math.round(data.guven_skoru * 100)} (${data.latency_ms || 18.5} ms)`;
        document.getElementById('descVal').innerText = data.aciklama;
        document.getElementById('piiVal').innerText = data.pii?.masked || txt;

        const dipCard = document.getElementById('diplomatCard');
        if (data.diplomat && data.diplomat.kurumsal) {
          dipCard.classList.remove('hidden');
          document.getElementById('diplomatVal').innerText = data.diplomat.kurumsal;
        } else {
          dipCard.classList.add('hidden');
        }

      } catch (err) {
        badge.className = 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-red-500/20 text-red-400';
        badge.innerText = 'Hata';
      }
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index_studio():
    return DASHBOARD_HTML

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
