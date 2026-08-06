---
title: Key Broker key creation and key retrieval 
description: KBS key creation and retrieval
author: carteepaul
topic: KBS
date: 02/26/2024
id: kbs.key.creation.retrieval
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Once the KBS service is installed and running successfully, follow the steps below to create keys and retrieve them.

:::note
The SGX attestation type is shown only as an example. Other attestation types, such as TDX, exist, and others are being developed. The term "attributes" is another way to describe claims. Attributes correspond to claims in the [attestation token](../Concepts/concept-attestation-tokens.md) issued by Trust Authority. "policy_ids" in the KBS policy is the same as "matched_policy_ids" in the attestationp token.
:::

## SGX supported attributes

|Attribute  |Description                                                  |
|-----------|:------------------------------------------------------------|
|isvprodid  |Product ID Specific to the workload running the SGX enclave  |
|isvsvn     |The Security Version Number of the Enclave                   |
|mrenclave  |Hash of the Contents of the SGX Enclave                      |
|mrsigner   |Hash of the key used to sign the SGX Enclave                 |
|policy_ids |List of policy IDs which are matched in Trust Authority|

## TDX supported attributes

|Attribute      |Description                                                          |
|---------------|:--------------------------------------------------------------------|
|mrseam         |Hash of the Contents of the TDX SEAM Module                          |
|mrsignerseam   |Hash of the key used to sign the TDX SEAM Module                     |
|mrtd           |SHA-384 measurement of a TD, accumulated during TD build             |
|rtmr0          |A SHA-384 measurement register that can be updated during TD run-time|
|rtmr1          |A SHA-384 measurement register that can be updated during TD run-time|
|rtmr2          |A SHA-384 measurement register that can be updated during TD run-time|
|rtmr3          |A SHA-384 measurement register that can be updated during TD run-time|
|seamsvn        |The Security Version Number of the TDX SEAM Module                   |
|policy_ids     |List of policy IDs which are matched in Trust Authority        |

## enforce_upto_date directive

The **enforce_tcb_upto_date** directive is a Boolean flag to check if the TCB status is up-to-date or not. If it is set to **true**, the KBS policy expects the **tcb_status** claim in the token to be up-to-date else the KBS policy verification fails, thus denying the key release. If it is set to **false**, any TCB status value will work for key release, and the KBS won’t check for up-to-date TCB status.

If you are using the [platform TCB policy](../Concepts/concept-platform-tcb.md) features, you should set **enforce_tcb_upto_date** to **false** and include the appraisal policy ID for your platform TCB policy in the list of **matched_ids** in your KBS policy. Doing this ensures that the Trust Authority appraisal policy controls TCB behavior instead of the KBS key release policy.

## Fetch the bearer token

### POST /token

Creates a JWT for the user specified in the request.

Use the admin token to create key transfer policies by defining the rules to retrieve the keys from the backend KMS (KMIP).

***Example request body***

```JSON
{
  "password": "testPassword",
  "username": "testUser"
}
```

## Create a key transfer policy for the SGX or TDX workload

A key transfer policy contains the information required for a key to be released to a relying party. A user with the "key-transfer-policy:create" permission in the token can create a policy for a key.

The table below lists the supported attributes for SGX and TDX.

### POST /key-transfer-policies 

Creates a key transfer policy. Only one key transfer policy can be created at a time. A key transfer policy can be created in the following ways:

- by providing only a list of policy-ids

    ```JSON
    {
        "attestation_type": "SGX",
            "policy_ids": ["37965f5f-ccaf-4cdc-a356-a8ed5268a5bf", "9846bf40-e380-4842-ae15-1b60996d1190"] 
    }
    ```

- by providing only TDX or SGX attributes 

    ```JSON
    {
        "attestation_type": "SGX",
        "sgx": {
            "attributes": {
                "mrsigner": ["cd171c56941c6ce49690b455f691d9c8a04c2e43e0a4d30f752fa5285c7ee57f"],
                "isvprodid": [12],
                "mrenclave": ["01c60b9617b2f96e53cb75ef01e0dccea3afc7b7992697eabb8f714b2ccd1953"],
                "isvsvn": 1
            }
        }
    }
    ```

- by providing both a list of policy-ids and TDX or SGX attributes

    ```JSON
    {
        "attestation_type": "SGX",
        "sgx": {
            "attributes": {
             "mrsigner": ["cd171c56941c6ce49690b455f691d9c8a04c2e43e0a4d30f752fa5285c7ee57f"],
             "isvprodid": [12],
              "mrenclave": ["01c60b9617b2f96e53cb75ef01e0dccea3afc7b7992697eabb8f714b2ccd1953"],
               "isvsvn": 1
         },
         "policy_ids": ["37965f5f-ccaf-4cdc-a356-a8ed5268a5bf", "9846bf40-e380-4842-ae15-1b60996d1190"]
        }
    }
    ```

<Tabs>
<TabItem value="sgx-policy" label="SGX policy">

```json
	{
    "attestation_type": "SGX",
    "sgx":{
            "attributes":{
                "mrsigner": ["83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e"],
                "isvprodid":[0],
                "mrenclave":["83f4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204410"],
                "isvsvn":0,
                "enforce_tcb_upto_date":false
            }
		}
	}
```

</TabItem>
<TabItem value="tdx-policy" label="TDX policy">

```json
	{
    "attestation_type":["TDX"],
    "tdx":{
            "attributes":{
                "mrseam":["2fd279c16164a93dd5bf373d834328d46008c2b693af9ebb865b08b2ced320c9a89b4869a9fab60fbe9d0c5a5363c656"],
                "mrsignerseam":["000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
                "seamsvn":"3",
                "mrtd":["5f53c3881242a5b418854923bb4adec34c72aa4b570d526179d63f9ee6e4cefb6abd4f0f35e5e6e29655a60d90bcf27f"],
                "rtmr0": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "rtmr1": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "rtmr2": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "rtmr3": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "enforce_tcb_upto_date" : "false"
            }
		}
	}
```
</TabItem>
</Tabs>

## Create a key

Use the Keys API to create new keys and provide the key-transfer-policy ID in the POST request.

### POST /keys

Creates or Registers a key.

***Request body for key creation***

```json
{"key_information":
{
"algorithm": "RSA",
"key_length": 3072
},
"transfer_policy_id" : "0855be44-45bd-4ff3-b545-7987e6a1c36b"
}
```

## Retrieve the key

### POST /keys/\{id\}/transfer

Refer to [Passport verification mode](../Key-broker/key-broker-service.md#intel-kbs-use-cases) and [Background verification mode](../Key-broker/key-broker-service.md#intel-kbs-use-cases) documentation on how the key is released.

***Sample request for passport mode***

```bash
{
"attestation_token": token
}
```

***Sample request for background mode***

```json
{
"quote": "{{SGX-QUOTE}}",
"nonce": {
"val": "{{NONCE}}",
"iat": "{{NONCE-DATE}}",
"signature": "{{NONCE-SIGNATURE}}"
},
"user_data": "{{USER-DATA}}"
}
```

### Retrieve the key without TEE attestation

Keys can be retrieved from the KBS without requiring TEE attestation and TEE evidence verification. The keys released from the KBS are always wrapped. Providing only a public key (must be an RSA key size of at least 2048 bits) to wrap the secret is one way to retrieve the key from the KBS. Refer to the following API to retrieve the key without Trust Authority.

URL: `POST /kbs/v1/keys/\{id\}`

***Sample request key***

```bash
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsjtGIk8SxD+OEiBpP2/T
JUAF0upwuKGMk6wH8Rwov88VvzJrVm2NCticTk5FUg+UG5r8JArrV4tJPRHQyvqK
wF4NiksuvOjv3HyIf4oaOhZjT8hDne1Bfv+cFqZJ61Gk0MjANh/T5q9vxER/7TdU
NHKpoRV+NVlKN5bEU/NQ5FQjVXicfswxh6Y6fl2PIFqT2CfjD+FkBPU1iT9qyJYH
A38IRvwNtcitFgCeZwdGPoxiPPh1WHY8VxpUVBv/2JsUtrB/rAIbGqZoxAIWvijJ
Pe9o1TY3VlOzk9ASZ1AeatvOir+iDVJ5OpKmLnzc46QgGPUsjIyo6Sje9dxpGtoG
QQIDAQAB
```

Refer to the API docs for more information.

:::note
Use the `docs/openapi.yml` OpenAPI specification to refer to each of the APIs mentioned above to create a token, keys, etc.
:::
