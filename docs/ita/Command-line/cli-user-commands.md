---
title: Intel Trust Authority CLI User Management
description: Intel Trust Authority CLI user management commands.
author: pcartee
topic-type: Reference
date: 08/17/2023
uid: cli-user-commands
---

*· August/17/2023 ·*

## User management

These instructions describe how to manage users with CLI commands. Users can also be managed through the [managing users](../How-to%20workflows/howto-manage-users.md) section of the Intel® Trust Authority portal.

## Create user

Create a new Intel Trust Authority user.

`trustauthorityctl create user -e < email Id> -r < Role (Tenant Admin/User) >`

**Sample call**

```bash
trustauthorityctl create user -e regularuser0@gmail.com -r User
```

**Sample response**

```bash
trace-id:  LOnduFR-IAMEVqw=
User: 

 {
  "id": "8f96ee5c-69a7-497d-9cf7-900ed2250470",
  "email": "regularuser0@gmail.com",
  "role": {
    "id": "885391bf-2a37-4dc7-9444-833c5a817cdf",
    "name": "User"
  },
  "active": false,
  "created_at": "2023-09-14T04:02:57.329824144Z",
  "privacy_acknowledgement": false
}
```

## Get Users

List the current users in your Intel Trust Authority environment.

`trustauthorityctl list user`

**Sample call**

```bash
trustauthorityctl list user
```

**Sample response**

```bash
trace-id:  LOnetHW6IAMEEQQ=
Users: [ { "id": "e3968eb8-e053-4646-98dd-7b61991a66d1", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "66ec2e33-8cd3-42b1-8963-c7765205446e", "name": "Tenant Admin" } ] } ], "active": true, "created_at": "2022-09-29T16:42:46.236499Z" }, { "id": "f9af3e31-9fc5-48db-afc3-c818049f6570", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "66ec2e33-8cd3-42b1-8963-c7765205446e", "name": "Tenant Admin" } ] } ], "active": false, "created_at": "2022-10-01T01:00:53.924856Z" }, { "id": "82ac5d98-c8ba-49cf-ac3e-4d4a1385be68", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "885391bf-2a37-4dc7-9444-833c5a817cdf", "name": "User" } ] } ], "active": false, "created_at": "2022-10-01T01:27:44.145412Z" }, { "id": "42850600-7a58-43a1-970a-85bb4008cd88", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "66ec2e33-8cd3-42b1-8963-c7765205446e", "name": "Tenant Admin" } ] } ], "active": false, "created_at": "2022-10-11T20:30:40.348744Z" }, { "id": "1c83eeb3-e9f7-4a59-8104-7009f6f385b0", "email": TC917-2@hello.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "66ec2e33-8cd3-42b1-8963-c7765205446e", "name": "Tenant Admin" } ] } ], "active": false, "created_at": "2022-10-11T21:16:45.358066Z" }, { "id": "598db1fc-4340-4bbc-9e19-2d596c3b7bd8", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "885391bf-2a37-4dc7-9444-833c5a817cdf", "name": "User" } ] } ], "active": false, "created_at": "2022-10-12T03:18:17.545383Z" }, { "id": "dd4b49c7-9207-43e4-a3c1-8c734cf828a4", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "66ec2e33-8cd3-42b1-8963-c7765205446e", "name": "Tenant Admin" } ] } ], "active": false, "created_at": "2022-10-12T03:18:19.458591Z" } ]
```

## Get users by email id

List the current users in your Intel Trust Authority environment by their email.

`trustauthorityctl list user -e`

**Sample call**

```bash
trustauthorityctl list user -e "regularuser0@gmail.com"
```

### Sample response

```bash
trace-id:  LOnezF_5oAMEHZQ=
Users: 

 {
  "id": "8f96ee5c-69a7-497d-9cf7-900ed2250470",
  "email": "regularuser0@gmail.com",
  "role": {
    "id": "885391bf-2a37-4dc7-9444-833c5a817cdf",
    "name": "User"
  },
  "active": false,
  "created_at": "2023-09-14T04:02:57.329824Z",
  "privacy_acknowledgement": false
}
```

## Update user role

Update the user role of a specific user.

`trustauthorityctl update user role -u < user id > -r < Role (Tenant Admin/User) >`

### Sample call

```bash
trustauthorityctl update user role -a 4rririr887604or09rfi484e7ordj879 -u "4324598fs-0404-4f4r-9oii9-8f8flk893w21" -r "Tenant Admin"
```

### Sample response

```bash
trace-id:  LOnetHW6IAMEEQQ=
Updated User: { "id": "598db1fc-4340-4bbc-9e19-2d596c3b7bd8", "email": user1@intel.com, "tenant_roles": [ { "tenant_id": "020f1162-25ed-441c-9d8f-69cfc7974cc1", "roles": [ { "id": "66ec2e33-8cd3-42b1-8963-c7765205446e", "name": "Tenant Admin" } ] } ], "active": false, "created_at": "2022-10-12T03:18:17.545383Z" }
```

## Delete user

Delete a specific user.

`trustauthorityctl delete user -u < user id >`

### Sample call

```bash
trustauthorityctl delete user -a 4rririr887604or09rfi484e7ordj879 -u "4324598fs-0404-4f4r-9oii9-8f8flk893w21"
```

### Sample response

```bash
trace-id:  LOnf6FS_oAMEXPw=
User 4324598fs-0404-4f4r-9oii9-8f8flk893w21 deleted
```

## List tenant setting

List the email address used to send notifications when an attestation failure occurs.

`trustauthorityctl list tenant-settings`

### Sample response

```bash
trace-id: LOnTaExEoAMECsQ=
Tenant Settings:
 {
  "attest_failure_email": ""
}
```

## Update tenant settings

Enter an email address and turn on notifications in the event of an attestation failure. Notifications are only sent when there is an attestation failure (not a policy mismatch). The default sends no notifications.

`trustauthorityctl update tenant-settings -e "<email id>"`

### Sample call

```bash
trustauthorityctl update tenant-settings -e user1@intel.com
```

### Sample response

```bash
trace-id:  LOnTgGR2IAMEFAA=
 {
  "attest_failure_email": "user1@intel.com"
}
```

## Disable tenant settings

Disable notifications when an attestation failure occurs.

`trustauthorityctl update tenant-settings -d`

### Sample Response

```bash
trace-id:  LOnTnGxjoAMEdWQ=
Updated Tenant Settings:
 {
  "attest_failure_email": ""
}
```
