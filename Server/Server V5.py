"""
Created by Hudson Brown, 100900963, December 14th, 2023
This project is heavily based on previous TPRG assignments
Use of ChatGPT to 'merge' multiple files together
(previous server file + gui file) in order to create a base to start from
"""

import socket
import os
import json
import time
import PySimpleGUI as sg
import threading

def server_thread():
    """ Allows multiple processes to occur at once """
    # initializes global variable between threads
    global sending_data
    global iteration
    global last_toggle_time
    global window

    # Server Startup
    s = socket.socket()
    host = '127.0.0.1'  # Localhost
    port = 5000
    s.bind((host, port))
    s.listen(5)

    while True:
        try:
            c, addr = s.accept()
            print('Got connection from', addr)
            window["-CONNECTION-"].update("Connection Status: ✔️")  # Update connection status
        except socket.error:
            window["-CONNECTION-"].update("Connection Status: ❌")  # Update connection status
            continue

        if sending_data:
            window["-CONNECTION-"].update("Connection Status: ✔️")  # Set check mark when sending data
            time.sleep(1)  # Display check mark for 1 second
            window["-CONNECTION-"].update("Connection Status: ❌")  # Set X mark after 1 second
            window.refresh()  # Force the window to refresh
            sending_data = False  # Reset the flag

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

        sending_data = True  # Set the flag to indicate that data is being sent

        c.close()
        time.sleep(1)  # Optional: Add a delay to avoid continuous rapid connections

def gui_thread():
    """ The thread specified to operate on the GUI """
    # initializing global variables for between the threads
    global sending_data
    global window

    # PySimpleGUI Layout
    layout = [
        [sg.Text("Connection Status: ❌", key="-CONNECTION-", font=('Helvetica', 14))],
        [sg.Text("Sent data:", font=('Helvetica', 14))],
        [sg.Multiline("", size=(40, 10), key="-OUTPUT-", font=('Helvetica', 12))],
        [sg.Button("Exit", key="-EXIT-", size=(10, 1))]
    ]

    window = sg.Window("Data Sender", layout, resizable=True)

    while True:
        event, values = window.read(timeout=100)  # Add timeout to allow checking for events

        if event == sg.WINDOW_CLOSED or event == "-EXIT-":  # Exit button will work or the X in the right corner
            break

    window.close()

# Mainguard
if __name__ == "__main__":
    sending_data = False
    iteration = 0
    last_toggle_time = 0

    server_thread = threading.Thread(target=server_thread)
    gui_thread = threading.Thread(target=gui_thread)

    server_thread.start()
    gui_thread.start()

    server_thread.join()
    gui_thread.join()
