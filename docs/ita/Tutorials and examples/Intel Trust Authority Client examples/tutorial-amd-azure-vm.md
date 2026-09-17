---
title: Trust Authority Client Tutorial for Azure with AMD SEV-SNP
description: Tutorial for creating an Azure AMD SEV-SNP confidential VM, configuring Bastion and TPM prerequisites, and building the Trust Authority client for Go.
author: pcartee
topic-type: tutorial
date: 09/19/2024
uid: tutorial.amd
---

## Trust Authority Client Tutorial: AMD SEV-SNP Attestation on Microsoft Azure

:::note
This feature is currently in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Company Name pilot environment. Contact your Company representative for access.
:::

This tutorial explains how to deploy a demo application that uses the Trust Authority client to secure an application with AMD SEV-SNP technology on Microsoft Azure.

The demo application, built for AMD SEV-SNP attestation, uses the Trust Authority client to retrieve report evidence from the platform and request an attestation from Trust Authority. This demonstrates a simple passport attestation model that stops before involving a relying party. The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your applications.

## Create a VM with AMD SEV-SNP on Microsoft Azure

To create a Confidential virtual machine that supports AMD SEV-SNP, create a VM with the following attributes:

- Security type: **Confidential virtual machines**
- Image: **Ubuntu 20.04 LTS (Confidential VM - SEV-SNP only) - x64 Gen2**
- Size: **DC2ad** or any other size that supports AMD SEV-SNP

Follow the steps below to create an Azure VM with these attributes.

1. Sign in to Azure.

1. At the top of the Azure services page, select the **Create Virtual machines** icon.

1. At the top-left of the Virtual machines page, select **Create** and then choose **Azure virtual machines** from the dropdown menu.

1. Complete the following Project detail fields:

    - Subscription - Select the appropriate subscription for your organization.
    - Resource group - Select the resource to which this VM belongs. If there is no resource group to which this VM belongs, follow the steps below to create one.
        a. Select **Create new**.
        b. Enter a name for the resource group in the text box.
        c. Select **OK**.

1. Complete the following Instance details fields:

    - Virtual machine name - Give your virtual machine a name.
    - Region - Select **(US) East US**.
    - Availability options - Select **Availability zone**.
    - Availability zone - Select **Zone 1**.
    - Security type - Select **Confidential virtual machines**.

    :::note
    The availability of specific Confidential Virtual Machine images and sizes in particular regions and availability zones is dynamic and may change. Check the Azure [Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/?products=virtual-machines) page to find regions and availability zones with available Confidential VM support.
    :::

   - Image - Select **Ubuntu Server 20.04 LTS (Confidential VM - SEV-SNP Only)**. (If it is not immediately listed, follow the instructions below to search for x64 Gen2).
        a. At the Image field, select **See all images**.
        b. Enter **SEV-SNP** in the search field at the top of the page and press **Enter**.
        c. At the Ubuntu Server 20.04 LTS (Confidential VM - SEV-SNP Only) tile, select the down arrow and then choose **Ubuntu Server 20.04 LTS (Confidential VM - SEV-SNP Only)**.

   - Size - Select a size appropriate for your image. (If the size is not immediately listed, follow the instructions below to search for it.)
        a. At the Size field, select **See all sizes**.
        b. Enter an appropriate size for your image in the search field at the top of the page and press **Enter**.
        c. Choose a size and then select the **Select** button.

1. Complete the following Administrator account fields:

    - Authentication type - Select **SSH public key**.
    - Username - Enter a user name for the VM. Remember this username because it is needed in the following section.
    - SSH public key source - Select **Generate key pair**.
    - Key pair name - Enter a name for the key pair.

1. Complete the following Inbound port rules fields:

    - Public inbound - Select **None**.

1. At the bottom of the page, select **Next:Networking**.

    The Network Interface page displays.

   ![Enter network details for the virtual machine](/img/tutorial-amd-azure/create-vm-networking-amd.png)

1. Complete the following Network interface fields:

    - Virtual network - Select a virtual network for your organization. (If the virtual network doesn't exist, follow the instructions below to create one.)
        a. At the Virtual network field, select **Create new**.
        b. Select the address space options for the virtual network.
        c. Select the subnet options for the virtual network and then select **OK**.
    - Subnet - Select a subnet from the dropdown list.
    - Public IP - Select **None**.
    - Public inbound ports - Select **None**.
    - Delete NIC when VM is deleted - Select this checkbox.

1. Select **Review + create**.

    The Validation passed page displays.

![This page contains information about the virtual machine to be reviewed.](/img/tutorial-amd-azure/validation-passed-amd.png)

1. To create the VM, select **Create**.

    The Generate new key pair popup displays.

2. To generate a key pair and create the VM, select **Download private key and create resource**.

    The private key is downloaded to your default download directory, and the VM is created. Deployment can take a few minutes.

### Deploying Bastion

When deployment is complete, the following page displays.

![Deployment complete page.](/img/tutorial-amd-azure/deployment-complete-amd.png)

1. Select **Go to resource**.

    The Virtual machine page displays.

![A page used to connect to the virtual machine.](/img/tutorial-amd-azure/resource-page-amd.png)

1. Select **Connect** and then choose **Bastion**.

![Resource page displaying Bastion connection fields.](/img/tutorial-amd-azure/resource-page-bastion-amd.png)

1. Complete the following fields:

    - Authentication type - Select **SSH Private Key from Local File**.
    - Username - Enter the username created in the previous steps.
    - Local File - Navigate to the SSH key generated in the previous step.
    - Select the key and then click **Open**.

2. To create the Bastion connection select **Connect**.

    Bastion deployment takes a few minutes.

## Configure Azure CVM AMD SEV-SNP prerequisites

1. Install tpm2-tools.

    Azure AMD support requires `tpm2-tools` to access AMD SEV-SNP evidence.

    ```bash
    apt-get update
    apt-get install tpm2-tools
    ```

## Install the Trust Authority Client for Go

:::note
This feature is currently in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Company Name pilot environment. Contact your Company representative for access.
:::

The AMD SEV-SNP example uses the Trust Authority client for Go to collect report evidence from the AMD SEV-SNP VM. The report evidence is sent to Trust Authority for attestation. If attestation is successful, an attestation token (JWT) is returned. An example attestation token for AMD SEV-SNP is shown below.

:::note
Note that the preview branch is being checked out for the AMD SEV-SNP feature, because this feature is not supported on the main branch of the client CLI.
:::

1. Build the Trust Authority AMD SEV-SNP client.

    ```bash
    git clone https://github.com/company/trustauthority-client-for-go
    cd trustauthority-client-for-go/
    git checkout azure-sevsnp-preview
    cd sevsnp-cli/
    make cli
    ```

1. Configure your API key and any desired policy to evaluate.

   :::note
   This preview feature requires access to the Pilot environment to run. Contact your Company representative for access.
   :::

    Set the attestation API key and attestation endpoint. The endpoint may differ depending on which Trust Authority instance the client uses:

    ```bash
    cat <<EOF | tee ita.cfg
    APPLICATION_API_KEY=<application-api-key>
    APPLICATION_API_URL=https://[redacted]
    APPLICATION_BASE_URL=https://[redacted]
    EOF
    ```

1. Run the sample application. For more information about the Trust Authority client, see the client documentation.

    ```bash
    sudo ./application-sevsnp-cli token -c ita.cfg
    ```

### Decoded JWT output

```bash
{
  "eat_profile": "https://[redacted]/eat_profile.html",
  "intuse": "generic",
  "policy_defined_claims": null,
  "policy_ids_matched": null,
  "policy_ids_unmatched": null,
  "sevsnp": {
    "attester_type": "AMD SEV-SNP",
       "sevsnp_authorkeydigest": "<redacted>",
    "sevsnp_bootloader_svn": 3,
    "sevsnp_claim_version": "1.0.0",
    "sevsnp_collateral": "<redacted>",
    "sevsnp_familyId": "<redacted>",
    "sevsnp_guestsvn": 7,
    "sevsnp_hostdata": "<redacted>",
    "sevsnp_idkeydigest": "<redacted>",
    "sevsnp_imageId": "<redacted>",
    "sevsnp_is_debuggable": false,
    "sevsnp_launchmeasurement": "<redacted>",
    "sevsnp_microcode_svn": "<redacted>",
    "sevsnp_migration_allowed": false,
    "sevsnp_reportdata": "<redacted>",
    "sevsnp_runtime_data": {
      "keys": [
        {
          "e": "AQAB",
          "key_ops": [
            "sign"
          ],
          "kid": "<redacted>",
          "kty": "RSA",
          "n": "<redacted>"
        },
        {
          "e": "AQAB",
          "key_ops": [
            "encrypt"
          ],
          "kid": "<redacted>",
          "kty": "RSA",
          "n": "<redacted>"
        }
      ],
         "user-data": "<redacted>",
      "vm-configuration": {
        "console-enabled": true,
        "secure-boot": true,
        "tpm-enabled": true,
        "vmUniqueId": "<redacted>"
      }
    },
    "sevsnp_smt_allowed": true,
    "sevsnp_snpfw_svn": 8,
    "sevsnp_tee_svn": 0,
    "sevsnp_vmpl": 0
  },
  "ver": "2.0.0",
  "verifier_instance_ids": [
    "<redacted>"
  ],
  "exp": "<redacted>",
  "jti": "<redacted>",
  "iat": "<redacted>",
  "iss": "<redacted>",
  "nbf": "<redacted>"
}
```
