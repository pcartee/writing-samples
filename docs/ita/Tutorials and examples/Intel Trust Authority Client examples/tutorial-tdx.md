---
title: Trust Authority Client Tutorial for Azure with TDX
description: Tutorial for deploying an Azure confidential VM with TDX and running the Trust Authority Client for C.
author: pcartee
topic-type: tutorial
date: 06/07/2024
uid: tutorial.tdx
---

## Trust Authority Client Tutorial - TDX Attestation on Microsoft Azure

This tutorial provides steps to deploy a demo app that uses the Trust Authority client when securing an application using Trust Domain Extensions (TDX) on the Microsoft Azure Cloud platform.

The demo application, built for TDX, uses the Trust Authority client to retrieve evidence from the platform and request an attestation from Trust Authority. This demonstrates a simple passport attestation model (stopping before involving a relying party). The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your applications.

## Creating a VM with TDX on Microsoft Azure

To create an Azure confidential VM with TDX, create a VM with the following attributes:

- Security type: **Trusted launch virtual machine**
- Image: **Ubuntu Server 22.04 LTS**
- Size: **DC2esv5**

The following are steps to create an Azure VM with these attributes.

1. Sign in to Azure.

1. Select **Create a resource**.

1. Select **virtual machine**.

    ![Enter instance details for the virtual machine.](/img/tutorial-sgx-azure/tdx-tutorial-vm-creation.png)

1. Complete the following fields:

    - Virtual machine name - Give your virtual machine a name.
    - Region - Select **(US) West US 2**.
    - Availability options - Select **Availability zone**.
    - Availability zone - Select **zone 2**.

    :::note
    The availability of specific Confidential Virtual Machine images and sizes in specific regions and availability zones is dynamic and may change. Check the Azure [Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/?products=virtual-machines) page to find the regions and availability zones with available Confidential VM support.
    :::

    - Security type - Select **Trusted launch virtual machine**.
    - Image - Select **Ubuntu Server 22.04 LTS - x64 Gen2**
    - Size - Select **DC2esv5** (If not immediately listed, you may need to select **see all sizes**" to select **DC1s_v3** from the full list.)
    - Public inbound - **None**

    ![Enter the administrative account security details for the virtual machine.](/img/tutorial-sgx-azure/tdx-tutorial-vm-creation-2.png)

    - On the Networking page: For Public IP, select **None**.

1. Review the options and then create the VM. Deployment typically takes a few minutes.

### Deploying Bastion

1. Select the VM resource.

1. Select **Connect** and then select **Bastion**.

1. Select **Deploy Bastion**.

![Settings used to deploy bastion.](/img/tutorial-sgx-azure/sgx-tutorial-deploy-bastion.png)

    Bastion deployment takes a few minutes.

2. Let Azure create a new SSH key pair, and then download the private key. You'll need this private key to connect to the VM.

1. Connect using **SSH private key from local file**.

1. Enter the username. The default is `azureuser` if you did not specify one during creation.

1. Set the local file to the downloaded key `<vm_name_key.pem>`.

## Configuring TDX prerequisites

1. Verify TDX is enabled.

    This verifies that TDX is enabled on the VM.

        ll /dev/tpmrm0

### Install the TDX Sample Application Using the Trust Authority Client for C on Microsoft Azure

1. Install TDX and build prerequisites.

        sudo apt install -y build-essential libssl-dev

1. Install Docker CE.

        curl https://download.docker.com/linux/ubuntu/gpg | sudo  gpg --dearmor -o /usr/share/keyrings/docker.gpg
        echo "deb [signed-by=/usr/share/keyrings/docker.gpg arch=amd64] https://download.docker.com/linux/ubuntu focal stable"| sudo tee /etc/apt/sources.list.d/docker.list
        sudo apt update
        sudo apt install -y docker-ce
        sudo usermod -aG docker azureuser # (azureuser by default, user created at VM creation, the user currently logged in)

1. Exit and then log back in via bastion using the SSH key.

## Install the Trust Authority Client for C

The Trust Authority client is a C program that runs inside a Trust Domain (TD). The client go-tdx adapter collects a quote from the Trust Domain and sends it to Trust Authority to retrieve a token.

![Intel TDX application stack](/img/tutorial-sgx-azure/tdx-application-stack.png)

1. Build the sample application.

        git clone https://github.com/[redacted]/trustauthority-client-for-c.git
        cd trustauthority-client-for-c/
        make azure_tdx_token_docker

2. Configure your API key and optionally, any desired policy to evaluate.

    ```bash
    cat <<EOF | tee tdx_token.env
    TRUSTAUTHORITY_API_KEY=<trustauthority-api-key>
    TRUSTAUTHORITY_POLICY_ID=<trustauthority-policy-id - optional>
    TRUSTAUTHORITY_API_URL=https://[redacted]
    TRUSTAUTHORITY_BASE_URL=https://[redacted]
    EOF
    ```

:::note
If you are in the European Union (EU) region, use the following Trust Authority URLs:

`TRUSTAUTHORITY_API_URL=https://[redacted]`
`TRUSTAUTHORITY_BASE_URL=https://[redacted]`
:::

1. Run the sample application.

    The sample TDX client application executes the attester and verifier portions of the passport attestation mode. The container uses the Trust Authority client to retrieve evidence from the platform. The Trust Authority client sends that evidence as a quote in an attestation request to Trust Authority. The application outputs the resulting attestation token, demonstrating a successful attestation.

        sudo docker run -it --rm --device=/dev/tpm0 --device=/dev/tpmrm0 --env-file tdx_token.env --group-add $(getent group tss | cut -d: -f3) [redacted]/azure_tdx_token:v1.0.0

### Output

```text
    [LOG:2024-05-02 17:33:48::/[redacted]/tdx_token.c::211] Info: Successfully verified token

    [LOG:2024-05-02 17:33:48::/[redacted]/tdx_token.c::212] Info: Parsed token :

    {
        "alg": "PS384",
        "jku": "https://[redacted]/certs",
        "kid": "[redacted]",
        "typ": "JWT"
    }
    .
    {
        "attester_held_data": "[redacted]",
        "attester_runtime_data": {
            "keys": [
                {
                    "e": "AQAB",
                    "key_ops": [
                        "sign"
                    ],
                    "kid": "[redacted]",
                    "kty": "RSA",
                    "n": "[redacted]"
                },
                {
                    "e": "AQAB",
                    "key_ops": [
                        "encrypt"
                    ],
                    "kid": "[redacted]",
                    "kty": "RSA",
                    "n": "[redacted]"
                }
            ],
            "user-data": "[redacted]",
            "vm-configuration": {
                "console-enabled": true,
                "root-cert-thumbprint": "[redacted]",
                "secure-boot": true,
                "tpm-enabled": true,
                "tpm-persisted": true,
                "vmUniqueId": "[redacted]"
            }
        },
        "attester_tcb_date": "[redacted]",
        "attester_tcb_status": "UpToDate",
        "attester_type": "TDX",
        "dbgstat": "disabled",
        "eat_profile": "https://[redacted]/eat_profile.html",
        "exp": "[redacted]",
        "iat": "[redacted]",
        "intuse": "generic",
        "iss": "Trust Authority",
        "jti": "[redacted]",
        "nbf": "[redacted]",
        "policy_ids_unmatched": [
            {
                "hash": "[redacted]",
                "id": "[redacted]",
                "version": "v1"
            }
        ],
        "tdx_collateral": {
            "qeidcerthash": "[redacted]",
            "qeidcrlhash": "[redacted]",
            "qeidhash": "[redacted]",
            "quotehash": "[redacted]",
            "tcbinfocerthash": "[redacted]",
            "tcbinfocrlhash": "[redacted]",
            "tcbinfohash": "[redacted]"
        },
        "tdx_is_debuggable": false,
        "tdx_mrconfigid": "[redacted]",
        "tdx_mrowner": "[redacted]",
        "tdx_mrownerconfig": "[redacted]",
        "tdx_mrseam": "[redacted]",
        "tdx_mrsignerseam": "[redacted]",
        "tdx_mrtd": "[redacted]",
        "tdx_report_data": "[redacted]",
        "tdx_rtmr0": "[redacted]",
        "tdx_rtmr1": "[redacted]",
        "tdx_rtmr2": "[redacted]",
        "tdx_rtmr3": "[redacted]",
        "tdx_seamsvn": 2,
        "tdx_td_attributes": "0000000000000000",
        "tdx_td_attributes_debug": false,
        "tdx_td_attributes_key_locker": false,
        "tdx_td_attributes_perfmon": false,
        "tdx_td_attributes_protection_keys": false,
        "tdx_td_attributes_septve_disable": false,
        "tdx_tee_tcb_svn": "[redacted]",
        "tdx_xfam": "[redacted]",
        "ver": "1.0.0",
        "verifier_instance_ids": [
            "[redacted]"
        ],
        "verifier_nonce": {
            "iat": "[redacted]",
            "signature": "[redacted]",
            "val": "[redacted]"
        }
    }
```

## Install the Trust Authority CLI Utility

This section describes an alternative to the containerized sample applications. Rather than using the client bindings directly in a sample application, the TDX CLI client provides a command-line wrapper for the Golang client libraries.

[trustauthority-cli for Azure](../../Integration/integrate-go-tdx-cli.md#using-the-intel-trust-authority-attestation-client-cli)

1. Download and run the Azure installer variant.

        curl -sL https://raw.githubusercontent.com/[redacted]/install-tdx-cli-azure.sh | sudo bash -

2. Configure the URL and API key:

    ```json
    {
      "trustauthority_api_url": "https://[redacted]",
      "trustauthority_api_key": "<attestation api key>"
    }
    ```

    :::note
    If you are in the European Union (EU) region, use the following Trust Authority URL:

    `"trustauthority_api_url": "https://[redacted]"`
    :::

1. Use the `trustauthority-cli` utility to request an attestation. The *token* command automatically collects evidence from TDX and requests an attestation token from Trust Authority. For full usage details, see the [Trust Authority CLI documentation](../../Integration/integrate-go-tdx-cli.md).

        trustauthority-cli token --config config.json
