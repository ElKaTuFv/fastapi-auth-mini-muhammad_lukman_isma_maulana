# FastAPI Authentication System

Proyek ini adalah sistem **autentikasi berbasis FastAPI** dengan fitur:

- Registrasi & Login JWT
- Verifikasi Email
- Lupa Password & Reset Password
- Admin Creation via CLI
- Brevo (SMTP) sebagai mail sender

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

## 📦 Instalasi

1. **Clone repository**

   ```bash
   git clone https://github.com/username/fastapi_auth.git
   cd fastapi_auth
   ```

2. **Buat virtual environment**

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

## 🔑 Konfigurasi Environment

Buat file `.env` di root project:

```ini
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
VERIFICATION_TOKEN_EXPIRE_MINUTES=5

# Database
DATABASE_URL=sqlite:///./app.db

# SMTP (Brevo)
SMTP_SERVER=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your_brevo_api_key
FROM_EMAIL=no-reply@yourdomain.com
```

---

## 🗄️ Inisialisasi Database

Jalankan perintah untuk membuat tabel:

```bash
python -m app.db_init
```

---

## 👑 Membuat Admin

Gunakan CLI:

```bash
python -m app.cli create-admin --email admin@example.com --password "S3cret!"
```

---

## 🚀 Menjalankan Server

```bash
uvicorn app.main:app --reload
```

API akan berjalan di: [http://localhost:8000](http://localhost:8000)

---

## 📡 Endpoint

### 🔐 Auth

- **POST** `/auth/register` → Registrasi user
- **POST** `/auth/login` → Login, return JWT
- **GET** `/auth/verify?token=...` → Verifikasi email

### 🔑 Forgot & Reset Password

- **POST** `/forgot-password`
  - Input: email → kirim link reset ke email
- **POST** `/reset-password`
  - Input: token, new_password, konfirm_password
  - Update password setelah validasi

---

## 📧 Email Verification

Email dikirim menggunakan **Brevo SMTP**:

```python
def send_email_verify(email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Email Verification"
    msg["From"] = SMTP_USER
    msg["To"] = email
    link = f"http://localhost:8000/auth/verify?token={token}"
    msg.set_content(f"Click this link to verify your account:\n\n{link}")
    ...
```

---

## 📝 License

Proyek ini menggunakan lisensi **MIT**.  
Edit di `LICENSE` sesuai nama kamu:

```
MIT License

Copyright (c) 2025 Nama Kamu
```
