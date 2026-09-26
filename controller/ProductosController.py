from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from database import get_bd
from entities.productos import Productos
from repository.ProductosRepository import ProductosRepository
from dto.ProductosRequest import ProductosRequest
from controller.SecurityController import SecurityController
from entities.usuarios import Usuarios
from typing import List


router = APIRouter(
    #prefix="/listar/productos",
    #tags=["Productos"] # Esto organiza la documentación de Swagger
)


@router.get("/listar/productos",response_model=List[ProductosRequest])
def listar_productos(
    db: Session = Depends(get_bd),
    usuario_actual: Usuarios = Depends(SecurityController.obtener_usuario_actual),
):
    return ProductosRepository.find_all(db)


#@router.post("", response_model=ProductoResponseDTO, status_code=status.HTTP_201_CREATED)
#def crear_producto(producto: ProductoCreateDTO, db: Session = Depends(get_db)):
#    return ProductoRepository.save(db, producto)
