# Goalsreports API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get Goals By Campaigns Report](#get-goals-by-campaigns-report) - `GET /goalsReports/getGoalsByCampaignsReport.do`
- [Get Goals By Source Report](#get-goals-by-source-report) - `GET /goalsReports/getGoalsBySourceReport.do`
- [Get Goals By Sub Affiliates Report](#get-goals-by-sub-affiliates-report) - `GET /goalsReports/getGoalsBySubAffiliatesReport.do`

---

### Get Goals By Campaigns Report
**`GET /goalsReports/getGoalsByCampaignsReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `offerID` (integer, query)
  - `payoutModel` (string, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Goals By Source Report
**`GET /goalsReports/getGoalsBySourceReport.do`**

**Parameters:**
  - `offerID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Goals By Sub Affiliates Report
**`GET /goalsReports/getGoalsBySubAffiliatesReport.do`**

**Parameters:**
  - `offerID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---
