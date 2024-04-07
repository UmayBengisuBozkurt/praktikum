'''from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel
from models import Sensor
from read_sensors import read_sensor

app = FastAPI()

db: List[Sensor] = [
    Sensor(id=1, is_read=False),
    Sensor(id=2, is_read=False),
    Sensor(id=3, is_read=False),
    Sensor(id=4, is_read=False),
    Sensor(id=5, is_read=False)
]


# get all
@app.get("/sensor_api/sensors")
async def fetch_sensors():
    return db;


# get sensor given by id
@app.get("/sensor_api/{sensor_id}")
def read_item(sensor_id: int, sensor: Sensor):
    return {"sensor_id": sensor_id, "is_read": sensor.is_read}


# update sensor with id
# daha update yapmıyor
@app.put("/sensor_api/{sensor_id}")
def update_item(sensor_id: int, sensor: Sensor):
    return {"sensor_id": sensor_id, "is_read": sensor.is_read}
'''