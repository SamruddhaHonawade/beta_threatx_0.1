def check_rules(prompt: str):
    patterns = [
        "ignore previous instructions",
        "bypass security",
        "reveal system prompt",
        "act as admin",
        "ignore all rules",
        "forget previous instructions",
        "system override",
        "disable safety"
    ]

    prompt_lower = prompt.lower()

    return any(p in prompt_lower for p in patterns)