---
title: Key Broker Service Installation
description: Key Broker Service Installation
author: pcartee
topic: KBS
date: 04/14/2025 
uid: kbs.installation
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

*· April/14/2025 ·*

## Key Broker Service installation and configuration

Installing and configuring the Key Broker System (KBS) requires you to follow these steps:

1. [Install and configure the Key Management System (KMS)](key-broker-service-kms-install.md)
1. [Install and configure the KBS](key-broker-service-install.md)
1. [KBS key creation and key retrieval](key-broker-service-key-creation.md)
1. [KBS user management](key-broker-service-user-management.md)

## Prerequisites

- You must have an Trust Authority account set up with access to the Trust Authority Download center
- Hashicorp Vault (Community Edition) or PyKMIP must be installed and running
- Docker Engine installed

## Install the Key Management System (KMS)

KBS works with two KMSs, [Hashicorp Vault](key-broker-service-kms-install.md) and [PyKMIP](key-broker-service-kms-install.md). Follow the installation instructions for the KMS appropriate for your environment:

### Build the KBS

Build the KBS using targets from the Makefile.

`make docker` is used to build the KBS docker image (key-broker-service:v1.0.0) using the Dockerfile.

### Install the KBS

On Linux, follow the steps below to install the KBS:

1. Create directories.

   Create the following directories on the host machine.

   ```bash
   sudo mkdir -p /opt/kbs/users /etc/kbs/certs/tls /opt/kbs/keys /opt/kbs/keys-transfer-policy /etc/kbs/certs/signing-keys
   ```

  :::important
  Data in the KBS directories is not encrypted. These folders should be stored in a protected filesystem.
  :::

1. Configure the KBS.

   Create a kbs.env file with all the configuration variables listed below.

   :::note
   The kbs.env file contains secrets, including the admin user and password and the KMS token or admin password. For improved security, you should remove the kbs.env file after running the KBS container for the first time. The kbs.env isn't needed after the initial configuration.
   :::

   ```bash
   LOG_LEVEL=<DEBUG, INFO, TRACE, ERROR>
   KEY_MANAGER=<VAULT or KMIP, default VAULT> //Chose VAULT is you are using Hashicoprt vault. Chose KMIP if you are using PyKMIP.
   ADMIN_USERNAME=<kbs admin username>
   ADMIN_PASSWORD=<kbs admin password>
   HTTP_READ_HEADER_TIMEOUT=<kbs server read header timeout, default 10sec>
   BEARER_TOKEN_VALIDITY_IN_MINUTES=<kbs auth token validity, default 5 min>
   TRUSTAUTHORITY_API_URL="api.trustauthority.company.com"
   TRUSTAUTHORITY_API_KEY=<Trust Authority API key>
   TRUSTAUTHORITY_BASE_URL="portal.trustauthority.company.com"
   AUTHENTICATION_DEFEND_MAX_ATTEMPTS=<max number of invalid login attempts;default 5 attempts>
   AUTHENTICATION_DEFEND_INTERVAL_MINUTES=<time interval of number of invalid token fetch attempts made;default 1 min>
   AUTHENTICATION_DEFEND_LOCKOUT_MINUTES=<number of minutes the user is blocked from getting a token in case of exceeds the number of attempts;default 1 min>
   SAN_LIST=<SAN list for KBS tls certificate>
   ```

:::note
If you are in the European Union (EU) region, use the following Trust Authority URLs:
<br />`TRUSTAUTHORITY_API_URL=" https://api.eu.trustauthority.company.com"`
<br />`TRUSTAUTHORITY_BASE_URL=" portal.eu.trustauthority.company.com"`
:::

<Tabs>
<TabItem value="hashicorp-config" label="Hashicorp vault KMS configuration">

## Hashicorp vault KMS configuration

Only use these configurations if the KBS is using Hashicorp's free version.

   ```bash
   VAULT_SERVER_IP=<vault server IP address>
   VAULT_SERVER_PORT=<vault port number; default 8200>
   VAULT_CLIENT_TOKEN=<vault root token>
   ```

</TabItem>
<TabItem value="pymip-config" label="PyKMIP configuration">

## PyKMIP configuration

Only use these configurations if using PyKMIP KMS.

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

1. Optionally, configure a proxy setting.

    If you're running behind a proxy, add the following to the kbs.env answer file.

    ```bash
    http_proxy=<http proxy>
    https_proxy=<https proxy>
    ```

1. Run the KBS container.

    ```bash
    docker run -d --restart unless-stopped --name kbs --env-file <KBS env file> -p <KBS port>:9443 -v /etc/kbs/certs:/etc/kbs/certs -v /etc/hosts:/etc/hosts -v /opt/kbs:/opt/kbs trustauthority/key-broker-service:v1.0.0
    ```
