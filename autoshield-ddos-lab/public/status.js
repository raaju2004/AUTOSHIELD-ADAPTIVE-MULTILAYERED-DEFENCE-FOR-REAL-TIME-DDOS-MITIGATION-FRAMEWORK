// Real-time metrics polling
setInterval(async () => {
    try {
        const resp = await fetch('/status.json');
        const data = await resp.json();
        
        document.getElementById('requests').textContent = `Requests: ${data.requests}`;
        document.getElementById('cpu').textContent = `CPU: ${data.cpu}%`;
        document.getElementById('latency').textContent = `Latency: ${data.latency}ms`;
        
        const statusEl = document.getElementById('status');
        statusEl.textContent = `Status: ${data.status}`;
        
        if (data.status === 'UNDER ATTACK') {
            statusEl.className = 'metric critical';
            document.body.style.background = '#330000';
        } else {
            statusEl.className = 'metric';
            document.body.style.background = '#000000';
        }
    } catch(e) {
        console.error('Monitoring failed:', e);
    }
}, 1000);
