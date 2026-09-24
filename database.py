from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE =  "mysql+pymysql://usuario:user1@localhost:3306/tienda_virtual"

motor=create_engine(DATABASE,echo=True)

session_local=sessionmaker(autocommit=False, autoflush=False,bind=motor)
Base=declarative_base() #constuctor para poder crear n cantidad de objetos

def get_bd():
    sb=session_local()
    try:
        yield sb
    finally:
        sb.close()