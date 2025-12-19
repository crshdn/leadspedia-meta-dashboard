# Leadsreports API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get Campaigns Leads Cap Report](#get-campaigns-leads-cap-report) - `GET /leadsReports/getCampaignsLeadsCapReport.do`
- [Get Campaigns Leads Fields Cap Report](#get-campaigns-leads-fields-cap-report) - `GET /leadsReports/getCampaignsLeadsFieldsCapReport.do`
- [Get Contracts Leads Cap Report](#get-contracts-leads-cap-report) - `GET /leadsReports/getContractsLeadsCapReport.do`
- [Get Contracts Leads Fields Cap Report](#get-contracts-leads-fields-cap-report) - `GET /leadsReports/getContractsLeadsFieldsCapReport.do`
- [Get Lead Distribution Report](#get-lead-distribution-report) - `GET /leadsReports/getLeadDistributionReport.do`
- [Get Leads By Advertisers Daily Report](#get-leads-by-advertisers-daily-report) - `GET /leadsReports/getLeadsByAdvertisersDailyReport.do`
- [Get Leads By Advertisers Report](#get-leads-by-advertisers-report) - `GET /leadsReports/getLeadsByAdvertisersReport.do`
- [Get Leads By Affiliates Daily Report](#get-leads-by-affiliates-daily-report) - `GET /leadsReports/getLeadsByAffiliatesDailyReport.do`
- [Get Leads By Affiliates Report](#get-leads-by-affiliates-report) - `GET /leadsReports/getLeadsByAffiliatesReport.do`
- [Get Leads By Campaigns Report](#get-leads-by-campaigns-report) - `GET /leadsReports/getLeadsByCampaignsReport.do`
- [Get Leads By Contracts Report](#get-leads-by-contracts-report) - `GET /leadsReports/getLeadsByContractsReport.do`
- [Get Leads By Offers Report](#get-leads-by-offers-report) - `GET /leadsReports/getLeadsByOffersReport.do`
- [Get Leads By Sub Affiliates Report](#get-leads-by-sub-affiliates-report) - `GET /leadsReports/getLeadsBySubAffiliatesReport.do`
- [Get Leads By Verticals Report](#get-leads-by-verticals-report) - `GET /leadsReports/getLeadsByVerticalsReport.do`
- [Get Offers Leads Cap Report](#get-offers-leads-cap-report) - `GET /leadsReports/getOffersLeadsCapReport.do`
- [Get Ping Post Report](#get-ping-post-report) - `GET /leadsReports/getPingPostReport.do`

---

### Get Campaigns Leads Cap Report
**`GET /leadsReports/getCampaignsLeadsCapReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)

**Responses:**
  - `200`: 

---

### Get Campaigns Leads Fields Cap Report
**`GET /leadsReports/getCampaignsLeadsFieldsCapReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)

**Responses:**
  - `200`: 

---

### Get Contracts Leads Cap Report
**`GET /leadsReports/getContractsLeadsCapReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)

**Responses:**
  - `200`: 

---

### Get Contracts Leads Fields Cap Report
**`GET /leadsReports/getContractsLeadsFieldsCapReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)

**Responses:**
  - `200`: 

---

### Get Lead Distribution Report
**`GET /leadsReports/getLeadDistributionReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `offerID` (integer, query)
  - `campaignID` (integer, query)
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

### Get Leads By Advertisers Daily Report
**`GET /leadsReports/getLeadsByAdvertisersDailyReport.do`**

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

### Get Leads By Advertisers Report
**`GET /leadsReports/getLeadsByAdvertisersReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `offerID` (integer, query)
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Leads By Affiliates Daily Report
**`GET /leadsReports/getLeadsByAffiliatesDailyReport.do`**

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

### Get Leads By Affiliates Report
**`GET /leadsReports/getLeadsByAffiliatesReport.do`**

**Parameters:**
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Leads By Campaigns Report
**`GET /leadsReports/getLeadsByCampaignsReport.do`**

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

### Get Leads By Contracts Report
**`GET /leadsReports/getLeadsByContractsReport.do`**

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

### Get Leads By Offers Report
**`GET /leadsReports/getLeadsByOffersReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)
  - `payoutModel` (string, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Leads By Sub Affiliates Report
**`GET /leadsReports/getLeadsBySubAffiliatesReport.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `affiliateAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Leads By Verticals Report
**`GET /leadsReports/getLeadsByVerticalsReport.do`**

**Parameters:**
  - `verticalGroupID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---

### Get Offers Leads Cap Report
**`GET /leadsReports/getOffersLeadsCapReport.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `verticalGroupID` (integer, query)

**Responses:**
  - `200`: 

---

### Get Ping Post Report
**`GET /leadsReports/getPingPostReport.do`**

**Parameters:**
  - `advertiserID` (integer, query)
  - `advertiserAccountManagerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)

**Responses:**
  - `200`: 

---
