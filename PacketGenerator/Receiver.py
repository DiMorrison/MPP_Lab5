import socket
from random import random

from scapy.layers.inet import UDP, IP
from scapy.packet import Raw
from scapy.sendrecv import send


def udp_echo_server(port):
    loopback_address = '127.0.0.1'

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            server_address = (loopback_address, port)
            sock.bind(server_address)
            data, address = sock.recvfrom(4096)
            print(f"Received {len(data)} bytes from {address}")

            sock.close()

        except ConnectionResetError:
            # Handle the connection reset error
            print("Connection was forcibly closed by the remote host.")
            continue
        except Exception as e:
            # Catch all other exceptions to avoid crashing the server
            print(f"An error occurred: {e}")
            continue


if __name__ == "__main__":
    port = 8080
    udp_echo_server(port)
