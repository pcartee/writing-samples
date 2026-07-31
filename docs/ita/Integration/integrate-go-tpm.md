---
title: Intel Trust Authority TPM API Reference
description: This article provides an API reference for the Intel Trust Authority Go TPM adapter.
author: grminch
topic: integration
date: 07/22/2024
uid: tpm.api.reference
---

*· 07/22/2024 ·*

## Intel® Trust Authority TPM API Reference

:::note
This feature is currently in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Intel Trust Authority pilot environment. Contact your Intel representative for access.
:::

This article provides an API reference for the Intel® Trust Authority Go TPM adapter. The adapter provides a set of APIs for interacting with a TPM. The adapter can be used to read and write NV indexes, read PCRs, and get quotes from the TPM. 

In this preview release the adapter supports Microsoft Azure\* confidential virtual machines with Intel® Trust Domain Extensions (Intel® TDX) and vTPM 2.0. Future releases may support physical TPMs and other platforms.

The preview TPM adapter supports composite attestation only. That is, vTPM + Intel TDX. You can't attest the vTPM by itself. The TPM adapter is used to get evidence from the vTPM. The evidence is endorsed by the Azure-provided AK, which is contained in the Intel TDX quote's runtime data. The Azure CVM with Intel TDX adapter is used to get evidence from the Intel TDX trust domain TEE. The evidence from the vTPM and the Intel TDX is combined for composite attestation.

### Prerequisites

- Go 1.22 or later
- Tpm2-tools must be installed on the confidential VM.

### Terms and definitions

The following acronyms and terms are used in this article. For more information about TPM terms, see the [Trusted Computing Group TPM 2.0 Library](https://trustedcomputinggroup.org/resource/tpm-library-specification). Part 1: Architecture, Section 4: Terms and Definitions.

| Term | Definition |
| --- | --- |
| AK | Attestation Key. The public AK is used to sign evidence quotes collected from the TPM. The AK for a physical TPM is normally provisioned by the user and written to the TPM. In the case of a vTPM, the Azure "paravisor" provisions an AK for you.|
| EK | Endorsement Key. The EK is unique for every TPM. The public EK is used by verifiers and relying parties to establish trust in the TPM. The EK is not used to sign quotes.|
| Handle | A 32-bit reference to an object in the TPM. Handles are assigned by the TPM and are used to reference objects in the TPM. For more information, see [Registry of Reserved TPM 2.0 Handles and Localities](https://trustedcomputinggroup.org/wp-content/uploads/RegistryOfReservedTPM2HandlesAndLocalities_v1p1_pub.pdf), published by the Trusted Computing Group.|
| NV | Non-volatile data storage. NV memory stores persistent state associated with the TPM. Some storage is allocated for use by the platform. |
| NV index | A reference to a location in NV memory. For more information see TPM 2.0 Library [Part 2: Structures](https://trustedcomputinggroup.org/wp-content/uploads/TPM-2.0-1.83-Part-2-Structures.pdf) , section 13 "NV Storage Structures." |
| PCR | Platform Configuration Register. |
| TPM | A physical Trusted Platform Module, which can be either a discrete device or a component of the CPU. |
| vTPM | A virtual Trusted Platform Module. A vTPM exists in software but provides functions and security similar to a physical TPM. In this document, TPM is used as a catch-all term. vTPM is used only when the distinction between a physical and virtual TPM is important. |

## TPM adapter APIs

The following APIs are provided by the Intel Trust Authority Go TPM adapter. This list is loosely grouped by functional area. 

### Certificates and keys

[**ReadPublic**](#readpublic) <br /> Reads the public key for an AK in the TPM.

[**GetEKCertificate**](#getekcertificate) <br /> Gets the EK certificate from the TPM.

### Evidence and quotes

[**GetEvidence**](#getevidence) <br /> Collects evidence from the TPM.

[**GetEvidenceIdentifier**](#getevidenceidentifier) <br /> Gets the evidence identifier for the TPM.

[**GetPcrs**](#getpcrs) <br /> Reads the PCRs from the TPM.

[**GetQuote**](#getquote) <br /> Gets a quote from the TPM. The quote is signed by the AK.

[**WithOwnerAuth**](#withownerauth) <br /> Sets the owner authorization value (password) to use when communicating with the TPM.

[**WithDeviceType**](#withdevicetype) <br /> Sets the type of TPM device to use.

[**WithAkHandle**](#withakhandle) <br /> Sets the AK handle to use for quote generation.

[**WithPcrSelections**](#withpcrselections) <br /> Sets the PCR selections to include in the quote.

### NV functions

[**NVExists**](#nvexists) <br /> Checks if an NV index exists in the TPM.

[**NVDefine**](#nvdefine) <br /> Defines an NV index in the TPM.

[**NVDelete**](#nvdelete) <br /> Deletes an NV index and associated data from the TPM.

[**NVRead**](#nvread) <br /> Reads data from an NV index in the TPM.

[**NVWrite**](#nvwrite) <br /> Writes data to an NV index in the TPM.

### TPM adapter

[**NewEvidenceAdapter**](#newevidenceadapter) <br /> Creates a new evidence adapter for the TPM.

[**NewEvidenceAdapterWithOptions**](#newevidenceadapterwithoptions) <br /> Creates a new evidence adapter for the TPM with options.

[**Close**](#close) <br /> Closes the connection to the TPM.

### Utility functions

[**HandleExists**](#handleexists) <br /> Checks to see if the specified handle exists in the TPM.

---


### `NVRead`

NVRead reads the bytes from the location specified by the NV handle.  

```go
func (tpm *canonicalTpm) NVRead(nvHandle int) ([]byte, error)
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _nvHandle_ | The handle of the NV index to read. |

#### Return value

A byte array containing the data read from the NV index. It returns an error if the handle isn't within the range of valid NV RAM or if the index doesn't exist.

### `NVWrite`

Writes data to an NV index in the TPM.

```go
func (tpm *canonicalTpm) NVWrite(nvHandle int, data []byte) error 
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _nvHandle_ | The handle of the NV index to write to. |
| _data_ | The data to write to the NV index. The maximum data size is 8192. |

#### Return value

Returns an error if the handle isn't within the range of valid NV RAM or if the index doesn't exist.

### `NVExists`

Checks if an NV index exists in the TPM.

```go
NVExists(nvHandle int) bool
```
#### Parameters

| Parameter | Description |
| --- | --- |
| _nvHandle_ | The handle of the NV index to check. |

#### Return value

Returns `true` if the NV index exists, or `false` if the handle isn't within the range of valid NV RAM or if the index doesn't exist.

### `NVDefine`

Defines an NV index in the TPM with the specified handle and length.

```go
func (tpm *canonicalTpm) NVDefine(nvHandle int, len int) error 
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _nvHandle_ | The handle of the NV index to define. |
| _len_ | The length in bytes of the NV index. The maximum length is 8192. |

#### Return value

Returns an error if the handle isn't within the range of valid NV RAM or if the index already exists.


### `NVDelete`

Deletes an NV index and associated data from the TPM.

```go
func (tpm *canonicalTpm) NVDelete(nvHandle int) error
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _nvHandle_ | The handle of the NV index to delete. |

#### Return value

Returns an error if the handle isn't within the range of valid NV RAM or if the index doesn't exist.


### `ReadPublic`

Reads the public key for an AK in the TPM.

```go
func (tpm *canonicalTpm) ReadPublic(handle int) (crypto.PublicKey, []byte, []byte, error)
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _handle_ | The handle of the AK to read. |

#### Return value

| Return value | Description |
| --- | --- |
| _crypto.PublicKey_ | The public key for the AK. |   
| _[]byte_ | The AK name. |
| _[]byte_ | The AK qualified name. |

It returns an error if the handle isn't persistent or doesn't exist.

#### Usage

### `GetEKCertificate`

Gets the EK certificate from the TPM.

```go
func (tpm *canonicalTpm) GetEKCertificate(nvIndex int) (*x509.Certificate, error)
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _nvIndex_ | The NV index of the EK certificate. |

#### Return value

| Return value | Description |
| --- | --- |
| *_x509.Certificate_ | A pointer to the EK certificate. |

Returns an error if the certificate doesn't exist or if the TPM is unable to read the certificate. Not all TPMs have a certificate for the EK.

### `GetQuote`

Gets a quote from the TPM. The quote is signed by the AK.

```go
func (tpm *canonicalTpm) GetQuote(akHandle int, nonce []byte, selection ...PcrSelection) ([]byte, []byte, error)
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _akHandle_ | The handle of the AK to use for signing the quote. |
| _nonce_ | An array of nonce bytes to include in the quote. |
| _selection_ | Optional. The PCR selections to include in the quote. If _selection_ isn't provided, all SHA-1 and SHA-256 PCRs will be included in the quote.|

```go
type PcrSelection struct {
	Hash crypto.Hash
	Pcrs []int
}
```

PcrSelection.Hash is the hash algorithm to use (SHA-1 or SHA-256), and PcrSelection.Pcrs is a list of comma-separated PCR index numbers.

#### Return value

| Return value | Description |
| --- | --- |
| _[]byte_ | The quote data. |
| _[]byte_ | The signature of the quote. The quote is signed with the public AK. |

Returns an error if the AK handle is invalid or if the TPM is unable to get the quote.

### `GetPcrs`

Reads the PCRs from the TPM.

```go
func (tpm *canonicalTpm) GetPcrs(selection ...PcrSelection) ([]byte, error) 
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _selection_ | Optional. The PCR selections to include in the quote. If _selection_ isn't provided, all SHA-1 and SHA-256 PCRs will be included in the quote. See [`GetQuote`](#getquote) for a definition of PcrSelection. |

#### Return value

`GetPcrs` returns the "flattened", concatenated, contiguous PCR measurements for SHA-256 banks 0-23 (in index order).  This is similar to the PCR values returned by `tpm2_quote` when -F values options are provided. 

### `HandleExists`

Checks to see if the specified handle exists in the TPM.

```go
HandleExists(handle int) bool  
```

#### Parameters

#### Return value

Returns `true` if the specified handle exists in the TPM, or `false` if the handle doesn't exist.

### `Close`

Closes the connection to the TPM. This should be called when the TPM is no longer needed.

```go
func (tpm *canonicalTpm) Close()
```

#### Parameters

None.

#### Return value

None.

### `NewEvidenceAdapter`

Creates a new evidence adapter for the TPM.

```go
func NewEvidenceAdapter(akHandle int, pcrSelections string, ownerAuth string) (connector.EvidenceAdapter2, error)
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _akHandle_ | The handle of the AK to use for signing the quote. |
| _pcrSelections_ | A list of PCRs in **tpm2-tools** PCR Bank Selection format. For more information, see [PCR Bank Specifiers](https://tpm2-tools.readthedocs.io/en/latest) in the tpm2-tools documentation. |
| _ownerAuth_ | The owner authorization value (password) to use when communicating with the TPM. The default password is blank (""). |

#### Return value

A new evidence adapter for the TPM, or an error if the adapter can't be created.

### `NewEvidenceAdapterWithOptions`

Creates a new evidence adapter for the TPM with options.

```go
func NewEvidenceAdapterWithOptions(opts ...TpmAdapterOptions) (connector.EvidenceAdapter2, error) 
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _opts_ | A list of options to use when creating the adapter. |

#### Return value

A new evidence adapter for the TPM with the specified options, or an error if the adapter can't be created.

### `WithOwnerAuth`

Sets the owner authorization value (password) to use when communicating with the TPM.

```go
func WithOwnerAuth(ownerAuth string) TpmAdapterOptions
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _ownerAuth_ | The owner authorization value (password) to use when communicating with the TPM. The default password is blank (""). |

#### Return value

None.

### `WithDeviceType`

Sets the type of TPM device to use. By default, the Linux device is used (/dev/tpmrm0). 

```go
func WithDeviceType(deviceType TpmDeviceType) TpmAdapterOptions
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _deviceType_ | The type of TPM device to use. |

#### Return value

None.

### `WithAkHandle`

Sets the AK handle to use for quote generation.

```go
func WithAkHandle(akHandle int) TpmAdapterOptions
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _akHandle_ | The handle of the AK to use for signing the quote. |

#### Return value

### `WithPcrSelections`

Sets the PCR selections to include in the quote. 

```go
func WithPcrSelections(selections string) TpmAdapterOptions
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _selections_ | A list of PCRs in **tpm2-tools** PCR Bank Selection format. For more information, see [PCR Bank Specifiers](https://tpm2-tools.readthedocs.io/en/latest/man/common/pcr/) in the tpm2-tools documentation.|

#### Return value

### `GetEvidenceIdentifier`

Gets the evidence identifier for the TPM.

```go
func (tca *tpmCompositeAdapter) GetEvidenceIdentifier() string
```

#### Parameters

None.

#### Return value

"tpm" is returned as the evidence identifier for the TPM.

### `GetEvidence`

Collects evidence from the TPM.

```go
func (tca *tpmCompositeAdapter) GetEvidence(verifierNonce *connector.VerifierNonce, userData []byte) (interface{}, error)
```

#### Parameters

| Parameter | Description |
| --- | --- |
| _verifierNonce_ | The Intel Trust Authority verifier nonce to include in the evidence. |
| _userData_ | Optional. User data to include in the evidence. |

#### Return value

| Return value | Description |
| --- | --- |
| _interface{}_ | The evidence data. |

---
**\*** Other names and brands may be claimed as the property of others.
