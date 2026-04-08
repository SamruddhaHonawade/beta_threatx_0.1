import re
import base64
import urllib.parse

# -------------------------
# 🔤 Leetspeak mapping
# -------------------------
leet_map = {
    '4': 'a', '@': 'a',
    '3': 'e',
    '1': 'i', '!': 'i',
    '0': 'o',
    '5': 's', '$': 's',
    '7': 't'
}


# -------------------------
# 🧠 Normalize text
# -------------------------
def normalize_text(text):
    text = text.lower()

    # Replace leetspeak
    for k, v in leet_map.items():
        text = text.replace(k, v)

    # Remove non-letters
    text = re.sub(r'[^a-z]', '', text)

    return text


# -------------------------
# 🔓 Decode Base64
# -------------------------
def detect_base64(prompt):
    try:
        decoded = base64.b64decode(prompt).decode("utf-8")
        return decoded
    except:
        return None


# -------------------------
# 🌐 Decode URL Encoding
# -------------------------
def detect_url_encoding(prompt):
    try:
        return urllib.parse.unquote(prompt)
    except:
        return None


# -------------------------
# 🔥 Semantic Detection
# -------------------------
def check_semantic(prompt: str) -> float:

    # 🔴 Categorized keywords (weighted)
    keyword_weights = {

        # Prompt injection / override (HIGH RISK)
        "ignorepreviousinstructions": 1.0,
        "disregardinstructions": 1.0,
        "override": 1.0,
        "bypass": 1.0,
        "jailbreak": 1.0,
        "disablefilters": 1.0,
        "breakrules": 1.0,

        # System prompt extraction (HIGH RISK)
        "revealsystemprompt": 1.0,
        "showhiddeninstructions": 1.0,
        "systemprompt": 0.9,
        "internalinstructions": 0.9,
        "developermode": 0.9,

        # Role manipulation (MEDIUM)
        "actasadmin": 0.7,
        "actas": 0.6,
        "pretendto": 0.6,
        "simulatebeing": 0.6,
        "roleplay": 0.6,

        # Data exfiltration (HIGH)
        "apikey": 1.0,
        "token": 0.8,
        "password": 1.0,
        "secret": 1.0,
        "credentials": 1.0,
        "privatekey": 1.0,

        # Safety bypass tricks
        "unfiltered": 0.8,
        "withoutlimit": 0.8,
        "nopolicies": 0.9,
        "no restrictions": 0.9,
        "safemodeoff": 0.9,

        # DAN / jailbreak styles
        "danmode": 1.0,
        "donow": 0.8,
        "resetall": 0.7,
        "forgetprior": 0.7,
        "stayincharacter": 0.6,

        # Obfuscation / encoding tricks
        "base64": 0.6,
        "rot13": 0.6,
        "encode": 0.5,
        "obfuscate": 0.6,
        "evadedetection": 0.8,

        # Advanced injection patterns
        "systemoverride": 1.0,
        "adminmode": 1.0,
        "rootaccess": 1.0,
        "debugmode": 0.7,

        # Context tricks
        "hypotheticalscenario": 0.6,
        "startfromscratch": 0.6,
        "initialmessage": 0.6,
        "internalreasoning": 0.7,
    }

    # -------------------------
    # 🔍 Check function
    # -------------------------
    def evaluate(text):
        score = 0

        for k, weight in keyword_weights.items():
            if k in text:
                score += weight

        return min(score, 1.0)


    # -------------------------
    # 🧠 Normalize original
    # -------------------------
    normalized = normalize_text(prompt)
    score_main = evaluate(normalized)

    # -------------------------
    # 🔓 Base64 check
    # -------------------------
    decoded_b64 = detect_base64(prompt)
    score_b64 = 0
    if decoded_b64:
        norm_b64 = normalize_text(decoded_b64)
        score_b64 = evaluate(norm_b64)

    # -------------------------
    # 🌐 URL decode check
    # -------------------------
    decoded_url = detect_url_encoding(prompt)
    score_url = 0
    if decoded_url:
        norm_url = normalize_text(decoded_url)
        score_url = evaluate(norm_url)

    # -------------------------
    # 🎯 Final score (max risk)
    # -------------------------
    final_score = max(score_main, score_b64, score_url)

    return final_score