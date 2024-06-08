import time

import scipy.stats as stats
from scapy.all import send
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw

'''
Tipovi usluga:
Agario - 0
Radio - 1
Video - 2
'''
service_types = {"Agario": 0, "Radio": 1, "Video": 2}

###################### Veličina paketa ######################
# Parametri za gamma distribuciju (alpha, scale, loc) za agario
gamma_params = (0.65, 63.03, 60.00)

# Parametri za dweibull distribuciju (c, scale, loc) za radio
dweibull_params_radio = (0.48, 150.64, 1488.00)

# Parametri za dweisbull distribuciju (c, scale, loc) za video
dweibull_params_video = (0.31, 22.37, 1434.00)

###################### Vrijeme kasnjena paketa ######################
#Parametri za vrijeme kasnjena paketa (loc, scale) za agario
norm_params_delay = (18.79, 9.70)

#Parametri za vrijeme kasnjena paketa (c,loc, scale) za radio
dweibull_params_delay_radio = (0.48, 204.81, 48.83)

#Parametri za vrijeme kasnjena paketa (loc, scale) za video
exp_params_delay_video = (0.00, 15.8)


def generate_packet(size):
    destination_address = "127.0.0.1"
    destination_port = 8080
    sender_port = 8081
    payload = b"A" * size

    packet = IP(dst=destination_address) / UDP(sport=sender_port, dport=destination_port) / Raw(load=payload)
    send(packet, verbose=False)
    #print(f"Sent {len(payload)} bytes to {destination_address} \n")


def generate_packet_with_distribution(service_type):
    packet_size = 0
    delay = [0]
    if service_type == service_types["Agario"]:
        packet_size = stats.gamma.rvs(a=gamma_params[0],
                                      scale=gamma_params[1],
                                      loc=gamma_params[2],
                                      size=1)
        delay = stats.norm.rvs(loc=norm_params_delay[0], scale=norm_params_delay[1], size=1)
    elif service_type == service_types["Radio"]:
        packet_size = stats.dweibull.rvs(dweibull_params_radio[0],
                                         scale=dweibull_params_radio[1],
                                         loc=dweibull_params_radio[2],
                                         size=1)
        delay = stats.dweibull.rvs(dweibull_params_delay_radio[0],
                                   loc=dweibull_params_delay_radio[1],
                                   scale=dweibull_params_delay_radio[2],
                                   size=1)
    elif service_type == service_types["Video"]:
        packet_size = stats.dweibull.rvs(dweibull_params_video[0],
                                         scale=dweibull_params_video[1],
                                         loc=dweibull_params_video[2],
                                         size=1)
        delay = stats.expon.rvs(loc=exp_params_delay_video[0], scale=exp_params_delay_video[1], size=1)

    #print(f"Generating packet for service type: {service_type}")
    #print(f"Sleeping for: {abs(delay[0])} ms")
    time.sleep(abs(delay[0]) / 1000)
    # Paket unutar MTU
    # generate_packet(min(int(packet_size[0]), 1472))

    # Paket preko MTU, moguće je da će biti fragmentiran
    generate_packet(min(int(packet_size[0]), 65507))


if __name__ == "__main__":
    for _ in range(5000):
        generate_packet_with_distribution(service_types["Agario"])
