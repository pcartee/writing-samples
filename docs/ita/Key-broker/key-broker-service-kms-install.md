---
title: Hashicorp Vault Installation
description: Hashicorp Vault Installation
author: carteepaul
topic: kbs
date: 04/14/2025
uid: kms.install
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

*· 04/14/2025 ·*

## Key Management Service installation

A Key Management Service (KMS) must be installed before installing the Key Broker System (KBS). The Intel KBS is compatible with two key management systems, Hashicorp Vault and PyKMIP. Select the proper key management system for your environment and follow the instructions.

<Tabs>
<TabItem value="hashicorp-config" label="Hashicorp vault KMS configuration">

### Hashicorp vault KMS configuration

1. Install Vault according to the instructions provided here: https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-install.

1. Create a Vault server config file: https://developer.hashicorp.com/vault/docs/configuration.

1. Start the Vault server: https://developer.hashicorp.com/vault/docs/commands/server.

1. Initialize the Vault server: https://developer.hashicorp.com/vault/docs/commands/server. Securely store/save the keys.

1. Unseal the Vault server: https://developer.hashicorp.com/vault/docs/commands/operator/unseal.

1. Login to Vault by running the following command:

   ```bash
   vault login <root-token>
   ```

1. Enable a kv secrets engine for KBS to use.

    ```bash
   vault secrets enable -path=keybroker kv
    ```

1. In the KBS config file, add the following Vault server information:

    ```bash
    VAULT_SERVER_IP=<vault server IP address>
    VAULT_SERVER_PORT=<vault port number; default 8200>
    VAULT_CLIENT_TOKEN=<vault root token>
    ```

</TabItem>
<TabItem value="pymip-config" label="PyKMIP configuration">

### PyKMIP configuration

:::important
The user must create all the certificates/keys required for KBS-PyKMIP communication. Intel KBS only reads the configuration file provided by the user and, therefore, uses the communication type defined by the user in that file.
:::

1. Follow the instructions at https://pykmip.readthedocs.io/en/latest/installation.html to install PyKMIP.

1. Create server certificates and configure the server as provided in the instructions here: https://pykmip.readthedocs.io/en/latest/server.html.

1. In the KBS config file, add the following PyKMIP server information:

    ```bash
    KMIP_CLIENT_KEY_PATH=<path to KMIP client key>
    KMIP_ROOT_CERT_PATH=<path to KMIP root certificate>
    KMIP_CLIENT_CERT_PATH=<path to KMIP client certificate>
    KMIP_SERVER_IP=<KMIP server IP address>
    KMIP_SERVER_PORT=<KMIP server port number>
    KMIP_HOSTNAME=hostname where KMIP is running
    KMIP_USERNAME=KMIP server username
    KMIP_PASSWORD=KMIP password
    KMIP_VERSION=KMIP version
    ```

</TabItem>
</Tabs>
