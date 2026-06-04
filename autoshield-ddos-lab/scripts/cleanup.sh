#!/bin/bash
echo "🧹 Cleaning up..."

# Flush iptables
iptables -F
iptables -t nat -F
iptables -t mangle -F

# Reset sysctl
sysctl -w net.ipv4.tcp_syncookies=0

# Kill processes
pkill -f "vulnerable_webserver"
pkill -f "real_ddos_botnet"

echo "✅ Cleaned up!"
