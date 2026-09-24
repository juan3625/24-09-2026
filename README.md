# Products & Categories API

Proyecto de pruebas del Módulo IV: API REST con FastAPI para administrar categorías y productos de una tienda tecnológica.

## Estructura

```text
 test-productos-y-categorias/
 ├── app/
 │   ├── __init__.py
 │   ├── database.py
 │   ├── main.py
 │   └── schemas.py
 ├── test/
 │   ├── __init__.py
 │   ├── test_categories.py
 │   └── test_products.py
 ├── docs/
 │   ├── plan-pruebas.md
 │   ├── matriz-trazabilidad.md
 │   ├── casos-prueba.md
 │   ├── registro-defectos.md
 │   ├── informe-ejecucion.md
 │   ├── CASOS_DE_PRUEBA.TXT
 │   └── Evidencias_Pruebas_Categorias.docx
 ├── Liteclient/
 ├── README.md
 └── requirements.txt
```

Los datos se almacenan temporalmente en memoria y se restablecen en las pruebas mediante fixtures. No se utiliza una base de datos productiva.

## Instalación

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar la API

Desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

Documentación interactiva:

- <http://127.0.0.1:8000/docs>
- <http://127.0.0.1:8000/redoc>

## Endpoints del contrato evaluable

| Método | Endpoint | Descripción | Éxito |
|---|---|---|---:|
| POST | `/categories` | Crear categoría | 201 |
| GET | `/categories` | Listar categorías | 200 |
| GET | `/categories/{category_id}` | Consultar categoría | 200 |
| POST | `/products` | Crear producto | 201 |
| GET | `/products` | Listar productos | 200 |
| GET | `/products/{product_id}` | Consultar producto | 200 |
| PUT | `/products/{product_id}` | Actualizar producto | 200 |
| DELETE | `/products/{product_id}` | Eliminar producto | 204 |

Se conservan además las funcionalidades existentes de Categorías: `PATCH /categories/{category_id}`, eliminación de categorías, filtros por `active` y búsqueda por `search`.

## Validaciones principales

- Categorías: nombre obligatorio de 3 a 60 caracteres y sin duplicados ignorando mayúsculas/minúsculas.
- Productos: nombre de 3 a 80 caracteres, precio mayor que cero, stock mayor o igual que cero y categoría existente.
- Las actualizaciones completas de Productos (`PUT`) mantienen las validaciones de creación.

## Ejecutar las pruebas

```bash
pytest -v

```

Los tests utilizan `TestClient`, fixtures de aislamiento y comentarios `CP-CAT-XX` / `CP-PROD-XX` para conservar trazabilidad con `docs/casos-prueba.md`.

## Documentación QA

La auditoría consolidada se encuentra en `docs/` y sigue el flujo requisito → riesgo → caso → ejecución → defecto → informe. El informe de ejecución debe completarse con la salida real del comando `pytest -v` y el commit auditado.
