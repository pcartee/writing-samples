---
title: Intel® Key Broker Service
description: Key Broker Service documentation.
author: carteepaul
topic: KBS
date: 04/18/2024
uid: kbs.about
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Key Broker Service - Intel® Trust Authority

The Intel Key Broker Service (KBS) enables key distribution using a Trusted Execution Environment (TEE) like Software Guard Extensions (SGX) and Trusted Domain Extensions (TDX) attestation to authorize key transfers by retaining image decryption keys. Intel KBS acts as a bridge between an attestation service (like Intel® Trust Authority) and the existing ecosystem of Key Management Interoperability Protocol (KMIP) key management platforms. It brokers access to the secrets stored in the Key Management Services (KMS) by evaluating attestation tokens against a key transfer policy that informs the broker of the specific trust requirements for retrieving a key.

In remote attestation, a relying party (e.g., a key manager, secrets vault, network access controller, etc.) must establish trust with a workload (an attester). The relying party uses a remote attestation service (e.g., a verifier) to appraise evidence from the attester and issue an attestation of that appraisal (an attestation token).

However, there is a gap between relying parties and verifiers - for example, Hashicorp Vault does not natively integrate with any remote attestation authority. Intel KBS attempts to fill this gap by providing an intermediary.

A KBS in the backend can plug into a KMIP Key Management Service (KMS), i.e., the KBS connects to a backend 3rd Party KMIP-compliant KMS such as Hashicorp Vault or PyKMIP for key creation and secure storage services.

## Intel KBS use cases

Intel KBS is a relying party in a remote attestation. It provides the following functionalities:

- Manages the policies associated with a key
- Provides the interface to support key requests/transfers in two situations:
  - Passport mode - A POST request to the key request URL with an attestation token in the request body.
  - Background check mode - The key is requested without an attestation token from Intel Trust Authority in the request body. Instead, Intel KBS requires a TEE quote, verifier-nonce, and runtime data, i.e., the public key created by the workload that was attested.

<Tabs>
<TabItem value="passport-verification-mode" label="Passport verification mode" default>

In Passport Verification mode, a relying party (a TEE agent or an Intel KBS client) makes an attestation request directly to the verifier (Trust Authority Attestation Service) and gets an attestation token. The attestera calls the Intel KBS key transfer API to request a key.

Intel KBS verifies the legitimacy of the attestation token and determines whether it complies with the key policy associated with the key ID. If it does, the requested key is issued.

</TabItem>
<TabItem value="backgroung-verification-mode" label="Background verification mode">

The workload (key requester) "requests to Intel KBS" to retrieve a particular key. Intel KBS then "reaches out" to Intel Trust Authority to get a nonce, which is forwarded to the workload to get a quote. The quote and nonce are then sent to Intel Trust Authority to get the attestation token.

### Background verification mode steps

- Intel KBS checks the corresponding key policy to see what type of attestation is required.
- If the attestation type and attestation token are not provided as a part of the key transfer API request, Intel KBS requests a nonce from Intel Trust Authority.
- Intel Trust Authority responds with a nonce. Intel KBS responds to the key requestor with the same nonce and attestation type present in the key policy.
- (For Intel native hardware only) The key requestor retrieves the quote from the attester. It sends a request to Intel KBS, this time with a quote, runtime-data (public-key generated inside TEE) in the request body, along with a verifier-nonce.
- KBS checks if the attestation type in the request is the same as the attestation type in the key policy.
- If the attestation type matches with the key policy, KBS forwards the request to Intel Trust Authority with the quote, runtime-data, and a verifier-nonce; it also optionally sends a list of policy IDs to be matched by Intel Trust Authority in the request body.
- Intel Trust Authority verifies the nonce and quote and then issues the attestation token to KBS on successful verification.
- KBS then parses the attestation token to get all the claims and matches the token claims with the policy associated with the key to be retrieved.
- If all the token claims match against the policy, KBS creates an symmetrical key and wraps the secret/key with the symmetrical key, and the symmetrical key is wrapped with a public key received in the request (runtime-data).
- KBS responds with a encpulated requested key and a wrapped symmetrical key to the key requestor.

</TabItem>
</Tabs>

## Format of the released key

After evaluating the key release policy and determining that the key can be released, Intel KBS wraps the key in a client-owned public key. A simple workflow sample for a KBS implementation is as follows:

- Intel KBS accespts a quote and a public key from the client.
- Intel KBS retrieves the key from the KMS and wraps it using the AES-GCMN wrapping algorithm creating a symmetric key. This is used to encrypt the user key (wrapped key).
- The symmetric key is wrapped using the RSA-OAEP algorithm using the public key provided in the Intel Trust Authority attestation token from the **attester_held_data** claim. The asymmetric key pair is usually created by the workload and sent to Intel Trust Authority along with the quote when the attestation token is retrieved.

The intent of wrapping the public key before releasing it is to protect the keys in transit. The key is meant to be decrypted only by the entity requesting it.

Sample output of key retrieval is as follows:

```bash
{
"wrapped_key" : ,
"wrapped_swk": <wrapped AES key with the public key from user/workload>
}
```

Follow the [Intel Key Broker Service installation](../Key-broker/key-broker-service-install.md) instructions to install Intel KBS.
