from fastapi import FastAPI, Depends
from fastapi.params import Query
from fastapi_pagination import Page, Params, paginate
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import TypeVar, Generic
from fastapi_pagination.default import Page as BasePage, Params as BaseParams
from pydantic import BaseModel
from typing import (Dict, List, Optional, Set, Tuple)
from enum import Enum
import json

from starlette.requests import Request

templates = Jinja2Templates(directory="templates")

T = TypeVar("T")

class Params(BaseParams):
    size: int = Query(5, ge=1, le=1_000, description="Page size")

class Page(BasePage[T], Generic[T]):
    __params_type__ = Params

class geometryTypeEnum(str, Enum):
    polygon='Polygon'
    multiPolygon='MultiPolygon'

class Country(BaseModel):
    id: str
    name: str
    geometry_type: geometryTypeEnum
    geometry: List = [] #Tuple[float, float] problem with nested models
    
    class Config:
        orm_mode = True
        use_enum_values = True

class isoName(BaseModel):
    id: str
    name: str
    geometry_type: Optional[str]
    geometry: Optional[List] = []

with open("countries.geojson") as f:
    data = json.load(f)

app = FastAPI()
app.mount("/statics", StaticFiles(directory="statics"), name="statics")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/devblog", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("devblog.html", {"request": request})

@app.get("/iso_code", response_model=Page[isoName])
def iso_code(*, names: List = Query(...), params: Params = Depends(), details: Optional[bool] = None): #Ellipsis (...) enables to make a parameter required
    isoNameReturnList = []
    for entry in data["features"]:
        if entry["properties"]["name"] in names:
            if details:
                isoNameReturnList.append({"id": entry["id"], "name": entry["properties"]["name"], "geometry_type": entry["geometry"]["type"], "geometry": entry["geometry"]["coordinates"][0]})
            else:
                isoNameReturnList.append({"id": entry["id"], "name": entry["properties"]["name"]})
    return paginate(isoNameReturnList, params)

# Get all the informations in the API
@app.get("/all_geometries")
def all_geometries():
    return data["features"]

# Get all the informations in the API in a Custom Response (HTML)
@app.get("/all_countries", response_class=HTMLResponse) #delete this endpoint when it's OK for /all_geometries
def all_countries(request: Request):
    return templates.TemplateResponse("all_geometries.html", {"request": request, "data": data["features"]})

@app.post("/add_country")
def add_country(country: Country):
    countryDict = {"type": "Feature", "id": country.id, "properties": {"name": country.name}, "geometry": {"type": country.geometry_type, "coordinates": [country.geometry]}}
    newData = data
    newData["features"].append(countryDict)
    with open('data.geojson', 'w') as outfile:
        json.dump(newData, outfile)
    return countryDict