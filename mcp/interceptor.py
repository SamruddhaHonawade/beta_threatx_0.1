from detectors.rule_engine import check_rules
from detectors.ml_engine import check_ml
from detectors.semantic_engine import check_semantic
from mcp.llm_client import call_llm
from mcp.response_filter import filter_response
from utils.logger import log_attack

def process_prompt(prompt: str):
    rule_flag = check_rules(prompt)
    ml_flag = check_ml(prompt)
    semantic_flag = check_semantic(prompt)

    risk_score = calculate_risk(rule_flag, ml_flag, semantic_flag)

    if risk_score >= 30:
        log_attack(prompt, "Prompt Injection Detected")
        return {
            "blocked": True,
            "reason": "Prompt Injection Detected",
            "risk_score": risk_score
        }

    response = call_llm(prompt)
    safe_response = filter_response(response)

    return {
        "blocked": False,
        "response": safe_response,
        "risk_score": risk_score
    }


def calculate_risk(rule, ml, semantic):
    score = 0
    if rule: score += 40
    if ml: score += 20
    if semantic: score += 40
    return score