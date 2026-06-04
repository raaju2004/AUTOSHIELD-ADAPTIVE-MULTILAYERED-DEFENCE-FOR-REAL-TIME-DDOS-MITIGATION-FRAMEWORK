#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import time
import random
import os
from collections import deque
import config
from defense_mechanism import DefenseMechanism  # ← CONNECTION!

class AutoShieldIDS:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.attack_patterns = deque(maxlen=10000)
        self.defense_active = False
        self.blocked_ips = set()
        self.confidence_history = deque(maxlen=100)
        self.defense = DefenseMechanism()  # ← ML CONTROLS DEFENSE!
        
    def capture_live_traffic(self):
        """Simulate + capture live traffic"""
        traffic_data = []
        for _ in range(100):
            flow = {
                'count': np.random.poisson(random.choice([5, 8, 500, 1200])),
                'bytes': random.choice([300, 600, 1800, 5000]),
                'pps': np.random.poisson(random.choice([2, 4, 150, 400])),
                'src_ip': f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            }
            traffic_data.append(flow)
        return pd.DataFrame(traffic_data)
    
    def train_adaptive_model(self):
        print("🎯 Training Adaptive ML Model...")
        X_live = self.capture_live_traffic()[['count', 'bytes', 'pps']].fillna(0)
        X_scaled = self.scaler.fit_transform(X_live)
        self.model.fit(X_scaled)
        self.is_trained = True
        print("✅ ML Model READY")
    
    def detect_and_defend(self):
        """ML DETECTION → AUTO DEFENSE ACTIVATION"""
        self.train_adaptive_model()
        
        print("🚀 LIVE ML DETECTION + DEFENSE")
        while True:
            df = self.capture_live_traffic()
            X = df[['count', 'bytes', 'pps']].tail(50)
            
            if len(X) > 10:
                X_scaled = self.scaler.transform(X)
                predictions = self.model.predict(X_scaled)
                anomalies = np.sum(predictions == -1) / len(predictions)
                
                self.confidence_history.append(anomalies)
                avg_confidence = np.mean(self.confidence_history)
                
                print(f"📊 ML Score: {avg_confidence:.2f} | Packets: {len(df)}")
                
                # 🔥 ML → DEFENSE TRIGGER
                if avg_confidence > config.DDOS_THRESHOLD:
                    if not self.defense_active:
                        print(f"\n🚨 DDOS DETECTED! ML Confidence: {avg_confidence:.2f}")
                        self.defense.implement_defense_mechanism(
                            config.TARGET_IP, config.TARGET_PORT
                        )
                        self.defense_active = True
                else:
                    if self.defense_active:
                        print("✅ Attack Mitigated - Defense Deactivated")
                        self.defense_active = False
                
                time.sleep(1)

if __name__ == "__main__":
    ids = AutoShieldIDS()
    ids.detect_and_defend()
