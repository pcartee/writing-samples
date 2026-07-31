The value of **eat_profile** is always `https://portal.trustauthority.intel.com/eat_profile.html`.

The following attestation token was generated from an Intel TDX trust domain.

```json
{
  "alg": "PS384",
  "jku": "https://.../Certs",
  "kid": "1881f519948621f7aeb...",
  "typ": "JWT"
}
.
{
  "tdx_tee_tcb_svn": "03000500000000000000000000000000",
  "tdx_mrseam": "2fd279c16164a93dd5bf373d834...",
  "tdx_mrsignerseam": "00000000000000000000...",
  "tdx_seam_attributes": "0000000000000000",
  "tdx_td_attributes": "0000000000000000",
  "tdx_xfam": "e718060000000000",
  "tdx_mrtd": "b1392f86586f9b15fb1b6345...",
  "tdx_mrconfigid": "0000000000000000000...",
  "tdx_mrowner": "0000000000000000000...",
  "tdx_mrownerconfig": "0000000000000000000...",
  "tdx_rtmr0": "0000000000000000000...",
  "tdx_rtmr1": "0000000000000000000...",
  "tdx_rtmr2": "0000000000000000000...",
  "tdx_rtmr3": "0000000000000000000...",
  "tdx_report_data": "0000000000000000000...",
  "tdx_seamsvn": 3,
  "tdx_td_attributes_debug": false,
  "tdx_td_attributes_septve_disable": false,
  "tdx_td_attributes_protection_keys": false,
  "tdx_td_attributes_key_locker": false,
  "tdx_td_attributes_perfmon": false,
  "tdx_is_debuggable": false,
  "tdx_collateral": {
    "qeidcerthash": "b2ca71b8e849d5e7...",
    "qeidcrlhash": "f454dc1b9bd4ce3...",
    "qeidhash": "665b5e4a8c34c2493...",
    "quotehash": "ac5efbb7ac2815acdd6...",
    "tcbinfocerthash": "b2ca71b8e849d5e79...",
    "tcbinfocrlhash": "f454dc1b9bd4ce36c...",
    "tcbinfohash": "0bc7962b158eaeb896..."
  },
  "policy_ids_unmatched": [
    {
      "id": "c7c49dd2-a96a-43bd-8cee-f2aa99503458",
      "version": "v4"
    }
  ],
  "policy_defined_claims": {},
  "attester_tcb_status": "OK",
  "attester_type": "TDX",
  "verifier_instance_ids": [
    "605a1fb4-4831-487b-9422-980c16ae0585",
    "08696fd9-c544-497b-bf6f-913effdfa579",
    "657ecb0b-5653-4deb-848b-71df26f8e907",
    "240426fa-d37a-4dde-8e37-ea236c9c961a"
  ],
  "dbgstat": "disabled",
  "eat_profile": "https://portal.trustauthority.intel.com/eat_profile.html",
  "intuse": "generic",
  "ver": "1.0.0",
  "exp": 1692376314,
  "jti": "304915ef-ec89-48a4-bae0-890c09978d3e",
  "iat": 1692376014,
  "iss": "Intel Trust Authority",
  "nbf": 1692376014
}
.[signature]

```

:::note

If you are in the European Union (EU) region, use the following Intel Trust Authority URL: 
`https://portal.eu.trustauthority.intel.com `

:::
