---
title: Event logs
description: TPM Logs
author: mkwilbux, pcartee, teknoll
topic-type: conceptual
date: 10/25/2024
uid: tpm.log
---

*· 10/25/2024 ·*

## Trusted Platform Module (TPM) event logs

TPMs have 24 Platform Configuration Registers (PCRs). These PCRs contain hash measurements based on a large number of measurement events. Most of these happen during boot (UEFI events) and others happen during runtime (IMA events). You can use these PCR measurements to verify the integrity of parts of the system. 

## TPM/vTPM Attestation
A Trusted Platform Module (TPM) is a device that provides several security functions. A Virtual TPM (vTPM) provides the functions of a TPM in software (typically in the hypervisor), providing TPM functions to virtual machines.

System components (such as the UEFI, OS kernel, boot loader, etc) are measured before execution during the boot process, and these measurements can be used to detect any modifications or unauthorized changes to those measured components.

# TPM Event Logs: Ensuring System Integrity

TPMs (Trusted Platform Module) play a crucial role in ensuring the integrity of a system. One of the key components of TPMs is the PCR (Platform Configuration Register), which contains hash measurements based on various measurement events. These events can occur during boot, such as UEFI events, or during runtime, like IMA events. 

TCG Event Logs (UEFI event logs) are used for boot time platform attestation, verified or replayed using PCRs. IMA logs are used for runtime file measurements, verified or replayed by PCRs.

Each of the 24 PCRs in a TPM will be extended with multiple measurement events. The `pcr_extend` process involves taking the existing PCR value, concatenating with the new measurement hash, and then hashing the concatenated value to calculate the new PCR hash value. This means that each PCR value can be used as cryptographic evidence of the integrity of all system elements extended to that PCR, and it is impossible to "reverse" the PCR value into the individual measurement events.

## The Challenge of PCR Measurements

While PCR measurements provide valuable information about the system's integrity, the details of the measurement events leading to the final PCR values are hidden. This lack of transparency makes it difficult to create human-understandable attestation policies, or to pinpoint the exact cause of a mismatch between the expected and actual PCR values.

For example, PCR 7 includes measurements related to the UEFI configuration — the Secure Boot status, boot manager code, boot manager configuration, option ROM code, and option ROM configuration. If you were to create a policy asserting a specific value of PCR 7, you could verify the integrity of all of these elements. However, you would have no way to tell which specific element changed in the case of a mismatch. In a similar scenario, you might want to only verify the Secure Boot state and disregard the other measurements. This is not possible when asserting PCR values alone.

In addition, some PCRs contain "fragile" measurements. This "fragility" comes from measurements that might change on every boot, or that might be different between identically configured systems. This can create a frustrating situation where you want to verify the integrity of a component, but the PCR value is not sufficient by itself.

## Leveraging Event Logs

To address the limitations of relying solely on PCR values, attestation can include the use of event logs. These logs offer a comprehensive list of events measured for each PCR. By replaying the event log and comparing the result with the PCR value, you can verify the integrity of the log itself. Once the log integrity is verified, you can trust the individual elements measured. For example, you can assert that you want Secure Boot to be enabled in PCR 7. We don't need to specifically assert the PCR 7 value. Instead, we only assert the Secure Boot state in the policy, and verify the full PCR 7 event log during attestation. If the event log replay does not match the PCR, an error will be returned. If the event log replay matches the PCR, we can verify the event log content against a policy to ensure that the Secure Boot state is enabled.

## Benefits of Using Event Logs

Using TPM event logs instead of fragile PCR values offers several benefits:

1. **Selective Verification**: With event logs, you can choose specific elements of the system that you want to verify using policies. This allows you to focus on critical components, such as ensuring Secure Boot is enabled, without including unnecessary measurements.

2. **Enhanced Troubleshooting**: In the event of an attestation failure, event logs provide valuable insights into which specific system element was changed. This simplifies the troubleshooting process and enables quicker resolution.

3. **Human-Readable Information**: Event logs are designed to be more human-understandable compared to PCR values or complex TCG specifications. This makes it easier for users to interpret the measurements and understand the system's integrity status.

4. **Mitigating PCR Fragility**: One of the main challenges of TPM attestation is the fragility of PCR values. By relying on event logs for verification, you can effectively mitigate this issue and ensure a more reliable and consistent attestation process. In many such cases, you don't need to know the measurement value. Instead, you assert the event data that you want to verify, and let the event log replay verify the actual measurements.
