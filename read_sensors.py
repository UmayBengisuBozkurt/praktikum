'''import serial
import threading
import time

def read_sensor(ser, sensor_name):
    while True:
        recv = ser.read(1)
        if recv:
            print(f"{sensor_name}: {recv}")

baudrate = 9600
# Sensor 1
port1 = 'COM7'
ser1 = serial.Serial(port1, baudrate, bytesize=8, parity='N', stopbits=1, timeout=None)

# Sensor 2
port2 = 'COM10'
ser2 = serial.Serial(port2, baudrate, bytesize=8, parity='N', stopbits=1, timeout=None)

# Sensor 3
port3 = 'COM5'
ser3 = serial.Serial(port3, baudrate, bytesize=8, parity='N', stopbits=1, timeout=None)

# Sensor 4
port4 = 'COM3'
ser4 = serial.Serial(port4, baudrate, bytesize=8, parity='N', stopbits=1, timeout=None)

# Sensor 5
port5 = 'COM6'
ser5 = serial.Serial(port5, baudrate, bytesize=8, parity='N', stopbits=1, timeout=None)

# Create separate threads for each sensor
thread1 = threading.Thread(target=read_sensor, args=(ser1, "Sensor 1"))
thread2 = threading.Thread(target=read_sensor, args=(ser2, "Sensor 2"))
thread3 = threading.Thread(target=read_sensor, args=(ser3, "Sensor 3"))
thread4 = threading.Thread(target=read_sensor, args=(ser4, "Sensor 4"))
thread5 = threading.Thread(target=read_sensor, args=(ser5, "Sensor 5"))

# Start the threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Close the serial connections
ser1.close()
ser2.close()
ser3.close()
ser4.close()
ser5.close()
'''
