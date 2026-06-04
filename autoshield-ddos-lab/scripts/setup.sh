#!/bin/bash
echo "🚀 AutoShield DDoS Lab Setup"

# Install dependencies
pip3 install -r requirements.txt

# Enable IP forwarding & SYN cookies
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv4.tcp_syncookies=1

# Create directories
mkdir -p data models logs public config scripts

# Generate training data
python3 scripts/generate_data.py

# Start services
echo "✅ Setup complete! Run: sudo python3 src/main.py"
