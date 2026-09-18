# Laboratorio 1 — GitHub, Docker y API REST

## Integrante
- Nombre completo — usuario GitHub

_(Laboratorio desarrollado individualmente; ver nota en la sección de Dificultades y aprendizajes)_

## Descripción
API REST sencilla para gestionar notas de trabajo de un equipo (`team-notes-api`).
Permite crear, consultar, actualizar y eliminar notas, cada una con título, contenido,
autor y fecha de creación.

## Tecnologías
- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy (ORM)
- Docker y Docker Compose

## Estructura del proyecto
```
team-notes-api/
├── app/
│   ├── main.py        # Endpoints de la API
│   ├── models.py       # Modelo SQLAlchemy de Note
│   ├── schemas.py       # Esquemas Pydantic (validación)
│   └── database.py      # Conexión a PostgreSQL
├── Dockerfile
├── compose.yaml
├── .env.example
├── requirements.txt
├── .gitignore
└── .dockerignore
```

## Estrategia de creación de la tabla
La tabla `notes` se crea automáticamente al iniciar la API mediante
`Base.metadata.create_all()` (SQLAlchemy), usando el modelo definido en `app/models.py`.
No se requiere un script SQL manual ni migraciones adicionales para este laboratorio.

## Cómo ejecutar

1. Copiar el archivo de variables de entorno:
   ```
   cp .env.example .env
   ```
   (cambiar al menos `DB_PASSWORD` para la ejecución local)

2. Levantar los servicios:
   ```
   docker compose up --build
   ```

3. La API queda disponible en `http://localhost:8000`.

## Endpoints

| Operación       | Método | Ruta          | Descripción                        |
|-----------------|--------|---------------|-------------------------------------|
| Estado del servicio | GET    | /health       | Informa que la API está activa      |
| Listar notas     | GET    | /notes        | Devuelve todas las notas            |
| Consultar nota    | GET    | /notes/{id}    | Devuelve una nota por id            |
| Crear nota       | POST   | /notes        | Registra una nueva nota             |
| Actualizar nota    | PUT    | /notes/{id}    | Actualiza una nota existente        |
| Eliminar nota     | DELETE | /notes/{id}    | Elimina una nota existente          |

## Pruebas realizadas

_(Completar con capturas de pantalla de Postman/Insomnia/Thunder Client/curl para cada endpoint)_

| Prueba                  | Resultado esperado           | Resultado obtenido |
|--------------------------|-------------------------------|----------------------|
| GET /health              | Estado de API activo          |                      |
| GET /notes sin registros    | Lista vacía                  |                      |
| POST /notes válido        | 201 y nota creada             |                      |
| POST /notes inválido       | 400                           |                      |
| GET /notes/{id} existente    | 200 y nota encontrada          |                      |
| GET /notes/{id} inexistente   | 404                           |                      |
| PUT /notes/{id} válido      | 200 y nota actualizada          |                      |
| PUT /notes/{id} inexistente   | 404                           |                      |
| DELETE /notes/{id} existente  | 200                           |                      |
| DELETE /notes/{id} inexistente | 404                           |                      |

## Persistencia
Se verificó que los datos persisten tras `docker compose down` y `docker compose up`,
gracias al volumen `db_data` definido en `compose.yaml`.

## Dificultades y aprendizajes

_(Completar: dificultades encontradas, cómo se resolvieron, y qué se aprendió del
proceso de ramas, Pull Requests, resolución de conflictos y Docker. Indicar que el
laboratorio se desarrolló individualmente y cómo se adaptó el flujo de revisión
cruzada — ej. autorevisión documentada en cada PR — para cumplir igual con la
práctica de branching, PRs y resolución de conflictos.)_

## Repositorio
Link: _(pegar aquí el link del repositorio en GitHub)_
