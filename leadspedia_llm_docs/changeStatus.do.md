# Changestatus.Do API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Change Status](#change-status) - `POST /changeStatus.do`

---

### Change Status
**`POST /changeStatus.do`**

**Parameters:**
  - `verticalID` (integer, query) **[required]**
  - `status` (string, query) (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---
