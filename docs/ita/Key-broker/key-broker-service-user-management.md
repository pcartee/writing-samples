---
title: Key Broker Service user management
description: Key Broker Service user management
author: pcartee
topic: KBS
date: 02/27/2024
uid: kbs.user.management
---

## Key Broker Service user management

An admin user is created using the credentials entered when the container is started. The admin user has access to all the KBS APIs and, therefore, can create other users.  

## Create users

The admin user uses the `POST /users` API to create other KBS users.

### POST /users

```bash
{
  "password": "testPassword",
  "permissions": [
    "users:create",
    "users:search"
  ],
  "username": "testUser"
}
```

:::note
Use the `docs/openapi.yml` OpenAPI specification to refer to each of the APIs mentioned above to create a token, keys, etc.
:::
