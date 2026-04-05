# Deployment Guide

## Method 1: Direct (simplest)

```bash
git clone https://github.com/yzha0302/asyre-file.git
cd asyre-file
python3 server.py
```

Requirements: Python 3.8+

## Method 2: Docker

```bash
git clone https://github.com/yzha0302/asyre-file.git
cd asyre-file
docker compose up -d
```

## Method 3: Behind Nginx (production)

```nginx
server {
    listen 80;
    server_name docs.example.com;

    location /editor/ {
        proxy_pass http://127.0.0.1:8765/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 50M;
    }
}
```

Then set `base_url` in config:
```json
{"server": {"base_url": "/editor"}}
```

## Method 4: systemd Service

```ini
# /etc/systemd/system/asyre-file.service
[Unit]
Description=Asyre File
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/asyre-file
ExecStart=/usr/bin/python3 server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now asyre-file
```

## Method 5: PM2 (Node.js process manager)

```bash
pm2 start server.py --name asyre-file --interpreter python3
pm2 save
```

## First-Run Setup

On first visit, you'll see the setup wizard. Alternatively, run headless setup:

```bash
python3 server.py --setup
```

## Backup

Back up these files regularly:
- `users.json` — user accounts
- `config.json` — configuration
- `data/` — all workspace files
- `api_tokens.json` — API tokens
