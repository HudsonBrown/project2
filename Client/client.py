import socket
import json

s = socket.socket()
host = '10.102.13.95'
port = 5000
s.connect((host, port))

received_data = s.recv(1024)
decoded_data = received_data.decode('utf-8')
json_data = json.loads(decoded_data)

print("Received data:")
for key, value in json_data.items():
    print(f"{key}: {value}")

s.close()
