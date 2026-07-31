---
title: Intel Trust Authority Client Tutorial for Google Cloud Platform with AMD* SEV-SNP
description: Step-by-step tutorial to stand up a GCP CVM with AMD* SEV-SNP 
author: mkwilbux
topic-type: tutorial
date: 12/19/24
uid: tutorial.sevsnp.gcp
---

*· 12/19/2024 ·*

## Intel Trust Authority Client Tutorial - AMD SEV-SNP Attestation on GCP

This tutorial provides steps to deploy a demo application that uses the Intel® Trust Authority client for securing an application using AMD* SEV-SNP on Google Cloud Platform**\*** (GCP).

The demo application, built for AMD* SEV-SNP, uses the Intel Trust Authority client to retrieve evidence from the platform and request an attestation from Intel Trust Authority. This demonstrates a simple passport attestation model (stopping before involving a relying party). The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your applications.

## Creating a CVM with AMD SEV-SNP on GCP

To create a Confidential virtual machine (CVM) with AMD SEVSNP on GCP, sign in to GCP and create a CVM using the terminal. When creating an instance using GCP web UI, all AMD CVMs default to SEV instead of SEV-SNP. These instructions use the Cloud Shell terminal to create an AMD SEV-SNP CVM.

Create a CVM that supports AMD SEV-SNP on GCP, with the following attributes: 

- Virtual machine name - Give your virtual machine a name
- Machine type: **n2d-standard-2**
- Minimum CPU platform: **AMD Milan**
- Zone: **us-central1-a**
- Confidential compute type: **SEV_SNP**      
- Maintenance policy: **TERMINATE**
- Image family: **ubuntu-2204-lts**  
- Image project: **ubuntu-os-cloud**

:::note
The availability of specific CVM images in specific regions and availability zones is dynamic and may change. This tutorial uses us-central-a as an example. If you're outside North America, you may need to select a different region and availability zone. Check the Google [Regions and zones](https://cloud.google.com/compute/docs/regions-zones) page to find the regions and availability zones with available Confidential VMs with AMD SEV-SNP support.
:::

To get a list of compute images for AMD SEV-SNP, use the following command in Google Cloud Shell.

```bash
gcloud compute images list --filter="guestOsFeatures[].type:SEV_SNP_CAPABLE" 
```

Use the following steps to create a GCP CVM in Cloud Shell.

1. Sign in to GCP [here](https://console.cloud.google.com/).

1. Select the option to **Create a VM**. 

1. Open the Cloud Shell by selecting the terminal icon in the upper right of the screen. Cloud Shell terminal displays.

1. Create the CVM in Cloud Shell.

   The following is an example of creating a CVM using Ubuntu* 22.04 LTS with AMD SEV-SNP in Cloud Shell.

   ```bash
      gcloud compute instances create sev-snp-vm \
         --machine-type=n2d-standard-2 \
         --min-cpu-platform="AMD  Milan" \
         --zone=us-central1-a \
         --confidential-compute-type=SEV_SNP \
         --maintenance-policy=TERMINATE \
         --image-family=ubuntu-2204-lts \
         --image-project=ubuntu-os-cloud
   ```

Once the CVM is created, you should have information display details such as name, zone, machine type, IP addresses, and status.
    
## Connect to the CVM via SSH 
After the CVM is created, exit the Cloud Shell terminal and connect to the CVM with SSH. You can connect in the browser with the following steps. 

1. Select the drop-down arrow for SSH in the **Connect** category for your CVM. 

1. Select **Open in browser window**.

   After this selection, you will have a **SSH in browser** window display. In this step, another window displays with a button for you to **Authorize**.

1. Select the **Authorize** button. After authorization you will have a terminal display, in the browser, connected via SSH to your CVM.

## GCP CVM AMD SEV-SNP prerequisites

To verify that the CVM is AMD SEV-SNP is enabled, use the following command. This should print `Memory Encryption Features active: SEV-SNP`. If this is missing, SEV-SNP is not enabled. In that case, check to see that the parameters are correct.

   ```bash
      sudo dmesg | grep -i sev-snp
   ```

To run the initial setup, you will need the following dependencies.
    
    - git
    - Go*
    - make
    - gcc 
    - gh

Install the required packages.

## Use the GitHub* CLI to connect to GitHub. 
Use the following commands to check the version, login, and check the status. 

To check the version, use `--version`.

```bash 
      gh --version
```

1. Login with GitHub CLI with the following command.

   ```bash
         gh auth login
   ```

   Follow the on-screen prompts. You will be prompted to select Github.com or Github Enterprise server. 
   
1. Select your account.
   
   ```
      What account do you want to login to? 
      Github.com or GitHub Enterprise Server
   ```

1. Select HTTPS or SSH.

   ```
      What is your preferred protocol for Git operationa? HTTPS or SSH
   ```

1. You will be prompted to authenticate with GitHub credentials. Press **Enter** for Yes or type **n** for no then **Enter**. 

   ```
      HTTPS > Authenticate Git with your Github credentials (Y/n)
   ```

1. You will be prompted to authenticate with a web browser or authentication token.

   ```
      How would you like to authenticate GitHub CLI?
      Login with a web browser or Paste an authentication token?
   ```

1. Select the option for web browser and use the **Enter** key. A one-time code displays.

1. Copy the one-time code. The following text displays to open the browser. 

   ```
      Press **Enter** to open github.com in your browser...
   ```

1. Press **Enter**. If the browser does not open, try entering the URL https://github.com/login/device in your browser manually to authorize your gh login in a browser. The URL takes you to **Device Activation**.
   
   a. Select **Continue**.
   
   b. Enter the one-time code. An **authorize cli** screen displays.
   
   c. Select **Authorize github**. A **confirm access** screen displays.
   
   d. Enter the password.
   
   e. Select **confirm**. A screen displays with the following message: Congratulations, you're all set! Your device is now connected. 
   
   f. Return to the SSH connect window. The terminal displays that the authentication is complete. 

1. Press **Enter** to continue. Information displays that you are logged in. 

1. Check the status of GitHub CLI by running the command below. The output will confirm you are logged into github.com.

   ```bash
      gh auth status 
   ```

## Install Intel Trust Authority client for Go

The Intel Trust Authority CLI client provides a command-line wrapper for Golang client libraries. The following steps will get and build Intel Trust Authority client for Go client.

:::note
The preview branch is being checked out for the GCP AMD SEV-SNP feature, because this feature is not supported on the main branch of the client CLI.
:::

1. Build the Intel Trust Authority client.

   ```bash
      git clone https://github.com/intel/trustauthority-client -b sevsnp-preview \
      cd trustauthority-client/sevsnp-cli \
      make cli
   ```

   Configure your API key and any desired policy to evaluate. Set the attestation API key and attestation endpoint.

1. Create config.json.

   ```bash
   touch config.json
   ```

1. You must configure certain properties before using the token and verify commands. The properties and values are saved as JSON in config.json. The config.json requires the following properties:

   ```bash
      cat <<EOF> config.json
         {
            "trustauthority_api_url": "https://api.pilot.trustauthority.intel.com",
            "trustauthority_api_key": "<attestation api key>"
         }
      EOF
   ```

:::note
If you are in the European Union (EU) region, use the following Intel Trust Authority URL:

`"trustauthority_api_url": "https://api.eu.trustauthority.intel.com"`
:::

1. Run the sample application. Use the `trustauthority-cli` utility to request an attestation. The _token_ command automatically collects evidence from SEV-SNP and requests an attestation token from Intel Trust Authority. Full usage details for the `trustauthority-cli` utility can be found at [Intel Trust Authority Attestation Client CLI documentation](https://docs.trustauthority.intel.com/main/articles/integrate-go-client.html).

   ```bash
      sudo ./trustauthority-sevsnp-cli token --config config.json
   ```

**\*** Other names and brands may be claimed as the property of others.