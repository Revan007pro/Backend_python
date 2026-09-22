from sqlalchemy.orm import Session
from entities.productos import Productos
from dto.ProductosRequest import ProductosRequest

class ProductosRepository:
    @staticmethod
    def find_all(db:Session):
        return db.query(Productos).all()

    #@staticmethod
    #def guardar(db.Session,producto_dto:ProductosRequest)
    #nuevo_producto=ProductosRepository(
    #    nombre=produto_dto.nombre,
        #precio
    #)
    #db.add(nuevo_producto)
    #db.commit()
    #db.refresh(nuevo_producto)
    #return nuevo_producto