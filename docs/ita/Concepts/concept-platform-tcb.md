---
title: Platform TCB Policy
description: An overview of platform trusted compute base (TCB) recovery policy.
author: pcartee
topic: conceptual
date: 01/26/2024
uid: attestation.tcb.policy
---

This article describes how to use Intel® Trust Authority policy features to make attestation decisions based on the attester's trusted compute base (TCB) status. This information applies to Intel® Software Guard Extensions (Intel® SGX) and Intel® Trust Domain Extensions (Intel® TDX) TEEs.

## Platform TCB 

The Intel platform TCB comprises the components that are critical to meeting Intel's platform security objectives. Platform TCB components include the processor hardware, processor microcode, system firmware, BIOS settings, and platform software (PSW). Most of the TCB is _mutable_, meaning that it can be updated when necessary. An exception to TCB mutability is the processor circuitry and cryptographic key fuses, which can't be changed after manufacture. It's not uncommon for a supported platform to receive one or more TCB updates during its service life. 

Intel publishes TCB updates twice a year, in February and August to align with the Intel Platform Update cycles. The current TCB level for any given FMSPC (Family, Model, Stepping, Platform Type, and Customized SKU) is available from Intel® SGX Provisioning Certification Service or Intel® TDX Provisioning Certification Service.

A new TCB level is defined when a security vulnerability or other update requires changes to the platform TCB. Publication of a new TCB level initiates a TCB recovery (TCB-R) event. For a detailed description of TCB and TCB-R, see [Intel Software Guard Extensions Trusted Computing Base Recovery](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/resources/q1-2024-intel-tcb-recovery-guidance.html).

A new TCB level is certified as of the publication date and time (tcbDate). If there are no changes to the platform, the previous platform is re-certified and issued under the latest TCB date.

Intel Trust Authority will get the new TCB-R as soon as it is published and immediately apply the latest TCB-R to attestation results. In contrast, a CSP needs some time to patch their entire confidential computing (CC) fleet to deploy the TCB-R. The CC workload owner might also need more time to patch the workload when a platform software update is needed to mitigate the TCB-R advisories. Thus, an attestation TCB status of other than UpToDate is a relatively common scenario following a recent TCB-R.

Given the above, the CC owner and/or relying party may need to accept—within well-defined limits—an out-of-date TCB status to maintain business continuity. The relying party must be able to compare the attester TCB status to the most recent TCB-R to decide if the attesting platform TCB is acceptable. Intel Trust Authority provides attester claims and built-in policy functions you can use to make appraisal policy decisions for an out-of-date attester TCB. The rest of this article describes the claims and gives example appraisal policies for common use cases.

## TCB policy

TCB policy is not another kind of Intel Trust Authority policy, like appraisal and token modification policies. TCB policy refers to your organization's policy regarding acceptable TCB status. You'll implement your TCB policy using appraisal policies.

In the case where platform TCB lags behind the most recent TCB-R, an appraisal policy that tests only for `attester_tcb_status="UpToDate"` will fail even though the platform TCB might still meet your CC platform minimum standard. The attester TCB claims provide enough information for you to make a go/no-go determination of platform TCB status by using an appraisal policy.

The basic steps for implementing a TCB policy in an appraisal policy are as follows:

1. Check the **attester_tcb_status** claim to see if it contains an acceptable TCB status value. 
2. Check the **attester_tcb_date** claim to see if the date is within an acceptable grace period or "time to live" (TTL) period. 
3. Check **attester_advisory_ids** to see which, if any, security advisories are included in the latest TCB-R. 

### Attester TCB claims

The following claims apply to both Intel SGX and Intel TDX TEEs.

| Claim | Description |
| --- | --- |
| **attester_tcb_date** | The attesting platform's TCB date, which is the publication date of the most recent TCB-R update. The date is a UTC time value in ISO 8601 format `YYYY-MM-DDThh:mm:ssZ`. |
| **attester_tcb_status** | The TCB status relative to the latest TCB level info obtained from the PCS. See the following table for TCB status value descriptions. |
| **attester_advisory_ids** | An array of one or more Intel Product Security Center Advisory IDs. An advisory ID is a string in the format `INTEL-SA-nnnnn`. See the [Intel® Product Security Center Advisories](https://www.intel.com/content/www/us/en/security-center/default.html) page for current advisories. |

| TCB status value | Description |
| --- | --- |
| "UpToDate" | The attesting platform is patched with the latest firmware and software and no known security advisories apply. |
| "SWHardeningNeeded" | The platform firmware and software are at the latest security patching level but there are vulnerabilities that can only be mitigated by software changes to the enclave or TD. |
| "ConfigurationNeeded" | The platform firmware and software are at the latest security patching level but there are platform hardware configurations required to mitigate vulnerabilities. |
| "ConfigurationAndSWHardeningNeeded" | Both of the above. |
| "OutOfDate" | The attesting platform software and/or firmware is not patched in accordance with the latest TCB Recovery (TCB-R). |
| "OutOfDateConfigurationNeeded" | The attesting platform is not patched in accordance with the latest TCB-R. Hardware configuration is needed. |

## Platform TCB custom policy examples

### Minimum TCB date policy

This policy enforces a minimum (earliest) TCB date.

```bash
default policy_matched := false
 
policy_matched {
    min_tcb_date := "2023-02-15T00:00:00Z" 
    attester_tcb_date_ns := time.parse_rfc3339_ns(input.attester_tcb_date)
    min_tcb_date_ns := time.parse_rfc3339_ns(min_tcb_date)
    attester_tcb_date_ns >= min_tcb_date_ns
}
```

### TCB TTL policy

This policy is to specify a lifespan (Time-To-Live, TTL) of the TCB level, i.e. a TCB level is acceptable as long as it's within the lifespan when it's evaluated. The policy fails if 1) the attesting platform TCB level (**attester_tcb_status**) is out of date, and 2) the attesting platform TCB date (**attester_tcb_date**) + TTL period is less than the current date & time (time.now). 

Intel publishes updated or re-certified TCB-Rs every six months. The latest TCB level will remain up to date for approximately six months after it's created or re-certified. When the TCB TTL is greater than six months, it allows the infrastructure provider to update its platforms to the new TCB-R within a grace period determined by the TTL. If the CSP typically needs up to one month to patch all its CC platforms, a TTL of seven months allows enough time to fully deploy the latest TCB-R.

```bash
default policy_matched := false
 
tcb_level_is_up2date {
    # List the acceptable TCB status values. 
    tcb_level_up2date := {"UpToDate", "SWHardeningNeeded", "ConfigurationNeeded", "ConfigurationAndSWHardeningNeeded"}
    tcb_level_up2date[input.attester_tcb_status]  # True if attester_tcb_status value is in the tcb_level_up2date array.
}
 
within_tcb_ttl {
    attester_tcb_date_ns := time.parse_rfc3339_ns(input.attester_tcb_date)
    ttl_period := 7 # months
    expiry_date_ns := time.add_date(attester_tcb_date_ns, 0, ttl_period, 0)
    expiry_date_ns > time.now_ns() #True only if the expiration date is in the future.
}

# Both tcb_level_is_up2date and within_tcb_ttl must be true for the policy to be matched.
policy_matched {
    tcb_level_is_up2date
}
 
policy_matched {
    within_tcb_ttl
}
```

### Allowed/disallowed security advisories policy

Compare the **attester_advisory_ids** value to your list of allowed or disallowed advisories.

```bash
default policy_matched := false
 
policy_matched {
    allowed_advisory_ids := {"INTEL-SA-00586", "INTEL-SA-00614", "INTEL-SA-00615"}
    attester_advisory_ids := {id | id := input.attester_advisory_ids[_]}
    object.subset(allowed_advisory_ids, attester_advisory_ids)
}
```

```bash
default policy_matched := false
 
policy_matched {
    disallowed_advisory_ids := {"INTEL-SA-00586", "INTEL-SA-00614", "INTEL-SA-00615"}
    attester_advisory_ids := {id | id := input.attester_advisory_ids[_]} # convert array to set
    intersection := attester_advisory_ids & disallowed_advisory_ids
    count(intersection) == 0
}
```
