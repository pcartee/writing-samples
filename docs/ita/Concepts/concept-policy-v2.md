---
title: Attestation policies V2
description: A comprehensive guide to Trust Authority's attestation policies, including the new V2 policy syntax, composite attestation, policy evaluation, and Rego language usage.
author: pcartee
topic: conceptual
date: 06/21/2024
uid: attestation.policy.v2
---
import TokenExample from '../Include/policy/_composite-token.md';

*· June/21/2024 ·*

## Attestation Policies V2

Starting in June 2024, Trust Authority introduces a new version (V2) of attestation policy syntax designed to support composite attestation. The goal of composite attestation to create a single attestation of a trusted computing boundary, which can include a TEE, GPU, and other components. Evidence is collected for each of the components within the trusted compute boundary, combined, and evaluated against one or more composite attestation policies. The result is a single attestation token that includes claims for all components within the trusted compute boundary.  

:::note
Users are strongly encouraged to transition from their existing V1 policies to V2 at their earliest convenience. While Trust Authority will continue to support V1 policies for the time being, it’s important to note that V1 will eventually be phased out.
:::

## What's new in policy V2

Trust Authority policy V2 syntax is designed to support composite attestation. V2 policy expands V1 policy in the following ways:

- Composite attestation allows for attestation of multiple TEEs in a single token.
- Policy is not bound to a single attestation type; V2 policy supports composite attestation of any valid combination of TEEs.
- Attestation Type is removed from the policy syntax.
- Policy Type is removed from the policy syntax.
- Introduction of functional keywords in policy body.
- New keyword **Export** allows a policy author to rename claims and include them in the token without need for a separate token customization policy as in V1.
- New keyword **ExportOnMatch** requires the containing policy to match before export is triggered.
- New keyword **Match** declares which rules must be matched for a successful attestation.
- Future keywords are allowed with inclusion of `import rego.v1` at the top of the policy.
- Nested claims are accessible with dot or bracket syntax.
- Allows for rules to test relationships between attestation types.

## Attestation policy overview

Trust Authority uses _attestation policies_ to evaluate the claims made by an attester. An attestation policy is a set of Rego rules that define the conditions under which an attester is considered trustworthy. The policy is applied to the claims made by the attester to determine whether the attester is in compliance with the policy. If the attester is in compliance, the attester is considered trustworthy and the policy is considered _matched_.

Trust Authority evaluates a complete appraisal policy to true or false; the policy is _matched_ or _unmatched_, respectively. The result of a policy is given in the attestation token by the **policy_ids_matched** and/or **policy_ids_unmatched** claims. 

By default, Trust Authority returns an attestation token when no policies have been specified, and if one or more of the specified policies are unmatched. In other words, unless an error occurs, an attestation token is always issued. The relying party code must examine the **policy_ids_matched** and **policy_ids_unmatched** to determine the policy results for an attestation request. 

The default token issuance behavior can be changed by using the **PolicyMustMatch** option in the attestation request. **PolicyMustMatch** is an optional boolean `{**true** \| **false**}` value that defaults to **false** if not specified. If set to **true**, Trust Authority will issue an attestation token only if all specified policies are matched. If _any_ policy is unmatched, no attestation token is issued.

The following JSON fragment is the unmatched policy section of an attestation token:

```json
"policy_ids_unmatched":  [
    {
      "id": "8500e95a-58da-4b8a-a585-274730576d31",
      "version": "v1",
      "hash": "PApC1bnOL/3KvC4IieSU6m/Ho7pbKLxrif1Yo6lfotJhJ/O49ApEzOLrTL7RIg+7"
    },
   {
      "id": "5210b351-5865-4fb2-a731-17c6793cd4ca",
      "version": "v1",
      "hash": "PApC1bnOL/3KvC4IieSU6m/Ho7pbKLxrif1Yo6lfotJhJ/O49ApEzOLrTL7RIg+7"
    }
],
```

Where `"id"` is the policy ID (UUID) for the unmatched policy, and `"version"` is the policy definition revision number. When a policy is uploaded to Trust Authority, it is hashed and whenever the policy is used, the hash value is returned in the matched or unmatched sections. This gives the relying party a way to check to see that the policy wasn't modified after upload. The **policy_ids_unmatched** claim is included in the token only if there is at least one unmatched policy and the **PolicyMustMatch** option is not set to **true**.

The attestation policies that apply to a given attestation request can be specified in two ways:

- By associating one or more policies with the API key used to make the attestation request.
- By supplying a policy ID in the attestation request itself.
 
A tenant can have up to ten (10) attestation policies per subscription, and up to ten policies can be specified for an attestation request.

## Default policy

Trust Authority defines built-in default policies for each TEE type. The default policy is a minimal set of requirements and validation applied to the evidence provided by the attester. The default policy is designed to ensure that the attester is able to provide evidence that can be verified, but it doesn't evaluate the trustworthiness of the attester. The default policy is a starting point for creating custom policies that evaluate the trustworthiness of the attester. Default policies are not visible to users and are not configurable. If the built-in default policy fails, the attestation request returns an error and no attestation token is issued.

:::important
Never rely solely on the default policy to decide the result of an attestation. The default policy for the TEE does *not* evaluate the trustworthiness of an attester. Instead, you should create your own custom policy that meets your specific requirements.
:::

Trust Authority defines a built-in default policy for Software Guard Extensions (SGX) and Trust Domain Extensions (TDX) CPUs that verifies the attesting platform's underlying SGX quoting enclave (this is common to both SGX and TDX CPUs) to ensure that the chain of trust is unbroken and that all quoting components that gather evidence needed for remote attestation are up to date. This is *not* the same as appraising the attester's TCB status; for more information, see [Platform TCB Policy](../Concepts/concept-platform-tcb.md).

Other TEEs have different default policies. In general, TEE default policies only check to see if the quote provided by the attester is able to be verified. An appraisal policy is required to establish the trustworthiness of the attester.

## Composite attestation

_Composite attestation_ refers to attesting more than one TEE for a given attester. Composite attestation is useful when an attester uses a combination of TEEs to perform a single task. For example, an attester might use a TDX trust domain (TD) to perform secure computations and one or more NVIDIA\* GPUs to perform parallel processing. In this case, the attester would need to provide evidence from both the TD and the NVIDIA GPU(s) to prove that the attester is trustworthy.

Trust Authority policy V2 is not bound to a single attestation type; it supports composite attestation of any valid combination of TEEs. Composite attestation allows you to define a policy that evaluates the claims made by multiple TEEs in a single attestation token. The policy can include rules that apply to all TEEs, rules that apply to specific TEEs, and rules that apply to combinations of TEEs. Composite attestation allows you to create more complex attestation policies that take into account the interactions between different TEEs.

Composite attestation doesn't support more than one TEE from the following set of mutually-exclusive TEEs: TDX, SGX, or AMD SEV-SNP. For the time being, only one GPU can be attested in a composite attestation token.

The following composite attestation token shows an example of a token that includes claims from multiple TEEs. This token includes claims from a TDX trust domain and an NVIDIA H100 GPU. We'll use this as an example throughout the article to illustrate the concepts of composite attestation policy.

<TokenExample />

## Rego Policy Language

Trust Authority uses OPA as its policy engine, and the Rego language is used to write the attestation policies that are evaluated by [Open Policy Agent (OPA)][opa_org]. Rego (pronounced "_ray-go_") is a high-level declarative language that is purpose-built for expressing policy logic. For more information about Rego, see the [Rego Policy Language](https://www.openpolicyagent.org/docs/latest/policy-language/) documentation on the Open Policy Agent website.

This article will not attempt to repeat or summarize the excellent OPA Policy Language documentation. Instead, we will highlight the specific aspects of Rego that are relevant to Trust Authority attestation policy V2. For an introduction to Rego policy language, see [The Basics](https://www.openpolicyagent.org/docs/latest/policy-language/#the-basics) in the Rego Policy Language documentation on the Open Policy Agent website. 

To use Rego [future keywords][rego_future_keywords] and most policy language features, you must import the `rego.v1` package by adding `import rego.v1` to the top of your policy. The `if` keyword is required before a rule body definition. You can use most policy language features in Rego, _except_ that only a [subset of built-in functions](#built-in-functions) are supported. 

### Term definitions

In the context of attestation, a _claim_ is a statement made by an attester about its own state. For example, an attester might claim that it is running in debug mode, or that it is using a specific version of a software component. Claims are the basic building blocks of attestation policy. The policy author writes rules that evaluate the claims made by the attester to determine whether the attester is trustworthy.

Attester claims aren't the only claims in a JSON Web Token. Some claims aren't collected as part of the evidence collection process, but are included in the token because they contain useful information about the token itself and the verifier (Trust Authority service). Verifier claims include information about certificates, verifier microservice instance IDs (traceable back to microservice attestation), and other metadata that is useful for verifying the token. A full list of all the claims in an attestation token can be found in the [Attestation token](../Concepts/concept-attestation-tokens.md) article.
Insofar as Rego and OPA are concerned, a claim is nothing more than a key-value pair in a JSON document. Whenever you see "claim" in this article, think "property" or "object" in JSON, and vice-versa. Technically, a JSON document doesn't contain objects; it contains objects represented and stored as a string called an _object literal_. For simplicity, we'll refer to these as objects.

A [_rule_][rego_rules] contains one or more conditions that must be true for the rule to be satisfied. If the condition is true, the rule is considered _matched_. If the condition is false, the rule is considered _unmatched_. Every attestation policy must have at least one rule.  

_Nested claims_ is a domain-specific term for what is commonly known as nested objects and arrays in JSON. Nested claims allow a structured approach to attestation claims, with claims grouped by attestation type. A Trust Authority attestation token is a JSON Web Token (JWT) that contains claims about the attestation evidence, represented as objects and properties in a JSON document. The claims are organized into a hierarchy of attestation types, with each attestation type containing its own set of claims. Many claims are simple data types such as **bool**, **string**, and **int**, but others contain nested objects with their own properties.

Some claims have a particular format or structure that is important for policy evaluation. For example, string comparisons are case sensitive, and reference values must exactly match the claim value. 

To access nested properties (claims), objects, and values, you'll usually use [dot-access syntax](#dot-access-syntax). However, you can (and in some instances, _must_) also use [bracket notation](#bracket-notation) to access nested claims. The examples below show how to access nested claims using both dot and bracket syntax.

### Built-in functions

Trust Authority allows a subset of the full Rego language, with some restrictions on the use of certain built-in functions and operators. You can use any of the following built-in functions in your policy.

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

For more information about these functions, see [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-reference/#built-in-functions).

Some built-in functions are not supported because they could be used to access information that is not available to the policy engine or to perform operations that could compromise the security of the system.

### Comments

Comments in Rego are denoted by a hash symbol (`#`). However, Trust Authority policy V2 does not support comments at this time. Comments are not allowed in the policy body.

### Input

Trust Authority assembles TEE claim sets and other claims and then formats the entire collection as a JSON document stream. This JSON document becomes the base document for OPA during policy evaluation. The Rego built-in `input` variable allows you to access most of the contents of the base document. Certain claims are not accessible through the `input` variable in policy, although they do appear in the attestation token if they contain a value. 
To find out which claims are usable in policy for a given TEE, see the TEE-specific documentation in the [Attestation tokens](../Concepts/concept-attestation-tokens.md) article.

### Dot-access syntax

Dot-access syntax is the most common and most human-readable way to access claims in a JSON document. To access a claim using dot-access syntax, you simply chain together the object names and property names separated by periods ("dots"). For example, to access the `tdx_mrseam` claim in an attestation token, you would use the following syntax:

```
    input.tdx.tdx_mrseam == "123abc"
```

### Bracket notation

Bracket notation allows you to reference properties and objects (claims) that contain characters that aren't otherwise allowed in Rego identifiers. Some TEEs, such as NVIDIA\* H100 GPU, have claim names that include hyphens. Because hyphens aren't allowed in Rego identifiers, you must use bracket notation to access these claims. For example, to access the `x-nvidia-gpu-driver-version` claim in an attestation token, you would use the following syntax:

```
    input.nvgpu["x-nvidia-gpu-driver-version"] == "470.57.02"
```

Bracket notation is also useful when you need to access a claim using a variable. For example, if you have a variable `tee` that contains the name of the TEE you want to access, you can use bracket notation to access the claim for that TEE:

```
    input[tee].claim_name == "comparison value"
```

See also the policy_ids_matched example under [Dot-access syntax](#dot-access-syntax).

## Policy structure

The minimum policy must one or more conditions that must be met for the policy to be matched. 

The following example shows the bare minimum policy structure:

```rego
    input.tdx.tdx_mrseam == "123abc"
```

This policy contains a single rule that evaluates the `tdx_mrseam` claim. If the value of `tdx_mrseam` is equal to "123abc", the policy is considered matched. 

Optionally, you can include the following:

- A `match` rule. Match is optional, but if match isn't included, the policy will be evaluated the same as a V1 policy. In that case, all of the conditions in the policy must be true for the policy to match. One or more conditions that must be met for the `match` rule to be satisfied.
- An `export` block that exports claims to the attestation token.
- An `exportonmatch` block that exports claims to the attestation token only if the policy is matched.
- Additional rules that evaluate other claims or relationships between claims. These rules don't necessarily need to be included in the `match` rule.

If you want to use future keywords and related features, you must import the `rego.v1` package at the top of your policy.

The example policies below show how to include these optional elements in your policy.

## Policy keywords

Trust Authority policy V2 defines several new keywords that allow you to write more flexible attestation policies: `export`, `exportonmatch`, and `match`. 

### Export

The `export` keyword is a replacement for policy [V1 token customization](../Concepts/concept-policies.md#token-customization-policies-and-custom-claims). Export allows you to rename claims and include them in the attestation token without the need for a separate token customization policy. If you previously used one or more token customization policies, those policies can be eliminated and `export` can be used instead. You can export static values, nested claims, and claims from multiple TEEs. All exported claims are put into a `policy_defined_claims` object at the top level of the attestation token.  

```rego
export := {
    "tdx_mrsignerseam": input.tdx.tdx_mrsignerseam
    "tdx_mrseam": input.tdx.tdx_mrseam
}
```

```rego
export := {
    "mrseam": input.tdx.tdx_mrseam
    "other_data": {
        "debuggable": input.tdx.tdx_is_debuggable
        "mrtd": input.tdx.tdx_mrtd
    },
}
```

### ExportOnMatch

The `exportonmatch` keyword works like `export`, except it exports the claim only if the policy is matched.  `exportonmatch` is evaluated after all other rules. Exported claims are put into a `policy_defined_claims` object at the top level of the attestation token. 

```rego
import rego.v1

default match := false

match if {
    match_nvgpu
    input.tdx.tdx_mrseam == "123abc"
    input.tdx.tdx_mrtd == "456def"
}

match_nvgpu if {
    input.nvgpu.secboot == true
}

export := {
    "nvgpu_matched": match_nvgpu,
}

exportOnMatch := {
    "tdx_mrseam": input.tdx.tdx_mrseam,
    "tdx_mrtd": input.tdx.tdx_mrtd,
}
```

### Match

The `match` keyword and variable lets you determine which rules in a policy must be matched for the entire policy to be matched. Match isn't required in V2 policy. If `match` isn't present, the evaluation logic will consider all boolean rules to determine the matched state, just as in V1 policy.  `export` and `exportonmatch` will still work as expected if match isn't present.

The `match` rule can reference other rules in the policy, or it can contain the conditions directly. The `match` rule evaluates to true if all the conditions in the rule are true. If the `match` rule is true, the policy is considered matched. If the `match` rule is false, the policy is considered unmatched. Rules not referenced in the `match` rule are evaluated but do not affect the policy result.

```rego

default match := false

match {
    <one or more conditions>
}
```

The following example shows a policy with a `match` rule that both contains rules and references other rules in the policy (match_nvgpu). This policy imports the `rego.v1` package, so that `if` is required before defining a rule block. Though not shown here, `rego.v1` enables all Rego "future keywords," including `in` and `contains`. These keywords make the policy easier to read. 

This policy applies to a composite attestation token.

```rego

import rego.v1

default match := false

match if {
    match_nvgpu
    input.tdx.tdx_mrseam == "123abc"
    input.tdx.tdx_mrtd == "456def"
}

match_nvgpu if {
    input.nvgpu.secboot == true
}

export := {
    "nvgpu_matched": match_nvgpu,
    "tdx_mrseam": input.tdx.tdx_mrseam,
    "tdx_mrtd": input.tdx.tdx_mrtd,
}
```

## Example policies

This section contains a selection of sample policies for different attestation scenarios. The following examples are for illustrative purposes only. They may not be suitable for your specific use case. You should carefully consider your own requirements and create policies that meet your specific needs.

:::note
AMD SEV-SNP and TDX with vTPM attestation are in preview status in the pilot environment, and not yet available for general use. Features and functionality may change before general availability.
:::

### Singular policies

A singular policy is applied to an attestation request that contains claims for a single TEE. 

The following example shows a policy for an SGX TEE.

```rego
import rego.v1

default match := false

match if {
    input.sgx.sgx_mrenclave == "bab91f200038076ac25f87de0...609038f51ab"
    input.sgx.sgx_mrsigner == "d412a4f07ef83892a5915f...950fd4eb8694d7b"
    input.sgx.sgx_is_debuggable == false
    input.sgx.sgx_isvsvn == 1
    input.sgx.sgx_isvprodid == 0
}
```

The following example shows a policy for an NVIDIA GPU. Notice two things: first, the use of bracket notation to reference claims that contain disallowed characters, and second, the use of a count function to evaluate the number of mismatched measurement records.

```rego 
import rego.v1

default match := false

match if {
    input.nvgpu.secboot == true
    matched_measurements
    verified_rim
}

matched_measurements if {
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == false
    count(input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-mismatch-measurement-records"]) == 0
}

verified_rim if  {
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-signature-verified"] == true
}
```

The following example is a policy for a TDX trust domain. This policy includes an `ExportOnMatch` block that exports a new claim to the attestation token only if the policy is matched. 

```rego
    import rego.v1

    default match := false
    seamsvn := [2,3]
    tdx := input.tdx

    match if {
        "tdx.tdx_mrseam" == "123abc"
        "tdx.tdx_mrsignerseam" == "abc123"
        seamsvn[tdx.tdx_seamsvn]   
        "tdx.tdx_is_debuggable" == false
    }

    ExportOnMatch := {
        "app_api_key": "djE6NjY3YzU..."
        "renamed_mrtd": tdx.tdx_mrtd
    }
```

Notice that in the preceding sample, ExportOnMatch exports a new claim with a static value. This new claim is not based on an existing token claim. The fictitious `app_api_key` claim is included in the attestation token only if the policy is matched.  

:::important
Trust Authority is not a KMS/KBS or a secure storage service. The method demonstrated here allows for the inclusion of a static value in the attestation token if the policy is matched. However, it is important to use caution when deciding what information to include in a policy. Avoid including highly sensitive information in plaintext in the policy or token, as the policy text can be viewed by any tenant admin with access to the Trust Authority portal. If secrets are to be included in the policy, they should be encrypted before being included in the policy.
:::

### Composite policies

Example policy for a composite attestation token. In this example, the policy contains two rules: `matches_tdx` and `matches_nvgpu`. The `match` rule evaluates to true if both `matches_tdx` and `matches_nvgpu` are true. The `matches_tdx` rule evaluates the claims made by the TDX trust domain, and the `matches_nvgpu` rule evaluates the claims made by the NVIDIA GPU. If both rules are matched, the policy is considered matched. There can be other rules in the policy that evaluate other claims or relationships between claims. These rules don't necessarily need to be included in the match rule.

```rego

import rego.v1

default match := false

match if {
    matches_tdx
    matches_nvgpu
}

matches_tdx if {

    tdx := input.tdx
    tdx.tdx_mrseam == "123abc"
    tdx.tdx_mrsignerseam == "abc123"
    tdx.tdx_is_debuggable == false
}

matches_nvgpu if {

    nvgpu := input.nvgpu
    nvgpu.secboot == true
    nvgpu["x-nvidia-gpu-driver-version"] == "535.104.05"
    nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == true
}
```

The following example is a composite policy for AMD SEV-SNP and NVIDIA GPU. Note: AMD SEV-SNP attestation is in preview status in the pilot environment, and not yet available for general use.

```rego
import rego.v1

default match := false

match if {
    match_sevsnp
    match_nvgpu
}

match_sevsnp if {
    input.sevsnp.sevsnp_is_debuggable == false
    input.sevsnp.sevsnp_bootloader_svn == 2
    input.sevsnp.sevsnp_reportdata == "a7ddd44a965d012ba26788283c4123a68c0f9139e2...
    input.sevsnp.sevsnp_launchmeasurement == "dfa2b37b1d75eab67026b3bf207690df50b3530ec..."
}

match_nvgpu if  {
    input.nvgpu.secboot == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == false
    count(input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-mismatch-measurement-records"]) == 0
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-signature-verified"] == true
}

export := {
    "sevsnp_debuggable": input.sevsnp.sevsnp_is_debuggable,
    "sevsnp_matched": match_sevsnp,
    "nvgpu_matched": match_nvgpu
}
```

## vTPM appraisal policy example

:::note
This feature is in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Trust Authority Pilot environment. Contact your representative for access.
:::

The following example is a composite policy using and vTPM and TDX as implemented by Microsoft* Azure* confidential virtual machines (VMs). 

This policy verifies the integrity of the confidential VM paravisor using TDX, which anchors the chain of trust for the virtual TPM (which is part of the paravisor). The TPM component of this policy verifies the integrity of PCR 0, which measures the VM's virtual UEFI/BIOS.

Additional PCR assertions can be added to this policy based on the trust requirements of your application.

``` rego
import rego.v1

default match := false

match if {
    is_azure_tdx_cvm
    is_azure_tdx_platform
}

is_azure_tdx_cvm if {
    input.tdx.tdx_mrseam == "360304d34a16aace0a18e09ad2d07d2b9fd3c17..."
    input.tdx.tdx_mrtd == "0cc279c02d62414498ef4455822f2aea53351c8dc..."
}

is_azure_tdx_platform if {
    pcr := input.tpm.pcrs[_]
    pcr.alg == "SHA-256"
    pcr.index == 0
    pcr.digest == "f70272c29c9fd4b76eab8441a768..."
}
```

### Sample Azure confidential VM attestation request (vTPM + TDX)

:::note
vTPM attestation should always include attestation of the underlying TEE, such as TDX, in a composite attestation. Attestation of the TEE verifies that the vTPM can be trusted.
:::

```curl
curl --location --request POST 'https://api.trustauthority.company.com/appraisal/v2/attest/azure' \
--header 'Accept: application/json' \
--header 'X-API-KEY: <API KEY>' \
--header 'Content-Type: application/json' \
--data-raw '{ 
  "policy_ids": [<comma-separated list of policy IDs to be evaluated during attestation>],
  "tdx": {
  "runtime_data": "eyJrZXlz...",
  "quote": "BAACAI..."
 },
 "tpm": {
  "quote": "/1...",
  "signature": "ABQA...",
  "pcrs": "9wJ..."
 }
}'
```

## AMD* SEV-SNP appraisal policy example

:::note
This feature is in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Trust Authority Pilot environment. Contact your representative for access.
:::

The following policy evaluates the launch measurements of the Trusted Execution Environment (TEE) and validates those measurements against expected values. `matches_sevsnp_policy` is set to false by default. It is only set to true if the incoming measurement matches the expected measurements.  If the incoming measurements do not match the expected values, the policy fails, and the workload is rejected.

```json
default matches_sevsnp_policy = false
matches_sevsnp_policy = true {
input.sevsnpvm_launchmeasurement == "dfa2b37b1d75eab67026b3bf207690df50b3530ec77f60c488ef73b270247f2908f6de85d799d362cf00fec551c7a5be"
input.sevsnpvm_reportdata == "d957ac64ccc5b1da3e7498eb21dcbcc1ade2fec6654756bb20ce89b6b5eaff31e20c4f3f970b220d054167d8faaf4f6bab332d3de0f7db278db2ad1184f837e1"

input.sevsnpvm_is_debuggable == false
}
```

## Sample AMD SEV-SNP attestation request

The following example shows a sample AMD SEV-SNP attestation request. For more information about these claims, see the [Attestation tokens](../Concepts/concept-attestation-tokens.md) article.

```curl
curl --location 'https://api.trustauthority.company.com/appraisal/sevsnp/v1/attest' \
--header 'x-api-key: <API KEY>' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
"report":"AgAAAAAAAAAAAAMA ...",
    "policy_ids": [<comma-separated list of policy IDs to be evaluated during attestation>]
}'
```

Policies specified in an attestation request will override any policies associated with the attestation API key. If policies are specified in an attestation request, only the policies included in the request will be appraised, and any policies associated with the API key will be ignored for this request.

/* External links */
[opa_input_doc]: https://www.openpolicyagent.org/docs/latest/envoy-primer/#input-document
[opa_docs]: https://www.openpolicyagent.org/docs/latest/
[opa_org]: https://www.openpolicyagent.org/
[rego_future_keywords]: https://www.openpolicyagent.org/docs/latest/policy-language/#future-keywords
[rego_rules]: https://www.openpolicyagent.org/docs/latest/policy-language/#rules
[rego_v1]: https://www.openpolicyagent.org/docs/latest/policy-language/#rego-v1
