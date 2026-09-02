---
title: Trust Domain Integrity
description: Instructions for creating policies.
author: pcartee
topic: Conceptual
date: 03/26/2025
uid: td.integrity
---

*· 03/26/2025 ·*

## Trust Domain Integrity Overview 

:::note
This feature is in pre-release status. For preview access, please contact your Intel sales representative. Details of implementation and usage may change before general availability.
:::

Trust Domain Integrity (TD Integrity) is a feature of Intel® Tiber™ Trust Authority that remotely attests the system components of an Intel® Trust Domain Extensions (Intel® TDX) Trust Domain (TD). A TD is a virtual machine that has its memory and CPU state protected from the underlying bare-metal host by Intel TDX. In this document, Trust Domains are also referred to confidential virtual machines (CVM).

Remote attestation of CVMs is an integral piece of confidential computing workflows that, for example, can be used to securely release secrets such as protected data, certificates, etc into cloud-based workloads. TD integrity is supported for Intel TDX-based CVMs running on Microsoft Azure\* and Google Cloud Platform\* (GCP).

By using Intel® TDX, security professionals can establish a “chain of trust” to ensure the security posture of their cloud-based workload. A chain of trust is established when each component or "link" of the CVM system from the underlying host's Intel TDX Hardware Root of Trust (HRoT) to the operating system is independently verified and trusted, thereby establishing the integrity of the remote TD. Each component attests the next component in the chain. This is also referred to as a _measured boot_, because every critical step of the boot process is cryptographically measured and logged. The boot logs may be replayed to verify certain claims made in the evidence collected from the TD.

In summary, Intel TDX TD Integrity establishes a chain of trust that ensures the trustworthiness of confidential virtual machines running on Azure and GCP CVMs with Intel TDX.

## The TD Integrity solution stack

The diagram below summarizes the various components and artifacts needed to establish TD integrity for a cloud-based workload.

![Cloud-based Intel TDX CVM attestation diagram](/img/concept-td-integrity/cloud-tdx-cvm-attestation.png)

The key takeaways from the above diagram are as follows:

- TD Integrity establishes a chain of trust from the underlying host's Intel TDX HRoT, through the TD's virtual bios, boot loader, and operating system. TD Integrity doesn't verify the application workload.
- Intel Trust Authority provides [client libraries and tools](../Integration/integrate-go-tdx-cli.md) to simplify the collection of evidence from an Intel TDX CVM.
- Intel Trust Authority verifies the evidence collected from the TD and then utilizes appraisal policies to enforce TD integrity. 
- Intel Trust Authority returns a signed attestation token (a JWT) that can be used by a relying party to verify the identity and integrity of the attesting TD/CVM.
- The tenant administrator must configure TD Integrity by manually downloading the **td-integrity.txt** file and then using the file to create a new TD Integrity policy. 

## Cloud-specific chains of trust

The following sections describe how the chain of trust is defined for Azure and GCP CVMs with Intel TDX.

### Azure TD Integrity

The diagram and table below depict the TD Integrity chain of trust on Azure CVMs with Intel TDX.

![Azure CVM chain of trust](/img/concept-td-integrity/azure-cvm-tdi.png)  

|Component            |Evidence Source/Collection             |Verification                       |
| :-------------------| :-------------------------------------| :---------------------------------|
|Intel® TDX           |The client collects Azure TDX quotes via vTPM (as designed by Azure).|Intel Trust Authority verifies the integrity of quote signatures against PCS collaterals. |
|vTPM                 |The client collects Azure **runtime-data** JSON evidence.|The integrity of **runtime-data** is checked against the Intel TDX quote's **report_data** hash.  The **runtime-data** contains the vTPM's AK public key and that is used to very vTPM quotes.|
|Virtual BIOS|Intel TDX quotes.|The virtual BIOS is compared against a known Intel TDX **MRTD** reference value that reflects the initial "golden" state of the CVM at boot time.|
|Operating System|UEFI event logs|The UEFI event logs are replayed for integrity against the verified TPM quote and PCRs. Those logs include measurements of the kernel image which is compared against a known reference value.|

### GCP TD Integrity
The diagram and table below depict the TD Integrity chain of trust on GCP CVMs with Intel TDX.

![GCP CVM chain of trust](/img/concept-td-integrity/gcp-cvm-tdi.png)  

|Component            |Evidence Source/Collection             |Verification                       |
| :-------------------| :-------------------------------------| :---------------------------------|
|Intel® TDX           |The client collects Intel TDX quotes via the ConfigFS-TSM interface.|Intel Trust Authority verifies the integrity of Intel TDX quote signatures against PCS collaterals.|
|Virtual BIOS         |TDX quotes.                            |The virtual BIOS is compared against a known Intel TDX **MRTD** reference value that reflects the initial "golden" state of the CVM at boot time.|
|Operating System     |UEFI event logs                        |The UEFI event logs are replayed for integrity against the TDX quote's **RTMR** values. Those logs include measurements of the kernel image which is compared against a known reference value.|


## Setup instructions

The following sections describe how to use Intel Trust Authority to verify the TD integrity for Azure and GCP CVMs with Intel TDX.

### Create a TD Integrity appraisal policy

1. Visit the [Intel® Tiber™ Trust Authority TD Integrity repo (intel / trustauthority-td-integrity)][tdi-repo] and follow the instructions for downloading **td-integrity.txt**. 
1. Sign in to the Intel Trust Authority portal.
1. Create a new policy by uploading **td-integrity.txt** to the portal. For detailed instructions, see [Create a policy](../How-to%20workflows/howto-manage-attestation-policies.md#create-a-policy).
1. Create a new Attestation API Key, or edit an existing API key. This key is referred to as `api-key` in the following instructions.
   1. Under **Assigned policies (Optional)**, select your TD Integrity policy. Choose **Save & Continue**. Your screen should look something like this:
      ![Confirm API key details](/img/concept-td-integrity/api-key-details.png)
   1. Ensure that your TD Integrity policy appears in the list of assigned policies. Tags are optional. Choose **Submit**.

This concludes the Intel Trust Authority portion of TD Integrity setup.

Instead of assigning the TD Integrity policy to an API key, you could rely on the attester to include the TD Integrity policy ID with the token request (for example, by using the `--policy-ids` option of the **token** command). We don't recommend relying on the client to ensure that the TD Integrity policy is appraised. We recommend that you assign the TD Integrity policy to the Attestation API Key (or keys, if you use more than one) you'll use to attest CSP CVMs. This method ensures that the TD Integrity policy is always appraised during attestation.

It's a good practice for the relying party to check that all required appraisal polices were applied during attestation. If you only want to check that all policies assigned to the API key were matched, you can check the **policy_ids_unmatched** section; it should be empty. Assuming that you trust the tenant administrator to correctly assign the TD Integrity policy to the API key, and that you're using the correct API key for attestation, a simple check of unmatched policy ids is sufficient to determine that the TD Integrity policy was appraised.

### TD Integrity for Azure CVMs with Intel TDX

1. Create an Azure CVM with Intel TDX. For more information, see [Creating a VM with TDX on Microsoft Azure](../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-tdx.md#creating-a-vm-with-tdx-on-microsoft-azure)
1. Install trustauthority-cli (v1.9+):  
   ```bash
   curl https://raw.githubusercontent.com/intel/trustauthority-client-for-go/main/release/install-tdx-cli.sh | sudo bash -
   ```
1. Create a **config.json** as described in [Attestation Client CLI](../Integration/integrate-go-tdx-cli.md#configuration)). **Note**:  the **config.json** requires `cloud_provider: azure` for Azure CVMs with Intel TDX.
1. Run `trustauthority-cli`, collecting Intel TDX and vTPM composite evidence and requesting a token by using the following command.
   ```bash
   sudo trustauthority-cli token --tdx --tpm --evl -c config.json --no-verifier-nonce
   ```
1. After TD verification, the attestation token returned from Intel Trust Authority will contain the TD Integrity policy ID in the list of `policy-ids-matched` and `appraisal_results` in the `policy_defined_claims` section of the attestation token, as shown in the following example.
   ```
   {
      "appraisal": {
         "method": "azure",
         "ver": 2
      },
      "policy_defined_claims": {
         "appraisal_results": {
            "description": "Microsoft Azure TDX CVM (6.8.0-1020-azure)",
            "reference_values": [
               {
                  "description": "Require that secure-boot is enabled.  The event_log event field contains the SecureBoot EFI variable value 1 (or true)",
                  "evidence_path": "tpm.uefi_event_logs",
                  "expected_value": {
                     "digest_matches_event": true,
                     "event": "Yd/ki8qT0hGqDQDgmAMrjAoAAAAAAA...=",
                     "index": 7,
                     "type_name": "EV_EFI_VARIABLE_DRIVER_CONFIG"
                  }
               },
               {
                  "description": "Require that the TD does not have debug enabled",
                  "evidence_path": "tdx.tdx_td_attributes_debug",
                  "expected_value": false
               },
               {
                  "description": "Verifies the kernel image hash from the TPM event-log in PCR 4",
                  "evidence_path": "tpm.uefi_event_logs",
                  "expected_value": {
                     "digests": [
                     {
                        "alg": "SHA-256",
                        "digest": "c8a2cda3454e9ee70afcf6b6a8d005c4..."
                     }
                     ],
                     "index": 4,
                     "type_name": "EV_EFI_BOOT_SERVICES_APPLICATION"
                  }
               }
            ]
         }
      },
      "policy_ids_matched": [
         {
            "id": "5a24e414-211a-4316-8388-f6e31e1fe6f1",
            "version": "v2",
            "hash": "aDg0dE9pdDcvWHA0SzZmWUxJT2FMSHQ3QWN..."
         }
      ]
   ...
   ```


### TD Integrity for GCP CVMs with Intel TDX

1. Create a GCP CVM with Intel TDX. For more information, see [Creating a CVM with TDX on GCP](../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-tdx-gcp.md#creating-a-cvm-with-tdx-on-gcp).
1. Install trustauthority-cli (v1.9+), run the following command:
   ```bash
   curl https://raw.githubusercontent.com/intel/trustauthority-client-for-go/main/release/install-tdx-cli.sh | sudo bash -
   ```
2. Create a **config.json** as described in [Attestation Client CLI](../Integration/integrate-go-tdx-cli.md#configuration).
3. Run `trustauthority-cli`, collecting Intel TDX and CCEL evidence by using the following command:
   ```bash
   sudo trustauthority-cli token --tdx --ccel -c config.json --no-verifier-nonce 
   ```
4. After verification, the attestation token claims will contain the TD Integrity policy ID in the list of `policy-ids-matched` and `appraisal_results` in `policy_defined_claims`, as shown in the following example from an attestation token.
   ```
   {
      "appraisal": {
         "method": "default",
         "ver": 2
      },
      "policy_defined_claims": {
         "appraisal_results": {
            "description": "GCP TDX CVM (6.8.0-1021-gcp)",
            "reference_values": [
               {
                  "description": "Require that secure-boot is enabled.  The CC event_log event field contains the Secure Boot EFI variable value 1 (or true)",
                  "evidence_path": "tdx.uefi_event_logs",
                  "expected_value": {
                     "digest_matches_event": true,
                     "event": "Yd/ki8qT0hGqDQDgmA...",
                     "index": 1,
                     "type_name": "EV_EFI_VARIABLE_DRIVER_CONFIG"
                  }
               },
               {
                  "description": "Require that the TD does not have debug enabled",
                  "evidence_path": "tdx.tdx_td_attributes_debug",
                  "expected_value": false
               },
               {
                  "description": "Verifies the kernel image hash using the CCEL event-log",
                  "evidence_path": "tdx.uefi_event_logs",
                  "expected_value": {
                  "details": {
                     "string": "/vmlinuz-6.8.0-1021-gcp"
                  },
                  "digests": [
                     {
                        "alg": "SHA-384",
                        "digest": "467c85d0194b98035f5d4d9a093e1d19503d..."
                     }
                     ],
                     "index": 3,
                     "type_name": "EV_IPL"
                  }
               }
            ]
         }
      },
      "policy_ids_matched": [
         {
            "id": "5a24e414-211a-4316-8388-f6e31e1fe6f1",
            "version": "v2",
            "hash": "aDg0dE9pdDcvWHA0SzZmWUxJT2FMSHQ3QWNLbVow..."
         }      
   ...
   ```

---
**\*** Other names and brands may be claimed as the property of others.

/* external reference link URLs */
[tdi-repo]: https://github.com/intel/trustauthority-td-integrity
[create-gcp-tdx-cvm]: https://cloud.google.com/confidential-computing/confidential-vm/docs/create-a-confidential-vm-instance#gcloud
[create-azure-tdx-cvm]: https://learn.microsoft.com/en-us/azure/confidential-computing/quick-create-confidential-vm-portal
[gcp-c3-machines]: https://cloud.google.com/compute/docs/general-purpose-machines#c3_machine_types
