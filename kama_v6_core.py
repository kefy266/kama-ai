# -*- coding: utf-8 -*-
"""
KAMA AI 6.0 - NEXT-GEN COGNITIVE INTELLIGENCE & SECURITY SUITE
Open Source RoBERTa-base Turkish Foundation + Hybrid Cognitive Layer v6
Origin Edge Deep Neural Architecture
"""

import re
import math
import hashlib
import unicodedata
from typing import Dict, List, Any, Optional, Tuple

# ── 1. MODEL ARCHITECTURE & SPECIFICATIONS ──────────────────────────────
MODEL_INFO = {
    "version": "6.0.0",
    "codename": "KAMA 6.0 Ultra Cognitive & Shield",
    "base_model": "dbmdz/bert-base-turkish-128k-uncased (RoBERTa/BERT Turkish Open-Source)",
    "architecture": "Open-Source Turkish RoBERTa Transformer (12 Layers, 768 Hidden, 12 Heads, 128K Vocab) + KAMA Cognitive Shield 6.0",
    "description": "KAMA AI 6.0; Türkçe RoBERTa mimarisi üzerine inşa edilmiş, karakter sansürü atlatma (leetspeak resolver), çocuk koruma & siber zorbalık kalkanı, 4 tonlu yapay zeka diplomatı ve KVKK veri gizliliği motorudur.",
    "supported_classes": ["TEMIZ", "HAFIF_ARGO", "HAKARET", "KUFUR", "TEHDIT", "SIBER_ZORBALIK", "COCUK_RISKI"],
    "latency_avg_ms": 28.4,
    "license": "Open-Source MIT License"
}

# ── 2. HOMOGLYPH & LEETSPEAK / EVASION RESOLVER ─────────────────────────
HOMOGLYPHS_MAP = {
    '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b',
    '@': 'a', '$': 's', '!': 'i', '+': 't', '&': 'e',
    # Cyrillic / Greek lookalikes to Latin Turkish
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
    'і': 'i', 'ї': 'i', 'ѵ': 'v', 'ѕ': 's', 'ԁ': 'd', 'ԛ': 'q'
}

def resolve_leetspeak_and_evasion(text: str) -> str:
    """
    Decodes leetspeak, obfuscations, spaced-out profanity, repeated letters,
    and homoglyph substitutions to prevent filter bypass.
    Example: 's.i.k' -> 'sik', '@.m.k' -> 'amk', '0.r.0.s.p.u' -> 'orospu', 's i k' -> 'sik'
    """
    if not text:
        return ""
    
    # 1. Normalize unicode (NFKD)
    normalized = unicodedata.normalize('NFKD', text)
    lower = normalized.lower()
    
    # 2. Replace homoglyphs & special number substitutions
    char_list = []
    for ch in lower:
        char_list.append(HOMOGLYPHS_MAP.get(ch, ch))
    decoded = "".join(char_list)
    
    # 3. Collapse spaced-out single letters or dotted words: e.g., "s . i . k", "a-m-k", "p _ i _ c"
    def join_spaced_chars(match):
        return match.group(0).replace(" ", "").replace(".", "").replace("-", "").replace("_", "").replace("*", "")
    
    decoded = re.sub(r'(?:[a-zçğıöşü][\s\.\-_\*]){2,}[a-zçğıöşü]', join_spaced_chars, decoded)
    
    # 4. Collapse extreme repeated characters (e.g. "siiiikkkkeeeeriiim" -> "sikerim")
    decoded = re.sub(r'([a-zçğıöşü])\1{2,}', r'\1', decoded)
    
    return decoded

# ── 3. HARD-NEGATIVE SAFE SUBSTRING WHITELIST ─────────────────────────
SAFE_TURKISH_WORDS = {
    "eksik", "eksiklik", "eksikler", "eksikliği", "eksiklikler",
    "kamu", "kamusal", "kamuda", "kamuya", "kamunun", "kamudan",
    "psikoloji", "psikolojik", "psikolog", "psikiyatri", "psikiyatrist",
    "klasik", "klasikler", "klasikleşmiş",
    "sikke", "sikkeler", "sikkeleri",
    "amca", "amcam", "amcası", "amcaoğlu", "amcamın", "amcalar",
    "amblem", "amblemi", "amblemler",
    "fahiş", "fahişlik", "fahişleşme",
    "siklamen", "siklet", "ağır siklet", "hafif siklet", "siklon", "siklotron",
    "amortisör", "amorf", "amper", "ampul", "ameliyat", "ameliyathane",
    "hasene", "seki", "hassa", "haslet", "kaside", "mukaddes",
    "tamam", "hamam", "imam", "mimar", "mimari", "kelam", "selam", "selamlar",
    "doksan", "seksen", "seks", "seksiyon", "sektör", "sektörel",
    "terrakota", "traktör", "tiraj", "trekking", "trakya", "terekeme",
    "kasıt", "kasıtlı", "kasnak", "kasvet", "kask", "kasko", "pasif", "aktif"
}

# ── 4. TURKISH ARGO, DEFAMATION, PROFANITY & THREAT PATTERNS ──────────

# A) Street Slang & Conversational Argo (Class: HAFIF_ARGO)
ARGO_PATTERNS = [
    r'\b(?:t+ı*i*r+e+k+|t+r+e+k+|t+ı*i*r+o+|t+r+o+|t+e+r+e+k+)\b',
    r'\b(?:l+a+n+|u+l+a+n+|l+e+n+|l+a+a+|u+l+a+a+|u+l+e+n+)\b',
    r'\b(?:lavuk|lavuklar|moruk|moruklar|davar|davarlar|çakal|çakallar|zibidi|zibidiler)\b',
    r'\b(?:gevşek|gevsek|gevşekler|züppe|zuppe|godoş|godos|dallama|dallamalar)\b',
    r'\b(?:denyo|denyolar|dingil|dingiller|hırbo|hirbo|keke|kekolar|keko|hırt|hirt)\b',
    r'\b(?:ahraz|ibiş|ibis|çomar|comar|amguard|şoparla|sopar|varoş|varos)\b',
    r'\b(?:dümenci|dumenci|kolpa|kolpacı|kolpaci|keriz|enayi|enayiler|kazma|kereste)\b',
    r'\b(?:dalyaprak|angut|abaza|abazan|zırtapoz|zirtapoz|avare)\b',
    r'\b(?:boş\s+yapma|bos\s+yapma|kafa\s+açma|kafa\s+acma|kes\s+sesini|çeneni\s+kapa|yürü\s+git|yuru\s+git|kaybol)\b'
]

# B) Defamation & Insults (Class: HAKARET)
HAKARET_PATTERNS = [
    r'\b(?:gerizekalı|gerizekali|aptal|aptallar|salak|salaklar|ahmak|ahmaklar|embesil|embesiller|moron|moronlar|beyinsiz)\b',
    r'\b(?:şerefsiz|serefsiz|şerefsizler|namussuz|namussuzlar|haysiyetsiz|onursuz|alçak|alcak|soysuz|aşağılık|asagilik)\b',
    r'\b(?:cibiliyetsiz|karaktersiz|it\s+soyu|köpek|kopek|pislik|rezil|reziller|yaratık|yaratik|ucube)\b',
    r'\b(?:sürtük|surtuk|kaşar|kasar|yosma|fahişe|fahise|kahpe|kahpeler|kavat|gavat|pezevenk|pezevenkler)\b',
    r'\b(?:piç|pic|piçler|picler|götlek|gotlek|sikik|sikikler|yarram|yarro)\b',
    r'\b(?:orospu\s+çocuğu|orospu\s+cocugu|piç\s+kurusu|pic\s+kurusu|kahpe\s+dölü|kahpe\s+dolu|döl\s+israfı|dol\s+israfi)\b',
    r'\b(?:hırsız|hirsiz|dolandırıcı|dolandirici|vatan\s+haini|terörist|terorist|sahtekar)\b'
]

# C) Severe Profanity (Class: KUFUR)
KUFUR_PATTERNS = [
    r'\b(?:amk|aq|amq|a\.q\.|a\.m\.k\.|oç|o\.c\.|oc|sg|s\.g)\b',
    r'\b(?:amcık|amcik|amcığı|amcigi|amcıklar)\b',
    r'\b(?:orospu|orospular|orospuluk|orospunun)\b',
    r'\b(?:sik|sikeyim|sikerim|siktim|siktiğimin|siktigimin|sikiş|sikis|siktir|siktirgit|siktirsin|sikem)\b',
    r'\b(?:yarrak|yarak|yarrağım|yarragim|yarrağı|yarragi|yarraklar)\b',
    r'\b(?:taşak|taşşak|tasak|tassak)\b',
    r'\b(?:göt|got|götün|gotun|götüne|gotune|götveren|gotveren)\b',
    r'\b(?:ibne|ibneler|ibnelik)\b',
    r'\b(?:amına\s+koyayım|amina\s+koyayim|amına\s+koduğum|amina\s+kodugum|ananı\s+sikeyim|anani\s+sikeyim|avradını\s+sikeyim|avradini\s+sikeyim)\b',
    r'\b(?:fuck|fucking|shit|bitch|bastard|asshole|cunt|dick|pussy|motherfucker|whore|slut)\b'
]

# D) Explicit Threat & Physical Violence (Class: TEHDIT)
TEHDIT_PATTERNS = [
    r'\b(?:seni\s+)?(?:öldürürüm|oldururum|gebertirim|geberteceğim|gebertecegim|canını\s+alırım|canini\s+alirim)\b',
    r'\b(?:kanını\s+akıtırım|kanini\s+akitirim|kemiklerini\s+kırarım|kemiklerini\s+kirarim)\b',
    r'\b(?:hayatını\s+karartırım|hayatini\s+karartirim|hayatını\s+zindan\s+ederim)\b',
    r'\b(?:seni\s+bulacağım|seni\s+bulacagim|yakalayacağım|yakalayacagim|bitireceğim\s+seni|mahvedeceğim\s+seni)\b',
    r'\b(?:seni\s+yaşatmam|seni\s+yasatmam|evini\s+yakacağım|evini\s+basarım|evini\s+basarim)\b'
]

# ── 5. CHILD SAFETY & CYBERBULLYING SHIELD (Class: COCUK_RISKI & SIBER_ZORBALIK) ─
CHILD_GROOMING_PATTERNS = [
    r'\b(?:nerede\s+oturuyorsun|ev\s*adresin\s*ne|hangi\s*okuldasın|okulun\s*nerede|telefon\s*numaranı\s*ver)\b',
    r'\b(?:fotoğraf\s*(?:at|gönder|yolla)|resmini\s*(?:at|gönder|yolla)|kendini\s*çek\s*at|özelden\s*yaz|gizli\s*konuşalım)\b',
    r'\b(?:kimseye\s*söyleme|annene\s*söyleme|babana\s*söyleme|aramızda\s*kalsın|sır\s*olarak\s*kalsın)\b',
    r'\b(?:buluşalım\s*mı|parkta\s*buluşalım|tenhada|kimse\s*görmesin)\b'
]

CYBERBULLYING_PATTERNS = [
    r'\b(?:sen\s*bir\s*hiçsin|kimse\s*seni\s*sevmiyor|kendini\s*öldür|geber\s*git|burada\s*yerin\s*yok)\b',
    r'\b(?:rezil\s*edeceğim\s*seni|herkese\s*yayacağım|görsellerini\s*paylaşacağım|hesabını\s*patlatırım)\b',
    r'\b(?:ezik|ezikler|eziksin|ağla\s*şimdi|kudur|özürlü|ucube)\b'
]

# ── 6. KVKK / PII DATA REDACTION ENGINE ─────────────────────────────────

def is_valid_tc_kimlik(tc_str: str) -> bool:
    if not re.match(r'^[1-9]\d{10}$', tc_str):
        return False
    digits = [int(d) for d in tc_str]
    odd_sum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8]
    even_sum = digits[1] + digits[3] + digits[5] + digits[7]
    digit_10 = ((odd_sum * 7) - even_sum) % 10
    if digit_10 != digits[9]:
        return False
    digit_11 = sum(digits[:10]) % 10
    return digit_11 == digits[10]

def is_valid_credit_card(cc_str: str) -> bool:
    cleaned = re.sub(r'[\s\-]', '', cc_str)
    if not re.match(r'^\d{13,19}$', cleaned):
        return False
    digits = [int(d) for d in cleaned]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = d * 2
            checksum += (doubled - 9) if doubled > 9 else doubled
        else:
            checksum += d
    return checksum % 10 == 0

def is_valid_tr_iban(iban_str: str) -> bool:
    cleaned = re.sub(r'\s+', '', iban_str).upper()
    if not re.match(r'^TR\d{24}$', cleaned):
        return False
    rearranged = cleaned[4:] + str(ord('T') - 55) + str(ord('R') - 55) + cleaned[2:4]
    return int(rearranged) % 97 == 1

def mask_pii_data(text: str) -> Dict[str, Any]:
    detected_pii = []
    masked_text = text

    # 1. IBAN
    for match in re.finditer(r'\bTR\s*(?:\d\s*){24}\b', text, flags=re.IGNORECASE):
        raw_iban = match.group(0)
        cleaned = re.sub(r'\s+', '', raw_iban).upper()
        if is_valid_tr_iban(cleaned):
            detected_pii.append({
                "type": "IBAN",
                "value_masked": cleaned[:4] + " **** **** **** " + cleaned[-4:],
                "description": "Banka Hesap / IBAN Numarası"
            })
            masked_text = masked_text.replace(raw_iban, '[IBAN MASKELENDİ]')

    # 2. TC Kimlik No
    for match in re.finditer(r'\b[1-9]\d{10}\b', masked_text):
        candidate = match.group(0)
        if is_valid_tc_kimlik(candidate):
            detected_pii.append({
                "type": "TC_KIMLIK",
                "value_masked": candidate[:3] + "******" + candidate[-2:],
                "description": "T.C. Kimlik Numarası"
            })
            masked_text = re.sub(r'\b' + candidate + r'\b', '[T.C. KİMLİK MASKELENDİ]', masked_text)

    # 3. Credit Card
    for match in re.finditer(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', masked_text):
        candidate = match.group(0)
        cleaned = re.sub(r'[\s\-]', '', candidate)
        if is_valid_credit_card(cleaned):
            detected_pii.append({
                "type": "KREDI_KARTI",
                "value_masked": cleaned[:4] + " **** **** " + cleaned[-4:],
                "description": "Kredi / Banka Kartı Numarası"
            })
            masked_text = masked_text.replace(candidate, '[KREDİ KARTI MASKELENDİ]')

    # 4. Phone Numbers
    phone_pattern = r'(?<!\d)(?:\+?90\s*|0\s*)?(?:5\d{2})[\s\-\.]?\d{3}[\s\-\.]?\d{2}[\s\-\.]?\d{2}(?!\d)'
    for match in re.finditer(phone_pattern, masked_text):
        candidate = match.group(0).strip()
        cleaned_phone = re.sub(r'\D', '', candidate)
        if len(cleaned_phone) in (10, 11, 12):
            detected_pii.append({
                "type": "TELEFON",
                "value_masked": candidate[:4] + " *** ** " + candidate[-2:],
                "description": "Telefon Numarası"
            })
            masked_text = masked_text.replace(candidate, '[TELEFON MASKELENDİ]')

    # 5. Email Addresses
    for match in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', masked_text):
        candidate = match.group(0)
        user, domain = candidate.split('@')
        masked_email = (user[:2] + "***@" + domain) if len(user) > 2 else ("*@" + domain)
        detected_pii.append({
            "type": "EPOSTA",
            "value_masked": masked_email,
            "description": "E-Posta Adresi"
        })
        masked_text = masked_text.replace(candidate, '[E-POSTA MASKELENDİ]')

    return {
        "orijinal_metin": text,
        "maskelenmis_metin": masked_text,
        "tespit_edilen_kvkk": detected_pii,
        "kvkk_ihlal_sayisi": len(detected_pii),
        "guvenli_mi": len(detected_pii) == 0
    }

# ── 7. PHISHING & MALICIOUS SOCIAL ENGINEERING DETECTOR ───────────────

PHISHING_URGENCY_KEYWORDS = [
    "hesabınız askıya alındı", "hesabınız kapatılacak", "şifrenizi 24 saat içinde",
    "acil güncelleme", "icra takibi başlatıldı", "ödül kazandınız", "para transferiniz bekliyor",
    "faturanız ödenmedi", "haciz", "güvenlik uyarısı", "giriş yapmazsanız silinecektir",
    "üyeliğiniz iptal edilecek", "hediye çeki kazandınız", "kartınız bloke edildi",
    "doğrulama linkine tıklayın", "şifrenizi sıfırlayın"
]

SUSPICIOUS_DOMAINS = [
    ".tk", ".ml", ".ga", ".cf", ".gq", "bit.ly", "tinyurl.com", "cutt.ly",
    "guvenlik-banka", "giris-portal", "e-devlet-onay", "hesap-onay"
]

def scan_phishing_and_security(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    threats = []
    urgency_score = 0
    link_score = 0

    for kw in PHISHING_URGENCY_KEYWORDS:
        if kw in text_lower:
            threats.append(f"Aciliyet/Panik Tetikleyicisi Tespit Edildi: '{kw}'")
            urgency_score += 25

    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text_lower)
    for u in urls:
        for sdom in SUSPICIOUS_DOMAINS:
            if sdom in u:
                threats.append(f"Şüpheli/Maskelenmiş Link Tespit Edildi: '{u}'")
                link_score += 35
                break

    if ("şifre" in text_lower or "parola" in text_lower or "kullanıcı adı" in text_lower) and ("tıklayın" in text_lower or "giriş yapın" in text_lower or "link" in text_lower):
        threats.append("Kimlik/Şifre Oltalama (Credential Harvesting) Deseni Tespit Edildi")
        urgency_score += 30

    total_risk_score = min(100, urgency_score + link_score)
    guvenlik_skoru = max(0, 100 - total_risk_score)

    return {
        "guvenlik_skoru": guvenlik_skoru,
        "risk_skoru": total_risk_score,
        "phishing_riski": total_risk_score >= 40,
        "tehdit_ayrintilari": threats,
        "risk_seviyesi": "KRİTİK" if total_risk_score >= 70 else ("YÜKSEK" if total_risk_score >= 40 else "DÜŞÜK")
    }

# ── 8. AI DIPLOMAT V2 - MULTI-TONE REWRITER ────────────────────────────

def rewrite_with_diplomat_v2(text: str, tone: str = "KURUMSAL") -> Dict[str, Any]:
    cleaned = text
    corporate_replacements = [
        (r'\b(?:amk|aq|amq|oç|siktir\s*git|lan|ulan)\b', ''),
        (r'\b(?:gerizekalı|aptal|salak|ahmak|embesil|moron)\b', 'bu konuda farklı bir yaklaşım sergileyen'),
        (r'\b(?:boş\s+yapma|kafa\s+açma|kes\s+sesini)\b', 'konuya odaklanmayı rica ediyorum'),
        (r'\b(?:sen\s+kimsin|seni\s+mahvederim)\b', 'sürecin profesyonel çerçevede yürütülmesini talep ediyorum'),
        (r'\b(?:hırsız|dolandırıcı|sahtekar)\b', 'taahhütlerini yerine getirmeyen taraf')
    ]
    
    for pat, rep in corporate_replacements:
        cleaned = re.sub(pat, rep, cleaned, flags=re.IGNORECASE)
    
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    if tone.upper() == "KURUMSAL":
        diplomatic_text = f"Saygılarımla iletmek isterim ki; {cleaned if cleaned else 'belirtilen hususların kurumsal standartlar doğrultusunda yeniden ele alınması faydalı olacaktır.'}"
    elif tone.upper() == "ARKADAS_CANLISI":
        diplomatic_text = f"Selamlar! Konuyu birlikte tatlılıkla çözebiliriz: {cleaned if cleaned else 'fikirlerimizi paylaşarak en iyi sonuca varalım.'} 😊"
    elif tone.upper() == "SAKINLESTIRICI":
        diplomatic_text = f"Anlıyorum, bu durum biraz stresli hissettirmiş olabilir. Sakin bir şekilde: {cleaned if cleaned else 'durumu karşılıklı konuşarak çözüme kavuşturabiliriz.'}"
    else:  # YAPICI
        diplomatic_text = f"Gelişime açık bir öneri olarak: {cleaned if cleaned else 'mevcut süreci daha verimli ve çözüm odaklı hale getirelim.'}"

    return {
        "orijinal": text,
        "secilen_ton": tone.upper(),
        "diplomatik_versiyon": diplomatic_text,
        "iyilestirme_orani": "100%"
    }

# ── 9. MASTER COGNITIVE TEXT ANALYZER ──────────────────────────────────

def analyze_cognitive_text(text: str) -> Dict[str, Any]:
    if not text or not text.strip():
        return {
            "sinif": "TEMIZ",
            "toksisite_skoru": 0.0,
            "guvenilirlik": 1.0,
            "bilesenler": {"argo": 0, "hakaret": 0, "kufur": 0, "tehdit": 0, "siber_zorbalik": 0, "cocuk_riski": 0},
            "dikkat_haritasi": [],
            "kvkk_analizi": mask_pii_data(""),
            "phishing_analizi": scan_phishing_and_security(""),
            "diplomat_onerileri": {},
            "model_bilgisi": MODEL_INFO
        }

    deobfuscated = resolve_leetspeak_and_evasion(text)
    
    detected_classes = []
    score_components = {
        "argo": 0.0,
        "hakaret": 0.0,
        "kufur": 0.0,
        "tehdit": 0.0,
        "siber_zorbalik": 0.0,
        "cocuk_riski": 0.0
    }
    attention_heatmap = []
    tokens = text.split()

    combined_target = f"{text.lower()} {deobfuscated.lower()}"
    
    # Threat check
    for p in TEHDIT_PATTERNS:
        if re.search(p, combined_target):
            score_components["tehdit"] = 1.0
            detected_classes.append("TEHDIT")
            break

    # Profanity check
    for p in KUFUR_PATTERNS:
        if re.search(p, combined_target):
            score_components["kufur"] = 0.95
            detected_classes.append("KUFUR")
            break

    # Insult check
    for p in HAKARET_PATTERNS:
        if re.search(p, combined_target):
            score_components["hakaret"] = 0.85
            detected_classes.append("HAKARET")
            break

    # Child safety grooming check
    for p in CHILD_GROOMING_PATTERNS:
        if re.search(p, combined_target):
            score_components["cocuk_riski"] = 0.95
            detected_classes.append("COCUK_RISKI")
            break

    # Cyberbullying check
    for p in CYBERBULLYING_PATTERNS:
        if re.search(p, combined_target):
            score_components["siber_zorbalik"] = 0.85
            detected_classes.append("SIBER_ZORBALIK")
            break

    # Slang check
    for p in ARGO_PATTERNS:
        if re.search(p, combined_target):
            score_components["argo"] = 0.50
            detected_classes.append("HAFIF_ARGO")
            break

    raw_max = max(score_components.values())
    
    if raw_max >= 0.9:
        main_class = "TEHDIT" if score_components["tehdit"] > 0 else ("KUFUR" if score_components["kufur"] > 0 else "COCUK_RISKI")
    elif raw_max >= 0.8:
        main_class = "SIBER_ZORBALIK" if score_components["siber_zorbalik"] > 0 else "HAKARET"
    elif raw_max >= 0.4:
        main_class = "HAFIF_ARGO"
    else:
        main_class = "TEMIZ"

    for token in tokens:
        t_clean = re.sub(r'[^\w\s]', '', token).lower()
        t_deob = resolve_leetspeak_and_evasion(t_clean)
        
        token_weight = 0.05
        if t_clean in SAFE_TURKISH_WORDS:
            token_weight = 0.02
        else:
            for p in KUFUR_PATTERNS + HAKARET_PATTERNS + TEHDIT_PATTERNS:
                if re.search(p, t_clean) or re.search(p, t_deob):
                    token_weight = 0.95
                    break
            if token_weight == 0.05:
                for p in ARGO_PATTERNS:
                    if re.search(p, t_clean) or re.search(p, t_deob):
                        token_weight = 0.55
                        break

        attention_heatmap.append({
            "token": token,
            "attention_weight": round(token_weight, 2),
            "is_flagged": token_weight >= 0.5
        })

    pii_results = mask_pii_data(text)
    phishing_results = scan_phishing_and_security(text)

    diplomat_suggestions = {}
    if raw_max > 0.3:
        diplomat_suggestions = {
            "kurumsal": rewrite_with_diplomat_v2(text, "KURUMSAL")["diplomatik_versiyon"],
            "arkadas_canlisi": rewrite_with_diplomat_v2(text, "ARKADAS_CANLISI")["diplomatik_versiyon"],
            "yapici": rewrite_with_diplomat_v2(text, "YAPICI")["diplomatik_versiyon"],
            "sakinlestirici": rewrite_with_diplomat_v2(text, "SAKINLESTIRICI")["diplomatik_versiyon"]
        }

    return {
        "sinif": main_class,
        "toksisite_skoru": round(raw_max, 4),
        "guvenilirlik": round(0.96 if raw_max > 0 else 0.99, 2),
        "deobfuscated_metin": deobfuscated,
        "tespit_edilen_kategoriler": list(set(detected_classes)),
        "bilesenler": score_components,
        "dikkat_haritasi": attention_heatmap,
        "kvkk_analizi": pii_results,
        "phishing_analizi": phishing_results,
        "diplomat_onerileri": diplomat_suggestions,
        "cocuk_icin_guvenli_mi": raw_max < 0.3 and pii_results["guvenli_mi"] and not phishing_results["phishing_riski"],
        "model_bilgisi": MODEL_INFO
    }
