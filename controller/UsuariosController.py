from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_bd
from repository.UsuariosRepository import UsuariosRepository
from entities.usuarios import Usuarios
from dto.UsuariosRequest import UsuariosRequest
from dto.CambiarContrasenia import CambiarContrasenia
from typing import List
from controller.SecurityController import SecurityController
from dto.CrearUsuario import CrearUsuario

router = APIRouter()


@router.get("/listar/usuarios",response_model=List[UsuariosRequest])
def listar_usuarios(
    db: Session = Depends(get_bd),
    usuario_actual: Usuarios = Depends(SecurityController.obtener_usuario_actual),
):
    return UsuariosRepository.find_all(db)

@router.post("/cambiar_contrasenia")
def cammbiar_contrasenia(
    request: CambiarContrasenia,
    db: Session = Depends(get_bd),
    usuario_actual: Usuarios = Depends(SecurityController.obtener_usuario_actual)):
   


    if not SecurityController.verificar_contrasenia(
        request.current_password, usuario_actual.contrasenia
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta",
        )
    if len(request.new_contrasenia.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña excede el límite admitido",
        )

    try:
        usuario_actual.contrasenia = SecurityController.cifrar_contrasenia(
            request.new_contrasenia
        )
        db.commit()
        db.refresh(usuario_actual)
        return {"mensaje": "Contraseña cambiada exitosamente"}
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la contraseña",
        ) from err

@router.post("/crear/usuario", status_code=status.HTTP_201_CREATED)
def crear_usuario(
    request: CrearUsuario,
    db: Session = Depends(get_bd),
):
    new_user = request.new_nombre.strip()
    new_apellidos = request.new_apellidos.strip()
    new_correo = request.new_correo.strip().lower()
    new_contrasenia = request.new_contrasenia

    if not new_user or not new_apellidos or not new_correo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre, apellidos y correo son obligatorios",
        )
    if request.confir_contrasenia != new_contrasenia:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden",
        )
    if len(new_contrasenia.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña excede el límite admitido",
        )

    if db.query(Usuarios).filter(Usuarios.correo == new_correo).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo crear el usuario con esos datos",
        )

    new_usuario = Usuarios(
        nombres=new_user,
        apellidos=new_apellidos,
        correo=new_correo,
        contrasenia=SecurityController.cifrar_contrasenia(new_contrasenia),
    )
    try:
        db.add(new_usuario)
        db.commit()
        db.refresh(new_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo crear el usuario con esos datos",
        ) from None
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo crear el usuario",
        ) from err

    return {"mensaje": "Usuario creado exitosamente", "id": new_usuario.id}
