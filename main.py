from ascraper.ascrape import get_cars, write_to_csv
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

@app.get("/cars/{count}")
def get_cars_endpoint(count: int):
    url = "https://autogidas.lt/en/skelbimai/automobiliai/?f_1%5B0%5D=Porsche&f_model_14%5B0%5D=&f_215=&f_216=&f_41=&f_42=&f_376="
    cars = get_cars(url, count)
    write_to_csv(cars)
    return JSONResponse(content={"cars": cars})