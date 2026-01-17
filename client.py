import socket
import threading

HOST = "127.0.0.1"
PORT = 8053


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


threading.Thread(target=receive_messages, args=(client,), daemon=True).start()


while True:
    msg = input()
    client.send(msg.encode())
    if msg.lower().strip() == "exit":
        break
client.close()