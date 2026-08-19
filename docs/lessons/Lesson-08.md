# Lesson-08: Authentication - Password Hashing, JWT, Auth Routes

## Objective

Implement secure user registration and login.

## Files Created

```text
backend/app/core/security.py
backend/app/api/dependencies.py
backend/app/api/routes/auth.py
```

## Knowledge Required

- **Authentication**: Proving who a user is.
- **Authorization**: Checking what a user may access.
- **Password hashing**: One-way password storage.
- **Argon2**: Secure hashing algorithm.
- **JWT**: Signed token containing user identity and expiration.
- **Bearer token**: Token sent in `Authorization` header.
- **HTTP 401**: Unauthorized.
- **HTTP 409**: Conflict, used for duplicate email.

## Data Flow

Register/login request -> password hash verification or creation -> JWT creation -> frontend stores token -> protected routes decode token -> current user loaded from database.

## Common Mistakes

- Storing plain passwords.
- Returning password hashes in API responses.
- Using weak JWT secrets.
- Not checking inactive users.

## Verification

Register a user, log in, call `/api/v1/auth/me` with the token.

