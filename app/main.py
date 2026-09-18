import os

from fastapi import FastAPI

from app.database import Base, engine

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(title="team-notes-api")

# Crea las tablas si no existen (estrategia simple de inicializacion para el laboratorio)
Base.metadata.create_all(bind=engine)
