from fastapi import FastAPI
from pydantic import BaseModel
from mcp.interceptor import process_prompt

app = FastAPI()

class Request(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "ThreatX MCP Running 🚀"}

@app.post("/query")
def query_llm(req: Request):
    return process_prompt(req.prompt)