from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
from app.thesis.router import router as thesis_router

app = FastAPI(title="EdTech ULSU")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(thesis_router)

@app.get("/", response_class=HTMLResponse)
def pipeline_page(request: Request):
    return templates.TemplateResponse(request, "pipeline.html")

