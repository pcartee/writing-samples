---
title: Attestation overview
description: An overview of how attestation works in Intel Trust Authority.
author: grminch
topic: conceptual
date: 09/01/2023
uid: attestation.overview
---

## Attestation overview

This article is a brief, high-level overview of how attestation works with Intel® Trust Authority. Intel Trust Authority is a _verifier_ in a remote attestation application architecture. To understand what a verifier is and how best to use Intel Trust Authority attestation, it's helpful to have a basic understanding of the Remote Attestation Procedures Architecture, as defined in [IETF RFC9334](https://datatracker.ietf.org/doc/rfc9334/). The terminology in this article is based on RFC9334.

Attestation is a process for establishing trust between a confidential computing workload and one or more relying parties. At its most basic, attestation involves three steps:

1. A confidential computing workload attests its identity and fidelity by providing TEE measurements and other cryptographic evidence, called a quote.
1. A verifier evaluates the quote against reference values and endorsers to determine if the quote is valid and if certain claims match stored values and policies.
1. A relying party uses information in the attestation token to decide if it should trust the attester.

## Verifier

Intel Trust Authority is focused on providing services for step 2, verification. For more information about where Intel Trust Authority fits into various workflows and the steps involved in each, see [Attestation patterns](concept-patterns.md).

## Attester

The _attester_ is a confidential computing environment that needs to prove its identity and that it hasn't been tampered with or otherwise compromised.

Intel Trust Authority also provides a [client](../Integration/integrate-go-client.md) and [TDX CLI](../Integration/integrate-go-tdx-cli.md) to simplify the task of getting a quote from the attesting workload. The Intel Trust Authority client adapter libraries handle the low-level calls to platform software, which greatly simplifies the integration of remote attestation into a confidential workload.

The attesting workload is responsible for collecting evidence for a quote, using a Intel Trust Authority library or other compatible method. That quote is then forwarded directly (passport) to Intel Trust Authority, or sent to a relying party that relays the quote (background check) to Intel Trust Authority.

## Relying party

The _relying party_ uses the attestation token to decide if it trusts the attester. The relying party must be able to process an attestation token issued by Intel Trust Authority. In the simplest passport case, the relying party performs a minimal verification of the attestation token and signing certificate without using any Intel Trust Authority services or REST API. In more complex scenarios, the relying party can have multiple points of contact with Intel Trust Authority and related utilities. For more information, see [Relying party integration](../Integration/integrate-relying-party.md).

## Faithful verification

An attestation token is only as good as the verifier and services in the chain of trust. Intel Trust Authority attestation tokens are signed with a certificate that is traceable to the Intel CA. Intel Trust Authority microservices run in TEEs and a record is kept of TEE quotes and the services used during quote verification and attestation. This feature, known as _Faithful Verification_, generates a token audit report that can be used to verify the Intel Trust Authority services involved in attestation and the Intel Trust Authority environment. For more information, see the [Faithful Verifier](../Utilites/utility-faithful-verifier.md) tool.

## Attestation policies

Intel Trust Authority uses _attestation_ (also called _appraisal_) _policies_ to define comparison tests that are applied to a quote during verification. For example, a policy can compare the latest **mrsigner** hash to the **mrsigner** hash from the quote to determine if the values match and then set the policy result. The list of policies that are matched or unmatched is included in the attestation token for further evaluation by the relying party. For more information, see [Policies](../Concepts/concept-policies.md).
