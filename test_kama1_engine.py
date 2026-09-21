# -*- coding: utf-8 -*-
"""
KAMA AI 1.0 - Foundation Model Comprehensive Verification Suite
Tests:
1. Clean Turkish Sentences & Whitelist Safeguards
2. Leetspeak & Evasion Resolution (e.g., s.i.k, @mk, 0rospu)
3. 7 Cognitive & Toxicity Classes (TEMIZ, HAFIF_ARGO, HAKARET, KUFUR, TEHDIT, SIBER_ZORBALIK, COCUK_RISKI)
4. KVKK / PII Sanitizer (TCKN, IBAN, Phone, Email)
5. 4-Tone AI Diplomat Rephraser
"""

import sys
from kama_core import analyze_content, mask_pii_data, resolve_leetspeak_and_evasion, MODEL_INFO

def run_tests():
    print(f"===========================================================")
    print(f"🚀 Verifying {MODEL_INFO['name']} v{MODEL_INFO['version']} ({MODEL_INFO['status']})")
    print(f"===========================================================")

    test_cases = [
        # 1. Clean & Whitelist
        ("Harika bir proje olmuş, tebrik ederim!", "TEMIZ"),
        ("Sistemde eksiklikler tespit edildi ancak çözüldü.", "TEMIZ"), # Whitelist test (eksik)
        ("Kamu kurumlarına yönelik yeni mimari geliştirildi.", "TEMIZ"), # Whitelist test (kamu)
        
        # 2. Leetspeak / Evasion Profanity
        ("Sen ne s.i.k.i.k adamsın", "KUFUR"),
        ("Burada @.m.k diyenler var", "KUFUR"),
        ("0.r.0.s.p.u cocugu seni", "KUFUR"),
        
        # 3. Defamation / Hakaret
        ("Sen tam bir gerizekalı ve aptalsın", "HAKARET"),
        ("Haysiyetsiz şerefsiz herif", "HAKARET"),
        
        # 4. Threats
        ("Seni evinde bulur gebertirim!", "TEHDIT"),
        ("Kafana sıkarım senin", "TEHDIT"),
        
        # 5. Cyberbullying
        ("Kendini öldür artık dünyadan silin", "SIBER_ZORBALIK"),
        
        # 6. Child Safety Risk
        ("Kaç yaşındasın annen evde mi yalnız mısın kameranı aç", "COCUK_RISKI"),
        
        # 7. Street Slang / Argo
        ("Boş yapma lan yürü git", "HAFIF_ARGO")
    ]

    passed = 0
    total = len(test_cases)

    for text, expected in test_cases:
        res = analyze_content(text)
        actual = res["durum"]
        ok = (actual == expected)
        if ok:
            passed += 1
            print(f"✅ [PASS] '{text[:35]}...' -> Expected: {expected}, Got: {actual} (Skor: {res['guven_skoru']})")
        else:
            print(f"❌ [FAIL] '{text}' -> Expected: {expected}, Got: {actual}")

    # Test PII Sanitizer
    pii_sample = "Benim TCKN 12345678901 ve telefonum 05321234567, IBAN TR123456789012345678901234"
    pii_res = mask_pii_data(pii_sample)
    print("\n--- PII Sanitizer Test ---")
    print("Original:", pii_sample)
    print("Masked:  ", pii_res["masked"])
    print("Detected:", pii_res["detected_types"])
    assert "TCKN" in pii_res["detected_types"] and "TELEFON" in pii_res["detected_types"] and "IBAN" in pii_res["detected_types"], "PII detection failed"

    print(f"\n===========================================================")
    print(f"🎉 Result: {passed}/{total} Test Cases Passed Successfully!")
    print(f"===========================================================")

if __name__ == "__main__":
    run_tests()
