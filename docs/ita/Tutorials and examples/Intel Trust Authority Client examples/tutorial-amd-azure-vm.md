---
title: Intel Trust Authority Client Tutorial for Azure with AMD SEV-SNP 
description: Step-by-step tutorial to stand up an Azure VM with AMD SEV-SNP  
author: pcartee
topic: tutorial
date: 09/19/2024
uid: tutorial.amd
---

*· 09/19/2024 ·*

## Intel Trust Authority Client Tutorial - AMD SEV-SNP Attestation on Microsoft Azure

:::note
This feature is currently in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Intel Trust Authority pilot environment. Contact your Intel representative for access.
:::

This tutorial provides steps to deploy a demo application that utilizes the Intel® Trust Authority client for securing an application using AMD SEV-SNP TEE technology on the Microsoft Azure Cloud platform.

The demo application, built for AMD SEV-SNP Attestation, uses the Intel Trust Authority client to retrieve AMD SEV-SNP report evidence from the platform and request an attestation from Intel Trust Authority. This demonstrates a simple Passport attestation model (stopping before involving a relying party). The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your own applications.

## Creating a VM with AMD SEV-SNP capability on Microsoft Azure

To create a Confidential virtual machine that supports AMD SEV-SNP, create a VM with the following attributes:

- Security type: **Confidential virtual machines**
- Image: **Ubuntu 20.04 LTS (Confidential VM - SEV-SNP only) - x64 Gen2**  
- Size: **DC2ad** or any other size support AMD SEV-SNP

Follow the steps below to create an Azure VM with these attributes.

1. Sign in to Azure.

1. At the top of the Azure services page, select the **Create Virtual machines** icon.

1. At the top-left of the Virtual machines page, select **Create** and then choose **Azure virtual machines** from the dropdown menu.

1. Complete the following Project detail fields:)

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
    The availability of specific Confidential Virtual Machine images and sizes in particular regions and availability zones is dynamic and may change. Check the Azure [Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/?products=virtual-machines) page to find the areas and availability zones with available Confidential VM support.
    :::

   - Image - Select **Ubuntu Server 20.04 LTS (Confidential VM - SEV-SNP Only)**. (If it is not immediately listed, follow the instructions below to search for x64 Gen2) 
        <br />a. At the Image field, select **See all images**. 
        <br />b. Enter **SEV-SNP** in the search field at the top of the page and press **Enter**.
        <br />c. At the Ubuntu Server 20.04 LTS (Confidential VM - SEV-SNP Only) tile, select the down arrow and then choose **Ubuntu Server 20.04 LTS (Confidential VM - SEV-SNP Only)**.

   - Size - Select a size appropriate for your image. (If the size is not immediately listed, follow the instructions below to search for it.) 
        <br />a. At the Size field, select **See all sizes**. 
        <br />b. Enter an approriate size for your image in the search field at the top of the page and press **Enter**. 
        <br />c. Choose a size and then select the **Select** button.

1. Complete the following Administrator account fields:

    - Authentication type - Select **SSH public key**.
    - Username - Enter a user name for the VM. Remember this username because it is needed in the following section.
    - SSH public key source - Select **Generate key pair**.
    - Key pair name - Enter a name for the key pair.

1. Complete the following Inbound port rules fields:

    - Public inbound - Select **None**.

1. At the bottom of the page, select **Next:Networking**.

    The Network Interface page displays.

   ![Enter network details for the virtual machine](../../../../Static/img/tutorial-amd-azure/create-vm-networking-amd.png)

1. Complete the following Network interface fields:

    - Virtual network - Select a virtual network for your organization. (If the virtual network doesn't exist, follow the instructions below to create one.)
        <br />a. At the Virtual network field, select **Create new**.
        <br />b. Select the address space options for the virtual network.
        <br />c. Select the subnet options for the virtual network and then select **OK**.
    - Subnet - Select a subnet from the dropdown list.
    - Public IP - Select **None**.
    - Public inbound ports - Select **None**.
    - Delete NIC when VM is deleted - Select this checkbox.

1. Select **Review + create**.

    The Validation passed page displays.

![This page contains information about the virtual machine to be reviewed.](../../../../Static/img/tutorial-amd-azure/validation-passed-amd.png)

1. To create the VM, select **Create**.

    The Generate new key pair popup displays.

2. To generate a key pair and create the VM, select **Download private key and create resource**.

    The privatekey is downloaded to your default download directory, and the VM is created. The deployment can take a few minutes to create.

### Deploying Bastion

When deployment is complete, the following page displays.

![[Depoloyment complete page.](../../../../Static/img/tutorial-amd-azure/deployment-complete-amd.png)

1. Select **Go to resource**.

    The Virtual machine page displays.

![A page used to connect to the virtual machine.](../../../../Static/img/tutorial-amd-azure/resource-page-amd.png)


1. Select **Connect** and then choose **Bastion**.

![Resource page displaying Bastion connection fields.](../../../../Static/img/tutorial-amd-azure/resource-page-bastion-amd.png)


1. Complete the following fields:

    - Authentication type - Select **SSH Private Key from Local File**.
    - Username - Enter the username created in the previous steps.
    - Local File - Navigate to the SSH key generated in the previous step.
    - Select the key and then click **Open**.

2. To create the Bastion connection select **Connect**.

    Bastion deployment takes a few minutes.

## Configuring Azure CVM AMD SEV-SNP prerequisites

1. Install tpm2-tools.

    Azure AMD support requires tpm2-tools installed to access the AMD SEV-SNP evidence

    ```bash
    apt-get update
    apt-get install tpm2-tools
    ```

## Install Intel Trust Authority client for Go

:::note
This feature is currently in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Intel Trust Authority pilot environment. Contact your Intel representative for access.
:::

The AMD SEV-SNP example uses the Intel Trust Authority client for Go to collect report evidence from the AMD SEV-SNP VM. The report evidence is sent to Intel Trust Authority for attestation. If attestation is successful, an attestation token (JWT) is returned. An example attestation token for AMD SEV-SNP is shown in the following listing.

:::note
Note that the preview branch is being checked out for the AMD SEV-SNP feature, because this feature is not supported on the main branch of the client CLI.
:::

1. Build the Intel Trust Authority AMD SEV-SNP Client.

    ```bash
    git clone https://github.com/intel/trustauthority-client-for-go
    cd trustauthority-client-for-go/
    git checkout azure-sevsnp-preview
    cd sevsnp-cli/
    make cli
    ```

1. Configure your API key and any desired policy to evaluate.

   :::note
   This preview feature requires access to the Pilot environment to run. Contact your Intel representative for access.
   :::

    Set the attestation API key and attestation endpoint (The endpoint may be different depending on which Intel Trust Authority instance the client intends to interact with.):

    ```bash
    cat <<EOF | tee ita.cfg
    TRUSTAUTHORITY_API_KEY=<trustauthority-api-key>
    TRUSTAUTHORITY_API_URL=https://api.pilot.trustauthority.intel.com
    TRUSTAUTHORITY_BASE_URL=https://portal.pilot.trustauthority.intel.com
    EOF
    ```

1. Run the sample application. For more details on Intel Trust Authority client, please refer to client documentations

    ```bash
    sudo ./trustauthority-sevsnp-cli token -c ita.cfg
    ```

### Output after decoding jwt token

```bash
{
  "eat_profile": "https://portal.pilot.trustauthority.intel.com/eat_profile.html",
  "intuse": "generic",
  "policy_defined_claims": null,
  "policy_ids_matched": null,
  "policy_ids_unmatched": null,
  "sevsnp": {
    "attester_type": "AMD SEV-SNP",
    "sevsnp_authorkeydigest": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "sevsnp_bootloader_svn": 3,
    "sevsnp_claim_version": "1.0.0",
    "sevsnp_collateral": "3f0c945b36eb0fca6533cdec93d72f819e332ba8c6daba0d0748536cb8855027b8c2460048482a208b85dc83079592e06996e4ddbdd5b7cf036ac864fe51ad7f",
    "sevsnp_familyId": "01000000000000000000000000000000",
    "sevsnp_guestsvn": 7,
    "sevsnp_hostdata": "0000000000000000000000000000000000000000000000000000000000000000",
    "sevsnp_idkeydigest": "0356215882a825279a85b300b0b742931d113bf7e32dde2e50ffde7ec743ca491ecdd7f336dc28a6e0b2bb57af7a44a3",
    "sevsnp_imageId": "02000000000000000000000000000000",
    "sevsnp_is_debuggable": false,
    "sevsnp_launchmeasurement": "70849475ad2039f6b98d55e8961df48f4b7eb310302a7bcfaff3853fde67842671e20c8fe53ad8f54d326286b82f9ce4",
    "sevsnp_microcode_svn": 210,
    "sevsnp_migration_allowed": false,
    "sevsnp_reportdata": "534ec4fd31eb4b5364aeab426ca5050a740da820de8754ac190142099bdfbd980000000000000000000000000000000000000000000000000000000000000000",
    "sevsnp_runtime_data": {
      "keys": [
        {
          "e": "AQAB",
          "key_ops": [
            "sign"
          ],
          "kid": "HCLAkPub",
          "kty": "RSA",
          "n": "rpA2ewAA6YxVGwRbAclC0iVqTXofo1aXXpUHwgJ44u7G5jQPvlX80w69uLLAClrV-TQgLR56DxliF-QLcS1IY4wG-skEn4gRHdhruHJZdx49oYpHucG3CDvmu7XFEaVxxzFwy3CAk8Xc-8I6899_Qoei4ngIRd-6I38S2dC31j9WAIy7_pJyTkC82CNTYSI-Nk6hWUtuyzmby-2Scr-PCkpbRflYfzKHyeGEjlPaHKVBR48i3wpgYuBi4cY2ZAeJcqvUt_A3qtpeznRBpEp7DdH1Sa3gO9dTMM1z3bewfaYZ3om3D_AafIXlzwmy-Z859kCvGvP9B6e6Ue2qQ24Hww"
        },
        {
          "e": "AQAB",
          "key_ops": [
            "encrypt"
          ],
          "kid": "HCLEkPub",
          "kty": "RSA",
          "n": "1P7oDQAAusglLCn6WVDh0KG7zrTXQ6q8o2Qt_KjyldyvFyPfRFyYbyg-1nIrLfHX38y9xXEVIehE4aTfPu8_0fJq_DZekUpgNdXPJ3LsmUBp-LCrA90bfKsZTCqDBQSFVpOGwnQyjkBpHWXP6zFySIMlUx4XS1vqjvRJOBBl2QMmqczXc2bP7qD4b3NR_TciGskeSx5xNwOAmo7uMyb6Xkty3irBd9HIV_BvBm0rCz5MCX975GvyUNEl-pAgjkEp443RZhI4Nmq6qBhccqfeI29qV-3hjDNx2vy7U3d7Cm87gmJdKmADQuXhJ-etnQnzRjq9LhwBMMq4OAGpy6MHtw"
        }
      ],
      "user-data": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
      "vm-configuration": {
        "console-enabled": true,
        "secure-boot": true,
        "tpm-enabled": true,
        "vmUniqueId": "B30B77C2-4FD9-4FA8-9EF6-B94DA33F63B6"
      }
    },
    "sevsnp_smt_allowed": true,
    "sevsnp_snpfw_svn": 8,
    "sevsnp_tee_svn": 0,
    "sevsnp_vmpl": 0
  },
  "ver": "2.0.0",
  "verifier_instance_ids": [
    "975b041b-011e-4243-8d42-eea6de252209",
    "9f62640b-57ba-4a38-8bed-3079b3f33737",
    "495a2547-6e1d-4679-815b-5617fd5c3ca2",
    "2b38a8b8-ecf5-4bae-94f5-93894310d0d5",
    "8bb6c52a-ba6e-4adb-92b2-71f9258eb883",
    "2d8c4155-28c5-4083-93ac-1ab45fbc8629"
  ],
  "exp": 1725561182,
  "jti": "c7c21d7b-9cdc-4441-88a9-e2e15c2a25ed",
  "iat": 1725560882,
  "iss": "Intel Trust Authority",
  "nbf": 1725560882
}
```
