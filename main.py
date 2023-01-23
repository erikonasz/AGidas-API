from ascraper.ascrape import get_cars
from fastapi import FastAPI, Request
import mysql.connector
import datetime


app = FastAPI()

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    database='carslist',
    password='',
    port=4306
)   
cursor = connection.cursor()

def log_request_to_db(path, method, status):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='carslist',
        port=4306
    )
    cursor = connection.cursor()

    query = "INSERT INTO requests (path, method, status, time) VALUES (%s, %s, %s, %s)"
    time = datetime.datetime.now()
    cursor.execute(query, (path, method, status, time))
    connection.commit()
    cursor.close()
    connection.close()

def log_request_decorator(endpoint_func):
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        log_request_to_db(request.url.path, request.method, 200)
        return await endpoint_func(*args, **kwargs)
    return wrapper

def insert_data(title, price, liter, fuel_type, year, transmission, city):
    query = "INSERT INTO carslist (title, price, liter, fuel_type, year, transmission, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (title, price, liter, fuel_type, year, transmission, city))
    connection.commit()
    print("Data inserted successfully.")

@app.get("/{title}")
def get_record(title: str):
    query = f"SELECT * FROM carslist WHERE title = '{title}'"
    cursor.execute(query)
    record = cursor.fetchone()
    return {"title": title, "data": record}

@log_request_decorator
@app.get("/cars/{count}")
def get_cars_endpoint(count: int, request: Request):
    url = "https://autogidas.lt/en/skelbimai/automobiliai/?f_1%5B0%5D=BMW&f_model_14%5B0%5D=Serija+3&f_215=&f_216=&f_41=&f_42=&f_376="
    cars = get_cars(url, count)
    for car in cars:
        title = car['title']
        price = car['price']
        liter = car['liter']
        fuel_type = car['fuel_type']
        year = car['year']
        transmission = car['transmission']
        city = car['city']
        insert_data(title, price, liter, fuel_type, year, transmission, city)
    return {"cars": cars}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Get 10 most recent requests
@app.get("/recent_requests")
async def recent_requests():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='carslist',
        port=4306
    )
    cursor = connection.cursor()

    query = "SELECT endpoint_name, local_datetime FROM requests ORDER BY local_datetime DESC LIMIT 10"
    cursor.execute(query)
    records = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return {"requests": records}