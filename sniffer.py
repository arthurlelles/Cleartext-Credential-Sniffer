from scapy.all import sniff, TCP, Raw

def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        source_port = packet[TCP].sport
        dest_port = packet[TCP].dport
        payload = packet[Raw].load

        if source_port in (21, 23):
            print(f"Source port: {payload}")
        elif dest_port in (21, 23):
            print(f"Destination port: {payload}")

    else:
        return

sniff(filter="tcp port 21 or tcp port 23", prn=process_packet, store=False)