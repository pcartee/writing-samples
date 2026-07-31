---
title: Signed Policy Management
description: Signed policy management commands.
author: various
topic-type: Reference
date: 08/17/2023
uid: cli-signed-policy-commands
---

## Signed policy management

This section provides commands to create signed attestation policies for Intel® Trust Authority with or without using a key, certificate, and encryption algorithm.

## Create signed JWT attestation policies

The following command creates a new signed policy with a key, certificate, and an encryption algorithm.

`trustauthorityctl create policy-jwt -f <rego policy file path> -p <signing key path> -c <cert path> -a <algorithm> -s`

### Sample call

```bash
trustauthorityctl create policy-jwt -f sgxpolicy.txt -p policyjwt/trustauthority-jwt.key -c policyjwt/trustauthority-jwt.crt -a RS384 -s
```

### Sample response

```bash
Original policy:
default matches_sgx_policy = false
matches_sgx_policy = true
{  input.sgx_is_debuggable == false
   input.sgx_isvsvn == 0
   input.sgx_isvprodid == 0
   input.sgx_mrsigner ==  "d912a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b"
   input.sgx_mrenclave == "bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab"
} Algorithm used during signing:  RS384
Policy token is stored in file  sgxpolicy.signed.20230321040145.txt
Policy token generated:
eyJh...gkw
```

## Create signed JWT attestation policies with the default algorithm

### Prerequisites

Create self signed key and certificate for policy JWT token creation:

#### Generate key and cert files for -algorithm (PS384 | RS384) (Recommend)

`openssl req -x509 -nodes -days 365 -newkey rsa:3072 -keyout trustauthority-jwt.key -out trustauthority-jwt.crt`

#### Generate key and cert files for -algorithm (PS256 | RS256)

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout trustauthority-jwt.key -out trustauthority-jwt.crt`

### Create Policy JWT

The following command creates a new signed policy with a key, certificate, and the default algorithm.

`trustauthorityctl create policy-jwt -f < rego policy file path > -p < signing key path > -c < cert path > -a < algorithm > -s`

### Sample call

```bash
trustauthorityctl create policy-jwt -f sgxpolicy.txt -p policyjwt/trustauthority-jwt.key -c policyjwt/trustauthority-jwt.crt -s
```

### Sample response

```bash
Original policy:
default matches_sgx_policy = false
matches_sgx_policy = true
{  input.sgx_is_debuggable == false
   input.sgx_isvsvn == 0
   input.sgx_isvprodid == 0
   input.sgx_mrsigner ==  "d912a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b"
   input.sgx_mrenclave == "bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab"
} Algorithm used during signing:  PS384
Policy token is stored in file  sgxpolicy.signed.20230321040159.txt
Policy token generated:
eyJh...0kJ
```

## Create unsigned JWT attestation policies

The following command creates a new unsigned policy without a key, certificate, or any encryption algorithm.

```bash
trustauthorityctl create policy-jwt -f <rego policy file path>
```
### Sample call

```bash
trustauthorityctl create policy-jwt -f sgxpolicy.txt
```

### Sample response

```bash
Original policy:
default matches_sgx_policy = false
matches_sgx_policy = true
{  input.sgx_is_debuggable == false
   input.sgx_isvsvn == 0
   input.sgx_isvprodid == 0
   input.sgx_mrsigner ==  "d912a4f07ef83892a5915fb2ab584be31e186e5a4f95ab5f6950fd4eb8694d7b"
   input.sgx_mrenclave == "bab91f200038076ac25f87de0ca67472443c2ebe17ed9ba95314e609038f51ab"
} Algorithm used during signing:  None
Policy token is stored in file  sgxpolicy.unsigned.20230321040138.txt
Policy token generated:
eyJ...biJ9.

```
