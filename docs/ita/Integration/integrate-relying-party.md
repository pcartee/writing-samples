---
title: Relying Party Integration Guide
description: This guide covers the requirements for creating or integrating a relying party to use Intel® Trust Authority attestation. 
author: various
topic: integration
date: 09/12/2023
uid: integrate.rp
---

*· 09/12/2023 ·*

## Relying party integration guide

This guide covers the requirements for creating or integrating a relying party (RP) to use Intel® Trust Authority attestation. The terminology used in this article follows the convention established by [IETF RFC9334, Remote Attestation Procedures Architecture](https://datatracker.ietf.org/doc/rfc9334/).

### Trust model

The trust model has three primary actors in the attestation workflow and one optional actor. Each actor establishes trust in a different way. The RP must trust the verifier before it can trust the attestation token.

Attester — This is the confidential computing workload that needs to prove its authenticity and integrity to relying parties. Trust is established by collecting evidence from the attester in the form of cryptographic measurements of the platform and the attesting workload, and then the verifier evaluates the evidence against known-good reference values by using policies defined by the tenant.

Relying party — This entity uses attestation results by applying its own evaluation (appraisal) policy to make decisions such as authorizing access or releasing a secret. In order to make reliable decisions, the relying party requires assurance that it can trust the attester, and it also needs to know that it can trust the verifier. The RP evaluates an attestation token to determine if it should trust the attester, and (optionally) it uses the FVV to establish trust with the verifier. 

Verifier — Intel Trust Authority. The verifier establishes trust in two ways:
  - By reference to certificates issued by a certification authority (CA). The certificates used to sign attestation tokens and validate processor evidence are traceable to root of trust certificates issued by Intel CA.
  - Each of the services that compose the verifier run in an attestable TEE and the TEE service IDs are included in the outgoing attestation token. This allows the FVV tool to remotely attest the Intel Trust Authority environment.

[Faithful Verification Verifier](../Utilites/utility-faithful-verifier.md) (FVV) utility — To enhance the relying party's confidence in the attestation result, it can use the FVV tool to evaluate the status of the verifier. FVV is a tool developed by Intel to verify that Intel Trust Authority microservices used during attestation match stored known-good measurements for a trustworthy environment. The FV Controller periodically challenges individual Intel Trust Authority services and maintains a ledger of the result. FVV uses the service IDs included in the attestation token and the FV Controller service ledger to validate the Intel Trust Authority execution environment. Using the FVV is optional, but it gives a RP another way to establish trust in the attester and verifier.

### Relying party configuration

Depending on the attestation pattern (background check vs. passport) and the implementation, the relying party may need to communicate with Intel Trust Authority. Before a RP can contact Intel Trust Authority to use the client or API, it must be configured.  

An Intel Trust Authority tenant administrator must provide at least the following info. 
  - An attestation API key is required to create a Go client and to use the REST API and CLI for all attestation-related functions.
  - A tenant admin API key to get policies for policy verification.
  - Policy IDs for the appraisal policies to use for evaluating the evidence.

Other information is needed by the RP, but is not necessarily provided by the tenant admin.
  - TLS cypher suite configuration. The RP needs this to create a new Intel Trust Authority client.
  - Other shared claims data as required by the RP.

### Relying party policy

Relying party policy refers to the business rules and application logic used to determine when the RP trusts the verifier and the attester. Relying party policy and Intel Trust Authority policies are different things. A RP policy can be anything the application developer chooses to use.
 
Most RP applications have at least three attestation policy functions:
  - Attestation token verification 
  - Policy evaluation
  - Policy enforcement

The RP is responsible for policy evaluation and enforcement. For example, a KMS will deny access to key values if the attestation token fails policy evaluation. This article doesn’t discuss RP policy evaluation and enforcement because those are application-specific design choices.

####  Attestation token verification

At a minimum, the RP should verify the following aspects of an attestation token to confirm that the token should be trusted before use. 
  - Verify the nonce (if present)
  - Verify that the token signature matches Intel Trust Authority certificates
  - Verify that the token has not expired 
  - Check the lists of matched and unmatched policies
  - Check that the TEE debug flag is false


#### Signed policy verification

Intel Trust Authority allows tenant administrators to update attestation policies. A policy update changes the policy but the policy ID (UUID) is constant. An RP can’t be certain that the matched policy ID actually represents the policy the RP expects.
 
In many instances it will be acceptable for the RP to trust the policy IDs alone. If elevated trust is required, the RP should verify the matched_policy IDs by requesting a copy of the signed policy stored in the Intel Trust Authority database. An RP can verify that both the policy ID and hash have the expected values.

As of this writing, the only way to get a signed policy is by using the [GET **RetrievePolicy**](../Restapi/restapi-policy-management.md) REST API, which requires an admin API key. The security implication for RP developers and tenant administrators is that you must share an admin API key with the RP and the tenant. This places a high level of trust in the RP, especially if the RP is a third-party application not under the direct control of the tenant.

:::caution
A Intel Trust Authority admin API key is a highly sensitive secret that can be used to compromise an entire tenant configuration.
:::

#### Faithful Verification Verifier

A RP can use the Faithful Verification Verifier (FVV) utility to verify that the attestation token was created by a trusted Intel Trust Authority environment. FVV isn’t available as an API, which means that it must be executed as a CLI tool.  By using FVV, the RP can verify:

  - The attester evidence quote is valid.
  - Each Intel Trust Authority service quote is valid.
  - Each Intel Trust Authority service measurement matches values in the permit list

The FVV requires Intel® SGX DCAP for quote verification. This means that DCAP must be installed on the system where the FVV will run, and the system must also have access to the Intel® SGX PCCS for SGX collaterals.

For more information, see the [Faithful Verification Verifier](../Utilites/utility-faithful-verifier.md). 

[RFC9334, section 7.1](https://datatracker.ietf.org/doc/rfc9334/) contains a brief description of how an independent verifier can help to enhance security.

### Background check policy IDs

In the background check pattern, the RP is responsible for obtaining an attestation token from Intel Trust Authority, using a quote obtained from the attester. The client methods, CLI commands, and REST API all accept an optional list of policy IDs to apply during verification. If you don’t supply policy IDs with your token request, Intel Trust Authority will use the policies associated with the attestation API key used to authorize the request. 

Note that Intel Trust Authority does not use the API key policies if one or more policies is supplied with the request for a token. That is, the list of  policies supplied with a token request is not additive to the list of API policies associated with the attestation API key, if any. If the API key doesn’t have associated policies, Intel Trust Authority will evaluate the quote using the built-in default policy only. The matched_policies and unmatched_policies claims aren't included in a token that was evaluated using only the built-in default policy.

Intel Trust Authority always returns an attestation token unless an error occurs. An attester can fail every policy and the RP will still receive a a valid token from Intel Trust Authority if the built-in default policy is satisfied. The built-in policy evaluates the underlying TEE environment and quoting enclave and ensures that the provided quote is valid, but it won’t tell you if the attester is trustworthy. The only way to know which policies were matched or unmatched is to check the lists in the attestation token.  
 
Intel strongly recommends that you define your own [appraisal policies](../Concepts/concept-policies.md#appraisal-policies). Don’t rely on the built-in default policy alone.

### Token customization

Intel Trust Authority allows you to customize token claim names to suit the requirements of the RP. At this time you’re limited to renaming an existing claim or assigning a static value. For more information, see [Token customization policies](../Concepts/concept-policies.md#token-customization-policies-and-custom-claims).

### Relying party sample workflow

The following diagram depicts the high-level RP workflow for the background-check [attestation pattern](../Concepts/concept-patterns.md). The RP has much more work to do in background check mode than it does in passport mode. In the simplest passport case, the relying party doesn't need to make any direct connection to Intel Trust Authority or rely on the REST API. In all cases, the RP is responsible for performing at least the minimum [attestation token verification](#attestation-token-verification). 

![Relying party background check pseudo-UML diagram](/img/integrations/replying-party-background.png)

1. Get a nonce. This step is optional but it's recommended to prevent replay attacks. It also limits the attestation process to no more than 120 seconds, which is the valid lifespan of a nonce. The nonce is passed to the attester, which will include it in the TEE quote.
1. The relying party challenges the attester, passing a nonce with the challenge and requesting a TEE quote in return.The attester replies with a quote, including the nonce with the evidence. An attester can add custom user data to the **user_data** field in the evidence type.
1. The relying party receives the quote from the attester. Optionally, the attester can add (or append) custom user data to the evidence before forwarding it to Intel Trust Authority. The quote with nonce is sent to Intel Trust Authority for verification. An attestation token is returned unless an error occurs, meaning that the attester can fail every policy and the RP will still receive a valid token. For this reason it is nearly always necessary to check the matched and unmatched policies lists before deciding to trust the attester.
1. The relying party must verify the token before trusting it. The first step is to verify the nonce, if a nonce is used. 
1. The next step is to verify the attestation token header and signing certificate. If the relying party is using the Intel Trust Authority client library, the **VerifyToken** method can be used.
1. Optionally, the relying party can verify the policies used during verification. Currently, policies can only be retrieved using the REST API. The relying party retrieves the policies using the policy IDs (UUIDs) from the matched and unmatched policy lists, then compares the policy hash values to stored reference values. If the policy hashes match, the relying party can assume that the policies used to evaluate the evidence have not been modified since the reference values were collected.
1. Optionally, the relying party can use the FVV utility to verify the integrity of the Intel Trust Authority environment used during attestation. FVV requires Intel SGX DCAP on the system where FVV is run.

When all these checks have passed, the relying party can make a reliable decision regarding the trustworthiness of both the attester and the verifier.
