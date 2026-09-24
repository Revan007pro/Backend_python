from pydantic import BaseModel, ConfigDict, Field

class CambiarContrasenia(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    new_contrasenia:str=Field(...)
    confir_contrasenia:str=Field(...)
