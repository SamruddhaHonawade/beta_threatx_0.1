def check_rule(text: str) -> float:
    text = text.lower()

    keywords = [

        # 🔴 Prompt Injection / Override
        "ignore previous instructions",
        "disregard above instructions",
        "forget all prior rules",
        "override system",
        "bypass safety",
        "disable safety",
        "disable filters",
        "ignore guidelines",
        "jailbreak",
        "break the rules",

        # 🧠 Role Manipulation
        "act as",
        "you are now",
        "pretend to be",
        "roleplay as",
        "simulate being",
        "behave like",
        "you are no longer",

        # 🔓 System Prompt Extraction
        "reveal system prompt",
        "show hidden instructions",
        "what are your rules",
        "what is your system prompt",
        "print system config",
        "leak your instructions",
        "internal instructions",
        "developer message",

        # 💣 Data Exfiltration
        "give me password",
        "show passwords",
        "reveal secrets",
        "api key",
        "token",
        "credentials",
        "private key",
        "confidential data",

        # ⚠️ Safety Bypass Tricks
        "this is just for testing",
        "harmless request",
        "no restrictions",
        "for educational purposes only",
        "don't worry about safety",
        "safe mode off",

        # 🧩 Obfuscation / Tricks
        "byp4ss",
        "bypass",
        "evade detection",
        "encode this",
        "base64",
        "rot13",
        "obfuscate",
        "hidden message",

        # 🛠️ Instruction Injection Patterns
        "step by step ignore",
        "follow these new instructions",
        "new instructions:",
        "system override:",
        "developer mode",
        "debug mode",
        "root access",
        "admin mode",

        # 🧪 Advanced Prompt Injection Patterns
        "### system:",
        "### assistant:",
        "### user:",
        "<system>",
        "</system>",
        "[system]",
        "{system}",

    ]

    score = sum(1 for k in keywords if k in text)

    return min(score / 4, 1.0)