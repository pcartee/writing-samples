---
title: Intel Trust Authority CLI Policy Management
description: Intel Trust Authority CLI policy management commands.
author: pcartee
topic-type: Reference
date: 08/15/2023
uid: cli-policy-commands
---

*· August/15/2023 ·*

## Policy management

This section provides commands to create, get, and update an Intel Intel® Trust Authority policy.

:::note
You need a Tenant Admin API key to perform these commands. To retrieve your admin API keys, follow the [Copy Admin API keys](../Quickstart/tutorial-api-key.md) instructions on the Getting Started page.
:::

## Create a policy

This command creates a new policy.

`trustauthorityctl create policy -n < name of policy > -t < policy type > -a < attestation type > -r < service offer id > -f < rego policy file path >`

:::note
The policy file size should be less than 10KB.
:::

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

## Get policies

This command retrieves a list of your Intel Trust Authority policies.

`trustauthorityctl list policy `

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

## Get policy by ID

This command retrieves a specific Intel Intel Trust Authority policy by `policy ID`.

`trustauthorityctl list policy -p < policy id >`

### Sample call

```bash
trustauthorityctl list policy -p 1f1f13e0-9fb1-4a57-baa42-361d86157fa3
```

### Sample response

```bash
trace-id:  LOoKzEtEIAMEKOQ=
Policies: 

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
  "created_time": "2023-09-14T04:07:14.39122Z",
  "modified_time": "2023-09-14T04:07:14.39122Z",
  "policy_hash": "cwaOYwsylekTKYQHRaoo3yMdCIepkNE0VNZT8igvgKTO9LQsQE96yOQTydEkToog",
  "policy_signature": "FLakjTY4KJOA0gsjO/MwN4JpIaRpiDZ/DaLt9Qne8RBml4TJrcFSNHimIkpKUQVog4O+Hw1C12/6TqupYucQvukW87JtJSM6dBA8lTa8dHtBSFH5IW7d10z0YLDPD1L7B/3ztDsJcCI28zFgmAPHjv71IqtnmCaEKV9IJJUSqkziuuitK9jmGSvsnEI7kwQ960gcOEjjfqZKjBTGoxjurI5mWY0797Y+rUhuzQyXphbHJekZVUln1895lvMHwSBbm5iKMzjYwqNwxjwI+TDdJ6GbaD3yxgdxHmTuZ3R4I54MGjVvpkGAFPsVsCBHtkl9AZY6gxMRMeLYa0KfTgWppbF8DO2jva/o6374uoe2rncaKNvkUBeQ7eMAu8uXvmDeFSTzZH/AsKrnvvjcdUe0tD5aAo3YHTyLZUkh3j/naW+65r6OsuvfT9fAcigHDuWtQ9IdzrEIRIaixVBLvkwocFYzFBix8FwwNIN1263suSg6ilmfuUhVkAEIElXwQ31F"
}
```

## Update a policy

The following command update your existing attestation policy.

`trustauthorityctl update policy -i < policy id > -n < name of policy > -f < rego policy file path >`

:::note
The policy file size should be less than or equal to 10KB.
:::

### Sample call

```bash
trustauthorityctl update policy -n Sample_Policy_SGX -f sgxpolicyupdated.txt -i e48dabc5-9608-4ff3-aaed-f25909ab9de1
```

:::note

The updated policy replaces the entire existing policy. Be sure to upload the entire replacement policy rather than updating only specific elements.

:::

### Sample response

```bash
trace-id:  LOoLdGRMoAMEBgA=
Updated policy: 

            {
  "policy_id": "1f1f13e0-9fb1-4a57-ba42-361d86157fa3",
  "policy": "default matches_sgx_policy = true\nmatches_sgx_policy = true {\ninput.sgx_mrenclave == \"83f4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204420\"\ninput.sgx_mrsigner == \"83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e\"\n}\n",
  "policy_name": "TestPolicySGX123",
  "policy_type": "Appraisal policy",
  "service_offer_id": "d47f9540-5bd6-47ff-b984-5fcf0d74c6e2",
  "attestation_type": "SGX Attestation",
  "creator_id": "4f8bb24f-2f4e-4855-a4e5-57a6c181ea01",
  "updater_id": "4f8bb24f-2f4e-4855-a4e5-57a6c181ea01",
  "deleted": false,
  "created_time": "2023-09-14T04:07:14.39122Z",
  "modified_time": "2023-09-14T04:07:49.87309683Z",
  "policy_hash": "Lb8dttYGnxdFN4QafS/RuGOrMffZK19jPgZUT/n6MDGO1Sbe3gHW+2C/o3FSS/TX",
  "policy_signature": "mgi9a5SIM9Ikw2Lx0THMp2SKi5cPAmppAz4lWxAfhLssHa3o+wAVjaxJLvdW8syHKgvTz33SnNQTURIv/dDze0odcu96vSyqUkhylLB60d61beqXYyB5XrjDYRT7B2Sr5NR5Lt4LuVLfRMnDFDWLXE8mCSKPGhOAsCADYTQ7X/KDzlvUK2VApBZ3/VoSwTa23AbI6iPsR52wNA7poKvO0PBK4H8ux3gv2glas2zQVLFQmsbnhSMMjmZotnSDFKWdldeNeuD7UQU6LowNjSXjG/JOWDIytsdOq1+ce/jX9UnHQeh8S7Wp4Xo5QK6Gd1Urc8DAZYk7s89qPV8jcrW/28FBzaYXQGjZJsWxRzZp15C4m3retcUajGiIsRO7fe/jrLqABLSEv+x/yYX9cpyxLnoPNuNzGi7oh1YOdIwHxL2+iX8OZdYWDZABTLm9ZWKRFocI7BqZ9GAMd8bkbtAZhQSBVSrupJ9F3KI1EOz28q/YigsqzCpzJgrzv/9rxjML"
}
```

## Delete policy

This command deletes a specific policy.

`trustauthorityctl delete policy -p < policy id >`

### Sample call

```bash
trustauthorityctl delete policy -p e6g83s7k-l82n-3o6z-537w-g4gt35khjfd4
```

### Sample response

```bash
trace-id:  LOoOVGU5IAMEZ2g=
Policy e6g83s7k-l82n-3o6z-537w-g4gt35khjfd4 deleted
```
