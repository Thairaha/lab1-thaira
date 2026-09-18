# Laboratorio 1 — GitHub, Docker y API REST

## Integrantes
- Thaira Hernandez — [Thairaha](https://github.com/Thairaha)

> Laboratorio realizado de forma individual. El flujo de trabajo original (pensado para
> parejas) se adaptó: en lugar de una revisión cruzada entre compañeros, cada Pull
> Request incluye un comentario de auto-revisión antes del merge, verificando que el
> código cumple los requisitos del laboratorio (endpoints, códigos de estado, pruebas).

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

Todas las pruebas se ejecutaron con Postman contra la API corriendo en Docker
(`docker compose up --build`). Capturas de cada prueba disponibles en el documento de
entrega.

| Prueba                  | Resultado esperado           | Resultado obtenido |
|--------------------------|-------------------------------|----------------------|
| GET /health              | Estado de API activo          | OK — 200, `{"status":"ok","environment":"development"}` |
| GET /notes sin registros    | Lista vacía                  | OK — 200, `[]` |
| POST /notes válido        | 201 y nota creada             | OK — 201, nota creada con `id` y `created_at` |
| POST /notes inválido       | 400                           | OK — 400, `{"detail":"Invalid or missing data"}` |
| GET /notes/{id} existente    | 200 y nota encontrada          | OK — 200, nota devuelta correctamente |
| GET /notes/{id} inexistente   | 404                           | OK — 404, `{"detail":"Note not found"}` |
| PUT /notes/{id} válido      | 200 y nota actualizada          | OK — 200, nota actualizada correctamente |
| PUT /notes/{id} inexistente   | 404                           | OK — 404, `{"detail":"Note not found"}` |
| DELETE /notes/{id} existente  | 200                           | OK — 200, nota eliminada |
| DELETE /notes/{id} inexistente | 404                           | OK — 404, `{"detail":"Note not found"}` |

## Persistencia
Se verificó que los datos persisten tras `docker compose down` y `docker compose up`
(sin usar `-v`), gracias al volumen `db_data` definido en `compose.yaml`: la nota
creada durante las pruebas siguió apareciendo en `GET /notes` después de reiniciar los
contenedores.

## Dificultades y aprendizajes

- **Condición de carrera API/base de datos**: al levantar `api` y `db` juntos, la API
  intentaba conectarse a PostgreSQL antes de que este aceptara conexiones
  (`depends_on` solo esperaba a que el contenedor arrancara, no a que el servicio
  estuviera listo). Se resolvió agregando un `healthcheck` con `pg_isready` a `db` y
  cambiando `depends_on` de `api` a `condition: service_healthy`.
- **Instalación de Docker Desktop en Windows**: requirió habilitar WSL2
  (`wsl --install`) y reiniciar el sistema antes de que Docker Desktop pudiera
  ejecutar contenedores Linux.
- **Trabajo individual con flujo de Git colaborativo**: al no tener un compañero de
  equipo, se adaptó el flujo original manteniendo todos los elementos exigidos
  (ramas `main`/`develop`, ramas feature, Pull Requests, conflicto de merge real y su
  resolución), sustituyendo la revisión cruzada por una auto-revisión documentada en
  cada PR antes de fusionarlo.
- **Aprendizaje principal**: el valor de separar el trabajo en commits pequeños y
  descriptivos por rama feature, y de nunca usar `docker compose down -v` cuando se
  quiere conservar los datos, ya que ese flag elimina también el volumen de la base
  de datos.

## Repositorio
Link: https://github.com/Thairaha/lab1-thaira
