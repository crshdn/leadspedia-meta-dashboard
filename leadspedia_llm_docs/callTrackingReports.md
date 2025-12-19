# Calltrackingreports API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get Call Routing Report](#get-call-routing-report) - `GET /callTrackingReports/getCallRoutingReport.do`
- [Get Calls By Advertisers Daily Report](#get-calls-by-advertisers-daily-report) - `GET /callTrackingReports/getCallsByAdvertisersDailyReport.do`
- [Get Calls By Advertisers Report](#get-calls-by-advertisers-report) - `GET /callTrackingReports/getCallsByAdvertisersReport.do`
- [Get Calls By Affiliates Daily Report](#get-calls-by-affiliates-daily-report) - `GET /callTrackingReports/getCallsByAffiliatesDailyReport.do`
- [Get Calls By Affiliates Report](#get-calls-by-affiliates-report) - `GET /callTrackingReports/getCallsByAffiliatesReport.do`
- [Get Calls By Campaigns Report](#get-calls-by-campaigns-report) - `GET /callTrackingReports/getCallsByCampaignsReport.do`
- [Get Calls By Contracts Report](#get-calls-by-contracts-report) - `GET /callTrackingReports/getCallsByContractsReport.do`
- [Get Calls By Offers Report](#get-calls-by-offers-report) - `GET /callTrackingReports/getCallsByOffersReport.do`
- [Get Calls By Sub Affiliates Report](#get-calls-by-sub-affiliates-report) - `GET /callTrackingReports/getCallsBySubAffiliatesReport.do`
- [Get Calls By Verticals Report](#get-calls-by-verticals-report) - `GET /callTrackingReports/getCallsByVerticalsReport.do`

---

### Get Call Routing Report
**`GET /callTrackingReports/getCallRoutingReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Advertisers Daily Report
**`GET /callTrackingReports/getCallsByAdvertisersDailyReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `contractID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `month` (string, query) **[required]**
  - `year` (string, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Calls By Advertisers Report
**`GET /callTrackingReports/getCallsByAdvertisersReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `offerID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Affiliates Daily Report
**`GET /callTrackingReports/getCallsByAffiliatesDailyReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `offerID` (integer, query)
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `month` (string, query) **[required]**
  - `year` (string, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Calls By Affiliates Report
**`GET /callTrackingReports/getCallsByAffiliatesReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Campaigns Report
**`GET /callTrackingReports/getCallsByCampaignsReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `offerID` (integer, query)
  - `payoutModel` (string, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Contracts Report
**`GET /callTrackingReports/getCallsByContractsReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Offers Report
**`GET /callTrackingReports/getCallsByOffersReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `payoutModel` (string, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Sub Affiliates Report
**`GET /callTrackingReports/getCallsBySubAffiliatesReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Calls By Verticals Report
**`GET /callTrackingReports/getCallsByVerticalsReport.do`**

**Parameters:**
  - `verticalGroupID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---
