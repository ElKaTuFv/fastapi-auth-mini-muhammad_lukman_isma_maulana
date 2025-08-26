# FastAPI Authentication System

This project is an **authentication system built with FastAPI** featuring:

- Registration & Login with JWT
- Email Verification
- Forgot Password & Reset Password
- Admin Creation via CLI
- Brevo (SMTP) as the mail sender

---

## ⚙️ Requirements

- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy
- Passlib (bcrypt)
- PyJWT
- Brevo SMTP account

---

## 📦 Installation

1. **Clone repository**

   ```bash
   git clone https://github.com/username/fastapi_auth.git
   cd fastapi_auth
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Environment Configuration

Create a `.env` or copy from `.env.example` file in the project root:

```ini
SECRET_KEY=changeme
ACCESS_TOKEN_EXPIRE_MINUTES=20

VERIFICATION_TOKEN_EXPIRE_MINUTES=5

RESET_TOKEN_EXPIRE_MINUTES=5

SMTP_SERVER=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=get_in_email
SMTP_PASS=get_in_email

```

---

## 🚀 Run the Server

```bash
uvicorn app.main:app --reload
```

The API will run at: [http://localhost:8000](http://localhost:8000) and the database will be created automatically.

---

## 👑 Create Admin

Use the CLI:

```bash
python -m app.cli create-admin --email admin@example.com --password "S3cret!"
```

An admin account will be created automatically.

---

## 📡 Endpoint

### 🔐 Auth

- **POST** `/auth/register` → User registration
  - Input: email, password
  - curl request:
  ```curl
      curl -X 'POST' \
          'http://127.0.0.1:8000/auth/register' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "email": "m.lukmanisma@gmail.com",
          "password": "123456789"
      }'
  ```
- **POST** `/auth/login` → User login, returns JWT
  - Input: email, password
  - curl request:
  ```curl
      curl -X 'POST' \
        'http://127.0.0.1:8000/auth/login' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "email": "m.lukmanisma@gmail.com",
        "password": "123456789"
      }'
  ```
- **GET** `/auth/verify?token=...` → Email verification
  - curl request:
  ```curl
      curl -X 'GET' \
        'http://127.0.0.1:8000/auth/verify?token=eyJhbGciOiJIUzI1NiIxxxx' \
        -H 'accept: application/json'
  ```
- **GET** `/me` → Get user profile (requires token)
  - curl request:
  ```curl
      curl -X 'GET' \
        'http://127.0.0.1:8000/me' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6Ikxxxx'
  ```

### 🔑 Forgot & Reset Password

- **POST** `/forgot-password`
  - Input: email → Sends reset link to user email
  - curl request:
  ```curl
      curl -X 'POST' \
        'http://127.0.0.1:8000/forgot-password' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "email": "m.lukmanisma@gmail.com"
      }'
  ```
- **POST** `/reset-password` → Reset password with token
  - Input: token, new_password, konfirm_password
  - curl request:
  ```curl
      curl -X 'POST' \
        'http://127.0.0.1:8000/reset-password' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwZW1idXJ1bWFnYW5nQGdtYWlsLmNvbSIsImV4cCI6MTc1NjExMzU0NX0.YvzS6dNx-86Ggxd6Lt5WwxMUEpQXGcX0RIHz5W-oUAA",
        "new_password": "987654321",
        "konfirm_password": "987654321"
      }'
  ```

---

## 💡 Candidate Questions

Q: What other services would improve this project, and why?

1. Email Verification
   Ensures users validate their identity and helps prevent fake signups.

2. Send Email Service
   Provides communication with users (Verification emails, password resets).

3. Forgot Password
   Allows users to securely request a password reset if they forget their credentials.

4. Reset Password
   Enhances account recovery by letting users update their password via a secure token.
