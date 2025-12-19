# Campaigns API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Assign Tracking Number](#assign-tracking-number) - `POST /campaigns/assignTrackingNumber.do`
- [Change Goals Static Throttle](#change-goals-static-throttle) - `POST /campaigns/changeGoalsStaticThrottle.do`
- [Change Mode](#change-mode) - `POST /campaigns/changeMode.do`
- [Change Offer Static Throttle](#change-offer-static-throttle) - `POST /campaigns/changeOfferStaticThrottle.do`
- [Change Status](#change-status) - `POST /campaigns/changeStatus.do`
- [Delete](#delete) - `POST /campaigns/delete.do`
- [Get All](#get-all) - `GET /campaigns/getAll.do`
- [Get Basic Info](#get-basic-info) - `GET /campaigns/getBasicInfo.do`
- [Get Goals Static Throtte](#get-goals-static-throtte) - `GET /campaigns/getGoalsStaticThrottle.do`
- [Get Offer Static Throtte](#get-offer-static-throtte) - `GET /campaigns/getOfferStaticThrottle.do`
- [Get Post Keys](#get-post-keys) - `GET /campaigns/getPostKeys.do`
- [Remove Expiration Date](#remove-expiration-date) - `POST /campaigns/removeExpirationDate.do`
- [Rename](#rename) - `POST /campaigns/rename.do`
- [Set Expiration Date](#set-expiration-date) - `POST /campaigns/setExpirationDate.do`
- [Unassign Tracking Number](#unassign-tracking-number) - `POST /campaigns/unassignTrackingNumber.do`
- [Update Basic Info](#update-basic-info) - `POST /campaigns/updateBasicInfo.do`
- [Update Clicks Revenue](#update-clicks-revenue) - `POST /campaigns/updateClicksRevenue.do`

---

### Assign Tracking Number
**`POST /campaigns/assignTrackingNumber.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `number` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Change Goals Static Throttle
**`POST /campaigns/changeGoalsStaticThrottle.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `goalsStaticThrottle` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Change Mode
**`POST /campaigns/changeMode.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `mode` (string, query) **[required]** (options: `Setup`, `Test`, `Live`)

**Responses:**
  - `200`: post-response

---

### Change Offer Static Throttle
**`POST /campaigns/changeOfferStaticThrottle.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `offerStaticThrottle` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /campaigns/changeStatus.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /campaigns/delete.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /campaigns/getAll.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `offerID` (integer, query)
  - `verticalID` (integer, query)
  - `status` (string, query) (options: `Active`, `InActive`, `Pending`)
  - `search` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Basic Info
**`GET /campaigns/getBasicInfo.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Goals Static Throtte
**`GET /campaigns/getGoalsStaticThrottle.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Offer Static Throtte
**`GET /campaigns/getOfferStaticThrottle.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Post Keys
**`GET /campaigns/getPostKeys.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Remove Expiration Date
**`POST /campaigns/removeExpirationDate.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Rename
**`POST /campaigns/rename.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `campaignName` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Set Expiration Date
**`POST /campaigns/setExpirationDate.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `expirationDate` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Unassign Tracking Number
**`POST /campaigns/unassignTrackingNumber.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `number` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Basic Info
**`POST /campaigns/updateBasicInfo.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `campaignName` (string, query)
  - `notes` (string, query)
  - `alternativeID` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Clicks Revenue
**`POST /campaigns/updateClicksRevenue.do`**

**Parameters:**
  - `campaignID` (integer, query) **[required]**
  - `startDate` (string, query) **[required]**
  - `endDate` (string, query) **[required]**
  - `revenue` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---
