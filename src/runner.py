from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.calculator import db
from src.app import CustomFastAPIApp
from src.extensions import Base, engine

Base.metadata.create_all(bind=engine)
app = CustomFastAPIApp()

BASE_PATH = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=f"{BASE_PATH}/static"), name="static")
templates = Jinja2Templates(directory=f"{BASE_PATH}/templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
