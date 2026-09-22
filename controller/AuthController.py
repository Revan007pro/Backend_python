
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from database import get_bd
from entities.usuarios import Usuarios
from dto.LoginRequest import LoginRequest
#from typing import List

router=APIRouter()
class AuthController:

    @router.post("/login/usuarios")
    def ingresar_user(request:LoginRequest,db:Session=Depends(get_bd)):
        try:
            respuesta={}
            nombres=request.nombre
            contrasenia=request.password

            user_db = db.query(Usuarios).filter(Usuarios.nombres == nombres).first()

            if not nombres and not contrasenia:
                respuesta["mensaje"]="debe ingresar datos"
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=respuesta)

            
            if not user_db:
                respuesta["mensaje"] = "Usuario no encontrado"
                respuesta["Code"] = 6
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=respuesta)

            if nombres and contrasenia:
                respuesta["mensaje"]=f"Bienvenido al sistema {user_db.nombres}"
                raise HTTPException(status_code=status.HTTP_200_OK, detail=respuesta)

            #return{
            #    "mensaje":f"bienvenido {user_db}",
            #    "codigo":1
            #}
        except HTTPException as http_err:
            raise http_err
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"mensaje": f"Error interno del servidor: {str(err)}"}
            )

