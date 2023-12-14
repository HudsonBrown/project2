import socket
import json
import PySimpleGUI as sg
import time

def is_connected():
    s = socket.socket()
    host = '127.0.0.1'
    port = 5000

    try:
        s.connect((host, port))
        connected = True
    except Exception as e:
        print(f"Connection failed: {e}")
        connected = False

    s.close()
    return connected

def receive_data():
    s = socket.socket()
    host = '127.0.0.1'
    port = 5000

    try:
        s.connect((host, port))
        connected = True
    except Exception as e:
        print(f"Connection failed: {e}")
        connected = False

    if not connected:
        return None

    received_data = s.recv(1024)
    decoded_data = received_data.decode('utf-8')
    json_data = json.loads(decoded_data)

    s.close()

    return json_data

def main():
    layout = [
        [sg.Text("Connection Status: ❌", key="-CONNECTION-", font=('Helvetica', 14))],
        [sg.Text("Counter: 0", key="-COUNTER-", font=('Helvetica', 14))],
        [sg.Text("Received data:", font=('Helvetica', 14))],
        [sg.Multiline("", size=(40, 10), key="-OUTPUT-", font=('Helvetica', 12))],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Data Receiver", layout, resizable=True)
    
    counter = 0  # Initialize the counter
    connected = False

    while True:
        event, values = window.read(timeout=100)  # Add timeout to allow checking for events

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        if not connected:
            connected = is_connected()

            if connected:
                window["-CONNECTION-"].update("Connection Status: ✔️")

        else:
            data = receive_data()

            if data is None:
                connected = False
                window["-CONNECTION-"].update("Connection Status: ❌")
                continue

            window["-OUTPUT-"].update(value="")  # Clear previous data

            for key, value in data.items():
                window["-OUTPUT-"].print(f"{key}: {value}", text_color='white')

            counter += 1
            window["-COUNTER-"].update(f"Counter: {counter}")

            time.sleep(2)  # Introduce a 2-second delay

        if counter >= 50:
            sg.popup("Counter reached 50. Exiting gracefully.")
            break

    window.close()

if __name__ == "__main__":
    main()
