from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import datetime

# MCP logic
from mcp.interceptor import process_prompt

app = FastAPI(title="ThreatX MCP Dashboard", version="2.0")

# ✅ Mount static files (IMPORTANT)
app.mount("/static", StaticFiles(directory="static"), name="static")

LOG_FILE = "logs/attacks.json"


# -------------------------
# Request Model
# -------------------------
class RequestModel(BaseModel):
    prompt: str


# -------------------------
# Load Logs
# -------------------------
def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# -------------------------
# Save Logs
# -------------------------
def save_log(entry):
    logs = load_logs()
    logs.insert(0, entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs[:100], f, indent=4)


# -------------------------
# Home Route
# -------------------------
@app.get("/")
def home():
    return {"message": "ThreatX Running 🚀"}


# -------------------------
# ✅ FIXED UI ROUTE (NO JINJA BUG)
# -------------------------
@app.get("/ui", response_class=HTMLResponse)
def ui():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# -------------------------
# 🔥 Analyze Prompt API
# -------------------------
@app.post("/api/analyze")
def analyze(req: RequestModel):
    result = process_prompt(req.prompt)

    log_entry = {
        "time": str(datetime.datetime.now()),
        "prompt": req.prompt,
        "blocked": result.get("blocked", False),
        "risk_score": result.get("risk_score", 0),
        "reason": result.get("reason", "Allowed")
    }

    save_log(log_entry)

    return JSONResponse(content=result)


# -------------------------
# 📊 Fetch Logs API
# -------------------------
@app.get("/api/logs")
def get_logs():
    return JSONResponse(content=load_logs())