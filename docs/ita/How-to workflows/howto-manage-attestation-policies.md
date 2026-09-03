---
title: Policy management
description: An overview of attestation policies.
author: pcartee
topic: how to
date: 12/09/2024
uid: manage.attestation.policies # Do not change uid!
---

*· December/09/2024 ·*

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Attestation policy management

This article contains sample workflows for managing attestation policies. See the [Policies](../Concepts/concept-policies.md) article for additional details on using policies.

## Policy Types

There are two types of policies, Appraisal and Token customization. Appraisal policies evaluate the evidence provided and determine whether Trust Authority issues an attestation token. A Token customization policy allows customized claims that are part of the attestation token.

Each policy type can be signed or unsigned. A signed policy assures the relying party that the signed policy is unchanged. Policies can be managed using the following:

- Trust Authority portal
- [TrustAuthority CLI](../Command-line/cli-policy-commands.md)
- [REST API](../Restapi/restapi-policy-management.md)

Policies can be managed using the Trust Authority portal, with the [client CLI](../Command-line/cli-policy-commands.md), or by [REST API](../Restapi/restapi-policy-management.md).

<Tabs>
<TabItem value="manage-policies-ui" label="Trust Authority Portal">

## View policies

You can view the list of policies using one of the following methods.

1. Sign in to the Trust Authority portal.

1. Select **Manage policies**. A list of attestation policies displays in the Policy Library pane.

    ![View Policies](/img/howto-manage-attestation-policies/policy-detail.png)

## Search by policy name

1. Sign in to the Trust Authority portal.

1. Select **Manage policies**.

1. In the **Search by policy name:** box, enter the policy name. The search is incremental. It begins after the first letter is entered.

    The search results are displayed in the Policy Library pane.

## Filter by attestation type

1. Sign in to the Trust Authority portal.

1. Select **Manage policies**.

1. Select the attestation type from the **Filter by attestation type:** dropdown list.

    The search results are displayed in the Policy Library pane.

## Create a policy
These instructions describe how to create a policy using the Trust Authority portal.

:::note
For more information on creating a policy see the [Author a custom policy](howto-author-custom-policy.md) article.
:::

1. Sign in to the Trust Authority portal.

1. Select **Manage policies**.

1. Select **ADD A POLICY**.

1. Enter a **Policy name**.

    ![View Policies](/img/howto-manage-attestation-policies/add-policy.png)

1. Select the attestation type you want from the **Choose an attestation type** dropdown list.

1. Select a policy type for the selected attestation.

1. Select **BROWSE**.

    ![Upload the policy](/img/howto-manage-attestation-policies/upload-policy.png)

1. Go to the policy.

1. Select the policy and then select **Open**.

1. Select **SAVE**.

    The Manage Policies page displays with the new policy displayed in the Policy Library pane.

## Edit a policy

1. Sign in to the Trust Authority portal.

1. Select **Manage policies**.

1. Select the ![edit ](/img/common-graphics/edit-icon.png) icon for the policy you want to edit.

1. Select **EDIT POLICY**.

    ![Edit Policy](/img/howto-manage-attestation-policies/edit-policy.png)

1. You can edit the following:

    - Policy name
        1. In the Policy name box, enter a new name for the policy.

    - Assign a new policy file
        1. Select **BROWSE**.

        1. Go to the policy file.

        1. Select the policy file and then select **Open**.

1. After your changes are made, select **SAVE**.

## Delete a policy

1. Sign in to the Trust Authority portal.

1. Select **Manage policies**.

1. Select the ![delete](/img/common-graphics/delete-icon.png) icon for the policy to be deleted.

1. Select **DELETE POLICY**.

    The policy is deleted.

## Sign a policy

See the [Policy Signing Tool](../Utilites/utility-policy-signing.md) article for instructions on signing a policy.

</TabItem>
<TabItem value="manage-policies-cli" label="CLI">

## Policy management

This section provides commands to create, get, and update a Trust Authority policy. For more information on creating a policy, see the [Author a custom policy](../How-to%20workflows/howto-manage-attestation-policies.md) article.

:::note
You need a tenant admin API key to perform these commands. See the [Retrieve Admin API key](../Command-line/cli-examples.md#retrieve-admin-api-keys) article for more information.
:::

## Create a policy

This command creates a new Trust Authority policy.

:::note
The policy file size must be less than 10KB.
:::

To create this policy you need:
- the file path to where the policy is to be stored
- the attestation type of the policy
- the id of the service offer to which this policy will be assigned

:::note
For more information on creating a policy see the [Author a custom policy](../How-to%20workflows/howto-author-custom-policy.md) article.
:::

```bash
trustauthorityctl create policy -n < name of policy > -t < policy type > -a < attestation type > -r < service offer id > -f < rego policy file path >
```

### Sample call

```bash
trustauthorityctl create policy -n TestPolicySGX123 -t "Appraisal policy" -a "SGX Attestation" -r d47f9540-5
5bd6-47ff-b984-5fcf0d74c6e2 -f sgxpolicyAppraisal.txt   
```

### Sample response

```bash
trace-id:  LOoF5EEbIAMEZRw=
Policy: 

 {
  "policy_id": "1f1f13e0-9fb1-4a57-ba42-361d86157fa3",
  "policy": "default matches_sgx_policy = true\nmatches_sgx_policy = true {\ninput.sgx_is_debuggable == true\ninput.sgx_mrenclave == \"83f4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204412\"\ninput.sgx_mrsigner == \"83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e\"\n}\n",
  "policy_name": "TestPolicySGX123",
  "policy_type": "Appraisal policy",
  "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
  "attestation_type": "SGX Attestation",
  "creator_id": "4f8bb24f-2f4e-4855-a4e5-57a6c181ea01",
  "updater_id": "4f8bb24f-2f4e-4855-a4e5-57a6c181ea01",
  "deleted": false,
  "created_time": "2023-09-14T04:07:14.391220115Z",
  "modified_time": "2023-09-14T04:07:14.391220115Z",
  "policy_hash": "cwaOYwsylekTKYQHRaoo3yMdCIepkNE0VNZT8igvgKTO9LQsQE96yOQTydEkToog",
  "policy_signature": "FLakjTY4KJOA0gsjO/MwN4JpIaRpiDZ/DaLt9Qne8RBml4TJrcFSNHimIkpKUQVog4O+Hw1C12/6TqupYucQvukW87JtJSM6dBA8lTa8dHtBSFH5IW7d10z0YLDPD1L7B/3ztDsJcCI28zFgmAPHjv71IqtnmCaEKV9IJJUSqkziuuitK9jmGSvsnEI7kwQ960gcOEjjfqZKjBTGoxjurI5mWY0797Y+rUhuzQyXphbHJekZVUln1895lvMHwSBbm5iKMzjYwqNwxjwI+TDdJ6GbaD3yxgdxHmTuZ3R4I54MGjVvpkGAFPsVsCBHtkl9AZY6gxMRMeLYa0KfTgWppbF8DO2jva/o6374uoe2rncaKNvkUBeQ7eMAu8uXvmDeFSTzZH/AsKrnvvjcdUe0tD5aAo3YHTyLZUkh3j/naW+65r6OsuvfT9fAcigHDuWtQ9IdzrEIRIaixVBLvkwocFYzFBix8FwwNIN1263suSg6ilmfuUhVkAEIElXwQ31F"
}
```

## List policies

This command retrieves a list of your Trust Authority policies.

```bash
trustauthorityctl list policy
```

### Sample call

```bash
trustauthorityctl list policy
```

### Sample response


```bash
trace-id:  LOoKsGIhIAMEFAA=
Policies: 
      [
        {
          "policy_id": "41677eb9-023d-402d-9966-909cdfff0889",
          "policy": "default matches_sgx_policy = false \n\n matches_sgx_policy = true { \n input.sgx_is_debuggable == false \n input.sgx_isvsvn == 0 \n input.sgx_isvprodid == 0 \n input.sgx_mrsigner == \"d412a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b\" \n \n input.sgx_mrenclave == \"bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab\" \n }",
          "policy_name": "Policy1SGXUsername",
          "policy_type": "Appraisal policy",
          "service_offer_id": "dca3fa42-a8e6-4eb6-bb3f-799d917bc529",
          "service_offer_name": "SGX Attestation",
          "creator_id": "00000000-0000-0000-0000-000000000000",
          "updater_id": "00000000-0000-0000-0000-000000000000",
          "deleted": false,
          "created_time": "2022-10-14T10:12:07.993695Z",
          "modified_time": "2022-10-14T10:12:07.993695Z",
          "policy_hash": "l5BKcCbuinJ7bPKnrp7g9TQhxQewoRRwK2ZKQJhUutKlrVeCHtyMvnV8ik2+iiEh",
          "policy_signature": "kIocVNQa9M6s5S9rE+cysBgNV63E6xLZ0bxKyExCAPkENWbXBU/9njt0FznpRuOziEUUKEaylx/7NpwdHsYKDUfirN3Owg26IbBUU/YOakqEFRWkkOJbvV//V/TCq4bNRIeschnIPWSVCmvOrAgexI5UwDbGgul6W+445TWm4WBOq+LIvZrQxFRVRPsdL1R0UqA3BGsggcCmOoSG3lK2dnV/SKM6EtHMiyT5e11M/TycJny04NQT7vm0jpkKV7hN2VdKorsAXsE4ffQp0BOwv/CjXoyRiuwWVEUwTQS5avS5vggyx1X46xApS7PWnYCZbRaBg/jmBNfNhCyvkD/EFAxubuNGwgDkppow1kltgKtRMtgvh8xLpRjmTLvhoZlzwrOV4136j49XFkhZE8zBl3qMh2k7OfWgYzzcfTb9kidCpMWX5Xf7x3eObyNPZ2GK1pql4ksOPG7SuaBqP75VOG40I0iGW33JxtMqZZaUZFRSJXzzVIlfvnuhgLhOwFQO"
        },
        {
          "policy_id": "4309afa9-9302-4efa-b95b-6a2e93e4f01a",
          "policy": "get_token_fields[token_fields] { \n token_fields := { \n \"dd-isv-svn\" : input.sgx_isvsvn, \n } \n }",
          "policy_name": "policy3210",
          "policy_type": "Token customization policy",
          "service_offer_id": "6c5a8f51-6259-4819-8d18-919b19f7a2e4",
          "service_offer_name": "SGX Attestation",
          "creator_id": "00000000-0000-0000-0000-000000000000",
          "updater_id": "00000000-0000-0000-0000-000000000000",
          "deleted": false,
          "created_time": "2022-10-06T23:42:59.535117Z",
          "modified_time": "2022-10-06T23:42:59.535117Z",
          "policy_hash": "/jVF9bCseJqqhFqWHAK7miMjhun1AcP92G0vywxEnW9PFfMeDhMbsJUJLLDHt7AJ",
          "policy_signature": "FqIm1m6YzZNbdXXHeDiBvFI8/oLgy8z7NeRfodRTMPu+r6I7IRd6KHL0W7+4wkKjWtG/HUmifQmDl1YUzicHgY3RjJcej7yXo1U2oYXlbYchrdPu4tRyLGW+YvZJv7wE/xB95IDIRRTR5d+CfZkL7/rDB6y4b1QBmO4x9FF0GkGITrdJJFXXFtLO+BCZqEcmavC9iqJns8QFjo03rO3fmTpUpr2kkN7kl35o0tD4nBlEZYqi2KYsgzvTh5StK7/2rQ3Fb/AcLEe3b84SJM6wEqoMG91z1XV52Wr5SI1zm2CAGeOb239pnLKKLFajvBRAK66FQ53wRYvRzC9jAPvzMOiRplsh3Gw5dHpaRZTjkpveH5X6fkZ24bgzZPeJYKsqI4J/GWaiMfN9BzkNfXIW73mY4ogVU2qIOCnTa6p2zucTusPrYmfTQn0bCFYpAZVgWOhvS9Nqt0r4OSfU7SXdvvPADY2ac0Yt5qDDQc6ypN3acIwKbsav/NKHfGPjR47K"
        }
      ]
```

## List policy by ID

This command retrieves a specific Trust Authority policy by `policy ID`.

```bash
trustauthorityctl list policy -p < policy id >
```

### Sample call

```bash
trustauthorityctl list policy -p e6g83s7k-l82n-3o6z-537w-g4gt35khjfd4
```

### Sample response

```bash
trace-id:  LOoKzEtEIAMEKOQ=
Policies: 
{
  "policy_id": "c3c77a2d-f71c-4e1c-96b5-c6fc29fecee2",
  "policy": "default matches_sgx_policy = false \n\n\n matches_sgx_policy = true {   \n input.amber_sgx_mrenclave == \"30d4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204410\" \n input.amber_sgx_mrsigner == \"83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e\" \n input.amber_sgx_is_debuggable == false } ",
  "policy_name": "Policy935",
  "policy_type": "Appraisal policy",
  "service_offer_id": "80898b5f-f8e3-4240-a6ad-8cbe72f23110",
  "service_offer_name": "SGX Attestation",
  "creator_id": "00000000-0000-0000-0000-000000000000",
  "updater_id": "00000000-0000-0000-0000-000000000000",
  "deleted": false,
  "created_time": "2022-10-14T01:19:27.987355Z",
  "modified_time": "2022-10-14T01:19:27.987355Z",
  "policy_hash": "ekbxp/xHnmxD/R3wojOcl5m1t1c6CV7xGDhnQGs0vEKyv3jyLhC1s4l8zXnjWT9o",
  "policy_signature": "SCkuDxFFjB4KTEEWssdwVjjurK4Y+8tbT4SKSNWJO816mJyndG+UU8sMlsPTWXncG53vSa6sF1zh/L86lHzMQXwcRobQWFjTWmjNqYzV+apUilPLGH/ksXw8iEmAh8+cZUzdv/l4O6lO1J6lXdkFI65QIUsbDk6Nr3SEOjX/Ord3ShoTZvEYf7/Vp+U5+IBaxEu/NVWnjlFkpUwa6UGiC6b9L6vVo11jHY7SJs/weeSTYKvlT/o7TVHHDoZMUZPAFaZt6VoQuQ/WBBSU31T+tq1ZUMQLdt5YzyLaC418ueuROVkwrM8DMs8+69f+dpvZ53udSu9bnOKhm8erYnCHecoukZANLZRR9P1lRA6ZXUPcfZSm+WwGR/28PX16KcMyVpYWYrUvmHcTFzPy8aK0a+yFaNRbXdsl/YrCNfChzT9Fdg2SY0QeuHIrW5DRXcZAMZa8VL0jDULtVndxSlnPCBGueV/i0g8TqdDs8N6u4LhhvddyDEnB8Y998FFjXdJc"
}
```

## Update a policy

The following command updates your existing attestation policy.

```bash
trustauthorityctl update policy -i < policy id > -n < name of policy > -f < policy file path >
```

### Sample call

```bash
trustauthorityctl update policy -i e48dabc5-9608-4ff3-aaed-f25909ab9de1 -n Sample_Policy_SGX -f sgxpolicyupdated.txt
```

### Sample response

```bash
trace-id:  LOoLdGRMoAMEBgA=
Updated policy: 
            {
      "policy_id": "e48dabc5-9608-4ff3-aaed-f25909ab9de1",
      "policy": "default matches_sgx_policy = false \n\n matches_sgx_policy = true { \n  input.amber_tee_is_debuggable == false \n input.amber_sgx_isvsvn == 0 \n input. amber_sgx_isvprodid == 0 \n input.amber_sgx_mrsigner ==   \"d412a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b\" \n  \n input. amber_sgx_mrenclave ==  \"bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab\" \n }",
      "user_id": "f04971b7-fb41-4a9e-a06e-4bf6e71f98b3",
      "policy_name": "Sample_Policy_SGX",
      "policy_type": "Appraisal policy",
      "service_offer_name": "SGX Attestation",
      "service_offer_id": "b04971b7-fb41-4a9e-a06e-4bf6e71f98bd"
      }
```

## Delete policy

This command deletes a specific policy.

```bash
trustauthorityctl delete policy -p < policy id >
```

### Sample call

```bash
trustauthorityctl delete policy -p e6g83s7k-l82n-3o6z-537w-g4gt35khjfd4
```

### Sample response

```bash
trace-id:  LOoOVGU5IAMEZ2g=
Policy e6g83s7k-l82n-3o6z-537w-g4gt35khjfd4 deleted
```

# Signed policy management

This section provides commands to create signed attestation policies for Trust Authority with or without using a key, certificate, and encryption algorithm.

:::note
The [Policy Signing Tool](../Utilites/utility-policy-signing.md) performs the same function. If you signed a policy with the policy signing tool, you do not need to sign the policy again.
:::


## Create signed JWT attestation policies

The following command creates a new signed policy with a key, certificate, and encryption algorithm.

```bash
trustauthorityctl create policy-jwt -f < policy file path > -p < signing key path > -c < cert path > -a < algorithm > -s
```

### Sample call

```bash
trustauthorityctl create policy-jwt -f sgxpolicy.txt -p policyjwt/trustauthority-jwt.key -c policyjwt/trustauthority-jwt.crt -a RS384 -s
```

### Sample response

```bash
Original policy:
default matches_sgx_policy = false
matches_sgx_policy = true
{  input.amber_tee_is_debuggable == false
   input.amber_sgx_isvsvn == 0
   input.amber_sgx_isvprodid == 0
   input.amber_sgx_mrsigner ==  "d912a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b"
   input.amber_sgx_mrenclave == "bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab"
} Algorithm used during signing:  RS384
Policy token is stored in file  sgxpolicy.signed.20230321040145.txt
Policy token generated:
eyJ...gkw
```

## Create signed JWT attestation policies with the default algorithm

The following command creates a new signed policy with a key, certificate, and the default algorithm.

```bash
trustauthorityctl create policy-jwt -f < policy file path > -p < signing key path > -c < cert path > -s
```

### Sample call

```bash
trustauthorityctl create policy-jwt -f sgxpolicy.txt -p policyjwt/trustauthority-jwt.key -c policyjwt/trustauthority-jwt.crt -s
```

### Sample response

```bash
Original policy:
default matches_sgx_policy = false
matches_sgx_policy = true
{  input.amber_tee_is_debuggable == false
   input.amber_sgx_isvsvn == 0
   input.amber_sgx_isvprodid == 0
   input.amber_sgx_mrsigner ==  "d912a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b"
   input.amber_sgx_mrenclave == "bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab"
} Algorithm used during signing:  PS384
Policy token is stored in file  sgxpolicy.signed.20230321040159.txt
Policy token generated:
eyJ...0kJ-
```

## Create an unsigned JWT attestation policy

The following command creates a new unsigned policy without a key, certificate, or any encryption algorithm. Unsigned JWT policies can be used with some 3rd-party integrations.

```bash
trustauthorityctl create policy-jwt -f < policy file path >
```

### Sample call

```bash
trustauthorityctl create policy-jwt -f sgxpolicy.txt
```

### Sample response

```bash
Original policy:
default matches_sgx_policy = false
matches_sgx_policy = true
{  input.amber_tee_is_debuggable == false
   input.amber_sgx_isvsvn == 0
   input.amber_sgx_isvprodid == 0
   input.amber_sgx_mrsigner ==  "d912a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b"
   input.amber_sgx_mrenclave == "bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab"
} Algorithm used during signing:  None
Policy token is stored in file  sgxpolicy.signed.20230321040138.txt
Policy token generated:
eyJhbGciOiJub25lIn0.eyJBdHRlc3RhdGlvblBvbGljeSI6ImRlZmF1bHQgbWF0Y2hlc19zZ3hfcG9saWN5ID0gZmFsc2UgXG5tYXRjaGVzX3NneF9wb2xpY3kgPSB0cnVlIFxueyAgaW5wdXQuYW1iZXJfdGVlX2lzX2RlYnVnZ2FibGUgPT0gZmFsc2UgXG4gICBpbnB1dC5hbWJlcl9zZ3hfaXN2c3ZuID09IDAgXG4gICBpbnB1dC5hbWJlcl9zZ3hfaXN2cHJvZGlkID09IDAgXG4gICBpbnB1dC5hbWJlcl9zZ3hfbXJzaWduZXIgPT0gIFwiZDkxMmE0ZjA3ZWY4Mzg5MmE1OTE1ZmIyYWI1ODRiZTMxZTE4NmU1YTRmOTVhYjVmNjk1MGZkNGViODY5NGQ3YlwiIFxuICAgaW5wdXQuYW1iZXJfc2d4X21yZW5jbGF2ZSA9PSBcImJhYjkxZjIwMDAzODA3NmFjMjVmODdkZTBjYTY3NDcyNDQzYzJlYmUxN2VkOWJhOTUzMTRlNjA5MDM4ZjUxYWJcIiBcbn1cbiJ9.
```
</TabItem>
<TabItem value="manage-policies-rest" label="REST API">

## Policy Management

Policy Management enables users to create and manage rules that inspect the quote generated and submitted by the client/workload during execution. The Policy Management allows Users to Create, Update, Delete, and Search SGX and TDX policies. The policies have an attestation-specific OPA format defined in Rego language and are stored as JSON.

There can be two types of policies - Appraisal or Token customization. The Appraisal policy includes details like server firmware measurements, hardware capabilities, security technology information, and additional workload-specific parameters. Token customization policy includes user-defined fields to be
populated in the issued Attestation Token.

Policy(s) are applied and verified against the quote\evidence provided by the client during the attestation request. The output returned is a signed JWT token that can be parsed to verify the policies evaluated.

:::note
For more information on creating a policy see the [Author a custom policy](../How-to%20workflows/howto-author-custom-policy.md) article.
:::

</TabItem>
</Tabs>
