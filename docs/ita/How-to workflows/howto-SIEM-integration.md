---
title: SIEM integration
description: An overview of SIEM integration with Trust Authority.
author: pcartee
topic: how to
date: 05/14/2024
uid: siem-integration  # Do not change uid!
---

*· May/14/2024 ·*

## Security Information and Event Management (SIEM) integration

This article shows how to integrate Trust Authority with 3rd party Security Information and Event Management (SIEM) services such as Splunk* or Datadog* to provide real-time notification of critical events such as attestation success or failure directly from your preferred reporting solution.

:::note
Trust Authority SIEM events are approximately 12kb in size. Default Splunk* event sizes are limited to 10KB. Event messages larger than 10kb are truncated. Splunk* administrators can increase the Splunk* character limit to above 10,000 to prevent messages from being truncated.
:::

- Successful attestation
    The attestation token is sent to the SIEM platform upon successful attestation. Note that by default, this does not indicate that all policies were matched in the attestation. To enforce policy matching (and throw an error on policy mismatch instead of returning a token), the attestation request must set the optional `policy_must_match` value to `true`.
- Failed attestation
    If the attestation request returns an error response, the error will be sent to the SIEM platform. By default an error indicates a malformed API request or a failed attestation against the default policy. If policy enforcement is enabled in the attestation request, any policies that evaluate to unmatched will also throw an error and be included in the "failed attestation" event type.

The data pushed to SIEM is the same data recorded in the Reports and Metrics date-range reports. For more details about reports and metrics, see the [Reports and Metrics article](../How-to%20workflows/howto-reports-metrics.md).

:::note
By default, Trust Authority always provides an attestation token regardless of policy evaluation unless the attestation request forces policy compliance.
:::

## Trust Authority Configurations and SIEM integration
Only a tenant admin is authorized to manage, add, update and delete the system details of SIEM services.

![SIEM service](/img/howto-SIEM-integration/siem-config.png)

1. The tenant admin logs into the Trust Authority.
2. Go to **Configurations**.
3. Select **Reporting (SIEM) applications**.

### Reporting (SIEM) applications

Complete the following sections to turn SIEM service on. 
1. Select a SIEM service.
1. Select the type of security event(s).
1. Choose the authentication type.
1. Enter the endpoint URL and API key.

#### SIEM service

Select an available SIEM service from the drop-down list.
In **SIEM service (required)**, select one service from the list. 
    - Datadog*
    - Splunk*

#### Security event type

Select option(s) for the security event type for real-time notification of critical events.

![Security event](/img/howto-SIEM-integration/siem-event.png)

1. Go to **Security event type (required)**.
1. Select from the checkbox options.
    - Successful attestation
    - Failed attestation

#### Authentication type

Select the authentication type.
1. Go to **Authentication Type**.
1. Select **Auth key (default)**.

![Configuration Data](/img/howto-SIEM-integration/siem-data.png)

#### Configuration data

Enter the endpoint URL and API key.
In  **Configuration Data** there are two entry fields. 
Endpoint URL - enter a valid URL.
Auth Key - enter the API key.
    A textual hint for user is provided that points to a location to find this data.

### Save

Click the **SAVE** button.
Upon successful validation, a green notification will display and the attestation token is sent to the SIEM platform

Upon failed validation, a red notification will display with information about the errors. Errors are sent to the SIEM platform.

**\*** Other names and brands may be claimed as the property of others.
