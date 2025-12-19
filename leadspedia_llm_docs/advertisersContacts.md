# Advertiserscontacts API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Change Password](#change-password) - `POST /advertisersContacts/changePassword.do`
- [Change Status](#change-status) - `POST /advertisersContacts/changeStatus.do`
- [Create](#create) - `POST /advertisersContacts/create.do`
- [Delete](#delete) - `POST /advertisersContacts/delete.do`
- [Get All](#get-all) - `GET /advertisersContacts/getAll.do`
- [Get Info](#get-info) - `GET /advertisersContacts/getInfo.do`
- [Update](#update) - `POST /advertisersContacts/update.do`
- [Verify Credentials](#verify-credentials) - `POST /advertisersContacts/verifyCredentials.do`

---

### Change Password
**`POST /advertisersContacts/changePassword.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**
  - `oldPassword` (string, query) **[required]**
  - `newPassword` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /advertisersContacts/changeStatus.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Create
**`POST /advertisersContacts/create.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
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
**`POST /advertisersContacts/delete.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /advertisersContacts/getAll.do`**

**Parameters:**
  - `contactID` (integer, query)
  - `advertiserID` (integer, query)
  - `portalAccess` (string, query) (options: `Yes`, `No`)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Info
**`GET /advertisersContacts/getInfo.do`**

**Parameters:**
  - `contactID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Update
**`POST /advertisersContacts/update.do`**

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
**`POST /advertisersContacts/verifyCredentials.do`**

**Parameters:**
  - `emailAddress` (string, query) **[required]**
  - `password` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---
