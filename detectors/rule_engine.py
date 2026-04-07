def check_rule(text: str) -> float:
    text = text.lower()

    keywords = [
        "ignore previous instructions",
        "override system",
        "bypass safety",
        "jailbreak",
        "act as",
        "reveal system prompt",
        "disable filters"
    ]

    score = sum(1 for k in keywords if k in text)

    return min(score / 3, 1.0)