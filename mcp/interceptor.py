from detectors.rule_engine import check_rule
from detectors.ml_engine import check_ml
from detectors.semantic_engine import check_semantic
from mcp.llm_client import call_llm
from mcp.response_filter import filter_response
from utils.logger import log_attack


def process_prompt(prompt: str):
    text = prompt.lower()

    # -------------------------
    # Detection scores (0–1)
    # -------------------------
    r = check_rule(prompt)
    s = check_semantic(prompt)
    m = check_ml(prompt)

    print(f"DEBUG → R:{r}, S:{s}, M:{m}")  # 👈 helps you debug

    # -------------------------
    # ✅ SAFE OVERRIDE (IMPORTANT)
    # -------------------------
    if r == 0 and s == 0 and m < 0.7:
        response = call_llm(prompt)
        safe_response = filter_response(response)

        return {
            "blocked": False,
            "response": safe_response,
            "risk_score": 0
        }

    # -------------------------
    # 🔐 STRONG ML BLOCK
    # -------------------------
    if m > 0.8:
        log_attack(prompt, f"ML Block (score={m})")
        return {
            "blocked": True,
            "reason": "ML detection",
            "risk_score": int(m * 100)
        }

    # -------------------------
    # 🔐 HYBRID LOGIC
    # -------------------------
    risk_score = calculate_risk(r, s, m)

    if risk_score >= 60:
        log_attack(prompt, f"Hybrid Block (R:{r}, S:{s}, M:{m})")
        return {
            "blocked": True,
            "reason": "Hybrid detection",
            "risk_score": risk_score
        }

    # -------------------------
    # ✅ SAFE → LLM CALL
    # -------------------------
    response = call_llm(prompt)
    safe_response = filter_response(response)

    return {
        "blocked": False,
        "response": safe_response,
        "risk_score": risk_score
    }


# -------------------------
# 🔢 SMART RISK FUNCTION
# -------------------------
def calculate_risk(r, s, m):
    score = 0

    # Rule (strong)
    if r > 0.5:
        score += 40

    # Semantic
    if s > 0.5:
        score += 30

    # ML scaled
    score += int(m * 30)   # max 30

    return score