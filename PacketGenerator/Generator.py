from random import random

from scapy.all import send
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw


def generate_packet(size):
    destination_address = "127.0.0.1"
    destination_port = 8080
    sender_port = 8081
    payload = b"A" * size

    packet = IP(dst=destination_address)/UDP(sport=sender_port, dport=destination_port)/Raw(load=payload)
    send(packet, verbose=False)
    print(f"Sent {len(payload)} bytes to {destination_address}")


if __name__ == "__main__":
    for _ in range(20):
        generate_packet(int(random() * 1000))