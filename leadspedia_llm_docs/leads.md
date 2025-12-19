# Leads API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Approve Return](#approve-return) - `POST /leads/approveReturn.do`
- [Get All](#get-all) - `GET /leads/getAll.do`
- [Get Delivered](#get-delivered) - `GET /leads/getDelivered.do`
- [Get Lead Data](#get-lead-data) - `GET /leads/getLeadData.do`
- [Get Lead Info](#get-lead-info) - `GET /leads/getLeadInfo.do`
- [Get Queue](#get-queue) - `GET /leads/getQueue.do`
- [Get Returns](#get-returns) - `GET /leads/getReturns.do`
- [Get Review](#get-review) - `GET /leads/getReview.do`
- [Get Scrubbed](#get-scrubbed) - `GET /leads/getScrubbed.do`
- [Get Sold](#get-sold) - `GET /leads/getSold.do`
- [Get Trash](#get-trash) - `GET /leads/getTrash.do`
- [Reject Return](#reject-return) - `POST /leads/rejectReturn.do`
- [Request Return](#request-return) - `POST /leads/requestReturn.do`
- [Return Lead](#return-lead) - `POST /leads/returnLead.do`
- [Return Lead From All Contracts](#return-lead-from-all-contracts) - `POST /leads/returnLeadFromAllContracts.do`
- [Review Approve](#review-approve) - `POST /leads/reviewApprove.do`
- [Review Reject](#review-reject) - `POST /leads/reviewReject.do`
- [Scrub Lead](#scrub-lead) - `POST /leads/scrubLead.do`
- [Unreturn Lead](#unreturn-lead) - `POST /leads/unreturnLead.do`
- [Update Lead](#update-lead) - `POST /leads/updateLead.do`

---

### Approve Return
**`POST /leads/approveReturn.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /leads/getAll.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `paid` (string, query) (options: `Yes`, `No`)
  - `scrubbed` (string, query) (options: `Yes`, `No`)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Delivered
**`GET /leads/getDelivered.do`**

**Parameters:**
  - `leadID` (string, query)
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `returned` (string, query) (options: `Yes`, `No`)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Lead Data
**`GET /leads/getLeadData.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Lead Info
**`GET /leads/getLeadInfo.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Queue
**`GET /leads/getQueue.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Returns
**`GET /leads/getReturns.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `status` (string, query) (options: `Pending`, `Approved`, `Rejected`, `Attempted Contact`, `Researching`)
  - `returnReasonID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Review
**`GET /leads/getReview.do`**

**Parameters:**
  - `leadID` (string, query)
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Scrubbed
**`GET /leads/getScrubbed.do`**

**Parameters:**
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Sold
**`GET /leads/getSold.do`**

**Parameters:**
  - `leadID` (string, query)
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `returned` (string, query) (options: `Yes`, `No`)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Trash
**`GET /leads/getTrash.do`**

**Parameters:**
  - `leadID` (string, query)
  - `campaignID` (integer, query)
  - `affiliateID` (integer, query)
  - `verticalID` (integer, query)
  - `fromDate` (string, query) **[required]**
  - `toDate` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Reject Return
**`POST /leads/rejectReturn.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `contractID` (integer, query) **[required]**
  - `rejectReasonID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Request Return
**`POST /leads/requestReturn.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `contractID` (integer, query) **[required]**
  - `returnReasonID` (integer, query) **[required]**
  - `returnNotes` (string, query)

**Responses:**
  - `200`: post-response

---

### Return Lead
**`POST /leads/returnLead.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `contractID` (integer, query) **[required]**
  - `returnReasonID` (integer, query) **[required]**
  - `scrub` (string, query) (options: `Yes`, `No`)
  - `replaceReturns` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Return Lead From All Contracts
**`POST /leads/returnLeadFromAllContracts.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `returnReasonID` (integer, query) **[required]**
  - `scrub` (string, query) (options: `Yes`, `No`)
  - `replaceReturns` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Review Approve
**`POST /leads/reviewApprove.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `leadAcceptReasonID` (integer, query) **[required]**
  - `leadAcceptReason` (string, query)

**Responses:**
  - `200`: post-response

---

### Review Reject
**`POST /leads/reviewReject.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `leadRejectReasonID` (integer, query) **[required]**
  - `leadRejectReason` (string, query)

**Responses:**
  - `200`: post-response

---

### Scrub Lead
**`POST /leads/scrubLead.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `scrubReasonID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Unreturn Lead
**`POST /leads/unreturnLead.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**
  - `contractID` (integer, query) **[required]**
  - `rejectReasonID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Lead
**`POST /leads/updateLead.do`**

**Parameters:**
  - `leadID` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---
