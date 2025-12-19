# Cloudflare Tunnel Setup

This document describes the Cloudflare Tunnel configuration for the Meta Lead Ads Dashboard.

## Overview

| Setting | Value |
|---------|-------|
| **Public URL** | `https://dashboard.hmebuild.com` |
| **Tunnel Name** | `meta-dashboard` |
| **Tunnel ID** | `74f34f4d-3784-4789-8748-3d616de90f90` |
| **Local Service** | `http://localhost:8501` (Streamlit) |
| **Authentication** | Cloudflare Access (Email OTP) |
| **Auto-start** | Yes (macOS Launch Daemon) |

## How It Works

1. **Cloudflare Tunnel** (`cloudflared`) runs as a system service on your Mac
2. It creates an outbound-only connection to Cloudflare's edge network
3. Traffic to `dashboard.hmebuild.com` is routed through this tunnel to `localhost:8501`
4. **Cloudflare Access** requires email authentication before allowing access
5. No ports are exposed on your Mac or router

## Requirements

- **Streamlit must be running** on `localhost:8501` for the dashboard to be accessible
- Your Mac must be on and connected to the internet

---

## Tunnel Management Commands

### Check Tunnel Status

```bash
cloudflared tunnel info meta-dashboard
```

### View Tunnel Logs

```bash
# Real-time logs
tail -f /Library/Logs/com.cloudflare.cloudflared.out.log

# Error logs
tail -f /Library/Logs/com.cloudflare.cloudflared.err.log

# View last 50 lines
tail -50 /Library/Logs/com.cloudflare.cloudflared.out.log
```

### Stop the Tunnel Service

```bash
sudo launchctl stop com.cloudflare.cloudflared
```

### Start the Tunnel Service

```bash
sudo launchctl start com.cloudflare.cloudflared
```

### Restart the Tunnel Service

```bash
sudo launchctl stop com.cloudflare.cloudflared && sudo launchctl start com.cloudflare.cloudflared
```

### Check if Service is Running

```bash
sudo launchctl list | grep cloudflare
```

---

## Streamlit Commands

### Start Streamlit (required for dashboard to work)

```bash
cd /Users/chris/Library/CloudStorage/SynologyDrive-Sync/Sites/meta-ads-api
source .venv/bin/activate
streamlit run app/dashboard.py
```

### Start Streamlit in Background

```bash
cd /Users/chris/Library/CloudStorage/SynologyDrive-Sync/Sites/meta-ads-api
source .venv/bin/activate
nohup streamlit run app/dashboard.py > /tmp/streamlit.log 2>&1 &
```

### Check if Streamlit is Running

```bash
lsof -i :8501
```

### Kill Streamlit Process

```bash
pkill -f "streamlit run"
```

---

## Configuration Files

### Tunnel Config

Location: `~/.cloudflared/config.yml`

```yaml
tunnel: 74f34f4d-3784-4789-8748-3d616de90f90
credentials-file: /Users/chris/.cloudflared/74f34f4d-3784-4789-8748-3d616de90f90.json

ingress:
  - hostname: dashboard.hmebuild.com
    service: http://localhost:8501
  - service: http_status:404
```

### Tunnel Credentials

Location: `~/.cloudflared/74f34f4d-3784-4789-8748-3d616de90f90.json`

**Keep this file secure** - it authenticates your tunnel with Cloudflare.

### Launch Daemon Plist

Location: `/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`

---

## Managing Access (Cloudflare Dashboard)

### Add/Remove Allowed Emails

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to **Access** → **Applications**
3. Click on **Meta Dashboard**
4. Edit the **Email Allowlist** policy
5. Add or remove email addresses
6. Save changes (takes effect immediately)

### View Access Logs

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to **Logs** → **Access**
3. Filter by application: `Meta Dashboard`

### Revoke a User's Session

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to **My Team** → **Users**
3. Find the user and revoke their session

---

## Troubleshooting

### Dashboard shows "Unable to connect"

1. Check if Streamlit is running:
   ```bash
   lsof -i :8501
   ```
2. If not running, start it:
   ```bash
   cd /Users/chris/Library/CloudStorage/SynologyDrive-Sync/Sites/meta-ads-api
   source .venv/bin/activate
   streamlit run app/dashboard.py
   ```

### Tunnel not connecting

1. Check tunnel status:
   ```bash
   cloudflared tunnel info meta-dashboard
   ```
2. Check logs for errors:
   ```bash
   tail -50 /Library/Logs/com.cloudflare.cloudflared.err.log
   ```
3. Restart the service:
   ```bash
   sudo launchctl stop com.cloudflare.cloudflared
   sudo launchctl start com.cloudflare.cloudflared
   ```

### DNS not resolving

1. Verify DNS record exists:
   ```bash
   nslookup dashboard.hmebuild.com
   ```
2. If missing, re-add the route:
   ```bash
   cloudflared tunnel route dns meta-dashboard dashboard.hmebuild.com
   ```

### Certificate/auth issues

1. Re-authenticate with Cloudflare:
   ```bash
   cloudflared tunnel login
   ```
2. Select `hmebuild.com` when prompted

---

## Uninstall / Cleanup

### Remove the System Service

```bash
sudo cloudflared service uninstall
```

### Delete the Tunnel

```bash
cloudflared tunnel delete meta-dashboard
```

### Remove DNS Record

This is automatic when deleting the tunnel, or manually remove it in Cloudflare DNS dashboard.

### Remove Local Config Files

```bash
rm -rf ~/.cloudflared
```

### Remove Cloudflare Access Application

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to **Access** → **Applications**
3. Delete **Meta Dashboard**

---

## Security Notes

- **No ports exposed**: The tunnel uses outbound connections only
- **End-to-end encryption**: Traffic is encrypted between Cloudflare and your Mac
- **Email OTP**: Users must verify their email before accessing
- **Session duration**: Set to 24 hours (configurable in Cloudflare Access)
- **Credentials file**: Keep `~/.cloudflared/*.json` secure (contains tunnel auth)

---

## Quick Reference

| Action | Command |
|--------|---------|
| Check tunnel status | `cloudflared tunnel info meta-dashboard` |
| View logs | `tail -f /Library/Logs/com.cloudflare.cloudflared.out.log` |
| Stop tunnel | `sudo launchctl stop com.cloudflare.cloudflared` |
| Start tunnel | `sudo launchctl start com.cloudflare.cloudflared` |
| Start Streamlit | `streamlit run app/dashboard.py` |
| Check Streamlit running | `lsof -i :8501` |
| Kill Streamlit | `pkill -f "streamlit run"` |

---

*Last updated: December 18, 2025*

