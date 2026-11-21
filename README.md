# Cleartext Credential Sniffer

A network sniffer built with [Scapy](https://scapy.net/) to capture and inspect cleartext traffic from insecure protocols (FTP, Telnet) as part of a Computer Networks coursework assignment. Built as a hands-on exercise to understand why cleartext authentication protocols are a security risk.

## Why this project

FTP and Telnet send credentials in plain text over the network. This tool demonstrates that risk by capturing and displaying the raw traffic on ports 21 (FTP) and 23 (Telnet) in a controlled lab environment.

## Status

**Work in progress.** Current version extracts and labels FTP and Telnet credentials from captured traffic. Telnet username output may still contain terminal negotiation noise (see roadmap). Password obfuscation and entropy scoring are planned next steps.

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

## Lab setup

Tested against [Metasploitable2](https://sourceforge.net/projects/metasploitable/) on an isolated host-only VirtualBox network, with a Kali Linux VM as the attacker/capture machine.

**⚠️ For educational use in controlled/isolated lab environments only.** Do not run against networks or systems you do not own or have explicit permission to test.

## Roadmap

- [x] Basic packet capture on ports 21/23
- [x] Extract FTP username/password from `USER`/`PASS` commands
- [x] Reassemble and parse Telnet character-by-character stream
- [ ] Obfuscate captured passwords in terminal output
- [ ] Calculate and classify password entropy

## Disclaimer

This project was developed for a university Computer Networks course assignment, for educational purposes only.