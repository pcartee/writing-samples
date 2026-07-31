_Long values are truncated for better readability._
```json

{
  "alg": "PS384",
  "jku": "https://portal.trustauthority.intel.com/certs",
  "kid": "c82989ba184f46ff363d23ed9612c0ab3849c712",
  "typ": "JWT"
}
.
{
"policy_ids_matched":  [
    {
      "id": "b802fff0-eba4-4286-9fdb-7a3cdc04e94d",
      "version": "v1",
      "hash": "PApC1bnOL/3KvC4IieSU6m/Ho7pbKLxrif1Yo6l..."
    },
   {
      "id": "3910b351-5865-4fb2-a731-17c6793cd4ca",
      "version": "v1",
      "hash": "PApC1bnOL/3KvC4IieSU6m/Ho7pbKLxrif1Yo6lf..."
    }
],
"policy_ids_unmatched":  [
    {
      "id": "8500e95a-58da-4b8a-a585-274730576d31",
      "version": "v1",
      "hash": "PApC1bnOL/3KvC4IieSU6m/Ho7pbKLxrif1Yo6lf..."
    },
   {
      "id": "5210b351-5865-4fb2-a731-17c6793cd4ca",
      "version": "v1",
      "hash": "PApC1bnOL/3KvC4IieSU6m/Ho7pbKLxrif1Yo6lf..."
    }
],
"verifier_instance_ids": [
    "6ff81e58-93a1-44c8-bac9-0ad96ef4e34a",
    "719c2db6-b45a-4a28-bbe6-4feb15705333",
    "171f2e20-b58a-4780-8d16-a31580a934b3",
    "968fa713-e9c3-4f0e-a20c-80fd38043475",
    "1f94527f-468b-4c42-a556-60646fe7b9bc"
  ],
  "ver": "1.0.0",
  "provider" : "intel",
  "eat_profile": "https://portal.trustauthority.intel.com/eat_profile.html",
  "intuse" : "generic",
  "exp": 1712619476,
  "jti": "7b42cdc6-1745-46a9-8bf5-2f3f225ad970",
  "iat": 1712619176,
  "iss": "Intel Trust Authority",
  "nbf": 1712619176
"nvgpu": {
        "sub": "NVIDIA-GPU-ATTESTATION",
        "secboot": true,
        "x-nvidia-gpu-manufacturer": "NVIDIA Corporation",
        "x-nvidia-attestation-type": "GPU",
        "iss": "https://nras.attestation.nvidia.com",
        "eat_nonce": "56623296D15318B184248494294EAAE03F8083...",
        "x-nvidia-attestation-detailed-result": {
          "x-nvidia-gpu-driver-rim-schema-validated": true,
          "x-nvidia-gpu-vbios-rim-cert-validated": true,
          "x-nvidia-mismatch-measurement-records": [
            {
              "runtimeSize": 48,
              "index": 9,
              "goldenValue": "059b32e712a153f490dbfb7976a9e275d...",
              "runtimeValue": "7f3e9382785513c1932dfcc9e87f6ef6b...",
              "goldenSize": 48
            }
          ],
          "x-nvidia-gpu-attestation-report-cert-chain-validated": true,
          "x-nvidia-gpu-driver-rim-schema-fetched": true,
          "x-nvidia-gpu-attestation-report-parsed": true,
          "x-nvidia-gpu-nonce-match": true,
          "x-nvidia-gpu-vbios-rim-signature-verified": true,
          "x-nvidia-gpu-driver-rim-signature-verified": true,
          "x-nvidia-gpu-arch-check": true,
          "x-nvidia-attestation-warning": null,
          "x-nvidia-gpu-measurements-match": false,
          "x-nvidia-mismatch-indexes": [
            9
          ],
          "x-nvidia-gpu-attestation-report-signature-verified": true,
          "x-nvidia-gpu-vbios-rim-schema-validated": true,
          "x-nvidia-gpu-driver-rim-cert-validated": true,
          "x-nvidia-gpu-vbios-rim-schema-fetched": true,
          "x-nvidia-gpu-vbios-rim-measurements-available": true,
          "x-nvidia-gpu-driver-rim-driver-measurements-available": true
        },
        "x-nvidia-ver": "1.0",
        "x-nvidia-gpu-driver-version": "535.104.05",
        "hwmodel": "GH100 A01 GSP BROM",
        "oemid": "XXXXXXXXXXXXXXXX",
        "measres": "comparison-fail",
        "x-nvidia-eat-ver": "EAT-21",
        "ueid": "XXXXXXXXXXXXXXXXXXXXXXXX",
        "x-nvidia-gpu-vbios-version": "96.00.5E.00.01",
    },
"tdx": {
  "tdx_tee_tcb_svn": "02010600000000000000...",
  "tdx_mrseam": "360304d34a16aace0a18...",
  "tdx_mrsignerseam": "00000000000000000000...",
  "tdx_seam_attributes": "0000000000000000",
  "tdx_td_attributes": "0000000000000000",
  "tdx_xfam": "e718060000000000",
  "tdx_mrtd": "0cc279c02d62414498ef...",
  "tdx_mrconfigid": "00000000000000000000...",
  "tdx_mrowner": "00000000000000000000...",
  "tdx_mrownerconfig": "0000000000000000000...",
  "tdx_rtmr0": "00000000000000000000...",
  "tdx_rtmr1": "00000000000000000000...",
  "tdx_rtmr2": "00000000000000000000...",
  "tdx_rtmr3": "00000000000000000000...",
  "tdx_report_data": "c7f47c17fd8c14c202a1...",
  "tdx_seamsvn": 2,
  "tdx_td_attributes_debug": false,
  "tdx_td_attributes_septve_disable": false,
  "tdx_td_attributes_protection_keys": false,
  "tdx_td_attributes_key_locker": false,
  "tdx_td_attributes_perfmon": false,
  "tdx_is_debuggable": false,
  "tdx_collateral": {
    "qeidcerthash": "b2ca71b8e849d5e79945...",
    "qeidcrlhash": "f454dc1b9bd4ce36c042...",
    "qeidhash": "b12321a4de768005c869...",
    "quotehash": "a5968716ae5509664c97...",
    "tcbinfocerthash": "b2ca71b8e849d5e79945...",
    "tcbinfocrlhash": "f454dc1b9bd4ce36c042...",
    "tcbinfohash": "15861e19a5940adefc8c..."
  },
  "attester_runtime_data": {
    "keys": [
      {
        "e": "AQAB",
        "key_ops": [
    "sign"
        ],
        "kid": "HCLAkPub",
        "kty": "RSA",
        "n": "vBhkFAABBPHqBkjjO_OzQ..."
      },
      {
        "e": "AQAB",
        "key_ops": [
    "encrypt"
        ],
        "kid": "HCLEkPub",
        "kty": "RSA",
        "n": "1G5L4wAAvlkx7USeXpIqG..."
      }
    ],
    "user-data": "00000000000000000000...",
    "vm-configuration": {
      "console-enabled": true,
      "root-cert-thumbprint": "6nZZnYaJc4KqUZ_yvA-...",
      "secure-boot": true,
      "tpm-enabled": true,
      "tpm-persisted": true,
      "vmUniqueId": "A54F896C-CD00-42DF-A84C-..."
    }
  },
  "attester_tcb_status": "UpToDate",
  "attester_tcb_date": "2023-08-09T00:00:00Z"
    }
}
```