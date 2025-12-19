# Changelog

All notable changes to the Meta Lead Ads Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.1] - 2025-12-19

### Changed
- Support multiple email recipients for alerts (comma-separated)

### Removed
- Debug logging and status displays from dashboard UI
- All `[DEBUG]` print statements from Leadspedia modules
- Config details display in sidebar

---

## [1.0.0] - 2025-12-18

### Added
- **Core Dashboard**: Streamlit-based dashboard for Meta Lead Ads reporting
- **Meta Graph API Integration**: Pull Lead Ads performance data at ad/creative level
- **Leadspedia Integration**: Revenue tracking and ROI calculation via Leadspedia API
- **CPL Analysis**: Cost-per-lead calculations with statistical confidence scoring
- **Revenue & ROI Analysis**: Combined spend/revenue profitability metrics
- **Statistical Significance**: Data requirements visualization for reliable decisions
- **Performance Breakdowns**: Age/Gender, Placement, Device breakdowns
- **Alerting System**: Real-time monitoring with configurable thresholds
  - Email notifications (SMTP) with support for multiple comma-separated recipients
  - Slack webhook integration
  - Per-vertical threshold configuration
- **Export Options**:
  - CSV download
  - Google Sheets integration (service account)
  - LLM-optimized markdown export for AI analysis
- **SQLite Caching**: Local cache layer to reduce API calls
- **Leadspedia LLM Documentation**: Complete API reference for AI assistants (`leadspedia_llm_docs/`)
- **Secure Remote Access**: Documentation for Cloudflare Tunnel setup with Access authentication

### Security
- Environment-based configuration (`.env` file not tracked)
- Example config with placeholder values only
- Permission checks for sensitive files
- Dashboard warns on insecure `.env` permissions

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.1 | 2025-12-19 | Multi-email support, remove debug logging |
| 1.0.0 | 2025-12-18 | Initial public release |

---

## Migration Notes

### From Pre-1.0 to 1.0.0
This is the initial release. No migration needed.

---

## Links

- [GitHub Repository](https://github.com/crshdn/leadspedia-meta-dashboard)
- [Meta Marketing API Docs](https://developers.facebook.com/docs/marketing-api/)
- [Leadspedia API Docs](https://api.leadspedia.com/core/v2/)

