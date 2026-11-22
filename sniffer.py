from scapy.all import sniff, TCP, Raw
from collections import Counter
from math import log2

buffer = ""
waiting_for = ""
clean_text = ""

def calculate_entropy(password):
    count = Counter(password)
    entropy = 0
    for character, quantity in count.items():
        probability = quantity/len(password)
        entropy += probability * log2(probability)

    return -entropy

def classify_entropy(entropy):
    if entropy < 2:
        print("Weak password")
    elif entropy >= 2 and entropy <= 3.5:
        print("Medium password")
    elif entropy > 3.5:
        print("Strong password")

def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        global buffer
        global waiting_for
        global clean_text
        source_port = packet[TCP].sport
        dest_port = packet[TCP].dport
        payload = packet[Raw].load

        try:
            string_payload = payload.decode(errors="ignore")
        except UnicodeDecodeError:
            return

        if source_port in (21, 23):
            if "login" in string_payload:
                waiting_for = "user"
            elif "Password" in string_payload:
                waiting_for = "password"

        elif dest_port in (21, 23):
            if dest_port == 21:
                parts = string_payload.split()
                if parts[0] == "USER":
                    print(f"{parts[0]}: {parts[1]}")
                elif parts[0] == "PASS":
                    print(f"{parts[0]}: {parts[1][:3]}***")
                    entropy = calculate_entropy(parts[1])
                    classify_entropy(entropy)

            elif dest_port == 23:
                clean_text = ""
                for character in string_payload:
                    if character.isprintable():
                        clean_text += character

                buffer += clean_text
                if "\r" in string_payload:
                    if waiting_for == "password":
                        print(f"{waiting_for}: {buffer[:3].strip()}***")
                        entropy = calculate_entropy(buffer.strip())
                        classify_entropy(entropy)
                    else:
                        print(f"{waiting_for}: {buffer.strip()}")
                    waiting_for = ""
                    buffer = ""

    else:
        return

sniff(filter="tcp port 21 or tcp port 23", prn=process_packet, store=True)