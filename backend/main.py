from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Lista de servicios de reparaciones agrupados por disciplina
servicios = [
    {"nombre": "Cambio de lámpara", "disciplina": "Electricidad"},
    {"nombre": "Cambio de enchufe", "disciplina": "Electricidad"},
    {"nombre": "Agujeros en pared", "disciplina": "Carpintería / Pintura"},
    {"nombre": "Desatascar fregadero", "disciplina": "Fontanería"},
    {"nombre": "Cambio de grifo", "disciplina": "Fontanería"},
    {"nombre": "Instalar estantería", "disciplina": "Carpintería"},
    {"nombre": "Pintar habitación", "disciplina": "Pintura"},
    {"nombre": "Reparar persiana", "disciplina": "Carpintería / Electricidad"},
]

# Diccionario para acceso rápido por "slug"
servicios_dict = {s["nombre"].replace(" ", "_").lower(): s for s in servicios}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "servicios": servicios}
    )

@app.get("/servicio/{slug}")
async def ver_servicio(request: Request, slug: str):
    servicio = servicios_dict.get(slug)
    if not servicio:
        return {"error": "Servicio no encontrado"}
    return templates.TemplateResponse(
        "servicio.html",
        {"request": request, "servicio": servicio}
    )