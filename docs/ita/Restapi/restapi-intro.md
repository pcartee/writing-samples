---
title: Intel Trust Authority REST API Reference
description: Introduction & landing page for the REST API reference documentation.
author: pcartee
topic-type: API_reference
date: 04/10/2025
uid: restapi.intro
---
*· 04/10/2025 ·*

## Intel® Trust Authority REST API Reference

Representational State Transfer (REST) APIs are service endpoints that allow you to use HTTPS to access nearly all the functionality provided by Intel Trust Authority. A few operations, such as creating a new Admin API key, can only be performed in the portal. All the REST APIs require an API key for authorization. For more information, see [API keys](../Concepts/concept-user-roles-and-api-keys.md).

The REST APIs are organized by service and functional area. 

- [Attestation](../Restapi/restapi-attestation.md) — Attestation and nonce APIs.
- [Azure Attestation](../Restapi/restapi-azure-attestation.md) — Attestation APIs specifically for Microsoft Azure Attestation compatibility.
- [Client Management](../Restapi/restapi-client-management.md) — This set of APIs supports CRUD operations on API clients.
- [Faithful Verification](../Restapi/restapi-faithful.md) — API to retrieve a Faithful Verification token audit report.
- [Policy Management](../Restapi/restapi-policy-management.md) — This set of APIs supports CRUD operations on appraisal and custom policies.
- [Product Management](../Restapi/restapi-product-management.md) — Management APIs to search for and retrieve products.
- [Service Management](../Restapi/restapi-service-management.md) — Management APIs to search for and retrieve services, such as Intel® SGX or Intel® TDX attestation.
- [Service Offer Management](../Restapi/restapi-service-offer-management.md) — Management APIs to search for and retrieve service offers.
- [Tenant Management](../Restapi/restapi-tenant-management.md) — This set of APIs supports management of tags, tenants, users, and user roles.

## Rate Limiting

Intel Trust Authority REST APIs have a rate limit of 1,000 requests per five minutes. If the rate limit is exceeded, additional requests will be throttled, and you may receive a `429 Too Many Requests` response. The REST APIs also have a body size limit of 500,000 bytes (500 KB) for each request.

> [!NOTE]
> A reduced rate limit of two requests per second is set for the Intel Trust Authority Pilot environments.

## Base and API URLs

There are two Intel Trust Authority deployment regions: European Union (EU) region, and a global region for all other countries. There are different BaseUrl and ApiUrl for each region, as follows:

  | Region | BaseUrl | ApiUrl |
  |--- | --- | --- |
  | **EU** | `https://portal.eu.trustauthority.intel.com` | `https://api.eu.trustauthority.intel.com` |
  | **World/US** | `https://portal.trustauthority.intel.com` | `api.trustauthority.intel.com` |

## OpenID configuration

The following URL returns the OpenID configuration document for Intel Trust Authority:

'https://portal.trustauthority.intel.com/.well-known/openid-configuration`

If you're in the European Union (EU) region, use the following URL:

`https://portal.eu.trustauthority.intel.com/.well-known/openid-configuration`

Sample response for status code 200:

```json
{
  "response_types_supported": [
    "token",
    "none"
  ],
  "id_token_signing_alg_values_supported": [
    "RS384"
  ],
  "revocation_endpoint": "https://portal.trustauthority.intel.com/crl/ats-ca-crl.der",
  "issuer": "https://portal.trustauthority.intel.com",
  "jwks_uri": "https://portal.trustauthority.intel.com/certs"
}
```

## Signing certificates

The following URL returns the JWKS of certificates used to sign Intel Trust Authority attestation tokens. 

`https://portal.trustauthority.intel.com/certs`

Intel Trust Authority supports PS386 and RS256 token signing algorithms. The signing key sets are identical for both algorithms and both sets are included in the JWKS.

If you are in the European Union (EU) region, use the following Intel Trust Authority URL to return JWKS certificates:

`https://portal.eu.trustauthority.intel.com/certs`

Sample response for status code 200 (truncated for brevity):

```json
{"keys":[{"alg":"PS384","e":"AQAB","kid":"79d807...6817785","kty":"RSA","n":"yE07D7FRSXLsswdeK7h22kw-Xv2K...ZnbSP"]}]}
```
