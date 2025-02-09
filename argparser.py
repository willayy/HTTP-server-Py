import argparse

def init_argparse():
    parser = argparse.ArgumentParser(description="HTTP Server")
    parser.add_argument("--host", type=str, help="Host name", default="127.0.0.1")
    parser.add_argument("--port", type=int, help="Port number", default=6666)
    return parser
