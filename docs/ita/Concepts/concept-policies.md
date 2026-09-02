---
title: Attestation policies
description: An overview of attestation policies in Intel® Trust Authority.
author: pcartee
topic: conceptual
date: 06/21/2024
uid: attestation.policies
---

*· 06/21/2024 ·*

## Attestation policies

:::important
This article describes the initial version (V1) of attestation policies supported by Intel Trust Authority. A new version (V2) of policies is now in pre-release preview in the Intel Trust Authority Pilot environment. Users are strongly encouraged to plan ahead to transition from their existing V1 policies to V2 once it's generally available. While Intel Trust Authority will continue to support V1 policies after the release of V2, it’s important to note that V1 will eventually be phased out. For more information about transitioning to V2 policy, see [Attestation policy V2](../Concepts/concept-policy-v2.md).
:::

Intel® Trust Authority uses _attestation policies_ to evaluate the claims made by an attester. Intel Trust Authority uses two kinds of policies: [_appraisal policies_](#appraisal-policies) that are used to evaluate claims and [_token modification policies_](#token-customization-policies-and-custom-claims) that are used to insert custom claims into the outgoing attestation token. 

A Tenant can have up to 10 policies (not including the default policy) associated with Trust Authority. Also, no more than 10 policies can be specified when making an attestation request.

Policies use the [Open Policy Agent (OPA)](https://www.openpolicyagent.org/docs/latest/policy-language/#what-is-rego) Rego language for rule definitions. For more information about writing Rego policies for Intel Trust Authority, see [How to author a custom policy](../How-to%20workflows/howto-author-custom-policy.md).

## Default policy

Intel Trust Authority defines a built-in default policy that verifies the attesting platform's underlying Intel® Software Guard Extensions (Intel® SGX) quoting enclave to ensure that the chain of trust is unbroken and that all quoting components (that is, the fundamental software and firmware that gather evidence needed for remote attestation) are up to date. This is not the same as appraising the attester's TCB status; for more information, see [Platform TCB Policy](../Concepts/concept-platform-tcb.md). The built-in default policy is an integral part of the attestation process, and it isn't visible to the user. If the built-in default policy fails, the attestation request returns an error and no attestation token is issued. You should never rely solely on the default policy to decide the result of an attestation.

## Policy results

Intel Trust Authority evaluates a complete appraisal policy to true or false; the policy is _matched_ or _unmatched_, respectively. Unlike Rego policies, appraisal policies can't return a value. The result of a policy is given in the attestation token by the **policy_ids_matched** and/or **policy_ids_unmatched** claims.

By default, Intel Trust Authority returns an attestation token when no policies have been specified, and if one or more of the specified policies are unmatched. In other words, unless an error occurs, an attestation token is always issued. The relying party code must examine the **policy_ids_matched** and **policy_ids_unmatched** to determine the policy results for an attestation request.

The default token issuance behavior can be changed by using the **PolicyMustMatch** option in the attestation request. **PolicyMustMatch** is an optional boolean `{**true** \| **false**}` value that defaults to **false** if not specified. If set to **true**, Intel Trust Authority will issue an attestation token only if all specified policies are matched. If _any_ policy is unmatched, no attestation token is issued.

The following JSON fragment is the unmatched policy section of an attestation token:

```json
 "policy_ids_unmatched": [
    {
      "id": "c7c49dd2-a96a-43bd-8cee-f2aa99503458",
      "version": "v4"
    }
  ]
```

Where `"id"` is the policy ID (UUID) for the unmatched policy, and `"version"` is the policy definition revision number. The **policy_ids_unmatched** claim is included in the token only if there is at least one unmatched policy and the **PolicyMustMatch** option is not set to **true**.

## Policy language functions

Intel Trust Authority implements a subset of the Rego policy language built-in functions. You can use any of the following built-in functions in your policy.

- time.now_ns()
- time.parse_rfc3339_ns(_value_)
- time.add_date(_ns, years, months, days_)
- object.subset(_super, sub_)
- count(_collection_)
- `&`   (And)
- `==`  (comparison; is equal)
- `=`   (unification; make equal)
- `>`
- `>=`
- `<`
- `<=`
- `:=`

For more information about these functions, see [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-reference/#built-in-functions). For an introduction to the Rego policy language, see [The Basics](https://www.openpolicyagent.org/docs/latest/policy-language/#the-basics).

## Claims

A claim is a name:value pair in a quote or attestation token. Claims include specific elements related to the attested Trusted Execution Environment (TEE). These elements are associated with the TEE’s combined hardware and software environment, also known as the Trusted-Compute Base (TCB). The trusted claims provider — that is, the software components that collect evidence from the TEE and package evidence as a quote — provides most of the incoming claims.

Intel Trust authority adds outgoing claims, including the token header, matched and unmatched policies, faithful verification, and other claims as described below. Every TEE is different, and the claims in a token will vary depending on both the TEE and attesting workload. See [Attestation tokens and claims](../Concepts/concept-attestation-tokens.md) for a complete listing of the claims defined by Intel Trust Authority.

Not all claims are available for use in policy. You can't reference any outgoing claims, and only a subset of incoming claims are available for use in policy. For more information, see [Claims usable in policy](../Concepts/concept-attestation-tokens.md#claims-usable-in-policy).

Certain claims are defined to allow attesting workloads to add data to the attestation token. For example, an attester can pass a public key to be used for securely returning data from a relying party. For more information, see **attester_held_data** in [Verifier claims](../Concepts/concept-attestation-tokens.md#verifier-claims).

Intel Trust Authority also supports [token customization policies](#token-customization-policies-and-custom-claims), which allow you to map built-in claim names to user-defined claim names.

## Appraisal Policies

An appraisal policy is a set of one or more rules applied to a quote to evaluate the claims it contains. Appraisal policies compare claim measurements in the quote from the attesting TEE to reference values in the policy.  

### Intel® SGX appraisal policy example:

This example is a bare-minimum appraisal policy for an Intel® Software Guard Extensions (Intel® SGX) enclave.

```json
default matches_sgx_policy = false
matches_sgx_policy = true {
  input.sgx_mrenclave == "1234e819861adef61232a4865efea9337b91ed301233491b17f123d9e8212311"
  input.sgx_mrsigner == "123719e77d123a1470f612362a4d774303c899db69123f9c70ee123c08123123"
  input.sgx_is_debuggable == false
}
```

The above example does the following:

1. Initializes the default result for the policy to false.
1. Sets the policy result to true if the following collection of rules all evaluate to true. The collection of rules is evaluated as a logical AND. All rules must be true for the entire statement to be true.  In the example, the collection of rules includes an expected value for the **mrenclave** value (a measurement of the enclave code verifying its integrity) and an expected value for the **mrsigner** (a hash of the key used to sign the enclave, an indication of the legitimate author/owner of the enclave code), as well as a check to ensure the enclave is not set to the insecure debug mode.

:::caution
A TEE in debug mode is not secure. When a TEE is debuggable, the processor and memory are accessible to applications outside the trust boundary of the enclave or TD.
:::

## Intel TDX appraisal policy example

```json
default matches_tdx_policy = false
matches_tdx_policy = true {
  input.tdx_mrsignerseam == "00000000000..."
  input.tdx_seamsvn == "2"
  input.attester_tcb_status == "OK"
  input.tdx_is_debuggable == false
}
```

The above example shows a minimal TDX attestation policy for a cloud-hosted TD. **tdx_seamsvn** is optional but should be checked if it's known. This policy assumes that we don't have all the measurements needed for a more complete attestation. If available, the following claims should also be checked: **tdx_mrtd**, **tdx_mrseam**, **tdx_rtmr0**, and **tdx_rmtr1**. For more information about these claims, see the [Attestation tokens](../Concepts/concept-attestation-tokens.md) article.

## Token customization policies and custom claims

Token customization policies allow the creation of a new claim name that can be mapped to a default claim. The new claim automatically adopts the value of the default claim, streamlining integration with relying parties seeking a specific claim name.

For example, a user wants to enable a key management system to read claims from an Intel Trust Authority token, and the key management system looks for a specific claim name **myappname_mrenclave** for the **mrenclave** value. Intel Trust Authority will default issue a token using the claim **sgx_mrenclave**. A token customization policy can map the value of the default claim **sgx_mrenclave** to a new claim name **myappname_mrenclave**, that the key management system expects. This allows the token to be modified instead of the relying party that wants to integrate with Intel Trust Authority.

The customized claims are output in the **custom_policy** object in the attestation token. This section only appears if there is a token customization policy applied during attestation.

Token customization policies can't modify outgoing attestation claims made by Intel Trust Authority. Token customization policies are evaluated before Intel Trust Authority outgoing claims, such as the token header claims, and matched and unmatched policies are added to the token. This is to prevent the token customization policy from modifying an attested value.

### Token customization policy for Intel SGX

Any number of incoming claim elements can be added.

```json

get_token_fields[token_fields] {
    token_fields := {
        "my_claim_isvsvn": input.sgx_isvsvn,
        "my_claim_mrenclave": input.sgx_mrenclave,
        "my_claim_mrsigner": input.sgx_mrsigner,
        "my_claim_isvprodid": input.sgx_isvprodid,
        "my_claim_isSgxDebuggable": input.sgx_is_debuggable
   }
}

```

In the preceding sample example, the **token_fields** is an output variable that will contain a set of one or more customized claims after the policy is applied, and `input` refers to the attestation token document.

The Intel SGX claims provide the input values for token customization. For more information on Intel SGX claims, see [Intel SGX claims](../How-to%20workflows/howto-author-custom-policy.md).

## Using policies with associated API keys

Appraisal and token customization policies can be associated with one or more [API keys](../Quickstart/tutorial-api-key.md). This allows an Intel Trust Authority user to define the attestation behavior for their applications. Policies can be managed on the API key object as needed, and no changes are required on the application itself.

## Attesting using specified policies

Appraisal and token customization policies can also be specified during an attestation request as part of the [Attestation API](../Restapi/restapi-attestation.md)).

### Sample /appraisal/v1/attest request with specified policies

```json
{
    "quote": "AwACA...Qo=",
    "verifier_nonce": {
        "val": "N0...PQ==",
        "iat": "12...RD",
        "signature": "vW...Am"
    },
    "policy_ids": ["11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222"],
    "runtime_data": "AQ...lA=="
}'

```

Policies specified in an attestation request will override any policies associated with the attestation API key.  If policies are specified in an attestation request, only the policies included in the request will be appraised, and any policies associated with the API key will be ignored for this request.

## Next steps

- Review [The Basics](https://www.openpolicyagent.org/docs/latest/policy-language/#the-basics) in the Rego Policy Language reference. You don't need to study Rego in detail, but you do need to understand the basic format of a Rego policy.
- Read [Attestation tokens](../Concepts/concept-attestation-tokens.md) to understand the format of an attestation token and the claims that apply to your TEE.
- Read [How to author a custom policy](../How-to%20workflows/howto-author-custom-policy.md) in the Intel Trust Authority documentation.
- Read [Policy Signing Tool](../Utilites/utility-policy-signing.md) for a description of how to sign policies. Signing policies is optional, but it's recommended as a step to help ensure that the policy uploaded to Intel Trust Authority is the same policy that is used in the attestation. For more information, see [Signed policy verification](../Integration/integrate-relying-party.md#signed-policy-verification)
