---
title: Getting Started
description: General quick start of the end-to-end management flow leading to a first attestation.
author: pcartee
topic: tutorial
date: 06/07/2024
uid: api.key
sidebar_position: 3
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

*· 06/07/2024 ·*

This page describes a quick sample workflow to cover the basic prerequisites so that you can generate your first attestation using Trust Authority.

## Admin API key management

Admin API Keys are needed to manage all non-attestation functions in Trust Authority. This includes creating Attestation API keys, inviting new users, changing user permissions, managing policies, and managing subscription levels.

:::note
Rotate the Admin API keys whenever a Tenant Admin user is removed, or "downgraded" to User. The Admin API keys previously accessible to the former Tenant Admin remain active and usable unless rotated.
:::

An admin API key is the only authorization required to execute nearly all REST APIs except attestation-related APIs, which require an attestation API key. (Thus, an admin API key can't be used to attest a TEE.) Nearly anything that can be done in the portal can also be done by using the [Trust Authority REST API](../Restapi/restapi-intro.md). An exception is retrieving the value of an attestation API key, which can only be done through the portal.

### View Admin API keys

1. Sign in to the Trust Authority portal.

    :::note
    The portal works best with Google Chrome, Microsoft Edge, Mozilla Firefox, and Safari.
    :::

1. Select **Admin API keys**.

1. View the API keys in the table.

    ![Admin API keys](/img/howto-manage-admin-api-keys/admin-api-keys.png)

### Copy Admin API keys {/* #admin-keys */}

1. Sign in to the Trust Authority portal.

1. Select **Admin API keys**.

1. Go to the API key to be copied.

1. Select the view ![View  icon](/img/common-graphics/view-icon.png) icon for the API key you want to copy.

    The API key is displayed.

1. Select the copy ![Copy icon](/img/common-graphics/copy-icon.png) icon.

    The API key is copied to your system memory.

1. The API key can be used with the **trustauthorityctl** CLI utility to manage admins and users.

<a id="attest-api-keys"></a>

## Attestation API Keys

Attestation API keys are used to authenticate attestation-related functions. Attestation functions include generating a new attestation token, creating a signed nonce, and requesting a Faithful Verification token audit report. An Attestation API key is required to accompany all attestation-related requests. An Attestation API key lets you attest any supported TEE.

You can create a new attestation API key in the portal or by using the REST API. You can only retrieve the new key value from the portal. This is to prevent a rogue client from creating and using a new attestation key. The only way a client can obtain and use a new attestation key is for a user with access to the portal to transfer the key to the client.

You can associate one or more attestation policies to an Attestation API key. The policies (if any) are applied to all attestation requests that are authorized by this key. Policies can also be specified in the attestation request, and in this case the policies specified with the attestation request replace the associated policies—that is, the associated policies are not evaluated; only the specified polices are evaluated. 

Attestation API keys may also have [tags](../How-to%20workflows/howto-manage-tags.md), which can be used for reporting and metrics visibility. All API keys have at least one tag, the default **Workload**.

<Tabs>
    <TabItem value="portal" label="Portal" default>

### Create an attestation API key

Any user can create attestation API keys available for all users within the tenant organization.

1. Sign into Trust Authority .

2. Select **Manage services**.

    ![Manage Services](/img/cli/manage-services-page.png)

3. Select **ADD API KEY**.

     The **Add API key** page displays.

     ![Add API key](/img/howto-manage-api-keys/add-api-key.png)

4. Provide a name for the API key. Names can be any string of up to 64 alphanumeric characters. Spaces and special characters other than "_" or "-" are not supported.

5. Optionally, assign one or more tags to the new API key. Tags are key-value pairs used to help track utilization for reports and metrics. The **Workload** tag is pre-defined. The workload tag can use values like an application's name to track the attestations requested by a given application.  See [Tag management](../How-to%20workflows/howto-manage-tags.md) for more details.

6. Optionally, assign one or more policies to the new API key. Use the **Select an existing policy** dropdown menu to choose from existing policies. Alternatively, you can create a new policy by selecting the **Create a new policy** radio button. See [Policy management](../How-to%20workflows/howto-manage-attestation-policies.md) for more details.

7. Once finished, select **SAVE & CONTINUE**.

8. Review the information on the **Confirm API key details** page.

9. If everything is correct, select **SUBMIT**.

   The new API key is created, along with any new tags and/or policies.
  </TabItem>

   <TabItem value="restapi" label="Rest API">

### Create an attestation API key

Creating an Attestation API key using the REST API requires an Admin API key for authentication.

1. Create and retrieve the IDs for tags and/or policies to be associated with this attestation API key (optional).

1. [Find the ServiceOfferId](../Restapi/restapi-service-offer-management.md)
1. [Retrieve the product ID](../Restapi/restapi-product-management.md) using the serviceOfferId
1. [Create a new API Client](../Restapi/restapi-client-management.md) using the POST method.

</TabItem>

</Tabs>

:::note
There might be a delay of up to two minutes before a new Attestation API key becomes active.
:::

## Requesting an Attestation

For this example we will attest an SGX enclave. Examples are provided using the REST API and the Golang client libraries.

<Tabs>
    <TabItem value="restapi" label="REST API">

### REST API

This option uses the Trust Authority REST API directly to request an attestation, but assumes you have an existing SGX application with an ability to retrieve an SGX quote.

1. Request a nonce

   ```bash
   curl --location 'https://api.trustauthority.company.com/appraisal/v1/nonce' \
     --header 'Accept: application/json' \
     --header 'x-api-key: <attestation API key>'
   ```

:::note
If you are in the European Union (EU) region, use the following Trust Authority URL

`curl--location 'https://api.eu.trustauthority.company.com/appraisal/v1/nonce`
:::
  
   Sample response:

   ```json
   {
    "val": "UHRKZ09RZFpxU3lCSzllS1FkbkgyMTFGN0ZNRHM4WERoR014b0Y0bENwUktaMDNrY2l3L2xjdmpCWW10eStLZERVWUtKSGRGRXI0THNMdkludEdsVFE9PQ==",
    "iat": "MjAyMy0wNi0xMiAyMDo0NDo0NiArMDAwMCBVVEM=",
    "signature": "kcnt3nLP0HhS0FMKnSB5pgZgDp0Pfar55MDt+lv9GqTrRi4lARaow/cGsPUJcK98Rcb6X2lxGtF8o2TP8AVMLANuqDga/QdpqR+vSfx523swM+ud1aJaTzbV4/o/lKSDSK/oV+Oe5o2IPfVKqedhXdJV/0xm51iMcESxw0wS8AnKliTRwsV9lCJujasAJIGt2LurLcuF89+DnXqo9p9WBUNv5vacjmz6p85Gun7VY9+5flWHBqEZTPWr4ddxHIOyUsOR31BtqgVIf5zFAKlLOUyrH4+ENUJADsnmBJmY5JIbaAFuetucj1dS5ISBTokrOSNUwrSeK0ktQoV7WV3yGdKrjwZS1vGEp85B0/ZUZAgwevsG9QhO8YPXIwbQ40bPUi/gssIogIpN6gC647YDGNqglHwlCopWFJE/O8D3k7f/ywHuNvCL1qYWjJbCdkrNLkBSUJ8eikcIiKqE/Dt2xMk+wiVsCK9nEkzLxzTeFRPayMQVRBRo9x4LLWzsybg2"
   }
   ```

1. Retrieve an SGX quote from an SGX-enabled application, including the actual quote and any enclave user_data/runtime_data. The nonce `val` and `iat` values from the nonce must be concatenated /* TODO clarify: nonce & runtime_data are concatenated and hashed - the hash goes in the quote, and the runtime_data ends up in an output claim in the token */ with any enclave runtime_data and included in the quote. For example:

`nonce.Val | nonce.Iat | runtime_data`

1. Request an attestation token
/* TODO update this to show the  policy must match option */

   ```bash
   curl --location 'https://api.trustauthority.company.com/appraisal/v1/attest' \
    --header 'Accept: application/json' \
    --header 'x-api-key: <attestation API key>' \
    --header 'Content-Type: application/json' \
    --data '{
        "quote": "<Full SGX quote>",
        "verifier_nonce": {
            "val": "<from nonce request>",
            "iat": "<from nonce request>",
            "signature": "<from nonce request>"
        },
        "policy_ids": [<optional list of additional policy IDs to appraise during attestation>],
        "runtime_data": "<SGX user_data from the SGX quote>"
    }'
   ```

  </TabItem>

  <TabItem value="go" label="Go client">

### Go client

This option uses the Trust Authority Golang client libraries to request a new attestation token. This example assumes you have integrated the Go client (including the `go-sgx` module) with an existing SGX-enabled application.

See the [Trust Authority client repo](https://github.com/trustauthority-client-for-go/tree/main) for more code samples.

1. Instantiate the client.

   ```go

    cfg := connector.Config{
            // Replace TRUSTAUTHORITY_URL with real Trust Authority URL
            BaseUrl: "TRUSTAUTHORITY_URL",
            // Replace TRUSTAUTHORITY_API_URL with real Trust Authority API URL
            ApiUrl: "TRUSTAUTHORITY_API_URL",
            // Provide TLS config
            TlsCfg: &tls.Config{},
            // Replace TRUSTAUTHORITY_API_KEY with real API key
            ApiKey: "TRUSTAUTHORITY_API_KEY",
            // Provide Retry config
            RClient: &RetryConfig{},
    }
   ```

1. Request a new signed nonce.

   ```go
   nonce, err := connector.GetNonce()
   if err != nil {
       fmt.Printf("Error getting nonce: %s\n\n", err)
       return err
   }
   ```

1. Collect evidence from the enclave.

   ```go
   adapter, err := sgx.NewEvidenceAdapter(enclaveId, enclaveHeldData, unsafe.Pointer(C.enclave_create_report))
   if err != nil {
       return err
   }

   evidence, err := adapter.CollectEvidence(nonce)
   if err != nil {
       return err
   }
   ```

1. Request an attestation token with nonce and evidence (note that no additional attestation policies will be evaluated unless the policyIds variable is set).

   ```go
   token, err := connector.GetToken(nonce, policyIds, evidence)
   if err != nil {
       fmt.Printf("Error getting attestation token: %s\n\n", err)
       return err
   }
   ```

1. Check the validity of the attestation token. This includes checking the token's issue time and signature.

   ```go
   //Download the token signing certificates
   jwks, err := connector.GetTokenSigningCertificates()
   if err != nil {
       fmt.Printf("Something bad happened: %s\n\n", err)
       return err
   }

   parsedToken, err := connector.VerifyToken(string(token))
   if err != nil {
       fmt.Printf("Error verifying token: %s\n\n", err)
       return err
   }
   ```

 </TabItem>

</Tabs>

## Changing your password

After changing your password, you may be unable to log back into the Trust Authority portal. If this occurs, close all your browser windows. A fresh browser will enable you to log in with the updated password. If you still have trouble logging in, please contact support.
