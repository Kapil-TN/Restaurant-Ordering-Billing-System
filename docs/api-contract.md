# API Contract - Authentication Service

> [!IMPORTANT]
> **To Members 2–4**: Please consume the authentication APIs strictly as defined in this contract document. Do not rely on internal implementation details.

## Endpoints

### 1. Register User
Registers a new user account in the system.

* **URL**: `/auth/register`
* **Method**: `POST`
* **Content-Type**: `application/json`

#### Request Body
```json
{
  "name": "kapil",
  "email": "k@mail.com",
  "password": "123"
}
```

#### Response (Success - 200 OK)
```json
{
  "message": "created"
}
```

---

### 2. Login User
Authenticates a user and returns a JSON Web Token (JWT).

* **URL**: `/auth/login`
* **Method**: `POST`
* **Content-Type**: `application/json`

#### Request Body
```json
{
  "email": "k@mail.com",
  "password": "123"
}
```

#### Response (Success - 200 OK)
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Error Response (Unauthorized - 401 Unauthorized)
Returned if the email does not exist or the password is incorrect.
```json
{
  "message": "invalid"
}
```

---

### 3. Get User Profile
Retrieves the profile information of the currently authenticated user.

* **URL**: `/auth/profile`
* **Method**: `GET`
* **Headers**:
  * `Authorization: Bearer <TOKEN>`

#### Request Body
*None (Empty)*

#### Response (Success - 200 OK)
```json
{
  "id": 1,
  "name": "kapil",
  "role": "customer"
}
```

#### Error Response (Unauthorized - 401 Unauthorized)
Returned if the JWT is missing, invalid, or expired.
```json
{
  "msg": "Missing Authorization Header"
}
```
