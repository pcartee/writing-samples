---
title: Trust Authority Client Tutorial for Azure with TDX 
description: Step-by-step tutorial to stand up an Azure VM with TDX  
author: teknoll
topic: tutorial
date: 06/07/2024
uid: tutorial.tdx
---

*· 12/19/2024 ·*

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

    - On the Networking page: Fore Public IP - Select **None**.

2. Review the options and then create the VM. Deployment typically takes a few minutes.

### Deploying Bastion

1. Select the VM resource.

1. Select **Connect** and then select **Bastion**.

1. Select **Deploy Bastion**.

![Settings used to deploy bastion.](/img/tutorial-sgx-azure/sgx-tutorial-deploy-bastion.png)

    Bastion deployment takes a few minutes.

2. Let Azure create a new SSH key pair, and then download the private key. You'll need this private key to connect to the VM.

3. Connect using "SSH private Key from Local File".

4. Enter the username (the default is "azureuser" if not specified during creation).

5. Set the "local file" to the downloaded key `<vm_name_key.pem>`.

## Configuring TDX prerequisites

1. Verify TDX is enabled.

    This verifies that the VM is SGX-enabled.

    ```bash
    ll /dev/tpmrm0
    ```

### Install TDX Sample Application using Trust Authority Client for C on Microsoft Azure

1. Install TDX and build prerequisites.

    ```bash
    sudo apt install -y build-essential libssl-dev
    ```

1. Install Docker-CE

    ```bash
    curl https://download.docker.com/linux/ubuntu/gpg | sudo  gpg --dearmor -o /usr/share/keyrings/docker.gpg
    echo "deb [signed-by=/usr/share/keyrings/docker.gpg arch=amd64] https://download.docker.com/linux/ubuntu focal stable"| sudo tee /etc/apt/sources.list.d/docker.list
    sudo apt update
    sudo apt install -y docker-ce
    sudo usermod -aG docker azureuser # (azureuser by default, user created at VM creation, the user currently logged in)
    ```

1. Exit and then log back in via bastion using the SSH key.

## Install the Trust Authority Client for C

The Trust Authority client is a C program that runs inside a Trust Domain (TD). The client go-tdx adaptor collects a quote from the Trust Domain and sends it to Trust Authority to retrieve a token.

![ntel TDX application Stack](/img/tutorial-sgx-azure/tdx-application-stack.png)

1. Build the sample application.

    ```bash
    git clone https://github.com/trustauthority-client-for-c.git
    cd trustauthority-client-for-c/
    make azure_tdx_token_docker
    ```

2. Configure your API key and optionally, any desired policy to evaluate.

    ```bash
    cat <<EOF | tee tdx_token.env
    TRUSTAUTHORITY_API_KEY=<trustauthority-api-key>
    TRUSTAUTHORITY_POLICY_ID=<trustauthority-policy-id - optional>
    TRUSTAUTHORITY_API_URL=https://api.trustauthority.company.com
    TRUSTAUTHORITY_BASE_URL=https://portal.trustauthority.company.com
    EOF
    ```

:::note
If you are in the European Union (EU) region, use the following Trust Authority URLs:

`TRUSTAUTHORITY_API_URL=https://api.eu.trustauthority.company.com`
`TRUSTAUTHORITY_BASE_URL=https://portal.eu.trustauthority.company.com `
:::

1. Run the sample application.

    The sample TDX client application executes the attester and verifier portions of the passport attestation mode. The container uses the Trust Authority client to retrieve evidence from the platform. The Trust Authority client sends that evidence as a quote in an attestation request to Trust Authority. The application outputs the resulting attestation token, demonstrating a successful attestation.

    ```bash
    sudo docker run -it --rm --device=/dev/tpm0 --device=/dev/tpmrm0 --env-file tdx_token.env --group-add $(getent group tss | cut -d: -f3) taas/azure_tdx_token:v1.0.0
    ```

### Output

```bash

[LOG:2024-05-02 17:33:48::/trustauthority-client/examples/tdx_token/tdx_token.c::211] Info: Successfully verified token

[LOG:2024-05-02 17:33:48::/trustauthority-client/examples/tdx_token/tdx_token.c::212] Info: Parsed token : 

{
    "alg": "PS384",
    "jku": "https://portal.trustauthority.company.com/certs",
    "kid": "79d80711b754cceb307d4278dc59957f27eb55a8e33d3b824967975843dcbf21df924eebaf93fce186fd291d36817785",
    "typ": "JWT"
}
.
{
    "attester_held_data": "Z...=",
    "attester_runtime_data": {
        "keys": [
            {
                "e": "AQAB",
                "key_ops": [
                    "sign"
                ],
                "kid": "HCLAkPub",
                "kty": "RSA",
                "n": "0CQeFAABO3WUWE8iFX73ci_UHZf3T7nqVO6JUDAcM5mqPVeJ2x2azZ8ErclqpUqTocd24L5Hhcp6afgrI_iBmdP0yEMO7XhWueAj4YkiQGhTtbahmcOKBhqNATr39C6eQ7bFrD4zNWGCD8tSCqs5dULI9TmMCMM-3xKc3zCR
S8AtW2L5RI1T01fr99jy7g7XR3GQuKzIAmrlbGiDFlsCvp7pIdBl00ywsF4ihSIJwzFTmxedsv8DtAc9HuO2HwDBMIo490eCzI9U_B0OOGtLqUFZm4o-sk4xjfzKBN86F93_ezZXISwAVgYpVt8UP3pT1P8OGyBz87-8bDhRyzAf9w"
            },
            {
                "e": "AQAB",
                "key_ops": [
                    "encrypt"
                ],
                "kid": "HCLEkPub",
                "kty": "RSA",
                "n": "v1RJXwAA8Oeb8XnCrt_LtO6c3AplbZ4LunVcp6SOAPbrlTahVaeANfxI3w9ZxCFxOukf1rdyYWx6UMnBikJaRMX9qGGodnag2lehakZX2T6-GZ_GOaIKxqthNZ_DrvIYyWbNxWv3S6CDk2Ov8hk-DguvlaHN_kaOUCLHMaas
B1udzYi4gyI3DO8c8pwsHfzya7MNlo0lZEyvB1C558cskMjbAezysylFVuzI7NTbCs6v4dmVbpxXUlXmlCuv3iymCH5aXQyjtSPl5BXAlWcnh1xhdYkRD6O607QnGeYfDrPbi5yILcdV4KVJLB7bSkIBHu-q_RceDnbzwjWQqPDj_Q"
            }
        ],
        "user-data": "3E107308A6FAB4C19E54825339DA7A0AD642D55B9D9801959F099F18B043A248272ABB4B6AA8D4B7C26CA84B4E05A7E4FAC96E618B8EB991B762D4E65BE089AE",
        "vm-configuration": {
            "console-enabled": true,
            "root-cert-thumbprint": "6nZZnYaJc4KqUZ_yvA-mucFdYNouvlPnITnNMXsHl-0",
            "secure-boot": true,
            "tpm-enabled": true,
            "tpm-persisted": true,
            "vmUniqueId": "C5EAB6CD-48EC-4415-942A-7EAC48429E7F"
        }
    },
    "attester_tcb_date": "2023-08-09T00:00:00Z",
    "attester_tcb_status": "UpToDate",
    "attester_type": "TDX",
    "dbgstat": "disabled",
    "eat_profile": "https://portal.trustauthority.company.com/eat_profile.html",
    "exp": 1714673027,
    "iat": 1714671227,
    "intuse": "generic",
    "iss": "Trust Authority",
    "jti": "32428945-766f-4e9b-8640-d6aec2819beb",
    "nbf": 1714671227,
    "policy_ids_unmatched": [
        {
            "hash": "RHdQVDZwUEdUN0k1QTFQZnBpN2Izekt1dDdLQ0RoYUFJVmh4UzNLTVZjOUJEamQzdmtIem5jNG92NnZONlFNNw==",
            "id": "d970fa2b-34bc-476d-ad8f-7a1b78f2885e",
            "version": "v1"
        }
    ],
    "tdx_collateral": {
        "qeidcerthash": "b2ca71b8e849d5e799451b4bfe43159a0ee548032cecb2c0e479bf6ee3f39fd1",
        "qeidcrlhash": "ca685ff1fa572b5fd5b0d10c1e06fce40f25544729b6052689583aa17166ab85",
        "qeidhash": "f1f671d997705c091eba97c63d1f8488ebd50fbd045e359c23f57ab56b15bad7",
        "quotehash": "8c3d3153638cfd1c7fab67c637b4642d03ee2f70fb0936b48cad67ba0f230218",
        "tcbinfocerthash": "b2ca71b8e849d5e799451b4bfe43159a0ee548032cecb2c0e479bf6ee3f39fd1",
        "tcbinfocrlhash": "ca685ff1fa572b5fd5b0d10c1e06fce40f25544729b6052689583aa17166ab85",
        "tcbinfohash": "2f76d93a6d6b77a766e534554f929505c74690177db7453cae054413beb98106"
    },
    "tdx_is_debuggable": false,
    "tdx_mrconfigid": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_mrowner": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_mrownerconfig": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_mrseam": "360304d34a16aace0a18e09ad2d07d2b9fd3c174378e5bf108388079827f89ff62acc5f8c473dd40706324834e202946",
    "tdx_mrsignerseam": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_mrtd": "0cc279c02d62414498ef4455822f2aea53351c8d4c265f587e695fa94b136386f97480c47bb5b26927023947cdf938d3",
    "tdx_report_data": "312fd9e8b8b9b0b72a07dd661065f45ff841686ca5ece0b429aeed77593400760000000000000000000000000000000000000000000000000000000000000000",
    "tdx_rtmr0": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_rtmr1": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_rtmr2": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_rtmr3": "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "tdx_seam_attributes": "0000000000000000",
    "tdx_seamsvn": 2,
    "tdx_td_attributes": "0000000000000000",
    "tdx_td_attributes_debug": false,
    "tdx_td_attributes_key_locker": false,
    "tdx_td_attributes_perfmon": false,
    "tdx_td_attributes_protection_keys": false,
    "tdx_td_attributes_septve_disable": false,
    "tdx_tee_tcb_svn": "02010600000000000000000000000000",
    "tdx_xfam": "e718060000000000",
    "ver": "1.0.0",
    "verifier_instance_ids": [
        "dd6a1f98-fa8e-4bcc-8223-086b80ff60e6",
        "1e0fe8b3-37b9-46df-bfa4-64559af84ecb",
        "f1477e85-dadb-4399-aa3b-deb08d290744",
        "6c13bbd5-f4fa-41c3-a8dc-c658db6b8296",
        "86b715d4-4995-43ec-b466-c14d428648a0",
        "f5f56afc-bf15-4235-b071-50a8d0f0f126"
    ],
    "verifier_nonce": {
        "iat": "MjAyNC0wNS0wMiAxNzozMzo0NiArMDAwMCBVVEM=",
        "signature": "XHrfgvBLxhSfBYemNq1gsWcyR6lcUSEFr33dkvmhpHntTUVOmIfICZukJ61wewePlV0zEWSjgDdrD7xxCUm7ViQHEdO+iuuGM9Me8MyCoz77gxF1C0mA0F9/US6t/miwpXSXvqR1EDQFkJFh97FWlD0SZNxzzPsx4HSLGtSI
rxgjEpWGsCOWuu7eqXyKHDBwzsKuoSojHWIU8xnQwuvWl/keX1wS/vv517tu4zHbWwQ79GjI7aECVBZ/oXDxrY0yLbmDcpnpCc60aDY8w2/J+88Rfx/3ACeMtMoZgtlscmbndxkbM01JQiCuhJP3AGy8Dg+X2m0XUX4cj2WaPvWK7l7N4rTJqgq+9v21iq
5sHfLdOFYO1+76slDh9I60iTWPRvTw5ZfGCfnwpUBmFJlXUmVzbOzRUboA7GG6BBr1CPTQwNBm1hJLQNl83VECwglf3iZ/cdIoVq0x6N4Bfh1HWHCAGVBWnAz+uQN7xNGcBX1NF1T6zgNtzP6UXTCMN0gO",
        "val": "TW1QUHVFKzNrNW9hK2tBMjJmTVlUbzZjejdwaTNuNUhXaWc1U0VpTzRVdWxwZ0NsRjR6MlppMmVXL1dKbUwvMzhqTXVEQXp5ZlFQUWZjNXlSTURmNHc9PQ=="
    }
}
```

## Install the trustauthority-cli Utility

This section describes an alternative to the containerized sample applications. Rather than using the client bindings directly in a sample application, the TDX CLI client provides a command-line wrapper for the Golang client libraries.

[trustauthority-cli for Azure](../../Integration/integrate-go-tdx-cli.md#using-the-intel-trust-authority-attestation-client-cli)

1. Download and run the Azure installer variant.

    ```bash
    curl -sL https://raw.githubusercontent.com/trustauthority-client-for-go/main/release/install-tdx-cli-azure.sh | sudo bash -
    ```

2. Configure the URL and API key:

    ```bash
    cat <<EOF | tee config.json
    {
        "trustauthority_api_url": "https://api.trustauthority.company.com",
        "trustauthority_api_key": "<attestation api key>"
    }
    EOF
    ```

:::note
If you are in the European Union (EU) region, use the following Trust Authority URL:

`"trustauthority_api_url": "https://api.eu.trustauthority.com"`
:::

1. Use the `trustauthority-cli` utility to request an attestation.  The _token_ command automatically collects evidence from TDX and requests an attestation token from Trust Authority. Full usage details for the `trustauthority-cli` utility can be found [here.](../../Integration/integrate-go-tdx-cli.md)

    ```bash
    trustauthority-cli token --config config.json
    ```
