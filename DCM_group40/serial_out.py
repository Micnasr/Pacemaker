import serial
import struct


def sendSerial(data, current_mode):
    
    st = struct.Struct('<BBBBddBBddHHHBBBBBB')

    start_bit = bytes([0x16])
    fn_code = bytes([0x22])

    LRL = int(data[0])
    URL = int(data[1])
    MSR = int(data[2])
    A_Amplitude = float(data[3])
    V_Amplitude = float(data[4])
    A_Pulse_Width = int(data[5])
    V_Pulse_Width = int(data[6])
    A_Sensitivity = float(data[7])
    V_Sensitivity = float(data[8])
    VRP = int(data[9])
    ARP = int(data[10])
    PVARP = int(data[11])
    Hysteresis = int(data[12])
    Rate_Smoothing = int(data[13])

    activity_threshold_map = {
        "V-Low": 0,
        "Low": 1,
        "Med-Low": 2,
        "Med": 3,
        "Med-High": 4,
        "High": 5,
        "V-High": 6
    }
    
    Activity_Threshold = activity_threshold_map[data[14]]
    Reaction_Time = int(data[15])
    Response_Factor = int(data[16])
    Recovery_Time = int(data[17])

    port = 'COM3'

    uC = None

    try:
        # Attempt to open the serial port
        uC = serial.Serial(port, baudrate=115200)

        # Pack and send the data
        serial_com = st.pack(int(current_mode), LRL, URL, MSR, A_Amplitude, V_Amplitude, A_Pulse_Width, V_Pulse_Width, A_Sensitivity,
                             V_Sensitivity, VRP, ARP, PVARP, Hysteresis, Rate_Smoothing, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time)

        print(serial_com)
        print(len(serial_com))

        uC.write(start_bit + fn_code + serial_com)

        # Unpack the sent data (for debugging purposes)
        unpacked = st.unpack(serial_com)
        print(unpacked)

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if uC and uC.is_open:
            uC.close()