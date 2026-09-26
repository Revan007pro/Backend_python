from pydantic import BaseModel, ConfigDict, Field

class CambiarContrasenia(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    current_password: str = Field(..., min_length=1, max_length=72)
    new_contrasenia: str = Field(..., min_length=12, max_length=72)
    confir_contrasenia: str = Field(..., min_length=12, max_length=72)
