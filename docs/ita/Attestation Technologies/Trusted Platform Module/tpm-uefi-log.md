---
title: UEFI Event Logs
description: How Intel Trust Authority uses UEFI event logs to validate PCR values and help with troubleshooting.
author: mkwilbux
topic-type: conceptual
date: 11/14/2024
uid: uefi.log
---

*· 10/25/2024 ·*

## Unified Extensible Firmware Interface (UEFI) event logs

Modern UEFI firmware triggers system integrity measurements during the boot sequence. These measurements are stored in event logs and can be consumed by Intel® Trust Authority during remote attestation. These logs include the individual measurement events for TPM PCRs 0-7 that were extended when the system booted. 

:::note
UEFI generates event logs using the hash algorithm set by the UEFI author, typically SHA-256. For UEFI event log replays to work correctly, the same algorithm must be enabled in the TPM PCR banks. Support for different TPM PCR banks differs by OEM. Some manufacturers allow multiple PCR banks to be enabled at the same time, while others only allow a single PCR bank to be enabled. Where possible, Intel recommends enabling all PCR banks on the TPM, as this will generally ensure that the PCR bank matching the event log algorithm is always available. Where this is not possible, check the UEFI event log at `/sys/firmware/security/tpm0/binary_bios_measurements` and use the hash length of the event measurements to determine the algorithm in use by your system's UEFI (16 bytes for SHA-1, 32 bytes for SHA-256, and 48 bytes for SHA-384).

Also note that the `pcr_slections` setting in the `config.json` configuration file defines the PCR bank that the attestation client CLI will use. This must match the algorith used for any event logs, so that the attestation client CLI picks the correct PCR bank for use in the event log replay.
:::

### When measurements change
PCR values change at system boot when firmware, the bootloader, OS kernel, or other changes are made.  

However, TPM measurements (except some IMA measurements) only update on system reboot. If you update the OS kernel, the new kernel will not be measured until reboot. UEFI logs are part of boot-time integrity attestation, not run-time.

### Sample appraisal policy to verify Secure Boot is active

This sample appraisal policy asserts that Secure Boot is enabled, as well as verifying chain-of-trust requirements.

`tdx.tdx_mrtd measurement`: this is a measurement from the Azure confidential VM trust domain. This requires Intel® Trust Domain Extensions (Intel® TDX) and is unique to this version of the trust domain from Azure, and may change if Azure performs an update. The purpose of including this measurement in policy is to verify that the attester (the confidential VM) is a legitimate Azure confidential VM with Intel TDX. This proves that we're using the vTPM version we expect, because Azure links their vTPM implementation with Intel TDX. Effectively this means that the "root" of our chain of trust is Intel TDX.

`evlog := input.tpm.uefi_event_logs[_]`: The notation `[_]` tells the policy to iterate over all elements in the event logs claim. 

`evlog.index == 7`: Tells the policy to verify that the PCR index for this event is 7. The measurement event for the Secure Boot enablement setting is extended to PCR7. 

`evlog.type_name == "EV_EFI_VARIABLE_DRIVER_CONFIG"`: This is the name of the measurement event.

`evlog.details.unicode_name == "SecureBoot"`: This is the unicode name of the measurement event, and this is how we verify that we're looking at the Secure Boot enablement boolean.

`evlog.details.variable_data == "AQ=="`: This is hexadecimal for True, so we are asserting that the SecureBoot state must be enabled.

You can generate an attestation token without any policy to see all of the claims, including event logs, for the attester. This is the easiest way to capture claims you might want to use when writing policies. The token is in base-64 encoding, so you'll need to decode it to see the claims. 

```bash

The same mechanics used to create this policy for Secure Boot can be applied to creating any number of other UEFI event log policies.

```json
default valid_evlog_measurements = false
valid_evlog_measurements = true {
  input.tdx.tdx_mrtd == "89b65df57162988700bb27b57b6dfb4fe21d9979bdbbc128cc0d4a291fb07cb6b790ab205ea59216e8bf1de414fc25aa"
  input.tdx.tdx_seamsvn == 4

  evlog := input.tpm.uefi_event_logs[_]
  evlog.index == 7
  evlog.type_name == "EV_EFI_VARIABLE_DRIVER_CONFIG"
  evlog.details.unicode_name == "SecureBoot"
  evlog.details.variable_data == "AQ=="
}
```

### UEFI event logs with Intel Trust Authority client

The Intel Trust Authority attestation client CLI provides options for collecting and including UEFI event logs during remote attestation.

To request an attestation including UEFI event logs with the Intel Trust Authority attestation client CLI, use the `--evl` flag  with `trustauthority-cli token`. Note that the `--evl` option requires the `--tpm` option as well.

```bash
sudo trustauthority-cli token --tdx --tpm --evl -c config.json
```

Linux distributions expose the event logs for each UEFI measurement event. The `--evl` option enables the collection of UEFI event logs. By default, the UEFI event logs are stored at `/sys/kernel/security/tpm0/binary_bios_measurements`. To customize the log collection path for the attestation client CLI (this may be required for different Linux distributions that expose the logs elsewhere), use the `--evl-path` option. 
```bash
trustauthoritycli token --evl-path <path> --tdx --tpm --evl -c config.json
```
## Evidence with event log

The following sample of evidence with event logs includes runtime and uefi event log evidence using the command below.  

```bash
./trustauthority-cli evidence --tpm --tdx --evl -c config.json > evidence-with-event-logs.json
```
```json
{
 "tdx": {
  "runtime_data": "eyJrZXlzIjpbeyJraWQiOiJIQ0xBa1B1YiIsImtleV9vcHMiOlsic2lnbiJdLCJrdHkiOiJSU0EiLCJlIjoiQVFBQiIsIm4iOiJ1NjkxdWdB9...",
  "quote": "BAACAIEAAAAAAAAAk5pyM/ecTKmUCg2zlX8GBw63EL/H5YFouU/M5DIyGdAAAAAABAEHAAAA=..."
 },
 "tpm": {
  "quote": "/1RDR4AYACIACy5qBmpdQckwKSj1obbaeHK1cdtpOCrctXVdXwDNeVo3AAAAAAAAZsI7wwAAAAUAAAAAASAgAxIAEgADAAAA=...",
  "signature": "ABQACwEAL4ucHZfySxfFepu25GGhs9CzLPITM36q/WHsAY+ATk6FhNqvFS3mXa+cshU6vg==...",
  "pcrs": "Qtj1VpAaTLqbxS0yxFnGxwoK11xTOsQgJd15V3Zy5A0Dr0oq/1P5g9s4ZSusAXpJIhX/+mFDhuS1l7EyXOECiy4PbhSXaULl7RlLyblKB0dfe5gIPUWM/lXMA+ofRD8VYr7sjfUcdeFKn8+acjShPxmOeWk9RYz+VcwDAAAAA=...",
  "uefi_event_logs": "AAAAAAMAAAAAAAvp3WQMyTb1gKPTnj3hLrh3Kiqt8S90hxaoZoyP1l70YUERddmlcspEMzLXxY7i9mvp3WQMyTb1gKPTnj3hLv8qkFEXyAUXBqq3fSmibmLZo43iVt/+t3oO7IZmq9mvp3WQMyTb1gKPTnj3hLyHWuio21RB/dX/.CeTtfTMKWHM6W9mvp3WQMyTb1gKPTnj3hLeDZGW9/652jvrty6qLV4e69RsnkqAg6A40Gj+CT/Tnj3hLpLP+4yTSXFP7XLSGMNyA3X7njBqsjI3uqSc5aZfjO869mvp3WQMyTb1gKPTnj3hLqYPnPle98BTJopMxKQ7offN/l8gdvMQ8bJM/4iCcC9W9mvp3WQMyTb1gKPTnj3hLtCBQnQ1pspRjP9euLDaytUnUWmqGPvFoQ6ERahESf1a9mvp3WQMyTb1gKPTnj3hLzoxE4YX6qgOVnPIyKWB4VO9+MW7Qdz1m175eCkgGHeW9mvp3WQMyTb1gKPTnj3hL6AijN+1pEe9WHCfKusq/TqbW4g+3D1QTsSGsJRq8wQy9mvp3WQMyTb1gKPTnj3hL6ccbfNWk3wukjSykjmxGjmVyV/c/ZgF95F4Y7nRu19W9mvp3WQMyTb1gKPTnj3hL/TBiNY4OHcTDpgOA7xvf1MUfRHO4YAk32SHfRy+/m2W9mvp3WQMyTb1gKPTnj3hLZWJaFD0iDqGE29XN+xuenDvZZUKU6qK5hii8Jz68GLW9mvp3WQMyTb1gKPTnj3hLgAQjzrfkdZYhpixym6vIH1MlnZX3ZFciStYBVCt7JtS9mvp3WQMyTb1gKPTnj3hLAyj33RK1Uu+nqeCDcwMzuF8/+w9O2G9mvp3WQMyTb1gKPTnj3hLCfdpljHBjbDDNJHrSzxluPJ5I4xfxeOrC6UnN9u9JvO9mvp3WQMyTb1gKPTnj3hL+YPVijrCXyq9mvp3WQMyTb1gKPTnj3hLaRujQU54YiWBvFGbrwvLFvsmLTq72GOfPg7KKin5lAa9mvp3WQMyTb1gKPTnj3hLbOHymG8MRmg7oH0pbQqERI7PdsadsYP+KcNu7Y+ofRD8VYr7sjfUcdeFKn8+vV6mYVxA9C9EptvroCgAAABFeGl0IEJvb3QgU2VydmljZXMgUmV0dXJuZWQgd2l0aCBTdWNjZXNz..."
 }
}
```

### Errors

You may experience errors under the following conditions.
- When the system is booted to legacy BIOS mode instead of UEFI.
- When `/sys/firmware/security/tpm0/binary_bios_measurements` is not the current path or does not exist, or the current user doesn't have permission to access the path.
- If the Linux user collecting TPM evidence does not have read access to `/sys/kernel/security/tpm0/binary_bios_measurements`.

Successful attestation requires that all provided event logs pass an event log replay check. This involves replaying the measurement extension events of each event ion the log and matching the final measurement against the actual PCR value. This is an integrity check that verifies that the event log can be trusted. If the event log replay for any PCR does not match the actual PCR value, the event log is considered untrustworthy and an error will be returned.
