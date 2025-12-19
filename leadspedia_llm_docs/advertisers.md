# Advertisers API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Adjust Credit](#adjust-credit) - `POST /advertisers/adjustCredit.do`
- [Change Status](#change-status) - `POST /advertisers/changeStatus.do`
- [Create](#create) - `POST /advertisers/create.do`
- [Delete](#delete) - `POST /advertisers/delete.do`
- [Enable Credit](#enable-credit) - `POST /advertisers/enableCredit.do`
- [Get All](#get-all) - `GET /advertisers/getAll.do`
- [Get Info](#get-info) - `GET /advertisers/getInfo.do`
- [Search](#search) - `GET /advertisers/search.do`
- [Update Authorize Net Customer Profile ID](#update-authorize-net-customer-profile-id) - `POST /advertisers/updateAuthorizeNetCustomerProfileID.do`
- [Update Auto Recharge Settings](#update-auto-recharge-settings) - `POST /advertisers/updateAutoRechargeSettings.do`
- [Update Billing](#update-billing) - `POST /advertisers/updateBilling.do`
- [Update Info](#update-info) - `POST /advertisers/updateInfo.do`
- [Update Leads Caps](#update-leads-caps) - `POST /advertisers/updateLeadsCaps.do`
- [Update Leads Daily Cap](#update-leads-daily-cap) - `POST /advertisers/updateLeadsDailyCap.do`
- [Update Leads Daily Revenue Cap](#update-leads-daily-revenue-cap) - `POST /advertisers/updateLeadsDailyRevenueCap.do`
- [Update Leads Monthly Cap](#update-leads-monthly-cap) - `POST /advertisers/updateLeadsMonthlyCap.do`
- [Update Leads Monthly Revenue Cap](#update-leads-monthly-revenue-cap) - `POST /advertisers/updateLeadsMonthlyRevenueCap.do`
- [Update Leads Revenue Caps](#update-leads-revenue-caps) - `POST /advertisers/updateLeadsRevenueCaps.do`
- [Update Leads Weekly Cap](#update-leads-weekly-cap) - `POST /advertisers/updateLeadsWeeklyCap.do`
- [Update Leads Weekly Revenue Cap](#update-leads-weekly-revenue-cap) - `POST /advertisers/updateLeadsWeeklyRevenueCap.do`
- [Update Portal Settings](#update-portal-settings) - `POST /advertisers/updatePortalSettings.do`

---

### Adjust Credit
**`POST /advertisers/adjustCredit.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `type` (string, query) **[required]** (options: `Credit`, `Debit`)
  - `amount` (number, query) **[required]**
  - `charge` (string, query) (options: `Yes`, `No`)
  - `generateInvoice` (string, query) (options: `Yes`, `No`)
  - `note` (string, query)
  - `transactionFee` (string, query) (options: `Yes`, `No`)
  - `transactionFeePercentage` (number, query)
  - `transactionFeeAmount` (number, query)

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /advertisers/changeStatus.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Create
**`POST /advertisers/create.do`**

**Parameters:**
  - `advertiserName` (string, query) **[required]**
  - `accountManagerID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /advertisers/delete.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Enable Credit
**`POST /advertisers/enableCredit.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /advertisers/getAll.do`**

**Parameters:**
  - `advertiserID` (integer, query)
  - `advertiserType` (string, query) (options: `Corporate`, `Individual`)
  - `accountManagerID` (integer, query)
  - `status` (string, query) (options: `Active`, `InActive`, `Prospect`, `Paused`, `Suspended`, `Pending InActive`)
  - `isCreditEnabled` (string, query) (options: `Yes`, `No`)
  - `hasCreditCardOnFile` (string, query) (options: `Yes`, `No`)
  - `search` (string, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Info
**`GET /advertisers/getInfo.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Search
**`GET /advertisers/search.do`**

**Parameters:**
  - `search` (string, query) **[required]**
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Update Authorize Net Customer Profile ID
**`POST /advertisers/updateAuthorizeNetCustomerProfileID.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `authNetCustomerProfileID` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Auto Recharge Settings
**`POST /advertisers/updateAutoRechargeSettings.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `enableAutoRecharge` (string, query) (options: `Yes`, `No`)
  - `autoChargeBalance` (number, query)
  - `autoChargeAmount` (number, query)
  - `chargeTransactionFee` (string, query) (options: `Yes`, `No`)
  - `transactionFeePercentage` (number, query)
  - `transactionFeeAmount` (number, query)
  - `generateInvoice` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Billing
**`POST /advertisers/updateBilling.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `billingCycle` (string, query) (options: `Monthly`, `BiMonthly`, `Weekly`, `Two Months`, `Quarterly`, `Manual`, `Other`)
  - `taxID` (string, query)
  - `taxClass` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Info
**`POST /advertisers/updateInfo.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `advertiserName` (string, query)
  - `website` (string, query)
  - `alternateID` (string, query)
  - `source` (string, query)
  - `externalCRMID` (string, query)
  - `numberOfStaff` (integer, query)
  - `address` (string, query)
  - `address2` (string, query)
  - `city` (string, query)
  - `state` (string, query)
  - `zipCode` (string, query)
  - `country` (string, query)
  - `reportingUrl` (string, query)
  - `reportingUsername` (string, query)
  - `reportingPassword` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Caps
**`POST /advertisers/updateLeadsCaps.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsDailyCap` (integer, query)
  - `leadsWeeklyCap` (integer, query)
  - `leadsMonthlyCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Daily Cap
**`POST /advertisers/updateLeadsDailyCap.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsDailyCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Daily Revenue Cap
**`POST /advertisers/updateLeadsDailyRevenueCap.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsDailyRevenueCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Monthly Cap
**`POST /advertisers/updateLeadsMonthlyCap.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsMonthlyCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Monthly Revenue Cap
**`POST /advertisers/updateLeadsMonthlyRevenueCap.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsMonthlyRevenueCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Revenue Caps
**`POST /advertisers/updateLeadsRevenueCaps.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsDailyRevenueCap` (integer, query)
  - `leadsWeeklyRevenueCap` (integer, query)
  - `leadsMonthlyRevenueCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Weekly Cap
**`POST /advertisers/updateLeadsWeeklyCap.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsWeeklyCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Weekly Revenue Cap
**`POST /advertisers/updateLeadsWeeklyRevenueCap.do`**

**Parameters:**
  - `advertiserID` (integer, query) **[required]**
  - `leadsWeeklyRevenueCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Portal Settings
**`POST /advertisers/updatePortalSettings.do`**

**Parameters:**
  - `portal_access` (string, query) (options: `Yes`, `No`)
  - `two_way_auth` (string, query) (options: `Yes`, `No`)
  - `manage_users` (string, query) (options: `Yes`, `No`)
  - `manage_offers` (string, query) (options: `Yes`, `No`)
  - `update_billing_info` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---
