# Offers API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Change Auto Approval](#change-auto-approval) - `POST /offers/changeAutoApproval.do`
- [Change Feature Listing](#change-feature-listing) - `POST /offers/changeFeatureListing.do`
- [Change Mode](#change-mode) - `POST /offers/changeMode.do`
- [Change Status](#change-status) - `POST /offers/changeStatus.do`
- [Delete](#delete) - `POST /offers/delete.do`
- [Get All](#get-all) - `GET /offers/getAll.do`
- [Get Basic Info](#get-basic-info) - `GET /offers/getBasicInfo.do`
- [Get Email Settings](#get-email-settings) - `GET /offers/getEmailSettings.do`
- [Get Terms Settings](#get-terms-settings) - `GET /offers/getTermsSettings.do`
- [Remove Expiration Date](#remove-expiration-date) - `POST /offers/removeExpirationDate.do`
- [Rename](#rename) - `POST /offers/rename.do`
- [Search](#search) - `GET /offers/search.do`
- [Set Expiration Date](#set-expiration-date) - `POST /offers/setExpirationDate.do`
- [Update Basic Info](#update-basic-info) - `POST /offers/updateBasicInfo.do`
- [Update Email Settings](#update-email-settings) - `POST /offers/updateEmailSettings.do`
- [Update Terms Settings](#update-terms-settings) - `POST /offers/updateTermsSettings.do`
- [Update Visibility](#update-visibility) - `POST /offers/updateVisibility.do`

---

### Change Auto Approval
**`POST /offers/changeAutoApproval.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `autoApprove` (string, query) **[required]** (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Change Feature Listing
**`POST /offers/changeFeatureListing.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `feature` (string, query) **[required]** (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Change Mode
**`POST /offers/changeMode.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `mode` (string, query) **[required]** (options: `Setup`, `Test`, `Live`)

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /offers/changeStatus.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /offers/delete.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /offers/getAll.do`**

**Parameters:**
  - `verticalID` (integer, query)
  - `revenueModel` (string, query) (options: `Revenue Per Lead`, `Revenue Per Call`)
  - `payoutModel` (string, query)
  - `advertiserID` (integer, query)
  - `status` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Basic Info
**`GET /offers/getBasicInfo.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Email Settings
**`GET /offers/getEmailSettings.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Terms Settings
**`GET /offers/getTermsSettings.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Remove Expiration Date
**`POST /offers/removeExpirationDate.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Rename
**`POST /offers/rename.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `offerName` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Search
**`GET /offers/search.do`**

**Parameters:**
  - `name` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Set Expiration Date
**`POST /offers/setExpirationDate.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `expirationDate` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Basic Info
**`POST /offers/updateBasicInfo.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `offerName` (string, query)
  - `notes` (string, query)
  - `alternativeID` (string, query)
  - `previewURL` (string, query)
  - `offerDescription` (string, query)
  - `testingInstructions` (string, query)
  - `offerRestrictions` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Email Settings
**`POST /offers/updateEmailSettings.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `testEmail` (string, query)
  - `allowedEmails` (string, query)
  - `allowedSubjects` (string, query)
  - `emailInstructions` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Terms Settings
**`POST /offers/updateTermsSettings.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `terms` (string, query)
  - `termsEnabled` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Visibility
**`POST /offers/updateVisibility.do`**

**Parameters:**
  - `offerID` (integer, query) **[required]**
  - `visibility` (string, query) **[required]** (options: `Public`, `Private`, `Hidden`)

**Responses:**
  - `200`: post-response

---
