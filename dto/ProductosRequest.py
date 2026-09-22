from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProductosRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int=Field(...)
    nombre:str=Field(...,min_length=2,max_length=100)

    #precio:float=Field(...,gt=0) #mayor a cero
    #imagen_url:Optional[str]=None