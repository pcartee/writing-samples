---
title: Intel Trust Authority CLI Examples
description: Example workflows for the Intel Trust Authority CLI.
author: various
topic-type: Reference
date: 08/15/2023
uid: cli-examples
---

## Intel® Trust Authority tenant CLI

The Intel Trust Authority Command-Line Interface (CLI) is a set of commands used by tenants to create and manage Intel Trust Authority resources with a focus on ease of use. The Intel Trust Authority CLI must be installed and configured for your environment.

The Intel Trust Authority CLI is an open-source tool available on [GitHub](https://github.com/intel/trustauthority-cli).

## Intel Trust Authority CLI commands

The Intel Trust Authority CLI contains the following command groups.

- [User Management](cli-user-commands.md) — Used to manage Intel Trust Authority users and administrators.
- [Service Management](cli-service-commands.md) — Used to manage Intel Trust Authority services.
- [API client management](cli-api-client-management.md) — Used to manage attestation APIs.
- [Policy Management](cli-policy-commands.md) — Used to create and update Intel Trust Authority policies.

## How to use command line options

The Intel Trust Authority CLI uses the following format:

   `CLI: trustauthorityctl < command > < resource >`

:::note
If you're using a network proxy service, you must add the Intel Trust Authority `FQDN to NO_PROXY` environment variable.
:::

## Retrieve an attestation API key

All the attestation-related APIs, CLI commands, and client libraries require an attestation API key for authorization. For more information, see [Attestation API keys](../Concepts/concept-user-roles-and-api-keys.md#attestation-api-keys). These instructions explain how to retrieve an attestation API key.

:::note
These instructions assume that your API key has already been created. If you need to create an API Key, follow the [Creating API keys](../Quickstart/tutorial-api-key.md) steps.
:::

1. Sign in to the Intel Trust Authority portal.

1. Go to the Manage services page.

    ![Manage services page](/img/cli/manage-services-page.png)

1. Scroll down to the Attestation API Keys section.

1. Locate the API from which you want to retrieve the key.

:::note
You can have more than one API key associated with your account. Be sure to select the appropriate API key for the CLI request you are attempting.
:::

1. Select the View ![reveal API icon](/img/cli/api-reveal.png) icon.

2. Select the Copy ![Copy API key icon](/img/cli/copy-api-key.png) icon.

## Retrieve Admin API keys

All the tenant management-related APIs, CLI commands, and client library methods require an Admin API key for authorization. Admin API keys can only be retrieved through the Intel Trust Authority web portal. For more information, see [Tenant admin API keys](../Concepts/concept-user-roles-and-api-keys.md#tenant-admin-api-keys).

1. Sign in to the Intel Trust Authority portal.

1. Select **Admin API keys**.

    ![Alt text](/img/howto-manage-admin-api-keys/admin-api-keys.png)

1. Select the View ![View  icon](/img/common-graphics/view-icon.png) icon for API key you want to copy.

    The API key is displayed.

1. Select the copy ![Copy icon](/img/common-graphics/copy-icon.png) icon.

    The API key is copied to your system memory.

1. The API key can be used with the Tenant CLI to manage admins and users.
