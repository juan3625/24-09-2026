# Registro de defectos

## DEF-001 — Módulo de Productos inactivo y sin endpoints ejecutables

- **Requisito/regla:** EP04–EP08; RF05–RF12; RN03–RN08.
- **Casos relacionados:** CP-PROD-01 a CP-PROD-18.
- **Tipo de detección:** Inspección inicial del código y comparación contra el contrato. No fue un `FAILED` de pytest porque la implementación estaba comentada antes de poder ejecutar la suite.
- **Precondición:** Proyecto recibido antes de la corrección.
- **Pasos para reproducir:**
  1. Abrir `app/main.py`, `app/database.py`, `app/schemas.py` y `test/test_products.py`.
  2. Observar que la implementación de Productos y sus pruebas estaban comentadas.
  3. Intentar consultar `POST /products`, `GET /products`, `GET /products/{id}`, `PUT /products/{id}` o `DELETE /products/{id}`.
- **Resultado esperado:** Los cinco endpoints deben existir, validar el payload y responder conforme al contrato del Módulo IV.
- **Resultado obtenido:** El código de Productos no estaba activo; por tanto, el módulo no podía cumplir ni ejecutar el contrato.
- **Severidad:** Crítica.
- **Prioridad:** Crítica.
- **Estado:** Cerrado después de la corrección.
- **Corrección aplicada:** Se activaron la base en memoria, esquemas Pydantic, endpoints, validaciones, pruebas automatizadas y trazabilidad de Productos.
- **Evidencia de corrección:** `docs/evidencia-pytest.txt`.

## Retest de DEF-001

Después de activar el módulo se reejecutaron los casos representativos que verifican creación, consulta inexistente, fronteras, categoría inexistente, actualización y eliminación: CP-PROD-01, CP-PROD-04, CP-PROD-07, CP-PROD-11, CP-PROD-14, CP-PROD-16, CP-PROD-17 y CP-PROD-18. Todos fueron `PASSED` dentro de la ejecución de Productos.

## Regresión posterior

Se ejecutó la suite completa con `pytest -q` después de la corrección. El resultado fue **40 passed, 0 failed**, sin casos bloqueados y sin defectos críticos abiertos confirmados.

## Criterio de clasificación

Un `FAILED` solo se registra como defecto después de descartar error en la prueba, los datos, el ambiente o la configuración. Los defectos deben conservar esperado, obtenido, pasos reproducibles, severidad, prioridad, estado y evidencia.


## DEF-002 — Nombres en blanco aceptados por la validación

- **Requisito/regla:** RN01 y RN03.
- **Casos relacionados:** CP-CAT-17 y CP-PROD-19.
- **Tipo de detección:** Prueba de regresión de validación.
- **Precondición:** API iniciada con la versión previa a la corrección de validación de nombres; datos en memoria en su estado inicial (categoría 1 existente).
- **Pasos para reproducir:**
  1. Enviar `POST /categories` con `{"name":"   "}`.
  2. Enviar `POST /products` con `name="   "` y el resto de campos válidos (`category_id=1`).
  3. Revisar el código de respuesta y consultar `GET /categories` y `GET /products` para confirmar si el registro quedó creado.
- **Resultado obtenido antes de la corrección:** `POST /categories` y `POST /products` aceptaban nombres compuestos únicamente por espacios y respondían HTTP 201.
- **Resultado esperado:** HTTP 422 y ningún registro creado.
- **Severidad:** Media.
- **Prioridad:** Alta.
- **Estado:** Cerrado.
- **Corrección aplicada:** Normalización con `strip()` y rechazo de texto vacío mediante `field_validator`.
- **Evidencia:** `docs/evidencia-pytest.txt`; CP-CAT-17 y CP-PROD-19.

## DEF-003 — Precio no finito aceptado

- **Requisito/regla:** RN04.
- **Caso relacionado:** CP-PROD-20.
- **Tipo de detección:** Prueba de regresión de validación.
- **Precondición:** API iniciada con la versión previa a `allow_inf_nan=False`; existe la categoría 1.
- **Pasos para reproducir:**
  1. Enviar `POST /products` con `price` igual a `Infinity` y el resto de campos válidos.
  2. Revisar el código de respuesta.
  3. Consultar `GET /products` y observar cómo se representa el precio almacenado.
- **Resultado obtenido antes de la corrección:** Un precio `Infinity` podía superar `gt=0` y quedar representado como un valor JSON inválido o nulo.
- **Resultado esperado:** HTTP 422 para `NaN`, `Infinity` y `-Infinity`.
- **Severidad:** Alta.
- **Prioridad:** Alta.
- **Estado:** Cerrado.
- **Corrección aplicada:** `allow_inf_nan=False` en el campo `price`.
- **Evidencia:** `docs/evidencia-pytest.txt`; CP-PROD-20.

## DEF-004 — Error interno con nombre nulo en PATCH

- **Requisito/regla:** Validación de payload y manejo de errores.
- **Caso relacionado:** CP-CAT-18.
- **Tipo de detección:** Prueba directa de caso límite.
- **Precondición:** API iniciada con la versión previa al validador de `CategoryUpdate`; existe la categoría 1.
- **Pasos para reproducir:**
  1. Enviar `PATCH /categories/1` con el cuerpo `{"name": null}`.
  2. Revisar el código de respuesta y el log del servidor.
- **Resultado obtenido antes de la corrección:** `PATCH /categories/1` con `{"name": null}` provocaba `AttributeError` y HTTP 500.
- **Resultado esperado:** HTTP 422 con error de validación.
- **Severidad:** Crítica.
- **Prioridad:** Crítica.
- **Estado:** Cerrado.
- **Corrección aplicada:** Validador explícito en `CategoryUpdate` que rechaza `null` cuando el campo se proporciona.
- **Evidencia:** `docs/evidencia-pytest.txt`; CP-CAT-18.

## DEF-005 — Campos desconocidos aceptados silenciosamente

- **Requisito/regla:** Contrato estricto de payload.
- **Casos relacionados:** CP-CAT-19 y CP-PROD-21.
- **Tipo de detección:** Inspección y prueba de contrato.
- **Precondición:** API iniciada con la versión previa a la configuración `extra="forbid"`; existe la categoría 1.
- **Pasos para reproducir:**
  1. Enviar `POST /categories` con un payload válido y el campo adicional `unexpected=true`.
  2. Enviar `POST /products` con un payload válido y el campo adicional `unexpected=true`.
  3. Revisar los códigos de respuesta.
- **Resultado obtenido antes de la corrección:** Los modelos Pydantic ignoraban campos adicionales.
- **Resultado esperado:** HTTP 422 para campos fuera del contrato.
- **Severidad:** Baja.
- **Prioridad:** Media.
- **Estado:** Cerrado.
- **Corrección aplicada:** Configuración compartida `extra="forbid"`.
- **Evidencia:** `docs/evidencia-pytest.txt`; CP-CAT-19 y CP-PROD-21.
