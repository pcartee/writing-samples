---
title: Trust Authority CLI Installation
description: Trust Authority CLI prerequisites and installation guide.
author: pcartee
topic-type: Reference
date: 06/12/2024
uid: cli-install
---
*· 06/12/2024 ·*

## Trust Authority CLI installation guide

These instructions describe how to build and install the Trust Authority CLI. The Trust Authority CLI is an open-source tool tenants use to make API calls to their instance of Trust Authority. The source code for the Trust Authority CLI is available on [GitHub](https://github.com/company/trustauthority-cli).

:::note
Valid characters include: numbers 0 through 9, upper and lowercase English characters, underscore (_), colon (;), period (.), slash  (/), dash (-), and a space ( ).
:::

## Build the Trust Authority CLI

Follow these instructions to build the Trust Authority CLI.

### Prerequisite packages

Install the following prerequisite packages before installing the Trust Authority CLI:

**Make and Makeself**

To instal the `make` and `makeself` packages, run the following command:

```
apt -y install make makeself
```

**Golang**

The supported Golang version is 1.20.x

1. To install Golang version 1.20.x, follow the install instructions on the golang website `https://go.dev/doc/install`.

1. Add the local binary path, namely $HOME/.local/bin/, to your PATH environment variable if not already present.

### Supported operating system

- Ubuntu LTS 20.04

:::note
You must be a Tenant Admin to install the CLI, however, both the admin and users can use the CLI.
:::

### Build the CLI

1. Create a directory on the build machine named `CLI`.

    `mkdir cli`

1. Go to the CLI directory.

    `cd cli`

1. To clone the Trust Authority CLI code to the newly created CLI directory, run the following command.

    `git clone https://github.com/company/trustauthority-cli`

1. Create the CLI installer in the newly created CLI directory.

    `cd trust-authority-cli and run "make installer"`

## Install the Intel Trust Authority CLI

Before beginning these instructions, have the following information available:

- URL of API Gateway
- API Key of the Tenant

1. If you have not already navigated to the CLI directory in which the CLI was built, navigate to it.

    `cd cli`

1. Copy the binary installer to the system on which it is being deployed.

     `trustauthorityctl-{version}.bin`

1. The `trustauthorityctl.env` file enables the CLI to contact a specific Intel Trust Authority instance so it can be used to make changes. Create the trustauthorityctl.env file in your home directory and add the following contents:

    - `TRUSTAUTHORITY_URL=https://api.trustauthority.intel.com`
    - `TRUSTAUTHORITY_API_KEY="< Admin API Key >`

       :::note
       If you are in the European Union (EU) region, use the following Intel Trust Authority URL: `TRUSTAUTHORITY_URL=https://api.eu.trustauthority.intel.com`
       :::

1. To install the tenant CLI on your system, run following command:

    `./trustauthorityctl-{version}.bin`

:::note
If you're behind a proxy, add the Intel Trust Authority FQDN to the NO_PROXY environment variable.
:::

### Directory structure

All files are stored in the user's home directory. The contents of the directories are listed below:

- Configuration: $HOME/.config/trustauthorityctl/config.yaml
- Logs: $HOME/.config/trustauthorityctl/logs/trustauthorityctl.log
- Bin: $HOME/.local/bin/trustauthorityctl

:::note
If you cannot access the command, add the binary path to the PATH env variable
:::

## Commands

:::note
Request ID could be a randomly generated string of at most 128 bytes, which can work as a unique identifier for each CRUD operation. This can be provided as an optional parameter to all the CRUD commands only.
:::

## Tenant CLI configuration

Use the command below to configure the tenant CLI. You need to know the file path to the `trustauthorityctl.env` file created in the previous step.

`trustauthorityctl config -v < env file path >`

## Install Bash completion

Use the following command to install bash completion for the Intel Trust Authority CLI.

`trustauthorityctl completion`

## Retrieve the version

To get the version number of the tenant CLI installed on your system, run the following command:

`trustauthorityctl version`

## Uninstall the CLI

To uninstall the tenant CLI, use the following command:

`trustauthorityctl uninstall`
