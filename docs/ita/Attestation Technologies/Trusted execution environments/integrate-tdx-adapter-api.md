---
title: TDX
description: Provides an overview of the Trust Authority Go client
author: pcartee
topic: integration
date: 12/22/2023
uid: integrate.tdx.api
---

*· 12/22/2023 ·*

## `go-tdx` adapter API reference

The Trust Authority Intel® TDX Attestation client includes a Go client and a [CLI](../../Integration/integrate-go-tdx-cli.md) for use on the command line or by languages other than Go, enabling you to use TDX remote attestation in your application.

:::note
Trust Authority uses the tdx_report_data claim to verify certain data provided with the quote. The TDX quote's `REPORTMACSTRUCT.REPORTDATA` must contain a SHA512 hash that is the cumulative value of of the nonce supplied with the evidence, runtime_data supplied during quote generation, optional user data (supplied via the `user_data` parameter in client APIs), and attester held data supplied by the TEE during quote generation. The Trust Authority clients take care of hashing the data for you, however, independently developed clients must contain the logic to add the hash to REPORTDATA. For more information, see the Go TDX adapter's [CollectEvidence](https://github.com/intel/trustauthority-client-for-go/blob/14b89ef3b58dac84feb125857f6837c1e1b166f0/go-tdx/collect_evidence.go#L26) function as an example.

Microsoft Azure TDX Preview users should use the [azure-tdx-preview](https://github.com/intel/trustauthority-client-for-go/tree/azure-tdx-preview/go-tdx) branch.  There are some key differences in the prerequisites, build process, and commands that are specific to the Microsoft Azure implementation.  See the README.md file for details.
:::

The following APIs are exposed by **go-tdx**.

```go
import "github.com/intel/trustauthority-client-for-go/go-tdx"
```

[**func CollectEvidence**](#func-collectevidence)

[**func Decrypt**](#func-decrypt)

[**func GenerateKeyPair**](#func-generatekeypair)

[**func GetEventLogs**](#func-geteventlogs)

[**func NewEvidenceAdapter**](#func-newevidenceadapter)

[**func NewEventLogParser**](#func-neweventlogparser)

The following code fragment creates a new TDX adapter and then collects evidence for a quote. 

```go
import "github.com/intel/trustauthority-client-for-go/go-tdx"

evLogParser := tdx.NewEventLogParser()
adapter, err := tdx.NewEvidenceAdapter(tdHeldData, evLogParser)
if err != nil {
    return err
}

evidence, err := adapter.CollectEvidence(nonce)
if err != nil {
    return err
}
```

### `func CollectEvidence`

```go
func (adapter *tdxAdapter) CollectEvidence(nonce []byte) (*connector.Evidence, error)
```
**CollectEvidence**  Collects evidence for a quote from the TDX trust domain. It takes a nonce as input, which is hashed during trust domain report creation. If successful, **CollectEvidence** returns an **Evidence** structure; otherwise it returns an error.

[Back to top](#go-tdx-adapter-api-reference)

### `func Decrypt`

```go
func Decrypt(encryptedData []byte, em *EncryptionMetadata) ([]byte, error)
```

**Decrypt** takes encrypted data as input and decrypts the data using the private key that is passed in the **EncryptionMetadata**. The Decrypt API returns a byte array containing decrypted data in case of success, else error in case of failure.

The following snippet shows how to decrypt an encrypted blob.

```go
em := &tdx.EncryptionMetadata{
	PrivateKeyLocation: privateKeyPath,
	HashAlgorithm:      "SHA256",
}
decryptedData, err := tdx.Decrypt(encryptedData, em)
if err != nil {
    fmt.Printf("Something bad happened: %s\n\n", err)
    return err
}
```

[Back to top](#go-tdx-adapter-api-reference)

### `func GenerateKeyPair`

```go
func GenerateKeyPair(km *KeyMetadata) ([]byte, []byte, error)
```
**GenerateKeyPair** is used to create a private key based on key metadata.

```go
km := &tdx.KeyMetadata{
	KeyLength: 3072,
}
privateKeyPem, publicKeyPem, err := tdx.GenerateKeyPair(km)
if err != nil {
    fmt.Printf("Something bad happened: %s\n\n", err)
    return err
}
```
[Back to top](#go-tdx-adapter-api-reference)

### `func GetEventLogs`

```go
func (parser *fileEventLogParser) GetEventLogs() ([]RtmrEventLog, error)
```

The **GetEventLogs** API returns a trust domain event log in the form of JSON. The trust domain event log consists of all the events that get measured to all the four RTMRs in order. The TD event log can be used to verify the integrity of RTMRs (Real-Time Monitoring and Response) by replaying all the event measurements in order.

The following snippet collects the event log from a TD.

```go
evLogParser := tdx.NewEventLogParser()
eventLog, err := evLogParser.GetEventLogs()
if err != nil {
    return err
}
```

[Back to top](#go-tdx-adapter-api-reference)

### `func NewEvidenceAdapter`

```Go
func NewEvidenceAdapter(udata []byte, evLogParser EventLogParser) (connector.EvidenceAdapter, error)
```

**NewEvidenceAdapter** initializes an instance of **TdxAdapter**, which manages the quote collection from a trust domain (TD). **TdxAdapter** is also responsible for collecting the event log for a TD.

The following code snippet shows how to create a new Go TDX adapter, and then use the adapter to collect a quote from the TDX-enabled platform.

```go
import "github.com/intel/trustauthority-client-for-go/go-tdx"

evLogParser := tdx.NewEventLogParser()
adapter, err := tdx.NewEvidenceAdapter(tdHeldData, evLogParser)
if err != nil {
    return err
}

```

[Back to top](#go-tdx-adapter-api-reference)

### `func NewEventLogParser`

```go
func NewEventLogParser() EventLogParser
```

**NewEventLogParser** initializes an instance of EventLogParser which manages the event log collection from a trust domain by reading either the ACPI (Advanced Configuration and Power Interface) tables or an EFI (Extensible Firmware Interface) file containing event log data. The event log for a trust domain is stored in ACPI tables.

See the code snippet in [**GetEventLogs**](#func-geteventlogs) for sample usage. 

[Back to top](#go-tdx-adapter-api-reference)

