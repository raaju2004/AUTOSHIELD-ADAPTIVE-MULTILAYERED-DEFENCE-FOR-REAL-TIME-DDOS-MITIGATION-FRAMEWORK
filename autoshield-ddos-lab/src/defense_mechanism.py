#!/usr/bin/env python3
import socket
import threading
import time
import subprocess
import random
from collections import defaultdict
import config

class DefenseMechanism:
    def __init__(self):
        self.rate_limiters = defaultdict(list)
        self.blacklist = set()
        self.running = True
        self.dropped = 0
        
    def implement_defense_mechanism(self, target_ip, target_port):
        """🚀 ML-TRIGGERED MULTI-LAYER DEFENSE"""
        print(f"🛡️ ML ACTIVATED DEFENSE: {target_ip}:{target_port}")
        
        # Layer 1: IPTables Rate Limiting
        self.setup_iptables(target_port)
        
        # Layer 2: SYN Proxy
        threading.Thread(target=self.syn_proxy_server, 
                        args=(target_ip, target_port), daemon=True).start()
        
        # Layer 3: JS Challenge
        threading.Thread(target=self.js_challenge_server, 
                        args=(target_port), daemon=True).start()
        
        # Layer 4: IP Blacklisting
        threading.Thread(target=self.blacklist_monitor, daemon=True).start()
    
    def setup_iptables(self, port):
        """🔒 Dynamic IPTables"""
        print("🔒 IPTables Rate Limiting")
        subprocess.run(["iptables", "-F", "INPUT"], capture_output=True)
        subprocess.run([
            "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(port),
            "-m", "limit", "--limit", f"{config.MAX_SYN_RATE}/s", "-j", "ACCEPT"
        ], capture_output=True)
        subprocess.run([
            "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "DROP"
        ], capture_output=True)
        print("✅ IPTables ACTIVE")
    
    def syn_proxy_server(self, target_ip, target_port):
        proxy_port = target_port + 1000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', proxy_port))
        s.listen(200)
        print(f"🔐 SYN Proxy: {proxy_port}")
        while self.running:
            try:
                client, addr = s.accept()
                if self.is_valid_client(addr[0]):
                    self.forward_to_target(client, addr, target_ip, target_port)
                else:
                    self.dropped += 1
                    client.close()
            except: pass
    
    def js_challenge_server(self, target_port):
        challenge_port = target_port + 2000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', challenge_port))
        s.listen(100)
        print(f"🤖 JS Challenge: {challenge_port}")
        while self.running:
            client, addr = s.accept()
            challenge = f"<html><script>setTimeout(()=>{{location.href='http://localhost:{target_port}'}},500);</script></html>"
            client.send(challenge.encode())
            client.close()
    
    def blacklist_monitor(self):
        while self.running:
            for ip, timestamps in self.rate_limiters.items():
                if len(timestamps) > 50: self.blacklist.add(ip)
            time.sleep(10)
    
    def is_valid_client(self, ip):
        now = time.time()
        self.rate_limiters[ip] = [t for t in self.rate_limiters[ip] if now-t < 10]
        if len(self.rate_limiters[ip]) > 20 or ip in self.blacklist:
            return False
        self.rate_limiters[ip].append(now)
        return True
    
    def forward_to_target(self, client, client_addr, target_ip, target_port):
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            target.connect((target_ip, target_port))
            t1 = threading.Thread(target=self._forward, args=(client, target))
            t2 = threading.Thread(target=self._forward, args=(target, client))
            t1.start(); t2.start()
            t1.join(); t2.join()
        except: pass
        finally: target.close()
    
    def _forward(self, src, dst):
        while self.running:
            try:
                data = src.recv(4096)
                if not data: break
                dst.send(data)
            except: break

    def generate_js_challenge(self):
        return f"<html><script>setTimeout(() => {{location.href = 'http://localhost:{config.TARGET_PORT}'}}, 500);</script></html>"
