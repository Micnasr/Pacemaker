import threading
import serial

# Create an event to signal the thread to stop
stop_event = threading.Event()

import time
from serial.serialutil import SerialException

def monitor_serial(port, baud_rate=115200):
    global received_data

    try:
        with serial.Serial(port, baud_rate) as ser:
            print(f"Monitoring serial port {port} at {baud_rate} baud rate.")

            while True:  # Continue monitoring indefinitely

                print(ser.in_waiting)
                if ser.in_waiting > 0:
                    received_data = ser.readline().decode('utf-8').strip()
                    print("SIMULINK DATA: " + received_data)
                time.sleep(0.1)  # Add a small delay to avoid busy-waiting

    except SerialException as e:
        print(f"Error: {e}")

def stop_serial_monitor():
    global stop_event
    # Set the event to signal the thread to stop
    stop_event.set()