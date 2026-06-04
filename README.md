# AUTOSHIELD-ADAPTIVE-MULTILAYERED-DEFENCE-FOR-REAL-TIME-DDOS-MITIGATION-FRAMEWORK
## Key Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| ML Engine | Accuracy | 94.7% |
| ML Engine | F1-Score | 0.947 |
| Mitigation | Block Rate | 99.2% |
| Dashboard | Refresh Rate | 1 second |
| Latency | E2E Response | 7.2ms |
| Attack | Throughput | 100K+ PPS |

## Features

### ML Forensics Engine
- Custom NumPy Isolation Forest (zero sklearn dependency)
- 5D feature extraction: cpu_percent, memory_percent, top20_pids_count, conn_count, anomaly_score
- Real-time anomaly scoring with 94.7% accuracy matching sklearn baseline
- Silent error handling and memory leak fixes applied

### ULTRA+ v3.1 Attack Simulator
- Multi-vector DDoS: SYN flood, UDP amplification, ICMP flood etc.
- 10K to 100K+ PPS ramp-up in 5 seconds
- Configurable target, port, rate, and duration

### Live Dashboard
- Real-time 1s AJAX refresh . 
- Whitelist fix: ports 5000/5001 survive during attack
- Self-block resolved with localhost ACCEPT first

### iptables Mitigation
- ML-triggered dynamic SYN proxy rules
- Dashboard whitelist integration
- 99.2% block rate at 7.2ms latency

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/autoshield-ddos-lab.git
cd autoshield-ddos-lab

# Deploy (one command)
sudo ./deploy.sh

# Or run manually
sudo python3 src/autoshield_enterprise.py -> machine learning cum defence 
sudo python3 src/ddos_botnet.py or ddos_botnet_pro.py-> simulation .
