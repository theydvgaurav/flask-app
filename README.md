# Backend Assignment

This project employs a well-structured architecture using Flask, PostgreSQL, Redis, and Celery to ensure robust and
efficient performance. Validation is handled with Pydantic, which ensures data integrity and adherence to defined
schemas. Asynchronous tasks are processed using Celery, leveraging Redis as the message broker to improve scalability
and responsiveness. The application architecture is organized using Flask blueprints and method views, promoting
modularity and maintainability. A custom authentication guard has been implemented to secure endpoints, and the
Flask-SQLAlchemy ORM is utilized for seamless database interactions. Additionally, comprehensive logging is integrated
to facilitate monitoring and debugging.

## Running Project Locally

Create a new python virtual environment

```bash
  python3.11 -m venv env
```

Activate the new python virtual environment

```bash
  source env/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Update Credentials in local.env

Apply the migrations

```bash
  set -a && source local.env && set +a
  export FLASK_APP=server.py
  flask db upgrade
```

### As Api to created Admin user is not there, so please make entries for admin user(s)

Start the application server

```bash
  set -a && source local.env && set +a
  FLASK_ENV=development FLASK_APP=server.py flask run --port 8000 --debug --reload 
```

Start celery worker

```bash
  set -a && source local.env && set +a
  export FLASK_APP=server.py
  celery -A server worker --loglevel=info 
```

## API Reference

#### Send OTP

```http
  POST /v1/users/send-otp/
```

| Body    | Type     | Description                      |
|:--------|:---------|:---------------------------------|
| `email` | `string` | Email of the user. **Required**. |

#### User Login

```http
  POST /v1/users/login/
```

| Body    | Type     | Description                         |
|:--------|:---------|:------------------------------------|
| `email` | `string` | Email of the user. **Required**.    |
| `otp`   | `string` | OTP sent to the user. **Required**. |

#### Get the list of all policies

```http
  GET /v1/policy/
```

| Headers         | Type     | Description                          |
|:----------------|:---------|:-------------------------------------|
| `Authorization` | `string` | Bearer Token the user. **Required**. |

| Query Parameters | Type      | Description                                                |
|:-----------------|:----------|:-----------------------------------------------------------|
| `policy_status`  | `string`  | Filter by policy status. **Optional**.                     |
| `customer_name`  | `string`  | Filter by customer name. **Optional**.                     |
| `page`           | `integer` | Page number for pagination. **Optional**.                  |
| `per_page`       | `integer` | Number of items per page. **Optional**.                    |
| `created_date`   | `string`  | Filter by policy creation date (YYYY-MM-DD). **Optional**. |

### Create a policy

```http
  POST /v1/policy/
```

| Headers         | Type     | Description                             |
|:----------------|:---------|:----------------------------------------|
| `Authorization` | `string` | Bearer Token of the user. **Required**. |

| Body                | Type      | Description                                                                               |
|:--------------------|:----------|:------------------------------------------------------------------------------------------|
| `policyType`        | `string`  | Type of the policy. **Required**. **values from ['max_life','hdfc_life','icici_life']  ** |
| `applicationNumber` | `string`  | Application number. **Required**.                                                         |
| `customerName`      | `string`  | Name of the customer. **Required**.                                                       |
| `email`             | `string`  | Email of the customer. **Required**.                                                      |
| `phoneNumber`       | `string`  | Phone number of the customer. **Required**.                                               |
| `dateOfBirth`       | `string`  | Date of birth of the customer (YYYY-MM-DD). **Required**.                                 |
| `policyCover`       | `integer` | Coverage amount of the policy. **Required**.                                              |
| `policyStatus`      | `string`  | Status of the policy. **Required**.                                                       |
| `policyNumber`      | `string`  | Number of the policy. **Required only if Policy Status is issued**.                       |
| `medicalType`       | `string`  | Type of medical examination. **Required based on policy Type**.                           |
| `medicalStatus`     | `string`  | Status of the medical examination. **Required based on policy Type**.                     |
| `remarks`           | `string`  | Additional remarks. **Required based on policy Type**.                                    |

### Update a policy

```http
  PUT /v1/policy/{policy_id}/
```

| Headers         | Type     | Description                             |
|:----------------|:---------|:----------------------------------------|
| `Authorization` | `string` | Bearer Token of the user. **Required**. |

| Path Parameters | Type     | Description                               |
|:----------------|:---------|:------------------------------------------|
| `policy_id`     | `string` | ID of the policy to update. **Required**. |

| Body            | Type      | Description                                                           |
|:----------------|:----------|:----------------------------------------------------------------------|
| `customerName`  | `string`  | Name of the customer. **Required**.                                   |
| `email`         | `string`  | Email of the customer. **Required**.                                  |
| `phoneNumber`   | `string`  | Phone number of the customer. **Required**.                           |
| `dateOfBirth`   | `string`  | Date of birth of the customer (YYYY-MM-DD). **Required**.             |
| `policyCover`   | `integer` | Coverage amount of the policy. **Required**.                          |
| `policyStatus`  | `string`  | Status of the policy. **Required**.                                   |
| `policyNumber`  | `string`  | Number of the policy. **Required only if policy status is issued**.   |
| `medicalType`   | `string`  | Type of medical examination. **Required based on policy type**.       |
| `medicalStatus` | `string`  | Status of the medical examination. **Required based on policy type**. |
| `remarks`       | `string`  | Additional remarks. **Required based on policy type**.                |

### Get a policy

```http
  GET /v1/policy/{policy_id}/
```

| Headers         | Type     | Description                             |
|:----------------|:---------|:----------------------------------------|
| `Authorization` | `string` | Bearer Token of the user. **Required**. |

| Path Parameters | Type     | Description                                 |
|:----------------|:---------|:--------------------------------------------|
| `policy_id`     | `string` | ID of the policy to retrieve. **Required**. |

### Delete a policy

```http
  DELETE /v1/policy/{policy_id}/
```

| Headers         | Type     | Description                             |
|:----------------|:---------|:----------------------------------------|
| `Authorization` | `string` | Bearer Token of the user. **Required**. |

| Path Parameters | Type     | Description                               |
|:----------------|:---------|:------------------------------------------|
| `policy_id`     | `string` | ID of the policy to delete. **Required**. |

### Create a comment on a policy

```http
  POST /v1/policy/{policy_id}/comments/
```

| Headers         | Type     | Description                             |
|:----------------|:---------|:----------------------------------------|
| `Authorization` | `string` | Bearer Token of the user. **Required**. |

| Path Parameters | Type     | Description                                   |
|:----------------|:---------|:----------------------------------------------|
| `policy_id`     | `string` | ID of the policy to comment on. **Required**. |

| Body      | Type     | Description                           |
|:----------|:---------|:--------------------------------------|
| `content` | `string` | Content of the comment. **Required**. |

### List all comments by policy_id

```http
  GET /v1/policy/{policy_id}/comments/
```

| Headers         | Type     | Description                             |
|:----------------|:---------|:----------------------------------------|
| `Authorization` | `string` | Bearer Token of the user. **Required**. |

| Path Parameters | Type     | Description                                          |
|:----------------|:---------|:-----------------------------------------------------|
| `policy_id`     | `string` | ID of the policy to list comments for. **Required**. |

## Authors

- [Gaurav Yadav](https://github.com/theydvgaurav)

