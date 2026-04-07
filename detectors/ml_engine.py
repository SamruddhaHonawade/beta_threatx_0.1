def check_ml(prompt: str):
    score = 0

    # Long suspicious prompts
    if len(prompt) > 300:
        score += 1

    # Too many special characters
    special_chars = sum(not c.isalnum() for c in prompt)
    if special_chars > 20:
        score += 1

    # Repeated patterns (possible attack)
    if prompt.count("ignore") > 2:
        score += 1

    return score >= 2
