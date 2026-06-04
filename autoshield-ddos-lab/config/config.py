#!/usr/bin/env python3
# AutoShield DDoS Lab Configuration
# ⚠️ AUTHORIZED PENTEST TARGET ONLY

TARGET_IP = "192.168.56.20"        # CHANGE TO YOUR TARGET VM IP
TARGET_PORT = 80
DDOS_THRESHOLD = 0.7               # ML detection confidence (0.0-1.0)
MAX_RETRAIN_INTERVAL = 30          # Auto-retrain seconds
RATE_LIMIT_SYN = "25/s"            # SYN flood protection
JS_CHALLENGE_TIMEOUT = 5           # Bot challenge seconds
ENABLE_AMPLIFICATION = True        # DNS/NTP amp attacks

print("✅ Config loaded - Authorized pentest mode")
