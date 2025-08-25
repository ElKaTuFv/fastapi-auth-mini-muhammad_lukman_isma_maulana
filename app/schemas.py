from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class RegisterRequest (BaseModel):
    email: EmailStr
    password: str
    
class ForgotRequest (BaseModel):
    email: EmailStr
    
class ResetPassword (BaseModel):
    token: str
    new_password: str
    konfirm_password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
        
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
            
    class Config:
        from_attributes = True