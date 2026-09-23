---
title: Trust Authority Client Tutorial for Azure with SGX
description: Tutorial for deploying an Azure SGX VM, installing the Trust Authority Client for C, and requesting a passport attestation token.
author: pcartee
topic-type: tutorial
date: 06/12/2024
uid: tutorial.sgx
---

This tutorial provides steps to deploy a demo application that utilizes the Application client for securing an application using Company® Software Guard Extensions (Company® SGX) on the Microsoft Azure Cloud platform.

The demo application, built for Company SGX, uses the Application client to retrieve evidence from the platform and request an attestation from Application. This demonstrates a simple Passport attestation model (stopping before involving a relying party). The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your own applications.

## Creating a VM with Company SGX on Microsoft Azure

To create an Azure Trusted Launch VM that supports Company SGX, create a VM with the following attributes:

- Security type: **Trusted launch virtual machine**
- Image: **Ubuntu 20.04 Gen2**  
- Size: **DC1s_v3**

The following are steps to create an Azure VM with these attributes.

1. Sign in to Azure.

1. Select **Create a resource**.

1. Select **virtual machine**.

    ![Enter instance details for the virtual machine](/img/tutorial-sgx-azure/sgx-tutorial-vm-creation.png)

1. Complete the following fields:

    - Virtual machine name - Give your virtual machine a name.
    - Region - Select **(US) West US 2**.
    - Availability options - Select **Availability zone**.
    - Availability zone - Select **zone 1**.

    :::note
    The availability of specific Confidential Virtual Machine images and sizes in specific regions and availability zones is dynamic and may change. Check the Azure [Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/?products=virtual-machines) page to find the regions and availability zones with available Confidential VM support.
    :::

    - Security type - Select **Trusted launch virtual machine**
    - Image - Select **Ubuntu Server 20.04 LTS - x64 Gen2**
    - Size - Select **DC1s_v3** (If not immediately listed, you may need to select **see all sizes**" to select **DC1s_v3** from the full list.)
    - Public inbound - **None**

    ![Enter the administrative account security details for the virtual machine.](/img/tutorial-sgx-azure/sgx-tutorial-vm-creation-2.png)

    - On the Networking page: Fore Public IP - Select **None**.

1. Review the options and then create the VM. Deployment typically takes a few minutes.

### Deploying Bastion

1. Select the VM resource.

1. Select **Connect** and then select **Bastion**.

1. Select **Deploy Bastion**.

    ![Settings used to deploy bastion.](/img/tutorial-sgx-azure/sgx-tutorial-deploy-bastion.png)

    Bastion deployment takes a few minutes.

1. Let Azure create a new SSH key pair, and then download the private key. You'll need this private key to connect to the VM.

1. Connect using **SSH private key from local file**.

1. Enter the username. The default is `azureuser` if you did not specify one during creation.

1. Set the local file to the downloaded key `<vm_name_key.pem>`.

## Configuring Company SGX prerequisites

1. Verify Company SGX is enabled.

    Verify the existence of these device files. This verifies that the VM is Company SGX-enabled.

    ```bash
    ls /dev/sgx_*
    /dev/sgx_enclave
    /dev/sgx_provision
    ```

1. Add the Company SGX SDK repo.

    ```bash
    curl https://download.01.org/company-sgx/sgx_repo/ubuntu/company-sgx-deb.key | sudo  gpg --dearmor -o /usr/share/keyrings/company.gpg
    echo "deb [signed-by=/usr/share/keyrings/company.gpg] https://download.01.org/company-sgx/sgx_repo/ubuntu focal main" | sudo tee -a /etc/apt/sources.list.d/company-sgx.list
    ```

1. Add the Azure repo for Company SGX.

    ```bash
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo  gpg --dearmor -o /usr/share/keyrings/msft.gpg
    echo "deb [signed-by=/usr/share/keyrings/msft.gpg arch=amd64] https://packages.microsoft.com/ubuntu/20.04/prod focal main" | sudo tee /etc/apt/sources.list.d/msprod.list

    sudo apt update
    ```

1. Install the Company SGX SDK and build prerequisites

    ```bash
    sudo apt install -y build-essential libssl-dev libsgx-quote-ex libsgx-enclave-common libsgx-enclave-common-dev libsgx-dcap-ql libsgx-dcap-ql-dev az-dcap-client
    ```

1. Install the Company SGX SDK.

    ```bash
    wget https://download.01.org/company-sgx/sgx-dcap/1.20/linux/distro/ubuntu20.04-server/sgx_linux_x64_sdk_2.23.100.2.bin

    chmod +x sgx_linux_x64_sdk_2.23.100.2.bin 
    sudo ./sgx_linux_x64_sdk_2.23.100.2.bin 
        Do you want to install in current directory? [yes/no] N
        Please input the directory which you want to install in : /opt/company
    source /opt/company/sgxsdk/environment
    echo "source /opt/company/sgxsdk/environment" >> ~/.bashrc && source ~/.bashrc
    ```

1. Install Docker-CE.

    ```bash
    curl https://download.docker.com/linux/ubuntu/gpg | sudo  gpg --dearmor -o /usr/share/keyrings/docker.gpg
    echo "deb [signed-by=/usr/share/keyrings/docker.gpg arch=amd64] https://download.docker.com/linux/ubuntu focal stable"| sudo tee /etc/apt/sources.list.d/docker.list
    sudo apt update
    sudo apt install -y docker-ce
    sudo usermod -aG docker <username> (azureuser by default)
    ```

1. Exit and then sign in via the bastion server using the SSH key.

## Install Application client for C

The Company SGX example uses the Application client for C and the Company SGX adapter to collect evidence from the enclave. The evidence is sent to Application for attestation. If attestation is successful, an attestation token (JWT) is returned. An example attestation token for Company SGX is shown in the following listing.

![SGX Application Stack](/img/tutorial-sgx-azure/sgx-application-stack.png)

This demonstrates the attester and verifier portions of the [passport attestation model.](../../Concepts/concept-patterns.md#workflows)

1. Build the sample application.

    ```bash
    git clone https://github.com/company/application-client-for-c
    cd application-client-for-c/
    make sgx_token_docker
    ```

2. Configure your API key and any desired policy to evaluate.

    Set the attestation API key and optionally a policy ID to evaluate (The POLICY_ID is commented out below):

    ```bash
    cat <<EOF | tee sgx_token.env
    application_API_KEY=<application-api-key>
    # application_POLICY_ID=<application-policy-id - optional>
    application_API_URL=https://api.application.company.com
    application_BASE_URL=https://portal.application.company.com
    SGX_AESM_ADDR=1
    EOF
    ```

:::note
If you are in the European Union (EU) region, use the following Application URLs:

`application_API_URL=https://api.eu.application.company.com`
`application_BASE_URL=https://portal.eu.application.company.com`
:::

1. Run the sample application.

    The sample SGX client application executes the attester and verifier portions of the passport attestation mode. The container uses the application client to retrieve evidence from the host and enclave. It sends that evidence as a quote in an attestation request to application. The application outputs the resulting attestation token, demonstrating a successful attestation.

    ```bash
    sudo docker run -it --rm --device=/dev/sgx_enclave --device=/dev/sgx_provision -v /var/run/aesmd/aesm.socket:/var/run/aesmd/aesm.socket --env-file sgx_token.env --group-add $(getent group sgx_prv | cut -d: -f3) taas/sgx_token:v1.0.0
    ```

### Output

```bash
[LOG:<timestamp>::/application-client/examples/sgx_token/sgx_token.c::205] Info: Successfully verified token

[LOG:<timestamp>::/application-client/examples/sgx_token/sgx_token.c::206] Info: Parsed token :

{
    "alg": "PS384",
    "jku": "https://[redacted]/certs",
    "kid": "<redacted>",
    "typ": "JWT"
}
.
{
    "attester_advisory_ids": [
        "<redacted>"
    ],
    "attester_held_data": "<redacted>",
    "attester_tcb_date": "<redacted>",
    "attester_tcb_status": "SWHardeningNeeded",
    "attester_type": "SGX",
    "dbgstat": "disabled",
    "eat_profile": "https://[redacted]/eat_profile.html",
    "exp": "<redacted>",
    "iat": "<redacted>",
    "intuse": "generic",
    "iss": "<redacted>",
    "jti": "<redacted>",
    "nbf": "<redacted>",
    "policy_ids_unmatched": [
        {
            "hash": "<redacted>",
            "id": "<redacted>",
            "version": "<redacted>"
        }
    ],
    "sgx_collateral": {
        "qeidcerthash": "<redacted>",
        "qeidcrlhash": "<redacted>",
        "qeidhash": "<redacted>",
        "quotehash": "<redacted>",
        "tcbinfocerthash": "<redacted>",
        "tcbinfocrlhash": "<redacted>",
        "tcbinfohash": "<redacted>"
    },
    "sgx_is_debuggable": false,
    "sgx_isvprodid": 0,
    "sgx_isvsvn": 0,
    "sgx_mrenclave": "<redacted>",
    "sgx_mrsigner": "<redacted>",
    "sgx_report_data": "<redacted>",
    "ver": "1.0.0",
    "verifier_instance_ids": [
        "<redacted>"
    ],
    "verifier_nonce": {
        "iat": "<redacted>",
        "signature": "<redacted>",
        "val": "<redacted>"
    }
}
```
