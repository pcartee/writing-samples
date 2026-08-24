---
title: GPU remote attestation with Intel® Trust Authority
description: Learn about the Intel® Trust Authority Python Client, CLI for Intel TDX and NVIDIA GPU, and Intel Trust Authority REST API that support GPU attestation.
author: pcartee
topic: conceptual, attestation, gpu
date: 09/17/2024
uid: gpu.attestation
---
import BasicToken from '../../Include/eat/_nv-basic-token.md';
import NVIDIA from '../../Include/eat/_nvidia-policy-claims.md';

*· September/17/2025 ·*

## GPU remote attestation with Intel® Trust Authority

Intel and NVIDIA have collaborated to add NVIDIA\* Tensor Core\* H100 GPU TEE remote attestation to Intel® Trust Authority. It's now possible to attest a confidential virtual machine TEE and a NVIDIA H100 GPU in one composite attestation workflow. This article provides an overview of the GPU attestation architecture, the Intel Trust Authority PythonS Client, CLI, and REST API updates that support GPU attestation, and examples of GPU and composite attestation JWTs.

:::note
This release supports on-premises hardware only. Cloud-based GPU attestation is not supported at this time, however, it is planned for a future release.
:::

The GPU as a TEE is a relatively new concept that extends the capabilities of a CPU TEE. Generative artificial intelligence (GAI) and other demanding workloads require hardware acceleration with a GPU to achieve acceptable performance. Many GAI models and parameters are themselves highly-valued intellectual property, and they often process sensitive data. The GPU TEE provides a secure execution environment for these workloads, helping to ensure that the data is protected from unauthorized access or tampering. 

However, a GPU on its own is not a complete TEE for confidential computing. The GPU confidential compute solution relies on a confidential VM CPU TEE, enabled by Intel® Trust Domain Extensions (Intel® TDX) 1.x on Intel CPUs. The CPU TEE provides the measurements and attestations needed to establish trust in the GPU. The CPU TEE serves as an orchestrator for securely transferring information to the GPU. This is done through a fully encrypted process. The GPU and confidential VM exchange keys to create an encrypted communications channel. 

The Intel Trust Authority Python Client, CLI for Intel TDX and NVIDIA GPU, and Intel Trust Authority REST API currently support two GPU attestation options.

1. Composite CPU TEE + GPU TEE attestation. The Intel Trust Authority client collects separate evidence from the confidential VM TEE and the GPU driver. The evidence is combined and sent to Intel Trust Authority for verification. Intel Trust Authority verifies the CPU evidence, and the GPU quote is sent to NVIDIA Remote Attestation Service (NRAS) for verification. The resulting attestation JWT issued by Intel Trust Authority contains CPU TEE claims and GPU claims, and other claims from the Intel Trust Authority SaaS service. Composite attestation is the preferred method for confidential computing solutions that include a GPU TEE.
1. GPU-only attestation using the Intel Trust Authority client. As described above, GPU-only attestation doesn't provide a complete confidential computing solution.

## GPU attestation architecture

The following diagram is a high-level view of the GPU attestation architecture. The focus is on the relationship among the major components and actors (attester, verifier, & relying party).

![Intel TDX and NVIDIA GPU attestation architecture diagram](/img/gpu-attestation/gpu_attestation_arch.png)

The attester comprises the confidential computing (CC) app and related software running in the TD, the Intel TDX-enabled host server, and an NVIDIA GPU (local or remote).

There are two independent verifiers: Intel Trust Authority SaaS service, and NVIDIA Remote Attestation Service (NRAS). NRAS verifies the GPU TEE by comparing the evidence collected from the driver with the so-called "golden measurements" stored in the NVIDIA Reference Integrity Manifest\* (RIM) service. 

GPU attestation begins when the Intel Trust Authority client GPU TEE adapter calls the NVIDIA SDK API to request evidence for the GPU. The GPU evidence is provided by the NVIDIA GPU driver running on the server where the GPU is installed. The GPU server can be local or remote, but the GPU driver must be running on the same server as the GPU.

When composite attestation (option 1 and 1a on the diagram) is requested, independent evidence is collected for both the Intel TDX TD and the NVIDIA H100 GPU. When an attestation request is made, Intel Trust Authority SaaS verifies the Intel TDX quote as usual and forwards the GPU evidence to the NRAS GPU verification service. 

Intel Trust Authority extracts the NRAS JWT from the NRAS API response body, verifies the NRAS JWT certificate, and returns the NRAS JWT embedded as a JSON sub object in the JWT. This method is called _composite_ attestation because it relies on multiple verifiers and and the attestation result includes claims from more than one TEE or device.

:::note
When composite attestation with a NVIDIA GPU is requested, the Intel Trust Authority service relies on NRAS to to verify the GPU quote and return a JWT. If NRAS is experiencing uneven performance, timeouts, or is unavailable, an error will occur and Intel Trust Authority won't return an attestation token. If service delay is lengthy, the verifier nonce may expire before an attestation request can be completed. It is recommended to include retry logic in the client application to handle these situations.
:::

When GPU-only attestation (option 2 on the diagram) is requested, the Intel Trust Authority Python Client GPU adapter collects GPU evidence, generates a nonce in NVIDIA 32-byte Hex format, and then sends an attestation request to Intel Trust Authority. Intel Trust Authority's GPU verification sends a request to NVIDIA NRAS to verify the GPU evidence. The NRAS JWT cert is verified, and then the NRAS JWT claims are copied to the `"nvgpu":{}` section of the JWT issued by Intel Trust Authority.

Composite attestation of both the CPU TEE and the GPU TEE provides a more secure confidential computing solution than GPU-only attestation. The trust model of a GPU TEE relies on the CPU TEE to establish trust in the GPU, and to manage data flow and computations on the secure channel between the CPU and GPU.

## Python client

NVIDIA GPU attestation is supported by the Intel Trust Authority Python Client. The client includes a GPU adapter that collects evidence from the NVIDIA GPU driver (running on the server where the GPU is installed) and sends it to Intel Trust Authority for verification.

:::note
Intel TDX and NVIDIA GPU attestation requires Ubuntu 24.04 LTS with Linux kernel 6.8 or later.
:::

The **ITAConnector.get_token_v2** method supports both singular (Intel TDX _or_ GPU) and composite (Intel TDX + NVIDIA H100) attestation. 

```python
def get_token_v2(self, tdx_args: GetTokenArgs, gpu_args: GetTokenArgs) -> GetTokenResponse:
```

You must supply at least one of either `tdx_args` or `gpu_args` to **get_token_v2**. If both are supplied, the client will request a composite attestation. 

An **ITAConnector.get_token** method is available for singular attestation of Intel TDX and Intel SGX. **get_token** doesn't support GPU or composite attestation.

## Python CLI

Intel® Trust Authority Python CLI for Intel® Trust Domain Extensions (Intel® TDX) and NVIDIA GPU **trustauthority-pycli** provides a CLI to attest an Intel TDX trust domain (TD) and NVIDIA GPU with Intel Trust Authority. 

**trustauthority-pycli** requires **`python-connector`**, **`python-intel-tdx`**, **`python-nvgpu`**, and NVIDIA Attestation SDK. A configuration file is required to be present in the **trustauthority-pycli** directory. See the README for details and more extensive documentation of the following commands.

**trustauthority-pycli** has three commands: **attest**, **evidence**, and **verify**. 

:::note
Root permissions are required to access the configfs-tsm device to collect evidence for Intel TDX attestation. You must run both **attest** and **evidence** commands as root. For example: `sudo python3 trustauthority-pycli attest --attest_type tdx+nvgpu`.  GPU-only attestation doesn't require sudo.
:::

The **attest** command collects evidence from the attester(s) and then forwards the evidence with an attestation request to Intel Trust Authority. `attest` requires an `--attest_type` parameter that can be one of `tdx`, `nvgpu`, or `tdx+nvgpu`. The `tdx+nvgpu` option is used for composite attestation of both the Intel TDX TD and the NVIDIA H100 GPU. 

The **evidence** command is used to collect evidence from Intel TDX, the GPU driver or both, and optionally saving evidence to a file. **evidence** supports the background-check attestation model, and it's helpful for development and testing. 

The **verify** command is used to verify an attestation token from Intel Trust Authority.  **verify** takes a JWT as input, then checks the iss signing certs, CRL, and expiration date.

## REST API updates

GPU and Intel TDX + GPU attestation uses the `/appraisal/v2/attest` endpoint of the Intel Trust Authority REST API. 

## GPU JWT example

The following sample shows a basic NVIDIA GPU attestation token as returned from NRAS.

<BasicToken />

## Composite JWT example

The following sample JWT is the result of a composite attestation with an Intel TDX TD and a NVIDIA H100 GPU. Notice that each of the embedded JWTs is a sub object that is identified with "intel_tee" and "nvidia_gpu".

<NVIDIA />

## Claims usable in policy

Not all claims in the JWT can be used in an appraisal policy. The following sample shows a NVIDIA GPU attestation token with claims that can be used in a policy. Claims not shown here are either informational or not intended for use in policy.

<NVIDIA />

This particular token shows a mixed result; the attestation report is valid, but the GPU measurements don't match. The mismatched measurements are identified in the `x-nvidia-mismatch-measurement-records` and `x-nvidia-mismatch-indexes` claims. A relying party can examine these claims to determine if the GPU is still within acceptable limits for use, or if it should be quarantined or taken offline.

## Example appraisals

This section includes sample appraisal policies that can be used to verify the GPU attestation results. Most of these examples are really fragments meant to be combined for a complete GPU or composite policy. For more information about appraisal policies, see the [Appraisal Policy V2](../../Concepts/concept-policy-v2.md) article.

### Secure boot

Policy that checks whether Secure Boot\* is enabled and all GPU measurements are matched

```rego

default match := false

match {
    input.nvgpu.secboot == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-measurements-match"] == true
}
```

### Validate attestation report

Policy that checks whether the attestation report is valid. 

```rego
default match := false

match {
      input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-cert-chain-validated"] == true
      input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-parsed"] == true
      input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-attestation-report-signature-verified"] == true
}

 ```

### GPU driver RIM

Policy that checks whether the GPU driver RIM is available and valid.

```rego
default match := false

match {    
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-validated"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-schema-fetched"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-signature-verified"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-cert-validated"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-driver-rim-driver-measurements-available"] == true
}

```

### GPU VBIOS RIM

Policy that checks whether the VBIOS RIM is available and valid.

```rego
default match := false

match {    
    input.nvgpu["x-nvidia-attestation-detailed-result"]['x-nvidia-gpu-vbios-rim-measurements-available'] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]['x-nvidia-gpu-vbios-rim-schema-fetched'] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-cert-validated"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-schema-validated"] == true
    input.nvgpu["x-nvidia-attestation-detailed-result"]["x-nvidia-gpu-vbios-rim-signature-verified"] == true
}
```

### GPU hardware info

Policy that checks the GPU HW information (e.g. Driver and VBIOS information). To use this, you need to know the specific values that apply to your GPU. 

This example is written in policy v2 format; for more information, see [Attestation Policies v2](../C
oncepts/concept-policy-v2.md).

```rego

import rego.v1

default match := false

match if {    
    input.nvgpu["x-nvidia-gpu-driver-version"] == "535.104.05"
    input.nvgpu.hwmodel == "GH100 A01 GSP BROM"
    input.nvgpu[x-nvidia-gpu-vbios-version"] == "96.00.5E.00.01"
}

```

**\*** Other names and brands may be claimed as the property of others.