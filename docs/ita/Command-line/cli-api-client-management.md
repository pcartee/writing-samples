---
title: API Client management
description: Trust Authority CLI API client management commands.
author: pcartee
topic-type: Reference
date: 01/03/2024
uid: api-client-management
---

*· January/03/2024 ·*

## API client management

These commands are used to manage API clients.

:::note
You need your admin API key to perform these commands. See the [Copy Admin API key](../Quickstart/tutorial-api-key.md#admin-keys) instructions for more information.
:::

## Create apiClient

This command creates a new attestation API key and its associated metadata (associating the key with policies, tags, etc.). However, you need to access the portal to get the API key's value. See the [Getting Started](../Quickstart/tutorial-api-key.md) article for instructions on how to view and copy the attestation API key's.

`trustauthorityctl create apiClient -r < service id > -p < product id > -n < api client name > -i "comma separated policy Ids" -v "tag-id1:tag-name1,tag-id2:tag-name2"`

### Sample Call

```bash
trustauthorityctl create apiClient -n "TestApiClientKeyDefaultTag" -p 095e2a13-b913-4d66-9c4d-f6e8a40f5915 -r 382d4141-103b-47f3-a001-13490db89d1d -v Workload:testworkload
```

### Sample response

```bash
trace-id:  LOnu-EK3IAMEHdA=
ApiClient: 

 {
  "id": "60e94c91-e181-4bbe-9325-df6d8ac52866",
  "service_id": "382d4141-103b-47f3-a001-13490db89d1d",
  "service_offer_name": "",
  "product_id": "095e2a13-b913-4d66-9c4d-f6e8a40f5915",
  "product_name": "Enterprise",
  "status": "Active",
  "name": "AmberApiClientKeyDefaultTag",
  "keys": [
    "7SgAk9i80NaqzR1kWX6RT2jfDS15p7uK2fezZ6EG"
  ],
  "policy_ids": null,
  "tags": [
    {
      "key": "Workload",
      "value": "testworkload",
      "predefined": true
    }
  ],
  "created_at": "2023-09-14T04:04:47.626821351Z",
  "product_type": "attestation"
}



```

## Update apiClient

 This command updates your current apiClient.

`trustauthorityctl update apiClient -r < service id > -p < product id > -c < api client id > -i "comma separated policy Ids" -v "tag-key1:tag-value1,tag-key2:tag-value2"`

### Sample call

```bash
trustauthorityctl update apiClient -r 382d4141-103b-47f3-a001-13490db89d1d -p 095e2a13-b913-4d66-9c4d-f6e8a40f5915 -c 0c5be66c-fac0-4c27-825b-22ee5abbbf71 -i 32489d08-9a79-4643-b526-f4402cba3c29 -v "Tag:abc123"
```

### Sample response

```bash
trace-id:  LOnw6Fv6oAMEstQ=
ApiClient: 

 {
  "id": "0c5be66c-fac0-4c27-825b-22ee5abbbf71",
  "service_id": "382d4141-103b-47f3-a001-13490db89d1d",
  "product_id": "095e2a13-b913-4d66-9c4d-f6e8a40f5915",
  "product_name": "",
  "status": "Active",
  "name": "Amber-ApiClient_Key123",
  "created_at": "2023-09-14T04:04:46.280101Z",
  "product_type": "attestation"
}
```

## Get apiClient

This command lists your apiClient.

`trustauthorityctl list apiClient -r < service id >`

### Sample call

```bash
trustauthorityctl list apiClient -r 382d4141-103b-47f33-a001-13490db89d1d
```

### Sample response

```bash
trace-id:  LOnw6Fv6oAMEstQ=
ApiClient: 

  {
    "id": "948rujr4-e3rt-0oke-ok8u-fr45tk9mf2q1",
    "service_id": "09kjmn3w-9i8u-043kd-p0j3-3erf098kjmnf",
    "product_id": "pldo9ide3e-09id-0odc-p0od-podo85mn324d",
    "product_name": "Enterprise",
    "status": "Inactive",
    "description": "TenantCliKeyUser2",
    "expired_at": "2022-11-14T11:08:40.804604Z",
    "created_at": "2022-10-14T10:15:24.376065Z"
  }

```

## Get apiClient by id

This command lists a specific Trust Authority apiClient.

`trustauthorityctl list apiClient -r < service id > -c < api Client id >`

### Sample call

```bash

trustauthorityctl list apiClient -r 382d4141-103b-47f33-a001-13490db89d1d -c 0c5be66c-fac0-4c27-825b-22ee5abbbf71
```

### Sample response

```bash
trace-id:  LOny2GU8IAMEgZw=
ApiClients: 

 {
  "id": "0c5be66c-fac0-4c27-825b-22ee5abbbf71",
  "service_id": "382d4141-103b-47f3-a001-13490db89d1d",
  "service_offer_name": "TEE Attestation",
  "product_id": "095e2a13-b913-4d66-9c4d-f6e8a40f5915",
  "product_name": "Enterprise",
  "status": "Active",
  "name": "Amber-ApiClient_Key123",
  "keys": [
    "zALiUm06Xf7aGKIWsLUUW2B4wGBRBORm9EvfRZyo"
  ],
  "policy_ids": [],
  "tags": [],
  "created_at": "2023-09-14T04:04:46.280101Z",
  "product_type": "attestation"
}
```

## Delete apiClient

This command deletes a Trust Authority apiClient.

`trustauthorityctl delete apiClient -r < service id > -c < api client id >`

### Sample Call

```bash
trustauthorityctl delete apiClient -r 382d4141-103b-477f3-a001-13490db89d1d -c 0c5be66c-fac0-4c27-825b-22ee5abbbf71
```

### Sample response

```bash
trace-id:  LOn0YHigIAMEX7g=
Deleted api client with Id: 36ffa32c-e1df-46a2-9d57-f2be51c07d9f
```

## List apiClient policies

`trustauthorityctl list apiClient policy -r < service id > -c < api client id >`

### Sample call

```bash
trustauthorityctl list apiClient policy -r 382d4141-103b-47f3-a001-13490db89d1d -c 3a7e48bc-0d7a-4078-b830-8d4da2b5b704

```

### Sample response

```bash
trace-id:  LOnzYH4uoAMEdiQ=
Policy IDs: 

 {
  "policy_ids": [
    "32489d08-9a79-4643-b526-f4402cba3c29"
  ]
}
```

## Create tag

This command creates a tag for Trust Authority.

`trustauthorityctl create tag -n < tag name >`

### Sample call

```bash
trustauthorityctl create tag -n "TestTagUsername"
```

### Sample response

```bash
trace-id:  LOnIBH5yIAMEJ5Q=
{
  "id": "60f29395-2ffc-4e65-8e60-5abbd2e97d1c",
  "name": "TestTagUsername",
  "predefined": false
}
```

## List tags

This command list the tags associated to your Trust Authority system.

`trustauthorityctl list tag`

### Sample call

```bash
trustauthorityctl list tag
```

### Sample Response

```bash
trace-id:  LOnI6FFjIAMEYaQ=
Tags: 

 {
  "tags": [
    {
      "id": "010fe8cf-5f6c-4840-a0b0-df96168bc2b3",
      "name": "Workload",
      "predefined": true
    },
    {
      "id": "976e4fe8-b5ba-4443-a7d6-fd2544cadb69",
      "name": "AmberTag",
      "predefined": false
    },
    {
      "id": "259d1b98-16d7-42ed-a3da-f9ddb2cc842d",
      "name": "Amber-Tag",
      "predefined": false
    },
    {
      "id": "63245ae5-7519-4347-9de2-fece6fc3848b",
      "name": "Amber_Tag",
      "predefined": false
    }
  ]
}
```

## Delete tag

This command deletes a tag.

`trustauthorityctl delete tag -t < tag id >`

### Sample call
```bash
trustauthorityctl delete tag -t 47yukjsv-29op-38sq-v3g8-xcqd456hju7i
```

### Sample response

```bash
{
 tag 47yukjsv-29op-38sq-v3g8-xcqd456hju7i deleted
 }
```


## List apiClient tags

This command lists all your Trust Authority tags.

`trustauthorityctl list apiClient tag -r < service id > -c <  api client id >`

### Sample call

```bash
trustauthorityctl list apiClient tag -r 382d4141-103b-47f3-a001-13490db89d1d -c 30686bc0-0a75-4086-9a4c-4c59bea6df64
```

### Sample response

```bash
trace-id:  LOnz5H8OoAMEVtQ=
Tags: 

 {
  "tags": [
    {
      "key": "AmberTag",
      "value": "AmberTagValue",
      "predefined": false
    }
  ]
}
```

## Get API client policies

This command lists your subscriptions and policies.

`trustauthorityctl list apiClient policy -r < service id > -c < api client id >`

### Sample call

```bash
trustauthorityctl list apiClient policy -r 382d4141-10
03b-47f3-a001-13490db89d1d -c 3a7e48bc-0d7a-4078-b830-8d4da2b5b704
```

### Sample response

```bash
trace-id:  LOnzYH4uoAMEdiQ=
Policy IDs: 

 {
  "policy_ids": [
    "32489d08-9a79-4643-b526-f4402cba3c29"
  ]
}
```


