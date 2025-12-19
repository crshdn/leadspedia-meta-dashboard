# Verticalgroups API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Create](#create) - `POST /verticalGroups/create.do`
- [Delete](#delete) - `POST /verticalGroups/delete.do`
- [Get All](#get-all) - `GET /verticalGroups/getAll.do`
- [Get Info](#get-info) - `GET /verticalGroups/getInfo.do`
- [Update](#update) - `POST /verticalGroups/update.do`

---

### Create
**`POST /verticalGroups/create.do`**

**Parameters:**
  - `groupName` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /verticalGroups/delete.do`**

**Parameters:**
  - `groupID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /verticalGroups/getAll.do`**

**Parameters:**
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Info
**`GET /verticalGroups/getInfo.do`**

**Parameters:**
  - `groupID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Update
**`POST /verticalGroups/update.do`**

**Parameters:**
  - `groupID` (integer, query) **[required]**
  - `groupName` (string, query)

**Responses:**
  - `200`: post-response

---
