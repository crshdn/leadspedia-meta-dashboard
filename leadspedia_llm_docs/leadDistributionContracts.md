# Leaddistributioncontracts API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Add Filter](#add-filter) - `POST /leadDistributionContracts/addFilter.do`
- [Add To Offer](#add-to-offer) - `POST /leadDistributionContracts/addToOffer.do`
- [Adjust Credit](#adjust-credit) - `POST /leadDistributionContracts/adjustCredit.do`
- [Assign Email Delivery Method](#assign-email-delivery-method) - `POST /leadDistributionContracts/assignEmailDeliveryMethod.do`
- [Assign SMS Delivery Method](#assign-sms-delivery-method) - `POST /leadDistributionContracts/assignSMSDeliveryMethod.do`
- [Change Mode](#change-mode) - `POST /leadDistributionContracts/changeMode.do`
- [Change Status](#change-status) - `POST /leadDistributionContracts/changeStatus.do`
- [Create](#create) - `POST /leadDistributionContracts/create.do`
- [Create Schedule](#create-schedule) - `POST /leadDistributionContracts/createSchedule.do`
- [Delete](#delete) - `POST /leadDistributionContracts/delete.do`
- [Delete All Delivery Methods](#delete-all-delivery-methods) - `POST /leadDistributionContracts/deleteAllDeliveryMethods.do`
- [Delete All Schedules](#delete-all-schedules) - `POST /leadDistributionContracts/deleteAllSchedules.do`
- [Delete Delivery Method](#delete-delivery-method) - `POST /leadDistributionContracts/deleteDeliveryMethod.do`
- [Delete Filter](#delete-filter) - `POST /leadDistributionContracts/deleteFilter.do`
- [Delete Schedule](#delete-schedule) - `POST /leadDistributionContracts/deleteSchedule.do`
- [Delete Scheduled Pause](#delete-scheduled-pause) - `POST /leadDistributionContracts/deleteScheduledPause.do`
- [Enable Credit](#enable-credit) - `POST /leadDistributionContracts/enableCredit.do`
- [Enable Multiple Delivery Methods](#enable-multiple-delivery-methods) - `POST /leadDistributionContracts/enableMultipleDeliveryMethods.do`
- [Get All](#get-all) - `GET /leadDistributionContracts/getAll.do`
- [Get Basic Info](#get-basic-info) - `GET /leadDistributionContracts/getBasicInfo.do`
- [Get Duplicates Settings](#get-duplicates-settings) - `GET /leadDistributionContracts/getDuplicatesSettings.do`
- [Get Filters](#get-filters) - `GET /leadDistributionContracts/getFilters.do`
- [Get Leads Cap Info](#get-leads-cap-info) - `GET /leadDistributionContracts/getLeadsCapInfo.do`
- [Get Leads Settings](#get-leads-settings) - `GET /leadDistributionContracts/getLeadsSettings.do`
- [Get Portal Settings](#get-portal-settings) - `GET /leadDistributionContracts/getPortalSettings.do`
- [Get Returns Settings](#get-returns-settings) - `GET /leadDistributionContracts/getReturnsSettings.do`
- [Get Revenue Cap Info](#get-revenue-cap-info) - `GET /leadDistributionContracts/getRevenueCapInfo.do`
- [Get Schedule](#get-schedule) - `GET /leadDistributionContracts/getSchedule.do`
- [Get Scheduled Pause](#get-scheduled-pause) - `GET /leadDistributionContracts/getScheduledPause.do`
- [Remove Expiration Date](#remove-expiration-date) - `POST /leadDistributionContracts/removeExpirationDate.do`
- [Rename](#rename) - `POST /leadDistributionContracts/rename.do`
- [Schedule Pause](#schedule-pause) - `POST /leadDistributionContracts/schedulePause.do`
- [Set Expiration Date](#set-expiration-date) - `POST /leadDistributionContracts/setExpirationDate.do`
- [Set Price](#set-price) - `POST /leadDistributionContracts/setPrice.do`
- [Update Auto Recharge Settings](#update-auto-recharge-settings) - `POST /leadDistributionContracts/updateAutoRechargeSettings.do`
- [Update Basic Info](#update-basic-info) - `POST /leadDistributionContracts/updateBasicInfo.do`
- [Update Distribution Priority](#update-distribution-priority) - `POST /leadDistributionContracts/updateDistributionPriority.do`
- [Update Duplicates Settings](#update-duplicates-settings) - `POST /leadDistributionContracts/updateDuplicatesSettings.do`
- [Update Leads Cap](#update-leads-cap) - `POST /leadDistributionContracts/updateLeadsCap.do`
- [Update Leads Settings](#update-leads-settings) - `POST /leadDistributionContracts/updateLeadsSettings.do`
- [Update Portal Settings](#update-portal-settings) - `POST /leadDistributionContracts/updatePortalSettings.do`
- [Update Returns Settings](#update-returns-settings) - `POST /leadDistributionContracts/updateReturnsSettings.do`
- [Update Revenue Cap](#update-revenue-cap) - `POST /leadDistributionContracts/updateRevenueCap.do`
- [Update Schedule](#update-schedule) - `POST /leadDistributionContracts/updateSchedule.do`

---

### Add Filter
**`POST /leadDistributionContracts/addFilter.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `fieldID` (integer, query) **[required]**
  - `operator` (string, query) **[required]**
  - `value` (string, query)
  - `date` (string, query)
  - `miles` (number, query)

**Responses:**
  - `200`: post-response

---

### Add To Offer
**`POST /leadDistributionContracts/addToOffer.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `offerID` (integer, query) **[required]**
  - `priority` (integer, query)

**Responses:**
  - `200`: post-response

---

### Adjust Credit
**`POST /leadDistributionContracts/adjustCredit.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
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

### Assign Email Delivery Method
**`POST /leadDistributionContracts/assignEmailDeliveryMethod.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `deliveryMethodID` (integer, query) **[required]**
  - `email_to` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Assign SMS Delivery Method
**`POST /leadDistributionContracts/assignSMSDeliveryMethod.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `deliveryMethodID` (integer, query) **[required]**
  - `sms_to` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Change Mode
**`POST /leadDistributionContracts/changeMode.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `mode` (string, query) **[required]** (options: `Setup`, `Test`, `Live`)

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /leadDistributionContracts/changeStatus.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`, `Paused`)

**Responses:**
  - `200`: post-response

---

### Create
**`POST /leadDistributionContracts/create.do`**

**Parameters:**
  - `verticalID` (integer, query) **[required]**
  - `advertiserID` (integer, query) **[required]**
  - `revenueModel` (string, query) **[required]** (options: `Fixed`, `Ping/Post`)
  - `contractName` (string, query) **[required]**
  - `defaultPrice` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Create Schedule
**`POST /leadDistributionContracts/createSchedule.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `cap` (integer, query) **[required]**
  - `revenueCap` (number, query) **[required]**
  - `price` (number, query) **[required]**
  - `startTime` (string, query) **[required]**
  - `endTime` (string, query) **[required]**
  - `type` (string, query) **[required]** (options: `Exclusive`, `Multisell`)
  - `Monday` (string, query) (options: `Yes`, `No`)
  - `Tuesday` (string, query) (options: `Yes`, `No`)
  - `Wednesday` (string, query) (options: `Yes`, `No`)
  - `Thursday` (string, query) (options: `Yes`, `No`)
  - `Friday` (string, query) (options: `Yes`, `No`)
  - `Saturday` (string, query) (options: `Yes`, `No`)
  - `Sunday` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /leadDistributionContracts/delete.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete All Delivery Methods
**`POST /leadDistributionContracts/deleteAllDeliveryMethods.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete All Schedules
**`POST /leadDistributionContracts/deleteAllSchedules.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete Delivery Method
**`POST /leadDistributionContracts/deleteDeliveryMethod.do`**

**Parameters:**
  - `deliveryMethodsContractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete Filter
**`POST /leadDistributionContracts/deleteFilter.do`**

**Parameters:**
  - `filterID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete Schedule
**`POST /leadDistributionContracts/deleteSchedule.do`**

**Parameters:**
  - `deliveryScheduleID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete Scheduled Pause
**`POST /leadDistributionContracts/deleteScheduledPause.do`**

**Parameters:**
  - `scheduledPauseID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Enable Credit
**`POST /leadDistributionContracts/enableCredit.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `buyerLevel` (string, query) **[required]** (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Enable Multiple Delivery Methods
**`POST /leadDistributionContracts/enableMultipleDeliveryMethods.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /leadDistributionContracts/getAll.do`**

**Parameters:**
  - `advertiserID` (integer, query)
  - `contractID` (integer, query)
  - `verticalID` (integer, query)
  - `status` (string, query) (options: `Active`, `InActive`, `Paused`)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Basic Info
**`GET /leadDistributionContracts/getBasicInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Duplicates Settings
**`GET /leadDistributionContracts/getDuplicatesSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Filters
**`GET /leadDistributionContracts/getFilters.do`**

**Parameters:**
  - `contractID` (integer, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Leads Cap Info
**`GET /leadDistributionContracts/getLeadsCapInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Leads Settings
**`GET /leadDistributionContracts/getLeadsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Portal Settings
**`GET /leadDistributionContracts/getPortalSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Returns Settings
**`GET /leadDistributionContracts/getReturnsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Revenue Cap Info
**`GET /leadDistributionContracts/getRevenueCapInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Schedule
**`GET /leadDistributionContracts/getSchedule.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Scheduled Pause
**`GET /leadDistributionContracts/getScheduledPause.do`**

**Parameters:**
  - `contractID` (integer, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Remove Expiration Date
**`POST /leadDistributionContracts/removeExpirationDate.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Rename
**`POST /leadDistributionContracts/rename.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `contractName` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Schedule Pause
**`POST /leadDistributionContracts/schedulePause.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `pauseDate` (string, query) **[required]**
  - `resumeDate` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Set Expiration Date
**`POST /leadDistributionContracts/setExpirationDate.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `expirationDate` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Set Price
**`POST /leadDistributionContracts/setPrice.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `price` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Auto Recharge Settings
**`POST /leadDistributionContracts/updateAutoRechargeSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
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

### Update Basic Info
**`POST /leadDistributionContracts/updateBasicInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `contractName` (string, query)
  - `alternativeID` (string, query)
  - `notes` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Distribution Priority
**`POST /leadDistributionContracts/updateDistributionPriority.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `offerID` (integer, query) **[required]**
  - `priority` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Duplicates Settings
**`POST /leadDistributionContracts/updateDuplicatesSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `enableDuplicateCheck` (string, query) (options: `Yes`, `No`)
  - `numberOfDays` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Cap
**`POST /leadDistributionContracts/updateLeadsCap.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `hourlyLeadsCap` (integer, query)
  - `dailyLeadsCap` (integer, query)
  - `weeklyLeadsCap` (integer, query)
  - `monthlyLeadsCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Leads Settings
**`POST /leadDistributionContracts/updateLeadsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `minimumLeadAge` (integer, query)
  - `maximumLeadAge` (integer, query)
  - `maximumPostErrors` (integer, query)
  - `timeLeadsPosts` (integer, query)
  - `allowQueueLeads` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Portal Settings
**`POST /leadDistributionContracts/updatePortalSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `showStatus` (string, query) (options: `Yes`, `No`)
  - `showLeadData` (string, query) (options: `Yes`, `No`)
  - `showSchedule` (string, query) (options: `Yes`, `No`)
  - `showCaps` (string, query) (options: `Yes`, `No`)
  - `showReturnSettings` (string, query) (options: `Yes`, `No`)
  - `allowStatusPause` (string, query) (options: `Yes`, `No`)
  - `allowUpdateSchedule` (string, query) (options: `Yes`, `No`)
  - `allowManageCaps` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Returns Settings
**`POST /leadDistributionContracts/updateReturnsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `allowReturns` (string, query) (options: `Yes`, `No`)
  - `autoApproveReturns` (string, query) (options: `Yes`, `No`)
  - `replaceReturns` (string, query) (options: `Yes`, `No`)
  - `replacementNonReturnable` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Revenue Cap
**`POST /leadDistributionContracts/updateRevenueCap.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `hourlyRevenueCap` (integer, query)
  - `dailyRevenueCap` (integer, query)
  - `weeklyRevenueCap` (integer, query)
  - `monthlyRevenueCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Schedule
**`POST /leadDistributionContracts/updateSchedule.do`**

**Parameters:**
  - `deliveryScheduleID` (integer, query) **[required]**
  - `cap` (integer, query)
  - `revenueCap` (number, query)
  - `price` (number, query)
  - `startTime` (string, query)
  - `endTime` (string, query)
  - `type` (string, query) (options: `Exclusive`, `Multisell`)

**Responses:**
  - `200`: post-response

---
