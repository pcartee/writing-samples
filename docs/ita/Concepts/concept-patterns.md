---
title: Intel® Trust Authority Attestation Patterns
description: An overview of the Passport and Background Check attestation patterns.
author: grminch
topic: Conceptual
date: 09/01/2023
uid: attestation.patterns  
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Attestation patterns

Attestation patterns provide a generalized communications topology for common attestation use cases. This article is an overview of the passport and background check models. 

In the _Passport_ model, the [attester](../glossary.md#attester) obtains an attestation token from Intel® Trust Authority and then forwards it to a [relying party](../glossary.md#relying-party) as a passport for authentication. In the _Background Check_ model, a relying party challenges the attester to prove its authenticity by obtaining a [quote](../glossary.md#quote) from the attester and forwarding it to Intel Trust Authority for verification or background check. In both models, the relying party must have the ability to verify an [attestation token](../glossary.md#attestation-token) issued by Intel Trust Authority.

Your application can use a combination of attestation models, depending on the role(s) it has in the attestation process. For more information about attestation roles and patterns (topologies), see [Remote ATtestation procedureS (RATS) Architecture (RFC 9334)][rats_rfc].  

_Key release_ is a common use case closely related to attestation. The key release pattern depends on using a Intel Trust Authority attestation token in the collateral needed to get an online vault or KMS to release keys (secrets) to the attester. The attester uses these secrets to get access to confidential data and workloads.

## Workflows

The following workflows are applicable to Intel SGX enclaves, Intel TDX Trust Domains, and Gramine Shielded Containers (GSC) with the integrated Intel Trust Authority client.

<Tabs>
<TabItem value="passport" label="Passport">

### Passport

The _Passport_ pattern is when the attester works with the verifier (Intel Trust Authority) to get an attestation token that is provided to a relying party. The attester initiates the attestation process and the attester works with the verifier to get an attestation token. The relying party plays no role in obtaining an attestation token, however, the relying party is responsible for verifying the attestation token and then deciding if it should trust the attester.

![Passport attestation model](../../../Static/img/concept-usecases-overview/passport-attestation.png)

### Passport workflow

In the passport model, the attester is responsible for initiating the process of collecting evidence, packaging the evidence as a quote, and then forwarding the quote to a verifier for attestation. The attester might need a token to respond to a challenge or to request protected resources from a relying party. The general workflow is as follows.

1. An application running in a supported TEE needs to get an attestation token. To obtain an attestation token from Intel Trust Authority, the application must present evidence to prove that it is authentic and trustworthy. The app uses the Intel Trust Authority client to get the quote and request a token. The client includes functions (virtual device files for Gramine) designed to simplify the process for getting an attestation token when using the passport model. 
    1. In the simplest case when there's no requirement to add user data to the evidence, an application only needs to make one call and specify a list of policy IDs to evaluate. 
    1. In more complex cases the attester can collect evidence, add a nonce and user data, and then retrieve a token from Intel Trust Authority.
1. Intel Trust Authority evaluates the claims evidence and applies policies.
1. Intel Trust Authority returns a signed attestation token that includes outgoing claims containing policy evaluation results. An attestation token is returned unless an error occurs, even if no user-supplied policies are matched.
1. The application forwards the attestation token to the relying party or challenger. 
1. The relying party verifies the attestation token and then decides if it should trust the attester.
    1. Use VerifyToken to check that the token header and signature are valid. 
    1. (Optional) Use Faithful Verifier to verify the integrity of the Intel Trust Authority microservices used during attestation.
    1. Check the list of matched_policies and unmatched_policies to verify that all of the required policies were matched during attestation.
    1. (Optional) Perform signed policy verification.
    1. Extract and verify other claims data as necessary.
</TabItem>
<TabItem value="background" label="Background Check">

### Background Check

The _Background Check_ pattern is when the attester provides a quote to a relying party that uses the quote to obtain an attestation token from the verifier (Intel Trust Authority). The relying party works with Intel Trust Authority to get an attestation token. In response to a challenge or in a request body, the attester must provide a quote and optionally, a nonce. The relying party is responsible for getting an attestation token from Intel Trust Authority and for verifying the token.

![Background Check attestation model](../../../Static/img//concept-usecases-overview//background-attestation.png)

### Background check workflow

1. The background check workflow can be initiated by the relying party or by the attester. In either case, the attester must send a quote to the relying party. The attester uses the Intel Trust Authority client or CLI to collect evidence from the TEE and package it as a quote.
    1. The quote can contain a nonce that is provided to the attester by the relying party. When the attester responds with a quote containing the nonce, the relying party knows that the attester is the same one that received the challenge.
    1. The attester can add user data to the evidence. If user data is included, Intel Trust Authority adds a user_data outgoing claim to the token. Frequently, the value of user_data is a key to use for key wrapping.
1. The relying party forwards the quote and a nonce to Intel Trust Authority with a request for an attestation token.
    1. The relying party can append user data to the evidence before sending it to Intel Trust Authority for attestation. User data added by the relying party can be appended to, or replace, user data added by the attester.
    1. The attestation request should include a list of policies to apply during evidence verification. The list of policies can include both appraisal and token customization policies.
1. Intel Trust Authority verifies the evidence against reference values stored in the HSM.
1. Intel Trust Authority returns an attestation token unless an error occurs.
1. The relying party verifies the attestation token and then decides if it should trust the attester.
    1. Use VerifyToken to check that the token header and signature are valid.
    1. (Optional) Use Faithful Verifier to verify the integrity of the Intel Trust Authority microservices used during attestation.
    1. Check the list of matched_policies and unmatched_policies to verify that all of the required policies were matched during attestation.
    1. (Optional) Perform signed policy verification.
    1. Extract and verify other claims data as necessary.


# [Key Release](#key,release)

Key release is common use case that relies on a key management system (KMS) that protects secret data, such as cryptographic keys, in an online vault. A user of the KMS trusts the vault to protect the user's keys when not in use and to make them available to the user when needed. The user may have multiple devices or cloud-hosted workload environments that need key provisioning. The KMS authenticates the user before provisioning keys to ensure the keys are not inadvertently provisioned to the wrong user.

If the user's authentication credentials are compromised by a malicious actor, the KMS may be tricked into releasing the keys erroneously. Attestation of the user's system and authentication credentials allows the KMS to assess if it is safe to release user keys. 

Key release does not depend on the pattern or model used to obtain an attestation token. In all cases, after an attestation token is obtained, it is used to gain access to resources such as cryptographic keys and confidential data. In a key release scenario, the KMS is the relying party. When a request is made for a secret, the KMS authenticates the requester by using the contents of the attestation token and verifies that the KMS' policy allows release of the information that was requested.

A key consideration for a Intel Trust Authority user is the requirement for the KMS to process a Intel Trust Authority attestation token. Implementation of the key release pattern depends heavily on the requirements of the KMS relying party. The entity requesting a secret must prove its identity and provide a token that is linked to the secret. In most cases, there is an evaluation policy on the KMS that is linked to the secret. The identity information and token must match a policy for the secret to be released.  

If the KMS doesn't have native support for Intel Trust Authority attestation tokens, you need to develop a component that can verify and parse an attestation token and then provide the KMS with the result. Depending on the KMS, you might need to develop an access broker application. An access broker is a proxy component that runs under an account with permission to access the KMS. The access broker authenticates the Intel Trust Authority attestation token, retrieves a key or token from the KMS, and then passes the key back to the attesting workload.

</TabItem>
</Tabs>
---

/* External URLs */
[rats_rfc]: https://datatracker.ietf.org/doc/rfc9334/