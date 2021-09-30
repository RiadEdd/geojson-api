from fastapi import FastAPI, Depends
from fastapi.params import Query
from fastapi_pagination import Page, Params, paginate
from typing import TypeVar, Generic
from fastapi_pagination.default import Page as BasePage, Params as BaseParams
from pydantic import BaseModel
from typing import (Dict, List, Optional, Set, Tuple)
import json

T = TypeVar("T")

class Params(BaseParams):
    size: int = Query(5, ge=1, le=1_000, description="Page size")

class Page(BasePage[T], Generic[T]):
    __params_type__ = Params

class Country(BaseModel):
    id: str
    name: str
    geometry_type: str
    geometry: List = [] #Tuple[float, float] problem with nested models
    
    #class Config:
    #    orm_mode = True

class isoName(BaseModel):
    id: str
    name: str
    geometry_type: Optional[str]
    geometry: Optional[List] = []

with open("countries.geojson") as f:
    data = json.load(f)
    
app = FastAPI()

@app.get("/he" , response_model=Country)
def home():
    print({"id": data["features"][0]["id"], "name": data["features"][0]["properties"]["name"], "geometry_type": data["features"][0]["geometry"]["type"], "geometry": list(data["features"][0]["geometry"]["coordinates"])})
    return {"id": data["features"][0]["id"], "name": data["features"][0]["properties"]["name"], "geometry_type": data["features"][0]["geometry"]["type"], "geometry": list(data["features"][0]["geometry"]["coordinates"])}

@app.get("/iso_code", response_model=Page[isoName])
def iso_code(*, names: List = Query(...), params: Params = Depends(), details: Optional[bool] = None): #Ellipsis (...) enables to make a parameter required
    isoNameReturnList = []
    for entry in data["features"]:
        if entry["properties"]["name"] in names:
            if details:
                isoNameReturnList.append({"id": entry["id"], "name": entry["properties"]["name"], "geometry_type": entry["geometry"]["type"], "coordinates": entry["geometry"]["coordinates"]})
            else:
                isoNameReturnList.append({"id": entry["id"], "name": entry["properties"]["name"]})
    return paginate(isoNameReturnList, params)


@app.get("/all_geometries")
def all_geometries():
    return data["features"]
