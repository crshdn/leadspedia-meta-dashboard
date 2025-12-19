# Meta Lead Ads Dashboard

A local Streamlit dashboard for Meta (Facebook) Lead Ads reporting with Leadspedia integration for revenue tracking and ROI analysis.

## Features

### Core Analytics
- **Lead Ads Performance**: Pull performance data at the ad/creative level
- **CPL (Cost Per Lead)**: Calculate and track cost per lead across campaigns
- **Breakdowns**: Age/Gender, Placement (publisher + position), Device

### Leadspedia Integration (Optional)
- **Revenue Tracking**: Match Meta leads to Leadspedia conversions
- **ROI Calculation**: Real-time return on investment metrics
- **Sell-through Rate**: Track sold vs. unsold leads
- **Profitability KPIs**: Combined Meta spend + Leadspedia revenue analysis

### Alerting System (Optional)
- **Real-time Monitoring**: Automatic alerts for performance issues
- **Email Notifications**: SMTP-based email alerts
- **Slack Integration**: Webhook-based Slack notifications
- **Configurable Thresholds**: Per-vertical threshold settings

### Export Options
- **CSV Download**: Export data for external analysis
- **Google Sheets**: Push data directly to Google Sheets (service account)

---

## Screenshots

### CPL Analysis
Creative performance ranking with statistical confidence indicators. Ads are categorized as Scale (green), Maintain (yellow), Kill (red), or Needs Data based on CPL performance and data volume.

![CPL Analysis](dashboard_examples/CPL%20Analysis.png)

### Revenue & ROI Analysis
Combined Meta Ads spend with Leadspedia revenue data for profitability analysis. View profit/loss, ROI percentage, sell-through rates, and break-even CPL at the campaign, adset, and ad level.

![Revenue & ROI](dashboard_examples/Revenue%20%26%20ROI.png)

### Statistical Significance
Data requirements visualization showing how many more leads (and spend) each ad needs to reach 95% statistical confidence. Helps prevent premature optimization decisions.

![Statistical Significance](dashboard_examples/Statistical%20Significance.png)

### LLM Analysis Export
Export your performance data in a markdown format optimized for AI assistants like Claude or ChatGPT. Filter by minimum spend and select top/bottom performers for analysis.

![LLM Analysis Export](dashboard_examples/LLM%20Analysis.png)

---

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/your-username/meta-ads-api.git
cd meta-ads-api

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with secure permissions:

```bash
touch .env
chmod 600 .env
```

Copy settings from `config.example.env.txt` and fill in your values:

```bash
# Required - Meta API
META_AD_ACCOUNT_ID=act_XXXXXXXXXXXXX
META_ACCESS_TOKEN=your_meta_access_token

# Optional - Leadspedia Integration
LEADSPEDIA_API_KEY=your_api_key
LEADSPEDIA_API_SECRET=your_api_secret
```

### 3. Run the Dashboard

```bash
source .venv/bin/activate
streamlit run app/dashboard.py
```

The dashboard will be available at `http://localhost:8501`

---

## Configuration Reference

### Meta API (Required)

| Variable | Description |
|----------|-------------|
| `META_AD_ACCOUNT_ID` | Your Meta ad account ID (format: `act_...`) |
| `META_ACCESS_TOKEN` | Meta Marketing API access token |

Get your access token from [Meta for Developers](https://developers.facebook.com/tools/explorer/).

### Leadspedia Integration (Optional)

| Variable | Description |
|----------|-------------|
| `LEADSPEDIA_API_KEY` | API key from Leadspedia (Settings → System Settings → Security) |
| `LEADSPEDIA_API_SECRET` | API secret from Leadspedia (Settings → Users → [Your User] → API Settings) |
| `LEADSPEDIA_CAMPAIGN_MAP` | JSON mapping of Meta campaign IDs to Leadspedia affiliates |

**Campaign Mapping Example:**

```bash
LEADSPEDIA_CAMPAIGN_MAP={"120210123456789012": {"affiliate_id": "123", "vertical": "auto"}}
```

### Alerting (Optional)

**Email Alerts:**

| Variable | Description |
|----------|-------------|
| `ALERT_EMAIL_ENABLED` | Set to `true` to enable |
| `ALERT_EMAIL_TO` | Recipient email address(es), comma-separated for multiple |
| `ALERT_EMAIL_FROM` | Sender email address |
| `ALERT_SMTP_HOST` | SMTP server hostname |
| `ALERT_SMTP_PORT` | SMTP port (typically 587 for TLS) |
| `ALERT_SMTP_USER` | SMTP username |
| `ALERT_SMTP_PASSWORD` | SMTP password |

**Slack Alerts:**

| Variable | Description |
|----------|-------------|
| `ALERT_SLACK_ENABLED` | Set to `true` to enable |
| `ALERT_SLACK_WEBHOOK_URL` | Slack incoming webhook URL |

**Alert Thresholds:**

```bash
ALERT_THRESHOLDS={"default": {"min_sell_rate": 95, "min_roi": 20}, "auto": {"min_sell_rate": 90}}
```

### Google Sheets Export (Optional)

| Variable | Description |
|----------|-------------|
| `GOOGLE_SHEETS_ENABLED` | Set to `true` to enable |
| `GOOGLE_SERVICE_ACCOUNT_JSON_PATH` | Path to service account JSON file |
| `GOOGLE_SHEET_ID` | Target Google Sheet ID |

---

## Project Structure

```
meta-ads-api/
├── app/
│   ├── alerts/           # Alert monitoring and notification channels
│   ├── analysis/         # Data analysis and LLM export utilities
│   ├── cache/            # SQLite caching layer
│   ├── export/           # CSV and Google Sheets export
│   ├── leadspedia/       # Leadspedia API client and matching logic
│   ├── meta/             # Meta Graph API client and insights
│   ├── metrics/          # CPL and revenue calculations
│   ├── pages/            # Additional Streamlit pages
│   ├── config.py         # Configuration management
│   ├── config_manager.py # Campaign configuration UI
│   └── dashboard.py      # Main Streamlit application
├── leadspedia_llm_docs/  # Complete Leadspedia API documentation for LLMs
├── config.example.env.txt
├── requirements.txt
└── README.md
```

---

## Leadspedia API Documentation for LLMs

This repository includes comprehensive Leadspedia API documentation in `leadspedia_llm_docs/` designed specifically for use with Large Language Models (LLMs).

### What's Included

- **Complete API Reference**: All endpoints with parameters, types, and examples
- **Quick Reference Guide**: Common operations and endpoint lookup
- **Organized by Resource**: Leads, campaigns, affiliates, advertisers, reports, etc.

### Using with LLMs

The documentation is formatted for easy consumption by AI assistants:

```
leadspedia_llm_docs/
├── INDEX.md              # Overview and authentication guide
├── QUICK_REFERENCE.md    # Fast endpoint lookup table
├── leads.md              # Leads API endpoints
├── leadsReports.md       # Lead reporting endpoints
├── campaigns.md          # Campaign management
├── affiliates.md         # Affiliate management
├── advertisers.md        # Advertiser management
├── conversions.md        # Conversion tracking
├── offers.md             # Offer management
└── ... (20+ resource files)
```

### Example LLM Prompt

```
I'm building an integration with Leadspedia. Using the documentation in 
leadspedia_llm_docs/, help me write code to:
1. Fetch all leads for a date range
2. Get conversion data for those leads
3. Calculate revenue by affiliate
```

---

## Remote Access (Optional)

For secure remote access without exposing ports, we recommend **Cloudflare Tunnel**:

1. Install cloudflared: `brew install cloudflare/cloudflare/cloudflared`
2. Authenticate: `cloudflared tunnel login`
3. Create tunnel: `cloudflared tunnel create my-dashboard`
4. Configure routing to `localhost:8501`
5. Add **Cloudflare Access** for authentication (email OTP, SSO, etc.)

Benefits:
- No ports exposed on your network
- End-to-end encryption
- Built-in authentication
- Free tier available

See [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) for details.

---

## Security Best Practices

### Credentials

- **Never commit `.env`** - It's in `.gitignore` by default
- **Use `chmod 600`** on `.env` and any credential files
- **Rotate tokens regularly** - Especially Meta access tokens

### Google Sheets Service Account

If using Google Sheets export:

```bash
mkdir -p .secrets
chmod 700 .secrets
mv your-service-account.json .secrets/google_service_account.json
chmod 600 .secrets/google_service_account.json
```

### File Permissions

The dashboard will warn you if `.env` permissions are too open.

---

## API References

- [Meta Marketing API](https://developers.facebook.com/docs/marketing-api/)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Leadspedia API](https://api.leadspedia.com/core/v2/) (see `leadspedia_llm_docs/` for complete reference)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## Requirements

- Python 3.10+
- Meta Marketing API access
- Leadspedia account (optional, for revenue tracking)

### Python Dependencies

```
streamlit>=1.37,<2
pandas>=2.2,<3
requests>=2.32,<3
python-dotenv>=1.0,<2
tenacity>=9.0,<10
gspread>=6.1,<7        # Optional: Google Sheets
google-auth>=2.35,<3   # Optional: Google Sheets
```

---

## License

MIT License - See LICENSE file for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
