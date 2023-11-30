import serial
import time
import tkinter as tk

# Define a global variable to store the received data
received_data = ""

def monitor_serial(port, baud_rate=115200):
    global received_data
    ser = serial.Serial(port, baud_rate)
    print(f"Monitoring serial port {port} at {baud_rate} baud rate.")

    try:
        while True:  # Continue monitoring indefinitely
            if ser.in_waiting > 0:
                received_data = ser.readline().decode('utf-8').strip()
                print("SIMULINK DATA: " + received_data)
            time.sleep(0.1)  # Add a small delay to avoid busy-waiting
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()

def update_egram_label(egram_label):
    global received_data
    egram_label.config(text=f"Egram Data: {received_data}")
    # Schedule the function to run again after a delay (adjust as needed)
    egram_label.after(1000, lambda: update_egram_label(egram_label))