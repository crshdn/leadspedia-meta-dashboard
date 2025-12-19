# Reports API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get Advertisers Report](#get-advertisers-report) - `GET /reports/getAdvertisersReport.do`
- [Get Affiliates Report](#get-affiliates-report) - `GET /reports/getAffiliatesReport.do`
- [Get Campaigns Report](#get-campaigns-report) - `GET /reports/getCampaignsReport.do`
- [Get Offers Report](#get-offers-report) - `GET /reports/getOffersReport.do`
- [Get Verticals Report](#get-verticals-report) - `GET /reports/getVerticalsReport.do`

---

### Get Advertisers Report
**`GET /reports/getAdvertisersReport.do`**

**Parameters:**
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Affiliates Report
**`GET /reports/getAffiliatesReport.do`**

**Parameters:**
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Campaigns Report
**`GET /reports/getCampaignsReport.do`**

**Parameters:**
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Offers Report
**`GET /reports/getOffersReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Verticals Report
**`GET /reports/getVerticalsReport.do`**

**Parameters:**
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---
