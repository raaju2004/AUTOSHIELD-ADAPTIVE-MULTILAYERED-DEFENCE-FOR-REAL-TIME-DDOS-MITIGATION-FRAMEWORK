import socketserver, threading, time, json, random, socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import subprocess, psutil

class EnhancedStats:
    rps = 0; anomaly = 0; status = "NORMAL"; dropped = 0
    failover_syn = False; failover_js = False; uptime = 0
    cpu = 0; mem = 0; connections = 0

class DebugHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/': self.modern_dashboard()
        elif self.path == '/api/stats': self.json_stats()
        elif self.path == '/api/debug': self.debug_info()
        elif self.path == '/api/ports': self.check_ports()
        else: self.error_404()
    
    def modern_dashboard(self):
        self.send_response(200); self.send_header('Content-Type', 'text/html'); self.end_headers()
        self.wfile.write(ULTIMATE_UI.encode())
    
    def json_stats(self):
        stats = {
            'rps': EnhancedStats.rps + random.randint(-20, 80),
            'anomaly': EnhancedStats.anomaly,
            'status': EnhancedStats.status,
            'dropped': EnhancedStats.dropped,
            'failover_syn': EnhancedStats.failover_syn,
            'failover_js': EnhancedStats.failover_js,
            'uptime': EnhancedStats.uptime,
            'cpu': EnhancedStats.cpu,
            'mem': EnhancedStats.mem,
            'connections': EnhancedStats.connections,
            'timestamp': datetime.now().isoformat()
        }
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
        self.wfile.write(json.dumps(stats).encode())
    
    def debug_info(self):
        debug = {
            'ml_running': any('ml_detection' in p.cmdline() for p in psutil.process_iter()),
            'iptables': subprocess.getoutput('sudo iptables -L INPUT -vn | grep 8080 || echo "NO DROP"'),
            'ports': {8080: self.port_check(8080), 9080: self.port_check(9080), 9280: self.port_check(9280)},
            'processes': subprocess.getoutput('ps aux | grep -E "ddos|ml_detection" | grep -v grep | head -5')
        }
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
        self.wfile.write(json.dumps(debug, indent=2).encode())
    
    def check_ports(self):
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
        ports = {8080: self.port_check(8080), 9080: self.port_check(9080), 9280: self.port_check(9280)}
        self.wfile.write(json.dumps(ports).encode())
    
    def port_check(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return {'status': 'UP' if result == 0 else 'DOWN', 'port': port}
    
    def error_404(self):
        self.send_response(404); self.send_header('Content-Type', 'text/plain'); self.end_headers()
        self.wfile.write(b'404 - Endpoint not found')

# 🔥 ULTIMATE DASHBOARD v2.0
ULTIMATE_UI = '''
<!DOCTYPE html><html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width">
<title>AutoShield Pro - DDoS Defense v2.0</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:linear-gradient(135deg,#000428 0%,#004e92 100%);min-height:100vh;color:#fff;overflow-x:hidden;position:relative}
#particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1}
.container{max-width:1600px;margin:0 auto;padding:2rem;position:relative;z-index:10}
.header{text-align:center;background:linear-gradient(135deg,rgba(255,255,255,0.1),rgba(255,255,255,0.05));backdrop-filter:blur(30px);border-radius:32px;padding:3rem 2rem;border:1px solid rgba(255,255,255,0.15);margin-bottom:3rem}
.header h1{font-size:clamp(3rem,6vw,5rem);background:linear-gradient(135deg,#00ff88,#00f5ff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;margin-bottom:1rem;letter-spacing:-2px}
.tagline{font-size:1.3rem;opacity:0.9;background:linear-gradient(135deg,#00ff88,#00f5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:2rem;margin-bottom:3rem}
.stat-card{background:rgba(255,255,255,0.08);backdrop-filter:blur(25px);border-radius:24px;padding:2.5rem 2rem;border:1px solid rgba(255,255,255,0.12);transition:all 0.4s cubic-bezier(0.25,0.46,0.45,0.94);position:relative;overflow:hidden}
.stat-card::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:2px;background:linear-gradient(90deg,transparent,#00ff88,transparent);transition:left 0.6s}
.stat-card:hover::before{left:100%}
.stat-card:hover{transform:translateY(-16px) scale(1.02);box-shadow:0 40px 80px rgba(0,0,0,0.4);border-color:rgba(0,255,136,0.3)}
.stat-value{font-size:clamp(2.8rem,5vw,6rem);font-weight:800;background:linear-gradient(135deg,#00ff88,#00f5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.75rem}
.stat-label{font-size:1.2rem;font-weight:500;opacity:0.85;text-transform:uppercase;letter-spacing:1px}
.status-badge{display:inline-flex;align-items:center;gap:0.75rem;padding:0.75rem 1.5rem;border-radius:50px;background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);font-weight:600;font-size:1rem;transition:all 0.3s}
.status-defense{background:rgba(239,68,68,0.2) !important;border-color:rgba(239,68,68,0.4) !important;color:#f87171 !important}
.status-badge .icon{width:20px;height:20px;border-radius:50%;animation:pulse 1.5s infinite}
.status-defense .icon{background:#ef4444 !important;box-shadow:0 0 20px #ef4444 !important}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.6;transform:scale(1.1)}}
.debug-panel{background:rgba(0,0,0,0.4);backdrop-filter:blur(20px);border-radius:24px;padding:2rem;border:1px solid rgba(255,255,255,0.1);margin-bottom:3rem}
.debug-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.5rem}
.debug-item{padding:1.5rem;background:rgba(255,255,255,0.05);border-radius:16px;border-right:4px solid transparent;transition:all 0.3s}
.debug-ok{border-right-color:#10b981 !important}
.debug-warn{border-right-color:#f59e0b !important}
.debug-err{border-right-color:#ef4444 !important}
.debug-label{font-size:0.95rem;opacity:0.7;margin-bottom:0.5rem;font-weight:500}
.debug-value{font-weight:600;font-size:1.1rem}
.failover-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin:3rem 0}
.failover-card{background:rgba(255,255,255,0.08);backdrop-filter:blur(25px);border-radius:24px;padding:3rem 2rem;text-align:center;border:1px solid rgba(255,255,255,0.15);transition:all 0.4s}
.failover-card:hover{transform:translateY(-12px);box-shadow:0 32px 64px rgba(0,0,0,0.3)}
.failover-title{font-size:1.4rem;font-weight:700;margin-bottom:1.5rem;background:linear-gradient(135deg,#00ff88,#00f5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.failover-btn{display:block;width:100%;padding:1.5rem 3rem;border-radius:20px;border:none;font-size:1.2rem;font-weight:700;cursor:pointer;transition:all 0.3s;text-decoration:none;text-align:center;margin-top:1.5rem}
.syn-proxy{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;box-shadow:0 12px 32px rgba(59,130,246,0.4)}
.syn-proxy:hover{background:linear-gradient(135deg,#2563eb,#1e40af);transform:translateY(-4px);box-shadow:0 20px 48px rgba(59,130,246,0.6)}
.js-challenge{background:linear-gradient(135deg,#10b981,#059669);color:white;box-shadow:0 12px 32px rgba(16,185,129,0.4)}
.js-challenge:hover{background:linear-gradient(135deg,#059669,#047857);transform:translateY(-4px);box-shadow:0 20px 48px rgba(16,185,129,0.6)}
.chart-container{background:rgba(255,255,255,0.05);backdrop-filter:blur(20px);border-radius:24px;padding:2rem;border:1px solid rgba(255,255,255,0.1);height:450px;margin-bottom:3rem;overflow:hidden}
#chart{position:relative;width:100%;height:100%}
.timestamp{color:rgba(255,255,255,0.5);text-align:center;font-size:0.95rem;margin-top:2rem;letter-spacing:0.5px}
@media (max-width:768px){.container{padding:1rem}.stats-grid{grid-template-columns:1fr;gap:1.5rem}}
</style></head><body>
<canvas id="particles"></canvas>
<div class="container">
<div class="header">
<h1>🛡️ AutoShield Pro</h1><p class="tagline">Next-Gen ML DDoS Protection • Real-time Analytics • Zero-Downtime Failover</p>
</div>

<div class="stats-grid">
<div class="stat-card"><div class="stat-value" id="rps">0</div><div class="stat-label">RPS <span class="status-badge" id="rps-badge"><span class="icon" style="background:#10b981"></span>NORMAL</span></div></div>
<div class="stat-card"><div class="stat-value" id="anomaly">0.00</div><div class="stat-label">Anomaly Score</div></div>
<div class="stat-card"><div class="stat-value" id="dropped">0</div><div class="stat-label">Dropped Pkts</div></div>
<div class="stat-card"><div class="stat-value" id="status">STANDBY</div><div class="stat-label">Status <span class="status-badge" id="status-badge"><span class="icon"></span>READY</span></div></div>
</div>

<div class="chart-container"><canvas id="chart"></canvas></div>

<div class="failover-grid">
<div class="failover-card">
<div class="failover-title">🔒 SYN Proxy</div>
<div>Port <strong>9080</strong> • 3-Way Handshake Validation</div>
<a href="http://localhost:9080" class="failover-btn syn-proxy" target="_blank">→ Test SYN Proxy</a>
<div id="syn-status" style="margin-top:1rem;font-size:0.95rem;color:#6b7280">Status: <span id="syn-port">Checking...</span></div>
</div>
<div class="failover-card">
<div class="failover-title">🎭 JS Challenge</div>
<div>Port <strong>9280</strong> • Browser Fingerprint + PoW</div>
<a href="http://localhost:9280" class="failover-btn js-challenge" target="_blank">→ Test JS Challenge</a>
<div id="js-status" style="margin-top:1rem;font-size:0.95rem;color:#6b7280">Status: <span id="js-port">Checking...</span></div>
</div>
</div>

<div class="debug-panel">
<h3 style="margin-bottom:1.5rem;font-size:1.3rem;font-weight:600">🔍 System Debug</h3>
<div class="debug-grid" id="debug-grid"></div>
<button onclick="refreshDebug()" style="background:rgba(0,255,136,0.2);border:1px solid #00ff88;color:#00ff88;padding:0.75rem 1.5rem;border-radius:12px;cursor:pointer;font-weight:600;margin-top:1rem;transition:all 0.3s">🔄 Refresh Debug</button>
</div>

<div class="timestamp" id="timestamp">Initializing...</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx=document.getElementById('chart').getContext('2d');
const chart=new Chart(ctx,{type:'line',data:{labels:[],datasets:[{label:'RPS',data:[],borderColor:'#00ff88',backgroundColor:'rgba(0,255,136,0.15)',tension:0.4,borderWidth:4,fill:true}]},options:{responsive:true,maintainAspectRatio:false,scales:{y:{beginAtZero:true,grid:{color:'rgba(255,255,255,0.1)'},ticks:{color:'rgba(255,255,255,0.6)'}},x:{grid:{color:'rgba(255,255,255,0.05)'},ticks:{color:'rgba(255,255,255,0.4)'}}},plugins:{legend:{labels:{color:'white'}}}}});

let dataPoints=[];function updateStats(){fetch('/api/stats').then(r=>r.json()).then(s=>{document.getElementById('rps').textContent=s.rps.toLocaleString();document.getElementById('anomaly').textContent=s.anomaly.toFixed(2);document.getElementById('dropped').textContent=s.dropped.toLocaleString();document.getElementById('status').textContent=s.status;const rpsBadge=document.getElementById('rps-badge'),statusBadge=document.getElementById('status-badge');rpsBadge.className=s.rps>25?'status-badge status-defense':'status-badge';statusBadge.className=s.status==='DEFENSE ACTIVE'?'status-badge status-defense':'status-badge';rpsBadge.querySelector('.icon').style.background=s.rps>25?'#ef4444':'#10b981';statusBadge.querySelector('.icon').style.background=s.status==='DEFENSE ACTIVE'?'#ef4444':'#10b981';dataPoints.push(s.rps);if(dataPoints.length>60)dataPoints.shift();chart.data.labels=Array(dataPoints.length).fill('').map((_,i)=>`${i*2}s`);chart.data.datasets[0].data=dataPoints;chart.update('none');document.getElementById('timestamp').textContent=`Updated: ${new Date(s.timestamp).toLocaleString()}`;EnhancedStats.failover_syn=s.failover_syn;EnhancedStats.failover_js=s.failover_js;}).catch(()=>console.error('Stats fetch failed'))}async function refreshDebug(){document.getElementById('debug-grid').innerHTML='<div class="debug-item">Loading...</div>';try{const d=await fetch('/api/debug').then(r=>r.json()),ports=await fetch('/api/ports').then(r=>r.json());let html='';html+=`<div class="debug-item ${d.ml_running?'debug-ok':'debug-warn'}"><div class="debug-label">ML Detection</div><div class="debug-value">${d.ml_running?'✅ RUNNING':'⚠️ NOT RUNNING'}</div></div>`;html+=`<div class="debug-item ${d.iptables.includes('DROP')?'debug-ok':'debug-warn'}"><div class="debug-label">IPTables</div><div class="debug-value">${d.iptables.includes('DROP')?'🛡️ ACTIVE':'⚪️ STANDBY'}</div></div>`;html+=`<div class="debug-item ${ports[8080].status==='UP'?'debug-ok':'debug-err'}"><div class="debug-label">Port 8080</div><div class="debug-value">${ports[8080].status}</div></div>`;html+=`<div class="debug-item ${ports[9080].status==='UP'?'debug-ok':'debug-warn'}"><div class="debug-label">SYN Proxy 9080</div><div class="debug-value">${ports[9080].status}</div></div>`;html+=`<div class="debug-item ${ports[9280].status==='UP'?'debug-ok':'debug-warn'}"><div class="debug-label">JS Challenge 9280</div><div class="debug-value">${ports[9280].status}</div></div>`;document.getElementById('debug-grid').innerHTML=html;document.getElementById('syn-port').textContent=ports[9080].status;document.getElementById('js-port').textContent=ports[9280].status;}catch(e){document.getElementById('debug-grid').innerHTML='<div class="debug-item debug-err"><div class="debug-label">Debug Error</div><div class="debug-value">API unavailable</div></div>';}}const canvas=document.getElementById('particles'),pCtx=canvas.getContext('2d');canvas.width=window.innerWidth;canvas.height=window.innerHeight;let particles=[];for(let i=0;i<150;i++)particles.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,vx:(Math.random()-0.5)*0.8,vy:(Math.random()-0.5)*0.8,r:Math.random()*1.5+0.5,alpha:Math.random()*0.5+0.2});function animate(){pCtx.clearRect(0,0,canvas.width,canvas.height);particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>canvas.width)p.vx*=-1;if(p.y<0||p.y>canvas.height)p.vy*=-1;pCtx.save();pCtx.globalAlpha=p.alpha;pCtx.beginPath();pCtx.arc(p.x,p.y,p.r,0,Math.PI*2);const gradient=pCtx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*3);gradient.addColorStop(0,'rgba(0,255,136,0.8)');gradient.addColorStop(1,'rgba(0,245,255,0)');pCtx.fillStyle=gradient;pCtx.fill();pCtx.restore();});requestAnimationFrame(animate);}animate();updateStats();setInterval(updateStats,1500);refreshDebug();setInterval(refreshDebug,10000);window.addEventListener('resize',()=>{canvas.width=window.innerWidth;canvas.height=window.innerHeight;});
</script></body></html>
'''

def update_stats():
    EnhancedStats.uptime = time.time()
    EnhancedStats.cpu = psutil.cpu_percent(interval=1)
    EnhancedStats.mem = psutil.virtual_memory().percent
    EnhancedStats.connections = len(psutil.net_connections())

def stats_worker():
    while True:
        update_stats()
        EnhancedStats.rps = random.randint(5, 850)  # Simulate
        EnhancedStats.anomaly = random.uniform(0, 0.65)
        EnhancedStats.status = EnhancedStats.rps > 200 and "DEFENSE ACTIVE" or "NORMAL"
        EnhancedStats.dropped = random.randint(0, 12500)
        EnhancedStats.failover_syn = random.choice([True, False])
        EnhancedStats.failover_js = random.choice([True, False])
        time.sleep(2)

if __name__ == '__main__':
    print("🚀 AutoShield Pro v2.0 - http://localhost:8080")
    print("📊 Debug: http://localhost:8080/api/debug")
    threading.Thread(target=stats_worker, daemon=True).start()
    httpd = HTTPServer(('localhost', 8080), DebugHandler)
    httpd.serve_forever()
