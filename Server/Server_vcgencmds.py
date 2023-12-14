# Server Code
# Starter File given by Phil. Jarvis and modified by Hudson Brown
# 100900963 on November 27th 2023.
# Use of ChatGPT for furthering my understanding of
# the vcgencmd functionality, of json objects and encoding and
# decoding
# Github @
import socket
import os
import json
import time

# Server Startup
s = socket.socket()
host = '10.102.13.95'  # Localhost
port = 5000
s.bind((host, port))
s.listen(5)


while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    # Get Core Temperature from Pi (vcgencmd)
    core_temperature_raw = os.popen('vcgencmd measure_temp').readline()
    core_temperature = float(core_temperature_raw.split('=')[1].split('\'')[0])

    # Get Core Voltage from Pi (vcgencmd)
    core_voltage_raw = os.popen('vcgencmd measure_volts core').readline()
    core_voltage = float(core_voltage_raw.split('=')[1].split('V')[0])

    # Get HDMI Clock from Pi (vcgencmd)
    hdmi_clock_raw = os.popen('vcgencmd measure_clock hdmi').readline()
    hdmi_clock = int(hdmi_clock_raw.split('=')[1])
    
    # Get Core Clock from Pi (vcgencmd)
    arm_clock_raw = os.popen('vcgencmd measure_clock arm').readline()
    arm_clock = int(arm_clock_raw.split('=')[1])
    
    # Get core clock from Pi (vcgencmd)
    sdram_voltage_raw = os.popen('vcgencmd measure_volts sdram_p').readline()
    sdram_voltage = (sdram_voltage_raw.split('=')[1].split('V')[0])
    
    

    # Create dictionary for json object
    data = {
        "Core Temperature": (str(core_temperature) + " C"),
        "Core Voltage": (str(core_voltage) + " V"),
        "HDMI Clock": (str(hdmi_clock) + " Hz"),
        "Arm Clock": (str(arm_clock) + " Hz"),
        "SDRAM Voltage": (str(sdram_voltage) + " V")
    }

    # Convert data to JSON string
    json_data = json.dumps(data)

    # Send data as bytes
    res = bytes(json_data, 'utf-8')
    c.send(res)

    c.close()
    time.sleep(1)  # Optional: Add a delay to avoid continuous rapid connections