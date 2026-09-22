from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from database import get_bd
from repository.UsuariosRepository import UsuariosRepository
from dto.UsuariosRequest import UsuariosRequest
from typing import List


router = APIRouter(
    prefix="/listar/usuarios",
    tags=["users"] # Esto organiza la documentación de Swagger
)


@router.get("",response_model=List[UsuariosRequest])
def listar_usuarios(db:Session=Depends(get_bd)):
    return UsuariosRepository.find_all(db)


#@router.post("", response_model=ProductoResponseDTO, status_code=status.HTTP_201_CREATED)
#def crear_producto(producto: ProductoCreateDTO, db: Session = Depends(get_db)):
#    return ProductoRepository.save(db, producto)
