---
title: Policy builder tool
description: An overview of the policy builder tool and how to use it to create simplified policies.
author: pcartee
topic: conceptual
date: 07/18/2024
uid: policy.builder.tool
---
*· July/18/2024 ·*

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Policy builder tool

The Policy Builder tool is a command line interface tool used to author simplified policies written in JSON format and convert them to Rego policies readable by Intel® Trust Authority. The Policy Builder currently supports Intel® Software Guard Extensions (Intel® SGX) and Intel® Trust Domain Extensions (Intel® TDX) TEEs.

To use the Policy Builder, you must first create a JSON file as shown in the examples below. This JSON file is a list of claims and allowable values. The claim:value pairs are converted to equality tests (`==`) in Rego. Certain "claims" are not really EAT ([Entity Attestation Token](https://datatracker.ietf.org/doc/draft-ietf-rats-eat/11/)) claims at all; they are keywords that Policy Builder expands to Rego code blocks. For example, **min_tcb_date** and **ttl_period** are not TEE claims, they are Policy Builder keywords. This is discussed in more detail below.

It's important to understand that JSON and Rego are completely different things, despite having superficial similarity in the examples that follow. JSON is an object notation language. Rego is a full-featured programming language that is optimized for querying documents and evaluating rules applied to the document content.  Intel Trust Authority currently exposes a subset of the full Rego feature set, though more functions may be exposed in the future.  Policies written in Rego have more options for built-in functions and syntax than the simplified JSON policy representation allows. For more information about Rego, see the [OPA Policy Language Reference](https://www.openpolicyagent.org/docs/latest/policy-language/) "The Basics". 

The purpose of the Policy Builder is to simplify the creation of basic/common policies so that policy authors do not need to learn Rego.

:::note
 JSON policies are simplified and have reduced capability from Rego policies. This utility exists to help users who do not want/need the complexity and power available through Rego but who still want to use a simple policy for attestation. The "default" policies only check whether the TEE is genuine and has an up-to-date TCB, but do not check any workload specific attributes of the TEE. Policies are needed to check those attributes, or to customize the attribute names, or to customize the acceptable TCB based on the capabilities and update schedule of the TEE provider. The Policy Builder can help create simplified policies for the most commonly used attributes.

When you run the Policy Builder with a JSON input file, it will generate Rego output that you can copy to the Intel Trust Authority Portal to create a policy, or you can use the [Policy Management REST API](../Restapi/restapi-policy-management.md) or the [Intel Trust Authority CLI (`trustauthorityctl`)](../Command-line/cli-policy-commands.md).

Creating policies is discussed in Attestation Policies and How To Author A Custom Policy.
:::

If you need to create appraisal policies that involve comparisons, AND logic, and other Rego features, the policies must be created in native Rego format. 

## Available commands

- `help` -  Provides help about any Policy Builder command
- `jsontorego` - jsontorego -i [input file] converts the JSON file to Rego
- `version` - Prints the policy builder version currently installed

Examples:

`./policy-builder-linux help`
`policy-builder-windows.exe version`

**Syntax**

The following syntax is used to convert a JSON policy to a Rego policy.

Linux
`./policy-builder-linux jsontorego -i <input file>`

Windows
`policy-builder-windows.exe jsontorego -i <input file>`

**Output**

The output is displayed in the terminal in Rego with two format options. 

The **original** format is used with the [Manage Policies](../How-to%20workflows/howto-manage-attestation-policies.md) page of the web portal. 

The **escaped** format is used with the [Policy Management REST API](../Restapi/restapi-policy-management.md) or with the [Intel Trust Authority CLI (`trustauthorityctl`)](../Command-line/cli-policy-commands.md). 

## Appraisal policy

### Intel SGX incoming claims

The following claims can be used in the JSON policy input file. For a complete description of the claims, see [Attestation Tokens](../Concepts/concept-attestation-tokens.md#tee-specific-claims). 

|Claim                  | Datatype                | 
|-----------------------|--------------------------|
|**sgx_mrsigner**           |String or list of strings. |
|**sgx_mrenclave**          |String or list of strings. |
|**sgx_isvprodid**          |Number                    |
|**sgx_isvsvn**             |Number                    |
|**sgx_isvsvn_min**         |Number                    |
|**sgx_is_debuggable**      |Boolean                   |

:::note
`sgx_isvsvn_min` is a keyword and this specifies the minimum acceptable `sgx_isvsvn` value. Both `sgx_isvsvn_min` and `sgx_isvsvn` cannot be specified in the same policy, as they will conflict. `sgx_isvsvn` defines a specific value (an `==` operation), where `sgx_isvsvn_min` specifies a minimum value (actual value `>=` `sgx_isvsvn_min` ).
:::

#### JSON Intel SGX appraisal policy

<Tabs>
    <TabItem value ="sgx-json" label="SGX JSON" default>

### SGX JSON

The following example shows an Intel SGX policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion. Each JSON claim corresponds to a claim in the Rego appraisal policy and in the attestation token.

```JSON
{
    "policy": {  
        "sgx_appraisal": {
            "sgx_isvprodid": 1,
            "sgx_isvsvn_min": 2,
            "sgx_mrenclave": "d777e819861adef6ffb2a4865efea9338b91ed30fa33491b17f0d5d9e8204410",
            "sgx_mrsigner": "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e",
            "sgx_is_debuggable": false
        }
    }
}   
```

    </TabItem>

    <TabItem value="sgx-rego" label="SGX Rego">

### SGX Rego

The following example shows the JSON input file, above, after conversion to an Intel SGX appraisal policy. This is what you'll use to create your policy in Intel Trust Authority. 

The five `sgx_` claims in JSON are converted to equality tests. Notice how the `sgx_isvsvn_min` claim is translated to a `>=` operation instead of `==` in Rego.

```rego
default matches_sgx_policy = false
matches_sgx_policy = true {
input.sgx_isvsvn >= 2
input.sgx_isvprodid == 1
input.sgx_mrenclave == "d777e819861adef6ffb2a4865efea9338b91ed30fa33491b17f0d5d9e8204410"
input.sgx_mrsigner == "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e"
input.sgx_is_debuggable == false
}
```
    </TabItem>
</Tabs>

### Intel TDX incoming claims

The following claims can be used in the JSON policy input file. For a complete description of the claims, see [Attestation Tokens](../Concepts/concept-attestation-tokens.md#tee-specific-claims). 

|Claim                  | Datatype                 |
|-----------------------|----------------------------|
|**tdx_seamsvn**            |Number                      |
|**tdx_rtmr0**              |String or list of strings.  |
|**tdx_rtmr1**              |String or list of strings.  |
|**tdx_rtmr2**              |String or list of strings.  |
|**tdx_rtmr3**              |String or list of strings.  |
|**tdx_mrtd**               |String or list of strings. |
|**tdx_mrsignerseam**       |String or list of strings.  |
|**tdx_tee_is_debuggable**      |Boolean                     |

#### JSON Intel TDX attestation policy

<Tabs>
    <TabItem value="tdx-json" label="TDX JSON" default>

### TDX JSON

The following example shows an Intel TDX policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion. The first object literal in the policy is `"tdx_appraisal":{}`. That tells Policy Builder that this is an Intel TDX appraisal policy. Notice that the **tdx_rmtr3** claim accepts a "list of strings" value, and in this example includes two values. By providing two values as a list of strings in the policy, you are saying "This claim evaluates to true if input.tdx_rmtr3 value is IN [a, b, ...]."

```JSON
{
    "policy": {
        "tdx_appraisal": {
            "tdx_seamsvn": 1,
            "tdx_rtmr0": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
            "tdx_rtmr1": "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c",
            "tdx_rtmr2": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
            "tdx_rtmr3": ["ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"],
            "tdx_mrtd": "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54",
            "tdx_mrsignerseam": "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c",   
            "tdx_is_debuggable": true
        }
    }
}  

 </TabItem>
 <TabItem value="tdx-rego" label="TDX Rego">

### TDX Rego

The following example shows output after conversion to a Rego Intel TDX appraisal policy. This is what you'll use to create your policy in Intel Trust Authority. 

The `tdx_` claims in JSON are converted to equality tests. Notice how the `tdx_rmtr3` values in the JSON input file were changed to a Rego set. First, the JSON notation is converted to Rego set notation `{...}` and assigned to a variable. The statement `acceptable_values_for_tdx_rtmr3[input.tdx_rtmr3]` evaluates to **true** if **input.tdx_rmtr3** (from the attestation token — `input` is the attestation token document) is IN the set assigned to `acceptable_values_for_tdx_rmtr3`.

```rego
default matches_tdx_policy = false
matches_tdx_policy = true {
input.tdx_seamsvn == 1
input.tdx_rtmr0 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
input.tdx_rtmr1 == "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c"
input.tdx_rtmr2 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
acceptable_values_for_tdx_rtmr3 := {"ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"}
acceptable_values_for_tdx_rtmr3[input.tdx_rtmr3]
input.tdx_mrtd == "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54"
input.tdx_mrsignerseam == "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c"
input.tdx_is_debuggable == true
}
```

</TabItem>
</Tabs>
---

## Custom TCB policy incoming claims

Custom TCB policies are used to adjust the default policy evaluation of the attester TEE's TCB update status. This is needed to account for the TEE provider's update schedule. TCB updates can be complex for datacenter and cloud providers and may take more time than allotted in the default policy.

The following attester TCB pseudo-claims can be used in the JSON policy input file. These are not claims in the usual sense because they're not in the Intel Trust Authority EAT profile and they don't appear in an attestation token. These are keywords that expand to Rego code blocks to implement custom attester TCB policies. For more information, see [Platform TCB Policies](../Concepts/concept-platform-tcb.md). 

|Field Name            |Type       |Field Description             |
|---------------------|---------------------|-----------------------------------|
|**min_tcb_date**     |Date(with time zoom)     |Minimum tcb date indicates the oldest TCB level that RP can tolerate.     |
|**tcb_status_allowed** |List of Strings     |Acceptable platform TCB status.     |
|**ttl_period**   |Number     |Time-To-Live (TTL). Policy provides a platform grace period which is a measurement in months. The Policy fails if the current date time > platform tcbDate + ttl_period     |
|**allowed_advisory_ids**	|List of Strings	|The policy fails if the platform TCB advisory_ids(attester_advisory_ids) array (if any) includes any advisory ID NOT in the allowed list.	|

### JSON custom TCB policy

<Tabs>
<TabItem value="tcb-json" label="TCB JSON">

### TCB JSON

The following example shows a custom TCB policy in JSON format, before conversion to Rego. The first object literal in the policy is ``. That tells Policy Builder that this is a TCB customization policy. This is the input file that is specified for conversion.

Note that the custom TCB policy needs to be embedded in an appraisal policy for a specific TEE. The example below uses a `sgx_appraisal` policy type, but the exact same policy would word for a `tdx_appraisal` policy type.

```JSON
{
    "policy": {  
            "sgx_appraisal": {
                "min_tcb_date" : "2023-03-15T00:00:00Z",
                "tcb_status_allowed": ["UpToDate", "SWHardeningNeeded"],
                "ttl_period" : 8,
                "allowed_advisory_ids" : ["INTEL-SA-00586", "INTEL-SA-00614", "INTEL-SA-00615"]
            }
    }
} 
```

</TabItem>
<TabItem value="tcb-rego" label="TCB Rego">

### TCB Rego

The following example shows the output after conversion to a custom TCB policy. This is what you'll use to create your policy in Intel Trust Authority. 

```rego
default matches_sgx_policy = false
matches_sgx_policy = true {
min_tcb_date := "2023-03-15T00:00:00Z"
date_ns_0 := time.parse_rfc3339_ns(input.attester_tcb_date)
min_date_ns := time.parse_rfc3339_ns(min_tcb_date)
date_ns_0 >= min_date_ns
acceptable_values_for_attester_tcb_status := {"UpToDate", "SWHardeningNeeded"}
acceptable_values_for_attester_tcb_status[input.attester_tcb_status]
ttl_period := 8
date_ns_1 := time.parse_rfc3339_ns(input.attester_tcb_date)
expiry_date_ns := time.add_date(date_ns_1, 0, ttl_period, 0)
expiry_date_ns >= time.now_ns()
allowed_advisory_ids := {"INTEL-SA-00586", "INTEL-SA-00614", "INTEL-SA-00615"}
attester_advisory_ids:= {id | id := input.attester_advisory_ids[_]}
object.subset(allowed_advisory_ids,  attester_advisory_ids)
}
```

</TabItem>
</Tabs>

## Token customization policies

A token customization policy allows you to create a new claim name, that you can map to a default claim. The new claim gets the value of the default claim. This allows for easier integration with relying parties that are looking for a specific claim name. For more information on token customization policies, see [Attestation Policies](../Concepts/concept-policies.md#token-customization-policies-and-custom-claims)

### Intel SGX incoming claims

The following claims can be used in the JSON policy input file. For a complete description of the claims, see [Attestation Tokens](../Concepts/concept-attestation-tokens.md#tee-specific-claims). 

|Field Name            |Type       |Field Description             |
|---------------------|---------------------|-----------------------------------|
|**sgx_mrsigner**          |String     |Customization claim name.     |
|**sgx_mrenclave**		   |String     |Customization claim name.     |
|**sgx_isvprodid**         |String     |Customization claim name.     |
|**sgx_isvsvn**            |String     |Customization claim name.     |
|**sgx_isvsvn_min**        |String     |Customization claim name.     |
|**sgx_is_debuggable**     |String     |Customization claim name.     |
|**attester_tcb_date**     |String     |Customization claim name.     |
|**attester_advisory_ids** |String     |Customization claim name.     |
|**attester_tcb_status**   |String     |Customization claim name.     |

#### JSON Intel SGX token customization policy

<Tabs>
<TabItem value="sgx-custom-json" label="SGX token custimization JSON">

### SGX token custimization JSON

The following example shows an Intel SGX TCB custom policy in JSON format, before conversion to Rego. The first object literal in the policy is `"sgx_customization":{}`. That tells Policy Builder that this is an Intel SGX claim set customization policy. This is the input file that is specified for conversion.

```JSON
{
    "policy": {  
            "sgx_customization": {
                "sgx_isvprodid": "my-sgx_isvprodid",
                "sgx_isvsvn": "my-sgx_isvsvn-svn",
                "sgx_mrenclave": "my-sgx_mrenclave",
                "sgx_mrsigner": "my_sgx_mrsigner",
                "sgx_is_debuggable": "my_debuggable",
                "attester_tcb_date": "my_attester_tcb_date",
                "attester_advisory_ids": "my_attester_advisory_id",
                "attester_tcb_status": "my_attester_tcb_status"
            }
    }
}
```

</TabItem>
<TabItem value="sgx-custom-rego" label="[SGX token custimization Rego">

### SGX token custimization Rego

The following example shows the JSON input file, above, after conversion to an Intel SGX TCB custom policy. This is what you'll use to create your policy in Intel Trust Authority. 

```rego
get_token_fields[token_fields] {
token_fields := { 
"my-sgx_isvsvn-svn" : input.sgx_isvsvn,
"my-sgx_isvprodid" : input.sgx_isvprodid,
"my-sgx_mrenclave" : input.sgx_mrenclave,
"my_sgx_mrsigner" : input.sgx_mrsigner,
"my_debuggable" : input.sgx_is_debuggable,
"my_attester_tcb_date" : input.attester_tcb_date,
"my_attester_advisory_id" : input.attester_advisory_ids,
"my_attester_tcb_status" : input.attester_tcb_status,
}}
```

</TabItem>
</Tabs>

### Intel TDX incoming claims

The following claims can be used in the JSON policy input file. For a complete description of the claims, see [Attestation Tokens](../Concepts/concept-attestation-tokens.md#tee-specific-claims). 

The following claims can be used in the JSON custom policy input file. That is, this is the list of input claims you can _rename_ in the output attestation token by using a custom policy. Any claim not on this list can't be renamed.

|Field Name           |Type       |Field Description           |
|---------------------|---------------------|-----------------------------------|
|**tdx_rtmr0**             |String     |Customization claim name.     |
|**tdx_rtmr1**             |String     |Customization claim name.     |
|**tdx_rtmr2**             |String     |Customization claim name.     |
|**tdx_rtmr3**             |String     |Customization claim name.     |
|**tdx_mrtd**              |String     |Customization claim name.     |
|**tdx_mrsignerseam**      |String     |Customization claim name.     |
|**tdx_seamsvn**           |String     |Customization claim name.     |
|**tdx_is_debuggable**     |String     |Customization claim name.     |
|**attester_tcb_date**     |String     |Customization claim name.     |
|**attester_advisory_ids** |String     |Customization claim name.     |
|**attester_tcb_status**   |String     |Customization claim name.     |

#### JSON Intel TDX token customization policy

<Tabs>
<TabItem value="tdx-custom-json" label="TDX token custimization JSON">

### TDX token custimization JSON

The following example shows a Intel TDX custom TCB policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "tdx_customization": {
            "tdx_seamsvn": "my_tdx_seamsvn",
            "tdx_rtmr0": "my_tdx_rtmr0",
            "tdx_rtmr1": "my_tdx_rtmr1",
            "tdx_rtmr2": "my_tdx_rtmr2",
            "tdx_rtmr3": "my_tdx_rtmr3",
            "tdx_mrtd": "my_tdx_mrtd",
            "tdx_mrsignerseam": "my_tdx_mrsignerseam",
            "tdx_is_debuggable": "my_debuggable",
            "attester_tcb_date": "my_attester_tcb_date",
            "attester_advisory_ids": "my_attester_advisory_id",
            "attester_tcb_status": "my_attester_tcb_status"
        }
    }
}
```
</TabItem>
<TabItem value="tdx-custom-rego" label="TDX token custimization Rego">

### TDX token custimization Rego

The following example shows the JSON input file, above, after conversion to an Intel TDX TCB custom policy. This is what you'll use to create your policy in Intel Trust Authority. 

```rego
get_token_fields[token_fields] {
token_fields := { 
"my_tdx_seamsvn" : input.tdx_seamsvn,
"my_tdx_rtmr0" : input.tdx_rtmr0,
"my_tdx_rtmr1" : input.tdx_rtmr1,
"my_tdx_rtmr2" : input.tdx_rtmr2,
"my_tdx_rtmr3" : input.tdx_rtmr3,
"my_tdx_mrtd" : input.tdx_mrtd,
"my_tdx_mrsignerseam" : input.tdx_mrsignerseam,
"my_debuggable" : input.tdx_is_debuggable,
"my_attester_tcb_date" : input.attester_tcb_date,
"my_attester_advisory_id" : input.attester_advisory_ids,
"my_attester_tcb_status" : input.attester_tcb_status,
}}
```

</TabItem>
</Tabs>

## Composite policies

:::note
This feature is in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Intel Trust Authority Pilot environment. Contact your Intel representative for access.
::::

In the latest release of the Policy Builder, Intel Trust Authority will use one policy (composite policy) for all attestations instead of creating an individual policy based on the attestation type. The composite policy supports multiple attestation types in a single policy file.

The composite policy supports the following attestation types:

- [V2 SGX](#v2-sgx-policy)
- [V2 TDX](#v2-tdx-policy)
- [V2 SEVSNP](#sevsnp-policy)
- [V2 NVGPU](#v2-nvgpu-incoming-claims)
- [V2 TDX + NVGPU](#v2-tdx--nvgpu-policy)
- [V2 TDX + TPM](#v2-tdx--tpm-policy)
- [V2 TPM](#v2-tpm-policy)
- [V2 SEVSNP + NVGPU](#v2-sevsnp--nvgpu-policy)
- [V2 SEVSNP + TPM](#v2-sevsnp--tpm-policy)
- [TDX + NVGPU](#v2-tdx--nvgpu-policy)
- [V2 SEVSNP + NVGPU](#v2-sevsnp--nvgpu-policy)

### V2 SGX policy

<Tabs>
<TabItem value="v2-sgx-json" label="V2 SGX JSON">

### V2 SGX JSON

The following example shows a Intel SGX policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "sgx": {
                "sgx_isvprodid": 0,
                "sgx_isvsvn": 1,
                "sgx_mrenclave": "d777e819861adef6ffb2a4865efea9338b91ed30fa33491b17f0d5d9e8204410",
                "sgx_mrsigner": "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e",
                "sgx_is_debuggable": false,
                "min_tcb_date" : "2023-03-15T00:00:00Z",
                "tcb_status_allowed": ["UpToDate", "SWHardeningNeeded"],
                "ttl_period" : 9,
                "allowed_advisory_ids" : ["INTEL-SA-00586", "INTEL-SA-00614", "INTEL-SA-00615"]
            },
            "export": {
                "sgx": {
                    "sgx_isvprodid": "dd-sgx_isvprodids",
                    "sgx_isvsvn": "dd-sgx_isvsvn-svn",
                    "sgx_mrenclave": "dd-sgx_mrenclave",
                    "sgx_mrsigner": "my_sgx_mrsigner",
                    "sgx_is_debuggable": "my_debuggable",
                    "attester_tcb_date": "my_attester_tcb_date",
                    "attester_advisory_ids": "my_attester_advisory_id"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="v2-sgx-rego" label="V2 SGX Rego">

### V2 SGX Rego

The following example shows the JSON input file, above, after conversion to an Intel SGX policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_sgx
}
 
match_sgx {
input.sgx.sgx_isvsvn == 1
input.sgx.sgx_isvprodid == 0
input.sgx.sgx_mrenclave == "d777e819861adef6ffb2a4865efea9338b91ed30fa33491b17f0d5d9e8204410"
input.sgx.sgx_mrsigner == "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e"
input.sgx.sgx_is_debuggable == false
min_tcb_date := "2023-03-15T00:00:00Z"
date_ns_0 := time.parse_rfc3339_ns(input.sgx.attester_tcb_date)
min_date_ns := time.parse_rfc3339_ns(min_tcb_date)
date_ns_0 >= min_date_ns
acceptable_values_for_tcb_status_allowed := {"UpToDate", "SWHardeningNeeded"}
acceptable_values_for_tcb_status_allowed[input.sgx.attester_tcb_status]
ttl_period := 9
date_ns_1 := time.parse_rfc3339_ns(input.sgx.attester_tcb_date)
expiry_date_ns := time.add_date(date_ns_1, 0, ttl_period, 0)
expiry_date_ns >= time.now_ns()
allowed_advisory_ids := {"INTEL-SA-00586", "INTEL-SA-00614", "INTEL-SA-00615"}
system_allowed_advisory_ids:= {id | id := input.sgx.attester_advisory_ids[_]}
object.subset(allowed_advisory_ids,  system_allowed_advisory_ids) }
export := {
"dd-sgx_isvsvn-svn" : input.sgx.sgx_isvsvn,
"dd-sgx_isvprodids" : input.sgx.sgx_isvprodid,
"dd-sgx_mrenclave" : input.sgx.sgx_mrenclave,
"my_sgx_mrsigner" : input.sgx.sgx_mrsigner,
"my_debuggable" : input.sgx.sgx_is_debuggable,
"my_attester_tcb_date" : input.sgx.attester_tcb_date,
"my_attester_advisory_id" : input.sgx.attester_advisory_ids,
}
```

</TabItem>
</Tabs>

### V2 TDX policy

<Tabs>
<TabItem value="v2-tdx-json" label="V2 TDX JSON">

### V2 TDX JSON

The following example shows a Intel TDX policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "tdx": {
                "tdx_seamsvn": 2,
                "tdx_rtmr0": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr1": "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c",
                "tdx_rtmr2": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr3": ["ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"],
                "tdx_mrtd": "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54",
                "tdx_mrsignerseam": "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c"
            },
            "export": {
                "tdx": {
                    "tdx_seamsvn": "my_tdx_seamsvn",
                    "tdx_rtmr0": "my_tdx_rtmr0",
                    "tdx_rtmr1": "my_tdx_rtmr1",
                    "tdx_rtmr2": "my_tdx_rtmr2",
                    "tdx_rtmr3": "my_tdx_rtmr3",
                    "tdx_mrtd": "my_tdx_mrtd",
                    "tdx_mrsignerseam": "my_tdx_mrsignerseam",
                    "tdx_is_debuggable": "my_debuggable",
                    "attester_tcb_date": "my_attester_tcb_date",
                    "attester_advisory_ids": "my_attester_advisory_id",
                    "attester_tcb_status": "my_attester_tcb_status"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="v2-tdx-reg" label="V2 TDX Rego">

### V2 TDX Rego

The following example shows the JSON input file, above, after conversion to an Intel TDX policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_tdx
}
 
match_tdx {
input.tdx.tdx_seamsvn == 2
input.tdx.tdx_rtmr0 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
input.tdx.tdx_rtmr1 == "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c"
input.tdx.tdx_rtmr2 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
acceptable_values_for_tdx_rtmr3 := {"ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"}
acceptable_values_for_tdx_rtmr3[input.tdx.tdx_rtmr3]
input.tdx.tdx_mrtd == "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54"
input.tdx.tdx_mrsignerseam == "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c"
input.tdx.tdx_is_debuggable == true
}
export := {
"my_tdx_seamsvn" : input.tdx.tdx_seamsvn,
"my_tdx_rtmr0" : input.tdx.tdx_rtmr0,
"my_tdx_rtmr1" : input.tdx.tdx_rtmr1,
"my_tdx_rtmr2" : input.tdx.tdx_rtmr2,
"my_tdx_rtmr3" : input.tdx.tdx_rtmr3,
"my_tdx_mrtd" : input.tdx.tdx_mrtd,
"my_tdx_mrsignerseam" : input.tdx.tdx_mrsignerseam,
"my_debuggable" : input.tdx.tdx_is_debuggable,
"my_attester_tcb_date" : input.tdx.attester_tcb_date,
"my_attester_advisory_id" : input.tdx.attester_advisory_ids,
"my_attester_tcb_status" : input.tdx.attester_tcb_status,
}
```

</TabItem>
</Tabs>

### V2 SEVSNP incoming claims


|Claim                    | Datatype                |Description               |
|-------------------------|-------------------------|-----------------------------|
|sevsnp_authorkeydigest   |String or List of String |This is the SHA-384 digest of the Author public key that certified the ID keys if provided in SNP_LAUNCH_FINISH. If the AUTHOR_KEY_EN is 1, zeros are privided.|
|sevsnp_guestsvn          |Number                   |The Software Version Number of the SEV-SNP guest..|
|sevsnp_bootloader_svn    |Number                   |Secure software version of bootloader in SEV-SNP TCB definition.|
|sevsnp_familyId          |String or List of String |The image ID provided at launch.|
|sevsnp_imageId           |String or List of String |Guest-provided data. |
|sevsnp_reportdata        |String or List of String |Guest-provided data. |
|sevsnp_launchmeasurement |String or List of String |This measurement contains the initial state of the VM or workload, platform configuration registers (PCRs) values, BIOS code measurements, hardware configuration details, and other data. |
|sevsnp_hostdata          |String or List of String |Data provided by the hypervisor at launch. |
|sevsnp_idkeydigest       |String or List of String |SHA-384 digest of the ID public key that signed the ID block provided in SNP_LAUNCH_FINISH.|
|sevsnp_is_debuggable     |Boolean                  |A debuggable TEE is not secure. Never trust a debuggable TEE with a confidential workload or secrets. 0: Debugging is disallowed. 1: Debugging is allowed.|
|sevsnp_microcode_svn     |Number                   |Secure software version of microcode in SEV-SNP TCB definition.|
|sevsnp_migration_allowed |Boolean                  |0: Association with a migration agent is disallowed. 1: Association with a migration agent is allowed.|
|sevsnp_smt_allowed       |Boolean                  |Simultaneous Multi-threading (SMT) 0: SMT is disallowed. 1: SMT is allowed.|
|sevsnp_snpfw_svn         |Number                   |Secure software version of secure processor firmware in SEV-SNP TCB definition. |
|sevsnp_tee_svn           |Number                   |Secure software version of trust execution environment in SEV-SNP TCB definition. |
|sevsnp_vmpl              |Number                   |The requested Virtual Machine Privilege Level (VMPL) for the attestation report.|

#### SEVSNP policy

<Tabs>
<TabItem value="v2-sevsp-json" label="V2 SEVSNP JASION">

#### V2 SEVSNP JSON

The following example shows an Intel SEVSNP policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
 {
    "policy": {
        "composite_appraisal":{
            "nvgpu": {
                "secboot" : true,
                "hwmodel": "GH100 A01 GSP BROM",
                "x-nvidia-gpu-arch-check": true,
                "x-nvidia-gpu-attestation-report-cert-chain-validated": true,
                "x-nvidia-gpu-attestation-report-parsed": true,
                "x-nvidia-gpu-attestation-report-signature-verified": true,
                "x-nvidia-gpu-driver-rim-driver-measurements-available": true,
                "x-nvidia-gpu-driver-rim-schema-fetched": true,
                "x-nvidia-gpu-driver-rim-schema-validated": true,
                "x-nvidia-gpu-driver-rim-signature-verified": true,
                "x-nvidia-gpu-measurements-match": true,
                "x-nvidia-gpu-nonce-match": true,
                "x-nvidia-gpu-vbios-rim-measurements-available": true,
                "x-nvidia-gpu-vbios-rim-schema-fetched'": true,
                "x-nvidia-gpu-vbios-rim-cert-validated": true,
                "x-nvidia-gpu-vbios-rim-schema-validated": true,
                "x-nvidia-gpu-vbios-rim-signature-verified": true,
                "x-nvidia-gpu-driver-version": "535.104.05",
                "x-nvidia-gpu-vbios-version": "96.00.5E.00.015"
            },
            "export": {
                "nvgpu": {
                    "secboot" : "mysecboot",
                    "hwmodel": "myhwmodel",
                    "x-nvidia-gpu-arch-check": "myx-nvidia-gpu-arch-check",
                    "x-nvidia-gpu-attestation-report-cert-chain-validated": "myreport-cert-chain-validated",
                    "x-nvidia-gpu-attestation-report-parsed": "myparsed",
                    "x-nvidia-gpu-attestation-report-signature-verified": "myverified",
                    "x-nvidia-gpu-driver-rim-driver-measurements-available": "measurements",
                    "x-nvidia-gpu-driver-rim-schema-fetched": "mysefetched",
                    "x-nvidia-gpu-driver-rim-schema-validated": "myvalidated",
                    "x-nvidia-gpu-driver-rim-signature-verified": "mysecboot",
                    "x-nvidia-gpu-measurements-match": "mysecbootmatch",
                    "x-nvidia-gpu-nonce-match": "my_x-nvidia-gpu-nonce-match",
                    "x-nvidia-gpu-vbios-rim-measurements-available": "myx-nvidia-gpu-vbios-rim-measurements-available",
                    "x-nvidia-gpu-vbios-rim-schema-fetched'": "mysx-nvidia-gpu-vbios-rim-schema-fetched",
                    "x-nvidia-gpu-vbios-rim-cert-validated": "mysex-nvidia-gpu-vbios-rim-schema-fetchedt",
                    "x-nvidia-gpu-vbios-rim-schema-validated": "mysx-nvidia-gpu-vbios-rim-schema-validated",
                    "x-nvidia-gpu-vbios-rim-signature-verified": "mysx-nvidia-gpu-vbios-rim-signature-verified",
                    "x-nvidia-gpu-driver-version": "myx-nvidia-gpu-driver-version",
                    "x-nvidia-gpu-vbios-version":"mys-nvidia-gpu-vbios-version"
                }
            }
        }
    }
}
```

</TabItem>

<TabItem value="v2-sevsp-rego" label="SEVSNP Rego">

#### V2 SEVSNP Rego

The following example shows the JSON input file, above, after conversion to an Intel SEVSNP policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_sevsnp
}
 
match_sevsnp {
input.sevsnp.sevsnp_authorkeydigest == "55795dcfb1e789925f193b414765dcdea9a5a2374c787c26bba2b070882ddd2fd08741da94d21dd1ec5091bfc0e715d7"
input.sevsnp.sevsnp_guestsvn == 0
input.sevsnp.sevsnp_bootloader_svn == 2
input.sevsnp.sevsnp_familyId == "00000000000000000000000000000000"
input.sevsnp.sevsnp_imageId == "00000000000000000000000000000000"
input.sevsnp.sevsnp_reportdata == "a7ddd44a965d012ba26788283c4123a68c0f9139e2297ef87736032a175544908d507f8481cb3a0191d426220c40e32c5d41b8b066fbef67ef426e5fa4193b93"
input.sevsnp.sevsnp_launchmeasurement == "dfa2b37b1d75eab67026b3bf207690df50b3530ec77f60c488ef73b270247f2908f6de85d799d362cf00fec551c7a5be"
input.sevsnp.sevsnp_hostdata == "a000000000000000000000000000000000000000000000000000000000000002"
input.sevsnp.sevsnp_idkeydigest == "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
input.sevsnp.sevsnp_is_debuggable == false
input.sevsnp.sevsnp_microcode_svn == 41
input.sevsnp.sevsnp_migration_allowed == false
input.sevsnp.sevsnp_smt_allowed == true
input.sevsnp.sevsnp_snpfw_svn == 18
input.sevsnp.sevsnp_tee_svn == 0
input.sevsnp.sevsnp_vmpl == 0
}
export := {
"my_sevsnp_isvprodid" : input.sevsnp.sevsnp_authorkeydigest,
"my_sevsnp_isvsvn" : input.sevsnp.sevsnp_guestsvn,
"my_sevsnp_mrenclave" : input.sevsnp.sevsnp_bootloader_svn,
"my_sevsnp_mrsigner" : input.sevsnp.sevsnp_familyId,
"my_debuggable" : input.sevsnp.sevsnp_reportdata,
"my_attester_tcb_date" : input.sevsnp.sevsnp_launchmeasurement,
"my_sevsnp_hostdata" : input.sevsnp.sevsnp_hostdata,
"my_sevsnp_idkeydigest" : input.sevsnp.sevsnp_idkeydigest,
"my_sevsnp_is_debuggable" : input.sevsnp.sevsnp_is_debuggable,
"my_sevsnp_microcode_svn" : input.sevsnp.sevsnp_microcode_svn,
"mysevsnp_migration_allowed" : input.sevsnp.sevsnp_migration_allowed,
"my_sevsnp_smt_allowed" : input.sevsnp.sevsnp_smt_allowed,
"my_sevsnp_snpfw_svn" : input.sevsnp.sevsnp_snpfw_svn,
"my_sevsnp_tee_svn" : input.sevsnp.sevsnp_tee_svn,
"mysevsnp_vmpl" : input.sevsnp.sevsnp_vmpl,
}
```

</TabItem>
</Tabs>

#### V2 NVGPU incoming claims

|Claim                                                | Datatype |Description               |
|-----------------------------------------------------|--------|-----------------------------|
|secboot                                              |Boolean |Checks whether Secure Boot is enabled, which ensures that the firmware and operating system were authenticated during the VM boot process.|
|hwmodel                                              |String  |The unique identifier for the hardware token. |
|x-nvidia-gpu-arch-check                              |Boolean |Determines whether the current GPU architecture is checked.|
|x-nvidia-gpu-attestation-report-cert-chain-validated |Boolean |Determines if the certificate chain of the GPU attestation report verification is successful.|
|x-nvidia-gpu-attestation-report-parsed               |Boolean |Determines if the GPU attestation report is parsed successfully. |
|x-nvidia-gpu-attestation-report-signature-verified   |Boolean |Checks to see if the comparison between the GPU attestation report and the attestation key in the GPU leaf certificate was done.|
|x-nvidia-gpu-driver-rim-driver-measurements-available|Boolean |Check if the Reference Integrity Manifest (RIM) corresponding to the driver version was retrieved from the GPU.|
|x-nvidia-gpu-driver-rim-schema-fetched               |Boolean |Checks if the Driver RIM schema validation is passed.|
|x-nvidia-gpu-driver-rim-schema-validated             |Boolean |Checks whether all GPU measurements are matched. If all measurements are matched, the determinhation is true.|
|x-nvidia-gpu-measurements-match                      |Boolean |Checks whether all GPU measurements are matched. If all measurements are matched, the determinhation is true.|
|x-nvidia-gpu-nonce-match                             |Boolean |Checks whether the nonce in the SPDM GET MEASUREMENT request message matches the generated nonce.|
|x-nvidia-gpu-vbios-rim-measurements-available        |Boolean |Checks if the VBIOS RIM measurements are available. |
|x-nvidia-gpu-vbios-rim-schema-fetched                |Boolean |Checks if the Reference Integrity Manifest (RIM) corresponding to the driver version was retrieved from the GPU. |
|x-nvidia-gpu-vbios-rim-cert-validated                |Boolean |Checks if the VBIOS certificate chain validation passed. |
|x-nvidia-gpu-vbios-rim-schema-validated              |Boolean |Checks if the BIOS RIM Schema validation passed. |
|x-nvidia-gpu-vbios-rim-signature-verified            |Boolean |Checks if the VBIOS RIM signature verification is successful. |
|x-nvidia-gpu-driver-version                          |String  |Driver version fetched from the attestation report. |
|x-nvidia-gpu-vbios-version                           |String  |VBIOS version fetched from the attestation report. |

#### NVGPU policy

<Tabs>
<TabItem value="nvgpu-json" label="V2 NVGPU JSON">

#### V2 NVGPU JSON

The following example shows a V2 NVGPU policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "nvgpu": {
                "secboot" : true,
                "hwmodel": "GH100 A01 GSP BROM",
                "x-nvidia-gpu-arch-check": true,
                "x-nvidia-gpu-attestation-report-cert-chain-validated": true,
                "x-nvidia-gpu-attestation-report-parsed": true,
                "x-nvidia-gpu-attestation-report-signature-verified": true,
                "x-nvidia-gpu-driver-rim-driver-measurements-available": true,
                "x-nvidia-gpu-driver-rim-schema-fetched": true,
                "x-nvidia-gpu-driver-rim-schema-validated": true,
                "x-nvidia-gpu-driver-rim-signature-verified": true,
                "x-nvidia-gpu-measurements-match": true,
                "x-nvidia-gpu-nonce-match": true,
                "x-nvidia-gpu-vbios-rim-measurements-available": true,
                "x-nvidia-gpu-vbios-rim-schema-fetched'": true,
                "x-nvidia-gpu-vbios-rim-cert-validated": true,
                "x-nvidia-gpu-vbios-rim-schema-validated": true,
                "x-nvidia-gpu-vbios-rim-signature-verified": true,
                "x-nvidia-gpu-driver-version": "535.104.05",
                "x-nvidia-gpu-vbios-version": "96.00.5E.00.015"
            },
            "export": {
                "nvgpu": {
                    "secboot" : "mysecboot",
                    "hwmodel": "myhwmodel",
                    "x-nvidia-gpu-arch-check": "myx-nvidia-gpu-arch-check",
                    "x-nvidia-gpu-attestation-report-cert-chain-validated": "myreport-cert-chain-validated",
                    "x-nvidia-gpu-attestation-report-parsed": "myparsed",
                    "x-nvidia-gpu-attestation-report-signature-verified": "myverified",
                    "x-nvidia-gpu-driver-rim-driver-measurements-available": "measurements",
                    "x-nvidia-gpu-driver-rim-schema-fetched": "mysefetched",
                    "x-nvidia-gpu-driver-rim-schema-validated": "myvalidated",
                    "x-nvidia-gpu-driver-rim-signature-verified": "mysecboot",
                    "x-nvidia-gpu-measurements-match": "mysecbootmatch",
                    "x-nvidia-gpu-nonce-match": "my_x-nvidia-gpu-nonce-match",
                    "x-nvidia-gpu-vbios-rim-measurements-available": "myx-nvidia-gpu-vbios-rim-measurements-available",
                    "x-nvidia-gpu-vbios-rim-schema-fetched'": "mysx-nvidia-gpu-vbios-rim-schema-fetched",
                    "x-nvidia-gpu-vbios-rim-cert-validated": "mysex-nvidia-gpu-vbios-rim-schema-fetchedt",
                    "x-nvidia-gpu-vbios-rim-schema-validated": "mysx-nvidia-gpu-vbios-rim-schema-validated",
                    "x-nvidia-gpu-vbios-rim-signature-verified": "mysx-nvidia-gpu-vbios-rim-signature-verified",
                    "x-nvidia-gpu-driver-version": "myx-nvidia-gpu-driver-version",
                    "x-nvidia-gpu-vbios-version":"mys-nvidia-gpu-vbios-version"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="nvgpu-rego" label="V2 NVGPU Rego">

#### V2 NVGPU Rego

The following example shows the JSON input file, above, after conversion to an NVGPU policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_nvgpu
}
 
match_nvgpu {
input.nvgpu.secboot == true
input.nvgpu.hwmodel == "GH100 A01 GSP BROM"
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-signature-verified"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
input.nvgpu["x-nvidia-gpu-driver-version"] == "535.104.05"
input.nvgpu["x-nvidia-gpu-vbios-version"] == "96.00.5E.00.015"
}
export := {
"mysecboot" : input.nvgpu.secboot,
"myhwmodel" : input.nvgpu.hwmodel,
"myx-nvidia-gpu-arch-check" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"],
"myreport-cert-chain-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"],
"myparsed" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"],
"myverified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"measurements" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"],
"mysefetched" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"],
"myvalidated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"],
"mysecbootmatch" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"],
"my_x-nvidia-gpu-nonce-match" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"],
"myx-nvidia-gpu-vbios-rim-measurements-available" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"],
"mysex-nvidia-gpu-vbios-rim-schema-fetchedt" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"],
"mysx-nvidia-gpu-vbios-rim-schema-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"],
"mysx-nvidia-gpu-vbios-rim-signature-verified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"myx-nvidia-gpu-driver-version" : input.nvgpu["x-nvidia-gpu-driver-version"],
"mys-nvidia-gpu-vbios-version" : input.nvgpu["x-nvidia-gpu-vbios-version"],
}
```

</TabItem>
</Tabs>

### V2 TPM incoming claims

|Claim                    | Datatype                |Description               |
|-------------------------|-------------------------|-----------------------------|
|pcrs |List | The PCR measurements that were included in TPM evidence.|

#### PCR Object

|Claim                    | Datatype                |Description               |
|-------------------------|-------------------------|-----------------------------|
|alg |String |  The PCR measurements that were included in TPM evidence.|
|index |Number|The index of the PCR (0 thru 23).|
|digest |String|The PCR's digest/measurement.  |

#### V2 TPM policy

<Tabs>
<TabItem value="tpm-json" label="V2 TPM JSON">

#### V2 TPM JSON

The following example shows a Intel TPM policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal" : {
            "tpm": {
                "pcrs": [
                    {
                        "alg": "SHA-256",
                        "index": 0,
                        "digest": "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 6,
                        "digest": "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 2,
                        "digest": "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
                    }
                ]
            },
            "export": {
                "tpm": {
                    "pcrs": "my_pcrs"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="tpm-rego" label="V2 TPM Rego">

#### V2 TPM Rego

The following example shows the JSON input file, above, after conversion to an Intel TPM policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_tpm
}
 
match_tpm {
pcr0 := input.tpm.pcrs[_]
pcr0.index == 0
pcr0.alg == "SHA-256"
pcr0.digest == "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
 
pcr6 := input.tpm.pcrs[_]
pcr6.index == 6
pcr6.alg == "SHA-256"
pcr6.digest == "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
 
pcr2 := input.tpm.pcrs[_]
pcr2.index == 2
pcr2.alg == "SHA-256"
pcr2.digest == "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
 
}
export := {
"my_pcrs" : input.tpm.pcrs,
}
```

</TabItem>
</Tabs>

#### V2 TDX + NVGPU policy

<Tabs>
<TabItem value="tdx-nvgpu-json" label="V2 TDX + NVGPU JSON">

#### V2 TDX + NVGPU JSON

The following example shows a V2 TDX + NVGPU policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "tdx": {
                "tdx_seamsvn": 2,
                "tdx_rtmr0": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr1": "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c",
                "tdx_rtmr2": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr3": ["ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"],
                "tdx_mrtd": "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54",
                "tdx_mrsignerseam": "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c"
            },
            "nvgpu": {
                "secboot" : true,
                "hwmodel": "GH100 A01 GSP BROM",
                "x-nvidia-gpu-arch-check": true,
                "x-nvidia-gpu-attestation-report-cert-chain-validated": true,
                "x-nvidia-gpu-attestation-report-parsed": true,
                "x-nvidia-gpu-attestation-report-signature-verified": true,
                "x-nvidia-gpu-driver-rim-driver-measurements-available": true,
                "x-nvidia-gpu-driver-rim-schema-fetched": true,
                "x-nvidia-gpu-driver-rim-schema-validated": true,
                "x-nvidia-gpu-driver-rim-signature-verified": true,
                "x-nvidia-gpu-measurements-match": true,
                "x-nvidia-mismatch-indexes" : [1],
                "x-nvidia-gpu-nonce-match": true,
                "x-nvidia-gpu-vbios-rim-measurements-available": true,
                "x-nvidia-gpu-vbios-rim-schema-fetched'": true,
                "x-nvidia-gpu-vbios-rim-cert-validated": true,
                "x-nvidia-gpu-vbios-rim-schema-validated": true,
                "x-nvidia-gpu-vbios-rim-signature-verified": true,
                "x-nvidia-gpu-driver-version": "535.104.05",
                "x-nvidia-gpu-vbios-version": "96.00.5E.00.015"
            },
            "export": {
                "tdx": {
                    "tdx_seamsvn": "my_tdx_seamsvn",
                    "tdx_rtmr0": "my_tdx_rtmr0",
                    "tdx_rtmr1": "my_tdx_rtmr1",
                    "tdx_rtmr2": "my_tdx_rtmr2",
                    "tdx_rtmr3": "my_tdx_rtmr3",
                    "tdx_mrtd": "my_tdx_mrtd",
                    "tdx_mrsignerseam": "my_tdx_mrsignerseam",
                    "tdx_is_debuggable": "my_debuggable",
                    "attester_tcb_date": "my_attester_tcb_date",
                    "attester_advisory_ids": "my_attester_advisory_id",
                    "attester_tcb_status": "my_attester_tcb_status"
                },
                "nvgpu": {
                    "secboot" : "my_secboot",
                    "hwmodel": "my_hwmodel",
                    "x-nvidia-gpu-arch-check": "my_x-nvidia-gpu-arch-check",
                    "x-nvidia-gpu-attestation-report-cert-chain-validated": "my_report-cert-chain-validated",
                    "x-nvidia-gpu-attestation-report-parsed": "my_parsed",
                    "x-nvidia-gpu-attestation-report-signature-verified": "my_verified",
                    "x-nvidia-gpu-driver-rim-driver-measurements-available": "my_measurements_available",
                    "x-nvidia-gpu-driver-rim-schema-fetched": "my_schema-fetched",
                    "x-nvidia-gpu-driver-rim-schema-validated": "my_schema-validated",
                    "x-nvidia-gpu-driver-rim-signature-verified": "my_signature-verified",
                    "x-nvidia-gpu-measurements-match": "my_measurements-match",
                    "x-nvidia-gpu-nonce-match": "my_x-nvidia-gpu-nonce-match",
                    "x-nvidia-gpu-vbios-rim-measurements-available": "my_x-nvidia-gpu-vbios-rim-measurements-available",
                    "x-nvidia-gpu-vbios-rim-schema-fetched'": "my_x-nvidia-gpu-vbios-rim-schema-fetched",
                    "x-nvidia-gpu-vbios-rim-cert-validated": "my_x-nvidia-gpu-vbios-rim-cert-validated",
                    "x-nvidia-gpu-vbios-rim-schema-validated": "my_x-nvidia-gpu-vbios-rim-schema-validated",
                    "x-nvidia-gpu-vbios-rim-signature-verified": "my_x-nvidia-gpu-vbios-rim-signature-verified",
                    "x-nvidia-gpu-driver-version": "my-nvidia-gpu-driver-version",
                    "x-nvidia-gpu-vbios-version":"my-nvidia-gpu-vbios-version"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="tdx-nvgpu" label="V2 TDX = NVGPU Rego">

#### V2 TDX + NVGPU Rego

The following example shows the JSON input file, above, after conversion to an Intel V2 TDX + NVGPU policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_tdx
match_nvgpu
}
 
match_tdx {
input.tdx.tdx_seamsvn == 2
input.tdx.tdx_rtmr0 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
input.tdx.tdx_rtmr1 == "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c"
input.tdx.tdx_rtmr2 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
acceptable_values_for_tdx_rtmr3 := {"ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"}
acceptable_values_for_tdx_rtmr3[input.tdx.tdx_rtmr3]
input.tdx.tdx_mrtd == "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54"
input.tdx.tdx_mrsignerseam == "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c"
}
match_nvgpu {
input.nvgpu.secboot == true
input.nvgpu.hwmodel == "GH100 A01 GSP BROM"
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-signature-verified"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
input.nvgpu["x-nvidia-gpu-driver-version"] == "535.104.05"
input.nvgpu["x-nvidia-gpu-vbios-version"] == "96.00.5E.00.015"
}
export := {
"my_tdx_seamsvn" : input.tdx.tdx_seamsvn,
"my_tdx_rtmr0" : input.tdx.tdx_rtmr0,
"my_tdx_rtmr1" : input.tdx.tdx_rtmr1,
"my_tdx_rtmr2" : input.tdx.tdx_rtmr2,
"my_tdx_rtmr3" : input.tdx.tdx_rtmr3,
"my_tdx_mrtd" : input.tdx.tdx_mrtd,
"my_tdx_mrsignerseam" : input.tdx.tdx_mrsignerseam,
"my_debuggable" : input.tdx.tdx_is_debuggable,
"my_attester_tcb_date" : input.tdx.attester_tcb_date,
"my_attester_advisory_id" : input.tdx.attester_advisory_ids,
"my_attester_tcb_status" : input.tdx.attester_tcb_status,
"my_secboot" : input.nvgpu.secboot,
"my_hwmodel" : input.nvgpu.hwmodel,
"my_x-nvidia-gpu-arch-check" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"],
"my_report-cert-chain-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"],
"my_parsed" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"],
"my_verified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"my_measurements_available" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"],
"my_schema-fetched" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"],
"my_schema-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"],
"my_measurements-match" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"],
"my_x-nvidia-gpu-nonce-match" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"],
"my_x-nvidia-gpu-vbios-rim-measurements-available" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"],
"my_x-nvidia-gpu-vbios-rim-cert-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"],
"my_x-nvidia-gpu-vbios-rim-schema-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"],
"my_x-nvidia-gpu-vbios-rim-signature-verified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"my-nvidia-gpu-driver-version" : input.nvgpu["x-nvidia-gpu-driver-version"],
"my-nvidia-gpu-vbios-version" : input.nvgpu["x-nvidia-gpu-vbios-version"],
}
```

</TabItem>
</Tabs>

#### V2 TDX + TPM policy

<Tabs>
<TabItem value="tdx-tpm-json" label="V2 TDX + TPM JSON">

#### V2 TDX + TPM JSON

The following example shows a V2 TDX + TPM policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```Json
{
    "policy": {
        "composite_appraisal":{
            "tdx": {
                "tdx_seamsvn": 2,
                "tdx_rtmr0": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr1": "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c",
                "tdx_rtmr2": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr3": ["ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"],
                "tdx_mrtd": "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54",
                "tdx_mrsignerseam": "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c",
                "tdx_is_debuggable": true
            },
            "tpm": {
                "pcrs": [
                    {
                        "alg": "SHA-256",
                        "index": 0,
                        "digest": "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 6,
                        "digest": "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 2,
                        "digest": "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
                    }
                ]
            },
            "export": {
                "tdx": {
                    "tdx_seamsvn": "my_tdx_seamsvn",
                    "tdx_rtmr0": "my_tdx_rtmr0",
                    "tdx_rtmr1": "my_tdx_rtmr1",
                    "tdx_rtmr2": "my_tdx_rtmr2",
                    "tdx_rtmr3": "my_tdx_rtmr3",
                    "tdx_mrtd": "my_tdx_mrtd",
                    "tdx_mrsignerseam": "my_tdx_mrsignerseam",
                    "tdx_is_debuggable": "my_debuggable",
                    "attester_tcb_date": "my_attester_tcb_date",
                    "attester_advisory_ids": "my_attester_advisory_id",
                    "attester_tcb_status": "my_attester_tcb_status"
                },
                "tpm": {
                    "pcrs": "my_pcrs"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="tdx-tpm-rego" label="V2 TDX - TPM Rego">

#### V2 TDX + TPM Rego

The following example shows the JSON input file, above, after conversion to an V2 TDX + TPM policy. This is what you'll use to create your policy in Intel Trust Authority. 

```rego
default match = false
match {
match_tdx
match_tpm
}
 
match_tdx {
input.tdx.tdx_seamsvn == 2
input.tdx.tdx_rtmr0 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
input.tdx.tdx_rtmr1 == "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c"
input.tdx.tdx_rtmr2 == "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"
acceptable_values_for_tdx_rtmr3 := {"ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c", "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"}
acceptable_values_for_tdx_rtmr3[input.tdx.tdx_rtmr3]
input.tdx.tdx_mrtd == "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54"
input.tdx.tdx_mrsignerseam == "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c"
input.tdx.tdx_is_debuggable == true
}
match_tpm {
pcr0 := input.tpm.pcrs[_]
pcr0.index == 0
pcr0.alg == "SHA-256"
pcr0.digest == "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
 
pcr6 := input.tpm.pcrs[_]
pcr6.index == 6
pcr6.alg == "SHA-256"
pcr6.digest == "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
 
pcr2 := input.tpm.pcrs[_]
pcr2.index == 2
pcr2.alg == "SHA-256"
pcr2.digest == "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
 
}
export := {
"my_tdx_seamsvn" : input.tdx.tdx_seamsvn,
"my_tdx_rtmr0" : input.tdx.tdx_rtmr0,
"my_tdx_rtmr1" : input.tdx.tdx_rtmr1,
"my_tdx_rtmr2" : input.tdx.tdx_rtmr2,
"my_tdx_rtmr3" : input.tdx.tdx_rtmr3,
"my_tdx_mrtd" : input.tdx.tdx_mrtd,
"my_tdx_mrsignerseam" : input.tdx.tdx_mrsignerseam,
"my_debuggable" : input.tdx.tdx_is_debuggable,
"my_attester_tcb_date" : input.tdx.attester_tcb_date,
"my_attester_advisory_id" : input.tdx.attester_advisory_ids,
"my_attester_tcb_status" : input.tdx.attester_tcb_status,
"my_pcrs" : input.tpm.pcrs,
}
```

</TabItem>
</Tabs>

#### V2 SEVSNP + NVGPU policy

<Tabs>
<TabItem value="sevnsnp-nvgpu-json" label="V2 SEVSNP + NVGPU JSON">

#### V2 SEVSNP + NVGPU JSON

The following example shows a V2 SEVSNP + NVGPU in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "tdx": {
                "tdx_seamsvn": "my_tdx_seamsvn",
                "tdx_rtmr0": "my_tdx_rtmr0",
                "tdx_rtmr1": "my_tdx_rtmr1",
                "tdx_rtmr2": "my_tdx_rtmr2",
                "tdx_rtmr3": "my_tdx_rtmr3",
                "tdx_mrtd": "my_tdx_mrtd"
            },
            "nvgpu": {
                "secboot" : true,
                "hwmodel": "GH100 A01 GSP BROM",
                "x-nvidia-gpu-arch-check": true,
                "x-nvidia-gpu-attestation-report-cert-chain-validated": true,
                "x-nvidia-gpu-attestation-report-parsed": true,
                "x-nvidia-gpu-attestation-report-signature-verified": true,
                "x-nvidia-gpu-driver-rim-driver-measurements-available": true,
                "x-nvidia-gpu-driver-rim-schema-fetched": true,
                "x-nvidia-gpu-driver-rim-schema-validated": true,
                "x-nvidia-gpu-driver-rim-signature-verified": true,
                "x-nvidia-gpu-measurements-match": true,
                "x-nvidia-gpu-nonce-match": true,
                "x-nvidia-gpu-vbios-rim-measurements-available": true,
                "x-nvidia-gpu-vbios-rim-schema-fetched'": true,
                "x-nvidia-gpu-vbios-rim-cert-validated": true,
                "x-nvidia-gpu-vbios-rim-schema-validated": true,
                "x-nvidia-gpu-vbios-rim-signature-verified": true,
                "x-nvidia-gpu-driver-version": "535.104.05",
                "x-nvidia-gpu-vbios-version": "96.00.5E.00.015"
            },
            "export": {
                "sevsnp": {
                    "sevsnp_authorkeydigest": "my_sevsnp_isvprodid",
                    "sevsnp_guestsvn": "my_sevsnp_isvsvn",
                    "sevsnp_bootloader_svn": "my_sevsnp_mrenclave",
                    "sevsnp_familyid": "my_sevsnp_mrsigner",
                    "sevsnp_reportdata": "my_debuggable",
                    "sevsnp_launchmeasurement": "my_attester_tcb_date",
                    "sevsnp_hostdata": "my_sevsnp_hostdata",
                    "sevsnp_idkeydigest": "my_sevsnp_idkeydigest",
                    "sevsnp_is_debuggable": "my_sevsnp_is_debuggable",
                    "sevsnp_microcode_svn": "my_sevsnp_microcode_svn",
                    "sevsnp_migration_allowed": "mysevsnp_migration_allowed",
                    "sevsnp_smt_allowed": "my_sevsnp_smt_allowed",
                    "sevsnp_snpfw_svn": "my_sevsnp_snpfw_svn",
                    "sevsnp_tee_svn": "my_sevsnp_tee_svn",
                    "sevsnp_vmpl": "mysevsnp_vmpl"
                },
                "nvgpu": {
                    "secboot" : "mysecboot",
                    "hwmodel": "myhwmodel",
                    "x-nvidia-gpu-arch-check": "myx-nvidia-gpu-arch-check",
                    "x-nvidia-gpu-attestation-report-cert-chain-validated": "myreport-cert-chain-validated",
                    "x-nvidia-gpu-attestation-report-parsed": "myparsed",
                    "x-nvidia-gpu-attestation-report-signature-verified": "myverified",
                    "x-nvidia-gpu-driver-rim-driver-measurements-available": "measurements",
                    "x-nvidia-gpu-driver-rim-schema-fetched": "mysefetched",
                    "x-nvidia-gpu-driver-rim-schema-validated": "myvalidated",
                    "x-nvidia-gpu-driver-rim-signature-verified": "mysecboot",
                    "x-nvidia-gpu-measurements-match": "mysecbootmatch",
                    "x-nvidia-gpu-nonce-match": "my_x-nvidia-gpu-nonce-match",
                    "x-nvidia-gpu-vbios-rim-measurements-available": "myx-nvidia-gpu-vbios-rim-measurements-available",
                    "x-nvidia-gpu-vbios-rim-schema-fetched'": "mysx-nvidia-gpu-vbios-rim-schema-fetched",
                    "x-nvidia-gpu-vbios-rim-cert-validated": "mysex-nvidia-gpu-vbios-rim-schema-fetchedt",
                    "x-nvidia-gpu-vbios-rim-schema-validated": "mysx-nvidia-gpu-vbios-rim-schema-validated",
                    "x-nvidia-gpu-vbios-rim-signature-verified": "mysx-nvidia-gpu-vbios-rim-signature-verified",
                    "x-nvidia-gpu-driver-version": "myx-nvidia-gpu-driver-version",
                    "x-nvidia-gpu-vbios-version":"mys-nvidia-gpu-vbios-version"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="sevnsnp-nvgpu-rego" label="V2 SEVSNP + NVGPU Rego">

#### V2 SEVSNP + NVGPU Rego

The following example shows the JSON input file, above, after conversion to an SEVSNP + NVGPU policy. This is what you'll use to create your policy in Intel Trust Authority. 

```rego
default match = false
match {
match_sevsnp
match_nvgpu
}
 
match_sevsnp {
input.sevsnp.sevsnp_authorkeydigest == "55795dcfb1e789925f193b414765dcdea9a5a2374c787c26bba2b070882ddd2fd08741da94d21dd1ec5091bfc0e715d7"
input.sevsnp.sevsnp_guestsvn == 0
input.sevsnp.sevsnp_bootloader_svn == 2
acceptable_values_for_sevsnp_familyId := {"00000000000000000000000000000000", "00000000000000000000000000000030"}
acceptable_values_for_sevsnp_familyId[input.sevsnp.sevsnp_familyId]
input.sevsnp.sevsnp_imageId == "00000000000000000000000000000000"
input.sevsnp.sevsnp_reportdata == "a7ddd44a965d012ba26788283c4123a68c0f9139e2297ef87736032a175544908d507f8481cb3a0191d426220c40e32c5d41b8b066fbef67ef426e5fa4193b93"
input.sevsnp.sevsnp_launchmeasurement == "dfa2b37b1d75eab67026b3bf207690df50b3530ec77f60c488ef73b270247f2908f6de85d799d362cf00fec551c7a5be"
input.sevsnp.sevsnp_hostdata == "a000000000000000000000000000000000000000000000000000000000000002"
input.sevsnp.sevsnp_idkeydigest == "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
input.sevsnp.sevsnp_is_debuggable == false
input.sevsnp.sevsnp_microcode_svn == 41
input.sevsnp.sevsnp_migration_allowed == false
input.sevsnp.sevsnp_smt_allowed == true
input.sevsnp.sevsnp_snpfw_svn == 18
input.sevsnp.sevsnp_tee_svn == 0
input.sevsnp.sevsnp_vmpl == 0
}
match_nvgpu {
input.nvgpu.secboot == true
input.nvgpu.hwmodel == "GH100 A01 GSP BROM"
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-signature-verified"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
input.nvgpu["x-nvidia-gpu-driver-version"] == "535.104.05"
input.nvgpu["x-nvidia-gpu-vbios-version"] == "96.00.5E.00.015"
}
export := {
"my_sevsnp_isvprodid" : input.sevsnp.sevsnp_authorkeydigest,
"my_sevsnp_isvsvn" : input.sevsnp.sevsnp_guestsvn,
"my_sevsnp_mrenclave" : input.sevsnp.sevsnp_bootloader_svn,
"my_sevsnp_mrsigner" : input.sevsnp.sevsnp_familyId,
"my_debuggable" : input.sevsnp.sevsnp_reportdata,
"my_attester_tcb_date" : input.sevsnp.sevsnp_launchmeasurement,
"my_sevsnp_hostdata" : input.sevsnp.sevsnp_hostdata,
"my_sevsnp_idkeydigest" : input.sevsnp.sevsnp_idkeydigest,
"my_sevsnp_is_debuggable" : input.sevsnp.sevsnp_is_debuggable,
"my_sevsnp_microcode_svn" : input.sevsnp.sevsnp_microcode_svn,
"mysevsnp_migration_allowed" : input.sevsnp.sevsnp_migration_allowed,
"my_sevsnp_smt_allowed" : input.sevsnp.sevsnp_smt_allowed,
"my_sevsnp_snpfw_svn" : input.sevsnp.sevsnp_snpfw_svn,
"my_sevsnp_tee_svn" : input.sevsnp.sevsnp_tee_svn,
"mysevsnp_vmpl" : input.sevsnp.sevsnp_vmpl,
"mysecboot" : input.nvgpu.secboot,
"myhwmodel" : input.nvgpu.hwmodel,
"myx-nvidia-gpu-arch-check" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"],
"myreport-cert-chain-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"],
"myparsed" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"],
"myverified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"measurements" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"],
"mysefetched" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"],
"myvalidated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"],
"mysecbootmatch" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"],
"my_x-nvidia-gpu-nonce-match" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"],
"myx-nvidia-gpu-vbios-rim-measurements-available" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"],
"mysex-nvidia-gpu-vbios-rim-schema-fetchedt" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"],
"mysx-nvidia-gpu-vbios-rim-schema-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"],
"mysx-nvidia-gpu-vbios-rim-signature-verified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"myx-nvidia-gpu-driver-version" : input.nvgpu["x-nvidia-gpu-driver-version"],
"mys-nvidia-gpu-vbios-version" : input.nvgpu["x-nvidia-gpu-vbios-version"],
}
```

</TabItem>
</Tabs>
---

#### V2 SEVSNP + TPM policy

<Tabs>
<TabItem value="sevnsnp-tpm-json" label="V2 SEVSNP + TPM JSON">

#### V2 SEVSNP + TPM JSON

The following example shows a V2 SEVSNP + TPM policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "sevsnp": {
                "sevsnp_authorkeydigest": "55795dcfb1e789925f193b414765dcdea9a5a2374c787c26bba2b070882ddd2fd08741da94d21dd1ec5091bfc0e715d7",
                "sevsnp_guestsvn": 0,
                "sevsnp_bootloader_svn": 2,
                "sevsnp_familyid" : ["00000000000000000000000000000000","00000000000000000000000000000030"],
                "sevsnp_imageid" : "00000000000000000000000000000000",
                "sevsnp_reportdata" : "a7ddd44a965d012ba26788283c4123a68c0f9139e2297ef87736032a175544908d507f8481cb3a0191d426220c40e32c5d41b8b066fbef67ef426e5fa4193b93",
                "sevsnp_launchmeasurement" : "dfa2b37b1d75eab67026b3bf207690df50b3530ec77f60c488ef73b270247f2908f6de85d799d362cf00fec551c7a5be",
                "sevsnp_hostdata" : "a000000000000000000000000000000000000000000000000000000000000002",
                "sevsnp_idkeydigest" : "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "sevsnp_is_debuggable" : false,
                "sevsnp_microcode_svn" : 41,
                "sevsnp_migration_allowed" : false,
                "sevsnp_smt_allowed" : true,
                "sevsnp_snpfw_svn" : 18,
                "sevsnp_tee_svn" : 0,
                "sevsnp_vmpl" : 0
            },
            "tpm": {
                "pcrs": [
                    {
                        "alg": "SHA-256",
                        "index": 0,
                        "digest": "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 6,
                        "digest": "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 2,
                        "digest": "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
                    }
                ]
            },
            "export": {
                "sevsnp": {
                    "sevsnp_authorkeydigest": "my_sevsnp_isvprodid",
                    "sevsnp_guestsvn": "my_sevsnp_isvsvn",
                    "sevsnp_bootloader_svn": "my_sevsnp_mrenclave",
                    "sevsnp_familyid": "my_sevsnp_mrsigner",
                    "sevsnp_reportdata": "my_debuggable",
                    "sevsnp_launchmeasurement": "my_attester_tcb_date",
                    "sevsnp_hostdata": "my_sevsnp_hostdata",
                    "sevsnp_idkeydigest": "my_sevsnp_idkeydigest",
                    "sevsnp_is_debuggable": "my_sevsnp_is_debuggable",
                    "sevsnp_microcode_svn": "my_sevsnp_microcode_svn",
                    "sevsnp_migration_allowed": "mysevsnp_migration_allowed",
                    "sevsnp_smt_allowed": "my_sevsnp_smt_allowed",
                    "sevsnp_snpfw_svn": "my_sevsnp_snpfw_svn",
                    "sevsnp_tee_svn": "my_sevsnp_tee_svn",
                    "sevsnp_vmpl": "mysevsnp_vmpl"
                },
                "tpm": {
                    "pcrs": "my_pcrs"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="sevnsnp-tpm-rego" label="V2 SEVSNP + TPM Rego">

#### V2 SEVSNP + TPM Rego

The following example shows the JSON input file, above, after conversion to an Intel TDX TCB custom policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_sevsnp
match_tpm
}
 
match_sevsnp {
input.sevsnp.sevsnp_authorkeydigest == "55795dcfb1e789925f193b414765dcdea9a5a2374c787c26bba2b070882ddd2fd08741da94d21dd1ec5091bfc0e715d7"
input.sevsnp.sevsnp_guestsvn == 0
input.sevsnp.sevsnp_bootloader_svn == 2
acceptable_values_for_sevsnp_familyId := {"00000000000000000000000000000000", "00000000000000000000000000000030"}
acceptable_values_for_sevsnp_familyId[input.sevsnp.sevsnp_familyId]
input.sevsnp.sevsnp_imageId == "00000000000000000000000000000000"
input.sevsnp.sevsnp_reportdata == "a7ddd44a965d012ba26788283c4123a68c0f9139e2297ef87736032a175544908d507f8481cb3a0191d426220c40e32c5d41b8b066fbef67ef426e5fa4193b93"
input.sevsnp.sevsnp_launchmeasurement == "dfa2b37b1d75eab67026b3bf207690df50b3530ec77f60c488ef73b270247f2908f6de85d799d362cf00fec551c7a5be"
input.sevsnp.sevsnp_hostdata == "a000000000000000000000000000000000000000000000000000000000000002"
input.sevsnp.sevsnp_idkeydigest == "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
input.sevsnp.sevsnp_is_debuggable == false
input.sevsnp.sevsnp_microcode_svn == 41
input.sevsnp.sevsnp_migration_allowed == false
input.sevsnp.sevsnp_smt_allowed == true
input.sevsnp.sevsnp_snpfw_svn == 18
input.sevsnp.sevsnp_tee_svn == 0
input.sevsnp.sevsnp_vmpl == 0
}
match_tpm {
pcr0 := input.tpm.pcrs[_]
pcr0.index == 0
pcr0.alg == "SHA-256"
pcr0.digest == "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
 
pcr6 := input.tpm.pcrs[_]
pcr6.index == 6
pcr6.alg == "SHA-256"
pcr6.digest == "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
 
pcr2 := input.tpm.pcrs[_]
pcr2.index == 2
pcr2.alg == "SHA-256"
pcr2.digest == "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
 
}
export := {
"my_sevsnp_isvprodid" : input.sevsnp.sevsnp_authorkeydigest,
"my_sevsnp_isvsvn" : input.sevsnp.sevsnp_guestsvn,
"my_sevsnp_mrenclave" : input.sevsnp.sevsnp_bootloader_svn,
"my_sevsnp_mrsigner" : input.sevsnp.sevsnp_familyId,
"my_debuggable" : input.sevsnp.sevsnp_reportdata,
"my_attester_tcb_date" : input.sevsnp.sevsnp_launchmeasurement,
"my_sevsnp_hostdata" : input.sevsnp.sevsnp_hostdata,
"my_sevsnp_idkeydigest" : input.sevsnp.sevsnp_idkeydigest,
"my_sevsnp_is_debuggable" : input.sevsnp.sevsnp_is_debuggable,
"my_sevsnp_microcode_svn" : input.sevsnp.sevsnp_microcode_svn,
"mysevsnp_migration_allowed" : input.sevsnp.sevsnp_migration_allowed,
"my_sevsnp_smt_allowed" : input.sevsnp.sevsnp_smt_allowed,
"my_sevsnp_snpfw_svn" : input.sevsnp.sevsnp_snpfw_svn,
"my_sevsnp_tee_svn" : input.sevsnp.sevsnp_tee_svn,
"mysevsnp_vmpl" : input.sevsnp.sevsnp_vmpl,
"my_pcrs" : input.tpm.pcrs,
}
```

</TabItem>
</Tabs>

#### V2 TDX + NVGPU + TPM policy

<Tabs>
<TabItem value="tdx-nvgpu-tpm-json" label="V2 TDX + NVGPU + TPM JSON">

#### V2 TDX + NVGPU + TPM JSON

The following example shows a V2 TDX + NVGPU + TPM policy in JSON format, before conversion to Rego. This is the input file that is specified for conversion.

```json
{
    "policy": {
        "composite_appraisal":{
            "tdx": {
                "tdx_seamsvn": 2,
                "tdx_rtmr0": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr1": "ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c",
                "tdx_rtmr2": "0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983",
                "tdx_rtmr3": ["ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","ca6acd5094d9319bb2d04b1859931a88124c81e4818d43cf582d98d8b2d334bba3eada276ae93a352ede1f1a5e7f2f5c","0b787fd971c0518f82ba4ec05109122093958517b2e19f918efa103c3f07017c8bc0ac63f97ecccfb081362fdc4bd983"],
                "tdx_mrtd": "3dfeeb7cf01210c0df8f5adffc65c7ad8a1741119ec873c8a3cf81adefb21fcd1b828b776ead31369cfe7470ac322d54",
                "tdx_mrsignerseam": "03f7b0e40e9ebd4bb4b346048bdc0879d0084d534f7848dd8d4f1be4b0e9610d22f72e45ce4d941c056d4db74eb0028c",
                "tdx_is_debuggable": true
            },
            "nvgpu": {
                "secboot" : true,
                "hwmodel": "GH100 A01 GSP BROM",
                "x-nvidia-gpu-arch-check": true,
                "x-nvidia-gpu-attestation-report-cert-chain-validated": true,
                "x-nvidia-gpu-attestation-report-parsed": true,
                "x-nvidia-gpu-attestation-report-signature-verified": true,
                "x-nvidia-gpu-driver-rim-driver-measurements-available": true,
                "x-nvidia-gpu-driver-rim-schema-fetched": true,
                "x-nvidia-gpu-driver-rim-schema-validated": true,
                "x-nvidia-gpu-driver-rim-signature-verified": true,
                "x-nvidia-gpu-measurements-match": true,
                "x-nvidia-gpu-nonce-match": true,
                "x-nvidia-gpu-vbios-rim-measurements-available": true,
                "x-nvidia-gpu-vbios-rim-schema-fetched'": true,
                "x-nvidia-gpu-vbios-rim-cert-validated": true,
                "x-nvidia-gpu-vbios-rim-schema-validated": true,
                "x-nvidia-gpu-vbios-rim-signature-verified": true,
                "x-nvidia-gpu-driver-version": "535.104.05",
                "x-nvidia-gpu-vbios-version": "96.00.5E.00.015"
            },
            "tpm": {
                "pcrs": [
                    {
                        "alg": "SHA-256",
                        "index": 0,
                        "digest": "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 6,
                        "digest": "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
                    },
                    {
                        "alg": "SHA-256",
                        "index": 2,
                        "digest": "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
                    }
                ]
            },
            "export": {
                "tdx": {
                    "tdx_seamsvn": "my_tdx_seamsvn",
                    "tdx_rtmr0": "my_tdx_rtmr0",
                    "tdx_rtmr1": "my_tdx_rtmr1",
                    "tdx_rtmr2": "my_tdx_rtmr2",
                    "tdx_rtmr3": "my_tdx_rtmr3",
                    "tdx_mrtd": "my_tdx_mrtd",
                    "tdx_mrsignerseam": "my_tdx_mrsignerseam",
                    "tdx_is_debuggable": "my_debuggable",
                    "attester_tcb_date": "my_attester_tcb_date",
                    "attester_advisory_ids": "my_attester_advisory_id",
                    "attester_tcb_status": "my_attester_tcb_status"
                },
                "nvgpu": {
                    "secboot" : "mysecboot",
                    "hwmodel": "myhwmodel",
                    "x-nvidia-gpu-arch-check": "myx-nvidia-gpu-arch-check",
                    "x-nvidia-gpu-attestation-report-cert-chain-validated": "myreport-cert-chain-validated",
                    "x-nvidia-gpu-attestation-report-parsed": "myparsed",
                    "x-nvidia-gpu-attestation-report-signature-verified": "myverified",
                    "x-nvidia-gpu-driver-rim-driver-measurements-available": "measurements",
                    "x-nvidia-gpu-driver-rim-schema-fetched": "mysefetched",
                    "x-nvidia-gpu-driver-rim-schema-validated": "myvalidated",
                    "x-nvidia-gpu-driver-rim-signature-verified": "mysecboot",
                    "x-nvidia-gpu-measurements-match": "mysecbootmatch",
                    "x-nvidia-gpu-nonce-match": "my_x-nvidia-gpu-nonce-match",
                    "x-nvidia-gpu-vbios-rim-measurements-available": "myx-nvidia-gpu-vbios-rim-measurements-available",
                    "x-nvidia-gpu-vbios-rim-schema-fetched'": "mysx-nvidia-gpu-vbios-rim-schema-fetched",
                    "x-nvidia-gpu-vbios-rim-cert-validated": "mysex-nvidia-gpu-vbios-rim-schema-fetchedt",
                    "x-nvidia-gpu-vbios-rim-schema-validated": "mysx-nvidia-gpu-vbios-rim-schema-validated",
                    "x-nvidia-gpu-vbios-rim-signature-verified": "mysx-nvidia-gpu-vbios-rim-signature-verified",
                    "x-nvidia-gpu-driver-version": "myx-nvidia-gpu-driver-version",
                    "x-nvidia-gpu-vbios-version":"mys-nvidia-gpu-vbios-version"
                },
                "tpm": {
                    "pcrs": "my_pcrs"
                }
            }
        }
    }
}
```

</TabItem>
<TabItem value="tdx-nvgpu-tpm-rego" label="V2 TDX + NVGPU + TPM Rego">

#### V2 TDX + NVGPU + TPM Rego

The following example shows the JSON input file, above, after conversion to a V2 TDX + NVGPU + TPM policy. This is what you'll use to create your policy in Intel Trust Authority.

```rego
default match = false
match {
match_sevsnp
match_tpm
match_nvgpu
}
 
match_sevsnp {
input.sevsnp.sevsnp_authorkeydigest == "55795dcfb1e789925f193b414765dcdea9a5a2374c787c26bba2b070882ddd2fd08741da94d21dd1ec5091bfc0e715d7"
input.sevsnp.sevsnp_guestsvn == 0
input.sevsnp.sevsnp_bootloader_svn == 2
acceptable_values_for_sevsnp_familyId := {"00000000000000000000000000000000", "00000000000000000000000000000030"}
acceptable_values_for_sevsnp_familyId[input.sevsnp.sevsnp_familyId]
input.sevsnp.sevsnp_imageId == "00000000000000000000000000000000"
input.sevsnp.sevsnp_reportdata == "a7ddd44a965d012ba26788283c4123a68c0f9139e2297ef87736032a175544908d507f8481cb3a0191d426220c40e32c5d41b8b066fbef67ef426e5fa4193b93"
input.sevsnp.sevsnp_launchmeasurement == "dfa2b37b1d75eab67026b3bf207690df50b3530ec77f60c488ef73b270247f2908f6de85d799d362cf00fec551c7a5be"
input.sevsnp.sevsnp_hostdata == "a000000000000000000000000000000000000000000000000000000000000002"
input.sevsnp.sevsnp_idkeydigest == "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
input.sevsnp.sevsnp_is_debuggable == false
input.sevsnp.sevsnp_microcode_svn == 41
input.sevsnp.sevsnp_migration_allowed == false
input.sevsnp.sevsnp_smt_allowed == true
input.sevsnp.sevsnp_snpfw_svn == 18
input.sevsnp.sevsnp_tee_svn == 0
input.sevsnp.sevsnp_vmpl == 0
}
match_tpm {
pcr0 := input.tpm.pcrs[_]
pcr0.index == 0
pcr0.alg == "SHA-256"
pcr0.digest == "079a2a9d8dff890295ecbca39089b01c06f0866f2080941a651f97433dcbf584"
 
pcr6 := input.tpm.pcrs[_]
pcr6.index == 6
pcr6.alg == "SHA-256"
pcr6.digest == "1e7acc6548735981543be740e8a8662985d0602ffe826f0ffaefce83a9182a3b"
 
pcr2 := input.tpm.pcrs[_]
pcr2.index == 2
pcr2.alg == "SHA-256"
pcr2.digest == "af3544b4e74294f11b94e5c0ea5660a2a9c0f7c0ad3247880e18b80b1a369674"
 
}
match_nvgpu {
input.nvgpu.secboot == true
input.nvgpu.hwmodel == "GH100 A01 GSP BROM"
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-signature-verified"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"] == true
input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
input.nvgpu["x-nvidia-gpu-driver-version"] == "535.104.05"
input.nvgpu["x-nvidia-gpu-vbios-version"] == "96.00.5E.00.015"
}
export := {
"my_sevsnp_isvprodid" : input.sevsnp.sevsnp_authorkeydigest,
"my_sevsnp_isvsvn" : input.sevsnp.sevsnp_guestsvn,
"my_sevsnp_mrenclave" : input.sevsnp.sevsnp_bootloader_svn,
"my_sevsnp_mrsigner" : input.sevsnp.sevsnp_familyId,
"my_debuggable" : input.sevsnp.sevsnp_reportdata,
"my_attester_tcb_date" : input.sevsnp.sevsnp_launchmeasurement,
"my_sevsnp_hostdata" : input.sevsnp.sevsnp_hostdata,
"my_sevsnp_idkeydigest" : input.sevsnp.sevsnp_idkeydigest,
"my_sevsnp_is_debuggable" : input.sevsnp.sevsnp_is_debuggable,
"my_sevsnp_microcode_svn" : input.sevsnp.sevsnp_microcode_svn,
"mysevsnp_migration_allowed" : input.sevsnp.sevsnp_migration_allowed,
"my_sevsnp_smt_allowed" : input.sevsnp.sevsnp_smt_allowed,
"my_sevsnp_snpfw_svn" : input.sevsnp.sevsnp_snpfw_svn,
"my_sevsnp_tee_svn" : input.sevsnp.sevsnp_tee_svn,
"mysevsnp_vmpl" : input.sevsnp.sevsnp_vmpl,
"my_pcrs" : input.tpm.pcrs,
"my_secboot" : input.nvgpu.secboot,
"my_hwmodel" : input.nvgpu.hwmodel,
"my_x-nvidia-gpu-arch-check" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-arch-check"],
"my_report-cert-chain-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"],
"my_parsed" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"],
"my_verified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"my_measurements_available" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"],
"my_schema-fetched" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"],
"my_schema-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"],
"my_measurements-match" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"],
"my_x-nvidia-gpu-nonce-match" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-nonce-match"],
"my_x-nvidia-gpu-vbios-rim-measurements-available" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-measurements-available"],
"my_x-nvidia-gpu-vbios-rim-cert-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"],
"my_x-nvidia-gpu-vbios-rim-schema-validated" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"],
"my_x-nvidia-gpu-vbios-rim-signature-verified" : input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"],
"my-nvidia-gpu-driver-version" : input.nvgpu["x-nvidia-gpu-driver-version"],
"my-nvidia-gpu-vbios-version" : input.nvgpu["x-nvidia-gpu-vbios-version"],
}
```

</TabItem>
</Tabs>
