---
title: What's New
description: A short description on the new features of Intel Trust Authority.
author: Paul Cartee
topic: conceptual
uid: whats.new
date: 5/20/2025
---

*· 5/20/2025 ·*

### Analytics page for Intel Transparent Supply Chain (TSC) and Intel Platform Lifecycle Integrity (PLI)

A new [analytics](xref:tsc-analytics) page has been added for TSC and PLI subscribers. This page offers a consolidated view for events related to your managed devices, including the number of managed devices, their most recent attestation states, etc. 

### Additional hierarchy layers for partners

[Partners](xref:partner.management) (including managed service partners and subscription resellers) now have the ability to manage additional partners. This allows one parent partner to manage multiple child partners, who in turn can manage or resell tenant subscriptions to Intel Tiber Trust Services.

### Public Preview for AMD SEV-SNP support with vTPM on Microsoft Azure

The [Intel Trust Authority C client](../Integration/integrate-c-client.md) has been updated to support AMD SEV-SNP and vTPM composite attestation for Microsoft Azure. Azure uses the vTPM as a critical chain of trust component for their AMD SEV-SNP implementation. This feature is in preview status, and can be accessed only using the Intel Trust Authority Pilot environment. Contact your Intel representative for access details.

## April 2025

### Google Cloud Platform (GCP) Confidential Spaces (Private Preview) Integration with Intel Trust Authority 

Intel Trust Authority now supports attestation for [Google Cloud Platform Confidential Spaces](../Integration/integrate-gcp-cs.md). This integration enables attestation of GCP Confidential Virtual Machines (CVMs) with Intel TDX using Intel Trust Authority as an independent verifier, separating the attestation provider from the platform provider. Intel Trust Authority provides OIDC-compliant attestation tokens that can be used for key-release scenarios. 

While this feature is generally available from Intel Trust Authority, GCP Confidential Spaces remains in Private Preview status. Contact your Google representative for access.

### Updated Token Claims for Intel TDX

Attestation tokens from Intel Trust Authority that attest Intel TDX will now include additional claims (**tdx_pcesvn** and **tdx_tcb_comp_svn**). For more details, see [Intel TDX claims](../Concepts/concept-attestation-tokens.md#tee-specific-claims)

## March 2025

### Intel Transparent Supply Chain Updates

The [Intel Transparent Supply Chain](xref:tsc.intro) web UI has undergone major changes. These changes are now generally available without access to the Pilot environment.

Intel TSC now supports a new subscription type: Platform Lifecycle Integrity (PLI), which can be obtained as a part of an Intel TSC subscription or standalone. This subscription allows the use of the new Remote Verify Tool to onboard and manage devices that were not part of Intel TSC at the time of manufacture.

### Trust Domain Integrity for Azure and Google Cloud Platform (GCP) Confidential VMs (CVMs) Beta 

Intel Trust Authority now supports [Trust Domain Integrity](../Concepts/concept-td-integrity.md), a sample policy that attests a full chain of trust for Azure and GCP CVMs using Intel TDX. This feature lets security teams use a single appraisal policy to evaluate the integrity of the Trust Domain, virtual firmware, boot loader, and OS, complete with reference values from GCP and Azure.

This feature is currently only enabled for preview on the Intel Trust Authority Pilot environment. See your Intel sales representative to request preview access. 

## February 2025

### Intel Transparent Supply Chain Updates

The [Intel Transparent Supply Chain](xref:tsc.intro) web UI has undergone major changes. These changes are currently only enabled for preview on the Intel Trust Authority Pilot environment. See your Intel sales representative to request preview access.

In addition to the UI changes, the new Transparent Supply Chain Remote Verify Tool is available for preview. This utility allows devices that were not originally manufactured with participation in Intel Transparent Supply Chain by the device OEM to be onboarded by the current device owner and tracked.

## February 2025

### Intel Transparent Supply Chain Updates

The [Intel Transparent Supply Chain](xref:tsc.intro) web UI has undergone major changes. These changes are currently only enabled for preview on the Intel Trust Authority Pilot environment. See your Intel sales representative to request preview access.

In addition to the UI changes, the new Transparent Supply Chain Remote Verify Tool is available for preview. This utility allows devices that were not originally manufactured with participation in Intel Transparent Supply Chain by the device OEM to be onboarded by the current device owner and tracked.

## January 2025

### C Client Support for TPM, AMD SEV-SNP, NVIDIA GPU 

The [C Client](https://github.com/intel/trustauthority-client-for-c) has been updated to add support for TPM, AMD SEV-SNP, and NVIDIA GPU attestation. This includes containerized example applications demonstrating how the client can be implemented for each of these attestation use cases.

AMD SEV-SNP attestation remains a preview feature, available only on the Intel Trust Authority Pilot environment. See your Intel sales representative to request preview access.

## November 2024

### TPM Attestation including IMA and UEFI Event Log General Availability

Attestation using TPMs (including physical TPM and Microsoft Azure vTPM), including attestation of UEFI event logs and using IMA to attest user-defined execution-time files, is now generally available.

### Intel Transparent Supply Chain General Availability

Intel TSC is now generally available. The web UI and Verify tools for both Linux and Windows have been updated.

## October 2024

### vTPM Attestation General Availability

Attestation using Microsoft Azure vTPMs is now generally available. Physical TPM attestation remains available for public preview as a BETA on the Intel Trust Authority Pilot environment.

### TPM attestation with IMA and UEFI Event Logs

Intel Trust Authority now supports optionally adding event log evidence for TPM attestation, including boot-time [UEFI event logs](../Attestation%20Technologies/Trusted%20Platform%20Module/tpm-uefi-log.md) and execution-time [IMA event logs](../Attestation%20Technologies/Trusted%20Platform%20Module/tpm-ima-logs.md). [Event log attestation](../Attestation%20Technologies/Trusted%20Platform%20Module/tpm-log.md) greatly enhances the usability and capability of creating and enforcing policies when using TPM attestation. The addition of IMA support allows attestation of files at execution time, after the system has booted, extending the chain of trust to files executed during runtime.

### Support for Managed Service Partners

Intel Trust Authority now supports [Managed Service Partners](xref:partner.introduction) who can resell and manage Intel Trust Authority subscriptions.

## September 2024

### NVIDIA H100 GPU Attestation is now Generally Available 

[NVIDIA H100 GPU attestation](../Attestation Technologies/GPU confidential computing/concept-gpu-attestation.md) is now generally available. This also means that [V2 Policies](../Concepts/concept-policy-v2.md) are now generally available supporting attestation of NVIDIA H100 GPUs, and composite attestation of NVIDIA H100 GPUs with Intel TDX.

### TPM Attestation Key Provisioning and Physical TPM Attestation BETA

[TPM attestation](../Concepts/concept-trusted-boot.md) is now available for physical TPMs in addition to Microsoft Azure virtual TPMs. Physical TPM attestation requires a TPM Attestation Key certificate endorsed by Intel Trust Authority. The [Attestation Client CLI](../Integration/integrate-go-tdx-cli.md) has new functions to facilitate provisioning an Intel Trust Authority-endorsed Attestation Key certificate. These features are available for preview on the Intel Trust Authority Pilot environment. For access to the Pilot environment, contact your Intel representative.

## July 2024

### TPM Attestation BETA

[TPM attestation](../Concepts/concept-trusted-boot.md) (specifically attestation of Microsoft Azure vTPM) is now available for preview on the Intel Trust Authority Pilot environment. For access to the Pilot environment, contact your Intel representative.

### Policy Builder V2 Policy Support

The [Policy Builder tool](../Utilites/utility-policy-builder.md#composite-policies) now supports V2 Policies (still in preview; see your Intel representative for access), allowing composite policy creation from JSON.

### The "TDX command-line integration" section has been renamed

The Intel Trust Authority [Attestation Client CLI](../Integration/integrate-go-tdx-cli.md) was previously referred to as the "CLI for Intel TDX." This client CLI now supports TPM and AMD SEV-SNP functions (in preview branches), and the section heading has been changed for clarity.

## June 2024

### Policies V2 BETA

[A new version of policy APIs](../Concepts/concept-policy-v2.md) is now available for preview on the Intel Trust Authority Pilot environment. For access to the Pilot environment, contact your Intel representative.

V2 Policies introduce new policy options including "composite" policies that can evaluate evidence from multiple technologies at once (for example, attesting a Virtual Machine using Intel TDX and an NVIDIA H100 GPU).

### AMD SEV-SNP Attestation BETA

[AMD SEV-SNP attestation](../Attestation%20Technologies/concept-tees-overview.md?tabs=amd) is now available for preview on the Intel Trust Authority Pilot environment. For access to the Pilot environment, contact your Intel representative.

### NVIDIA H100 GPU Attestation BETA

[NVIDIA H100 GPU attestation](../Attestation%20Technologies/GPU%20confidential%20computing/concept-gpu-attestation.md) is now available for preview on the Intel Trust Authority Pilot environment. For access to the Pilot environment, contact your Intel representative.

## May 2024

### New Client Tutorials

Added new tutorials demonstrating an attestation workflow using Microsoft Azure with the Intel Trust Authority client libraries. These tutorials are now available for both [Intel SGX](../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-sgx.md) and [Intel TDX](../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-tdx.md).

### SIEM Integration Now Available

You can now [integrate Intel Trust Authority with SIEM platforms](../How-to%20workflows/howto-SIEM-integration.md) (Splunk or Datadog) to push consolidated attestation results as security events.

### Python Client Libraries

Added [Python libraries](../Integration/integrate-python-client.md) for the Intel Trust Authority client.

### Support for External Identity Providers

The Intel Trust Authority portal now supports identity providers other than Intel's SSO. Your login experience may change slightly as a result. Details can be found [here.](../Quickstart/howto-manage-subscriptions.md)

## April 2024
 
### Intel TDX Artificial Intelligence Model Key Release Demo
 
Added a new [tutorial demo](../Tutorials%20and%20examples/tutorial-tdx-workload.md) using Intel Trust Authority and Intel TDX with an encrypted AI model to demonstrate a sample workflow. This tutorial includes pre-configured containers for an attester (the AI workload) and relying party (the Intel Key Broker Service) and a demo script that shows each step of a [key release](../Concepts/concept-patterns.md#key-release) attestation pattern. The decryption key to unseal the AI model is only released when the workload is successfully attested by Intel Trust Authority.

### Attestation Policy Enforcement Option

By default, Intel Trust Authority returns an attestation token regardless of the evaluation of any policies. The relying party must examine the **policy_ids_matched** and **policy_ids_unmatched** in the token to determine the policy results for an attestation request. 

This default token issuance behavior can now be changed by using the **PolicyMustMatch** option in the attestation request. **PolicyMustMatch** is a new optional boolean `{**true** \| **false**}` value that defaults to **false** if not specified. If set to **true**, Intel Trust Authority will issue an attestation token only if all specified policies are matched. If _any_ policy is unmatched, no attestation token is issued.

### Reports and Metrics Page Redesign

The [Reports and Metrics](../How-to%20workflows/howto-reports-metrics.md) page on the Intel Trust Authority Portal has been redesigned for an improved experience.

## March 2024

### Policy Builder Tool

Added the [Policy Builder tool](../Utilites/utility-policy-builder.md). This downloadable utility is available for Linux and Windows, and helps create simplified policies using JSON rather than Rego scripting. The utility accepts a JSON policy as input and produces a Rego policy that can be used with the Intel Trust Authority portal, REST API, or CLI.

### Reports and Metrics

The [Reports and Metrics](../How-to%20workflows/howto-reports-metrics.md) page has received a significant UI redesign.

### Simplified installation for the Intel Trust Authority CLI for Intel TDX

The [Intel Trust Authority TDX CLI client](../Integration/integrate-go-tdx-cli.md) can now be installed via bash scripts. The script will automatically install the correct dependencies and download the correct TDX CLI binary for your TDX provider. 

## February 2024

### [Intel Trust Authority Client for Java](../Integration/integrate-java-client.md)

Client libraries for the Intel Trust Authority [have been added for Java](https://github.com/intel/trustauthority-client-for-java).  

### Support for Intel TDX 1.4 on Microsoft Azure

A number of updates have been made to support Intel TDX 1.4 on Microsoft Azure. This includes:
- changes to [attestation token claims](../Concepts/concept-attestation-tokens.md)
- a new Azure TDX Preview branch for the [Intel Trust Authority client libraries for Go](https://github.com/intel/trustauthority-client-for-go/blob/azure-tdx-preview/go-connector/README.md)
- a new [REST API endpoint](../Restapi/restapi-attestation.md), and 
- updated requirements for the [Intel Trust Authority TDX CLI client](../Integration/integrate-go-tdx-cli.md).

## December 2023

### [Intel Trust Authority Client for C](../Integration/integrate-c-client.md)

Client libraries for the Intel Trust Authority [have been added for C](https://github.com/intel/trustauthority-client-for-c).  As part of this update, the existing client repo (which contains the Golang client) has been moved (https://github.com/intel/trustauthority-client-for-go) to make the repo locations for different language bindings consistent and more intuitive.

## November 2023

### [Platform TCB Policies](../Concepts/concept-platform-tcb.md)

Appraisal policies have been expanded to be capable of evaluating the trusted compute base (TCB) attributes of an attester system.  Not all hardware owners update TCB components like CPU microcode or firmware on the same schedule.  This feature allows the creation of policies that evaluate TCB-related claims including TCB date or security advisory IDs to accommodate patching/upgrade schedules.

### [Decoded JWT attestation tokens in browser](../How-to%20workflows/howto-reports-metrics.md)

When viewing historical attestation tokens from the Reports and Metrics attestation request summary report, the tokens can now be decoded directly in the report window for easier readability.

### Updates to eat_profile

The [eat_profile](https://portal.trustauthority.intel.com/eat_profile.html) has been updated, including a change to the URL.  

## October 2023

### Browser compatibility added to Mozilla Firefox and Safari

Intel Trust Authority is now compatible with Mozilla Firefox and Safari. 

## September 2023

### Intel® Trust Authority General Availability Announcement

Intel Trust Authority, formerly code named _Project Amber_, is now generally available to the public. Customers will now have access to Intel's independent attestation service to verify Confidential Computing environments.  Subscriptions are available by [contacting an Intel® sales representative.](mailto:trustauthority@intel.com)

For more information, visit the [Intel Trust Authority](https://trustauthority.intel.com) product page.

## August 2023 

### Project Amber Limited Availability Launch

Intel’s independent attestation service code named _Project Amber_ has advanced to Limited Availability. Customers interested in using Project Amber to verify Confidential Computing environments or related workloads will have access to production candidate software.