---
title: Intel® Trust Authority Java Client Integration
description: Java Client Adaptor documentation.
author: pcartee
topic: integration
date: 11/08/2024
uid: integrate.java.client
---

*· 11/08/2024 ·*

## Intel Trust Authority Client for Java
 
The Java Connector is one of several language-specific clients available for Intel Trust Authority. The client libraries provide an interface to the Intel Trust Authority REST API and (for attesters) the platform software that collects measurements for a quote. A TEE adapter is needed to collect evidence for attestation. Currently, the Java TEE adapters support Intel SGX and Intel TDX. Supported Intel TDX platforms include on-premises Intel TDX hosts, GCP confidential VMs with Intel TDX, and Azure confidential VMs with Intel TDX.


The Intel Trust Authority Java client modules, build, and installation instructions are on [GitHub](https://github.com/intel/trustauthority-client-for-java).

## Java client API index

### Java-connector APIs

[**TrustAuthorityConnector**](#trustauthorityconnector-api)<br />
Establishes a connection with Intel Trust Authority services.

[**attest**](#attest) <br />
Provides a relatively simple method to obtain an attestation token for the client.

[**GetNonce**](#getnonce)<br />
 Retrieves a signed nonce from Intel Trust Authority.

[**GetToken**](#gettoken) <br />
Fetches the token from the TrustAuthority server using the specified API URL.

[**getTokenSigningCertificates**](#gettokensigningcertificates) <br />
Retrieves a certificate from the collection of signing certificates used by Intel Trust Authority to sign attestation tokens.

[**verifyToken**](#verifytoken) <br />
Performs signature verification of attestation token received from Intel Trust Authority.

### Java-SGX adaptor

[**SgxAdapter**](#sgxadapter)<br />
Create a new SGX Adapter.

[**collectEvidence**](#collectevidence)<br />
Collect evidence from an Intel SGX enclave.

### Java-TDX adaptor

[**TdxAdapter**](#tdxadapter)<br />
Create a new Intel TDX adapter.

[**collectEvidence**](#collectevidence)<br />
Collect evidence from an Intel TDX trust domain.


## Java-connector API

The Java Connector module uses Intel Trust Authority REST APIs to communicate with the Intel Trust Authority service. The first step for using the Java Connector is to create a connector instance.

### `TrustAuthorityConnector` API

Create a new Connector instance, then use the exposed interfaces to access different parts of the Intel Trust Authority API.

```java

// Initialize config required for connector using trustAuthorityBaseUrl (https://portal.trustauthority.intel.com), trustAuthorityApiUrl (https://api.trustauthority.intel.com), trustAuthorityApiKey, and retryConfig
Config cfg = new Config(trustAuthorityBaseUrl, trustAuthorityApiUrl, trustAuthorityApiKey, retryConfig);

// Initialize TrustAuthorityConnector with the config
TrustAuthorityConnector connector = new TrustAuthorityConnector(cfg);
```

#### Parameters

|Name     |I/O   |Description                                     |
|---------|------|------------------------------------------------|
|connector|Output|Receives a pointer to a Java TrustAuthorityConnector instance.|
|cfg      |Input |The configuration file provided by the user.    |


#### Cfg Parameters

|Name                  |I/O   |Description                                     |
|----------------------|------|------------------------------------------------|
|trustAuthorityBaseUrl |Input |Intel Trust Authority URL. In the US, use `https://portal.trustauthority.intel.com`. In the EU, use `https://portal.eu.trustauthority.intel.com`.|
|trustAuthorityApiUrl  |Input |Intel Trust Authority API URL. In the US, use `https://api.trustauthority.intel.com`. In the EU, use `https://api.eu.trustauthority.intel.com`. |
|trustAuthorityApiKey  |Input |An Attestation API key for Intel Trust Authority.  |
|retryConfig           |Input |A java class object that holds multiple values required for retry mechanism like retryWaitMin, retryWaitMax, and retryMax.|
|retryWaitMin          |Input |Minimum time required to wait between retries.The default is 2 seconds. | 
|retryWaitMax          |Input |Maximum time required to wait between retries. The fault is 10 seconds. |
|retryMax              |Input |Maximum number of retries.|

### `attest`

**attest** provides a relatively simple method to obtain an attestation token for the client.

```java
public class TrustAuthorityConnector {
    public AttestResponse attest(AttestArgs args) throws Exception{}
}
```
Initiates remote attestation with Trust Authority.

```java
AttestResponse attestResponse = connector.attest(attestArgs);
```

#### attest arguments

|Name      |I/O   |Description                                     |
|----------|------|------------------------------------------------|
|AttestArgs |Input  |The AttestARgs argument has five members: <br /> ***adapter*** - Pointer to an EvidenceAdapter. <br /> ***policyIds*** - An optional list of policyIds provided by the user. <br /> ***requestId*** - An optional request ID to identify the request. For more information, see [Request ID](../glossary.md#request-id). <br /> ***tokenSigningAlg*** — Optional, allows you to select "PS384" (the default if no option is specified) or "RS256" for the token signing algorithm. <br /> ***policyMustMatch*** — Optional, boolean `{true \| false}`. If set to **true**, specifies that all policies must match for Intel Trust Authority to issue an attestation token. The default is **false**, which means that one or more policies can be unmatched and an attestation token will still be issued. |

#### Usage

**attest** is designed for a passport attestation model where the attester wants to get a token and doesn't need to append user data to evidence. The attester only needs to create a new Intel® Trust Authority Client connection and evidence adapter before calling **attest**. If you need to include user data with the evidence, see [GetToken](#gettoken).

**attest** performs the following actions:

- Gets a nonce from Intel Trust Authority.
- Collects evidence by using the TEE adapter.
- Forwards the evidence and policy IDs to Intel Trust Authority.
- Returns an attestation token and HTTP response headers.


### `GetNonce`

**GetNonce** retrieves a signed nonce from Intel Trust Authority.

```java
public class TrustAuthorityConnector {
    public GetNonceResponse GetNonce(GetNonceArgs args) throws Exception {}
}
```

```java
    GetNonceResponse nonceResponse = connector.GetNonce(nonceArgs);
```

#### GetNonce arguments

|Name     |I/O   |Description                                     |
|---------|------|------------------------------------------------|
|**GetNonceArgs.requestId**   |Input |An optional request ID to identify the request. If you don't provide a request ID, the API gateway will create a request ID for you, but it's not guaranteed to be unique. |
|nonce |Output |A signed nonce returned by Intel Trust Authority. |


### `GetToken`

**GetToken** Requests a new Intel Trust Authority attestation token.

```java
public class TrustAuthorityConnector {
    public GetTokenResponse GetToken(GetTokenArgs args) throws Exception {}
}
```

```java
GetTokenResponse tokenResponse = connector.GetToken(tokenArgs);
```

#### GetToken arguments


|Name      |I/O   |Description                                     |
|----------|------|------------------------------------------------|
|GetTokenArgs |Input  |The GetTokenArgs argument has five members:|
|             |       | ***nonce*** - VerifierNonce provided by the user.|
|             |       | ***evidence*** - Pointer to an array containing zero to a maximum of ten policy IDs of policies to apply during attestation.|
|             |       | ***policyIds*** - An optional list of policyIds provided by the user.|
|             |       | ***requestId*** - An optional request ID to identify the request. |
|    |    | ***tokenSigningAlg*** — Optional, allows you to select "PS384" (the default if no option is specified) or "RS256" for the token signing algorithm.  |
|   |   | ***policyMustMatch*** — Optional, boolean `{true \| false}`. If set to **true**, specifies that all policies must match for Intel Trust Authority to issue an attestation token. The default is **false**, which means that one or more policies can be unmatched and an attestation token will still be issued. |


#### Usage

**GetToken** is for complex scenarios where **attest** doesn't provide enough flexibility. **GetToken** Provides more control than attest, by allowing a confidential app to include user_data, provide a nonce, or modify evidence structures before requesting a token. **GetToken** supports both Passport and Background-check validation models.

Policies can be associated with an attestation API key, but if the policyIds are specified directly in the call, this overrides and replaces any policies associated with the API key.


### `getTokenSigningCertificates`

**getTokenSigningCertificates** retrieves a JSON Web Key Set (JWKS) that contains the collection of signing certificates (in JWT format) used by Intel Trust Authority to sign attestation tokens and nonces.

```java
public class TrustAuthorityConnector {
    public String getTokenSigningCertificates() throws Exception {}
}
```
#### Parameters

**getTokenSigningCertificates** doesn't take any input.

```java
String certs = connector.getTokenSigningCertificates();
```


### `verifyToken`

Verifies the signature of the JWT token received from Intel Trust Authority.

The verifyToken does the following:

- Gets the kid from the header
- Gets the signing certificates
- Finds the JWT from kid & verifies the cert against the CA
- Checks to see that the public key can be retrieved from the certificate
- Returns the parsed JWT

A relying party could use the connector and the verifyToken function to validate any received tokens before establishing trust.

```java
public class TrustAuthorityConnector {
    public JWTClaimsSet verifyToken(String token) throws Exception {}
}
```


```Java
JWTClaimsSet claims = connector.verifyToken(token);
```

#### Parameters

|Name     |I/O   |Description                                     |
|---------|------|------------------------------------------------|
|token    |Input |JWT token returned from Intel Trust Authority. |

## Java SGX adapter API reference

Prior to integrating an Intel® SGX workload with the Intel Trust Authority client, the workload must implement a function to generate an enclave report. This function should take the SHA256 hash of the nonce and user data to form report data for the `EnclaveReport`. The Intel Trust Authority Attestation Service performs a report data verification where it expects the report data to be a SHA256 hash of nonce and user_data (if any).


### `SgxAdapter`

The following code fragment creates a new Java SGX adapter and then uses the adapter to collect a quote from the SGX TEE.

```java
SgxAdapter sgxAdapter = new SgxAdapter(enclaveID, useData, EnclaveLibrary.EnclaveFunction);
```

#### Parameters

|Name            |I/O   |Description                                     |
|----------------|------|------------------------------------------------|
|enclaveID       |Input |enclave ID specified by user. |
|userData        |Input |The data, in binary or json format, provided by the user.  |
|EnclaveLibrary.EnclaveFunction  |Input |Function pointer to enclave create report. |


### `collectEvidence`

**collectEvidence** is used to get a quote from an Intel SGX enclave by using Intel® SGX DCAP..

```java
Evidence evidence = sgxAdapter.collectEvidence(nonce);
```

#### Parameters

|Name     |I/O   |Description                                     |
|---------|------|------------------------------------------------|
|nonce|Input |The nonce value provided by the user. |


## Java Intel TDX adapter API reference



The Intel TDX adapter for Java is actually two adapters, one for systems that use the configfs-tsm Linux subsystem for quote generation, such as on-premises Intel TDX hosts and Google Cloud Platform CVMs with Intel TDX, and one for Azure confidential VMs with Intel TDX. Azure uses a proprietary scheme for quote generation. These adapters are installed from the same source and they share an identical package name  (`com.intel.trustauthority.tdx`) and API in the `TdxAdapter` class.


### `TdxAdapter`

Creates a new TdxAdapter instance

```java
TdxAdapter tdxAdapter = new TdxAdapter(userData);
```

#### Parameters

|Name     |I/O   |Description                                     |
|---------|------|------------------------------------------------|
|userData |Input |The userData user data provided by the user.    |


### `collectEvidence`

**collectEvidence**  takes a nonce as input, which is hashed (along with user data, if supplied) during trust domain report creation. 

```java
Evidence evidence = tdxAdapter.collectEvidence(nonce);
```

#### Parameters
|Name     |I/O   |Description                                     |
|---------|------|------------------------------------------------|
|nonce|Input |The nonce value provided by the user. |


