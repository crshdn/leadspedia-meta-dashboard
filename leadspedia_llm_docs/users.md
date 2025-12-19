# Users API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Get All](#get-all) - `GET /users/getAll.do`

---

### Get All
**`GET /users/getAll.do`**

**Parameters:**
  - `role` (integer, query)
  - `status` (string, query) (options: `Active`, `InActive`)
  - `search` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---
