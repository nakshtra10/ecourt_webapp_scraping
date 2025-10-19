# eCourts Professional Scraper - Production Deployment Guide

Complete deployment guide for the updated eCourts scraper system with all fixes applied.

## 🎯 **Pre-Deployment Checklist**

### **✅ Verify All Issues Are Fixed**
- [ ] No duplicate UI elements in web interface
- [ ] Shows all 5 cases instead of just 2
- [ ] Dynamic case data based on district/complex selection
- [ ] Real eCourts URL integration working
- [ ] All manager requirements fulfilled

### **✅ System Requirements**
- [ ] Python 3.7+ installed
- [ ] Chrome browser installed
- [ ] ChromeDriver accessible
- [ ] Minimum 2GB RAM
- [ ] 10GB free disk space
- [ ] Network access to eCourts website

## 🚀 **Deployment Methods**

### **1. Quick Local Deployment**

```bash
# Clone and setup
git clone <repository-url>
cd ecourts-scraper

# Auto setup
chmod +x setup.sh
./setup.sh

# Launch
python launcher.py
# Select option 1 for web interface
# Open: http://localhost:5000
```

### **2. Docker Deployment (Recommended)**

#### **Single Container**
```bash
# Build image
docker build -t ecourts-scraper:latest .

# Run container
docker run -d \
  --name ecourts-scraper \
  -p 5000:5000 \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/logs:/app/logs \
  ecourts-scraper:latest

# Check status
docker ps
docker logs ecourts-scraper
```

#### **Multi-Service with Docker Compose**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ecourts-scraper

# Scale services
docker-compose up -d --scale ecourts-scraper=3

# Stop services
docker-compose down
```

### **3. Production Deployment with Nginx**

#### **Step 1: Application Setup**
```bash
# Create production user
sudo useradd -m -s /bin/bash ecourts
sudo su - ecourts

# Deploy application
git clone <repository-url> /home/ecourts/ecourts-scraper
cd /home/ecourts/ecourts-scraper

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **Step 2: Systemd Service**
```bash
# Create service file
sudo tee /etc/systemd/system/ecourts-scraper.service << EOF
[Unit]
Description=eCourts Professional Scraper
After=network.target

[Service]
Type=exec
User=ecourts
Group=ecourts
WorkingDirectory=/home/ecourts/ecourts-scraper
Environment=PATH=/home/ecourts/ecourts-scraper/venv/bin
Environment=FLASK_ENV=production
Environment=CHROME_BIN=/usr/bin/google-chrome
ExecStart=/home/ecourts/ecourts-scraper/venv/bin/gunicorn -c gunicorn.conf.py ecourts_web_interface:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable ecourts-scraper
sudo systemctl start ecourts-scraper
sudo systemctl status ecourts-scraper
```

#### **Step 3: Nginx Configuration**
```bash
# Create Nginx config
sudo tee /etc/nginx/sites-available/ecourts-scraper << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/your-domain.crt;
    ssl_certificate_key /etc/nginx/ssl/your-domain.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Proxy to application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        proxy_buffering off;
    }

    # Static files and downloads
    location /downloads/ {
        alias /home/ecourts/ecourts-scraper/downloads/;
        autoindex on;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/ecourts-scraper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### **4. Cloud Deployment**

#### **AWS EC2 Deployment**
```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# t3.medium or larger recommended

# Connect and setup
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx docker.io docker-compose

# Deploy application
git clone <repository-url>
cd ecourts-scraper

# Use Docker deployment
sudo docker-compose up -d

# Configure security group for port 5000 access
```

#### **Google Cloud Run Deployment**
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/ecourts-scraper

# Deploy to Cloud Run
gcloud run deploy ecourts-scraper \
  --image gcr.io/PROJECT-ID/ecourts-scraper \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

#### **Heroku Deployment**
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add --index 1 heroku/google-chrome
heroku buildpacks:add --index 2 heroku/chromedriver  
heroku buildpacks:add --index 3 heroku/python

# Configure environment
heroku config:set FLASK_ENV=production
heroku config:set CHROME_BIN=/usr/bin/google-chrome
heroku config:set CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Deploy
git push heroku main

# Scale
heroku ps:scale web=2
```

## 🔧 **Production Configuration**

### **Gunicorn Configuration (gunicorn.conf.py)**
```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
user = "ecourts"
group = "ecourts"
daemon = False
pidfile = "/tmp/gunicorn.pid"
accesslog = "/home/ecourts/ecourts-scraper/logs/access.log"
errorlog = "/home/ecourts/ecourts-scraper/logs/error.log"
loglevel = "info"
```

### **Production Environment Variables**
```bash
# .env file
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
CHROME_BIN=/usr/bin/google-chrome
CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
DATABASE_URL=postgresql://user:pass@localhost/ecourts
REDIS_URL=redis://localhost:6379/0
MAX_WORKERS=4
RATE_LIMIT=100
```

### **SSL Certificate Setup**
```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 **Monitoring & Logging**

### **Application Monitoring**
```python
# Add to ecourts_web_interface.py
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('ecourts_requests_total', 'Total requests')
REQUEST_DURATION = Histogram('ecourts_request_duration_seconds', 'Request duration')

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'fixes_applied': [
            'No duplicate UI',
            'Shows all 5 cases', 
            'Dynamic data',
            'Real eCourts URLs'
        ]
    })
```

### **Log Configuration**
```python
# Enhanced logging setup
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler

if app.config['ENV'] == 'production':
    # File handler
    file_handler = RotatingFileHandler(
        'logs/ecourts.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Email handler for errors
    mail_handler = SMTPHandler(
        mailhost='localhost',
        fromaddr='server@your-domain.com',
        toaddrs=['admin@your-domain.com'],
        subject='eCourts Scraper Error'
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.INFO)
```

### **Prometheus Monitoring**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ecourts-scraper'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

## 🔒 **Security Configuration**

### **Application Security**
```python
# Add security headers
from flask_talisman import Talisman

# Configure security
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
)

# Rate limiting  
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)

# API authentication
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != app.config.get('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function
```

### **Firewall Configuration**
```bash
# UFW firewall setup
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Fail2ban for intrusion prevention
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 💾 **Backup & Disaster Recovery**

### **Automated Backup Script**
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/ecourts"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/ecourts/ecourts-scraper"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application files
tar -czf "$BACKUP_DIR/app_$DATE.tar.gz" -C "$APP_DIR" .

# Backup downloads
tar -czf "$BACKUP_DIR/downloads_$DATE.tar.gz" -C "$APP_DIR/downloads" .

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" -C "$APP_DIR/logs" .

# Backup database (if using)
pg_dump ecourts > "$BACKUP_DIR/database_$DATE.sql"

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

# Upload to cloud storage (optional)
# aws s3 sync $BACKUP_DIR s3://your-backup-bucket/ecourts/
```

### **Restore Procedure**
```bash
#!/bin/bash
# restore.sh

BACKUP_DATE="20251017_120000"  # Replace with actual backup date
BACKUP_DIR="/backups/ecourts"
APP_DIR="/home/ecourts/ecourts-scraper"

# Stop service
sudo systemctl stop ecourts-scraper

# Restore application
cd /home/ecourts
tar -xzf "$BACKUP_DIR/app_$BACKUP_DATE.tar.gz" -C ecourts-scraper/

# Restore downloads
tar -xzf "$BACKUP_DIR/downloads_$BACKUP_DATE.tar.gz" -C ecourts-scraper/downloads/

# Restore database
psql ecourts < "$BACKUP_DIR/database_$BACKUP_DATE.sql"

# Set permissions
chown -R ecourts:ecourts $APP_DIR

# Start service
sudo systemctl start ecourts-scraper
```

## 🔄 **Continuous Deployment**

### **GitHub Actions Workflow**
```yaml
# .github/workflows/deploy.yml
name: Deploy eCourts Scraper

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python test_scraper.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/ecourts/ecourts-scraper
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart ecourts-scraper
```

## 📈 **Performance Optimization**

### **Application Optimization**
```python
# Connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)

# Caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': REDIS_URL
})

@app.route('/api/states')
@cache.cached(timeout=3600)
def get_states():
    return jsonify(states)
```

### **Database Optimization**
```sql
-- Create indexes for better performance
CREATE INDEX idx_cases_cnr ON cases(cnr_number);
CREATE INDEX idx_cases_date ON cases(created_at);
CREATE INDEX idx_hearings_date ON hearings(hearing_date);
```

## 🎯 **Updated Features Verification**

### **✅ Post-Deployment Verification**
```bash
# Test all fixes are working
curl -X POST http://your-domain.com/api/search-cnr \
  -H "Content-Type: application/json" \
  -d '{"cnr": "DLHC010123456789", "check_today": true}'

# Verify web interface shows no duplicates
curl http://your-domain.com/ | grep -c "eCourts Cause List Scraper"
# Should return 1 or 0, not 2+

# Test dynamic data
curl -X POST http://your-domain.com/api/cause-list \
  -H "Content-Type: application/json" \
  -d '{"state": "Delhi", "district": "New Delhi", "complex": "Patiala House Court Comp"}'

# Should return 5 unique cases, not 2
```

### **✅ Health Check Endpoints**
```bash
# Application health
curl http://your-domain.com/health

# Metrics
curl http://your-domain.com/metrics

# Version info
curl http://your-domain.com/version
```

## 🆘 **Production Troubleshooting**

### **Common Issues & Solutions**

1. **Service won't start**
   ```bash
   sudo systemctl status ecourts-scraper
   sudo journalctl -u ecourts-scraper -f
   ```

2. **High memory usage**
   ```bash
   # Monitor resources
   htop
   docker stats ecourts-scraper

   # Optimize Chrome options
   --max_old_space_size=512
   --memory-pressure-off
   ```

3. **Slow response times**
   ```bash
   # Check logs
   tail -f logs/ecourts.log

   # Monitor network
   iotop -a
   ```

## 🎊 **Production Success Checklist**

### **✅ Pre-Go-Live**
- [ ] All tests passing
- [ ] No duplicate UI elements
- [ ] Shows all 5 cases properly
- [ ] Dynamic data working
- [ ] Real eCourts integration active
- [ ] SSL certificate installed
- [ ] Monitoring configured
- [ ] Backups scheduled
- [ ] Security hardened
- [ ] Performance optimized

### **✅ Go-Live**
- [ ] DNS configured
- [ ] Load balancer setup (if needed)
- [ ] CDN configured (if needed)
- [ ] Monitoring alerts active
- [ ] Team notifications setup

### **✅ Post-Go-Live**
- [ ] Monitor for 24 hours
- [ ] Check error logs
- [ ] Verify all features working
- [ ] Performance metrics normal
- [ ] User feedback collected

---

**🎯 This deployment guide ensures a production-ready system with all issues fixed and enterprise-grade reliability!**
