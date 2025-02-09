import logging
import os
import select
import socket
import argparse
import datetime

# Create a folder called logs if it doesn't exist
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Get the current date
start_time = datetime.datetime.now()
log_date = start_time.strftime("%Y-%m-%d")

# Create a logger for the day
logging.basicConfig(
    filename=f"logs/{log_date}_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Get host and port from the supplied arguments
parser = argparse.ArgumentParser(description="HTTP Server")

parser.add_argument("--host", type=str, help="Host name", default="127.0.0.1")
parser.add_argument("--port", type=int, help="Port number", default=6666)
args = parser.parse_args()

HOST = args.host
PORT = args.port
BUFFER_SIZE = 1024
GET = "GET"

# Create a socket object, AF_INET specifies that the address family is IPv4
# SOCK_STREAM means that the socket is of type TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to our specified host and port
    s.bind((HOST, PORT))
    # Listen for incoming connections, the argument specifies the maximum number of queued connections
    s.listen(5)

    logging.info("# --------------- NEW SESSION --------------- #")
    start_message = f"Server started on {HOST}:{PORT}"
    print(start_message + " (Ctrl+C to stop), check server.log for logs")
    logging.info(start_message)

    # List of sockets for select.select()
    socks = [s]
    # Dictionary to store address of clients
    clients = {}

    while True:
        read_socks: list[socket.socket]
        read_socks, _, _ = select.select(socks, [], [])

        # every 5 minutes, log the number of active connections
        current_time = datetime.datetime.now()
        if (current_time - start_time).seconds % 300 == 0:
            logging.info(f"Active sockets: {socks}")
            logging.info(f"Active clients: {clients}")

        for notified_socket in read_socks:
            if notified_socket == s:
                # Accept new connection
                sock, addr = s.accept()
                socks.append(sock)
                clients[sock] = addr
                logging.info(f"Connection with socket {sock}")
            else:
                # Receive data from existing connection
                data = notified_socket.recv(BUFFER_SIZE)
                if not data:
                    # If no data is received, the connection is closed
                    logging.info(f"Connection closed from {clients[notified_socket]}")
                    socks.remove(notified_socket)
                    del clients[notified_socket]
                    notified_socket.close()
                else:
                    request = data.decode()
                    logging.info(f"Request received: \n{request}")
                    request_lines = request.split("\r\n")
                    method, path, protocol = request_lines[0].split(" ")
                    response = ""

                    if method != GET:
                        logging.info(f"Unsupported method: {method}")
                        response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\nContent-Length: 25\r\nConnection: Closed\r\n\r\nOnly GET method is allowed on this server"

                    else:
                        # Create a response
                        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 21\r\nConnection: Closed\r\n\r\nHello im a server! :)"

                    notified_socket.sendall(response.encode())
                    logging.info(
                        f"Response \n{response} \n\nsent to: {notified_socket}"
                    )
