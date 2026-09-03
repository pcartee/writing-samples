---
title: Intel Trust Authority Client Tutorial for Azure with SGX 
description: Step-by-step tutorial to stand up an Azure VM with Intel SGX  
author: pcartee
topic: tutorial
date: 06/12/2024
uid: tutorial.sgx
---

*· June/12/2024 ·*

This tutorial provides steps to deploy a demo application that utilizes the Intel® Trust Authority client for securing an application using Intel® Software Guard Extensions (Intel® SGX) on the Microsoft Azure Cloud platform.

The demo application, built for Intel SGX, uses the Intel Trust Authority client to retrieve evidence from the platform and request an attestation from Intel Trust Authority. This demonstrates a simple Passport attestation model (stopping before involving a relying party). The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your own applications.

## Creating a VM with Intel SGX on Microsoft Azure

To create an Azure Trusted Launch VM that supports Intel SGX, create a VM with the following attributes:

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

## Configuring Intel SGX prerequisites

1. Verify Intel SGX is enabled.

    Verify the existence of these device files. This verifies that the VM is Intel SGX-enabled.

    ```bash
    ls /dev/sgx_*
    /dev/sgx_enclave
    /dev/sgx_provision
    ```

1. Add the Intel SGX SDK repo.

    ```bash
    curl https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | sudo  gpg --dearmor -o /usr/share/keyrings/intel.gpg
    echo "deb [signed-by=/usr/share/keyrings/intel.gpg] https://download.01.org/intel-sgx/sgx_repo/ubuntu focal main" | sudo tee -a /etc/apt/sources.list.d/intel-sgx.list
    ```

1. Add the Azure repo for Intel SGX.

    ```bash
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo  gpg --dearmor -o /usr/share/keyrings/msft.gpg
    echo "deb [signed-by=/usr/share/keyrings/msft.gpg arch=amd64] https://packages.microsoft.com/ubuntu/20.04/prod focal main" | sudo tee /etc/apt/sources.list.d/msprod.list

    sudo apt update
    ```

1. Install the Intel SGX SDK and build prerequisites

    ```bash
    sudo apt install -y build-essential libssl-dev libsgx-quote-ex libsgx-enclave-common libsgx-enclave-common-dev libsgx-dcap-ql libsgx-dcap-ql-dev az-dcap-client
    ```

1. Install the Intel SGX SDK.

    ```bash
    wget https://download.01.org/intel-sgx/sgx-dcap/1.20/linux/distro/ubuntu20.04-server/sgx_linux_x64_sdk_2.23.100.2.bin

    chmod +x sgx_linux_x64_sdk_2.23.100.2.bin 
    sudo ./sgx_linux_x64_sdk_2.23.100.2.bin 
        Do you want to install in current directory? [yes/no] N
        Please input the directory which you want to install in : /opt/intel
    source /opt/intel/sgxsdk/environment
    echo "source /opt/intel/sgxsdk/environment" >> ~/.bashrc && source ~/.bashrc
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

## Install Intel Trust Authority client for C

The Intel SGX example uses the Intel Trust Authority client for C and the Intel SGX adapter to collect evidence from the enclave. The evidence is sent to Intel Trust Authority for attestation. If attestation is successful, an attestation token (JWT) is returned. An example attestation token for Intel SGX is shown in the following listing.

![SGX Application Stack](/img/tutorial-sgx-azure/sgx-application-stack.png)

This demonstrates the attester and verifier portions of the [passport attestation model.](../../Concepts/concept-patterns.md#workflows)

1. Build the sample application.

    ```bash
    git clone https://github.com/intel/trustauthority-client-for-c
    cd trustauthority-client-for-c/
    make sgx_token_docker
    ```

2. Configure your API key and any desired policy to evaluate.

    Set the attestation API key and optionally a policy ID to evaluate (The POLICY_ID is commented out below):

    ```bash
    cat <<EOF | tee sgx_token.env
    TRUSTAUTHORITY_API_KEY=<trustauthority-api-key>
    # TRUSTAUTHORITY_POLICY_ID=<trustauthority-policy-id - optional>
    TRUSTAUTHORITY_API_URL=https://api.trustauthority.intel.com
    TRUSTAUTHORITY_BASE_URL=https://portal.trustauthority.intel.com
    SGX_AESM_ADDR=1
    EOF
    ```

:::note
If you are in the European Union (EU) region, use the following Intel Trust Authority URLs:

`TRUSTAUTHORITY_API_URL=https://api.eu.trustauthority.intel.com`
`TRUSTAUTHORITY_BASE_URL=https://portal.eu.trustauthority.intel.com`
:::

1. Run the sample application.

    The sample SGX client application executes the attester and verifier portions of the passport attestation mode. The container uses the Intel Trust Authority client to retrieve evidence from the host and enclave. It sends that evidence as a quote in an attestation request to Intel Trust Authority. The application outputs the resulting attestation token, demonstrating a successful attestation.

    ```bash
    sudo docker run -it --rm --device=/dev/sgx_enclave --device=/dev/sgx_provision -v /var/run/aesmd/aesm.socket:/var/run/aesmd/aesm.socket --env-file sgx_token.env --group-add $(getent group sgx_prv | cut -d: -f3) taas/sgx_token:v1.0.0
    ```

### Output

```bash
[LOG:2024-04-30 02:16:13::/trustauthority-client/examples/sgx_token/sgx_token.c::205] Info: Successfully verified token

[LOG:2024-04-30 02:16:13::/trustauthority-client/examples/sgx_token/sgx_token.c::206] Info: Parsed token : 

{
    "alg": "PS384",
    "jku": "https://portal.trustauthority.intel.com/certs",
    "kid": "79d80711b754cceb307d4278dc59957f27eb55a8e33d3b824967975843dcbf21df924eebaf93fce186fd291d36817785",
    "typ": "JWT"
}
.
{
    "attester_advisory_ids": [
        "INTEL-SA-00615"
    ],
    "attester_held_data": "AQABADlv1PbS1x7IfABDWhiRefEW3gL/2sh7jDxJPwpTFIpEjgbNTkmSAPC/oT/3hhKI5PERYnpC4fwZycYWl9vYyv4YC4Ogjy7xjMmOuE3Eizqothe/Gb4nHa0KhVgq2vLYAd6O/jvvDD1X3MKtJs/wJDVBFWzt++n
dN9bxdG12cjida5TBihJyACdDwbwDLV3fTGtPaHCIT6f/FV5C3dwqUwkE/hfHR2ykImp7kKGldPkQt3XRlv/Ot4fgU2seWqv6uJ0EDf6dWrdyFYumF3RvrzFEhz2Xf0pQyXCJjKEFTJTdhktDd1qLmyccyz0NBz5SVbh/sk4WzUllhsSrmYmpGxClNZRn8
4sv8JRGMxYM6FZzSgiPO67HPkg5+S/My4+AaRvaqyZgiqADzQkE61IRpyFGk+KePGKuS9/jwe3/6i6/8SM0aXRyE3E2CwjorfIZ0As5VhdMzH/duvIuAoyzVOSy+Qj1+cC64g3t6sAAonC87V9c3w+4nhPbj/lslGTp1Q==",
    "attester_tcb_date": "2023-08-09T00:00:00Z",
    "attester_tcb_status": "SWHardeningNeeded",
    "attester_type": "SGX",
    "dbgstat": "disabled",
    "eat_profile": "https://portal.trustauthority.intel.com/eat_profile.html",
    "exp": 1714443672,
    "iat": 1714443372,
    "intuse": "generic",
    "iss": "Intel Trust Authority",
    "jti": "59aeaed5-d127-420b-939d-b378ad4ac300",
    "nbf": 1714443372,
    "policy_ids_unmatched": [
        {
            "hash": "RHdQVDZwUEdUN0k1QTFQZnBpN2Izekt1dDdLQ0RoYUFJVmh4UzNLTVZjOUJEamQzdmtIem5jNG92NnZONlFNNw==",
            "id": "d970fa2b-34bc-476d-ad8f-7a1b78f2885e",
            "version": "v1"
        }
    ],
    "sgx_collateral": {
        "qeidcerthash": "b2ca71b8e849d5e799451b4bfe43159a0ee548032cecb2c0e479bf6ee3f39fd1",
        "qeidcrlhash": "ca685ff1fa572b5fd5b0d10c1e06fce40f25544729b6052689583aa17166ab85",
        "qeidhash": "e22c9d22d3e2323586c713ffdb0c840477e7435cabc8d6ded7c32f6e86e45160",
        "quotehash": "0ce7045396560ba539baf2755103b3e3d47c9bf11232ce8b85c64ac832502f6b",
        "tcbinfocerthash": "b2ca71b8e849d5e799451b4bfe43159a0ee548032cecb2c0e479bf6ee3f39fd1",
        "tcbinfocrlhash": "ca685ff1fa572b5fd5b0d10c1e06fce40f25544729b6052689583aa17166ab85",
        "tcbinfohash": "0e69d829c612d7dcad0916a34290fc0a313864200a30c2f5de40b45b2d927ddf"
    },
    "sgx_is_debuggable": false,
    "sgx_isvprodid": 0,
    "sgx_isvsvn": 0,
    "sgx_mrenclave": "69a8788a94e77a4d0cb91a5974022c4fa3422fb6fad96d576af38ff42a7a9f3d",
    "sgx_mrsigner": "d412a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b",
    "sgx_report_data": "5446be95dcffa3c875fd6f5611122241c2997bf1fafa575ce7bc9ad26d52d4b80000000000000000000000000000000000000000000000000000000000000000",
    "ver": "1.0.0",
    "verifier_instance_ids": [
        "aece4c92-dab7-43b6-b05a-e8ec6544669f",
        "45d26b15-a647-4df2-8392-757d549e4534",
        "be637f4e-7a84-4caa-b9bd-7dc49134b63d",
        "df99b3b0-62d4-476b-8243-bbb294776883",
        "53eeeba5-dc3c-4070-85b4-3192c6f1e01c"
    ],
    "verifier_nonce": {
        "iat": "MjAyNC0wNC0zMCAwMjoxNjoxMiArMDAwMCBVVEM=",
        "signature": "hFiNLoiTeStP18ZXIERxgVT2BTYhu76OWnNbycnpPt4CymibR2DHfejFpr65gvgLsnPiwoVRj51ld374BdNueFu+lHdqFqlmdzgPZ93UzN2zwQZKn318lVo+Fhhp9rSn2kAhwM+Opb6do2PmG7JpWf61det9V/m+9jZcQVX8
kzdbhOGtSbqFpSwD9KaXoxTRPha/+zzN8oKqrNhG0/XYCD7112Arlfxdao5RDASNqGJmt27d9ivE2zX77dXt1RUSI9TdEkjVKYIuBdTUq+fkLm3kfeqqM0b//zG0ov3ceoDluySVwv162A1X6lHvoJfNcC2VwlYhHWW/9dT9ptQPx9OZXaQFRaK7ZwjoVo
CmbO6/s86b8GdVEKOTI2+CVNbE/lRPQEFthc4L6uRzPJboKqzTlCYMvc6nxVo3fqWsMVE83llw8bJ2KkFUzZPVl3Wlzp4CLUcpdVT31X5Pm8KC0+l3lQfThSdYiBvFt6fDOfvzcilMQO2DDX/5JNYaiCqD",
        "val": "VVJTM1duVXBGbS9XVEc1cG82WXl3MlVpWGRSM3VJL20wUnUrZ3UvSVBKbGN4bUZjd0Z2ekxvNjlUcy9VZHIvQjEvRzRhSXFLY3Z5QjhraFNrc3RlS3c9PQ=="
    }
}
```
