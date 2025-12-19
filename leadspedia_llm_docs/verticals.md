# Verticals API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Create](#create) - `POST /verticals/create.do`
- [Delete](#delete) - `POST /verticals/delete.do`
- [Get All](#get-all) - `GET /verticals/getAll.do`
- [Get Info](#get-info) - `GET /verticals/getInfo.do`
- [Update](#update) - `POST /verticals/update.do`

---

### Create
**`POST /verticals/create.do`**

**Parameters:**
  - `verticalName` (string, query) **[required]**
  - `groupID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /verticals/delete.do`**

**Parameters:**
  - `verticalID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /verticals/getAll.do`**

**Parameters:**
  - `groupID` (integer, query)
  - `status` (string, query) (options: `Active`, `InActive`)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Info
**`GET /verticals/getInfo.do`**

**Parameters:**
  - `verticalID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Update
**`POST /verticals/update.do`**

**Parameters:**
  - `verticalID` (integer, query) **[required]**
  - `groupID` (integer, query)
  - `verticalName` (string, query)
  - `notes` (string, query)

**Responses:**
  - `200`: post-response

---
