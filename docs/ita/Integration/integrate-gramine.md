---
title: Gramine Integration
description: Understanding Gramine integration with Intel® Trust Authority.
author: grminch, mkwilbux
topic: integrate
date: 06/04/2024
uid: integrate.gramine
---
import Gramine from '../Include/_code-gramine-client.md';

## Gramine integration

Gramine is a library OS that provides a means to host application-facing code from the operating system kernel. Using a platform adaptation layer (PAL) in which to operate, Gramine supports unmodified applications that run inside an [Intel® SGX](../Attestation%20Technologies/concept-tees-overview.md) enclave. This means there is minimal development needed to run the application from within a Gramine environment. Instead of having to rewrite code to run the application in a different environment, Gramine encapsulates the code in a container in an Intel® SGX enclave. This makes it much easier for customers to adopt Intel® SGX without rewriting the core application code.

The Gramine Library OS provides tool kits to help include customer workloads in Gramine Shielded Containers (GSC). GSC protects a customer’s workload by utilizing the secure hardware features enabled by Intel® SGX.  

To facilitate attestation from Intel Trust Authority using Gramine, a fork of the Gramine Project includes the Intel Trust Authority client. This enables applications to perform attestation with Intel Trust Authority with minimal changes to the customer application.

## Gramine Intel Trust Authority architecture and device files 

The Intel Trust Authority client is integrated as part of a forked Gramine project's library OS. Figure 1 illustrates the architecture and how the user application interacts with it in a [passport attestation model](../Concepts/concept-patterns.md#workflows).  

![Intel Trust Authority Gramine client architecture](../../../Static/img/integrations/gramine-integration.png)

### Gramine Intel Trust Authority client architecture

The Intel Trust Authority fork of Gramine provides a set of pseudo-device files an application uses to trigger the attestation flow with Intel Trust Authority service. The attestation flow is transparent to the application, as illustrated in Figure 1. The application reads the device file `/dev/amber/token` to get an attestation token from Intel Trust Authority. The Intel Trust Authority client performs the following steps to help the application attest with Intel Trust Authority.

1. User application reads `dev/amber/token`. Reading this device file triggers the attestation process.
1. The Intel Trust Authority client is triggered to collect an Intel® SGX quote from the quoting enclave, and then forwards the quote to Intel Trust Authority service for verification.
1. Intel Trust Authority verifies the quote and returns an attestation token if the quote is successfully verified. The Intel Trust Authority client writes the token to a device file. 
1. The application reads the token from the device file and then forwards the token to the relying party with a request for a protected resource. 
1. The relying party applies its own appraisal policy to the token, and if all is well, it returns the requested resource to the application.


### Gramine Intel Trust Authority client pseudo-device files

The Intel Trust Authority client branch of Gramine exposes device files that user applications can use to get status and configure endpoints.

**`/dev/amber/token`** — Reading this file triggers a new attestation request to Intel Trust Authority, and then reads the resulting attestation token response.  

**`/dev/amber/endpoint_apikey`** — This file contains the attestation [API key](../Quickstart/tutorial-api-key.md) used for Intel Trust Authority attestation. The application must write the API key to this file, and the Intel Trust Authority client will use it for future attestation requests.

**`/dev/amber/status`** — This file contains the status of the client connection to Intel Trust Authority and is updated whenever a new attestation attempt is made.

**`/dev/amber/endpoint_url`** — The Gramine library OS does not innately support DNS resolution, and so the Intel Trust Authority URL and IP address must be configured for the client to function. Write the Intel Trust Authority service base URL (https://projectamber.intel.com/) to this file.

**`/dev/amber/endpoint_ip`** — The Gramine library OS does not innately support DNS resolution, so that the Intel Trust Authority URL and IP address must be configured for the client to function. Write the Intel Trust Authority service IP address to this file.

## Cloud deployment using Gramine

Azure Confidential Computing Services support Intel® SGX and are available to provide virtual machines capable of supporting Intel® SGX attestation. The Gramine Project offers [instructions for compiling the Gramine OS for use on Azure](https://gramine.readthedocs.io/en/stable/cloud-deployment.html) with a sample application. 

To build Gramine with the Intel Trust Authority client pre-installed, use the Intel Trust Authority fork instead of the main Gramine version branch, as shown in the following example.

```bash
$ git clone --depth 1  https://github.com/gramineproject/gramine.git
$ cd gramine
$ git fetch origin pull/1065/head:amber_pr_kbs
$ git checkout amber_pr_kbs
```

## Gramine Shielded Containers

The Gramine Project maintains a separate project called Gramine Shielded Containers, which provides a tool to convert existing container images into a so-called _graminized_ image. Graminization provides the simplest possible migration of an existing container-based application to an SGX-enabled Gramine application. 

For more information, see the [Gramine Shielded Containers synopsis](https://gramine.readthedocs.io/projects/gsc/en/latest/).

To add the Intel Trust Authority client, update the `config.yaml` file to set the Intel Trust Authority client branch before building the GSC tool, as shown in the following code.

```bash
# Specify the OS distro. Currently tested distros are
# ``ubuntu:18.04``, ``ubuntu:20.04``, ``ubuntu:21.04`` and ``centos:8``.
Distro: "ubuntu:18.04"

# If the image has a specific registry, define it here.
# Empty by default; example value: "registry.access.redhat.com/ubi8".
Registry: ""

# If you're using your own fork and branch of Gramine, specify the GitHub link and the branch name
# below; for Intel Trust Authority, use the values in the sample below:
Gramine:
    Repository: "https://github.com/bigdata-memory/gramine.git"
    Branch:     "amber_pr"

# Specify the Intel SGX driver installed on your machine (more specifically, on the machine where
# the graminized Docker container will run); there are several variants of the SGX driver:
#
#   - legacy out-of-tree driver: use something like the below values, but adjust the branch name
#         Repository: "https://github.com/01org/linux-sgx-driver.git"
#         Branch:     "sgx_driver_1.9"
#
#   - DCAP out-of-tree driver: use something like the below values
#         Repository: "https://github.com/intel/SGXDataCenterAttestationPrimitives.git"
#         Branch:     "DCAP_1.11 && cp -r driver/linux/* ."
#
#   - DCAP in-kernel driver: use empty values like below
#         Repository: ""
#         Branch:     ""
#
SGXDriver:
    Repository: ""
    Branch:     ""
```

## Gramine container integration

The Gramine Project maintains a [base Gramine Docker image](https://hub.docker.com/r/gramineproject/gramine) at DockerHub. This Gramine image is a minimal collection of the essential Gramine binaries and tools. It still requires Intel® SGX support on the underlying virtual machine or physical server host (including DCAP drivers). The image **does not** contain the Intel Trust Authority client. This option can be used to handle the Intel® SGX enclave implementation if the [Intel Trust Authority client](integrate-go-client.md) is added to the customer application.

For more information, see the [Gramine Container integration documentation](https://gramine.readthedocs.io/en/stable/container-integration.html).

## Update the manifest workload

Change the manifest file of the target workload by configuring the following Intel Trust Authority related settings:

```bash
# dummy configuration for Intel Trust Authority
# please replace the IP with real IP of Intel Trust Authority endpoint
sgx.amber_ip = "127.0.0.1"
sgx.amber_url = "https://api.trustauthority.intel.com/appraisal/v1/"
sgx.amber_apikey = ""

# dummy configuration for KBS provided by Intel Trust Authority
# the public key component of a 2048-bit RSA key for secret wrapping
sgx.amber_userdata = "5wISSLU3UP0vZ8G+pgkO3BhhRAtdcY22UMomtdQabSxlA=="
sgx.kbs_ip = "127.0.0.1"
sgx.kbs_url = "https://127.0.0.1:9443/kbs/v1/keys/"
sgx.kbs_keyid = "ae6281b3-e4fe-3db5-82fd-eed40f6e4f18"
```

:::note
If you are in the European Union (EU) region, use the following Intel Trust Authority URLs:

`sgx.amber_url = "https://api.eu.trustauthority.intel.com/appraisal/v1/" `
:::

## Gramine Intel Trust Authority client code samples 

The code sample (in Go) below demonstrates using the pseudo device files exposed in the Gramine project fork to interact with Intel Trust Authority.

<Gramine />
