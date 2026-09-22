from pydantic import BaseModel,Field

class LoginRequest(BaseModel):
    nombre: str=Field(...)
    password: str=Field(...)