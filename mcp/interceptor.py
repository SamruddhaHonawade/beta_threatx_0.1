from detectors.rule_engine import check_rule
from detectors.ml_engine import check_ml
from detectors.semantic_engine import check_semantic
from mcp.llm_client import call_llm
from mcp.response_filter import filter_response
from utils.logger import log_attack


def process_prompt(prompt: str):

    r = check_rule(prompt)
    s = check_semantic(prompt)
    m = check_ml(prompt)

    print(f"DEBUG → R:{r}, S:{s}, M:{m}")

    # ✅ Safe case
    if r < 0.1 and s < 0.1 and m < 0.5:
        response = call_llm(prompt)
        safe_response = filter_response(response)

        return {
            "blocked": False,
            "response": safe_response,
            "risk_score": 0,
            "rule_score": r,
            "semantic_score": s,
            "ml_score": m
        }

    # 🔐 Strong ML block
    if m > 0.8:
        log_attack(prompt, f"ML Block (score={m})")
        return {
            "blocked": True,
            "reason": "ML detection",
            "risk_score": int(m * 100),
            "rule_score": r,
            "semantic_score": s,
            "ml_score": m
        }

    # 🔐 Hybrid logic
    risk_score = calculate_risk(r, s, m)

    if risk_score >= 60:
        log_attack(prompt, f"Hybrid Block (R:{r}, S:{s}, M:{m})")
        return {
            "blocked": True,
            "reason": "Hybrid detection",
            "risk_score": risk_score,
            "rule_score": r,
            "semantic_score": s,
            "ml_score": m
        }

    # ✅ Safe → LLM
    response = call_llm(prompt)
    safe_response = filter_response(response)

    return {
        "blocked": False,
        "response": safe_response,
        "risk_score": risk_score,
        "rule_score": r,
        "semantic_score": s,
        "ml_score": m
    }


def calculate_risk(r, s, m):
    score = 0

    if r > 0.5:
        score += 40

    if s > 0.5:
        score += 30

    score += int(m * 30)

    return score