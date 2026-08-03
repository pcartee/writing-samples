---
title:  Trust Authority Client Tutorial for Google Cloud Platform with TDX
description: Step-by-step tutorial to stand up a GCP VM with TDX 
author: mkwilbux
topic-type: tutorial
date: 12/19/24
uid: tdx.gcp
--- 

*· 12/19/2024 ·*

## Trust Authority Client Tutorial - TDX Attestation on GCP

This tutorial provides steps to deploy a demo app that uses the Trust Authority client when securing an application using Trust Domain Extensions (TDX) on on Google Cloud Platform**\*** (GCP).

The demo application, built for TDX, uses the Trust Authority client to retrieve evidence from the platform and request an attestation Authority. This demonstrates a simple passport attestation model (stopping before involving a relying party). The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your applications.

## Creating a CVM with TDX on GCP
Create a Confidential VM (CVM) that supports TDX on GCP, with the following attributes:

- Virtual machine name - Give your virtual machine a name
- Machine type: **c3-standard-4**
- Zone: **us-central1-a**
- Confidential compute type: **TDX**      
- Maintenance policy: **TERMINATE**
- Image family: **ubuntu-2204-lts**  
- Image project: **ubuntu-os-cloud**

    :::note
    The availability of confidential VMs with TDX images and sizes in specific regions and availability zones is dynamic and may change. This tutorial uses US Cental a as an example. If you're outside North America, you may need to select a different region and availability zone. Check the Google [Products by Region](https://cloud.google.com/compute/docs/regions-zones) page to find the regions and availability zones with available Confidential VM with TDX support.
    :::

To get a list of compute images for TDX, use the following command in Cloud Shell.

```bash
gcloud compute images list --filter="guestOsFeatures[].type:(TDX_CAPABLE)"
```

To create a GCP CVM with TDX, perform the following steps. 

1. Sign in to GCP [here](https://console.cloud.google.com/).

1. Select the option to **Create a VM**. 

1. Open the Cloud Shell by selecting the terminal icon in the upper right of the screen. The Cloud Shell terminal displays.

   The following is an example of creating a CVM in the Cloud Shell with Ubuntu* 22.04 LTS TDX.

   ```bash
      gcloud compute instances create gcp-tdx-vm \
         --machine-type=c3-standard-4 \
         --zone=us-central1-a \
         --confidential-compute-type=TDX \
         --maintenance-policy=TERMINATE \
         --image-family=ubuntu-2204-lts \
         --image-project=ubuntu-os-cloud
   ```

Once the CVM is created, you should have information display details in the Cloud Shell such as name, zone, machine type, IP addresses, and status. Refresh the browser to view the CVM in the **VM Instances** list.

## Connect to the CVM via SSH 
After the CVM is created, exit the Cloud Shell terminal and connect to the CVM via SSH. You can connect in the browser with the following steps. 

1. Select the drop-down arrow for SSH in the **Connect** category for your VM. 

1. Select **Open in browser window**.

    After this selection, you will have a **SSH in browser** window display. In this step, another window displays with a button for you to **Authorize**.

1. Select the **Authorize** button.
After authorization you will have a terminal display, in the browser, connected via SSH to your CVM.

## GCP CVM TDX prerequisites
In this section, you will verify tdx is active, install required packages, and login to github. 

1. To verify that the CVM is TDX enabled, use the following command. This should print `Memory Encryption Features active: TDX`. If this is missing, TDX is not enabled. In that case, check to see that the parameters are correct.

   ```bash
      sudo dmesg | grep -i tdx
   ```

CVM setup is now complete. You can now proceed to install the Trust Authority Attestation Client CLI.

## Install and configure the Attestation Client CLI

The Trust Authority CLI client provides a command-line wrapper for Golang client libraries. Follow these steps to install and configure the Trust Authority Attestation Client CLI.

1. Go 1.22 or later is required to run the Attestation Client CLI. The following commands install Go on Ubuntu 22.04 LTS.

    ```bash
    wget https://go.dev/dl/go1.23.1.linux-amd64.tar.gz;ls
    sudo tar -xvf go1.23.1.linux-amd64.tar.gz -C /usr/local
    export PATH=$PATH:/usr/local/go/bin
    ```
1. Verify that Go is installed correctly by running `go version`. The output should be similar to `go version go1.23.1 linux/amd64`.

1. Install the Attestation Client CLI. This script will install the Attestation Client CLI and its dependencies. You might need to restart one or more services.

```bash
curl -sL https://raw.githubusercontent.com/company/trustauthority-client-for-go/main/release/install-tdx-cli.sh | sudo bash -
```

Verify the Attestation Client CLI is installed correctly by running `trustauthority-cli version`. 

Configure your API key and any desired policy to evaluate. Set the attestation API key and attestation endpoint.

1. Create config.json. 

   ```bash
   touch config.json 
   ```
   
1. You must configure certain properties before using the token and verify commands. The properties and values are saved as JSON in config.json. The config.json requires the following properties:

   ```bash
   cat <<EOF> config.json
   {
      "trustauthority_api_url": "https://api.trustauthority.company.com",
      "trustauthority_api_key": "<attestation api key>"
   }
   EOF
   ```

    :::note
    If you are in the European Union (EU) region, use the following Trust Authority URL:

    `"trustauthority_api_url": "https://api.eu.trustauthority.company.com"`
    :::
## Demonstrate attestation of TDX on GCP

This section takes you through the steps to attest your confidential virtual machine (CVM) with the Trust Authority Attestation Client CLI. 

1. Display evidence for TDX. This displays the evidence that would be sent to the Trust Authority verifier for attestation.

   ```bash
   sudo trustauthority-cli evidence --tdx -c config.json
   ```
   
   ```
   [DEBUG] GET https://api.trustauthority.company.com/appraisal/v2/nonce
   {
   "tdx": {
        "runtime_data": null,
        "quote": "BA... AA=",
        "event_log": "W3...1d=",
        "verifier_nonce": {
           "val": "cV...Q==",
           "iat": "M...EM=",
           "signature": "vc...L"
           }
        }
   }
   ```
1. Generate an TDX attestation token. The _token_ command automatically collects evidence from TDX, and sends it to Trust Authority for attestation. The output will be an attestation token containing the claims for TDX.

   ```bash
   sudo trustauthority-cli token -c config.json
   ```
   
You can experiment with the other `trustauthority-cli` commands. To see them all, run `trustauthority-cli --help`. When you're done experimenting, you can delete the resource group to free up all the resources you created for this tutorial.

For more information about TDX see
the [TDX main page](https://www.company.com/content/www/us/en/developer/articles/technical/company-trust-domain-extensions.html).

For more information, see the [Trust Authority Attestation Client CLI documentation](https://docs.trustauthority.company.com/main/articles/integrate-go-tdx-cli.html).

**\*** Other names and brands may be claimed as the property of others.