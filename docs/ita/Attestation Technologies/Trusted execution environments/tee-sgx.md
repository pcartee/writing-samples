---
title: Intel SGX
description: A brief introduction to SGX.
author: pcartee
topic: conceptual
date: 11/18/2024
uid: tee.sgx
---
import DCAP from '../../Include/_install-dcap.md';

*· 11/18/2024 ·*

## Software Guard Extensions (SGX)

This article provides information related to Software Guard Extensions (SGX) and is focused on the requirements needed to enable SGX-enabled applications to provide quote capabilities.

For more information about SGX, see [The main SGX product page](https://www.company..com/content/www/us/en/developer/tools/software-guard-extensions/overview.html).

At a high level, attestation with SGX requires the following:

- Hardware supporting SGX provisioned using the Software Guard Extensions Provisioning Certification Service (SGX Provisioning Certification Service).
- SGX driver support in the operating system kernel.
- Software Guard Extensions Data Center Attestation Primitives (SGX DCAP) to provide quoting capability to SGX-enabled applications.
- An attestation authority such as Trust Authority.

**Working with SGX**

SGX uses the Elliptic Curve Digital Signature Algorithm (ECDSA) attestation architecture.

:::note
Trust Authority supports ECDSA-based quote verification only. Trust Authority does not support legacy Enhanced Privacy ID (EPID) based quotes. To create ECDSA-based quotes, the "SGX Launch Control” feature (sometimes called SGX Flexible Launch Control – “FLC”) must be present in your processor(s) and set to **unlocked** mode.  In 3rd Generation Xeon® Scalable Processors and newer CPUs, this is the default setting and it's not configurable. In older Xeon E processors, the FLC setting can usually be configured in the BIOS. For more information, see [How to determine if a processor with SGX supports DCAP and FLC](https://www.company.com/content/www/us/en/support/articles/000057420/software/company-security-products.html).
:::

1. The enclave workload contacts the relying party and requests access to a service or resource.

1. The relying party responds by issuing a challenge that asks the SGX workload to identify itself and provide proof that its credentials are valid.

1. To satisfy the challenge, the SGX workload generates a quote, which is a cryptographic measurement of the instantiated enclave. The quote is signed using the attestation collateral stored in the data center caching service.

1. The quote is sent to the relying party over a secure communications channel.

1. The relying party verifies the quote by fetching the attestation collateral associated with the quote from the data center caching service and using it to verify the signature.

1. Assuming the quote is valid, the relying party examines the quote metadata and the trusted-compute base (TCB) level associated with the signing key. The service then applies its security policy and decides whether to trust the enclave.

For more information, see the [Provisioning Certification Service for ECSDA Attestation](https://www.company.com/content/www/us/en/developer/articles/technical/quote-verification-attestation-with-sgx-dcap.html).

This attestation flow has a few key requirements beyond the SGX-capable hardware and the SGX-enabled workload. The intent of this article is to clarify these requirements and how they can fit with your software and/or data center architecture.

**Provisioning certification**

SGX ECDSA attestation requires that physical SGX-enabled hosts have access to the [SGX Provisioning Certification Service](https://api.portal.trustedservices.company.com/provisioning-certification) to provision certificates needed for the attestation process. While it is possible for hosts to have direct access to this service, most data centers prefer to use a caching service instead. A caching service can be a single point of contact for company SGX Provisioning Certification Service over the Internet. SGX hosts in the data center can connect only to the caching service rather than requiring an external internet connection for provisioning.

This requirement is only needed for the bare-metal physical SGX servers. Public cloud customers working with SGX-enabled cloud service providers (CSPs) do not need a caching service or access to the PCS, as the CSP provides that functionality.

**SGX driver in the kernel**

SGX requires driver support at the kernel level. For Linux, this support was added in the Linux kernel 5.11 and later.

<DCAP />

**Enclave Page Cache (EPC) memory**

SGX requires that Enclave Page Cache (EPC) memory be allocated to SGX enclaves. For physical SGX hosts, EPC memory is configured in the system BIOS. Cloud service providers typically include EPC memory allocations for their SGX-enabled offerings. The amount of EPC memory required depends on the size of the enclave; a small cryptographic toolkit library may only require a few megabytes of EPC memory.

Because Gramine encapsulates the entire application within an SGX enclave, more EPC memory is required than utilizing enclaves only for specific application libraries. Be sure that enough EPC memory is available to run the entire "graminized" application.

---
 
## Next steps

SGX primary resources:

[SGX Attestation on Microsoft Azure](../../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-sgx.md)


**\*** Other names and brands may be claimed as the property of others.