1. Extract the executable binary, signature and the certificate from the downloaded .zip file.

1. Extract the public key from the certificate. 

 ```bash
$ openssl x509 -in <certificate>.cer -pubkey -noout > public_key.pem
```

1. Create a hash of the binary.

```bash
    $ openssl dgst -out binaryHashOutput -sha512 -binary <Signed binary file to be verified>
```

1. Verify the signature using the hash of the binary.

```bash
    $ openssl pkeyutl -verify -pubin -inkey public_key.pem -sigfile <signature_file>.sig -in binaryHashOutput -pkeyopt digest:sha512 -pkeyopt rsa_padding_mode:pss
```

