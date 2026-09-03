---
title: Attestation Tokens and Claims
description: attestation token JWT JWK JWKS JOSE EAT profile sample claim 
author: pcartee
topic: conceptual
date: 04/15/2025
uid: attestation.token
---

*· April/15/2025 ·*

import SgxToken from '../Include/eat/_sgx-token.md';
import TdxToken from '../Include/eat/_tdx-token.md';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Attestation tokens and claims

An attestation token is a [JSON Web Token (JWT)][jwt-rfc7519] issued by the verifier (Intel® Trust Authority) and contains the results of an attestation request. The token contains the result of one or more policy appraisals against evidence supplied by an attester. The token is composed of a token header, a token body (various incoming and outgoing claims), and an attestation signature. The contents of the token vary according to the attesting TEE, but certain claims are common to all environments. This article describes the attestation token format and the claims that can be included in an attestation token.

There are three sections in an Intel Trust Authority JWT:

```json
{token header}.{token body}.[signature]
```

1. [Token header](#token-header), also known as the JOSE header. Contains signing and content type claims.
1. [Token body](#token-body), also known as the payload. Contains attester (incoming), verifier (outgoing), and policy-defined (outgoing) claims related to the attested environment.
1. [Token signature](#token-signature). Contains the signature hash for the certificate used by Intel Trust Authority to sign the JWT.

## Token signing algorithm

Intel Trust Authority uses the PS384 algorithm to sign attestation tokens. In some situations it is desirable to use an alternate algorithm to reduce computational overhead and for compatibility with other systems. For this reason, you have the option to request an attestation token signed with the RS256 algorithm.

The token signing algorithm option does not apply to nonces, which are only signed with PS384.

You can select a token signing algorithm when you request an attestation token, either through the [REST API](../Restapi/restapi-intro.md) or one of the [client libraries](../Integration/integrate-overview.md).

For more information about cryptographic algorithms used for signing JWKs, see [IETF RFC-7518](https://datatracker.ietf.org/doc/html/rfc7518).

## Claims usable in policy

Not all claims are available to be referenced in a policy. None of the outgoing claims can be evaluated, and only the following incoming claims are available for use in an appraisal or token customization policy.

- **attester_tcb_status**
- **attester_tcb_date**
- **attester_advisory_ids**
- **sgx_mrenclave**
- **sgx_mrsigner**
- **sgx_isvprodid**
- **sgx_isvsvn**
- **sgx_is_debuggable**
- **tdx_seamsvn**
- **tdx_rtmr0**
- **tdx_rtmr1**
- **tdx_rtmr2**
- **tdx_rtmr3**
- **tdx_mrtd**
- **tdx_mrsignerseam**
- **tdx_is_debuggable**
  
The following AMD SEV-SNP claims can be used in a policy but are only available in pre-release preview in the Intel Trust Authority Pilot environment.

- **sevsnp_guestsvn**
- **sevsnp_authorkeydigest**
- **sevsnp_familyId**
- **sevsnp_imageId**
- **sevsnp_reportdata**
- **sevsnp_launchmeasurement**
- **sevsnp_idkeydigest**
- **sevsnp_hostdata	string**
- **sevsnp_is_debuggable**
- **sevsnp_migration_allowed**
- **sevsnp_smt_allowed**
- **sevsnp_bootloader_svn**
- **sevsnp_microcode_svn**
- **sevsnp_snpfw_sv**
- **sevsnp_tee_svn**
- **sevsnp_vmpl**

## Token header

The JSON Object Signing and Encryption (JOSE) token header is the first bracketed section of the token. The JOSE header contains information regarding the attestation token, such as the type of token, type of the algorithm used, and reference certificate for token verification.

| Claim  | Claim type |Description              |
| ---------- | ------ | ------------------------ |
| **alg**        |  Outgoing |Signature algorithm. Intel Trust Authority uses the **PS384** algorithm, which is RSASSA-PSS using SHA-384 and MFG1 with SHA-384. For more information, see [JSON Web Algorithms RFC7518][jwa-rfc7518]. Attestation tokens returned via the [MAA Adapter](../Concepts/concept-maa-adapter.md) use **RS256** (RSASSA-PCKS1-v1-5 with SHA-256) signature algorithm for compatibility with existing Azure Attestation apps. |
| **jku**        |  Outgoing | JSON web keyset URI. This is the location from which you can retrieve the JSON-encoded public token signing key identified by **kid** to validate the token signature. In practice, this claim is advisory. The recommended best practice is to download the certificates from the Intel Trust Authority well-known URL, and then use **kid** to locate the key used to sign the token. This method avoids using the information contained in the token to validate the token. |
| **kid**        |  Outgoing | Key ID (UUID) for the signing key that is used to sign the token. |
| **typ**        |  Outgoing | Token content type, always `JWT`. |

## Token body

The token body (sometimes called the _payload_), is the main portion of the JWT that contains all incoming and outgoing claims, with the exception of claims in the JOSE header.

Claims in the token body:

- JWT claims that are reused by Intel Trust Authority.
- Verifier claims, including common TEE claims and all Intel Trust Authority claims not covered in EAT-defined claims.
- TEE-specific claims.
- Policy-defined claims inserted by token customization policies.

#### Claim type

A claim is _incoming_ if it is provided to Intel Trust Authority by the attester, or in some cases, by the relying party in background-check mode. A claim is _outgoing_ if it inserted by Intel Trust Authority (verifier) or a custom claim.

### JWT claims

The following claims are reused from JSON Web Token (JWT) [RFC7519](https://datatracker.ietf.org/doc/html/rfc7519). For more information about individual claims, see [Section 4, JWT Claims](https://datatracker.ietf.org/doc/html/rfc7519#section-4).

The term _JWT_ in the following claim definitions refers to the JWT attestation token issued by Intel Trust Authority.

| Claim     | Claim type   | Description                                |
|:------------- | ------------ | ------------------------------------------ |
| **iat**       | Outgoing     | Token issued time. All time-based claims are in Unix epoch time. |
| **exp**       | Outgoing     | Token expiration time. This is the time on or after which the token must not be accepted for processing.  |
| **iss**       | Outgoing     | Token issuer.                              |
| **jti**       | Outgoing     | JWT identifier.                            |
| **ver**       | Outgoing     | Token version.                             |
| **nbf**       | Outgoing     | "Not before" — The time before which the token must not be accepted for processing. |

### EAT claims

Entity Attestation Token (EAT) claims are defined in IETF **draft-ietf-rats-eat** [Section 4, The Claims](https://datatracker.ietf.org/doc/html/draft-ietf-rats-eat#name-the-claims). These claims were added to enhance compatibility with other attestation verifiers.

| Claim     | Claim type   | Description                                |
|:------------- | ------------ | ------------------------------------------ |
| **eat_profile** | Outgoing |The **eat_profile** claim contains a URL or OID that links to the EAT claim profile as defined in the IETF EAT specification Section 6. The value of **eat_profile** is always `https://portal.trustauthority.intel.com/eat_profile.html`. |
| **dbgstat** | Outgoing | The **dbgstat** claim applies to entity-wide or submodule-wide debug facilities of the diagnostic hardware built into chips. This value will be "disabled" if **tee_is_debuggable** is false, or "enabled" if **tee_is_debuggable** is true. This is an important claim to check because debuggable TEEs are not secure. **Never** trust debuggable TEEs with secrets.|
| **intuse** | Outgoing | The **intuse** claim provides an indication to a token consumer about the intended usage of the token. The **intuse** claim  is always "generic" for JWT issued by Intel Trust Authority. Generic is the type reserved for security-oriented attestation/appraisal tokens. |

:::note
If you are in the European Union (EU) region, use the following Intel Trust Authority URL for the value of **eat_profile**:

`https://portal.eu.trustauthority.intel.com/eat_profile.html`
:::

### Verifier claims

| Claim          | Claim type    | Description  |
|:-------------- | ------------- | ------------ |
| **verifier_nonce** | Incoming | If present, contains a complete nonce signed by Intel Trust Authority. |
| **policy_ids_matched**  | Outgoing  | Matched policies — The evaluated policies matched against the quote. This claim is present only if policies are specified and matched.   |
| **policy_ids_unmatched** | Outgoing  | Unmatched policies — The evaluated policies do not match against the quote. This claim is present only if there are unmatched policies.|
| **verifier_instance_ids** | Outgoing  | Instance IDs of the Intel Trust Authority microservices involved in the attestation. These IDs are used for Faithful Verification. For more information, see [Faithful Verification Verifier](../Utilites/utility-faithful-verifier.md).   |

### Attester claims

These claims apply to Intel SGX and Intel TDX attesters.

| Claim   | Claim type    | Description     |
|:------- | ------------- | --------------- |
| **attester_type**   | Outgoing     | The TEE type of the attesting platform, currently either "SGX" or "TDX ".|
| **attester_tcb_date** | Incoming    | The TCB date for the attesting platform. The time value is UTC in ISO 8601 format (YYYY-MM-DDThh:mm:ssZ). |
| **attester_tcb_status**  | Incoming     | TCB level status of the attesting platform. Intel Trust Authority always evaluates TCB status against the latest TCB info from Intel PCS. See the list of [TCB status values](#tcb-status-values) at the end of this section.|
| **attester_advisory_ids**  | Incoming     | An array of Advisory IDs referring to Intel security advisories that provide insight into the reason(s) for the value of **attester_tcb_status** of the platform TCB level being evaluated. To find more information about an Advisory ID (Advisory Number), search the [Intel® Product Security Center Advisories page](https://www.intel.com/content/www/us/en/security-center/default.html).|
| **attester_inittime_data** | Incoming | JSON object literal containing claims that are defined and verified at initialization time of the attested environment. |
| **attester_runtime_data**  | Outgoing | Optional. Runtime_data is optional user data that can be provided along with the quote in an attestation request. The supplied data can be either JSON or binary. If runtime_data is in JSON format, it's output in this claim. If runtime_data is in binary format, it's output in the **attester_held_data** claim. Runtime data is limited to 1 MiB. |
| **attester_held_data** | Outgoing | Optional. If runtime_data or user_data is provided in binary (non-JSON) format, it is output in this claim in base64-encoded format. |
| **attester_user_data** | Outgoing | Optional. This claim is a JSON type. Currently, this claim is present only if the attester is an Azure TDX VM TD _and_ the client provides optional user data in JSON format. |

The last three claims are interrelated. All are optional. These claims are present in the attestation token only if the client provides optional runtime_data with the attestation request. Runtime_data can be provided in JSON or binary format, but due to claims datatype checking performed by Intel Trust Authority, both binary and JSON can't be output to a single claim. That's why there are separate claims for **attester_runtime_data** (JSON object literal) and **attester_held_data** (base64-encoded binary), depending on the data type of the original data.  

An Azure TDX VM is a special case, and the data claims behave differently than as described above. The Azure TD **attester_runtime_data** claim is a pre-defined JSON object literal that is always present. The `runtime_data.user-data` field always contains a SHA512 hash of the verifier nonce (always) and user data (optional). For that reason, a new API `/appraisal/v1/attest/azure/tdxvm` is provided so that the client can supply optional user_data with the runtime_data supplied by the Azure TD client. Optional user_data can be in JSON or binary format. If it's JSON, it's output in **attester_user_data**. If it's binary, it's output in **attester_held_data**.

:::note
Intel Trust Authority expects the lower 32 bytes of the TEE **_report_data** claim to contain a SHA256 hash of the `runtime_data` provided for attestation. 
:::

#### TCB status values

The **attester_tcb_status** claim can have any one of the following values: 

- `UpToDate` — The attesting platform is patched with the latest firmware and software and no known security advisories apply.
- `SWHardeningNeeded` — The platform firmware and software are at the latest security patching level but there are vulnerabilities that can only be mitigated by software changes to the enclave or TD.
- `ConfigurationNeeded` — The platform firmware and software are at the latest security patching level but there are platform hardware configurations required to mitgate vulnerabilities.
- `ConfigurationAndSWHardeningNeeded` — Both of the above.
- `OutOfDate` — The attesting platform software and/or firmware is **not** patched in accordance with the latest TCB Recovery (TCB-R).
- `OutOfDateConfigurationNeeded` The attesting platform is **not** patched in accordance with the latest TCB-R. Hardware configuration is needed.

### Policy-defined claims

Policy-defined claims can be added to the **policy_defined_claims** (outgoing) section by using a token customization policy. Policy-defined claims aren't documented here because the names can be anything the user wants. For more information, see [Token customization policies and custom claims](../Concepts/concept-policies.md#token-customization-policies-and-custom-claims).

### TEE-specific claims

The following claims are specific to the TEEs supported by Intel Trust Authority. In addition to these TEE-specific claims, there are a few claims that are common to all TEEs. The common TEE claims are described in the [Verifier claims](#verifier-claims) section, above.

<Tabs>
<TabItem value="sgx" label="Intel SGX claims" default>

The following claims apply to Intel® Software Guard Extensions (Intel® SGX) enclaves. 

| Claim  | Claim type | Allowed in Policy | Description  |
|:------ | -----------| ------------------| -------------|
| **sgx_mrenclave** | Incoming | Yes | Contains a 256-bit hash that identifies the code and initial data to be placed inside the enclave, the expected order and position in which they are to be placed, and the security properties of those pages. A change in any of these variables will result in a different MRENCLAVE measurement. |
| **sgx_mrsigner** | Incoming |  Yes | Contains a hash of the enclave author's public key. The MRSIGNER value is part of the enclave's signature structure (SIGSTRUCT), and serves to uniquely identify the enclave author. |
| **sgx_isvprodid** | Incoming |  Yes | The ISV product ID of the enclave. It is assigned by the enclave author. |
| **sgx_isvsvn** | Incoming |  Yes |  Yes | The ISV Security Version Number (SVN) of the enclave. The SVN is incremented when a security-related update is made to the enclave. Updates that are not related to the security status don't normally increment the SVN. |
| **sgx_is_debuggable** | Incoming |  Yes | **True** if the Intel SGX debug attribute is enabled, otherwise **false**. **CAUTION**: Debug-enabled enclaves are not secure. The OS and other processes can access a debug-enabled enclave's memory and resources. A debug enclave must never be trusted with any secret. |
| **sgx_config_id** | Incoming | No   |The configuration ID for the Intel SGX report. |
| **sgx_report_data** | Incoming | No   |This claim contains the contents of the 64-byte report data buffer in the Intel SGX report. This claim can be used to transfer data to a relying party, such as a nonce, hash, or cryptographic key. 
| **sgx_collateral** | Incoming |   No |Contains the hash value of the Trusted Compute Base (TCB) attestation collateral being used to verify the quote.|

For more information about these claims, see Intel® SGX Data Center Attestation Primitives: [ECDSA Quote Library API](https://download.01.org/intel-sgx/dcap-1.1/linux/docs/Intel_SGX_ECDSA_QuoteGenReference_DCAP_API_Linux_1.1.pdf).
</TabItem>

<TabItem value="tdx" label="Intel TDX claims">
These claims apply to Intel® Trust Domain Extensions (Intel® TDX) trust domains (TD). The complete definitions of the claims are available in the section A.3.2 of [Intel® Trust Domain Extensions Data Center Attestation Primitives (Intel® TDX DCAP) Quoting Library_API](https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_TDX_DCAP_Quoting_Library_API.pdf). Current versions of the Intel TDX adapter don't use Intel DCAP (quotes are obtained from configfs-tsm), but the claims are still relevant.

| Claim     | Claim type   | Description              |
|:--------- | ------------ | ------------------------ |
| **tdx_mrsignerseam** | Incoming | The measurement of the Intel TDX module signer, if valid. |
| **tdx_mrseam** | Incoming | The measurement of the Intel TDX module. |
| **tdx_mrtd** | Incoming | The measurement of the TD build process and the initial contents of the TD. |
| **tdx_seamsvn** | Incoming | The Intel TDX module security version number (SVN). This claim is incremented by the developer when a security-related change is made to the TD. Updates that don't affect the security status don't usually increment the SVN. For more information, see [SEAM Loader Interface Specification](https://cdrdv2.intel.com/v1/dl/getContent/733584). |
| **tdx_rtmr0** | Incoming | RTMR[0] contains a measurement of the TD virtual firmware (TDVF) configuration. |
| **tdx_rtmr1** | Incoming | RTMR[1] contains measurements of the TD OS loader and kernel. |
| **tdx_rtmr2** | Incoming | RTMR[2] is for the OS application. |
| **tdx_rtmr3** | Incoming | RMTR[3] is reserved for special usage. |
| **tdx_mrconfigid** | Incoming | The software-defined ID for non-owner-defined configuration of the TD, for example, the runtime or OS configuration. |
| **tdx_mrowner** | Incoming | The software-defined ID for the TD’s owner. |
| **tdx_mrownerconfig** | Incoming | The software-defined ID for owner-defined configuration of the TD, that is, specific to the workload rather than the runtime or OS. |
| **tdx_report_data** | Incoming | This claim contains the cumulative SHA512 hash of the nonce supplied with the evidence, runtime_data supplied during quote generation, optional user data (supplied via the `user_data` parameter in client APIs), and attester held data supplied by the TEE during quote generation. Intel Trust Authority quote verification uses this hash to verify the data supplied in the quote. The Intel Trust Authority clients take care of hashing the data for you, however, independently developed clients must contain this logic. For more information, see the Go TDX adapter's [CollectEvidence](https://github.com/intel/trustauthority-client-for-go/blob/14b89ef3b58dac84feb125857f6837c1e1b166f0/go-tdx/collect_evidence.go#L26) function as an example. |
| **tdx_seam_attributes** | Incoming | Additional configuration of the Intel TDX module.  |
| **tdx_td_attributes** | Incoming | The TD attributes bitmap. This claim contains the entire bitmap. The following claims break out certain specific attributes specified in the bitmap. For more information about the TD Attributes structure and the following attributes claims, see Section A.3.4 in the [Intel TDX DCAP][intel_tdx_dcap] quoting library API.|
| **tdx_td_attributes_debug** | Incoming | Defines whether the TD runs in TD debug mode (set to 1) or not (set to 0). **CAUTION**: In TD debug mode, the CPU state and private memory are accessible by the host VMM. |
| **tdx_td_attributes_key_locker** | Incoming | This claim indicates if the TD is allowed to use Intel® Key Locker hardware resources for AES key protection. |
| **tdx_td_attributes_perfmon** | Incoming | TD is allowed to use Perfmon and PERF_METRICS capabilities. |
| **tdx_attributes_protection_keys** | Incoming | TD is allowed to use Supervisor Protection Keys. |
| **tdx_td_attributes_septve_disable** | Incoming | The TD is allowed to use Supervisor Protection Keys.
| **tdx_tee_tcb_svn** | Incoming | Describes the TCB SVNs of TDX. For more information, see [Get TDX TCB Info](https://api.portal.trustedservices.intel.com/documentation#pcs-tcb-info-tdx-v4). |
| **tdx_xfam** | Incoming | Contains an XFAM mask of CPU extended features that the TD is allowed to use. XFAM (eXtended Features Available Mask) is defined as a 64-bit bitmap. For more information, see Section 22.2.2 in the [TDX Module 1.0 specification](https://cdrdv2.intel.com/v1/dl/getContent/733568).   |
| **tdx_is_debuggable** | Incoming | This claim indicates if the Intel TDX debug attribute is enabled or not. **True** if enabled, otherwise **false**. **CAUTION**: A TD in debug mode is not secure because the host VM can access the CPU state and TD private memory.|
| **tdx_collateral** | Incoming | Contains the hash value of the binary TCB collateral being used to verify the the quote.  |
| **tdx_pcesvn** | Incoming | The security version number (SVN) of the Intel TDX Provisioning Certification Enclave (PCE). |
| **tdx_tcb_comp_svn** | Incoming | The Intel TDX PCE is implemented as an Intel SGX enclave. **tdx_tcb_comp_svn** contains an array of tcb sgxcomp(onent) SVNs encoded in JSON. The list comes from the Provisioning Certification Key (PCK) certificate (PckCerts) "tcb" object, which is referenced during remote attestation of the PCE. The list of component SVNs can be useful for troubleshooting unexpected **attester_tcb_status** status values. For more information, see [Get SGX TCB Info V4](https://api.portal.trustedservices.intel.com/content/documentation.html#pcs-tcb-info-v4) in the Intel API Documentation.|
</TabItem>
</Tabs>

## Token signature

This section contains the cryptographic hash produced by the key that was used to sign the token. Verifying the signature ensures that the contents of the token haven't been tampered with.

To verify the token signature, first download the Intel Trust Authority signing certificates from the portal. Then use the **kid** claim to retrieve the key you need. The **jku** claim is there for informational purposes.

## Sample tokens

The following attestation token examples were generated for their respective TEE. These samples don't contain every possible claim for the TEE, but they are typical for most scenarios. The claims hash values and Base64 or base64url-encoded strings are truncated for brevity.

<Tabs>
<TabItem value="sgx-token" label="Intel SGX">

### Intel SGX

<SgxToken />

</TabItem>

<TabItem value="tab/tdx-token" label="Intel TDX">

### Intel TDX

<TdxToken />

</TabItem>
</Tabs>

**\*** Other names and brands may be claimed as the property of others.

/* External link URLs */
[jwt-rfc7519]: https://www.rfc-editor.org/rfc/rfc7519
[jwa-rfc7518]: https://datatracker.ietf.org/doc/rfc7518/
[draft-ietf-rats-eat21]: https://datatracker.ietf.org/doc/html/draft-ietf-rats-eat
[ietf]: https://www.ietf.org/
[intel_sgx]: https://www.intel.com/content/www/us/en/developer/tools/software-guard-extensions/overview.html
[intel_tdx]: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-trust-domain-extensions.html
[intel_tdx_dcap]: https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_TDX_DCAP_Quoting_Library_API.pdf