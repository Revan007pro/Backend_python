import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

#DATABASE = os.getenv("DATABASE_URL")
#if not DATABASE:
#    raise RuntimeError("Configura DATABASE_URL antes de iniciar la aplicación")

DATABASE =  "mysql+pymysql://usuario:user1@localhost:3306/tienda_virtual"

motor=create_engine(DATABASE, echo=False, pool_pre_ping=True)

session_local=sessionmaker(autocommit=False, autoflush=False,bind=motor)
Base=declarative_base() #constuctor para poder crear n cantidad de objetos

def get_bd():
    sb=session_local()
    try:
        yield sb
    finally:
        sb.close()