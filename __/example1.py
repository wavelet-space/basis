import socket

HOST = ""  # Listen on any interface
PORT = 5000  # Listen on port 8000
MAX_SIZE = 1024 * 100


def handle_request(request):
    request.decode("utf-8").split("\n")
    # print(request.decode("utf-8"))
    print(f"Received {len(request)} bytes.")
    return """HTTP/1.1 200 OK
              Content-Type: text/html

              <html><body><h1>Hello, world!</h1></body></html>
            """


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(MAX_SIZE)
            if not data:
                print(f"Client {conn} disconnected!")
                break
            response = handle_request(data)
            conn.sendall(response.encode("utf-8"))
