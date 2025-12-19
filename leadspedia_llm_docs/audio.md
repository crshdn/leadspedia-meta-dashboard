# Audio API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Delete](#delete) - `POST /audio/delete.do`
- [Get All](#get-all) - `GET /audio/getAll.do`

---

### Delete
**`POST /audio/delete.do`**

**Parameters:**
  - `audioID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /audio/getAll.do`**

**Parameters:**
  - `audioID` (integer, query)
  - `audioType` (string, query) (options: `General`, `Hold Music`)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---
