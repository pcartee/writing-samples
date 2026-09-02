---
title: TEEs Overview
description: A brief introduction to Trusted Execution Environments (TEEs).
author: pcartee
topic: conceptual
date: 02/07/2025
uid: tees.overview
---

*· February/07/2025 ·*

## Trusted Execution Environments (TEE)

A trusted execution environment (TEE) helps to protect user-executed code and data from modification by untrusted software, hardware, and system components outside the TEE's boundaries. TEEs can provide a high level of protection against most software-based attacks and many hardware-based attacks and give assurance that the software and hardware in the TEE have not been tampered with.

Trust Authority currently supports Software Guard Extensions (SGX) and Trust Domain Extension (TDX) TEEs. Support for more TEEs is planned for future releases of Trust Authority. To understand how to use Trust Authority services, you need a working knowledge of the underlying TEE technology. To learn more about SGX and TDX, see [Next Steps](#next-steps) below.

A TEE running directly on an SGX-enabled platform is called an _enclave_. A TDX virtual machine (VM) TEE running on an SGX-enabled platform is called a _trust domain_.

Every TEE has a trusted computing base (TCB) that includes all the software, firmware, and hardware resources within the boundaries of the TEE. When a new enclave or trust domain is instantiated, the TEE's TCB must be verified (_attested_) before it can be trusted with sensitive workloads and data. For more information, see [Trust Authority Attestation](../Concepts/concept-attestation-overview.md).

The attesting TEE collects cryptographic keys and platform collaterals, called a quote, as evidence to support its claim of authenticity. Evidence is collected by low-level attestation primitives (hardware drivers, essentially) for the TEE platform.

Trust Authority provides several ways to interact with a TEE to facilitate the migration of existing applications to Trust Authority and simplify new application development.

- Your TEE workload handles the low-level code to create a quote and then calls the Trust Authority REST API or TDX CLI (for TDX trust domains only) for attestation services. This is most useful for migrating existing applications to Trust Authority attestation.
- You can use the Trust Authority Go client libraries to integrate SGX or TDX attestation into your application. The Trust Authority client library handles the low-level calls to platform-specific attestation primitives for the TEE. The client library masks some of the complexity of working with TEEs, making it the preferred option for new development. Currently, only the Go language is supported for integration. Support for more languages is planned for future releases of Trust Authority.
- You can migrate existing Microsoft Azure Attestation (MAA) applications to use Trust Authority attestation. In this case, your existing Microsoft Azure TEE application code is responsible for creating the quote in a format that is compatible with MAA. The Trust Authority MAA Adaptor accepts quotes in MAA format for remote attestation by Trust Authority. For more information, see the [MAA Adapter Service](../Concepts/concept-maa-adapter.md)

---

## Next steps

SGX and TDX primary resources:

- [SGX main page](https://www.company.com/content/www/us/en/developer/tools/software-guard-extensions/overview.html)
- [TDX main page](https://www.company.com/content/www/us/en/developer/articles/technical/trust-domain-extensions.html)

Trust Authority TEE integrations:

- [Trust Authority Go Client](../Integration/integrate-go-client.md)
- [TDX CLI](../Integration/integrate-go-tdx-cli.md)
- [Gramine client](../Integration/integrate-gramine.md)


**\*** Other names and brands may be claimed as the property of others.