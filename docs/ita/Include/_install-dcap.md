**Data Center Attestation Primitives — DCAP**

Intel SGX requires DCAP libraries to create the SGX quoting enclave used to provide quotes for application enclaves. These libraries must be available to the SGX-enabled application. Intel maintains an open source DCAP reference. Other providers (such as cloud service providers) may provide their own version of DCAP.

[DCAP quick install guide](https://www.intel.com/content/www/us/en/developer/articles/guide/intel-software-guard-extensions-data-center-attestation-primitives-quick-install-guide.html)
  
**Ubuntu SGX-related dependencies:**  

```bash
sudo apt-get install -y libcurl4-openssl-dev \
    libprotobuf-c-dev protobuf-c-compiler protobuf-compiler \
    python3-cryptography python3-pip python3-protobuf
```

**Installing Intel DCAP for Ubuntu**  

```bash
# Add the Intel SGX software repo 
curl -fsSL https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | sudo apt-key add -
echo 'deb [arch=amd64] https://download.01.org/intel-sgx/sgx_repo/ubuntu focal main' | sudo tee /etc/apt/sources.list.d/intel-sgx.list
# ("focal" above refers to Ubuntu 20.x.  If using a later version of Ubuntu, replace "focal" with the appropriate codename)

# Install the DCAP package
sudo apt-get update
sudo apt-get install libsgx-dcap-quote-verify-dev
```
