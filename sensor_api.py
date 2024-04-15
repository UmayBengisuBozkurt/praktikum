#! /usr/bin/python3
import time
import uvicorn
import os
import signal
import sys
from multiprocessing import Process
from fastapi import FastAPI, HTTPException
from sensor_reader import SensorReader
import asyncio
import json

app = FastAPI()
# Create instances of SensorReader for each sensor
sensors = {}
usb_names = {
    1: "USB1",
    2: "USB2"
   # 3: ('COM3', "Sensor 3"),
   # 4: ('COM7', "Sensor 4"),
   # 5: ('COM4', "Sensor 4"),
}

for sensor_id, usb_name in usb_names.items():
    sensors[sensor_id] = SensorReader(usb_name, f"Sensor {sensor_id}")
    sensors[sensor_id].start_reading()
sensor_first_detection = {sensor_id: False for sensor_id in sensors}


@app.get("/")
def read_root():
    #sensors = {1: sensor1, 2: sensor2, 3: sensor3, 4: sensor4, 5: sensor5}
    return sensors

@app.get("/sensor_api/{sensor_id}")
def read_sensor_value(sensor_id: int):
    #sensors = {1: sensor1, 2: sensor2, 3: sensor3, 4: sensor4, 5: sensor5}
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")
    if sensors[sensor_id].sensor_value is not None:
        return sensors[sensor_id].sensor_value
    return 0

async def write_to_json(sensor_data):
    with open("sensor_data.json", "a") as json_file:
        if any(value is not None for value in sensor_data.values()):
            json.dump(sensor_data, json_file)
            json_file.write("\n")

async def read_sensors_data():
    #sensors_data = {}
    while True:
        start_time = time.time()
        sensor_values = {sensor_id: sensor.sensor_value for sensor_id, sensor in sensors.items()}
        #sensor_values = {1: sensor1.sensor_value, 2: sensor2.sensor_value, 3: sensor3.sensor_value, 4: sensor4.sensor_value, 5: sensor5.sensor_value}
        # Update the sensors_data dictionary
        non_null_sensor_values = {key: value for key, value in sensor_values.items() if value is not None}
        sensors_data = non_null_sensor_values

        for sensor_id, value in sensor_values.items():
            if value is not None:
                if not sensor_first_detection[sensor_id]:
                    print(f"Object detected by Sensor {sensor_id} for the first time: {value}")
                    await write_to_json({sensor_id: value})
                    sensor_first_detection[sensor_id] = True

        # Write sensor values to JSON file asynchronously

        elapsed_time = time.time() - start_time
        # Sleep for a while before reading again
        await asyncio.sleep((max(0.0, 1 - elapsed_time)))

# Return all sensor values
@app.get("/sensors")
async def get_all_sensor_values():
    return sensors

@app.get("/check_sensors")
def check_sensors():
    sensor_status = {}
    for sensor_id, sensor in sensors.items():
        if sensor.sensor_value is not None:
            sensor_status[sensor_id] = sensor.sensor_value
        else:
            sensor_status[sensor_id] = 0
    return sensor_status
     
@app.get("/check_sensor/{sensor_id}")
def check_sensor(sensor_id: int):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor = sensors[sensor_id]
    sensor_value = sensor.sensor_value
    if sensor_value is not None:
        return sensor_value
    else:
        return 0

@app.on_event("startup")
async def startup_event():
    # Start the asynchronous sensor data reading task
    asyncio.create_task(read_sensors_data())

def run_server():
     pid = os.fork()
     if pid != 0:
         return
     print('Starting ' + str(os.getpid()))
     print(os.getpid(), file=open('sensor.pid', 'w'))
     uvicorn.run("sensor_api:app", host="::", port=9119, log_level="info")

if __name__ == "__main__":
     if os.path.exists('sensor.pid'):
       with open("sensor.pid","r") as f: pid =f.read()
       print('Killing ' + str(int(pid)))
       os.kill(int(pid),signal.SIGINT)
       os.remove('sensor.pid')
     proc = Process(target=run_server, args=(), daemon=True)
     proc.start()
     proc.join()

