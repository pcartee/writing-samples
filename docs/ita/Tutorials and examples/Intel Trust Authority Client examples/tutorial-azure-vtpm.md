---
title: Intel Trust Authority Client Tutorial for Azure with vTPM and Intel TDX 
description: Step-by-step tutorial to stand up an Azure VM with vTPM and Intel TDX  
author: various
topic: tutorial
date: 10/16/2024
uid: tutorial.tpm.azure
---

*· 10/16/2024 ·*

## Intel® Trust Authority Client Tutorial — vTPM with Intel® TDX Attestation on Microsoft Azure

This tutorial provides steps to use the Intel® Trust Authority Attestation CLient CLI to attest evidence from a virtual Trusted Platform Module (vTPM) on Microsoft Azure. The [latest version of the client CLI with vTPM support](https://github.com/intel/trustauthority-client-for-go/tree/main/tdx-cli) is required to attest the vTPM. The client CLI is a command-line tool that collects evidence from the vTPM and sends it to the Intel Trust Authority for attestation. The Intel Trust Authority will verify the evidence and return an attestation token (a JWT) containing the claims for the vTPM. If attestation is successful, this demonstration will print the attestation token to the screen.

Microsoft Azure's implementation of vTPM uses Intel® Trust Domain Extensions (Intel® TDX) to ensure the integrity and authenticity of the "paravisor" (where the vTPM resides) and VM image. The vTPM public attestation key (AK, used to verify the TPM quote signature) is included as part of the `user-data` in the Intel TDX quote, tying the vTPM identity to the trust domain.

This tutorial has three main sections:

1. Create a Microsoft Azure confidential VM (CVM) with Intel TDX, verify that Intel TDX and the vTPM are enabled, and configure access to the vTPM.
2. Install and configure the Intel Trust Authority Attestation Client CLI.
3. Demonstrate attestation of the Intel TDX trust domain and vTPM.

## Prerequisites

- An Azure account with permissions to create a confidential VM and deploy a Bastion host.
- A subscription to Intel Trust Authority with access to the pilot environment.

## Create a VM with Intel TDX on Microsoft Azure

In this section you'll create an Azure CVM with Intel TDX and a vTPM. 

:::note
The availability of Azure confidential VMs with Intel TDX images and sizes in specific regions and availability zones is dynamic and may change. This tutorial uses US West 2 and Availability Zone 1 as an example. If you're outside North America, you may need to select a different region and availability zone. Check the Azure [Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/?products=virtual-machines) page to find the regions and availability zones with available Confidential VM with Intel TDX support.
:::

To create an Azure confidential VM with Intel TDX, perform the following steps. 

1. Sign in to Azure.

1. Select **Create a resource**.

1. Select **Virtual machine**, and then **create**.

1. On the **Basics** tab, under **Project Details**, select an existing **Resource group** or create a new group. It's recommended to create a new resource group for this tutorial. That way, when you're done you can delete the resource group and free all the resources in one step. To create a new resource group, select **Create new** (under the resource group text box) and give it a name.

1. In the **Instance details** section, complete the following fields:

    - Virtual machine name - Give your virtual machine a name.
    - Region - **(US) West US 2**.
    - Availability options -  **Availability zone**.
    - Availability zone -  **zone 1**.
    - Security type -  **Trusted launch virtual machine**.
    - Image -  **Ubuntu Server 22.04 LTS (Confidential VM) - x64 Gen2**
    - Size -  **DC1s_v3** (If not immediately listed, you may need to select **see all sizes**" to select **DC1s_v3** from the full list.) The smallest size with 1 vCPU is sufficient for this tutorial.
    - Public inbound - **None**


1. In the **Administrator account** section

    - Authentication type - **SSH public key** (recommended, but you can use a password if you prefer).
    - Username - **azureuser** (or another username of your choice).
    - SSH public key - **Generate new key pair** 
    - Accept the defaults for SSH key type and key pair name.


1. In the **Inbound port rules** section, select **None**.

1. Skip ahead to the **Networking** tab. For **Public IP**, select **None**.

1. At this point, you can skip the remaining sections and go directly to **Review + create**. 

1. Review the options and then select **Create**.

1. The **Generate new key pair** screen appears. Select **Download private key and create resource**. Deployment usually takes a few minutes to complete.

1. Once the deployment is complete, select **Go to resource** to view the VM. The Virtual machine overview page appear.

1. Select **Connect** from the menu pane on the left and then select **Bastion**.

1. Select **Deploy Bastion**. Bastion deployment takes a few minutes.

1. When deployment is complete, select **Connect** and then **Go to Bastion**
    1. Set **Authentication Type** to **SSH Private Key from Local File**.
    1. For **Username**, use the username you specified when creating the VM. The default is "azureuser".
    1. Select the private key file you downloaded when creating the VM.
    1. Select **Connect**. This will open a new browser tab with a connection to the VM terminal.

Once you are connected, proceed with the following steps to confirm that you have an Intel TDX-enabled VM with a vTPM. Then add the current user to the `tss` group to provide the needed permissions for the TPM. 

1. Verify TDX is enabled. This step and the next step should print character device file attributes for `tpmrm0` and `tpm0`. If either one is missing, Intel TDX is not enabled. In that case, check to see that the VM image (OS) and size (Standard DC1s_v3) are correct.

    ```bash
    ll /dev/tpmrm0
    ```
1. Verify the vTPM is enabled.

    ```bash
    ll /dev/tpm0
    ```
1. Add the current user to the `tss` user group to provide the needed permissions for the TPM (the username is assumed to be the default "azureuser" in the example below).

    ```bash
    sudo usermod -aG tss azureuser
    ```

1. Exit and then reconnect via bastion.

CVM setup is now complete. You can now proceed to install the Intel Trust Authority Attestation Client CLI.

## Install and configure the Attestation Client CLI

Connect to the Azure CVM via Bastion and follow these steps to install and configure the Intel Trust Authority Attestation Client CLI.

1. Go 1.22 or later is required to run the Attestation Client CLI. The following commands install Go on Ubuntu 22.04 LTS.

    ```bash
    wget https://go.dev/dl/go1.23.1.linux-amd64.tar.gz;ls
    sudo tar -xvf go1.23.1.linux-amd64.tar.gz -C /usr/local
    export PATH=$PATH:/usr/local/go/bin
    ```
    Verify that go is installed correctly by running `go version`. The output should be similar to `go version go1.23.1 linux/amd64`.

1. Install the Attestation Client CLI. This script will install the Attestation Client CLI and its dependencies. You might need to restart one or more services.

    ```bash
    curl -sL https://github.com/intel/trustauthority-client-for-go/blob/main/release/install-tdx-cli-azure.sh | sudo bash -
    ```
    Verify the Attestation Client CLI is installed correctly by running `trustauthority-cli version`. 

1. You must configure certain properties before using the token and verify commands. The properties and values are saved as JSON in config.json. The config.json requires the following properties:

    ```bash
    cat << EOF | tee ./tpm-cli.json
    {
    "cloud_provider": "azure"
    "trustauthority_url": "https://portal.trustauthority.intel.com",
    "trustauthority_api_url": "https://api.trustauthority.intel.com",
    "trustauthority_api_key": "<trustauthority attestation api key>",
    "tpm": {
        "owner_auth": "",
        "ak_handle": "81000003"
        }
    }
    EOF
    ```

    Owner_auth is the TPM owner password and ak_handle is the TPM attestation key handle. The owner_auth is an empty string and the ak_handle is hardcoded to 81000003, which is the location of the Azure-provisioned AK in the vTPM.

| Setting | Description |
| --- | --- |
| `trustauthority_api_key` | Your Intel Trust Authority API key. This key is used to authenticate your requests to the Intel Trust Authority. |
| `trustauthority_api_url` | The Intel Trust Authority API URL. This is the base URL for the Intel Trust Authority API. EU residents see note 1. |
| `trustauthority_url` | The Intel Trust Authority URL. This is the base URL for the Intel Trust Authority portal. EU residents see note 1. |
| `tpm.owner_auth` | The TPM owner password. This is the password used to establish authority for making some TPM commands. For Azure Confidential VMs, this is empty. |
| `tpm.ak_handle` | The TPM Attestation Key (AK) handle. This is a reference to the TPM Attestation Key (AK) to be used when generating a TPM quote. For Microsoft Azure Confidential VMs with Intel TDX, this handle is always "81000003". |

[1] If you are in the European Union (EU) region, use the following Intel Trust Authority URLs: Base URL — https://portal.eu.pilot.trustauthority.intel.com,
API URL — https://api.eu.pilot.trustauthority.intel.com. All other regions use the URLs shown in the example.


## Demonstrate attestation of the Intel TDX trust domain and vTPM

This section takes you through the steps to attest your confidential virtual machine (CVM) with the Intel Trust Authority Attestation Client CLI. 

1. Display composite evidence for both Intel TDX and vTPM. This displays the evidence that would be sent to the Intel Trust Authority verifier for attestation.

    ```
    trustauthority-cli evidence --tdx --tpm -c ~/tpm-cli.json
    ```

    ```bash
    [DEBUG] GET https://api.pilot.trustauthority.intel.com/appraisal/v1/nonce
    INFO[0001] Successfully wrote 64 bytes at NV index 1400002 
    INFO[0001] Sleeping for 3 seconds to allow Azure to read the runtime data 
    {
    "tdx": {
        "runtime_data": "eyJrZX...J9",
        "quote": "BA...AA=",
        "verifier_nonce": {
            "val": "dk...Q==",
            "iat": "M...EM=",
            "signature": "Im...g"
            }
        },
    "tpm": {
        "quote": "/1...DA==",
        "signature": "AB...AA",
        "pcrs": "h/...AA",
        "verifier_nonce": {
            "val": "dk...PQ==",
            "iat": "Mj...EM=",
            "signature": "Im...Ag"
            }
        }
    }
    ```

1. Generate a composite Intel TDX/TPM attestation token. This will collect evidence from both Intel TDX and the TPM, and send it to Intel Trust Authority for attestation. The output will be an attestation token containing the claims for both Intel TDX and TPM.

    ```bash
    trustauthority-cli token --tdx --tpm -c ./tpm-cli.json
    ```

You can experiment with the other `trustauthority-cli` commands. To see them all, run `trustauthority-cli --help`. When you're done experimenting, you can delete the resource group to free up all the resources you created for this tutorial.

## Conclusion

This tutorial demonstrated how to create an Azure confidential VM with Intel TDX and a vTPM, install and configure the Intel Trust Authority Attestation Client CLI, and attest the Intel TDX trust domain and vTPM. This is an example of composite attestation, that is, the attestation of a TEE and vTPM in a single attestation token. 

For more information, see the [Intel Trust Authority Attestation Client CLI documentation](https://docs.trustauthority.intel.com/main/articles/integrate-go-tdx-cli.html). 
