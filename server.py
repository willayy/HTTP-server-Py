import select
from socket import socket, AF_INET, SOCK_STREAM
from argparser import init_argparse
from server_clock import ServerClock
from server_utils import (
    accept_new_connections,
    allowed_method,
    close_connection,
    receive_request,
    request_method,
    send_response,
)
from serverlog import init_logging, log_info, log_warning

# Initialize logging
init_logging()

# Initialize the argument parser
parser = init_argparse()
args = parser.parse_args()

HOST = args.host
PORT = args.port
BACKLOG = 5

# Create a socket object, AF_INET specifies that the address family is IPv4 SOCK_STREAM means that the socket is of type TCP
with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Bind the socket to our specified host and port
    server_socket.listen(
        BACKLOG
    )  # Listen for incoming connections, with a backlog of n connections
    active_sockets = [
        server_socket
    ]  # Create a list of sockets to keep track of active connections
    server_clock = ServerClock()  # Create a server clock object
    log_info("# --------------------------- NEW SESSION --------------------------- #")
    print(
        f"Server started on {HOST}:{PORT} (Ctrl+C to stop), check server.log for logs"
    )

    while True:

        read_sockets: list[socket] = select.select(active_sockets, [], [], 1)[0]

        for notified_socket in read_sockets:
            try:
                if notified_socket == server_socket:
                    accept_new_connections(
                        server_socket, active_sockets
                    )  # Accept new connections
                else:
                    # Receive data from existing connection
                    request = receive_request(notified_socket)
                    if not request:
                        close_connection(
                            notified_socket, active_sockets
                        )  # Close the connection if no data is received
                    else:
                        log_info(f"Request received: \n{request}")
                        method = request_method(request)
                        if allowed_method(method):
                            send_response(
                                notified_socket,
                                "200 OK",
                                "text/html",
                                "keep-alive",
                                server_clock.get_up_time_sec().__str__(),
                            )
                        else:
                            log_info(f"Unsupported method in request: {method}")
                            send_response(
                                notified_socket,
                                "405 Method Not Allowed",
                                "text/html",
                                "close",
                                "This server only supports GET requests",
                            )
            except (ConnectionResetError, BrokenPipeError):
                log_warning(f"Socket {notified_socket} forcefully disconnected")
                close_connection(notified_socket, active_sockets)
