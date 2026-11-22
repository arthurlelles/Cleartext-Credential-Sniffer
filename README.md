# Cleartext Credential Sniffer

> 🇧🇷 [Leia em português](README.pt-BR.md)

A network sniffer built with [Scapy](https://scapy.net/) to capture and inspect cleartext traffic from insecure protocols (FTP, Telnet) as part of a Computer Networks coursework assignment. Built as a hands-on exercise to understand why cleartext authentication protocols are a security risk.

## Why this project

FTP and Telnet send credentials in plain text over the network. This tool demonstrates that risk by capturing traffic on ports 21 (FTP) and 23 (Telnet), extracting usernames and passwords, obfuscating captured passwords on screen, and scoring their strength using Shannon entropy.

## Status

**Functional.** Captures and parses FTP (`USER`/`PASS` commands) and Telnet (character-by-character session reconstruction) credentials. Passwords are obfuscated in terminal output and scored for strength.

## Requirements

- Python 3
- Root privileges (raw packet capture requires elevated permissions)
- See `requirements.txt` for Python dependencies

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
sudo python3 sniffer.py
```

Run this on a machine positioned to observe FTP/Telnet traffic (e.g., same host-only network as the target). Generate traffic by connecting to an FTP or Telnet server while the sniffer is running:

```bash
ftp <target-ip>
telnet <target-ip>
```

## How it works

- **FTP**: parses `USER`/`PASS` commands sent as plain-text lines by the client.
- **Telnet**: Telnet sends data one character at a time, so characters are buffered until a carriage return (`\r`) is detected, reconstructing full lines. The server's `login:`/`Password:` prompts are used to track which credential (username or password) is expected next.
- **Password obfuscation**: only the first 3 characters of a captured password are shown; the rest is masked with `***`.
- **Entropy scoring**: password strength is estimated using Shannon entropy (character frequency distribution). Classification thresholds (`< 2` weak, `2–3.5` medium, `> 3.5` strong) were defined empirically for this exercise and are not an official standard.

## Lab setup

Tested against [Metasploitable2](https://sourceforge.net/projects/metasploitable/) on an isolated host-only VirtualBox network, with a Kali Linux VM as the attacker/capture machine.

**⚠️ For educational use in controlled/isolated lab environments only.** Do not run against networks or systems you do not own or have explicit permission to test.

## Known limitations

- **Telnet negotiation noise**: Telnet's protocol negotiation (terminal type, display settings, etc.) is marked by a control byte (IAC, `0xFF`) that can carry literal, human-readable text (e.g., `XTERM-256COLOR`, `DISPLAY`) as part of its payload. Because this text is technically printable, it is not filtered out by the current printable-character check and may appear mixed into the captured username line. A proper fix would require detecting and stripping IAC-prefixed negotiation sequences from the raw payload before reconstructing lines — this was identified but not implemented due to time constraints.

## Roadmap

- [x] Basic packet capture on ports 21/23
- [x] Extract FTP username/password from `USER`/`PASS` commands
- [x] Reassemble and parse Telnet character-by-character stream
- [x] Obfuscate captured passwords in terminal output
- [x] Calculate and classify password entropy
- [ ] Strip Telnet IAC negotiation sequences from captured text (see Known limitations)

## Disclaimer

This project was developed for a university Computer Networks course assignment, for educational purposes only.