---
title: CI/CD Integration
description: Automatically updating policies with GitHub Actions.
author: Various
topic: tutorial
date: 08/1/2023
uid: tutorial.update.policies
---

*· 08/01/2023 ·*

## Update policies with GitHub actions

When a TEE-protected application is part of a continuous delivery (CD) workflow, the policies used to attest to the application's security often must also be a part of the CD workflow. Some of the application's attributes (for example, the `mrenclave` measurement) change every time an application is built. If updating the policy is not part of the CD workflow, the policy uses the attributes of the previous version to attest to the application's security. Appraisals of the unmodified policy will not match the new evidence. These instructions describe a sample GitHub Actions workflow that will automate the policy-updating process. This can be included in your CD workflow to keep your attestation policies up-to-date.

## Sample policy

These instructions assume familiarity with GitHub Actions.

:::note
This example assumes that you have an existing application that uses Software Guard Extensions (SGX) and that you have the `mrenclave` value for the enclave measurement available. An unsigned sample policy is provided below. We assume the sample policy is uploaded, and you know the policy ID. This policy will evaluate a number of claims during attestation, including the `mrenclave`, `mrsigner`, and other SGX claims. In this example workflow, we will update the `mrenclave` value only and leave the other evaluated values unchanged, as the `mrenclave` value will change every time the enclave code is rebuilt.
:::

```json
 {

 "policy": "default matches_sgx_policy = false \n\n matches_sgx_policy = true { \n input.sgx_is_debuggable == false \n input.sgx_isvsvn == 0 \n input.sgx_isvprodid == 0 \n input.sgx_mrsigner == \"d412a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b\" \n \n input.sgx_mrenclave == \"bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab\" \n }"
  "user_id": "f04971b7-fb41-4a9e-a06e-4bf6e71f98b3",
  "policy_name": "Sample_Policy_SGX",
  "policy_type": "Appraisal policy",
  "service_offer_name": "SGX Attestation",
  "service_offer_id": "b04971b7-fb41-4a9e-a06e-4bf6e71f98bd"
  }
```

## GitHub actions workflow

The following steps explain how to write a GitHub Actions workflow to update the `mrenclave` value in an existing policy. This example illustrates retrieving TEE information for an SGX application running in a [Gramine Shielded Container (GSC)](../Integration/integrate-gramine.md) with the integrated Trust Authority client. It uses the [Docker integration for Gramine](https://github.com/gramineproject/gsc) `gsc/gsc info-image` action to get the latest `mrenclave` value from a newly-built container image. This new value is used to update an existing appraisal policy so that the Trust Authority can attest the GSC enclave with the correct, updated value.

While this sample uses a Gramine Shielded container, it still represents a workflow useful for images not using a Gramine Shielded container.

1. The first step needs to acquire the Trust Authority tenant management [CLI utility](../Command-line/cli-install.md). Replace `run:wget path/to/executable` with the path and file name of the trustauthorityctl tool.

   ```bash
   name: get Trust Authority tenant CLI
   run:  wget path/to/trustauthorityctl
   ```

1. This job retrieves the policy to be updated and temporarily writes it to `policy.txt`. The GitHub Actions variable `vars.APPRAISAL_POLICY_ID` should be configured with the UUID of the appraisal policy to be updated.  The  variable `secrets.TENANT_ADMIN_API_KEY` should contain an Trust Authority Tenant Admin API key value.  Be sure this is configured as a "secret" value, as a Tenant Admin API key has expansive permissions beyond only updating a policy.

    ```bash
    name: retrieve policy
    run:  `trustauthorityctl list policy -a ${{ secrets.TENANT_ADMIN_API_KEY }} -p ${{ vars.APPRAISAL_POLICY_ID }} > policy.txt`
    ```

1. Retrieve the updated mrenclave value from the GSC image.

    In the example below, the `${repo}` variable represents the path to the image, including the registry URL (for example, `container-registry-sample.com/sample-imagename`). The `${tag}` variable represents the image tag.

    ```bash
    name: Update mrenclave hash
    run:  info=($(gsc/gsc info-image ${repo}:${tag}))
         if [ $? -ne 0 ]; then
           echo "Failed to collect gsc info from ${repo}:${tag}"
           exit 1
         fi

         mrenclave=$(echo ${info[2]} | tr -d '"'| xxd -r -p | base64)
    ```

1. Replace the `mrenclave` in the policy.

    ```bash
    name: Replace mrenclave value
    run:  sed -ri 's:mrenclave == "[a-zA-Z0-9]+":mrenclave == "'"$mrenclave"'":' policy.txt
    ``````

1.Update the policy in Trust Authority. This will overwrite the existing policy content, including the updated `mrenclave` value.

    ```bash
    name: update the policy in Trust Authority
    run:  trustauthorityctl update policy  -a ${{ secrets.TENANT_ADMIN_API_KEY }} -i ${{ vars.APPRAISAL_POLICY_ID }} -f policy.txt
    ```
