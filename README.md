# Shore Capital Agent Referral Backend
[![Shore Capital Backend](https://github.com/alujan45/Shore-Capital-Agent-Referral/workflows/DjangoCI/badge.svg)](https://github.com/AndreSand/BornInApp/actions)

Shore Capital Agent Referral Backend, Basic referral system backend.

Recruiters will create account and use their unique referral link to recruit other users, 
those Recruits will complete a transaction and based on that transaction, the recruiter will get commission

## Used Stacks

### Framework

1. Django
2. Django Rest Framework

### Database
1. Postgresql

## Models

1. User
2. Recruiter
3. Recruit
4. Referral
5. Transaction

### User
`User` model contains Account information, 
1. `email`: Email [Username]
2. `first_name`: String
3. `last_name`: String
4. `role`: Int [Recruiter | Recruit | Admin]
5. `created_at`: Time Stamp
6. `password`: Hash
7. `city`: String
8. `state`: String
9. `zip`: String
10. `address`: String
11. `phone_number`: String

### Recruiter
`Recruiter` model contains recruiter information and referral code
1. `user`: User Model Instance
2. `ref_code`: Int

### Recruit
`Recruit` model contains Recruit Information
1. `nmls_id`: String
2. `dre_license`: String
3. `cba_license`: Boolean
4. `association`: String

### Referral
`Referral` Contains Relationship between Recruit and Recruiter
1. `Recruiter`: User Model Instance
2. `Recruit`: User Model Instance
3. `Commission`: Float

### Transaction
`Transaction` can be done by a recruit
1. `Recruit`: User Model Instance
2. `Amount`: Float


## API Docs

#### 1. Login

`api/auth/login`

Method: `POST`

Request Body:
```json5
{
    email: "example@email.com",
    password: "Password"
}
```

Response: 
```json5
{ token: "String", 
  user: {
    email: "example@test.com", 
    role: 1
  }
}
```

#### 2. Change Password

`api/auth/change-password/`

Method: `POST`

Request Body:
```json5
{
    old_password: "Old Password",
    new_password: "New Password"
}
```


Response: `{token: String}`

#### 3. User Update | Update User Information


`api/auth/user/update/`

Method: `PATCH`

Partial Update

Request Body:
```json5
{
    first_name: "String",
    last_name: "String",
    phone_number: "String",
    address: "String",
    city: "String",
    state: "String",
    zip: "String",
}
```


Response: `Same as body`

#### 4. Check Email Available


`user/email/check`

Method: `POST`

Request Body:

```json5
{
     email: "Email"
}
```


Response: `{msg: 0 / 1}`

```python
# 0 > Email Is not Available
# 1 > Email is available
```

#### 5. Get Ref Code

`/api/core/ref-code`

Method: `POST`

Request Body

```json
{
  "ref_code": "123455"
}    
```

Response
```json5
{
  email: "example@email.com",
  full_name: "Full Name"
}
```

#### 6. Recruiter Create
`/api/core/recruiter/create`

Method: `POST`

Request Body
```json5
{
   user: {
    first_name: "String",
    last_name: "String",
    phone_number: "String",
    address: "String",
    city: "String",
    state: "String",
    zip: "String",
    password: "String" 
   }
}
```
Response 
```json5
{
  token: "String",
  data: {
    "key": "value"
  }
}
```
`Data Same as Request Body`

#### 7. Recruit Create and List

`/api/core/recruit/`

METHOD: `POST`

Request Body
```json5
{
     user:{
        first_name: "String",
        last_name: "String",
        phone_number: "String",
        address: "String",
        city: "String",
        state: "String",
        zip: "String",
        password: "String" 
     },
    phone_number: "String",
    nmls_number: "String",
    dre_license: "String",
    ref_code: "String"
}

```
Response 
```json5
{
  token: "String",
  data: {
    "key": "value"
  }
}
```
`Data Same as Request Body`

#### 7. Referral Data

`api/core/referral`

METHOD: `GET`

Query Params: `?page=<page_number>`

Response Body
```json5
{
  page: 1,
  next: "Link",
  prev: "Link",
  results: [
    {
       id: 1,
       recruiter: 1,
       recruit: {
         email: "Email",
         first_name: "First Name",
         last_name: "Last Name"
       },
       commission: 200,
       time_stamp: "2020-02-02 12:19:34.45666"
    }
  ]
}

```