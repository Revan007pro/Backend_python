from sqlalchemy import Column, Integer,String,DECIMAL,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class Productos(Base):
    __tablename__='productos'

    id=Column(Integer(),primary_key=True)
    nombre=Column(String(50),nullable=False)
    #imagen= decidir despues donde va a ir las imagenes