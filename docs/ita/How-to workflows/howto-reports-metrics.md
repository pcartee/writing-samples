---
title: Reports and metrics
description: An overview of the reports and metrics available in Intel Trust Authority.
author: various, mkwilbux
topic: conceptual
date: 06/26/2024
uid: reports.metrics # Do not change uid!
---
*· 06/26/2024 ·*

## Reports and metrics

This article provides information about the reports and metrics functions of Intel® Trust Authority. Reports and metrics can provide a summary of the attestation tokens and API key usage for your subscription, along with the status and response times. Intel® Trust Authority supports pre-defined and custom reports that can be downloaded for specific time ranges. These reports can be exported to a CSV file or a PDF file.

Four report tabs are available for selection.

- Attestation request summary (custom report).
- All services and products by month.
- Usage data by status for top three API keys by month.
- Custom reports, includes pre-defined reports.

![Tab Options](/img/howto-reports-metrics/tabOptions.png)

These functions are only available on the Intel Trust Authority portal.

## Select a report - Attestation Requests

:::note
Attestation request summary is now located in the first tab (default). The API now supports metrics for ALL API keys.
:::

The **Attestation request summary** report provides a record of attestation requests for the selected API key. This report displays the attestation requests by date and metrics associated with the request. You can view the attestation token associated with the request if a token was issued. The attestation request summary report shows up to 1000 requests for a period up to two years previous to the current date.

![Select a Report](/img/howto-reports-metrics/tabOptions.png)

1. Sign in to the Intel Trust Authority portal.
1. Select **Reports and metrics**.
1. Select the **Attestation Service** tab.
1. Select the **Attestation Service**.
1. Select **API Key** from the drop-down menu.
1. Select **Timeframe**.
Enter a Start Date and an End Date for the report.
1. Click **Submit**.

The report result table displays the result, if any:

  ![Attestation request summary report result table](/img/howto-reports-metrics/attestation-table-summary.png)

To view the JWT attestation token, click the **View token** link in the **Attestation Token** column. The token details are displayed in the **View token details** screen.

![View attestation token details](/img/howto-reports-metrics/encodedview.png)

In the **View token details** screen, click either **Encoded mode** or **Decoded mode** to view the token details format in encoded and decoded mode respectively. You can also click the **Copy** button to copy the token details in either mode. 

Results diplay with the following fields:
- Date
- API Key name
- Tag name
- Status
- Messages
- Attestation token
- Response time

:::note
The results are available to export as a CSV file.
:::
 
### Download report
1. Export a CSV by clicking the **EXPORT CSV FILE** button.
1. The report is downloaded and available to view.

![Select a Report - Attestation requests](/img/howto-reports-metrics/tabs-reports-attestation.png)

## Select a report — all services and products by month

1. Sign in to the Intel Trust Authority portal.

1. Select **Reports and metrics**.

1. Select the **All Attestation Services by Mo.** tab.

![Select a Report - All attestation services by month](/img/howto-reports-metrics/all-services-attestation-mo.png)

1. In the Attestation token response time pane, click the **View** option from the drop-down menu.
The options are: Minimum, Maximum and Avg/Min/Max response times. 

1. A summary of the search results is displayed.

1. In the Total attestation token requests usage and status data pane, select the **View** option from the drop-down menu. Options are **Total token requests** and **Total token requests by status**.

![Attestation usage and status](/img/howto-reports-metrics/attestation-usage-status.png)

### Download report
1. Export a PDF by clicking the **EXPORT PDF FILE** button.
1. The report is downloaded and available to view.

## Select a report — usage data by status for top three API keys by month

1. Sign in to Intel Trust Authority.

1. Select the **Reports and metrics** item from the Intel Trust Authority menu.

1. Select the **API Token Status and Usage (top 3)** tab.

![Select a Report](/img/howto-reports-metrics/top3usage.png)

1. In the Attestation token response time pane, click the **View** option from the drop-down menu.
The options are: Minimum, Maximum and Avg/Min/Max response times. 
1. A summary of the search results is displayed.
1. In the Total attestation token requests usage and status data pane, select the **View** option from the drop-down menu. Options are **Total token requests** and **Total token requests by status**.

A summary of the search results is displayed.

### Download report
1. Export a PDF by clicking the **EXPORT PDF FILE** button.
1. The report is downloaded and available to view.

## Select a report — Custom reports

The Attestation request summary is now located as the first tab option.

**Pre-defined** reports provide API token response time and API token status and usage data for the selected API key during the pre-defined time periods day, week, month, quarter, and year.

:::note
Some failed attestation requests may not appear in the report.
:::

To generate a custom report, do the following.

1. Sign in to Intel Trust Authority.
1. Select the **Reports and metrics** item from the Intel Trust Authority menu.
1. Select the **Custom report** tab.

  ![Select a Report](/img/howto-reports-metrics/custom-rm.png)

1. Select the **Attestation service**.
1. Select the **Select API key** option from the drop-down menu.
1. Select the desired **Timeframe** option in the drop-down menu.
1. In the API token response time (Custom report) pane, select a **View** option from the drop-down menu.
Available options are: Avg/Min/Max response times, Maximum response times or Minimum response times.

A summary of the search results is displayed.

### Download report
1. Export a PDF by clicking the **EXPORT PDF FILE** button.
1. The report is downloaded and available to view.

## Security Information and Event Management (SIEM) integration
 Intel Trust Authority supports integration with 3rd party Security Information and Event Management (SIEM) services such as Splunk* or Datadog* to provide real-time notification of critical events such as attestation success or failure directly from your preferred reporting solution. For detailed instructions on integrating with a SIEM service, see the [SIEM integration article](../How-to%20workflows/howto-SIEM-integration.md).

 **\*** Other names and brands may be claimed as the property of others.
