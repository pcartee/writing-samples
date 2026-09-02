---
title: Intel Trust Authority Attestation Client CLI
description: Provides an overview of Intel® Trust Authority Attestation CLI.
author: pcartee
topic: integration
date: 05/20/2025
uid: integrate.tdx.cli
---

*· May/20/2025 ·*

## Intel® Tiber™ Trust Authority Attestation Client CLI

Intel® Tiber™ Trust Authority includes an Attestation Client CLI that provides a command line interface for attesting various platforms. The CLI can be used manually, in scripts, and called by from application code when you don't want to (or can't) import the Intel Trust Authority Client packages into your project. The Attestation Client CLI exposes all the major functions in the client API. The CLI can be used by either the attester or a relying party.

Besides remote attestation, an important use case for the Attestation Client CLI is to collect reference measurements from a known-good environment. For example, you can build the confidential computing VM, install the CLI, and then use the CLI to collect evidence or request an attestation token from Intel Trust Authority. Then you would use evidence or token claims values as reference information for your own appraisal policies. 

The client CLI is built using the [Go language][golang] and is available in the [Intel Trust Authority Client for Go][trustauthority-client-for-go] repository. The client CLI is used to collect evidence from the underlying host and request attestation tokens from Intel Trust Authority The client CLI can also be used to verify Intel Trust Authority attestation tokens.

The following attestation technologies are supported:

* Intel® Trust Domain Extensions (TDX) for Intel TDX on-premises hosts (go-tdx), with or without TPM (go-tpm) composite attestation.
* Azure confidential VMs with Intel TDX (go-aztdx). Azure CVM vTPM (go-tpm) is supported for composite attestation. 
* Google Cloud Platform (GCP) confidential virtual machines (VMs) with Intel TDX. GCP CVMs use the same go-tdx adapter as on-prem Intel TDX hosts.
* NVIDIA H100 GPUs and composite attestation with an Intel TDX-based CVM. GPU attestation is currently in preview status.

Support for Azure and GCP CVMs with AMD SEV-SNP and vTPM is available on a limited preview status in the pilot environment only. For access to the pilot, contact your Intel representative. A pre-release version of the SEV-SNP adapter and Client CLI is available on [GitHub][sevsnp-preview]. 

## Simplified Installation (Linux)

The Intel Trust Authority Attestation client can be installed via bash scripts. The script will automatically install the correct dependencies and download the correct client CLI binary. These scripts support Ubuntu, SuSe, and Red Hat Enterprise Linux.

```sh
curl https://raw.githubusercontent.com/intel/trustauthority-client-for-go/main/release/install-tdx-cli.sh | sudo bash -
``` 
### Building the Intel Trust Authority Attestation Client CLI

For detailed build instructions, see the [client CLI Readme][tdxcli-repo-readme] on GitHub.

### Prerequisites

- Ubuntu 22.04 LTS, 24.04 LTS, or Red Hat Enterprise Linux (RHEL) 8.0 or newer. 
- [Go 1.22 or newer][go-download]
- Azure requires a customized OS distribution for confidential VMs. Ubuntu 22.04 (confidential VM) is available. 

## Configuration

You must configure certain properties before using the CLI. The properties and values are saved as JSON in `config.json`. The `config.json` requires the following properties:

```json
{
    "cloud_provider": "azure",
    "trustauthority_url": "https://portal.trustauthority.intel.com",
    "trustauthority_api_url": "https://api.trustauthority.intel.com",
    "trustauthority_api_key": "<trustauthority attestation api key>",
    "tpm": {
        "owner_auth": "",
        "ak_handle": "81000003",
        "pcr_selections": "sha1:10+sha256:all",
        "ak_certificate": "file:///home/user/akcert.pem",
    }
}
```

This example includes all possible properties, and it's not valid as-is. You can't use the "cloud_provider" and "ak_certificate" properties together.

This example includes all possible properties, and it's not valid as-is. You can't use the "cloud_provider" and "ak_certificate" properties together.

The `"cloud_provider":` is needed only for Microsoft Azure. Omit this setting for all other Intel TDX platforms.

The `tpm` section is needed only if you're using the TPM. `Owner_auth` is the TPM owner password and ak_handle is the TPM attestation key handle. For Azure CVM attestation only, the owner_auth is an empty string and the `ak_handle` is hardcoded to 81000003, which is the location of the Azure-provisioned AK in the vTPM. Note that you can't provision an AK on a vTPM, and the "ak_certificate" property is only valid with physical TPMs. However, you can set the ak_handle property for physical TPM.

`pcr_selections` is the list of PCRs to include in the quote. By default, PCR selections include all 24 SHA256 PCRs. However, if you intend to collect [IMA logs](../Attestation%20Technologies/Trusted%20Platform%20Module/tpm-ima-logs.md), you must include the SHA1 PCR 10 to enable event replay for IMA. Although TPM support no longer requires tpm2-tools, the [PCR bank specifier][pcr-bank-spc] format is still used.

For more information about PCRs, see the [Trusted Computing Group Firmware Profile Specification][tpm-spec]

`ak_certificate` is the path to the AK certificate. This setting is needed only if you're using a physical TPM. The AK certificate is generated by Intel Trust Authority and is used to verify the TPM quote signature. The AK certificate is written to stdout when the `provision-ak` command is run. The AK certificate must be saved to a file and the path to the file must be specified in the `config.json` file. For more information, see [Physical TPM Attestation Keys and certificates](../Attestation%20Technologies/Trusted%20Platform%20Module/tpm-ak-provision.md).

## TPM evidence

The **token** and **evidence** commands are able to use the **go-tpm** adapter to collect evidence from a TPM. Not all trust domains have access to a TPM, and vTPM implementations differ. How you use the `--tdx` and `--tpm` flags depends on the platform:

    - Azure CVMs with Intel TDX use Intel TDX measurements to back the integrity of the virtual TPM quote. You can't collect only vTPM evidence on Azure. To collect vTPM evidence in Azure, you must specify both the `--tdx` and `--tpm` flags for the **token** and **evidence** commands.

    - Physical TPMs and Google Cloud Platform (GCP) vTPMs allow you to collect only TPM evidence, and the TPM quote is verified by Intel Trust Authority and an attestation token is returned. On these platforms, you can use either or both the `--tdx` and `--tpm` flags, depending on what type(s) of evidence you want to collect.

An attester can improve their security posture by collecting evidence from as many relevant attestable technologies as possible. You should collect and appraise evidence from both Intel TDX and a TPM when both are available. Intel TDX helps ensure the integrity and isolation of the virtualized environment. The TPM helps to validate the integrity of the host system. When combined with UEFI, CCEL, and IAM logging as described below, a "chain of trust" from the hardware to the CVM can be established even in a cloud environment.

## Event logs

The token and evidence commands have parameters you can use to include measurements from system event logs UEFI, IMA, and CCEL in the evidence collected from the TEE or TPM. User and group permissions must be set to allow read access to the relevant event logs, as described below.

### CCEL (--ccel)

If the `--ccel` flag is included, evidence is collected from the confidential computing event log (CCEL) and included in the quote. **The user account must have read access to the following files**: `/sys/firmware/acpi/tables/ccel` and `/sys/firmware/acpi/tables/data/ccel`.

The CCEL is similar to the UEFI TPM logs, except that the boot measurements are extended to the Intel TDX RTMRs in addition to the TPM PCRs. For more information, see [Section 38](https://uefi.org/specs/UEFI/2.10/38_Confidential_Computing.html) of the UEFI 2.10 specification.

### IMA (--ima)

To include IMA logs in evidence (--ima), the user collecting TPM evidence must have read access to `/sys/kernel/security/ima/ascii_runtime_measurements`. You must also grant read access to this file for the **tss** group by using the following commands:

```bash
sudo chgrp tss /sys/kernel/security/ima/ascii_runtime_measurements
sudo chmod g+r /sys/kernel/security/ima/ascii_runtime_measurements
```
### UEFI (--evl)

If `--evl` is included, the user collecting TPM evidence must have read access to `/sys/kernel/security/tpm0/binary_bios_measurements`. You must also grant read access to this file for the **tss** group by using the following commands:

```bash
sudo chgrp tss /sys/kernel/security/tpm0/binary_bios_measurements
sudo chmod g+r /sys/kernel/security/tpm0/binary_bios_measurements
```


## Using the Intel Trust Authority Attestation Client CLI

The **trustauthority-cli** exposes the following commands that can be used from the command line or in applications. A list of all the commands can obtained by typing `trustauthority-cli --help` at the command line. To get help for a specific command, type `trustauthority-cli <command> --help`.

:::note
Valid characters in the CLI include numbers 0 through 9, upper and lowercase English characters, underscore (_), colon (;), period (.), slash (/), and dash (-).
:::

**In this section**

[**decrypt**](#decrypt) Decrypts an encrypted blob using the private key passed as input.

[**create-key-pair**](#create-key-pair) Creates an RSA3k key pair.

[**evidence**](#evidence) Gets evidence from the TEE or TPM.

[**provision-ak**](#provision-ak) Provisions a host's physical TPM with an attestation key (AK) signed by Intel Trust Authority.

[**provision-ak**](#provision-ak) Provisions a host's physical TPM with an attestation key (AK) signed by Intel Trust Authority.

[**token**](#token) Gets an attestation token from Intel Trust Authority.

[**verify**](#verify) Verifies a signed Intel Trust Authority attestation token.

[**version**](#version) Shows the version and build date of the client CLI.

### token

The `token` command fetches an attestation token from Intel Trust Authority. The token command also accepts optional policy IDs as input for verification. In the current client CLI version, the `--tdx` flag must be used for Azure attestation. TPM-only attestation isn't supported.

```bash
trustauthority-cli token --config <config-file-path> [--user-data <user-data>] [--policy-ids <policy IDs>] [--pub-path <path to public key>] [--request-id <request id>] [--tdx ] [--tpm ] [--no-verifier-nonce ] [--token-signing-alg RS256|PS384] [--policy-must-match] [--ima] [--evl] [--ccel]
```

#### Required Parameters

**`--config -c`** <br /> A path to the configuration file in JSON format. If no path is specified, the CLI looks for the file in the directory where the `trustauthority-cli` is installed.

#### Optional Parameters

**`--user-data -u`** <br /> User data in base64|base64url-encoded format. Maximum 1Mb.

**`--policy-ids -p`** <br /> A comma-separated list of one or more policy IDs.

**`--pub-path -f`** <br /> A public key to be included as user data.

**`--request-id -r`** <br /> A user-supplied request ID to associate with the request.

**`--token-signing-alg  -a`** <br /> The algorithm to use for signing the token. Can be "RS256" or "PS384" (default).

**`--policy-must-match`** <br /> The token will be issued only if all policies match. By default (if this flag is not included), a token is issued even if one or more appraisal policies fail.

**`--tdx`** <br /> Use the TDX adapter to collect evidence. See [TPM evidence](#tpm-evidence) for details.

**`--tpm`** <br /> Use the TPM adapter to collect evidence. See [TPM evidence](#tpm-evidence) for details.

**`--no-verifier-nonce`** <br /> Don't include a verifier nonce in the evidence.

**`--ima`** <br /> If set, the TPM evidence will include IMA measurements. See [Event logs](#event-logs)), above.

**`--evl`** <br /> TPM evidence will include the UEFI event logs. See [Event logs](#event-logs)), above.

**`--ccel`** <br /> Confidential computing event logs (CCEL) will be collected with the evidence. See [Event logs](#event-logs)), above.

---

### evidence

The `evidence` command collects evidence from the underlying host and displays it in JSON format. The evidence values can be used in policy, or the JSON output can be used as the body of a request to the Intel Trust Authority API. Multiple evidence types can be collected by using the `--tpm` and `--tdx` flags. At least one of these flags must be set. 

```sh
trustauthority-cli evidence --config [--tpm] [--tdx] [--no-verifier-nonce] [--user_data <user-data>] [--policy-ids <policy IDs>] [--token-signing-alg RS256|PS384] [--policy-must-match] [--ima] [--evl] [--ccel]
```


#### Required Parameters

**`--config  -c`** <br /> Path to the configuration file.

**`--tpm`** <br /> Use the TPM adapter to collect evidence. See [TPM evidence](#tpm-evidence) for details.

**`--tdx`** <br /> Use the TDX adapter to collect evidence. See [TPM evidence](#tpm-evidence) for details.

#### Optional Parameters

**`--no-verifier-nonce`** <br /> Don't include a verifier nonce in the evidence.

**`--user-data`** <br /> User data in base64|base64url-encoded format. Maximum 1Mb.

**`--policy-ids`** <br /> A comma-separated list of one or more policy IDs.

**`--token-signing-alg`** <br /> The algorithm to use for signing the token. Can be "RS256" or "PS384" (default).

**`--policy-must-match`** <br /> The token will be issued only if all policies match. By default (if this flag is not included), a token is issued even if one or more appraisal policies fail.

**`--ima`** <br /> TPM evidence will include IMA measurements.

**`--evl`** <br /> TPM evidence includes UEFI event logs.

**`--ccel`** <br /> Confidential computing event logs are collected with the evidence.

### decrypt

The `decrypt` command is used to decipher the encrypted string using the private key passed as input. The `decrypt` command takes the private key location and encrypted blob as input and writes the decrypted data either to stdout or to the output file if passed as an argument. The encrypted blob must be passed as base64|base64url encoded string. The decrypted blob is written to stdout.

`trustauthority-cli decrypt --key <private key>|--key-path <path to private key> --in <blob>`

#### Required parameters

**`--key  -k`** <br /> Base64|base64url-encoded private key. One of `--key` OR `--key-path` is required.

**`--key-path  -f`** <br /> Path to a private key file.

**`--in`** <br /> Base64|base64url-encoded encrypted blob.

### create-key-pair

The `create-key-pair` command is used to generate an RSA3k key pair. The public key is written to a `public-key.pem` file in the path specified by the `--pub-path` parameter. The private key is written to stdout.

`trustauthority-cli create-key-pair --pub-path <public key file path>`

#### Required parameters

**`--pub-path  -f`** <br /> Path to public key file. Required.

### provision-ak

The `provision-ak` command provisions the host's physical TPM with an attestation key (AK) signed by Intel Trust Authority. This command cannot be used with virtual TPMs. The `config.json` file "tpm" section must be configured as described in [Configuration](#configuration), above.

`trustauthority-cli provision-ak 

### provision-ak

The `provision-ak` command provisions the host's physical TPM with an attestation key (AK) signed by Intel Trust Authority. This command cannot be used with virtual TPMs. The `config.json` file "tpm" section must be configured as described in [Configuration](#configuration), above.

`trustauthority-cli provision-ak 

### verify

The `verify` command validates a signed Intel Trust Authority attestation token. This command requires the **trustauthority_url** property in the `config.json` file.

`trustauthority-cli verify --config <config.json> --token <attestation token in JWT format>`

#### Required parameters

**`--config  -c`** <br /> Configuration file.

**`--token  -t`** <br /> Intel Trust Authority attestation token in base64-encoded format.

### version

Displays the version and build date of the client CLI.  

`trustauthority-cli version`


/* External URLs */
[amber-tdx-cli]: https://github.com/intel/trustauthority-client-for-go/tree/main/tdx-cli
[go-download]: https://go.dev/dl/
[golang]: https://go.dev/
[trustauthority-client-for-go]: https://github.com/intel/trustauthority-client-for-go/tree/main
[tdxcli-repo-readme]: https://github.com/intel/trustauthority-client-for-go/blob/main/tdx-cli/README.md
[sevsnp-preview]: https://github.com/intel/trustauthority-client-for-go/tree/azure-sevsnp-preview
[pcr-bank-spc]: ttps://tpm2-tools.readthedocs.io/en/latest/man/common/pcr/
[pcr-spec]: https://trustedcomputinggroup.org/wp-content/uploads/TCG_PCClientSpecPlat_TPM_2p0_1p04_pub.pdf
