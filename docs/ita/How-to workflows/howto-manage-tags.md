---
title: Tag management
description: An overview of tags in Intel Trust Authority.
author: pcartee
topic: how to
date: 09/06/2024
uid: manage.tags # Do not change uid!
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Last updated: 07/18/2024

## Tag management

This article contains workflow examples related to tags, which are metadata elements like key-value pairs that can be applied to API keys. These can be used to identify usage based on settings relevant to your organization.

Tags can be managed using the Intel® Trust Authority portal, with the [CLI](../Command-line/cli-api-client-management.md), or by [REST API](../Restapi/restapi-tenant-management.md).

<Tabs>
<TabItem value="manage-tags-portal" label="Intel Trust Authority portal">

## Portal

### Add a tag

This option enables you to add a tag to an existing API key.

1. Sign in to the Intel Trust Authority portal.

1. Select **Manage Services**.

1. Select the **Edit** ![Edit icon](/img/common-graphics/edit-icon.png) icon for the API key to which you are adding a tag.

1. To confirm your intent to add a tag, select **YES, EDIT** on the pop-up.

1. On the **Edit API key** page, select **ADD A TAG ROW**.

1. Select the down arrow in the **Enter a name** box.

    ![Add Tag](/img/howto-manage-tags/add-tag-rows.png)

1. Select **Create a new tag name**.

1. Enter a name for the tag in the **Enter a tag name here** box.

1. Optionally enter a value for the tag.

1. On the Confirm API key details page, select **SAVE & CONTINUEt**.

1. Select the **SUBMIT** button.

1. The new value is displayed in the Assigned tags (optional) pane.

### View tags

1. Sign in to the Intel Trust Authority portal.

1. Select **Manage services**.

1. Select the dropdown arrow of an API key to view the tags associated with it.

    ![View Tags](/img/howto-manage-tags/view-tag.png)

### Edit existing tags

You can add, edit, or delete the values of an existing tag. You can disassociate a tag from an API key and select another tag to associate with the API key, but you cannot delete a tag once it's created.

1. Sign in to the Intel Trust Authority portal.

1. Select **Manage services**.

1. Select the edit icon ![Edit icon](/img/common-graphics/edit-icon.png) next to the API key associated with the tag to be edited.

1. Select **YES, EDIT** on the popup.

    The **Edit API key** page displays.

    ![Edit Service](/img/howto-manage-tags/edit-services.png)

1. To display the existing tags, select the **Assigned tags (optional)** arrow.

1. Select the dropdown arrow in the **Enter a name** box.

    ![Add Tag](/img/howto-manage-tags/add-tag-rows.png)

1. Choose from the following:

   - To rename the tag, select a different name from the dropdown list.
   - To edit an existing tag value, delete the existing tag value and enter a new one.
   - To add an additional value to the tag, select **ADD A Value** and then enter an additional value for the tag.

1. Select **SAVE & CONTINUE**.

    The changes are reflected in the **Assigned tags (optional)** section of the **Confirm API keys details** page.

1. Confirm the information is correct.

1. Select **SUBMIT**.

    The changes are committed to the system.

</TabItem>
<TabItem value="manage-tags-cli" label="CLI">

## CLI

### Create tag

This command creates a tag for Intel Trust Authority.

`trustauthorityctl create tag -n < tag name >`

#### Sample call: create tag

```bash
trustauthorityctl create tag -n TestTagUsername
```

#### Sample response: create tag

```bash
trace-id:  LOnIBH5yIAMEJ5Q=
Tag:
{
  "id": "60f29395-2ffc-4e65-8e60-5abbd2e97d1c",
  "name": "TestTagUsername",
  "predefined": false
}
```

### List tags

This command lists the tags in your Intel Trust Authority system.

`trustauthorityctl list tag`

#### Sample call: list tags

```bash
trustauthorityctl list tag
```

#### Sample response: list tags

```bash
trace-id:  LOnI6FFjIAMEYaQ=
Tags:
{
  "tags": [

    {
      "id": "7u8ikldg-s382-7hud-vb38-78jhsf3r5tf0",
      "name": "UsernameTag",
      "predefined": false
    },
    {
      "id": "47yukjsv-29op-38sq-v3g8-xcqd456hju7i",
      "name": "Username-Tag",
      "predefined": false
    }

  ]
}
```

### Delete a tag

This command deletes a tag.

`trustauthorityctl delete tag -t < tag id >`

#### Sample call: delete a tag

```bash
trustauthorityctl delete tag -t 47yukjsv-29op-38sq-v3g8-xcqd456hju7i
```

#### Sample response: delete a tag

```bash
trace-id:  LOnJAEcPIAMEotg=
Tag 7yukjsv-29op-38sq-v3g8-xcqd456hju7i Deleted
```

### List API client tags

This command lists the tags associated to a specific subscription.

`trustauthorityctl list apiClient tag -r < service id > -c < api client id >`

#### Sample call: list API client tags

```bash
trustauthorityctl list tag
```

#### Sample response: list API client tags

```bash
trace-id:  LOnz5H8OoAMEVtQ=
Tags:
{
"tags": [
{
"id": "7110194b-a703-4657-9d7f-3e02b62f2ed8",
"name": "TestTagUsername",
"predefined": false
}
]
}
```

### Delete tag

This command deletes a tag.

`trustauthorityctl delete tag -t < tag id >`

#### Sample call: delete tag

```bash
trustauthorityctl delete tag -t 976e4fe8-b5ba-4443-a7d6-fd2544cadb69
```

#### Sample response: delete tag

```bash
trace-id:  LOnJAEcPIAMEotg=
Tag 976e4fe8-b5ba-4443-a7d6-fd2544cadb69 deleted
```

### List apiClient tags

Returns the list of tags associated with the specified serviceId and apiClientId for the logged in Tenant.

`trustauthorityctl list apiClient tag -r < serviceId > -c < apiclientId >`

#### Sample call: list apiClient tags

```bash
trustauthorityctl list apiClient tag -r 382d4141-103b-47f3-a001-13490db89d1d -c 30686bc0-0a75-4086-9a4c-4c59bea6df64
```

#### Sample response: list apiClient tags

```bash
trace-id:  LOnz5H8OoAMEVtQ=
Tags:

{
  "tags": [
    {
      "key": "Tag1",
      "value": "Tag1Value",
      "predefined": false
    }
  ]
}
```

</TabItem>
</Tabs>
