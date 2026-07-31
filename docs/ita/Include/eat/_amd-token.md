:::note
This feature is in limited preview status. Details of implementation and usage may change before general availability. Preview features are only available on the Intel Trust Authority Pilot environment. Contact your Intel representative for access.
:::

The following attestation token was generated from AMD* SEV-SNP. 

Long values have been truncated for brevity.

```json
{
  "sevsnpvm-authorkeydigest": "0000000000",
  "sevsnpvm-bootloader-svn": 2,
  "sevsnpvm-familyId": "00000000000000000000000000000000",
  "sevsnpvm-imageId": "00000000000000000000000000000000",
  "sevsnpvm-reportdata": "a7ddd44",
  "sevsnpvm-lauchmeasurement": "dfa2b37b1",
  "sevsnpvm-hostdata": "0000000000000000000000000000000000",
  "sevsnpvm-idkeydigest": "00000000000000000000000000000",
  "sevsnpvm-is-debuggable": false,
  "sevsnpvm-microcode-svn": 41,
  "sevsnpvm-migration-allowed": false,
  "sevsnpvm-smt-allowed": true,
  "sevsnpvm-snpfw-svn": 18,
  "sevsnpvm-tee-svn": 0,
  "sevsnpvm-vmpl": 0,
  "ita-ver": "1.0",
  "sevsnpvm-collateral": "84d15a56",
  "attester_held_data": "dGVzd",
  "policy_ids_matched": [
    {
      "id": "b802fff",
      "version": "v1",
      "hash": "PApC1bnOL"
    }
  ],
  
  "attester_tcb_status": "true",
  "attester_tcb_date": "2024-04-09T17:18:48Z",
  "attester_type": "SNP",
  "verifier_instance_ids": [
    "3dfa-80f0-4575-a57f-217",
    "538e-9cc2-4cb6-a15b-813",
    "4f89-57e0-4f85-9a42-d34",
    "b839-48d2-42f3-8448-d17",
    "6365-1db4-4401-b31a-8b0"
  ],

  "dbgstat": "disabled",
  "eat_profile": "https://portal.trustauthority.intel.com",
  "intuse": "generic",
  "ver": "1.0.0",
  "exp": 1718252618,
  "jti": "63f20a47-7dac-4766-ad2e-df",
  "iat": 1718252318,
  "iss": "Intel Trust Authority",
  "nbf": 1718252318
}

```
