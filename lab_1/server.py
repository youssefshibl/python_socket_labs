import time
import socket
import threading


# all parameters
port = 9001
data_formate = "utf-8"
header_length = 64
server_ip = socket.gethostbyname(socket.gethostname())
close_server_key = "DDD"

# make socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, port))


def start():
    clients = []
    server.listen()
    print(f"Server is listening to {server_ip}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread_connection = threading.Thread(
            target=client, args=(conn, addr, clients))
        thread_connection.start()


def client(conn, addr, clients):
    print(f"{addr} is Connected successfuly")
    connaction_status = True
    while connaction_status:
        message_len = conn.recv(header_length).decode(data_formate)
        if message_len:
            message_len = int(message_len)
            message_text = conn.recv(message_len).decode(data_formate)
            if message_text == close_server_key:
                connaction_status = False
                print(f"{addr} connection is closed")
            else:
                print(f"{addr} send:{message_text}")
                handel(conn,addr,clients,message_len,message_text)

    conn.close()

def send(message,client):
    message = message.encode(data_formate)
    message_len = len(message)
    header_message = str(message_len).encode(data_formate)
    header_message += b' '*(header_length-len(header_message))
    client.send(header_message)
    client.send(message)


def handel(conn,addr,clients,message_len,message_text):
    #handel function
    send(message_text,conn)
    #print("")

start()
