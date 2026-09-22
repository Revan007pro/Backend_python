from sqlalchemy import Column, Integer,String,DECIMAL,ForeignKey,TIMESTAMP,func
from sqlalchemy.orm import relationship
from database import Base

class Usuarios(Base):
    __tablename__='usuarios'

    id=Column(Integer(),primary_key=True,autoincrement=True)
    nombres=Column(String(50),nullable=False)
    apellidos=Column(String(50),nullable=True)
    correo=Column(String(70),nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())
    contrasenia=Column(String(50),nullable=False)

    
    #imagen= decidir despues donde va a ir las imagenes