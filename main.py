from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from shortener import shortener
from scrape import metadata_tags
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")






@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

# "https://www.epicurious.com/expert-advice/indonesian-spice-pastes-bumbu-dasar-article"

@app.get("/createlink")
def createlink(request: Request):
    """Create short link 
    """
    result = "a shortened link"
    return templates.TemplateResponse("create.html", {"request": request, "result": result, "path": request.url})

@app.post("/createlink")
def createlink(request: Request, url: str = Form(...)):
    unique_string = shortener(url)
    result = unique_string #cia vietoi "url" reikia returninti sushoritnta linka pvz: 127.0.0.1:8000/g/4kjl56j4kl6
    return templates.TemplateResponse("create.html", {"request": request, "result": 'http://127.0.0.1:8000/g/'+result, "path": request.url})

