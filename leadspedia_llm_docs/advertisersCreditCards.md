# Advertiserscreditcards API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Add](#add) - `POST /advertisersCreditCards/add.do`
- [Delete](#delete) - `POST /advertisersCreditCards/delete.do`
- [Get All](#get-all) - `GET /advertisersCreditCards/getAll.do`
- [Get Default](#get-default) - `GET /advertisersCreditCards/getDefault.do`
- [Get Info](#get-info) - `GET /advertisersCreditCards/getInfo.do`
- [Set Default](#set-default) - `POST /advertisersCreditCards/setDefault.do`
- [Update](#update) - `POST /advertisersCreditCards/update.do`
- [Update Payment Profile ID](#update-payment-profile-id) - `POST /advertisersCreditCards/updatePaymentProfileID.do`

---

### Add
**`POST /advertisersCreditCards/add.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `cardNumber` (string, query) **[required]**
  - `nameOnCard` (string, query) **[required]**
  - `expMonth` (string, query) **[required]**
  - `expYear` (string, query) **[required]**
  - `cvv` (string, query) **[required]**
  - `address` (string, query) **[required]**
  - `address2` (string, query)
  - `city` (string, query) **[required]**
  - `state` (string, query) **[required]**
  - `zipCode` (string, query) **[required]**
  - `country` (string, query) **[required]**
  - `defaultCard` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /advertisersCreditCards/delete.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `creditCardID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /advertisersCreditCards/getAll.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Default
**`GET /advertisersCreditCards/getDefault.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Info
**`GET /advertisersCreditCards/getInfo.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `creditCardID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Set Default
**`POST /advertisersCreditCards/setDefault.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `creditCardID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update
**`POST /advertisersCreditCards/update.do`**

**Parameters:**
  - `creditCardID` (integer, query) **[required]**
  - `advertiserID` (integer, query) **[required]**
  - `nameOnCard` (string, query) **[required]**
  - `expMonth` (string, query) **[required]**
  - `expYear` (string, query) **[required]**
  - `address` (string, query) **[required]**
  - `address2` (string, query)
  - `city` (string, query) **[required]**
  - `state` (string, query) **[required]**
  - `zipCode` (string, query) **[required]**
  - `country` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Payment Profile ID
**`POST /advertisersCreditCards/updatePaymentProfileID.do`**

**Parameters:**
  - `creditCardID` (integer, query) **[required]**
  - `advertiserID` (integer, query) **[required]**
  - `paymentProfileID` (string, query)
  - `expMonth` (string, query)
  - `expYear` (string, query)
  - `address` (string, query)
  - `address2` (string, query)
  - `city` (string, query)
  - `state` (string, query)
  - `zipCode` (string, query)
  - `country` (string, query)

**Responses:**
  - `200`: post-response

---
