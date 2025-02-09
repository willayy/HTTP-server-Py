from socket import socket
from serverlog import log_info

BUFFER_SIZE = 1024
GET = "GET"

def accept_new_connections(server_socket: socket, active_sockets: list[socket]) -> None:
    '''
    Looks for an accepts a connection from a client and adds it to the list of active sockets by mutating the active_sockets list.
    '''
    sock, _ = server_socket.accept()
    active_sockets.append(sock)
    log_info(f"Connection with socket {sock} accepted and added to active sockets list")

def close_connection(sock: socket, active_sockets: list[socket]) -> None:
    '''
    Closes a connection with a client socket and removes it from the list of active sockets by mutating the active_sockets list.
    '''
    log_info(f"Connection with socket {sock} closed")
    active_sockets.remove(sock)
    sock.close()

def receive_request(sock: socket) -> str:
    '''
    Receives a request from a client socket and returns it as a string.
    '''
    data = sock.recv(BUFFER_SIZE)
    return data.decode()

def request_method(request: str) -> str:
    '''
    Returns the method of the request.
    '''
    request_lines = request.split("\r\n")
    method_line = request_lines[0]
    return method_line.split(" ")[0]

def allowed_method(method: str):
    '''
    Returns True if the request method is GET, False otherwise.
    '''
    return method == GET

def send_response(socket: socket, http_header:str, content_type: str, connection: str, body: str) -> None:
    '''
    Sends a http response to a client socket.
    '''
    response =  f"HTTP/1.1 {http_header}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += f"Connection: {connection}\r\n"
    response += f"\r\n{body}"
    socket.sendall(response.encode())
    log_info(f"Response: \n{response} \n\nsent to: {socket}")