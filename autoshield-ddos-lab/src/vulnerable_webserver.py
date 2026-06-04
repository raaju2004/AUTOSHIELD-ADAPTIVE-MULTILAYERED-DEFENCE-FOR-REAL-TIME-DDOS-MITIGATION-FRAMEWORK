def do_GET(self):
    if '/status.json' in self.path:
        self.send_status_json()
        return
    
def send_status_json(self):
    import psutil
    import time
    
    self.outer.requests += 1
    
    status_data = {
        'requests': self.outer.requests,
        'errors': self.outer.errors,
        'cpu': psutil.cpu_percent(interval=0.1),
        'memory': psutil.virtual_memory().percent,
        'timestamp': time.time(),
        'status': 'UNDER ATTACK' if self.outer.requests > 200 else 'NORMAL'
    }
    
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(status_data).encode())
