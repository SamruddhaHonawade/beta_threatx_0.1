import re
import base64
import urllib.parse

# Leetspeak mapping
leet_map = {
    '4': 'a', '@': 'a',
    '3': 'e',
    '1': 'i', '!': 'i',
    '0': 'o',
    '5': 's', '$': 's',
    '7': 't'
}

def normalize_text(text):
    text = text.lower()

    # Replace leetspeak
    for k, v in leet_map.items():
        text = text.replace(k, v)

    # Remove spaces + special chars
    text = re.sub(r'[^a-z]', '', text)

    return text


def detect_base64(prompt):
    try:
        decoded = base64.b64decode(prompt).decode("utf-8")
        return decoded
    except:
        return None


def detect_url_encoding(prompt):
    try:
        decoded = urllib.parse.unquote(prompt)
        return decoded
    except:
        return None


def check_semantic(prompt: str):
    keywords = [
        "override",
        "jailbreak",
        "exploit",
        "bypass",
        "ignoreinstructions",
        "revealsystemprompt",
        "actasadmin"
    ]

    # Normalize original
    normalized = normalize_text(prompt)

    # Check normal + normalized
    for word in keywords:
        if word in normalized:
            return True

    # Check Base64 attack
    decoded_b64 = detect_base64(prompt)
    if decoded_b64:
        norm_b64 = normalize_text(decoded_b64)
        for word in keywords:
            if word in norm_b64:
                return True

    # Check URL encoding
    decoded_url = detect_url_encoding(prompt)
    if decoded_url:
        norm_url = normalize_text(decoded_url)
        for word in keywords:
            if word in norm_url:
                return True

    return False
