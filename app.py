"""IDAI-Detect web app — FastAPI + Jinja2 + vanilla JS.

Jalanin:  python3 app.py
Buka:     http://localhost:8000
"""

from pathlib import Path

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from engine.rule_engine import analyze, paragraphs_with_flags, read_text

app = FastAPI(title="IDAI-Detect")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

ALLOWED = {".txt", ".docx", ".pdf"}


class AnalyzeIn(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


def _result(text: str):
    if not text.strip():
        return JSONResponse({"error": "tidak ada teks yang bisa dibaca dari file"}, status_code=400)
    result = analyze(text)
    result["paragraphs"] = paragraphs_with_flags(text)
    return result


@app.post("/api/analyze")
def api_analyze(body: AnalyzeIn):
    return _result(body.text)


@app.post("/api/upload")
async def api_upload(file: UploadFile):
    if Path(file.filename or "").suffix.lower() not in ALLOWED:
        return JSONResponse({"error": "format harus .txt / .docx / .pdf"}, status_code=400)
    data = await file.read()
    tmp = Path("/tmp/opencode") / file.filename
    tmp.write_bytes(data)
    try:
        return _result(read_text(tmp))
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)