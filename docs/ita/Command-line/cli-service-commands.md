---
title: Intel Trust Authority CLI Service Management
description: Intel Trust Authority CLI service management commands.
author: pcartee
topic-type: Reference
date: 08/16/2023
uid: cli-service-commands
---

*· August/15/2023 ·*

## Service management

Use the commands listed below to manage your services.

:::note
Have your API key available before attempting these commands. To obtain your API key, follow the [retrieve API key](cli-examples.md#retrieve-admin-api-keys) instructions.
:::

## Get service offers

The following command list your Intel® Trust Authority service offer.

`trustauthorityctl list serviceOffer`

### Sample call

```bash
trustauthorityctl list serviceOffer
```

### Sample response

```bash
trace-id:  LOm53EuHoAMEIhA=
Service offers: 

 [
  {
    "id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
    "name": "TEE Attestation"
  }
]
```

## Get services

Returns all the subscribed services for the tenant associated with the API key.

`trustauthorityctl list service`

### Sample response

```bash
trace-id:  LOm7kE9WoAMEG_w=
 [
  {
    "id": "1dceedae-0f71-4bb7-a076-52b29f751fbd",
    "tenant_id": "92b8f7a8-3a3b-4530-a562-91edca330fac",
    "service_offer_id": "8fe770d6-aec0-4eca-bc9d-893ae198fab7",
    "name": "TEE_Attestation",
    "plan_id": "b5fae544-5894-4305-8754-5e18d7b4cb25",
    "plan_name": "Enterprise",
    "active": true,
    "created_at": "2023-03-27T04:39:23.888083Z"
  }
]
```

## Get service by id

Retrieves subscribed service details for the specified serviceId for tenant associated with the API key.

`trustauthorityctl list service -r < service Id >`

### Sample call

```bash
	trustauthorityctl list service -r 1dceedae-0f71-4bb7-a076-52b229f751fbd
```

### Sample response

```bash
trace-id:  LOm7qHi1oAMEtkg=
Services:
{
  "id": "1dceedae-0f71-4bb7-a076-52b29f751fbd",
  "service_offer_id": "8fe770d6-aec0-4eca-bc9d-893ae198fab7",
  "service_offer_name": "TEE Attestation",
  "name": "TEE_Attestation",
  "created_at": "2023-03-27T04:39:23.888083Z",
  "active": true,
  "plan_id": "b5fae544-5894-4305-8754-5e18d7b4cb25",
  "plan_name": "Enterprise"
}
```

## Get plans

This command retrieves the plans in your Intel Trust Authority environment.

`trustauthorityctl list plan -r < service offer id >`

### Sample call

```bash
trustauthorityctl list plan -r 8fe770d6-aec0-4eca-bc9d-893ae1998fab7
```

### Sample response

```bash
trace-id:  LOm5_EPjoAMEN4Q=
Plans: 

 [
  {
    "id": "e8b6cf50-e2d2-4b2e-ad1b-93994002b980",
    "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
    "name": "Starter",
    "max_key": 1,
    "max_tenant_admin": 2,
    "max_tenant_user": 100,
    "max_policy": 1,
    "ledger": true
  },
  {
    "id": "e66ae43b-3150-44a2-b54f-5d31e7f72361",
    "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
    "name": "Enterprise",
    "max_key": 10,
    "max_tenant_admin": 5,
    "max_tenant_user": 100,
    "max_policy": 10,
    "ledger": true
  }
]
```

## Get plan by id

Retrieves details of a plan associated with the serviceOfferId for the specified planId.

`trustauthorityctl list plan -r < service offer id > -p < plan id >`

### Sample call

```bash
trustauthorityctl list plan -r 8fe770d6-aec0-4eca-bc9d-893ae1998fab7 -p b5fae544-5894-4305-8754-5e18d7b4cb25
```

### Sample response

```bash
trace-id:  LOm6XED-oAMEoFQ=
Plans: 

 {
  "id": "e8b6cf50-e2d2-4b2e-ad1b-93994002b980",
  "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
  "name": "Starter",
  "max_key": 1,
  "max_tenant_admin": 2,
  "max_tenant_user": 100,
  "max_policy": 1,
  "ledger": true,
  "products": [
    {
      "id": "0ce6c2b6-c81f-48d6-a14b-ddca2e607ead",
      "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
      "name": "Starter",
      "policy": {
        "limit": 60,
        "quota": 1000,
        "limit_renewal_period": 60,
        "quota_renewal_period": 604801
      },
      "plan_id": "e8b6cf50-e2d2-4b2e-ad1b-93994002b980",
      "product_type": "attestation"
    },
    {
      "id": "db44d79a-12e7-46ff-9bae-88db114ded75",
      "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
      "name": "Management",
      "policy": {
        "limit": 60,
        "quota": 200000,
        "limit_renewal_period": 60,
        "quota_renewal_period": 604801
      },
      "plan_id": "e8b6cf50-e2d2-4b2e-ad1b-93994002b980",
      "product_type": "management"
    }
  ]
}
```

## Get products

The following command list the products in your Intel Trust Authority environment.

`trustauthorityctl list product -r < service offer id >`

### Sample call

```bash
trustauthorityctl list product -r ea6ad8d3-fd3f-4ccb-82c7-ac021899a199
```

### Sample Response

```bash
trace-id:  LOm7LHeVIAMEttg=
Products: 

 [
  {
    "id": "0ce6c2b6-c81f-48d6-a14b-ddca2e607ead",
    "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
    "name": "Starter",
    "policy": {
      "limit": 60,
      "quota": 1000,
      "limit_renewal_period": 60,
      "quota_renewal_period": 604801
    },
    "plan_id": "e8b6cf50-e2d2-4b2e-ad1b-93994002b980",
    "product_type": "attestation"
  },
  {
    "id": "095e2a13-b913-4d66-9c4d-f6e8a40f5915",
    "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
    "name": "Enterprise",
    "policy": {
      "limit": 60,
      "quota": 5000000,
      "limit_renewal_period": 60,
      "quota_renewal_period": 604801
    },
    "plan_id": "e66ae43b-3150-44a2-b54f-5d31e7f72361",
    "product_type": "attestation"
  },
]
```
