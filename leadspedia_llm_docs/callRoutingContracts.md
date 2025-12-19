# Callroutingcontracts API

**Base URL:** `https://api.leadspedia.com/core/v2`

**Authentication:** All endpoints require `api_key` and `api_secret` query parameters.

---

## Endpoints

- [Adjust Credit](#adjust-credit) - `POST /callRoutingContracts/adjustCredit.do`
- [Change Mode](#change-mode) - `POST /callRoutingContracts/changeMode.do`
- [Change Status](#change-status) - `POST /callRoutingContracts/changeStatus.do`
- [Create](#create) - `POST /callRoutingContracts/create.do`
- [Delete](#delete) - `POST /callRoutingContracts/delete.do`
- [Delete Scheduled Pause](#delete-scheduled-pause) - `POST /callRoutingContracts/deleteScheduledPause.do`
- [Enable Credit](#enable-credit) - `POST /callRoutingContracts/enableCredit.do`
- [Get All](#get-all) - `GET /callRoutingContracts/getAll.do`
- [Get Basic Info](#get-basic-info) - `GET /callRoutingContracts/getBasicInfo.do`
- [Get Billable Transfers Cap Info](#get-billable-transfers-cap-info) - `GET /callRoutingContracts/getBillableTransfersCapInfo.do`
- [Get Portal Settings](#get-portal-settings) - `GET /callRoutingContracts/getPortalSettings.do`
- [Get Repeat Calls Settings](#get-repeat-calls-settings) - `GET /callRoutingContracts/getRepeatCallsSettings.do`
- [Get Returns Settings](#get-returns-settings) - `GET /callRoutingContracts/getReturnsSettings.do`
- [Get Revenue Cap Info](#get-revenue-cap-info) - `GET /callRoutingContracts/getRevenueCapInfo.do`
- [Get Scheduled Pause](#get-scheduled-pause) - `GET /callRoutingContracts/getScheduledPause.do`
- [Get Transfers Cap Info](#get-transfers-cap-info) - `GET /callRoutingContracts/getTransfersCapInfo.do`
- [Remove Expiration Date](#remove-expiration-date) - `POST /callRoutingContracts/removeExpirationDate.do`
- [Remove Whisper Message](#remove-whisper-message) - `POST /callRoutingContracts/removeWhisperMessage.do`
- [Rename](#rename) - `POST /callRoutingContracts/rename.do`
- [Schedule Pause](#schedule-pause) - `POST /callRoutingContracts/schedulePause.do`
- [Set Audio Whisper Message](#set-audio-whisper-message) - `POST /callRoutingContracts/setAudioWhisperMessage.do`
- [Set Expiration Date](#set-expiration-date) - `POST /callRoutingContracts/setExpirationDate.do`
- [Set Text-To-Speech Whisper Message](#set-text-to-speech-whisper-message) - `POST /callRoutingContracts/setTextToSpeechWhisperMessage.do`
- [Update Auto Recharge Settings](#update-auto-recharge-settings) - `POST /callRoutingContracts/updateAutoRechargeSettings.do`
- [Update Basic Info](#update-basic-info) - `POST /callRoutingContracts/updateBasicInfo.do`
- [Update Billable Transfers Cap](#update-billable-transfers-cap) - `POST /callRoutingContracts/updateBillableTransfersCap.do`
- [Update Portal Settings](#update-portal-settings) - `POST /callRoutingContracts/updatePortalSettings.do`
- [Update Repeat Calls Settings](#update-repeat-calls-settings) - `POST /callRoutingContracts/updateRepeatCallsSettings.do`
- [Update Returns Settings](#update-returns-settings) - `POST /callRoutingContracts/updateReturnsSettings.do`
- [Update Revenue Cap](#update-revenue-cap) - `POST /callRoutingContracts/updateRevenueCap.do`
- [Update Revenue Model](#update-revenue-model) - `POST /callRoutingContracts/updateRevenueModel.do`
- [Update Transfer Number](#update-transfer-number) - `POST /callRoutingContracts/updateTransferNumber.do`
- [Update Transfers Cap](#update-transfers-cap) - `POST /callRoutingContracts/updateTransfersCap.do`

---

### Adjust Credit
**`POST /callRoutingContracts/adjustCredit.do`**

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

### Change Mode
**`POST /callRoutingContracts/changeMode.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `mode` (string, query) **[required]** (options: `Setup`, `Test`, `Live`)

**Responses:**
  - `200`: post-response

---

### Change Status
**`POST /callRoutingContracts/changeStatus.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `status` (string, query) **[required]** (options: `Active`, `InActive`, `Paused`)

**Responses:**
  - `200`: post-response

---

### Create
**`POST /callRoutingContracts/create.do`**

**Parameters:**
  - `verticalID` (integer, query) **[required]**
  - `advertiserID` (integer, query) **[required]**
  - `contractName` (string, query) **[required]**
  - `defaultPrice` (number, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete
**`POST /callRoutingContracts/delete.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Delete Scheduled Pause
**`POST /callRoutingContracts/deleteScheduledPause.do`**

**Parameters:**
  - `scheduledPauseID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Enable Credit
**`POST /callRoutingContracts/enableCredit.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `buyerLevel` (string, query) **[required]** (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Get All
**`GET /callRoutingContracts/getAll.do`**

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
**`GET /callRoutingContracts/getBasicInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Billable Transfers Cap Info
**`GET /callRoutingContracts/getBillableTransfersCapInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Portal Settings
**`GET /callRoutingContracts/getPortalSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Repeat Calls Settings
**`GET /callRoutingContracts/getRepeatCallsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Returns Settings
**`GET /callRoutingContracts/getReturnsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Revenue Cap Info
**`GET /callRoutingContracts/getRevenueCapInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Get Scheduled Pause
**`GET /callRoutingContracts/getScheduledPause.do`**

**Parameters:**
  - `contractID` (integer, query)
  - `start` (integer, query)
  - `limit` (integer, query)

**Responses:**
  - `200`: 

---

### Get Transfers Cap Info
**`GET /callRoutingContracts/getTransfersCapInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: 

---

### Remove Expiration Date
**`POST /callRoutingContracts/removeExpirationDate.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Remove Whisper Message
**`POST /callRoutingContracts/removeWhisperMessage.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Rename
**`POST /callRoutingContracts/rename.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `contractName` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Schedule Pause
**`POST /callRoutingContracts/schedulePause.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `pauseDate` (string, query) **[required]**
  - `resumeDate` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Set Audio Whisper Message
**`POST /callRoutingContracts/setAudioWhisperMessage.do`**

**Parameters:**
  - `contractID` (string, query) **[required]**
  - `audioID` (integer, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Set Expiration Date
**`POST /callRoutingContracts/setExpirationDate.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `expirationDate` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Set Text-To-Speech Whisper Message
**`POST /callRoutingContracts/setTextToSpeechWhisperMessage.do`**

**Parameters:**
  - `contractID` (string, query) **[required]**
  - `message` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Auto Recharge Settings
**`POST /callRoutingContracts/updateAutoRechargeSettings.do`**

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
**`POST /callRoutingContracts/updateBasicInfo.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `contractName` (string, query)
  - `transferNumber` (string, query)
  - `alternativeID` (string, query)
  - `notes` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Billable Transfers Cap
**`POST /callRoutingContracts/updateBillableTransfersCap.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `hourlyBillableCap` (integer, query)
  - `dailyBillableCap` (integer, query)
  - `weeklyBillableCap` (integer, query)
  - `monthlyBillableCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Portal Settings
**`POST /callRoutingContracts/updatePortalSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `showStatus` (string, query) (options: `Yes`, `No`)
  - `showSchedule` (string, query) (options: `Yes`, `No`)
  - `showCaps` (string, query) (options: `Yes`, `No`)
  - `showReturnSettings` (string, query) (options: `Yes`, `No`)
  - `allowStatusPause` (string, query) (options: `Yes`, `No`)
  - `allowUpdateSchedule` (string, query) (options: `Yes`, `No`)
  - `allowManageCaps` (string, query) (options: `Yes`, `No`)
  - `callRecordings` (string, query) (options: `Yes`, `No`)
  - `hideCallerID` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Repeat Calls Settings
**`POST /callRoutingContracts/updateRepeatCallsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `repeatCallDays` (integer, query)
  - `transferRepeat` (string, query) (options: `Yes`, `No`)
  - `repeatBillable` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Returns Settings
**`POST /callRoutingContracts/updateReturnsSettings.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `allowReturns` (string, query) (options: `Yes`, `No`)
  - `autoApproveReturns` (string, query) (options: `Yes`, `No`)

**Responses:**
  - `200`: post-response

---

### Update Revenue Cap
**`POST /callRoutingContracts/updateRevenueCap.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `hourlyRevenueCap` (integer, query)
  - `dailyRevenueCap` (integer, query)
  - `weeklyRevenueCap` (integer, query)
  - `monthlyRevenueCap` (integer, query)

**Responses:**
  - `200`: post-response

---

### Update Revenue Model
**`POST /callRoutingContracts/updateRevenueModel.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `revenueModel` (string, query) **[required]** (options: `Transfer`, `Duration`)
  - `price` (number, query) **[required]**
  - `duration` (string, query)

**Responses:**
  - `200`: post-response

---

### Update Transfer Number
**`POST /callRoutingContracts/updateTransferNumber.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `transferNumber` (string, query) **[required]**

**Responses:**
  - `200`: post-response

---

### Update Transfers Cap
**`POST /callRoutingContracts/updateTransfersCap.do`**

**Parameters:**
  - `contractID` (integer, query) **[required]**
  - `hourlyTransfersCap` (integer, query)
  - `dailyTransfersCap` (integer, query)
  - `weeklyTransfersCap` (integer, query)
  - `monthlyTransfersCap` (integer, query)

**Responses:**
  - `200`: post-response

---
