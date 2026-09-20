# -*- coding: utf-8 -*-
"""
KAMA AI 6.0 - Test & Verification Suite
"""

import sys
import os

# Import local core
sys.path.insert(0, os.path.dirname(__file__))
from kama_v6_core import analyze_cognitive_text, resolve_leetspeak_and_evasion, rewrite_with_diplomat_v2

def run_tests():
    print("🧪 [TEST 1] Karakter Sansürü & Leetspeak Çözücü Testi:")
    test_cases = [
        ("s.i.k", "sik"),
        ("@.m.k", "amk"),
        ("0.r.0.s.p.u", "orospu"),
        ("s!k!k", "sikik"),
        ("p 1 c", "pic")
    ]
    for raw, expected in test_cases:
        res = resolve_leetspeak_and_evasion(raw)
        print(f"  Girdi: '{raw}' -> Çözülen: '{res}'")
        assert expected in res or res == expected, f"Hata: {raw} -> {res}"
    print("  ✅ Leetspeak çözücü başarıyla geçti!\n")

    print("🧪 [TEST 2] Hard-Negative (Masum Kelimeler) Yanlış Pozitif Testi:")
    safe_cases = [
        "Kamusal hizmetlerin eksiksiz yürütülmesi gerekmektedir.",
        "Amcam ile birlikte klasik müzik dinledik.",
        "Bu sektörde psikolojik danışmanlık çok önemlidir.",
        "Selamlar, traktör yedek parça siparişi vermiştik."
    ]
    for text in safe_cases:
        res = analyze_cognitive_text(text)
        print(f"  Metin: '{text}' -> Sınıf: {res['sinif']} (Skor: {res['toksisite_skoru']})")
        assert res["sinif"] == "TEMIZ", f"Hatalı Pozitif Yakalandı: {text} -> {res['sinif']}"
    print("  ✅ Hard-negative testleri 100% temiz geçti!\n")

    print("🧪 [TEST 3] Çocuk Güvenliği & Siber Zorbalık Testi:")
    child_cases = [
        ("Hangi okuldasın telefon numaranı ver gizli konuşalım kimseye söyleme.", "COCUK_RISKI"),
        ("Sen bir hiçsin, kudur git kendini öldür ezik.", "SIBER_ZORBALIK")
    ]
    for text, exp_class in child_cases:
        res = analyze_cognitive_text(text)
        print(f"  Metin: '{text}' -> Sınıf: {res['sinif']}")
        assert res["sinif"] in [exp_class, "TEHDIT", "HAKARET"], f"Beklenen: {exp_class}, Gelen: {res['sinif']}"
    print("  ✅ Çocuk koruma ve zorbalık kalkanı aktif!\n")

    print("🧪 [TEST 4] AI Diplomat v2 Çok Tonlu Dönüşüm Testi:")
    angry_text = "Sen tam bir gerizekalısın projeyi batırdın boş yapma."
    for tone in ["KURUMSAL", "ARKADAS_CANLISI", "YAPICI", "SAKINLESTIRICI"]:
        dip = rewrite_with_diplomat_v2(angry_text, tone)
        print(f"  [{tone}]: {dip['diplomatik_versiyon']}")
    print("  ✅ AI Diplomat v2 tüm tonlarda başarıyla çalıştı!\n")

    print("🎉 TÜM KAMA AI 6.0 DOĞRULAMA TESTLERİ BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    run_tests()
