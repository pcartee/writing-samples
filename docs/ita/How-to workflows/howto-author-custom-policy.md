---
title: Author a custom policy
description: Instructions for creating custom policies.
author: pcartee
topic: how to
date: 07/17/2024
uid: author.custom.policy  # Do not change uid!
# Added pre-deprecation warning & article date - 06/12/2024 grminch cassini-17914
---

*· November/16/2023 ·*

## Author a custom policy

:::important
This article describes the initial version (V1) of the attestation policy supported by Intel Trust Authority. A new version (V2) of the policy is now available. Users are strongly encouraged to transition from their existing V1 policies to V2 at their earliest convenience. While Intel Trust Authority will continue to support V1 policies for the time being, it’s important to note that V1 will eventually be phased out. For more information about transitioning to V2 policy, see [Attestation policy V2](../Concepts/concept-policy-v2.md).
:::

This article describes how to create policies for Intel® Trust Authority. Intel Trust Authority uses [Open Policy Agent (OPA)](https://www.openpolicyagent.org/docs/latest/) to decouple policy evaluation logic from policy enforcement. Policies are written in [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-language/).

Intel Trust Authority always issues a token, even on policy failure. The one exception is the built-in default policy, which evaluates the integrity of the Intel® Software Guard Extensions (Intel® SGX) quoting enclave and TCB. If the built-in policy fails, an error occurs, and no token is issued.

Policies are evaluated and categorized into matched and unmatched policies in the issued token.

## Allowed built-in functions

You can use any of the following built-in functions in your policy:
- time.now_ns()
- time.parse_rfc3339_ns(_value_)
- time.add_date(_ns, years, months, days_)
- object.subset(_super, sub_)
- count(_collection_)
- `&`   (And)
- `==`  (Comparison; is equal)
- `=`   (Unification; make equal)
- `>`
- `>=`
- `<`
- `<=`
- `:=`

For more information, see [Policy language functions](../Concepts/concept-policies.md#policy-language-functions).

## Minimum required contents for a policy

- An output variable:
   - Appraisal policies have a logical true/false output and use the equality operator  `=` to set the matches_policy output. Appraisal policies perform comparison functions.
   -	Token customization policies output a set of name:value claims and use an assignment operator `:=` to set the token_fields output variable. Token customization policies define custom claims and set the claims values.
- Every policy must have at least one rule that evaluates to the correct output type.
- As a best practice, the output variable for any appraisal policy should be initialized to false. 

## Attestation policies

Attestation policies define the requirements that the appraiser (Intel Trust Authority) compares against the evidence provided by an attester. When user-defined attestation policies are specified in the request for a token, the resulting attestation token will contain arrays of matched and unmatched policy IDs, indicating which policies had their requirements satisfied by the provided evidence.

### Obtaining policy values

Attestation policies require definition of expected claims values. For example, a policy might require that the claim "**sgx.mrenclave**" matches the specific value "83f4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204410". The method to initially obtain the expected value so that it can be set in a policy depends on the claims being evaluated and the technology being attested. 

The easiest method is to request an attestation for a known-good example of the application to be protected using the Intel Trust Authority client. You can then examine the claims in the resulting attestation token to see all of the supported claims values, and use the specific claims values to author a policy that meets your application's trust requirements. For most attestation technologies, this can be accomplished using the [Attestation Client CLI](../Integration/integrate-go-tdx-cli.md) by using the `token` command. For example, to request an attestation of a VM protected by Intel TDX, use the command `trustauthority-cli token --config config.json`. 

Alternatively, some technologies produce claims values as build outputs, or are defined by the software owner. For example, with Intel SGX, the **sgx.mrenclave** value is a hash of the SGX enclave (a code library) and can be output as part of the build process. The **sgx_isvsvn** is an integer value defined by the software developer indicating the security version level of the enclave.

Some claims values are defined or known only to the infrastructure owner. These may be published by some service providers. 

See the vendor-provided documentation for the supported attestation technology needed to determine best practices for obtaining attestation policy values.

## Default policies

Intel Trust Authority supplies a default policy that is always applied even when other policies are associated with the API key or specified in an array included in the request token. The default policy validates the Trusted Compute Base (TCB) of the enclave against the latest firmware and authenticated code modules, providing assurance that the quoting enclave is genuine and up to date. When a customer-defined policy is assigned to an API key or specified in an array included with the request token, lists of matched and unmatched policy ids are included in the attestation token. An outgoing Intel Trust Authority attestation token only contains a list of matched and unmatched policy ids if a customer-defined attestation policy is specified in the request for a token or associated with the API key. These lists are not included when the only policy being evaluated is the default policy. The Intel Trust Authority team recommends defining one or more appraisal policies to validate specific claims in the quote.

## Sample Intel SGX attestation policy

This sample policy sets `false` as a default pre-evaluation value and only resets the condition value to `true` if all the rules match.

```
default matches_sgx_policy = false
matches_sgx_policy = true {
   input.sgx_mrenclave == "83f4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204410"
   input.sgx_mrsigner == "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e"
   input.sgx_isvprodid == 3
   input.sgx_isvsvn == 2
   input.sgx_is_debuggable == false
}
```

## Create an Intel SGX policy

An Intel SGX attestation policy is used as an example. However, the authoring process is the same for all policies supported by Intel Trust Authority.

Before beginning these instructions, have access to the hash for the **mrenclave** measurement and the hash for the signing key.

1. Create a new file.

1. Add the default pre-evaluation value.

   ```
   default matches_sgx_policy = false
   ```

1. Add the conditions (rules) to be met to change the value to **true**.

   ```
   default matches_sgx_policy = false
   matches_sgx_policy = true {
      input.sgx_mrenclave == "83f4e819861adef6ffb2a4865efea9337b91ed30fa33491b17f0d5d9e8204410"
      input.sgx_mrsigner == "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e"
      input.sgx_isvprodid == 3
      input.sgx_isvsvn == 2
      input.sgx_is_debuggable == false
   }
   ```

1. Save the file.

## Sample Azure* confidential VM policy with Intel® TDX and vTPM attestation 

:::note
This feature is in pre-release status. For preview access, please contact your Intel sales representative. Details of implementation and usage may change before general availability.
:::

This sample policy verifies the Azure* confidential VM with Intel TDX is verified and authenticated Azure* VM with Intel TDX Azure* hypervisor and VM image. The match keyword and variable lets you determine which rules in a policy must be matched for the entire policy to be matched. This sample shows a policy with a match rule that contains references other rules in the policy. The Intel TDX **mrseam** and **mrtd** measurements check the integrity and authenticity of the trust domain and image. The PCR 0 measurement verifies the integrity of the virtual UEFI firmware.

 This policy imports the rego.v1 package and if is required before defining a rule block. For future keywords and related features, rego.v1 is used. 

### Integrity verification of an Azure* confidiential VM (vTPM and Intel® TDX)

:::note
TPM PCR measurements are extended by many different elements of a system. With vTPM, the policy verifies the integrity and authenticity of the hypervisor and image. When an Azure* confidential VM runs updates, PCR values change at boot time (with the exception runtime PCR extensions such as IMA). The changed PCRs are updated on boot.
:::

This sample policy sets `false` as a default pre-evaluation value and only resets the condition value to `true` if all the rules match.

```
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

## Create Azure* confidential VM with Intel TDX and vTPM policy

An Intel TDX with vTPM attestation policy is used as an example. However, the authoring process is the same for all policies supported by Intel Trust Authority.

Before beginning these instructions, have access to the hash for the **mrseam** and **mrtd** measurements and the hash for PCR digest.

1. Create a new file.

1. Import rego.v1 at the top of your policy.

   ```
   import rego.v1
   ```

1. Add the default pre-evaluation value for verification of an Azure* confidential virtual machine with Intel TDX.

   ```
   default match := false   
   ```

1. Add the conditions (rules) to be met to change the value to **true**.

   ```
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

1. Save the file.

## Next Steps

- Optionally, sign the policy using the [Policy Signing Tool](../Utilites/utility-policy-signing.md) to ensure policy integrity.
- Upload the new policy using the web portal, REST API, or command line tool.
- Learn more about [policies](../Concepts/concept-policies.md).
