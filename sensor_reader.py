from fastapi import FastAPI, HTTPException
import serial
import threading

class SensorReader:
    def __init__(self, usb_name, sensor_name):
        self.usb_name = usb_name
        self.sensor_name = sensor_name
        self.thread = None
        self.sensor_value = None

    def read_sensor(self):
        try:
            with serial.Serial(f'/dev/tty{self.usb_name}', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None) as ser:
                while True:
                    recv = ser.read(1)
                    if recv:
                        self.sensor_value = recv.decode('utf-8')
                        print(f"{self.sensor_name}: {self.sensor_value}")
        except serial.SerialException as e:
            print(f"Serial communication error for sensor {self.sensor_name}: {e}")

    def start_reading(self):
        self.thread = threading.Thread(target=self.read_sensor)
        self.thread.start()

    def stop_reading(self):
        if self.thread:
            self.thread.join()
            self.thread = None




