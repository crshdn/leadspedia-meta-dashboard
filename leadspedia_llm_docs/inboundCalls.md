# Inboundcalls API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get All](#get-all) - `GET /inboundCalls/getAll.do`
- [Get Calls In Progress](#get-calls-in-progress) - `GET /inboundCalls/getInProgress.do`
- [Get Numbers](#get-numbers) - `GET /inboundCalls/getNumbers.do`
- [Get Returned Calls](#get-returned-calls) - `GET /inboundCalls/getReturned.do`
- [Get Scrubbed Calls](#get-scrubbed-calls) - `GET /inboundCalls/getScrubbed.do`
- [Get Transferred Calls](#get-transferred-calls) - `GET /inboundCalls/getTransferred.do`

---

### Get All
**`GET /inboundCalls/getAll.do`**

**Parameters:**
  - `callerID` (string, query)
  - `affiliateID` (integer, query)
  - `campaignID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `verticalID` (integer, query)
  - `offerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Calls In Progress
**`GET /inboundCalls/getInProgress.do`**

**Parameters:**
  - `callerID` (string, query)
  - `affiliateID` (integer, query)
  - `campaignID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `verticalID` (integer, query)
  - `offerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Numbers
**`GET /inboundCalls/getNumbers.do`**

**Parameters:**
  - `search` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Returned Calls
**`GET /inboundCalls/getReturned.do`**

**Parameters:**
  - `callerID` (string, query)
  - `affiliateID` (integer, query)
  - `campaignID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `verticalID` (integer, query)
  - `offerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Scrubbed Calls
**`GET /inboundCalls/getScrubbed.do`**

**Parameters:**
  - `callerID` (string, query)
  - `affiliateID` (integer, query)
  - `campaignID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `verticalID` (integer, query)
  - `offerID` (integer, query)
  - `fromDate` (string, query)
  - `toDate` (string, query) **[required]**
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Transferred Calls
**`GET /inboundCalls/getTransferred.do`**

**Parameters:**
  - `callerID` (string, query)
  - `affiliateID` (integer, query)
  - `campaignID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `verticalID` (integer, query)
  - `offerID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---
