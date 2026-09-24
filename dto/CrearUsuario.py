from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CrearUsuario(BaseModel):
    new_nombre:str=Field(...)
    new_apellidos:str=Field(...)
    new_correo:str=Field(...)
    fecha_registro:Optional[datetime]=None
    new_contrasenia:str=Field(...)
    confir_contrasenia:str=Field(...)
