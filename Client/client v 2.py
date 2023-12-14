import socket
import json
import PySimpleGUI as sg
import time

def receive_data():
    s = socket.socket()
    host = '127.0.0.1'
    port = 5000
    s.connect((host, port))

    received_data = s.recv(1024)
    decoded_data = received_data.decode('utf-8')
    json_data = json.loads(decoded_data)

    s.close()
    
    return json_data

def main():
    layout = [
        [sg.Text("Counter: 0", key="-COUNTER-", font=('Helvetica', 14))],
        [sg.Text("Received data:", font=('Helvetica', 14))],
        [sg.Multiline("", size=(40, 10), key="-OUTPUT-", font=('Helvetica', 12))],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Data Receiver", layout, resizable=True)
    
    counter = 0  # Initialize the counter

    while True:
        event, values = window.read(timeout=100)  # Add timeout to allow checking for events

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        data = receive_data()

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
