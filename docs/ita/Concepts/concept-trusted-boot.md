---
title: Measured Boot
description: Measured boot
author: mkwilbux
topic-type: conceptual
date: 07/22/24
uid: trusted.boot
---

*· 07/23/2024 ·*

## Trusted Platform Modules and Measured Boot

A Trusted Platform Module (TPM) is a chip that provides several security functions, including but not limited to securely storing and quoting platform measurements that help ensure the platform remains trustworthy. These platform measurements can be used as evidence in remote attestation to prove that the platform remains trustworthy.

A Virtual TPM (vTPM) provides the functions of a TPM in software (typically in the hypervisor), providing TPM functions to virtual machines.

System components (such as the UEFI/BIOS, OS kernel, boot loader, Secure Boot policy, etc) are measured before execution during the boot process, and these measurements can be used to detect any modifications or unauthorized changes to those measured components. These measurements, represented as cryptographic hashes, are stored in the TPM's Platform Configuration Registers (PCRs). Each new measurement _extends_ its corresponding PCR, where extension means to concatenate the previous PCR value with the new has, and then hash the result. This means that the value of a PCR can be used to ensure the integrity of all components measured in that PCR. 

The TPM can generate a signed _quote_ for use with a remote attestation verifier, such as Intel® Trust Authority. By attesting the TPM quote against a policy asserting expected system measurements, you can prove that the platform booted in a trustworthy state.

For more information about TPM, visit: [Trusted Computing Group: TPM Library Specification](https://trustedcomputinggroup.org/resource/tpm-library-specification/)

For details on the components measured by firmware during a measured boot, see the Trusted Computing Group [PC Client Platform Firmware Profile Specification](https://trustedcomputinggroup.org/resource/pc-client-specific-platform-firmware-profile-specification/).

## Trusted boot and Azure* confidential virtual machines(VM) with Intel® Trust Domain Extensions (Intel® TDX) and vTPM 

:::note
This feature is in pre-release status. For preview access, please contact your Intel sales representative. Details of implementation and usage may change before general availability.
:::

Microsoft Azure* implements Intel TDX and vTPM together, using an Intel TDX Trust Domain (TD) to protect the function of the vTPM. By combining attestation of the TD and vTPM, you can prove the authenticity and integrity of the vTPM and the VM image.

For example, PCR values from the vTPM can be used to ensure the integrity of the TD's UEFI BIOS, boot loader and kernel image.

Intel Trust Authority can be used as a Certificate Authority to issue [TPM Attestation Keys and Certificates (AK and AK certs)](../Attestation%20Technologies/Trusted%20Platform%20Module/tpm-ak-provision.md#physical-tpm-attestation-keys-and-certificates)

[Client TPM API Reference](../Integration/integrate-go-tpm.md)

[Attestation Client CLI](../Integration/integrate-go-tdx-cli.md)

[TPM Attestation Policies](../Concepts/concept-policy-v2.md#vtpm-appraisal-policy-example)