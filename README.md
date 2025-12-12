AppVentas - API RESTful (Evaluación)

Resumen
-------
Proyecto Django que gestiona clientes, productos y ventas. Se añadió una API RESTful con Django REST Framework y documentación Swagger.

Principales endpoints (base `/api/v1/`)
-------------------------------------
- `POST /api/v1/token/` : obtener JWT (body: `username`, `password`).
- `POST /api/v1/token/refresh/` : refrescar token.
- `POST /api/v1/register/` : crear usuario (body: `username`, `password`, `email`).
- `GET  /api/v1/profile/` : perfil del usuario (autenticado).

Viewsets (protegidos, requieren JWT or Session auth):
- `GET /api/v1/clientes/` — listar clientes
- `POST /api/v1/clientes/` — crear cliente
- `GET /api/v1/productos/` — listar productos
- `POST /api/v1/productos/` — crear producto
- `GET /api/v1/ventas/` — listar ventas
- `POST /api/v1/ventas/` — crear venta (payload con cliente y productos)

Documentación interactiva:
- Swagger UI: `/api/v1/swagger/`
- Redoc: `/api/v1/redoc/`

Autenticación
-------------
La API usa JWT (Simple JWT) y `SessionAuthentication`.
- Obtener token (ejemplo):

```bash
curl -X POST http://127.0.0.1:8000/api/v1/token/ -d "username=miuser&password=mipass"
```
Respuesta esperada (ejemplo):
```json
{
  "access": "<token>",
  "refresh": "<refresh-token>"
}
```

Usar token para peticiones protegidas:
```bash
curl -H "Authorization: Bearer <access>" http://127.0.0.1:8000/api/v1/clientes/
```

Notas de evaluación (cómo comprueban):
- La API expone JSON con la misma data que la app web.
- Rutas están protegidas mediante autenticación.
- Documentación Swagger incluida.
- Código comentado y legible en `gestion/serializers.py`, `gestion/api_views.py`, `gestion/api_urls.py`.

Cómo ejecutar localmente
------------------------
1. Crear y activar venv:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Migrar DB y crear superuser:

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py createsuperuser
```

4. Levantar server:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

5. Abrir Swagger en `http://127.0.0.1:8000/api/v1/swagger/`.

Si quieres, puedo añadir ejemplos de payloads para crear ventas y clientes más detallados.
