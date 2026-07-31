---
title: TEE TDX
description: A brief introduction to TDX.
author: pcartee
topic: conceptual
date: 05/16/2025
uid: tee.tdx
---

*· 05/16/2025 ·*

## Intel® Trust Domain Extensions (Intel® TDX)

[Intel® Trust Domain Extension (Intel® TDX)][intel-tdx-dev] allows you to deploy hardware-isolated confidential virtual machines (CVMs) called **trust domains** (TDs). A TD VM is isolated from the virtual machine manager (VMM), hypervisor, and other non-TD software on the host platform. The memory contents of a TD are encrypted using a multiple-key encryption method. Intel TDX aims to exclude the host platform from the TD's trusted computing base (TCB) and isolate multi-tenant TDs from each other.

For the most part, it's not necessary to understand the inner working of Intel TDX to use Intel Trust Authority attestation and tools. However, you _do_ need to know how claims made in evidence relate to system state and the TCB. For more information, see the Intel TDX section of [Attestation Tokens](../../Concepts/concept-attestation-tokens.md). [Attestation policies](../../Concepts/concept-policy-v2.md) provide the enforcement mechanism that allows you to compare the claims and evidence collected from the Intel TDX CVM to reference values, and apply rules and conditions to the claim values.

The root of trust for TDs is the Intel TDX Provisioning Certification Enclave (PCE). The PCE is implemented as an Intel SGX enclave. The PCE signs evidence reports (quotes) for attestation, provisions cryptographic keys, and certifies the platform TCB status. The PCE is remotely attested when the TD is instantiated and whenever an attesting party requests a TD quote.

For more background information about Intel TDX remote attestation at the host level, see the Intel® Confidential Computing Documentation, Intel TDX Enabling Guide [Infrastructure Setup][#tdx-enable-infrastructure]. Fortunately, you don't need to know the details of Intel TDX infrastructure setup if you're using cloud-based CVMs with Intel TDX. You don't need to know any of this info to use Intel Trust Authority attestation. However, if you're setting up an Intel TDX host on-premises, the Intel TDX Enabling Guide and the Canonical [Intel Trust Domain Extensions (TDX) on Ubuntu][#canonical-tdx] are two primary sources for information with which you will become well acquaint ed.

Confidential Virtual Machines (CVM) with Intel TDX can run on-premises and on cloud platforms such as Microsoft Azure **\*** (Azure) and Google Cloud Platform **\*** (GCP). Azure and GCP implement CVMs with Intel TDX differently, however the TEE adapters provided with the Intel® Tiber™ Trust Authority attestation client handle the low-level details. An attesting workload or relying party doesn't need to know which Intel TDX platform it's running on. There are Intel TDX software adapters for on-premises, Azure CVMs with Intel TDX, and GCP CVMs with Intel TDX. The combination of Intel TDX CVM and NVIDIA H100 **\*** GPUs is supported.  [trustauthority-pycli](../GPU%20confidential%20computing/concept-gpu-attestation.md#pytthon-cli) provides a CLI for composite attestation of an Intel TDX CVM and NVIDIA GPU.

To make it easier to add Intel TDX attestation to your workload, Intel Tiber Trust Authority includes an [Attestation CLI](../../Integration/integrate-go-tdx-cli.md) and [Attestation Client](../../Integration/integrate-overview.md) libraries for Go, Python, Java, and C. The Attestation CLI and client connectors abstract most platform details. Attesters and relying parties use the same API for all platforms.

[TD Integrity](../../Concepts/concept-td-integrity.md) is a feature of Intel Tiber Trust Authority that uses evidence collected from boot logs, platform, TPM, and the trust domain to establish a remotely-attested "chain of trust" for CVMs with Intel TDX. A verified chain of trust helps ensure that all of the components of the TCB from hardware to TD are remotely validated and may be considered "trusted."

Some platform and image reference values needed for TD Integrity are obtained from CSPs. CSP reference values are used in an attestation policy to evaluate the evidence collected from the platform and TD. For more information, see the [Intel® Tiber™ Trust Authority TD Integrity repo on GitHub][tdi-repo].

---

**\*** Other names and brands may be claimed as the property of others.

?8 external links */
[tdi-repo]: https://github.com/intel/trustauthority-td-integrity
[tdx-enable-infrastructure]: https://cc-enabling.trustedservices.intel.com/intel-tdx-enabling-guide/02/infrastructure_setup/
[canonical-tdx]: https://github.com/canonical/tdx
[intel-tdx-dev]: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-trust-domain-extensions.html
