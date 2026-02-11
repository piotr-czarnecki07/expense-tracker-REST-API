# endpoints

List of API endpoints and operations that they make.\
For any data-changing operations **token must be provided in either query parameters (for GET and DELETE methods) or in request body (POST, PUT and PATCH methods).**

## /users/

### GET

Returns a list of all users.\
No data is necessary.

Response:

```json
[
    {
        "username": "user1",
        "email": "user1@example.com"
    },
    {
        "username": "user2",
        "email": "user2@example.com"
    }
]
```

### POST

Creates a new user and returns it's database record.\
Needs the following parameters:

Data:

```json
{
    "username": "admin",
    "email": "admin@example.com",
    "password": "2026-02-09"
}
```

Response:

```json
{
    "token": "token_data"
}
```

## /users/str:username/?token=token_here_if_necessary

### GET

Returns user data.\
Requires token in query parameters.

Response:

```json
{
    "username": "user1",
    "email": "user1@example.com",
    "expense_ids": [
        1,
        2
    ],
    "created_at": "2021-06-06"
}
```

### PUT

Replaces all user data fields with new ones.\
Requires the same data as with creating a new user, eventually a token if it is not in query parameters.

Response is the same as with creating a new user.

### PATCH

Replaces some user data fields with new ones.\
Requires some parameters as with creatings a new user, eventually a token if it is not in query parameters.

Response is the same as with creating a new user.

### DELETE

Deletes user from database.\
Requires token, if not in query parameters.

Returns database record of deleted user.

## /users/str:username/expenses/?token=token_here_if_necessary

### GET

Returns a list of all expenses.\
Requires token in query parameters.

Response:

```json
{
    "title": "Breakfast",
    "amount": 12.34
}
```

### POST

Adds a new expense.\
Requires token in query parameters or in request body.

Data:

```json
{
    "title": "Breakfast",
    "amount": 12.34,
    "category": "Food",
    "token": "token_here"
}
```

Response:

```json
{
    "id": 1,
    "title": "Breakfast",
    "amount": 12.34,
    "category": "Food",
    "created_at": "2025-05-12T15:32:23.345345Z",
    "updated_at": "2025-05-13T12:13:55.846532Z"
}
```

## /users/str:username/expenses/int:expense_id/?token=token_here_if_necessary

### GET

Returns data of the expense.\
Requires token in query parameters.

Response:

```json
{
    "id": 1,
    "title": "Breakfast",
    "amount": 12.34,
    "category": "Food",
    "created_at": "2025-05-12T15:32:23.345345Z",
    "updated_at": "2025-05-13T12:13:55.846532Z"
}
```

### PUT

Replaces all data fields of expense.\
Requires the same data as creating a new expense.

Returns the expese record with replaced data.

### PATCH

Replaces some data fields of expense.\
Requires some of the data as with creating a new expense.

Returns the expese record with replaced data.

### DELETE

Deletes an expense.\
Requires token in quert parameters.

Returns deleted expense record.

## /users/str:username/tokens/

### GET

Reminds token assigned to user aftetr validating password.\
Requires password in query parameters.

Response:

```json
{
    "token": "token_data"
}
```

### POST

Regenerates token.\
New token will be used instead of the former one\
Requires password in query parameters.

Resposne:

```json
{
    "new_token": "new_token_data"
}
```
