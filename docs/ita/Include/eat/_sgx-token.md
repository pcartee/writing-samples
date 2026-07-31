The following attestation token was generated from an Intel SGX enclave. 

```json
{
  "alg": "PS384",
  "jku": "https://.../Certs",
  "kid": "1881f519948621f7...",
  "typ": "JWT"
}
.
{
  "sgx_mrenclave": "ab9989f1c4c1ffa3...",
  "sgx_mrsigner": "7f4e8adbc1d8da7ae...",
  "sgx_isvprodid": 1,
  "sgx_isvsvn": 1,
  "sgx_report_data": "7192385c3c0605...",
  "sgx_is_debuggable": false,
  "sgx_collateral": {
    "qeidcerthash": "b2ca71b8e849...",
    "qeidcrlhash": "f454dc1b9bd4c...",
    "qeidhash": "d862cab332b96a7fb...",
    "quotehash": "e36b3df6fd3d1...",
    "tcbinfocerthash": "b2ca71b8e849d5...",
    "tcbinfocrlhash": "f454dc1b9bd4ce3...",
    "tcbinfohash": "dc800f168c528af..."
  },
  "attester_held_data": "SnVzdCBzb21lIHRlc3QgZ...",
  "policy_ids_matched": [
    {
      "id": "c7c49dd2-a96a-43bd-8cee-f2aa99503458",
      "version": "v4"
    }
  ],
  "policy_defined_claims": {},
  "attester_tcb_status": "OUT_OF_DATE",
  "attester_advisory_ids": [
    "INTEL-SA-00586",
    "INTEL-SA-00614",
    "INTEL-SA-00615",
    "INTEL-SA-00657",
    "INTEL-SA-00730",
    "INTEL-SA-00738",
    "INTEL-SA-00767"
  ],
  "attester_type": "SGX",
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
  "exp": 1692376242,
  "jti": "0c1b3de7-2487-485f-9f7b-066e299d83fc",
  "iat": 1692375942,
  "iss": "Intel Trust Authority",
  "nbf": 1692375942
}.[Signature]

```

 :::note

 If you are in the European Union (EU) region, use the following Intel Trust Authority URL:
 `https://portal.eu.trustauthority.intel.com`

 :::
