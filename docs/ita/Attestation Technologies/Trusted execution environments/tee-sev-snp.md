---
title: AMD SEV-SNP
description: A brief introduction to SEV-SNP.
author: pcartee
topic: conceptual
date: 05/20/2025
uid: tee.sev.snp
---

*· 05/20/2025 ·*

## AMD* Secure Encrypted Virtualization — Secure Nested Paging (AMD* SEV-SNP)

:::note
This feature is in pre-release status. For preview access, please contact your Intel sales representative. Details of implementation and usage may change before general availability.
:::

AMD* Secure Encrypted Virtualization — Secure Nested Paging (AMD* SEV-SNP) provides a secure computing environment for virtual machines by isolating them from the hypervisor and other VMs on the host system. This allows for the creation of hardware-isolated virtual machines.

Read more about [AMD* SEV-SNP](https://www.amd.com/en/developer/sev.html).

### AMD SEV-SNP driver support in the kernel

AMD* SEV-SNP requires driver support at the kernel level. For Linux, this support requires a development kernel with IOMMU enabled in the BIOS, as the SNP patches have not been merged into the main Linux kernel.

See [AMDSEV](https://github.com/AMDESE/AMDSEV/blob/snp-latest/stable-commits) for more information on kernel support.

 A signed attestation report validates the state and identity to ensure it is genuine AMD hardware. Attestation provides confidence in the guest configuration, launch, and platform configuration.

 AMD* SEV-SNP attestation uses [V2 Policies](../../Concepts/concept-policy-v2.md) and a new [V2 appraisal API endpoint.](../../Restapi/restapi-attestation-v2.md).

---
## Next steps

Intel SGX primary resources:

- [Intel Trust Authority Client Tutorial for Azure with vTPM and Intel TDX](../../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-azure-vtpm.md)
- [Intel Trust Authority Client Tutorial - Intel SGX Attestation on Microsoft Azure](../../Tutorials%20and%20examples/Intel%20Trust%20Authority%20Client%20examples/tutorial-sgx.md)

**\*** Other names and brands may be claimed as the property of others.


[text](<../../Tutorials and examples/Intel Trust Authority Client examples/tutorial-amd-azure-vm.md>)