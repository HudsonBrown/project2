import socket
import os
import json
import time
import PySimpleGUI as sg

def run_server():
    # Server Startup
    s = socket.socket()
    host = '127.0.0.1'  # Localhost
    port = 5001
    s.bind((host, port))
    s.listen(5)

    iteration = 0  # Initialize the iteration counter

    # PySimpleGUI Layout
    layout = [
        [sg.Text("Server Data Display", font=('Helvetica', 16))],
        [sg.Multiline("", size=(40, 10), key="-OUTPUT-", font=('Helvetica', 12))],
    ]

    window = sg.Window("Server", layout, resizable=True)

    while True:
        event, values = window.read(timeout=100)  # Add timeout to allow checking for events

        if event == sg.WINDOW_CLOSED:
            break

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

        # Get SDRAM Voltage from Pi (vcgencmd)
        sdram_voltage_raw = os.popen('vcgencmd measure_volts sdram_p').readline()
        sdram_voltage = sdram_voltage_raw.split('=')[1].split('V')[0]

        # Increment the iteration counter
        iteration += 1

        # Display data in PySimpleGUI window
        display_data = f"Iteration: {iteration}\n" \
                       f"Core Temperature: {core_temperature} C\n" \
                       f"Core Voltage: {core_voltage} V\n" \
                       f"HDMI Clock: {hdmi_clock} Hz\n" \
                       f"Arm Clock: {arm_clock} Hz\n" \
                       f"SDRAM Voltage: {sdram_voltage} V\n"

        window["-OUTPUT-"].update(value=display_data)

        # Create dictionary for json object
        data = {
            "iteration": iteration,
            "Core Temperature": f"{core_temperature} C",
            "Core Voltage": f"{core_voltage} V",
            "HDMI Clock": f"{hdmi_clock} Hz",
            "Arm Clock": f"{arm_clock} Hz",
            "SDRAM Voltage": f"{sdram_voltage} V"
        }

        # Convert data to JSON string
        json_data = json.dumps(data)

        # Send data as bytes
        res = bytes(json_data, 'utf-8')
        c.send(res)

        c.close()
        time.sleep(1)  # Optional: Add a delay to avoid continuous rapid connections

    window.close()

if __name__ == "__main__":
    run_server()
