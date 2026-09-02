---
title: Policy signing tool
description: An overview of the policy signing tool and how to use it to sign policies.
author: pcartee
topic: conceptual
date: 12/21/2023
uid: policy.signing.tool
---
import VerifyBinary from '../Include/_verify-signed-binaries.md';

## Policy signing tool

The Policy Signing tool is a command-line utility used to sign user-defined policies. A signed attestation policy takes the form of a JSON Web Token (JWT) signed by the user's private key to protect the integrity of the policy. The signed policy file can then be uploaded to Intel Trust Authority to evaluate the trust of a workload and produce an attestation token. Signing is not required to use custom policies but adds the ability to verify that policies used for attestation have not been changed.

A plaintext version of a policy is required before using the Policy Signing tool.  For information on the structure, syntax, usage, and other requirements for attestation policies, see the [Attestation Policies](../Concepts/concept-policies.md) article.

The Policy Signing tool can sign policies or generate an unsigned JWT policy.  Unsigned JTW policies can be used with some 3rd-party integrations.

The Policy Signing tool is available for both Linux and Microsoft Windows and can be downloaded from the Intel® Trust Authority downloads page.

:::note
Valid characters include: numbers 0 through 9, upper and lowercase English characters, underscore (_), colon (;), period (.), slash  (/), dash (-), and a space ( ).
:::

## Signature Verification

To verify the signature of the Policy Signing tool, perform the following steps.

<VerifyBinary />

## Creating a signing key and certificate

A signing key and certificate are required to generate signed policies.  Below is a sample command using OpenSSL to generate a key and self-signed certificate:

```bash
$ openssl req -x509 -nodes -days 365 -newkey rsa:3072 -keyout trustauthority-jwt.key -out trustauthority-jwt.crt
```


## Creating unsigned JWT attestation policies

To create an unsigned policy in JWT format, execute the policy-sign tool providing the plaintext policy without a signing key or certificate.

```bash
$ ./policy-sign --policyfile plaintext-policy-file.txt
```

Sample output:

```bash
Original policy file:
default matches_sgx_policy = false
matches_sgx_policy = true {
   input.sgx_mrenclave == "771df07c10229cab0106a5187bfee45441a4cf47e46c4ef7a56c48e824bba333"
   input.sgx_mrsigner == "965e5026a0cefd27792b99d50d225bf60b53bae4005d2fc11d67d8ff742c2ec5"
   input.sgx_isvprodid == 0
   input.sgx_isvsvn == 0
   input.sgx_is_debuggable == false
}

Algorithm used during signing:  None
Policy token is stored in file policy.unsigned.txt
Policy token generated:
eyJhbGciOiJub25lIn0.eyJBdHRlc3RhdGlvblBvbGljeSI6IlpHVm1XXX.
```

The policy is saved in unsigned JWT format as `policy.unsigned.txt`.  Unsigned policies in JWT format can be used by some 3rd-party applications.

## Creating signed JWT attestation policies

To create a signed policy, execute the policy-sign tool and provide a signing certificate and private key along with the plaintext policy:

```bash
$ ./policy-sign --policyfile policy.txt --privkeyfile trustauthority-jwt.key --certfile trustauthority-jwt.crt

Original policy file:
default matches_sgx_policy = false
matches_sgx_policy = true {
   input.sgx_mrenclave == "771df07c10229cab0106a5187bfee45441a4cf47e46c4ef7a56c48e824bba333"
   input.sgx_mrsigner == "965e5026a0cefd27792b99d50d225bf60b53bae4005d2fc11d67d8ff742c2ec5"
   input.sgx_isvprodid == 0
   input.sgx_isvsvn == 0
   input.sgx_is_debuggable == false
}

Algorithm used during signing:  PS384
Policy token is stored in file policy.signed.txt
Policy token generated:
eyJhbGciOiJSUzM4NCIsIng1XXX.YyI6WyJNSUlFdGpDQ0F4NmdBd0lCQWdJVWEwQWXXX.FGempmdGpvT2hkbGN3d3dEUVlKS29aSWh2Y05BUUVMXG5CUXXX
```

The policy is saved in signed JWT format as `policy.signed.txt`.

## Policy Signing tool parameters

The Policy signing tool accepts the following parameters:

```bash
Usage of ./policy-sign:
  -algorithm string
        Supported algorithm of policy signing key pair (RS256|PS256|RS384|PS384) (default "PS384")
  -certfile string
        Required for signed policies. Path to PEM formatted file that contains your signing certificate
  -policyfile string
        Required. Path to text policy file to be signed into a JWT format Intel Trust Authority policy
  -privkeyfile string
        Required for signed policies. Path to PEM formatted file that contains your RSA private key
```

## Uploading the signed policy to Intel® Trust Authority

Once the policy has been converted to JWT format (whether signed or unsigned), the JWT can be uploaded as a new policy in Intel® Trust Authority.

Policies can be uploaded using the [Intel® Trust Authority web UI](../How-to%20workflows/howto-manage-attestation-policies.md) or via the command line using the [Intel® Trust Authority Tenant CLI](../Command-line/cli-policy-commands.md), as well as by REST API.

Once the policy has been converted to JWT format (whether signed or unsigned), the JWT can be uploaded as a new policy in the Intel® Trust Authority portal.

Policies can be uploaded using the [Intel® Trust Authority portal](../How-to%20workflows/howto-manage-attestation-policies.md) or via the command line using the [Intel® Trust Authority CLI](../Command-line/cli-policy-commands.md), as well as by REST API.

After you upload a signed policy to the Intel Trust Authority portal, you can view the policy under **Manage Policies** dashboard with a green tick mark.
