
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_bd
from entities.usuarios import Usuarios
from dto.LoginRequest import LoginRequest
from controller.SecurityController import SecurityController

router = APIRouter()

@router.post("/login/usuarios")
def ingresar_user(request: LoginRequest, db: Session = Depends(get_bd)):
    try:
        correo = request.correo.strip().lower()
        user_db = db.query(Usuarios).filter(Usuarios.correo == correo).first()
        hash_db = user_db.contrasenia if user_db is not None else None

        if user_db is None or not SecurityController.verificar_contrasenia(
            request.password, hash_db
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "mensaje": f"Bienvenido al sistema {user_db.nombres}",
            "Code": 1,
            "access_token": SecurityController.crear_token_acceso(user_db.id,user_db.correo)
            #"token_type": "bearer",
        }
    except Exception as err:
        return {"error":f"error interno {err}"}

