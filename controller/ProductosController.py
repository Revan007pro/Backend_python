from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from database import get_bd
from entities.productos import Productos
from repository.ProductosRepository import ProductosRepository
from dto.ProductosRequest import ProductosRequest
from typing import List


router = APIRouter(
    prefix="/listar/productos",
    tags=["Productos"] # Esto organiza la documentación de Swagger
)


@router.get("",response_model=List[ProductosRequest])
def listar_productos(db:Session=Depends(get_bd)):
    return ProductosRepository.find_all(db)


#@router.post("", response_model=ProductoResponseDTO, status_code=status.HTTP_201_CREATED)
#def crear_producto(producto: ProductoCreateDTO, db: Session = Depends(get_db)):
#    return ProductoRepository.save(db, producto)
