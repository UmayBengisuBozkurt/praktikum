from fastapi import FastAPI, HTTPException
import serial
import threading

class SensorReader:
    def __init__(self, usb_name, sensor_name):
        self.ser = serial.Serial('tty/'+ usb_name, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None)
        self.thread = threading.Thread(target=self.read_sensor)
        self.sensor_value = None

    def read_sensor(self):
        while True:
            recv = self.ser.read(1)
            if recv:
                self.sensor_value = recv.decode('utf-8')
                return self.sensor_value

    def start_reading(self):
        self.thread.start()

    def stop_reading(self):
        self.ser.close()



