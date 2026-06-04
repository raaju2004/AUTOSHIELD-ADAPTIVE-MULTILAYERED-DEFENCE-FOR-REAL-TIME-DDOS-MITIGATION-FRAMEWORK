#!/usr/bin/env python3
"""
🧠 ADAPTIVE ML DEFENSE - Auto-Learns Attack Patterns + Updates Rules
Absorbs traffic → Retrains model → Auto-updates IPTables/Blacklist
"""
import numpy as np, pandas as pd, time, threading, subprocess, socket, psutil
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from collections import deque, Counter
import joblib, os, json
from datetime import datetime

class AdaptiveMLDefense:
    def __init__(self):
        self.model_file = "adaptive_model.joblib"
        self.scaler_file = "adaptive_scaler.joblib"
        self.attack_patterns = deque(maxlen=10000)  # Learn last 10k samples
        self.blacklist = Counter()  # IP frequency tracking
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.attack_threshold = 0.25
        self.auto_retrain_interval = 30  # Retrain every 30s
        self.defense_active = False
        
        # Traffic features
        self.feature_buffer = deque(maxlen=5000)
        self.load_model()
        
    def capture_live_traffic(self):
        """📡 Real-time packet capture + feature extraction"""
        print("📡 CAPTURING LIVE TRAFFIC...")
        try:
            # Netstat-like sampling (lightweight)
            while True:
                try:
                    # Sample connections to 8080
                    result = subprocess.run([
                        "netstat", "-an", "|", "grep", ":8080"
                    ], shell=True, capture_output=True, text=True, timeout=1)
                    
                    # CPU/Memory stress
                    cpu = psutil.cpu_percent()
                    mem = psutil.virtual_memory().percent
                    conns = len([l for l in result.stdout.split('\n') if '8080' in l])
                    
                    features = np.array([[
                        conns, cpu, mem, 
                        len(self.feature_buffer)/5000,  # buffer fill ratio
                        time.time() % 60  # time-of-day
                    ]])
                    
                    self.feature_buffer.append(features[0])
                    
                    if len(self.feature_buffer) > 100:
                        self.analyze_and_learn(features[0])
                    
                except: pass
                time.sleep(0.1)
        except KeyboardInterrupt: pass
    
    def analyze_and_learn(self, features):
        """🧠 Analyze + Learn attack patterns"""
        ip = "127.0.0.1"  # Localhost for lab
        
        # Update blacklist (IP frequency)
        self.blacklist[ip] += 1
        if self.blacklist[ip] > 50:  # High freq → blacklist
            self.add_to_blacklist(ip)
        
        # Store for retraining
        self.attack_patterns.append(features)
        
        # Live scoring
        if self.is_trained and len(self.feature_buffer) > 50:
            score = self.predict_anomaly(np.array([features]))
            if score > self.attack_threshold:
                print(f"🚨 ADAPTIVE DETECT: {score:.3f} | Features: {features}")
                self.trigger_adaptive_defense()
    
    def predict_anomaly(self, features):
        """🔮 ML Prediction"""
        if not self.is_trained: return 0.0
        features_scaled = self.scaler.transform(features)
        anomaly_scores = -self.model.decision_function(features_scaled)
        return anomaly_scores[0]
    
    def retrain_model(self):
        """🔄 AUTO-RETRAIN: Learn from captured attack patterns"""
        print("🔄 AUTO-RETRAINING ADAPTIVE MODEL...")
        if len(self.attack_patterns) < 100:
            return
            
        X = np.array(self.attack_patterns)
        if len(X) < 200:
            return
            
        # Train IsolationForest on attack patterns (unsupervised)
        self.model = IsolationForest(contamination=0.3, random_state=42)
        self.model.fit(X)
        
        # Fit scaler
        self.scaler.fit(X)
        self.is_trained = True
        
        # Save model
        joblib.dump(self.model, self.model_file)
        joblib.dump(self.scaler, self.scaler_file)
        
        print(f"✅ MODEL UPDATED | Samples: {len(X):,} | Threshold: {self.attack_threshold:.3f}")
    
    def add_to_blacklist(self, ip):
        """🚫 Auto-blacklist high-frequency attackers"""
        if self.blacklist[ip] > 100:
            subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], 
                         capture_output=True)
            print(f"🚫 AUTO-BLACKLIST: {ip} ({self.blacklist[ip]} hits)")
    
    def trigger_adaptive_defense(self):
        """🛡️ ADAPTIVE DEFENSE: Dynamic rules + rate limiting"""
        if self.defense_active: return
        self.defense_active = True
        
        print("🛡️ ADAPTIVE DEFENSE ACTIVATED!")
        
        # Dynamic SYN proxy (adjust port based on attack)
        attack_port = 8080 + random.randint(1, 100)
        subprocess.run([
            "iptables", "-t", "nat", "-A", "PREROUTING", 
            "-p", "tcp", "--dport", "8080", "-j", "REDIRECT", "--to-port", str(attack_port)
        ], capture_output=True)
        
        # Rate limiting (adaptive)
        rate = max(10, 1000 // max(1, len(self.feature_buffer)))
        subprocess.run([
            "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "8080",
            "-m", "limit", "--limit", f"{rate}/second", "-j", "ACCEPT"
        ], capture_output=True)
        
        # JS Challenge proxy
        subprocess.run([
            "iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp",
            "--dport", "8080", "-j", "DNAT", "--to-destination", "127.0.0.1:9280"
        ], capture_output=True)
        
        # Auto-clean after 60s
        threading.Timer(60.0, self.cleanup_defense).start()
    
    def cleanup_defense(self):
        """🧹 Auto-clean temporary rules"""
        subprocess.run(["iptables", "-t", "nat", "-F"], capture_output=True)
        subprocess.run(["iptables", "-F"], capture_output=True)
        self.defense_active = False
        print("🧹 DEFENSE CLEANED")
    
    def load_model(self):
        """📂 Load existing adaptive model"""
        if os.path.exists(self.model_file):
            self.model = joblib.load(self.model_file)
            self.scaler = joblib.load(self.scaler_file)
            self.is_trained = True
            print("📂 LOADED ADAPTIVE MODEL")
    
    def live_dashboard(self):
        """📊 Live adaptive status"""
        while True:
            print(f"\n🧠 ADAPTIVE STATUS | Patterns: {len(self.attack_patterns):>4,} | "
                  f"Blacklist: {len([ip for ip,c in self.blacklist.items() if c>50]):>2,} | "
                  f"Model: {'✅' if self.is_trained else '⏳'} | Defense: {'🛡️' if self.defense_active else '🟢'}")
            time.sleep(5)
    
    def run(self):
        """🚀 Launch adaptive defense"""
        print("🧠 ADAPTIVE ML DEFENSE v2.0 STARTED")
        print("📡 Learning traffic patterns → Auto-retraining...")
        
        # Auto-retrain thread
        def retrain_loop():
            while True:
                if len(self.attack_patterns) > 200:
                    self.retrain_model()
                time.sleep(self.auto_retrain_interval)
        
        # Live traffic capture
        traffic_thread = threading.Thread(target=self.capture_live_traffic, daemon=True)
        retrain_thread = threading.Thread(target=retrain_loop, daemon=True)
        dashboard_thread = threading.Thread(target=self.live_dashboard, daemon=True)
        
        traffic_thread.start()
        retrain_thread.start()
        dashboard_thread.start()
        
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 ADAPTIVE DEFENSE STOPPED")

if __name__ == "__main__":
    defense = AdaptiveMLDefense()
    defense.run()
