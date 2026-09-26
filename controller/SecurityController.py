import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_bd
from entities.usuarios import Usuarios


bearer_scheme = HTTPBearer(auto_error=False)


class SecurityController:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
    @staticmethod
    def cifrar_contrasenia(password_str: str) -> str:
        password_bytes = password_str.encode("utf-8")
        if len(password_bytes) > 72:
            raise ValueError("La contraseña excede el límite admitido")
        return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verificar_contrasenia(password_str: str, hash_almacenado: str | None) -> bool:
        if not hash_almacenado:
            return False
        try:
            return bcrypt.checkpw(
                password_str.encode("utf-8"), hash_almacenado.encode("utf-8")
            )
        except (ValueError, TypeError):
            return False

    @staticmethod
    def crear_token_acceso(user_id: int, correo: str) -> str:
        if not SecurityController.SECRET_KEY or len(SecurityController.SECRET_KEY.encode("utf-8")) < 32:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="La autenticación no está configurada de forma segura",
            )

        now = datetime.now(timezone.utc)
    
        token_payload = {
            "sub": str(user_id),
            "email": correo,          # <-- Aquí guardas el correo de forma segura
            "iat": now,
            "exp": now + timedelta(minutes=60)
        }
        return jwt.encode(
            token_payload,
            SecurityController.SECRET_KEY,
            algorithm="HS256"
        )

    @staticmethod
    def obtener_usuario_actual(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
        db: Session = Depends(get_bd),
    ) -> Usuarios:
        unauthorized = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida o token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if credentials is None:
            raise unauthorized

        try:
            payload = jwt.decode(credentials.credentials,SecurityController.SECRET_KEY, algorithms=["HS256"])
            user_id = int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            raise unauthorized from None

        user = db.query(Usuarios).filter(Usuarios.id == user_id).first()
        if user is None:
            raise unauthorized
        return user