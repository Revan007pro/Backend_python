# Configuración

Configura la conexión y una clave JWT aleatoria de al menos 32 bytes antes de iniciar la API:

```sh
export DATABASE_URL='mysql+pymysql://usuario:contraseña@localhost:3306/tienda_virtual'
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
uvicorn main:app --host 127.0.0.1 --port 8000
```

No publiques estas variables ni las guardes en el repositorio. Los tokens de acceso expiran a los 15 minutos. Usa `Authorization: Bearer <access_token>` para listar usuarios, listar productos o cambiar tu contraseña.

## Migración de MySQL existente

`Base.metadata.create_all()` no modifica columnas ni índices existentes. Antes de desplegar, revisa y resuelve correos duplicados; después aplica:

```sql
ALTER TABLE usuarios MODIFY contrasenia VARCHAR(60) NOT NULL;
ALTER TABLE usuarios ADD CONSTRAINT uq_usuarios_correo UNIQUE (correo);
```

Haz una copia de seguridad y valida la migración en una copia de la base antes de producción.
