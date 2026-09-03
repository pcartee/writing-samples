---
title: Glossary
description: Contains definitions for terms used in the documentation.
author: pcartee
topic: conceptual
date: 10/15/2024
uid: concept.glossary
---

*· October/15/2024 ·*

# Intel® Trust Authority Glossary

The following terms are used in the Intel Trust Authority documentation. Terminology related to the attestation process (attester, endorser, verifier, etc) is derived from [IETF RFC 9334](https://datatracker.ietf.org/doc/rfc9334/), Remote ATestation procedureS (RATS). Terms specific to Intel Trust Authority are prefixed with "Intel Trust Authority," for example, "Intel Trust Authority admin API key." Other terms are industry standard. Terms marked with an asterisk ( * ) may be names and/or brands that are claimed as the property of entities other than Intel.

#### Admin API key
An Intel Trust Authority _admin API key_ (also called a _management API key_) is required to manage Intel Trust Authority products, service offers, users, policies, and tags. An Admin API key allows the bearer to manage a tenant's entire Intel Trust Authority subscription.

:::warning
Intel Trust Authority admin API keys are extremely sensitive values that must be safeguarded against unauthorized use.
:::

#### API URL

**Intel Trust Authority Base URL** redirects here.

The REST API, and therefore all integration clients and CLIs, require two URLs to function: the Base URL `https://portal.trustauthority.intel.com` and the API URL `https://api.trustauthority.intel.com`.

There is a third well-known URL to return the JWKS of signing certificates used for Intel Trust Authority attestation tokens and nonces: `https://portal.trustauthority.intel.com/certs`.

:::note
If you are in the European Union (EU) region, use the following Intel Trust Authority URLs:

- Base URL — `https://portal.eu.trustauthority.intel.com`
- API URL — `https://api.eu.trustauthority.intel.com`

:::

#### Attestation API key
An Intel Trust Authority _attestation API key_ is required for all attestation-related functions. An attestation API key can't be used for management APIs (and vice-versa; an Admin API key can't be used for attestation). An Attestation API key can be created using the REST API, but the key value can only be retrieved through the [Intel Trust Authority Portal](https://portal.trustauthority.intel.com).

#### Attestation appraisal policy
An _attestation appraisal policy_ is used by the relying party to evaluate claims in the attestation token.

#### Attestation token
An Intel Trust Authority _attestation token_ is a JSON Web Token (JWT) that is generated as a result of verification. An attestation token is sometimes called an "attestation report," though that term is not used in this documentation. The JWT contains both incoming claims (evidence) and outgoing claims and is signed with a certificate that can be traced to Intel. Relying parties use attestation tokens to decide what, if any, confidential services or data to release to the attester.

#### Attester
The _attester_ is an entity that provides evidence (a _quote_) to a verifier as to its integrity.

#### Attestation
_Attestation_ is the process by which cryptographically verifiable claims can be made by a trusted authority based on a set of evidence. For example, an Intel® Software Guard Extensions (Intel® SGX) enclave can generate a quote that can be sent to an attestation authority (such as Intel Trust Authority) to validate the integrity and identity of the quoted enclave.

#### Challenger
A _challenger_ is an entity that requests integrity metrics and evaluates the level of trust in the attester. When an attester is challenged, it may respond with either a quote or an attestation token, depending on the needs of the relying party.

#### Claim
Quotes and attestation tokens are composed of elements called _claims_. A claim usually assigns some value to a named element, often a cryptographic token that represents the signature of a component of the TCB. _Incoming claims_ are part of the attester quote. _Outgoing claims_ are elements added to the attestation token by Intel Trust Authority. For more information, see [Attestation tokens and claims](Concepts/concept-attestation-tokens.md).



#### Composite attestation

The goal of _composite attestation_ to create a single attestation of a trusted computing boundary, which can include a TEE, GPU, and other components. Evidence is collected for each of the components within the trusted compute boundary, combined, and evaluated against one or more composite attestation appraisal policies. The result is a single attestation token that includes claims for all components within the trusted compute boundary.

#### Intel SGX DCAP
_Intel® Software Guard Extensions Data Center Attestation Primitives (Intel® SGX DCAP)_ is a software infrastructure that helps collect TEE evidence for a quote, which is sent to a verifier (such as Intel Trust Authority) for attestation. 

#### ECDSA
_Elliptic Curve Digital Signature Algorithm (ECDSA)_ is a cryptographic algorithm. Intel Trust Authority uses ECDSA as an integral part of the attestation process. For more information, see [Intel Software Guard Extensions ECDSA - Attestation for Data Center Orientation Guide](https://download.01.org/intel-sgx/dcap-1.0.1/docs/Intel_SGX_DCAP_ECDSA_Orientation.pdf).

/* #### Enclave identity */

#### Endorser
An _endorser_ is an entity that endorses or substantiates evidence provided by the attester or verifier. For example, when the attester provides the key that identifies the Intel® SGX-enabled processor, that key can be verified, or endorsed, by comparing it to the original value provided by the Intel® SGX Provisioning Certification Service.

#### Entity
An _entity_ is any component or actor with a role in the attestation process. Entities are usually logical, e.g. a service, complex logic, or human component, as opposed to a device such as a disk controller or router card.

#### Faithful Verification
The [Intel Trust Authority Faithful Verifier (FV) tool](././Utilites/utility-faithful-verifier.md) is a Linux command-line utility that is used to verify the fidelity of an Intel Trust Authority token. The Faithful Verifier tool can be downloaded from the Intel Trust Authority web interface downloads page.

#### GSC
_Gramine Shielded Containers (GSC)_* provide the infrastructure to deploy Docker* containers protected by Intel SGX enclaves using the Gramine Library OS*. For more information, see [Intel Trust Authority Gramine integration](../ita/Integration/integrate-gramine.md).

#### HSM
A _Hardware Security Module (HSM)_ is a highly secure, tamper-resistant, hardware-based component for storing and managing digital secrets. 

#### ISV SVN
The Intel SGX enclave author assigns a _Security Version Number (SVN)_ to each version of an enclave. The SVN indicates when security-related updates have occurred. A new version of the enclave can be issued without updating the SVN if no security-related changes are made.

#### ISV Product ID
The enclave author assigns a _product ID_ to each enclave. The product ID allows the enclave author to segment enclaves with the same enclave author identity. After an enclave is successfully initialized, the product ID is recorded by the CPU to be used during attestation.

#### JSON Web Key (JWK)

From [IETF RFC 7517](https://datatracker.ietf.org/doc/html/rfc7517): "A JSON Web Key (JWK) is a JavaScript Object Notation (JSON) data structure that represents a cryptographic key." RFC 7517 also defines a JWK Set JSON data structure that represents a set of JWKs. Intel Trust Authority signing certificates conform to the JWK standard. The list of signing certificates used by Intel Trust Authority for signing attestation tokens and nonces is returned in a JWKS (JSON Web Key Set). The Intel Trust Authority JWKS URL is `https://portal.trustauthority.intel.com/certs`.

#### KMS

**KBS** redirects here.

A Key Management System (KMS) is a secure system for storing and managing keys and other digital secrets. A KMS may or may not also implement a Key Broker System (KBS), which brokers access to secrets pending a successful remote attestation. A KMS stores and safeguards secrets. A KBS acts as an intermediary between the KMS and confidential computing workload by confirming the identity and attestation status and applying key release policies. The KMS or KBS is a relying party in the remote attestation workflow.

#### Nonce
A _nonce_ is a signed JSON object literal that's used to help mitigate replay attacks and ensure the freshness of an attestation quote or token. A nonce is signed with the PS384 algorithm.

A user-provided nonce is optional for most APIs. If provided, the verifier nonce that was used for the attestation request is embedded in the resulting attestation token. The integration client API requests a nonce if the user doesn't provide one.  

#### OPA
Intel Trust Authority uses _Open Policy Agent (OPA)*_ as its policy evaluation engine. For more information about OPA, see the [OPA documentation](https://www.openpolicyagent.org/docs/latest/).

#### PCS
_Intel® Software Guard Extensions Provisioning Certification Service (Intel® SGX Provisioning Certification Service)_ is a  provisioning certificate caching service implemented in nodejs for reference. It retrieves PCK certificates and other collaterals on demand using the internet at runtime, and then caches them in local database.

#### Policy
An Intel Trust Authority _policy_ is a collection of rules that are used to evaluate claims and define the requirements to issue an attestation token. Relying parties usually have their own distinct policy language and requirements.

#### Product
An Intel Trust Authority _product_ is a grouping of APIs used to define the services enabled for tenants.

#### Quote
A TEE _quote_ is evidence of trustworthiness of the enclave and is used during remote attestation. Different TEEs implement quoting mechanisms differently, but in all cases the quote represents cryptographically verifiable evidence gathered from a variety of sources during enclave provisioning. A quote is made up of a collection of claims.

#### Reference value
A _reference value_ is a value that claims can be compared against. Reference values are often cryptographic measurements of entities and devices. Reference values are stored in a secure repository such as an HSM or TPM.

#### Relying party
The _relying party_ is any consumer of an attestation token, or to put it another way, the relying party is any entity that must trust the attester.  The relying party is so called because it relies on claims made in the attestation token created by the verifier to establish trust in the attester. Relying parties must have their own verifier or verification logic to parse and appraise an Intel Trust Authority attestation token.

#### Request ID
The REST API and client library APIs generally accept an optional RequestID parameter. Intel Trust Authority doesn't read this value, it just passes the value along with the request throughout the system as a method of tracking. If you don't assign a request ID the API gateway will assign an ID, however, it is not guaranteed to be unique.

The request ID maximum length is 128 characters. It can include characters a-z, A-Z, 0-9, and - (hyphen); no other special characters are allowed.
#### Service Offer
An Intel Trust Authority _service offer_ is a collection of one or more products bundled together.

/* #### Signing identity */

#### Intel SGX
_Intel® Software Guard Extensions (Intel® SGX)_ helps protect data in use via application isolation technology. By protecting selected code and data from modification, developers can partition their application into hardened enclaves or trusted execution modules to help increase application security. Intel SGX enclaves can be attested to prove their integrity and isolation from other system processes.

#### SIEM
Security Information and Event Management (SIEM). SIEM services provide consolidation of security logs and events into a single management tool.

#### Tag
An Intel Trust Authority _tag_ is an optional key-value pair that can be associated with an API key to help collect reporting and metrics information.

#### TCB
The Intel platform Trusted Computing Base (TCB) comprises the components that are critical to meeting Intel's platform security objectives. Platform TCB components include the processor hardware, processor microcode, system firmware, BIOS settings, and platform software (PSW).

#### TEE
A _Trusted Execution Environment (TEE)_ is a secured environment that protects the integrity and confidentiality of code and data during execution by isolating itself from the rest of the compute elements. Intel SGX is an example of a TEE. For more information about TEEs, see the [TEE Overview](Attestation%20Technologies/concept-tees-overview.md).

#### Trust
_Trust_ is the assured reliance on the attributes and behaviors of a given entity.

#### TPM
A _Trusted Platform Module (TPM)_ is a secure cryptoprocessor that provides cryptographic generation and storage functions. A TPM is often a separate chip, but it can be integrated as an independent device in a processor or a virtual hardware emulator (vTPM).  For more information, see the [TPM Library Specification](https://trustedcomputinggroup.org/resource/tpm-library-specification/).

#### Verifier
A _verifier_ is an entity that evaluates evidence from an attester.

 
---

**\*** Other names and brands may be claimed as the property of others.
