# Affiliatescontacts API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Change Password](#change-password) - `POST /affiliatesContacts/changePassword.do`
- [Change Status](#change-status) - `POST /affiliatesContacts/changeStatus.do`
- [Create](#create) - `POST /affiliatesContacts/create.do`
- [Delete](#delete) - `POST /affiliatesContacts/delete.do`
- [Get All](#get-all) - `GET /affiliatesContacts/getAll.do`
- [Get Info](#get-info) - `GET /affiliatesContacts/getInfo.do`
- [Update](#update) - `POST /affiliatesContacts/update.do`
- [Verify Credentials](#verify-credentials) - `POST /affiliatesContacts/verifyCredentials.do`

---

### Change Password
**`POST /affiliatesContacts/changePassword.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**
  - `oldPassword` (string, query) **[required]**
  - `newPassword` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /affiliatesContacts/changeStatus.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Create
**`POST /affiliatesContacts/create.do`**

**Parameters:**
  - `affiliateID` (integer, query) **[required]**
  - `firstName` (string, query) **[required]**
  - `lastName` (string, query) **[required]**
  - `emailAddress` (string, query) **[required]**
  - `password` (string, query) **[required]**
  - `jobTitle` (string, query)
  - `phoneNumber` (string, query)
  - `portalAccess` (string, query) (options: `Yes`, `No`)
  - `status` (string, query) (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /affiliatesContacts/delete.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /affiliatesContacts/getAll.do`**

**Parameters:**
  - `contactID` (integer, query)
  - `affiliateID` (integer, query)
  - `portalAccess` (string, query) (options: `Yes`, `No`)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Info
**`GET /affiliatesContacts/getInfo.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Update
**`POST /affiliatesContacts/update.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**
  - `firstName` (string, query)
  - `lastName` (string, query)
  - `jobTitle` (string, query)
  - `emailAddress` (string, query)
  - `phoneNumber` (string, query)
  - `officePhone` (string, query)
  - `ext` (string, query)
  - `portalAccess` (string, query) (options: `Yes`, `No`)
  - `role` (string, query)
  - `massEmail` (string, query) (options: `Yes`, `No`)
  - `permission_account` (string, query) (options: `Yes`, `No`)
  - `permission_billing` (string, query) (options: `Yes`, `No`)
  - `permission_offers` (string, query) (options: `Yes`, `No`)
  - `permission_reports` (string, query) (options: `Yes`, `No`)
  - `permission_users` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Verify Credentials
**`POST /affiliatesContacts/verifyCredentials.do`**

**Parameters:**
  - `emailAddress` (string, query) **[required]**
  - `password` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---
