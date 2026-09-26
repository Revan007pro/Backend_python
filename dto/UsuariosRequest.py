from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class UsuariosRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int=Field(...)
    nombres: str = Field(..., min_length=2, max_length=50)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=50)
    correo: str = Field(..., min_length=2, max_length=70)
    fecha_registro: datetime = Field(...) 
