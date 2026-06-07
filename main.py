from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.thesis.router import router as thesis_router
from app.auth.router import router as auth_router
from app.auth.pages import router as auth_pages_router

app = FastAPI(title="EdTech ULSU")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(thesis_router)
app.include_router(auth_router)
app.include_router(auth_pages_router)

@app.get("/", response_class=HTMLResponse)
def pipeline_page(request: Request):
    return templates.TemplateResponse(request, "pipeline.html")

@app.get("/heads_of_thesis", response_class=HTMLResponse)
def supervisor_page(request: Request):
    return templates.TemplateResponse(request, "heads_of_thesis.html")
