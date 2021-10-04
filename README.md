# geojson-api

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a simple API for informations about countries (coordinates, ISO Code, name). It is based on a geojson file (countries.geojson). I used vanilla JavaScript and CSS for a faster rendering.
	
## Technologies
Project is created with:
* Python: 3.9.7
* FastAPI: 0.68.1
	
## Setup
To run this project, install it locally and run this command :

```
$ python -m uvicorn main:app --reload
```

It'll run locally on the port 8000 (127.0.0.1:8000/).  
Make sure you have the following dependencies :

```
$ pip install fastapi
$ pip install uvicorn[standard]
$ pip install aiofile
$ pip install pydantic
$ pip install fastapi-pagination
```
