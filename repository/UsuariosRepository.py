from sqlalchemy.orm import Session
from entities.usuarios import Usuarios
from dto.ProductosRequest import ProductosRequest

class UsuariosRepository:
    @staticmethod
    def find_all(db:Session):
        return db.query(Usuarios).all()

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