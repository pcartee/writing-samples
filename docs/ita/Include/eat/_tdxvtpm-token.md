The following composite attestation token was collected after running 
``` ./trustauthority-cli attest --aztdx --tpm --no-verifier-nonce```

``` json
{
  "tdx": {
    "tdx_tee_tcb_svn": "020106000000000000000000000...",
    "tdx_mrseam": "360304d34a16aace0a18e09a00000000...",
    "tdx_mrsignerseam": "00000000000000000000000000...",
    "tdx_seam_attributes": "00000000000000000000000...",
    "tdx_td_attributes": "0000000000000000000000000...",
    "tdx_xfam": "e718060000000...",
    "tdx_mrtd": "0cc279c02d62414498ef4455822f2aea53...",
    "tdx_mrconfigid": "0000000000000000000000000000...",
    "tdx_mrowner": "0000000000000000000000000000000...",
    "tdx_mrownerconfig": "0000000000000000000000000...",
    "tdx_rtmr0": "000000000000000000000000000000000...",
    "tdx_rtmr1": "000000000000000000000000000000000...",
    "tdx_rtmr2": "000000000000000000000000000000000...",
    "tdx_rtmr3": "000000000000000000000000000000000...",
    "tdx_report_data": "c7f47c17fd8c14c202a1b04a978...",
    "tdx_seamsvn": 2,
    "tdx_td_attributes_debug": false,
    "tdx_td_attributes_septve_disable": false,
    "tdx_td_attributes_protection_keys": false,
    "tdx_td_attributes_key_locker": false,
    "tdx_td_attributes_perfmon": false,
    "tdx_is_debuggable": false,
    "tdx_collateral": {
      "qeidcerthash": "b2ca71b8e849d5e799451b4bfe43159a0ee548032...",
      "qeidcrlhash": "f454dc1b9bd4ce36c04241e2c8c37a2ae26b077f2c...",
      "qeidhash": "b12321a4de768005c869734aba3bea2cef5a5aaa06115...",
      "quotehash": "c9ca86a915eeee8490855eb32cde90fe0a342a0a8e2d...",
      "tcbinfocerthash": "b2ca71b8e849d5e799451b4bfe43159a0ee548...",
      "tcbinfocrlhash": "f454dc1b9bd4ce36c04241e2c8c37a2ae26b077...",
      "tcbinfohash": "15861e19a5940adefc8c1c8a6071f83ba697df11a2..."
    },
    "claims": null,
    "attester_runtime_data": {
      "keys": [
        {
          "e": "AQAB",
          "key_ops": [
            "sign"
          ],
          "kid": "HCLAkPub",
          "kty": "RSA",
          "n": "vBhkFAABBPHqBkjjO_OzQBeZQkxfzcFiPaIqoKiLg2Ye9M0..."
        },
        {
          "e": "AQAB",
          "key_ops": [
            "encrypt"
          ],
          "kid": "HCLEkPub",
          "kty": "RSA",
          "n": "1G5L4wAAvlkx7USeXpIqGvfirE5W6iEdN7htk6SZNg6kt6BaaSrJ..."
        }
      ],
      "user-data": "000000000000000000000000000000000000000000000000...",
      "vm-configuration": {
        "console-enabled": true,
        "root-cert-thumbprint": "6nZZnYaJc4KqUZ_yvA-mucFdYNouvlPnITn...",
        "secure-boot": true,
        "tpm-enabled": true,
        "tpm-persisted": true,
        "vmUniqueId": "A54F896C-CD00-42DF..."
      }
    },
    "attester_tcb_status": "UpToDate",
    "attester_tcb_date": "2023-08-09T00:00:00Z",
    "attester_type": "TDX",
    "verifier_instance_ids": [
      "357a11dd-b02e-47df-...",
      "bda9d175-6cf3-421f-...",
      "e39d6d47-ff17-4aee-...",
      "28d987c0-7ba5-4668-...",
      "8554904b-1332-4cd8-..."
    ],
    "dbgstat": "disabled",
    "intuse": "generic",
    "ver": "1.0.0"
  },
  "tpm_claims": {
    "claims": {
      "ak_certificate_hash": "",
      "pcr_records": [
        {
          "algorithm": "SHA-1",
          "hash": "82d6759c283acd5cd6286cc2...",
          "index": 0
        },
        {
          "algorithm": "SHA-1",
          "hash": "46c9702a6c714dcbddc0a8686...",
          "index": 1
        },
        {
          "algorithm": "SHA-1",
          "hash": "b2a83b0ebf2f8374299a5b2bdf...",
          "index": 2
        },
        {
          "algorithm": "SHA-1",
          "hash": "b2a83b0ebf2f8374299a5b2bdfc...",
          "index": 3
        },
        {
          "algorithm": "SHA-1",
          "hash": "2eb5e2ed47d1966cb603b1efb36...",
          "index": 4
        },
        {
          "algorithm": "SHA-1",
          "hash": "0c15af32184d9c01f80a7b2dba0...",
          "index": 5
        },
        {
          "algorithm": "SHA-1",
          "hash": "e8edc1d14d92b6addc44707aad1...",
          "index": 6
        },
        {
          "algorithm": "SHA-1",
          "hash": "61599eb17a833c34dcc388c06231...",
          "index": 7
        },
        {
          "algorithm": "SHA-1",
          "hash": "0000000000000000000000000000...",
          "index": 8
        },
        {
          "algorithm": "SHA-1",
          "hash": "befda6e9c411b9f579f3ac1d1400...",
          "index": 9
        },
        {
          "algorithm": "SHA-1",
          "hash": "5eb75218f1ba9b2b2aea9adb2ee...",
          "index": 10
        },
        {
          "algorithm": "SHA-1",
          "hash": "0000000000000000000000000000...",
          "index": 11
        },
        {
          "algorithm": "SHA-1",
          "hash": "2a6d6d4124b1ec83a4d5a69111fb...",
          "index": 12
        },
        {
          "algorithm": "SHA-1",
          "hash": "0000000000000000000000000000...",
          "index": 13
        },
        {
          "algorithm": "SHA-1",
          "hash": "77db66d60aa0c2cd1cea6c34fed4...",
          "index": 14
        },
        {
          "algorithm": "SHA-1",
          "hash": "0000000000000000000000000000...",
          "index": 15
        },
        {
          "algorithm": "SHA-1",
          "hash": "00000000000000000000000000000...",
          "index": 16
        },
        {
          "algorithm": "SHA-1",
          "hash": "fffffffffffffffffffffffffffff...",
          "index": 17
        },
        {
          "algorithm": "SHA-1",
          "hash": "fffffffffffffffffffffffffffff...",
          "index": 18
        },
        {
          "algorithm": "SHA-1",
          "hash": "fffffffffffffffffffffffffffff...",
          "index": 19
        },
        {
          "algorithm": "SHA-1",
          "hash": "fffffffffffffffffffffffffffff...",
          "index": 20
        },
        {
          "algorithm": "SHA-1",
          "hash": "ffffffffffffffffffffffffffffff...",
          "index": 21
        },
        {
          "algorithm": "SHA-1",
          "hash": "fffffffffffffffffffffffffffffff...",
          "index": 22
        },
        {
          "algorithm": "SHA-1",
          "hash": "0000000000000000000000000000000...",
          "index": 23
        },
        {
          "algorithm": "SHA-256",
          "hash": "f70272c29c9fd4b76eab8441a768787...",
          "index": 0
        },
        {
          "algorithm": "SHA-256",
          "hash": "606196e22d38d5abd246d455db678c88...",
          "index": 1
        },
        {
          "algorithm": "SHA-256",
          "hash": "3d458cfe55cc03ea1f443f1562beec8df...",
          "index": 2
        },
        {
          "algorithm": "SHA-256",
          "hash": "3d458cfe55cc03ea1f443f1562beec8df5...",
          "index": 3
        },
        {
          "algorithm": "SHA-256",
          "hash": "53da3283cde884f0985cfea595df251f17...",
          "index": 4
        },
        {
          "algorithm": "SHA-256",
          "hash": "8486892e36cf093952a90e8b53ff73abad...",
          "index": 5
        },
        {
          "algorithm": "SHA-256",
          "hash": "f1ea4ff450d0c65fa9fa704c3b61fd9b4c...",
          "index": 6
        },
        {
          "algorithm": "SHA-256",
          "hash": "eb683d3fe52c5eb33a6302c3a868b917eb...",
          "index": 7
        },
        {
          "algorithm": "SHA-256",
          "hash": "0000000000000000000000000000000000...",
          "index": 8
        },
        {
          "algorithm": "SHA-256",
          "hash": "cae36ff4d6352815370b97655c0d23b242...",
          "index": 9
        },
        {
          "algorithm": "SHA-256",
          "hash": "19f27b73c762906c7f7fadf11d641409b8...",
          "index": 10
        },
        {
          "algorithm": "SHA-256",
          "hash": "0000000000000000000000000000000000...",
          "index": 11
        },
        {
          "algorithm": "SHA-256",
          "hash": "f1a142c53586e7e2223ec74e5f4d1a4942...",
          "index": 12
        },
        {
          "algorithm": "SHA-256",
          "hash": "0000000000000000000000000000000000...",
          "index": 13
        },
        {
          "algorithm": "SHA-256",
          "hash": "e3991b7ddd47be7e92726a832d6874c5349...",
          "index": 14
        },
        {
          "algorithm": "SHA-256",
          "hash": "00000000000000000000000000000000000...",
          "index": 15
        },
        {
          "algorithm": "SHA-256",
          "hash": "00000000000000000000000000000000000...",
          "index": 16
        },
        {
          "algorithm": "SHA-256",
          "hash": "ffffffffffffffffffffffffffffffffffff...",
          "index": 17
        },
        {
          "algorithm": "SHA-256",
          "hash": "ffffffffffffffffffffffffffffffffffff...",
          "index": 18
        },
        {
          "algorithm": "SHA-256",
          "hash": "ffffffffffffffffffffffffffffffffffff...",
          "index": 19
        },
        {
          "algorithm": "SHA-256",
          "hash": "fffffffffffffffffffffffffffffffffffff...",
          "index": 20
        },
        {
          "algorithm": "SHA-256",
          "hash": "ffffffffffffffffffffffffffffffffffffff...",
          "index": 21
        },
        {
          "algorithm": "SHA-256",
          "hash": "fffffffffffffffffffffffffffffffffffffff...",
          "index": 22
        },
        {
          "algorithm": "SHA-256",
          "hash": "0000000000000000000000000000000000000000...",
          "index": 23
        }
      ]
    },
    "attester_tcb_status": "UpToDate",
    "attester_tcb_date": "",
    "attester_type": "TPM",
    "verifier_instance_ids": [
      "1b550968-5d76-...",
      "0430f33e-bc99-...",
      "28d987c0-7ba5-...",
      "8554904b-1332-..."
    ],
    "ver": "v1.0.0"
  },
  "exp": 1713900257,
  "jti": "7e615321-fd9b-...",
  "iat": 1713899957,
  "iss": "Intel Trust Authority",
  "nbf": 1713899957
}

```