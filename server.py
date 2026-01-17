import socket
import threading

HOST = "127.0.0.1"
PORT = 8053

clients = {}
last_sender = {}
lock = threading.Lock()

def handle_client(client_socket, addr):
    username = ""
    try:

        while True:
            client_socket.send("Enter your username: ".encode())
            data = client_socket.recv(1024)
            if not data:
                return

            candidate = data.decode(errors="ignore").strip().lower()
            if not candidate:
                client_socket.send("ERROR: Username cannot be empty.\n".encode())
                continue

            with lock:
                if candidate in clients:
                    client_socket.send("ERROR: Username already taken. Try another.\n".encode())
                    continue
                clients[candidate] = client_socket

            username = candidate
            break

        print(f"[CONNECTED] {username}", flush=True)

        current_target = ""  

        while True:
            
            if current_target == "":
                client_socket.send("\n--> Enter username to chat with (or type 'exit' to quit): ".encode())

            data = client_socket.recv(1024)
            if not data:
                return

            text = data.decode(errors="ignore").strip()
            if not text:
                continue

            if text.lower() == "exit":
                return

            if text.lower() == "/change":
                current_target = ""
                client_socket.send("Switching user...\n".encode())
                continue

            words = text.split()
            tag = next((w for w in words if w.startswith("@") and len(w) > 1), None)

            if tag:
                tagged_user = tag[1:].strip().lower()  # מאחדים ל-lowercase
                body = " ".join(w for w in words if w != tag).strip()

                with lock:
                    tagged_sock = clients.get(tagged_user)

                if tagged_sock and tagged_user != username:
                    if body == "":
                        body = "(empty)"
                    tagged_sock.send(f"\n[{username}]: {body}\n".encode())
                    with lock:
                        last_sender[tagged_user] = username
                    current_target = tagged_user  # ממשיכים לדבר איתו
                    continue
                else:
                    client_socket.send("ERROR: Tagged user not found.\n".encode())
                    continue

            candidate_target = text.strip().lower()

            with lock:
                is_username = (candidate_target in clients and candidate_target != username)
                auto = last_sender.get(username)
                auto_ok = (auto in clients) if auto else False

            if is_username:
                current_target = candidate_target
                client_socket.send(
                    f"--- Chat started with {current_target}. Type '/change' to switch user ---\n"
                    f"Tip: send to a specific user using @username (example: hi @may)\n".encode()
                )
                continue

            target_to_send = current_target or (auto if auto_ok else "")
            if not target_to_send:
                client_socket.send("System: No target. Type a username to start chatting.\n".encode())
                continue

            with lock:
                target_sock = clients.get(target_to_send)

            if not target_sock:
                client_socket.send(f"System: {target_to_send} has disconnected. Type '/change'.\n".encode())
                if current_target == target_to_send:
                    current_target = ""
                continue

            try:
                target_sock.send(f"\n[{username}]: {text}\n".encode())
                with lock:
                    last_sender[target_to_send] = username
               
                if current_target == "":
                    current_target = target_to_send
            except:
                client_socket.send(f"System: {target_to_send} has disconnected. Type '/change'.\n".encode())
                if current_target == target_to_send:
                    current_target = ""

    except Exception as e:
        print(f"[ERROR] {e}", flush=True)
    finally:
        if username:
            with lock:
                if clients.get(username) == client_socket:
                    del clients[username]
                last_sender.pop(username, None)

        try:
            client_socket.close()
        except:
            pass

        print(f"[DISCONNECTED] {username}", flush=True)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"SERVER LISTENING on port {PORT}...", flush=True)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()