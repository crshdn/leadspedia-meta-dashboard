# List API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get All](#get-all) - `GET /list/getAll.do`

---

### Get All
**`GET /list/getAll.do`**

**Parameters:**
  - `type` (string, query) (options: `Profanity Matches`, `Profanity Contains`, `Return Reasons`, `Return Rejected Reasons`, `Affiliate InActive`, `Affiliate Reject`, `Leads Rejected`, `Leads Accepted`, `Blacklist`, `Media Types`, `Post Responses`, `Conversions Approved`, `Conversions Rejected`, `Scrub Reasons`, `Campaign Reject`, `Pixel Reject`, `Calls Return Reasons`, `Calls Return Rejected Reasons`)
  - `advertiserID` (integer, query)
  - `verticalID` (integer, query)

**Responses:**
  - `200`: 

---
