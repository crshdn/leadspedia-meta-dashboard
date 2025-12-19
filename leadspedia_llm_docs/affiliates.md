# Affiliates API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Change Status](#change-status) - `POST /affiliates/changeStatus.do`
- [Create](#create) - `POST /affiliates/create.do`
- [Delete](#delete) - `POST /affiliates/delete.do`
- [Get All](#get-all) - `GET /affiliates/getAll.do`
- [Get Info](#get-info) - `GET /affiliates/getInfo.do`
- [Search](#search) - `GET /affiliates/search.do`
- [Update Billing](#update-billing) - `POST /affiliates/updateBilling.do`
- [Update Info](#update-info) - `POST /affiliates/updateInfo.do`

---

### Change Status
**`POST /affiliates/changeStatus.do`**

**Parameters:**
  - `affiliateID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `Pending`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Create
**`POST /affiliates/create.do`**

**Parameters:**
  - `affiliateName` (string, query) **[required]**
  - `accountManagerID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `Pending`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /affiliates/delete.do`**

**Parameters:**
  - `affiliateID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /affiliates/getAll.do`**

**Parameters:**
  - `affiliateID` (integer, query)
  - `accountManagerID` (integer, query)
  - `status` (string, query) (options: `Active`, `Pending`, `InActive`)
  - `search` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Info
**`GET /affiliates/getInfo.do`**

**Parameters:**
  - `affiliateID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Search
**`GET /affiliates/search.do`**

**Parameters:**
  - `search` (string, query) **[required]**
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Update Billing
**`POST /affiliates/updateBilling.do`**

**Parameters:**
  - `affiliateID` (integer, query) **[required]**
  - `billingCycle` (string, query) (options: `Monthly`, `BiMonthly`, `Weekly`, `Two Months`, `Quarterly`, `Manual`, `Other`)
  - `taxID` (string, query)
  - `taxClass` (string, query)
  - `tax_doc_received` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Info
**`POST /affiliates/updateInfo.do`**

**Parameters:**
  - `affiliateID` (integer, query) **[required]**
  - `affiliateName` (string, query)
  - `website` (string, query)
  - `alternateID` (string, query)
  - `address` (string, query)
  - `address2` (string, query)
  - `city` (string, query)
  - `state` (string, query)
  - `zipCode` (string, query)
  - `country` (string, query)
  - `reportingUrl` (string, query)
  - `reportingUsername` (string, query)
  - `reportingPassword` (string, query)

**Responses:**
  - `200`: post-response

---
