from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Definir carpeta base y templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Montar carpeta de archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Datos de ejemplo de servicios agrupados por disciplina
servicios = [
    {"nombre": "Cambio de lámpara", "disciplina": "Electricidad", "img": "lampara.svg"},
    {"nombre": "Cambio de enchufe", "disciplina": "Electricidad", "img": "enchufe.svg"},
    {"nombre": "Agujeros en pared", "disciplina": "Pintura", "img": "pared.svg"},
    {"nombre": "Pintar habitación", "disciplina": "Pintura", "img": "pintura.svg"},
    {"nombre": "Desatascar fregadero", "disciplina": "Fontanería", "img": "fregadero.svg"},
    {"nombre": "Cambiar grifo", "disciplina": "Fontanería", "img": "grifo.svg"},
    {"nombre": "Arreglar puerta", "disciplina": "Carpintería", "img": "puerta.svg"},
    {"nombre": "Montar estantería", "disciplina": "Carpintería", "img": "estanteria.svg"},
]

@app.get("/")
async def home(request: Request):
    # Obtener disciplinas únicas para desplegable
    disciplinas = sorted(list({s["disciplina"] for s in servicios}))
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "servicios": servicios, "disciplinas": disciplinas}
    )

@app.get("/servicio/{nombre}")
async def servicio_detalle(request: Request, nombre: str):
    # Buscar servicio por nombre
    servicio = next((s for s in servicios if s["nombre"].replace(' ', '_').lower() == nombre.lower()), None)
    if servicio is None:
        return templates.TemplateResponse("404.html", {"request": request})
    return templates.TemplateResponse("servicio.html", {"request": request, "servicio": servicio})