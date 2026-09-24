# Plan de Pruebas

## 1. Información general

| Campo | Valor |
|---|---|
| Proyecto | Products & Categories API |
| Versión auditada | 1.0.0 |
| Tecnologías | Python, FastAPI, Pydantic, pytest, TestClient |
| Persistencia | Listas en memoria para ambiente de pruebas |
| Suite | `test/test_categories.py`, `test/test_products.py` |
| Fecha | Septiembre de 2026 |

## 2. Objetivo

Verificar que la API cumpla el contrato funcional de Categorías y Productos, incluyendo respuestas HTTP, estructura JSON, validaciones, fronteras, recursos inexistentes y operaciones de creación, consulta, actualización y eliminación.

## 3. Alcance

### Incluido

- `POST /categories`, `GET /categories`, `GET /categories/{id}`.
- Funcionalidades existentes de Categorías: `PATCH`, `DELETE`, filtros `active` y búsqueda `search`.
- `POST /products`, `GET /products`, `GET /products/{id}`, `PUT /products/{id}`, `DELETE /products/{id}`.
- RF01–RF12 y RN01–RN08 del contrato evaluable.
- Códigos HTTP, payloads JSON, validaciones positivas, negativas y de frontera.
- Automatización reproducible con pytest y TestClient.

### Fuera de alcance

Autenticación, rendimiento, seguridad especializada, interfaz gráfica, despliegue productivo y persistencia real en base de datos.

### Inventario de endpoints incluidos

| # | Método | Endpoint | Módulo | Requisitos | Casos asociados |
|---|---|---|---|---|---|
| 1 | POST | `/categories` | Categorías | RF01, RN01, RN02 | CP-CAT-01, 05, 06, 07, 09, 10, 17, 19 |
| 2 | GET | `/categories` (filtros `active`, `search`) | Categorías | RF02 | CP-CAT-02, 14, 15 |
| 3 | GET | `/categories/{id}` | Categorías | RF03, RF04 | CP-CAT-03, 04, 08 |
| 4 | PATCH | `/categories/{id}` | Categorías | Funcionalidad existente | CP-CAT-11, 16, 18 |
| 5 | DELETE | `/categories/{id}` | Categorías | Funcionalidad existente | CP-CAT-12, 13 |
| 6 | POST | `/products` | Productos | RF05, RN03–RN07 | CP-PROD-01, 09–16, 19, 20, 21 |
| 7 | GET | `/products` | Productos | RF06 | CP-PROD-02 |
| 8 | GET | `/products/{id}` | Productos | RF07, RF08 | CP-PROD-03, 04 |
| 9 | PUT | `/products/{id}` | Productos | RF09, RF10, RN08 | CP-PROD-05, 06, 17, 18 |
| 10 | DELETE | `/products/{id}` | Productos | RF11, RF12 | CP-PROD-07, 08 |

`GET /` y `GET /health` solo se verifican como comprobación de arranque (ver `docs/evidencia-pytest.txt`) y no tienen casos formales.

## 4. Riesgos priorizados

| ID | Riesgo | Probabilidad | Impacto | Prioridad | Casos mitigadores |
|---|---|---|---|---|---|
| R01 | Aceptar precio cero o negativo | Alta | Alto | Crítica | CP-PROD-11, 12 |
| R02 | Permitir stock negativo | Media | Alto | Alta | CP-PROD-14, 15 |
| R03 | Crear producto con categoría inexistente | Media | Alto | Alta | CP-PROD-16, 18 |
| R04 | Permitir categorías duplicadas sin distinguir mayúsculas | Media | Alto | Alta | CP-CAT-07 |
| R05 | Aceptar nombres por debajo del mínimo | Alta | Medio | Alta | CP-CAT-05, CP-PROD-09 |
| R06 | Responder incorrectamente para recursos inexistentes | Media | Alto | Alta | CP-CAT-04, CP-PROD-04, 06, 08 |
| R07 | Actualización que omite validaciones de creación | Media | Alto | Alta | CP-PROD-17, 18 |
| R08 | Código HTTP incorrecto en creación/eliminación | Media | Medio | Media | CP-CAT-01, CP-PROD-01, 07 |

## 5. Estrategia

Se aplicarán pruebas funcionales positivas, negativas y de frontera. Se automatizarán casos representativos con pytest y TestClient, usando datos aislados y restableciendo las listas en memoria antes de cada prueba. Un resultado `FAILED` se investigará antes de clasificarlo como defecto.

> **Adaptación de organización:** la guía utiliza `tests/` como nombre de referencia, pero este proyecto ya estaba organizado con `test/`. Se conserva `test/` para no romper imports ni la organización existente; los comandos equivalentes son `pytest test/test_categories.py -v`, `pytest test/test_products.py -v` y `pytest -v`.

## 6. Ambiente y datos

Python 3.x, FastAPI, Pydantic, pytest, Uvicorn y TestClient. Instalación: `pip install -r requirements.txt`. Ejecución: `pytest -v` desde la raíz. No se usa producción.

Datos principales: categorías `Computadores`, `Accesorios`, `Cámaras`; producto válido `Teclado mecánico / 250000 / 10 / category_id=1`; stock 0; precio 0; precio negativo; stock -1; `category_id=99999`; ID de recurso `99999`.

## 7. Criterios de entrada

La API debe importar e iniciar, los endpoints del alcance deben existir, las dependencias deben estar instaladas, el contrato debe estar disponible y el ambiente de pruebas debe ser aislado.

## 8. Suspensión y reanudación

Se suspende si la API no inicia, el ambiente no está disponible o un defecto bloquea los casos críticos. Se reanuda cuando la causa se corrige, la versión corregida está instalada y el ambiente queda listo para retest.

## 9. Criterios de salida

- 100 % de RF01–RF12 y RN01–RN08 trazados.
- 100 % de casos críticos ejecutados y al menos 90 % del total ejecutado.
- Al menos 90 % de aprobación; objetivo interno recomendado: 95 %.
- Cero defectos críticos abiertos.
- Al menos 15 casos automatizados.
- Todo defecto relacionado con su caso y requisito.

## 10. Responsables

El equipo QA es responsable de diseño, automatización, ejecución, análisis, registro de defectos, retest, regresión e informe. Cada integrante debe poder explicar casos positivos, negativos, de frontera y análisis de fallos.
