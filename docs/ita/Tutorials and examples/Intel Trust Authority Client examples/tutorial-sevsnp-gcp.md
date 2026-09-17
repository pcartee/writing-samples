---
title: Trust Authority Client Tutorial for Google Cloud Platform with AMD SEV-SNP
description: Tutorial for creating a Google Cloud confidential VM with AMD SEV-SNP, authenticating with GitHub CLI, and building the Trust Authority client for Go.
author: pcartee
topic-type: tutorial
date: 12/19/24
uid: tutorial.sevsnp.gcp
---

## Trust Authority Client Tutorial: AMD SEV-SNP Attestation on GCP

This tutorial explains how to deploy a demo application that uses the Trust Authority client to secure an application with AMD SEV-SNP on Google Cloud Platform**\*** (GCP).

The demo application, built for AMD SEV-SNP, uses the Trust Authority client to retrieve evidence from the platform and request an attestation from Trust Authority. This demonstrates a simple passport attestation model that stops before involving a relying party. The application's output is the resulting attestation token. The demo application can be used as a workflow reference for your applications.

## Create a CVM with AMD SEV-SNP on GCP

To create a confidential VM (CVM) with AMD SEV-SNP on GCP, sign in to GCP and create a CVM using the terminal. When creating an instance using the GCP web UI, all AMD CVMs default to SEV instead of SEV-SNP. These instructions use the Cloud Shell terminal to create an AMD SEV-SNP CVM.

Create a CVM that supports AMD SEV-SNP on GCP with the following attributes:

- Virtual machine name - Give your virtual machine a name
- Machine type: **n2d-standard-2**
- Minimum CPU platform: **AMD Milan**
- Zone: **us-central1-a**
- Confidential compute type: **SEV_SNP**
- Maintenance policy: **TERMINATE**
- Image family: **ubuntu-2204-lts**
- Image project: **ubuntu-os-cloud**

:::note
The availability of specific CVM images in specific regions and availability zones is dynamic and may change. This tutorial uses `us-central1-a` as an example. If you're outside North America, you may need to select a different region and availability zone. Check the Google [Regions and zones](https://cloud.google.com/compute/docs/regions-zones) page to find the regions and availability zones with available Confidential VMs with AMD SEV-SNP support.
:::

To get a list of compute images for AMD SEV-SNP, use the following command in Google Cloud Shell.

```bash
gcloud compute images list --filter="guestOsFeatures[].type:SEV_SNP_CAPABLE"
```

Use the following steps to create a GCP CVM in Cloud Shell.

1. Sign in to the [Google Cloud console](https://console.cloud.google.com/).

1. Select the option to **Create a VM**.

1. Open Cloud Shell by selecting the terminal icon in the upper-right corner of the screen. The Cloud Shell terminal displays.

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

Once the CVM is created, you should see details such as the name, zone, machine type, IP addresses, and status.

## Connect to the CVM via SSH

After the CVM is created, exit the Cloud Shell terminal and connect to the CVM through SSH. You can connect in the browser with the following steps.

1. Select the drop-down arrow for SSH in the **Connect** category for your CVM.

1. Select **Open in browser window**.

   After this selection, an **SSH in browser** window appears. Another window displays a button for you to **Authorize**.

1. Select the **Authorize** button. After authorization, a browser terminal connects to your CVM through SSH.

## GCP CVM AMD SEV-SNP Prerequisites

To verify that AMD SEV-SNP is enabled on the CVM, use the following command. This should print `Memory Encryption Features active: SEV-SNP`. If this is missing, SEV-SNP is not enabled. In that case, check that the parameters are correct.

   ```bash
      sudo dmesg | grep -i sev-snp
   ```

To run the initial setup, you will need the following dependencies:

- git
- Go
- make
- gcc
- gh

Install the required packages.

## Use GitHub CLI to Connect to GitHub

Use the following commands to check the version, log in, and check the status.

To check the version, use `--version`.

```bash
gh --version
```

1. Log in with GitHub CLI by running the following command.

   ```bash
         gh auth login
   ```

   Follow the on-screen prompts. You will be prompted to select GitHub.com or a GitHub Enterprise Server.

1. Select your account.

   ```text
      What account do you want to log in to?
      GitHub.com or GitHub Enterprise Server
   ```

1. Select HTTPS or SSH.

   ```text
      What is your preferred protocol for Git operations? HTTPS or SSH
   ```

1. You will be prompted to authenticate with GitHub credentials. Press **Enter** for Yes or type **n** for no, then press **Enter**.

   ```text
      HTTPS > Authenticate Git with your GitHub credentials (Y/n)
   ```

1. You will be prompted to authenticate with a web browser or authentication token.

   ```text
      How would you like to authenticate GitHub CLI?
      Login with a web browser or Paste an authentication token?
   ```

1. Select the option for web browser and use the **Enter** key. A one-time code displays.

1. Copy the one-time code. The following text displays to open the browser.

   ```text
      Press **Enter** to open github.com in your browser...
   ```

1. Press **Enter**. If the browser does not open, manually enter [the GitHub device activation URL](https://github.com/login/device) in your browser to authorize your `gh` login. The URL takes you to **Device Activation**.

   a. Select **Continue**.

   b. Enter the one-time code. An **Authorize CLI** screen displays.
   c. Select **Authorize GitHub**. A **Confirm access** screen displays.

   d. Enter the password.

   e. Select **Confirm**. A screen displays the following message: Congratulations, you're all set! Your device is now connected.

   f. Return to the SSH connect window. The terminal displays that authentication is complete.

1. Press **Enter** to continue. Information displays that you are logged in.

1. Check the status of GitHub CLI by running the command below. The output will confirm you are logged into github.com.

   ```bash
      gh auth status
   ```

## Install the Trust Authority Client for Go

The Trust Authority CLI client provides a command-line wrapper for Go client libraries. The following steps download and build the client for Go.

:::note
The preview branch is being checked out for the GCP AMD SEV-SNP feature, because this feature is not supported on the main branch of the client CLI.
:::

1. Build the Trust Authority client.

   ```bash
      git clone https://github.com/company/application-client -b sevsnp-preview \
      cd application-client/sevsnp-cli \
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
            "application_api_url": "https://[redacted]",
            "application_api_key": "<attestation api key>"
         }
      EOF
   ```

:::note
If you are in the European Union (EU) region, use the following Company Name URL:

`"application_api_url": "https://[redacted]"`
:::

1. Run the sample application. Use the `application-cli` utility to request an attestation. The *token* command automatically collects evidence from SEV-SNP and requests an attestation token from Trust Authority. For full usage details, see the [Trust Authority Client CLI documentation](https://docs.application.company.com/main/articles/integrate-go-client.html).

   ```bash
      sudo ./application-sevsnp-cli token --config config.json
   ```

**\*** Other names and brands may be claimed as the property of others.
