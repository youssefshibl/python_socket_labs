import time
import socket
import threading


# all parameters
port = 9001
data_formate = "utf-8"
header_length = 64
server_ip = socket.gethostbyname(socket.gethostname())
close_server_key = "DDD"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))


def send(message):
    message = message.encode(data_formate)
    message_len = len(message)
    header_message = str(message_len).encode(data_formate)
    header_message += b' '*(header_length-len(header_message))
    client.send(header_message)
    client.send(message)


def read():
    message_len = client.recv(header_length).decode(data_formate)
    if message_len:
        message_len = int(message_len)
        message_text = client.recv(message_len).decode(data_formate)
        print(f"server {server_ip} send:{message_text}")
        



while True:
    input_message = input("send message to server :")
    if input_message == close_server_key:
        send(close_server_key)
        break
    send(input_message)
    #threading.Thread(target=read).start()
    read()
