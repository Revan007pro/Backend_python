from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from database import get_bd
from repository.UsuariosRepository import UsuariosRepository
from entities.usuarios import Usuarios
from dto.UsuariosRequest import UsuariosRequest
from dto.CambiarContrasenia import CambiarContrasenia #as change
from typing import List
from controller.SecurityController import SecurityController
from dto.CrearUsuario import CrearUsuario


router = APIRouter(
    #prefix=,
    #tags=["users"] # Esto organiza la documentación de Swagger
)


@router.get("/listar/usuarios",response_model=List[UsuariosRequest])
def listar_usuarios(db:Session=Depends(get_bd)):
    return UsuariosRepository.find_all(db)

@router.post("/cambiar_contrasenia/{idUser}")
def cammbiar_contrasenia(idUser:int,request:CambiarContrasenia,db:Session=Depends(get_bd)):
    try:
        respuesta={}
        new_contrasenia:str=request.new_contrasenia
        confi_contrasenia:str=request.confir_contrasenia
        userDB=db.query(Usuarios).where(Usuarios.id==idUser).first()

        if not userDB:
            respuesta["mensaje"]="no se encontro el usuario"
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=respuesta)
        if new_contrasenia == "" or not new_contrasenia:
            respuesta["mensaje"]="hay algun error en la contraseña"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        if confi_contrasenia == "" or not confi_contrasenia:
            respuesta["mensaje"]="hay algun error en confirmacion de la contraseña"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        if new_contrasenia != confi_contrasenia:
            respuesta["mensaje"]="contraseñas no coinciden"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        userDB.contrasenia = new_contrasenia
        db.commit()
        db.refresh(userDB)
        return {"mensaje": "Contraseña cambiada exitosamente"}
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la contraseña: {err}"
        )
    

@router.post("/crear/usuario")
def crear_usuario(request: CrearUsuario,db:Session=Depends(get_bd)):
    respuesta={}
    try:
        new_user=request.new_nombre
        new_apellidos=request.new_apellidos
        new_correo=request.new_correo
        new_contrasenia=request.new_contrasenia
        confir_contra=request.confir_contrasenia

        user_db=db.query(Usuarios).filter(Usuarios.correo==new_correo).first()
        

        if user_db !=None:
            respuesta["mensaje"]="el usuario ya existe en la base de datos"
            raise HTTPException(status_code=status.HTTP_226_IM_USED,detail=respuesta)

        if new_user=="":
            respuesta["mensaje"]="Tiene que ingresar un nombre valido"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=respuesta)
        if new_apellidos=="":
            respuesta["mensaje"]="Tiene que ingresar apellidos validos"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=respuesta)
        if new_correo=="":
            respuesta["mensaje"]="Tiene que ingresar un correo valido"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=respuesta)
        if new_contrasenia=="":
            respuesta["mensaje"]="Tiene que ingresar una contraseña"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=respuesta)
        if confir_contra=="" or new_contrasenia !=confir_contra:
            respuesta["mensaje"]="Las contraseñas no coinciden"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=respuesta)
        
        password_encriptada = SecurityController.cifrar_contrasenia(new_contrasenia)
        new_usuario=Usuarios(
            nombres=new_user,
            apellidos=new_apellidos,
            correo=new_correo,
            contrasenia=password_encriptada 
        )
        db.add(new_usuario)
        db.commit()
        db.refresh(new_usuario)
        respuesta["mensaje"]="usuario creado exitosamente"

        return HTTPException(status_code=status.HTTP_201_CREATED,detail=respuesta)
        #return {"mensaje": "usuario creado exitosamente"}
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al interno del servidor: {err}"
        )





#@router.post("", response_model=ProductoResponseDTO, status_code=status.HTTP_201_CREATED)
#def crear_producto(producto: ProductoCreateDTO, db: Session = Depends(get_db)):
#    return ProductoRepository.save(db, producto)
