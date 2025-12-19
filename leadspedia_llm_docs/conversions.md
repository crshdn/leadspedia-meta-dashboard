# Conversions API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get All](#get-all) - `GET /conversions/getAll.do`

---

### Get All
**`GET /conversions/getAll.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `offerID` (integer, query)
  - `affiliateID` (integer, query)
  - `campaignID` (integer, query)
  - `advertiserID` (integer, query)
  - `status` (string, query) (options: `Approved`, `Pending`, `Rejected`)
  - `showGoal` (string, query) (options: `Yes`, `No`)
  - `showNonGoal` (string, query) (options: `Yes`, `No`)
  - `showThrottled` (string, query) (options: `Yes`, `No`)
  - `showNonThrottled` (string, query) (options: `Yes`, `No`)
  - `showTest` (string, query) (options: `Yes`, `No`)
  - `showNonTest` (string, query) (options: `Yes`, `No`)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---
