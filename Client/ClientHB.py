"""
Created by Hudson Brown, 100900963, December 14th, 2023
This project is heavily based on previous TPRG assignments
Use of ChatGPT to 'merge' multiple files together
(previous client file + gui file) in order to create a base to start from
"""

import socket
import json
import PySimpleGUI as sg
import time

def receive_data():
    """ Receives data from decided host address and decodes it """
    s = socket.socket()
    host = '127.0.0.1'
    port = 5001
    s.connect((host, port))

    received_data = s.recv(1024)
    decoded_data = received_data.decode('utf-8')
    json_data = json.loads(decoded_data)

    s.close()
    
    return json_data

def main():
    """ Main program """
    layout = [
        [sg.Text("Connection Status: ⚪", key="-CONNECTION-", font=('Helvetica', 14))],
        [sg.Text("Received data:", font=('Helvetica', 14))],
        [sg.Multiline("", size=(40, 10), key="-OUTPUT-", font=('Helvetica', 12))],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Data Receiver", layout, resizable=True)
    
    connected = False  # Initializes the varable

    while True:
        event, values = window.read(timeout=100)  # Add timeout to allow checking for events

        if event == sg.WINDOW_CLOSED or event == "Exit":  # Allows both exit button and x button to close program
            break

        if not connected:
            data = receive_data()

            if data is not None:
                connected = True
                window["-CONNECTION-"].update("Connection Status: ⚫")

        else:
            data = receive_data()

            if data is None:
                connected = False
                window["-CONNECTION-"].update("Connection Status: ⚪")  # Shows appropriate connection status
                continue

            window["-OUTPUT-"].update(value="")  # Clear previous data

            for key, value in data.items():
                window["-OUTPUT-"].print(f"{key}: {value}", text_color='black')  # prints values received from the server

            #time.sleep(2)  # Introduce a 2-second delay

        if data.get("iteration") == 50:  # Closes program after 50 iterations
            sg.popup("Iteration reached 50. Exiting gracefully.")
            break

    window.close()
    
# mainguard
if __name__ == "__main__":
    main()
