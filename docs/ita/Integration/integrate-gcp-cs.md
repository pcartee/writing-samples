---
title: Integrating GCP Confidential Space with Intel Trust Authority
description: GCP CS workload development with Intel Trust Authority attestation
author: pcartee
topic: integration
date: 05/10/2025
uid: integrate.gcp.cs
#
---
*· 05/10/25 ·*

## Using GCP Confidential Space with Intel Trust Authority

:::note
This feature is in GA status for Intel® Tiber™ Trust Authority. However, the corresponding Google deployment to support Intel Trust Authority attestation for Confidential Space is currently in _preview_ status. Contact your Google Cloud representative for preview access.
:::

Google Cloud Platform\* (GCP) Confidential Space\* (CS) provides a method for isolating a workload and sensitive data ensuring that data is released only to authorized workloads. GCP CS provides isolation between data owners (data owners can't see each other's data) and workload owners (can't see the data), and isolation from the platform operators (can't examine the workload or the data).

In the basic CS workflow, one or more data collaborators own protected data or other resources, which they will not release until certain conditions are met. The workload itself is a containerized image stored in an artifact registry that won't release the image until its own conditions are met. 

The containerized workload runs on a Confidential Virtual Machine (CVM) with Intel TDX (the TEE). Intel® Tiber™ Trust Authority is used to validate the evidence. Platform evidence from Intel TDX, the TPM, and event logs collected by the CS launcher component, signed, and sent to Intel Trust Authority for validation and attestation. Intel Trust Authority returns an OpenID Connect (OIDC) compliant attestation token if CVM attestation succeeds. If attestation of the Intel TDX CVM fails, no token will be released.

Intel Trust Authority also verifies the evidence against the known-good reference integrity measurements (RIM) provided by Google. The RIM claims evaluated include **MRTD**, which mainly indicates that the CVM is using the known-good firmware, and measurements of the CVM image to verify that the CVM is running the known-good image. 

During the Google preview period, an attestation token will be released if the Intel TDX attestation passes and RIM verification fails. In that case, the **swname** claim in the token will contain "GCE" instead of "CONFIDENTIAL_SPACE". If **swname** contains "CONFIDENTIAL_SPACE" it indicates that the CVM has passed both attestation and RIM verification. After Google concludes the preview phase, the behavior will change so that no attestation token is issued if either the Intel TDX verification or RIM verification fails. 

The attestation token is evaluated by using attribute (claims) conditions set in the Workload Identity Pool (WIP). The WIP is configured with one or more providers and service accounts that can access the protected data or workload resources. After the CVM/TEE is attested by Intel Trust Authority and the token claims (attributes) have met certain conditions, the WIP authorizes access to protected resources. WIP authorization is the access credential release step to unlock protected resources.

Using Intel Trust Authority as the attestation provider removes Google from the trust boundary for confidential compute on GCP. To that end, Google has made modifications to GCP CS to enable Intel Trust Authority attestation, and Intel Trust Authority adds several new features to support GCP CS:

- An API endpoint to request attestation for Confidential Space TEEs: `/appraisal/v2/attest/gcp/confidentialspace`. For more information, see the [Attestation V2 REST API](../Restapi/restapi-attestation-v2.md). This endpoint is intended for use by GCP CS launcher components.
- A collection of attestation token claims specific to GCP CS, and an OIDC-compliant attestation token output. 
- A Google catalog policy to evaluate the attesting CVM's TCB status. Catalog policy is not visible to the user. There are two components: 
    - A default attestation policy that is applied to every GCP CS CVM to check the TCB status. 
    - A catalog of TCB reference values for each of the hardened OS images (values provided by Google). The catalog is updated when Google updates their images.

The rest of this article assumes that you have a basic working familiarity with GCP CS and the constellation of GCP services that CS relies upon. For more information about Confidential Space, see [Confidential Space overview][cs-overview] in the Google Cloud documentation. The following sections contain the details of launching a CS workload with Intel Trust Authority attestation.

## Workload authoring

To use ITA tokens in your workload you must fetch custom OIDC tokens from the TEE Server in the Confidential Space launcher. For more information, see [Access resources not managed by Google Cloud IAM][cs-access] in the Google Cloud documentation.

Google Confidential Space puts the attestation tokens in well-known locations in the workload container. 

- Google Cloud Attestation token location URL: "http://localhost/v1/token" 
- Intel Trust Authority token location URL: "http://localhost/v1/intel/token"

For detailed information about the claims included in a GCP-compatible OIDC token, see [Attestation token claims][cs-token-claims] in the Google Cloud documentation.

The following snippet (written in Go) shows an example request to retrieve the Intel Trust Authority token. When the token request is posted to the endpoint, a new attestation request is triggered. A full example can be found [here][gh-joshua-sample].

```go
// Construct Request body
body := tokenRequest{
    Audience: audience,
    TokenType: "OIDC",
}

val, err := json.Marshal(body)
if err != nil {...}

// Set up HTTP client
httpClient := http.Client{
    Transport: &http.Transport{
        // Set the DialContext field to a function that creates
        // a new network connection to a Unix domain socket
        DialContext: func(_ context.Context, _, _ string) (net.Conn, error) 
        {
            return net.Dial(unixNetwork, socketPath)
        },
    },
}
// POST to the ITA endpoint
itaPath := "http://localhost/v1/intel/token"
resp, err := httpClient.Post(itaPath, contentType, strings.NewReader(body))
if err != nil { ... }
defer resp.Body.Close()

tokenbytes, err := io.ReadAll(resp.Body)

// Use token to gain access to protected resources

```
## Workload deployment

To deploy your workload, you must deploy a CVM with Intel TDX. Be sure to deploy in an [Intel TDX supported region][gcp-tdx-region].

The following details must be specified when deploying. **Bold** options are specific to
machines with Intel Trust Authority as a verifier.

- **Machine type Intel TDX**
- **An Intel Trust Authority compatible VM image**
- Metadata:
    - **Intel Trust Authority API Key**
    - **Intel Trust Authority Region**
    - Your container image reference
    - (Optional) Logging redirect
- Secure boot enabled
- VM restart policy
- Cloud Zone
- Service account to associate with the machine
- Cloud platform scope
- VM name

The API key must be an attestation API key associated with the region. There are two regions:

- EU — `https://api.eu.trustauthority.intel.com`
- US — `https://api.trustauthority.intel.com`

Additional regions may be supported in the future, but for now EU and US are the only choices. The pilot environment is not available.  The `ita-api-key` and `ita-region` are included in the `--metadata` parameter. For example, `--metadata="^~^ita-api-key=<API_key>=~ita-region=<US|EU>...`.

For more information, see [Deploy workloads][cs-deploy] in the Google Cloud documentation.

Here is a sample deployment command:

```shell
gcloud compute instances create --maintenance-policy=TERMINATE \
--zone=us-west1-a --confidential-compute-type=TDX \
--machine-type=c3-standard-4 --shielded-secure-boot \
--image=https://compute.googleapis.com/compute/v1/projects/confidential-space-images
-dev/global/images/confidential-space-debug-0-presubmit-12ecf60 \
--metadata="^~^ita-api-key=abcdefg123=~ita-region=US~tee-image-reference=asia-east
1-docker.pkg.dev/yourrepo/yourimage:latest~tee-container-log-redirect=true~tee-env-custom_y
ourcustomervarkey=yourcustomvarvalue"
--service-account=svcaccoun1@your-project.iam.gserviceaccount.com
--scopes=cloud-platform \
vmname
```

---
**\*** Other names and brands may be claimed as the property of others.

/* External URLs */
[cs-overview]: https://cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview
[gh-joshua-sample]: https://github.com/JoshuaKrstic/utilities/blob/main/awsintegration/ita/main.go
[cs-access]: https://cloud.google.com/confidential-computing/confidential-space/docs/connect-external-resources
[gcp-tdx-region]: https://cloud.google.com/confidential-computing/confidential-vm/docs/supported-configurations#intel-tdx_1 
[cs-deploy]: https://cloud.google.com/confidential-computing/confidential-space/docs/deploy-workloads
[cs-token-claims]: https://cloud.google.com/confidential-computing/confidential-space/docs/reference/token-claims
