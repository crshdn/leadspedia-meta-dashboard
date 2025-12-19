## Meta Lead Ads Dashboard (Local)

Local Streamlit dashboard + export tool powered by Meta's Marketing API ([docs](https://developers.facebook.com/docs/marketing-api/)) with optional Leadspedia integration for revenue tracking.

### What it does
- Pulls **Lead Ads** performance and computes **CPL** at the **ad/creative** level
- Breakdowns:
  - Age/Gender
  - Placement (publisher + position)
  - Device
- **Leadspedia Integration** (optional):
  - Revenue tracking and ROI calculation
  - Sell-through rate, unsold leads, avg sale price
  - Combined profitability KPIs
- **Alerting System** (optional):
  - Real-time monitoring for performance issues
  - Email and Slack notifications
  - Configurable thresholds per vertical
- Exports:
  - CSV download
  - Optional push to Google Sheets

### Setup (safe defaults)
1. Install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a local `.env` (not committed) **with tight permissions**:

```bash
cd "/Users/chris/Library/CloudStorage/SynologyDrive-Sync/Sites/meta-ads-api"
touch .env
chmod 600 .env
```

3. Copy variables from `config.example.env.txt` into `.env` and fill in:
- `META_AD_ACCOUNT_ID` (like `act_...`)
- `META_ACCESS_TOKEN`

### Leadspedia Integration (Optional)

To enable revenue tracking via Leadspedia:

1. Get your API credentials from Leadspedia:
   - API Key: Settings > System Settings > Security
   - API Secret: Settings > Users > [Your User] > API Settings

2. Add to your `.env`:
```bash
LEADSPEDIA_API_KEY=your_api_key
LEADSPEDIA_API_SECRET=your_api_secret
```

3. Configure campaign mappings (JSON format):
```bash
LEADSPEDIA_CAMPAIGN_MAP={"120210123456789012": {"affiliate_id": "123", "vertical": "auto"}}
```

### Alerting (Optional)

Enable alerts by configuring one or more channels:

**Email:**
```bash
ALERT_EMAIL_ENABLED=true
ALERT_EMAIL_TO=alerts@yourcompany.com
ALERT_EMAIL_FROM=noreply@yourcompany.com
ALERT_SMTP_HOST=smtp.gmail.com
ALERT_SMTP_PORT=587
ALERT_SMTP_USER=your_user
ALERT_SMTP_PASSWORD=your_password
```

**Slack:**
```bash
ALERT_SLACK_ENABLED=true
ALERT_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

**Thresholds:**
```bash
ALERT_THRESHOLDS={"default": {"min_sell_rate": 95, "min_roi": 20}, "auto": {"min_sell_rate": 90}}
```

### Run

```bash
source .venv/bin/activate
streamlit run app/dashboard.py
```

### Security notes
- Never commit tokens or Google credentials.
- If you enable Google Sheets export with a service account JSON file, keep it in `.secrets/` and restrict permissions:

```bash
mkdir -p .secrets
chmod 700 .secrets
chmod 600 .secrets/google_service_account.json
```


