from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timezone

from . import schemas, models, utils, database

app = FastAPI()
security = HTTPBearer()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not utils.verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    token = utils.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}    

@app.post("/auth/register")
def register(req: schemas.RegisterRequest, db:Session = Depends(get_db)):
    existing_email = db.query(models.User).filter(models.User.email == req.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    hashed_pw = utils.hash_password(req.password)
    user = models.User(
        email=req.email,
        password_hash=hashed_pw,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token =  utils.create_verification_token({"sub": str(user.id)})
    utils.send_email_verify(req.email, token)
    return {
    "message": "User registered successfully! Verification email has been sent.",
    "email": user.email
    }

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/auth/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        db.commit()
        return{"message": "Email verified successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or Expired token")
        
@app.get("/me", response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/forgot-password")
def forgot(req: schemas.ForgotRequest, db: Session = Depends(get_db)):
    email = req.email
    existing_email = db.query(models.User).filter(models.User.email == email).first()
    if not existing_email:
        raise HTTPException(status_code=404, detail="Email not found!")
    token = utils.create_reset_token({"sub": email})
    utils.send_email_reset(email, token)
    return {
        "message": "Reset password has been sent! Check your email"
    }
    
@app.post("/reset-password")
def reset(req: schemas.ResetPassword, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(req.token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_email: str = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if req.new_password != req.konfirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        user.password_hash = utils.hash_password(req.new_password)
        db.commit()
        db.refresh(user)
        return {"message": "Password changed successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
