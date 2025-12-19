# Conversionsreports API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get Conversions By Advertisers Report](#get-conversions-by-advertisers-report) - `GET /conversionsReports/getConversionsByAdvertisersReport.do`
- [Get Conversions By Affiliates Report](#get-conversions-by-affiliates-report) - `GET /conversionsReports/getConversionsByAffiliatesReport.do`
- [Get Conversions By Campaigns Report](#get-conversions-by-campaigns-report) - `GET /conversionsReports/getConversionsByCampaignsReport.do`
- [Get Conversions By Offers Report](#get-conversions-by-offers-report) - `GET /conversionsReports/getConversionsByOffersReport.do`
- [Get Conversions By Source Report](#get-conversions-by-source-report) - `GET /conversionsReports/getConversionsBySourceReport.do`
- [Get Conversions By Sub Affiliates Report](#get-conversions-by-sub-affiliates-report) - `GET /conversionsReports/getConversionsBySubAffiliatesReport.do`
- [Get Conversions By Verticals Report](#get-conversions-by-verticals-report) - `GET /conversionsReports/getConversionsByVerticalsReport.do`
- [Get Conversions Daily Report](#get-conversions-daily-report) - `GET /conversionsReports/getConversionsDailyReport.do`

---

### Get Conversions By Advertisers Report
**`GET /conversionsReports/getConversionsByAdvertisersReport.do`**

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

### Get Conversions By Affiliates Report
**`GET /conversionsReports/getConversionsByAffiliatesReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Conversions By Campaigns Report
**`GET /conversionsReports/getConversionsByCampaignsReport.do`**

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

### Get Conversions By Offers Report
**`GET /conversionsReports/getConversionsByOffersReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `payoutModel` (string, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Conversions By Source Report
**`GET /conversionsReports/getConversionsBySourceReport.do`**

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

### Get Conversions By Sub Affiliates Report
**`GET /conversionsReports/getConversionsBySubAffiliatesReport.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Conversions By Verticals Report
**`GET /conversionsReports/getConversionsByVerticalsReport.do`**

**Parameters:**
  - `verticalGroupID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Conversions Daily Report
**`GET /conversionsReports/getConversionsDailyReport.do`**

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
