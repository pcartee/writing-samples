---
title: Integrity Measurement Architecture (IMA) logs
description: An overview of Integrity Measurement Architecture (IMA) logs and how to verify the application's integrity using IMA logs with Intel Trust Authority.
author: pcartee
topic: IMA logs
date: 11/14/2024
uid: ima-log 
---

*· 10/25/2024 ·*

## Integrity Measurement Architecture (IMA)

The Linux Integrity Measurement Architecture (IMA) is a security subsystem in the Linux kernel that includes three main features: IMA-Measurement, IMA-Appraisal, and IMA-Audit. These features are activated based on IMA Policy rule actions. Intel® Trust Authority can include IMA event logs in TPM attestations.

:::note
IMA generates event logs using the hash algorithm set by kernel modules. The default kernel modules for most current distributions use SHA-256 (for example, Ubuntu 24.04), but some OS versions still in wide use will by default use SHA-1 (for example, Ubuntu 20.04). For event log replays to work correctly, the same algorithm must be enabled in the TPM PCR banks. Support for different TPM PCR banks differs by OEM. Some manufacturers allow multiple PCR banks to be enabled at the same time, while others only allow a single PCR bank to be enabled. Where possible, Intel recommends enabling all PCR banks on the TPM, as this will generally ensure that the PCR bank matching the event log algorithm is always available. Where this is not possible, check the kernel flags enabled for your system.

 ```bash
 cat /boot/config-$(uname -r) | grep CONFIG_IMA_DEFAULT_HASH

 # CONFIG_IMA_DEFAULT_HASH_SHA1 is not set
 CONFIG_IMA_DEFAULT_HASH_SHA256=y
```

In this example, the IMA default hash algorithm is set to SHA-256. For event log replays to work correctly, the SHA-256 PCR bank must be enabled on the TPM.

Also note that the `pcr_slections` setting in the `config.json` configuration file defines the PCR bank that the attestation client CLI will use. This must match the algorith used for any event logs, so that the attestation client CLI picks the correct PCR bank for use in the event log replay.
:::

## IMA boot-time vs. runtime measurement

Boot-time measurements focus on the system's initial state, while runtime measurements focus on maintaining integrity during normal operation. Boot-time measurements are only updated when the system is booted. Runtime measurements can be extended while the system is powered on.

### IMA runtime measurements

Runtime measurements are taken during the regular operation of the system. These measurements help ensure the system remains in a known good state during its operation and no unauthorized modifications occur. IMA runtime measurements typically include measuring the integrity of the following:

- Executable files loaded and executed
- Critical configuration files read during runtime
- Kernel modules loaded after the initial boot process
- Scripts executed
- Data files accessed by applications

IMA generates event logs for each triggered measurement event. These logs represent an ordered list of all measurements extended to the TPM. During attestation, the verifier (Intel Trust Authority) "replays" the event logs to verify that the final resulting measurement matches the actual PCR value. If these values match, the event log integrity is verified, and the log content can be trusted for use with appraisal policies.

If the event log replay does not match the PCR value, the event log is untrustworthy, and its integrity cannot be verified. This will result in an error during attestation.

You must provision an IMA policy to determine what files or resources need to be measured to satisfy your security needs. The IMA policy is configured on the system to be attested (the "attester"), and differs from appraisal policies configured using Intel Trust Authority.

IMA policy:
- Configured on the attester (the system with a TPM), using a text file provisioned to `/etc/ima/ima-policy`
- Determines which files on the system will be measured, and under what conditions the measurement will be repeated

Appraisal policy:
- Configured on the verifier (Intel Trust Authority) using Rego policy language
- Determines required claims values in an attestation token to indicate that the policy matches

Attestation of a TPM including IMA logs requires setting both an IMA policy on the attester to measure the desired files, and configuring an appraisal policy using Intel Trust Authority to assert the expected values of those measured files.

### Integrity Measurement Architecture (IMA) documentation

To learn more about configuring IMA and understanding IMA policies, see the [Integrity Measurement Architecture (IMA)](https://sourceforge.net/p/linux-ima/wiki/Home/) wiki page.

## Configure an Azure Confidential VM for vTPM attestation with IMA

1. Create an Azure confidential virtual machine (CVM) with Intel TDX. Azure's vTPM uses Intel TDX as its root of trust, and IMA is enabled by default on Azure confidential VMs. However, you must add an IMA policy to measure anything other than the default TCB policy.

:::note
See the [Intel TDX Attestation on Microsoft Azure](<../../Tutorials and examples/Intel Trust Authority Client examples/tutorial-tdx.md>) tutorial for guidance on how to build an Azure CVM with the required features enabled.
:::

1. Install the Intel Trust Authority attestation client CLI on the new Azure confidential VM.

```sh
curl https://raw.githubusercontent.com/intel/trustauthority-client-for-go/main/release/install-tdx-cli-azure.sh | sudo bash - 
```

1. Configure the attestation client CLI.

You must configure certain properties before using the token and verify commands. The properties and values are saved as JSON in config.json. Create `~/config.json` with the following content:

```json
{
    "cloud_provider": "azure"
    "trustauthority_url": "https://portal.trustauthority.intel.com",
    "trustauthority_api_url": "https://api.trustauthority.intel.com",
    "trustauthority_api_key": "<trustauthority attestation api key>",
    "tpm": {
        "owner_auth": "",
        "ak_handle": "81000003"
        "pcr_selections": "sha1:10+sha256:all"
    }
}
```

The "cloud_provider": is needed only for Microsoft Azure. Owner_auth is the TPM owner password, and ak_handle is the TPM attestation key handle. For this release, the owner_auth is an empty string, and the ak_handle is hardcoded to 81000003, which is the location of the Azure-provisioned AK in the vTPM. The pcr_selections field specifies which PCRs to include in the attestation token. The default is all SHA256 PCRs, however, IMA replay won't verify if SHA1 PCR10 isn't included.

This config file is used when executing the attestation client CLI.

### Configure an IMA policy on the Azure confidential VM

An IMA policy is needed to tell the system which files need to be measured and under what circumstances. As an example, we will create an IMA policy that measures all files executed by a specific user.

#### Create a user

The user "imajean" is created solely for demonstration purposes. The IMA policy outlined in these instructions requires a UID, hence the creation of this user. The user "imajean" will execute the workload and be utilized in the IMA policy to replay issues and mitigate log size.

1. `sudo useradd -m imajean`

1. `sudo passwd imajean` (enter password)

1. `sudo id imajean` (apply to the ima-policy.txt below; in this example assume that the uid is "1001")

1. `sudo usermod -aG tss imajean` (grant access to the TPM)

#### Grant read access to IMA log files

Grant read access to the IMA logs for the TSS group so "imajean" can read them.

1. `sudo chgrp tss /sys/kernel/security/ima/ascii_runtime_measurements`

1. `sudo chmod g+r /sys/kernel/security/ima/ascii_runtime_measurements`

#### Deploy the trustauthority-cli and configuration to the "imajean" user's home directory

1. `sudo cp trustauthority-cli /home/imajean`

1. `sudo cp config.json /home/imajean`

1. `sudo chown -R imajean:imajean /home/imajean/trustauthority-cli`

1. `sudo chown -R imajean:imajean /home/imajean/config.json`

#### Create "ima-policy.txt" in the "imajean" user's home directory

This IMA policy is based on the default "TCB" policy with additions for monitoring processes run by the "uuid" created above. This configures IMA so that it measures all files executed by the "imajean" user.

:::note
For more information on IMA policies, see the [IMA Recipes](https://wiki.gentoo.org/wiki/Integrity_Measurement_Architecture/Recipes) page.
:::

:::warning
Copying and pasting the policy below may alter its formatting. Ensure there are no spaces before the text in the file. Verify the formatting before using it. Improperly formatted IMA policies can prevent the system from booting.
:::

```bash
# https://wiki.gentoo.org/wiki/Integrity_Measurement_Architecture/Recipes
# PROC_SUPER_MAGIC = 0x9fa0
dont_measure fsmagic=0x9fa0
# SYSFS_MAGIC = 0x62656572
dont_measure fsmagic=0x62656572
# DEBUGFS_MAGIC = 0x64626720
dont_measure fsmagic=0x64626720
# TMPFS_MAGIC = 0x01021994
dont_measure fsmagic=0x1021994
# DEVPTS_SUPER_MAGIC=0x1cd1
dont_measure fsmagic=0x1cd1
# BINFMTFS_MAGIC=0x42494e4d
dont_measure fsmagic=0x42494e4d
# SECURITYFS_MAGIC=0x73636673
dont_measure fsmagic=0x73636673
# SELINUX_MAGIC=0xf97cff8c
dont_measure fsmagic=0xf97cff8c
# SMACK_MAGIC=0x43415d53
dont_measure fsmagic=0x43415d53
# CGROUP_SUPER_MAGIC=0x27e0eb
dont_measure fsmagic=0x27e0eb
# CGROUP2_SUPER_MAGIC=0x63677270
dont_measure fsmagic=0x63677270
# NSFS_MAGIC=0x6e736673
dont_measure fsmagic=0x6e736673 
dont_measure func=MMAP_CHECK mask=MAY_EXEC 
dont_measure func=FILE_CHECK mask=MAY_READ uid=0 
dont_measure func=MODULE_CHECK 
dont_measure func=FIRMWARE_CHECK

# measure kernel and initramfs
measure func=KEXEC_KERNEL_CHECK
measure func=KEXEC_INITRAMFS_CHECK 

# This is the actual addition made for this example. This policy will not measure the execution of binaries by the root user (uid=0) but will measure the execution of binaries by the "imajean" user (uid=1001). This setup is useful for monitoring the integrity of a specific user's workload without collecting too much data.
dont_measure func=BPRM_CHECK mask=MAY_EXEC uid=0
measure func=BPRM_CHECK mask=MAY_EXEC uid=1001
```

:::note
The "uid=1001" in the "ima-policy.txt" file is the ID of the user "imajean" created above. Only files executed by "imajean" will be measured. Other users can execute any number of files without triggering an IMA measurement. Ensure that any user being used to execute files whose integrity needs to be measured matches the UID in the IMA policy.
:::

1. Deploy the ima-policy. The file `/etc/ima/ima-policy` defines the measurements IMA will record on the next boot.

`sudo cp ima-policy.txt /etc/ima/ima-policy`

1. Reboot the Azure VM from the control panel to ensure the system starts with the new policy.

#### Verify the IMA policy

Validate the IMA policy to ensure that the policy is correctly applied and functioning as intended.

1. After reboot, inspect the IMA logs:

`sudo cat /sys/kernel/security/ima/ascii_runtime_measurements`

1. Run a process as the "imajean" user to generate IMA log entries:

   1. `su - imajean (password)`

   1. `ls` Listing directories will generate an IMA log entry for the "ls" binary.

   1. `exit` Exiting will generate an IMA log entry.
  
1. Confirm the ima-policy is working as expected (`cat /sys/kernel/security/ima/ascii_runtime_measurements`) should include "/usr/bin/ls".

```bash
10 98aa9e41ffe519d74f9a8d20f5f9fdad8b998855 ima-ng sha1:7448a72f7519d1d1564a2456bc178b30673836d6 /usr/bin/ls
```

### Author an appraisal policy for IMA measurements

These instructions explain how to collect reference values from the token created in the previous step and use them to configure an appraisal policy on Intel Trust Authority.

1. Collect reference values from token claims. We create a new attestation token using the system for which we have just successfully configured an IMA policy. This will ensure the IMA logs containing the measurements in our example will show up in the token claims.

:::note
Be sure to log in as the "imajean" user first. This will ensure the files executed are measured by the IMA policy.
:::

```sh
# Azure Confidential VM with vTPM:
sudo ./trustauthority-cli token --tdx --tpm --ima -c config.json

# Physical TPM or vTPM not dependent on Intel TDX:
sudo ./trustauthority-cli token --tpm --ima -c config.json
```

1. The returned token is base64 encoded. Decode the token to make it human-readable so you can retrieve the claims.

```json
  ...other token claims...
  "runtime_measurements": [
    {
      "alg": "SHA-1",
      "index": 10,
      "cumulative_hash": "6128FC2C16F02D...",
      "measurements": [
        {
          "file_path": "/usr/bin/trustauthority-cli",
          "digest": "c25e74f77e121e7a61429..."
        }
```

1. Use token claims to build an appraisal policy (see sample policy below).

```sh
import rego.v1

default valid_runtime_measurements = false
valid_runtime_measurements = true {
  input.tdx.tdx_mrtd == "b4f3e2748d800711d81fa75d5b4fee1e9..."
  input.tdx.tdx_seamsvn == 4

# The above section of the policy verifies the integrity of the trust domain. The TD in Azure includes the vTPM, so this measurement is needed to maintain the chain-of-trust for Azure confidential VMs. To trust the IMA measurements, we need to trust the TPM. To trust the TPM, we need to trust the TD. Note that this tdx_mrtd measurement will be uniform across all Azure Confidential VMs for a given version; if Azure updates the TD version, this measurement will change, and the policy needs to be updated. Capture the value from the token; the claim name is "tdx_mrtd". This section is not necessary for physical TPMs or vTPMs that do not depend on Intel TDX.

# Example: "tdx_mrtd": "bb379...f2de0d7154"

default ima_cli_rtm_match := false
ima_cli_rtm_match if {
  ima_rtm_match(input.tpm.runtime_measurements, 10, "/home/imajean/trustauthority-cli", "753a72acc9828e99ad8f1b37b8954471e31803f6fee66fda6bad09ecd3dfa534")
}

# The section above invokes the "ima_rtm_match" function, which is defined below. It passes the IMA event log from the "tpm.runtime_measurements" claim, sets the TPM PCR index to 10 (where IMA extends measurements), sets the event file path to "/home/imajean/trustauthority-cli", and asserts the required measurement.

ima_rtm_match(runtime_measurements, idx, fp, dig) := r if {
  fp_digests := [ digest |
    some _, m in [measurements |runtime_measurements[i].index == idx
      measurements := runtime_measurements[i].measurements[_]
    ]
    m.file_path == fp
    digest = m.digest
  ]

  cnt := count(fp_digests)
  cnt > 0
  r := fp_digests[cnt-1] == dig
}

# The "ima_rtm_match" function iterates over the array of event log measurements for the specified PCR index and finds events where the file path matches. It then checks only the latest event if multiple measurements of the same file path are present. Because IMA measurements are triggered during runtime whenever the specified file is executed, this function ensures that older, matching measurements are disregarded and it only checks the most recent measurement of that file. This way the policy will detect changes to the executable. Note that only changes in the measurement are recorded (so repeated executions of the same binary with the same hash measurement will be represented by just one measurement event) and that attestation must still be triggered for the appraisal policy to be evaluated. In this example the policy is checking the attestation client CLI, so every attestation request is also verifying the integrity of the client that provided the evidence.
```

1. Use this file (with real digest values captured from the attestation token claims and without comments) to create a new appraisal policy using the [Intel Trust Authority web UI](<../../How-to workflows/howto-manage-attestation-policies.md>) or the [tenant management CLI](../../Command-line/cli-policy-commands.md).

### Demonstrate Attestation

Run trustauthority-cli as the "imajean" user and inspect token claims to verify the policy.

1. Log in to the Azure confidenctial VM as the "imajean" user.
  
```bash
su - imajean (provide password)
```

1. Run the following command to attest the system using the new IMA appraisal policy.

```bash
./trustauthority-cli token --tdx --tpm --ima -c config.json --policy-ids <appraisal policy UUID>
```

The output includes details such as the EAT profile, intended use, matched policy IDs, and unmatched policy IDs.

```bash
  ...
  "policy_ids_matched": [
    {
      "id": "<appraisal policy UUID>",
      "version": "v1",
      "hash": "bkxNYT...2dNazczNVJFbnFBZA=="
    }
  ],
  "policy_ids_unmatched": null,
```

By verifying that the policy is in the `policy_ids_matched` array, we confirm that the evidence provided matches the assertions in the policy. In our sample policy, this means that we've verified the Intel TDX Trust Domain as the root of trust for the Azure vTPM; we've verified the boot-time integrity of all measurements extended to PCR4, including the VM's OS kernel; we've verified the vTPM event log integrity; and we've verified the execution-time integrity of the Intel Trust Authority attestation client CLI.

### Sample IMA token claim

The sample IMA token claim in JSON format includes details about TPM, PCRs and runtime measurements.

```json
tpm {
  "pcrs": [
    ...
    {
      "alg": "SHA-1",
      "digest": "6128FC2C16F02D...",
      "index": 10
    }
  ],
  "runtime_measurements": [
    {
      "alg": "SHA-1",
      "index": 10,
      "cumulative_hash": "6128FC2C16F02D...",
      "measurements": [
        {
          "file_path": "/usr/bin/trustauthority-cli",
          "digest": "c25e74f77e121e7a61429..."
        }
        ...
```

### Sample IMA evidence

IMA event logs located in `/sys/kernel/security/ima/ascii_runtime_measurements` have six fields separated by spaces. The fields are as follows:

- **10** - The PCR index
- **92bbbb...** The PCR value before the measurement was extended
- **ima-ng** - The event, in this case, Integrity Measurement Architecture Next Generation. The ima-gn format includes a hash algorithm identifier and the hash value of the object
- **sha-1** - The sha algorithm used to hash the object
- **47f202...** - The hash value of the measured object
- **/usr/lib/modules/6.5** - the path to the file that ws measured

```sh
10 92bbbbbb24cdc02f01bb139cbd73fa7d51111958 ima-ng sha1:47f2024b02af118e838ad61aa915b078755aa85c boot_aggregate
10 9a2a67974ba6a9be1a6e5592912e2a14dfe90be5 ima-ng sha1:fd957dec0fcd03e32ada63fd3953599eaf53e679 /usr/bin/bash
10 b9e605c844d52bcbefb07aac6cc7a70377cf55bc ima-ng sha1:c434fdbf2ec9d659c2ba76cf6a23b97d78ec16b1 /usr/bin/groups
10 d6ca063aab29ed50c199f5174b2e068c47876e9a ima-ng sha1:5629b219107447a0bd948100e5eafd82180eba4b /usr/bin/lesspipe
10 042c9ed10b091c35a5e75aa3350ef4583e942c6e ima-ng sha1:42e94914c7800c7063c51d7a17aec3a2069a3769 /usr/bin/dash
...
```

### Sample IMA claims in an attestation token

The IMA event log claims will be in the "tpm" section listed as "runtime_measurements" in an attestation token issued by Intel Trust Authority. This array will contain the same data as the IMA event log located in `/sys/kernel/security/ima/ascii_runtime_measurements` for the attester whose evidence was used to generate the attestation token.

```json
  ...
  "runtime_measurements": [
    {
      "alg": "SHA-1",
      "index": 10,
      "cumulative_hash": "6128FC2C16F02D...",
      "measurements": [
        {
          "file_path": "/usr/bin/bash",
          "digest": "c25e74f77e121e7a61429..."
        },
        {
          "file_path": "/usr/bin/groups",
          "digest": "c434fdbf2ec9d65..."
        },
        ...
```
