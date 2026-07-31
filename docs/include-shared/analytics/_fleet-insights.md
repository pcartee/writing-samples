---
date: 05/19/2025
---

## Service analytics

The top of the **Analytics** page displays summary information about the service including:

- **Total devices**: The total number of your managed devices.
- **Direct data downloads**: (TSC Only) The number of device file downloads performed by the service. See the [Transfer devices](tsc-transfer-devices.md#download-device-information-files) article for more information.
- **Total operations**: The number of operations performed by the service. This includes the number of operations performed through the UI and through the API.
- **Total attestations**: The number of attestations performed by the service with in the selected date range.
- **Baselines created**: This refers to the number of baselines established by the service. A baseline is created when a device is first attested, representing the original configuration of that device.
- **Baselines updated**: This indicates the number of baselines that have been updated by the service. A baseline is updated when a device is attested again, and its configuration has changed. The updated baseline reflects the new configuration of the device.

## Filter data

All analytics reports can be filtered using the **Select date range** and **Device serial** functions. The selected filters apply to all information displayed on the page.

### Select date range

The **Select date range** function allows you to filter data by a specific date range. The date range can be selected using the calendar tool or the slider.

- **Calendar tool**: Select the left calendar icon to set the beginning date. Select the right calendar icon to set the ending date. The date range is displayed in the format MM/DD/YYYY.
- **Slider**: Select and drag the left slider icon to set the beginning date. Select and drag the right slider icon to set the ending date.

### Device serial

The **Device serial** function allows you to filter data by all devices or by a specific device. A specific device serial number can be selected from the drop-down menu or entered manually. Selecting **All** displays information for all devices in the system.

### Default date ranges

The default date ranges are listed at the top of the page. Choose a date range in which to filter data by selecting the appropriate button. The default date ranges are:

- **Last 7 days**
- **Last 30 days**
- **Last 60 days**
- **Last 90 days**

## Select a report

The tabs at the bottom of the page enable you to select different reports.  The three report are:

- [Overview](#overview) - This report provides summary information about the devices being managed.
- [Device Report](#device-report) - This report provides detailed information about your managed devices.
- [Remote verification report/PLI report](#remote-verification-reportpli-report) - This report provides detailed information about your the attestations taken against your devices. Attestations are resolved into 4 different verdicts:

  - **Matched**: The current measurement of the device matches its current baseline.
  - **Unmatched**: The current measurement of the device does not match its current baseline.
  - **Unknown device**: The device does not have a baseline recorded with your system.
  - **Bad request**: The attestation request was not formatted correctly or contained invalid data.

## Overview

The **Analytics** page defaults to the **Overview** report. This report provides summary information about the service. It includes metrics on the devices managed by the system, the number of operations performed, and attestation results. The **Overview** report is available for both TSC and PLI subscriptions. Select the appropriate tab to view the report for your service.

# [TSC Overview](#tab/tsc-overview)

The **Overview** page for TSC is divided into four sections:

**Total services by type**: Displays the number of devices associated with your TSC and a PLI subscriptions.

**Operations**: Shows the total number of operations performed by the service. There are two options to choose from:

- **Total operations**: The number of operations performed by the UI and through the API.
- **API operations**: The number of operations performed only through the API.

**Remote verification report/PLI Report**: Displays the attestations of PLI enabled devices. It displays the number of successful and failed attestation attempts.

**Remote verifications results**: Attestations are resolved to verdicts such as **Matched**, **Unmatched**, **Unknown device,** and **Bad request**. This section displays the number of times each verdict was reached.

# [PLI Overview](#tab/pli-overview)

The Overview page for PLI is divided into three sections:

**Platform integrity**: Displays the number of successful and failed attestations.

**Operations** - Shows the total number of operations performed by the service. There are two options to choose from in this section:

- **Total operations** -  The number of operations performed by the UI and through the API.
- **API operations**- The number of operations performed through the API.

**Platform integrity results** - Attestations are resolved to verdicts such as **Matched**, **Unmatched**, **Unknown device,** and **Bad request**. This section displays the number of times each verdict was reached.

---

## Device Report

The **Device Report** provides a summary of the devices managed by your Intel TSC and PLI system. The report includes the following information:

**Total operations over period** - This section shows you the trends of the devices managed by your Intel TSC or Intel PLI system. It displays the following:

- **Serial searches** - Searches performed on your devices using serial numbers.
- **Downloads** -  The downloads of delta certification files for your devices. A delta certification file is an XML file that contains information about changes made to a device's components compared to its original configuration. The delta file includes details about components that have been added, modified, or removed, allowing you to track and validate changes in the device over time.
- **Baseline uploaded**- The trend of delta certification file uploads performed for your devices.

There are two options to choose from in this section:

- **All** - This displays the trends for all of the devices being managed by you service.
- **API operations**- The number of operations performed only through the API.

### Sort data (TSC only)

You can sort the data in the Device report using the following options:

**Remote verification status** - select Successful or Failed.

**Remote verification result** - select Matched, Unmatched, Unknown device, or Bad request.

**Remote verifications (TSC) / Platform integrity attestations (PLI)** - This section shows you the results from the latest attestations performed by the service. This section displays the following:

- **Date**: The date the attestation was performed.
- **Serial number**: The serial number of the device that was attested.
- **Status**: The status of the attestation: **Succeeded** or **Failed**.
- **Result**: The result of the attestation: **MATCHED**, **UNMATCHED**, **UNKNOWN DEVICE**, and **BAD REQUEST**.
- **Failure reason**: The reason the attestation failed.

## Remote verification report/PLI report

The **Remote verification report / PLI report** provide a summary of the devices managed by your TSC/PLI system. The report includes the following sections:

**Updated components** - This section shows you which components have been updated and the device that component affects.

**Component property differences** -  This section shows you the previous and current version of the component that was updated.

**Latest platform integrity results**- This section shows you the changes to the device from the latest attestation attempt.

### Filter report data

The information on this page can be filtered by the following: 

- **Remote verification result**
- **Component type**
- **Device manufacturer**
- **Device model**

After selecting the filters, the results are listed below under three categories: Modified, Added, and Removed. Select a category to view the results in the **Latest remote verification results** section.
