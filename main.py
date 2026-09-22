from fastapi import FastAPI
from database import motor,Base
from controller import ProductosController
from controller import UsuariosController
from controller import AuthController

Base.metadata.create_all(bind=motor) #crea automaticamante tablas si no existen

app=FastAPI(title="tienda virtual lizeth Alexandra Agredo Dorado")

app.include_router(ProductosController.router)
app.include_router(UsuariosController.router)
app.include_router(AuthController.router)