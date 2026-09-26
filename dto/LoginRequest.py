from pydantic import BaseModel,Field

class LoginRequest(BaseModel):
    correo: str = Field(..., min_length=1, max_length=70)
    password: str = Field(..., min_length=1, max_length=72)