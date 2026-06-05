# Secure Authentication Backend (Deploy Ready)

A production-focused Flask authentication backend designed with modern security practices and deployment readiness in mind.

## Features

### Authentication

* User Registration (Signup)
* User Login
* JWT Access Tokens
* JWT Refresh Tokens
* Secure Logout
* Token Revocation / Blocklisting

### Security Features

* Password Hashing using bcrypt
* JWT stored in HttpOnly Cookies
* CSRF Protection Enabled
* Rate Limiting Protection
* Account Lockout After Failed Login Attempts
* Secure Session Cookies
* Security Headers Enabled
* Token Blocklist Support
* Input Validation Ready
* PostgreSQL Database Support

### Deployment Ready

* Environment Variable Configuration
* PostgreSQL Integration
* Flask Blueprints Structure
* Production Security Headers
* Secure Cookie Configuration
* JWT Revocation Support
* Scalable Project Structure

---

## Project Structure

```text
.
├── auth/
│   ├── login.py
│   ├── signup.py
│   └── model.py
│
├── extensions.py
├── main.py
├── run.py
├── requirements.txt
└── .env
```

---

## Required Files

Place the following files inside the `auth` folder:

```text
auth/
├── login.py
├── signup.py
└── model.py
```

Once these files are added, the backend is ready to run.

---

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret_key

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_db

FLASK_ENV=production
```

---

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create a PostgreSQL database.

Update the database credentials in the `.env` file.

Create tables automatically:

```bash
python run.py
```

The application initializes all configured database models.

---

## Running the Server

```bash
python run.py
```

Default configuration:

```text
Host: 0.0.0.0
Port: 5000
```

---

## Security Highlights

### Password Security

Passwords are never stored in plain text.

All passwords are hashed before storage using bcrypt.

### JWT Security

* Access tokens stored in HttpOnly cookies
* Refresh tokens supported
* CSRF protection enabled
* Token revocation supported through blocklisting

### Brute Force Protection

The system supports:

* Failed login tracking
* Temporary account lockout
* Rate limiting

### Security Headers

The backend includes protections such as:

* X-Frame-Options
* X-Content-Type-Options
* Referrer-Policy
* Permissions-Policy
* Content-Security-Policy
* Cache-Control

### Database Security

* SQLAlchemy ORM
* Parameterized queries
* PostgreSQL support
* No raw SQL required

---

## Production Deployment Checklist

Before deployment:

* Configure HTTPS
* Use strong SECRET_KEY values
* Use strong JWT_SECRET_KEY values
* Store secrets in environment variables
* Enable secure cookies
* Configure trusted frontend origins
* Use a production WSGI server (Gunicorn / uWSGI)
* Configure reverse proxy (Nginx)
* Enable monitoring and logging

---

## Backend Status

✅ Secure Authentication Architecture

✅ JWT Cookie-Based Authentication

✅ CSRF Protection

✅ Rate Limiting

✅ Account Lockout Protection

✅ PostgreSQL Integration

✅ Security Headers Enabled

✅ Production-Oriented Configuration

✅ Deploy Ready

Simply add `login.py`, `signup.py`, and `model.py` to the `auth` directory, configure the environment variables, and start the server.
