#!/usr/bin/env python3
"""
🚀 AutoShield DDoS Lab - SIMPLIFIED MAIN
"""

import sys
import os
import time
import threading
import subprocess

# Fix path issues
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# EMBEDDED CONFIG - NO EXTERNAL FILES NEEDED
TARGET_IP = "192.168.56.20"  # CHANGE THIS TO YOUR TARGET
TARGET_PORT = 80
DDOS_THRESHOLD = 0.7

print(f"🎯 TARGET: {TARGET_IP}:{TARGET_PORT}")

# Simple HTTP server for demo dashboard
import http.server
import socketserver
import json
import psutil

class DemoDashboard(http.server.SimpleHTTPRequestHandler):
    requests_count = 0
    
    def do_GET(self):
        DemoDashboard.requests_count += 1
        
        if '/status.json' in self.path:
            data = {
                'requests': DemoDashboard.requests_count,
                'cpu': psutil.cpu_percent(),
                'memory': psutil.virtual_memory().percent,
                'status': 'UNDER ATTACK' if DemoDashboard.requests_count > 100 else 'NORMAL'
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            return
        
        super().do_GET()

def start_dashboard():
    print("🌐 Dashboard: http://localhost:8080")
    with socketserver.TCPServer(("", 8080), DemoDashboard) as httpd:
        httpd.serve_forever()

# Simple attack simulation
def simulate_ddos_attack():
    print("🔥 SIMULATING DDOS ATTACK...")
    for i in range(500):
        print(f"💥 Attack packet #{i+1} - PPS: {i*10}")
        time.sleep(0.01)
    print("✅ Attack complete!")

if __name__ == "__main__":
    print("🚀 AutoShield DDoS Lab - DEMO MODE")
    
    # Start dashboard
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()
    
    time.sleep(2)
    
    # Simulate attack
    simulate_ddos_attack()
    
    print("🎯 Check dashboard: http://localhost:8080/status.json")
    input("Press Enter to exit...")
