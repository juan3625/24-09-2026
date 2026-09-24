# Casos de prueba

Los resultados obtenidos y estados reflejan la ejecución final registrada en docs/evidencia-pytest.txt.

## Categorías

### CP-CAT-01 — Crear categoría válida

- Título: Crear categoría válida
- Requisito: RF01 / Endpoint: `POST /categories`
- Prioridad: Alta
- Precondiciones: API disponible.
- Datos: `{"name":"Monitores","description":"Pantallas para computadores"}`
- Pasos: Enviar el JSON al endpoint y revisar respuesta.
- Resultado esperado: HTTP 201, objeto creado y nombre igual al enviado.
- Resultado obtenido: HTTP 201; categoría creada correctamente.
- Estado: PASSED

### CP-CAT-02 — Listar categorías

- Título: Listar categorías
- Requisito: RF02 / Endpoint: `GET /categories`
- Prioridad: Media
- Precondiciones: Existe al menos una categoría.
- Datos: Sin payload.
- Pasos: Consultar el endpoint.
- Resultado esperado: HTTP 200 y lista JSON.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-03 — Consultar categoría existente

- Título: Consultar categoría existente
- Requisito: RF03 / Endpoint: `GET /categories/{id}`
- Prioridad: Alta
- Precondiciones: Existe la categoría 1.
- Datos: `id=1`.
- Pasos: Consultar `/categories/1`.
- Resultado esperado: HTTP 200 y objeto con `id=1`.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-04 — Consultar categoría inexistente

- Título: Consultar categoría inexistente
- Requisito: RF04 / Endpoint: `GET /categories/{id}`
- Prioridad: Alta
- Precondiciones: No existe el ID 99999.
- Datos: `id=99999`.
- Pasos: Consultar `/categories/99999`.
- Resultado esperado: HTTP 404.
- Resultado obtenido: HTTP 404; detalle `Category not found`.
- Estado: PASSED

### CP-CAT-05 — Nombre de categoría menor a 3 caracteres

- Título: Nombre de categoría menor a 3 caracteres
- Requisito: RN01 / Endpoint: `POST /categories`
- Prioridad: Alta
- Precondiciones: API disponible.
- Datos: `{"name":"AB"}`.
- Pasos: Enviar el payload.
- Resultado esperado: HTTP 422 y no crear categoría.
- Resultado obtenido: HTTP 422; el nombre fue rechazado por tener menos de 3 caracteres.
- Estado: PASSED

### CP-CAT-06 — Nombre de categoría exactamente de 3 caracteres

- Título: Nombre de categoría exactamente de 3 caracteres
- Requisito: RN01 / Endpoint: `POST /categories`
- Prioridad: Media
- Precondiciones: API disponible.
- Datos: `{"name":"Red"}`.
- Pasos: Enviar el payload.
- Resultado esperado: HTTP 201 y categoría creada.
- Resultado obtenido: HTTP 201; categoría `Red` creada correctamente en la frontera inferior válida.
- Estado: PASSED

### CP-CAT-07 — Duplicado case-insensitive

- Título: Duplicado case-insensitive
- Requisito: RN02 / Endpoint: `POST /categories`
- Prioridad: Alta
- Precondiciones: Existe `Computadores`.
- Datos: `{"name":"computadores"}`.
- Pasos: Enviar una categoría con el mismo nombre en minúsculas.
- Resultado esperado: HTTP 409 y no crear duplicado.
- Resultado obtenido: HTTP 409; detalle `Category name already exists`.
- Estado: PASSED

## Productos

### CP-PROD-01 — Crear producto válido

- Título: Crear producto válido
- Requisito: RF05 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe categoría 1.
- Datos: `{"name":"Teclado mecánico","price":250000,"stock":10,"category_id":1}`.
- Pasos: Enviar el payload.
- Resultado esperado: HTTP 201 y producto creado con los datos enviados.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-02 — Listar productos

- Título: Listar productos
- Requisito: RF06 / Endpoint: `GET /products`
- Prioridad: Media
- Precondiciones: Existe al menos un producto.
- Datos: Sin payload.
- Pasos: Consultar el endpoint.
- Resultado esperado: HTTP 200 y lista JSON.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-03 — Consultar producto existente

- Título: Consultar producto existente
- Requisito: RF07 / Endpoint: `GET /products/{id}`
- Prioridad: Alta
- Precondiciones: Existe producto 1.
- Datos: `id=1`.
- Pasos: Consultar `/products/1`.
- Resultado esperado: HTTP 200 y objeto con `id=1`.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-04 — Consultar producto inexistente

- Título: Consultar producto inexistente
- Requisito: RF08 / Endpoint: `GET /products/{id}`
- Prioridad: Alta
- Precondiciones: No existe el ID 99999.
- Datos: `id=99999`.
- Pasos: Consultar `/products/99999`.
- Resultado esperado: HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-05 — Actualizar producto válido

- Título: Actualizar producto válido
- Requisito: RF09 / Endpoint: `PUT /products/{id}`
- Prioridad: Alta
- Precondiciones: Existe producto 1 y categoría 1.
- Datos: Payload válido con nombre actualizado.
- Pasos: Enviar PUT a `/products/1`.
- Resultado esperado: HTTP 200 y datos actualizados.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-06 — Actualizar producto inexistente

- Título: Actualizar producto inexistente
- Requisito: RF10 / Endpoint: `PUT /products/{id}`
- Prioridad: Alta
- Precondiciones: No existe el ID 99999.
- Datos: Payload válido.
- Pasos: Enviar PUT a `/products/99999`.
- Resultado esperado: HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-07 — Eliminar producto existente

- Título: Eliminar producto existente
- Requisito: RF11 / Endpoint: `DELETE /products/{id}`
- Prioridad: Alta
- Precondiciones: Existe producto 1.
- Datos: `id=1`.
- Pasos: Eliminar y consultar nuevamente el producto.
- Resultado esperado: HTTP 204, cuerpo vacío y consulta posterior HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-08 — Eliminar producto inexistente

- Título: Eliminar producto inexistente
- Requisito: RF12 / Endpoint: `DELETE /products/{id}`
- Prioridad: Alta
- Precondiciones: No existe el ID 99999.
- Datos: `id=99999`.
- Pasos: Enviar DELETE.
- Resultado esperado: HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-09 — Nombre menor a 3 caracteres

- Título: Nombre menor a 3 caracteres
- Requisito: RN03 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `name="AB"`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 422.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-10 — Nombre exactamente de 3 caracteres

- Título: Nombre exactamente de 3 caracteres
- Requisito: RN03 / Endpoint: `POST /products`
- Prioridad: Media
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `name="TVX"`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 201.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-11 — Precio igual a cero

- Título: Precio igual a cero
- Requisito: RN04 / Endpoint: `POST /products`
- Prioridad: Crítica
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `price=0`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 422 y no crear producto.
- Resultado obtenido: HTTP 422; `price=0` fue rechazado por la restricción `gt=0`.
- Estado: PASSED

### CP-PROD-12 — Precio negativo

- Título: Precio negativo
- Requisito: RN04 / Endpoint: `POST /products`
- Prioridad: Crítica
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `price=-1000`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 422 y no crear producto.
- Resultado obtenido: HTTP 422; `price=-1000` fue rechazado por la restricción `gt=0`.
- Estado: PASSED

### CP-PROD-13 — Precio mínimo positivo

- Título: Precio mínimo positivo
- Requisito: RN04 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `price=0.01`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 201.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-14 — Stock igual a cero

- Título: Stock igual a cero
- Requisito: RN05/RN07 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `stock=0`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 201; stock 0 aceptado.
- Resultado obtenido: HTTP 201; producto creado con `stock=0`, frontera válida aceptada.
- Estado: PASSED

### CP-PROD-15 — Stock negativo

- Título: Stock negativo
- Requisito: RN05 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe categoría 1.
- Datos: Producto válido con `stock=-1`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 422.
- Resultado obtenido: HTTP 422; `stock=-1` fue rechazado por la restricción `ge=0`.
- Estado: PASSED

### CP-PROD-16 — Categoría inexistente al crear

- Título: Categoría inexistente al crear
- Requisito: RN06 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: No existe categoría 99999.
- Datos: Producto válido con `category_id=99999`.
- Pasos: Enviar POST.
- Resultado esperado: HTTP 404 y no crear producto.
- Resultado obtenido: HTTP 404; detalle `Category not found`.
- Estado: PASSED

### CP-PROD-17 — Precio inválido al actualizar

- Título: Precio inválido al actualizar
- Requisito: RN08/RN04 / Endpoint: `PUT /products/{id}`
- Prioridad: Crítica
- Precondiciones: Existe producto 1 y categoría 1.
- Datos: Payload completo con `price=0`.
- Pasos: Enviar PUT a `/products/1`.
- Resultado esperado: HTTP 422.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-PROD-18 — Categoría inexistente al actualizar

- Título: Categoría inexistente al actualizar
- Requisito: RN08/RN06 / Endpoint: `PUT /products/{id}`
- Prioridad: Alta
- Precondiciones: Existe producto 1; no existe categoría 99999.
- Datos: Payload completo con `category_id=99999`.
- Pasos: Enviar PUT a `/products/1`.
- Resultado esperado: HTTP 404.
- Resultado obtenido: HTTP 404; detalle `Category not found` al actualizar.
- Estado: PASSED

## Casos adicionales de Categorías conservados del proyecto original

### CP-CAT-08 — ID de categoría con formato inválido

- Título: ID de categoría con formato inválido
- Requisito relacionado: Validación de entrada del endpoint de consulta.
- Endpoint: `GET /categories/{category_id}`
- Prioridad: Media
- Precondiciones: API disponible.
- Datos: `category_id=abc`.
- Pasos: Consultar `/categories/abc`.
- Resultado esperado: HTTP 422.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-09 — Nombre de categoría ausente

- Título: Nombre de categoría ausente
- Requisito/regla: RN01
- Endpoint: `POST /categories`
- Prioridad: Alta
- Precondiciones: API disponible.
- Datos: `{"description":"Sin nombre"}`.
- Pasos: Enviar el payload sin `name`.
- Resultado esperado: HTTP 422 y no crear categoría.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-10 — Descripción de categoría demasiado larga

- Título: Descripción de categoría demasiado larga
- Requisito relacionado: Validación de esquema de Categorías.
- Endpoint: `POST /categories`
- Prioridad: Media
- Precondiciones: API disponible.
- Datos: Nombre válido y `description` de 201 caracteres.
- Pasos: Enviar el payload.
- Resultado esperado: HTTP 422.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-16 — Actualizar categoría existente

- Título: Actualizar categoría existente
- Requisito relacionado: Funcionalidad adicional conservada del proyecto.
- Endpoint: `PATCH /categories/{category_id}`
- Prioridad: Media
- Precondiciones: Existe la categoría 1.
- Datos: `{"name":"Computadores portátiles"}`.
- Pasos: Enviar PATCH a `/categories/1`.
- Resultado esperado: HTTP 200 y nombre actualizado.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-11 — Actualizar categoría inexistente

- Título: Actualizar categoría inexistente
- Requisito relacionado: Manejo de recurso inexistente en funcionalidad adicional.
- Endpoint: `PATCH /categories/{category_id}`
- Prioridad: Media
- Precondiciones: No existe la categoría 999.
- Datos: `{"name":"Monitores"}`.
- Pasos: Enviar PATCH a `/categories/999`.
- Resultado esperado: HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-12 — Eliminar categoría existente

- Título: Eliminar categoría existente
- Requisito relacionado: Funcionalidad adicional conservada del proyecto.
- Endpoint: `DELETE /categories/{category_id}`
- Prioridad: Media
- Precondiciones: Existe la categoría 1.
- Datos: `category_id=1`.
- Pasos: Enviar DELETE y consultar nuevamente la categoría.
- Resultado esperado: HTTP 204, cuerpo vacío y consulta posterior HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-13 — Eliminar categoría inexistente

- Título: Eliminar categoría inexistente
- Requisito relacionado: Manejo de recurso inexistente en funcionalidad adicional.
- Endpoint: `DELETE /categories/{category_id}`
- Prioridad: Media
- Precondiciones: No existe la categoría 999.
- Datos: `category_id=999`.
- Pasos: Enviar DELETE.
- Resultado esperado: HTTP 404.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-14 — Filtrar categorías activas

- Título: Filtrar categorías activas
- Requisito relacionado: Funcionalidad adicional conservada del proyecto.
- Endpoint: `GET /categories?active=true`
- Prioridad: Baja
- Precondiciones: Existen categorías activas e inactivas.
- Datos: `active=true`.
- Pasos: Consultar el endpoint con el parámetro.
- Resultado esperado: HTTP 200 y todos los elementos con `active=true`.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED

### CP-CAT-15 — Buscar categorías por nombre

- Título: Buscar categorías por nombre
- Requisito relacionado: Funcionalidad adicional conservada del proyecto.
- Endpoint: `GET /categories?search=comp`
- Prioridad: Baja
- Precondiciones: Existe la categoría `Computadores`.
- Datos: `search=comp`.
- Pasos: Consultar el endpoint con el parámetro.
- Resultado esperado: HTTP 200 y coincidencia `Computadores`.
- Resultado obtenido: PASSED; respuesta observada conforme al resultado esperado.
- Estado: PASSED


## Casos de regresión de validación

### CP-CAT-17 — Nombre de categoría en blanco

- Título: Nombre de categoría en blanco
- Requisito/regla: RN01 / Endpoint: `POST /categories`
- Prioridad: Alta
- Precondiciones: API disponible.
- Datos: `{"name":"   "}`.
- Pasos: Enviar el payload con un nombre compuesto solo por espacios y revisar la respuesta.
- Resultado esperado: HTTP 422; no crear categoría.
- Resultado obtenido: HTTP 422; el nombre en blanco fue rechazado.
- Estado: PASSED

### CP-CAT-18 — Nombre nulo en actualización parcial

- Título: Nombre nulo en actualización parcial
- Requisito/regla: Validación de payload / Endpoint: `PATCH /categories/{category_id}`
- Prioridad: Crítica
- Precondiciones: Existe la categoría 1.
- Datos: `{"name":null}`.
- Pasos: Enviar `PATCH /categories/1` con el payload y revisar código y cuerpo de la respuesta.
- Resultado esperado: HTTP 422, sin error interno.
- Resultado obtenido: HTTP 422; se evitó el `AttributeError` que producía HTTP 500.
- Estado: PASSED

### CP-CAT-19 — Campo desconocido en categoría

- Título: Campo desconocido en categoría
- Requisito/regla: Contrato estricto del payload / Endpoint: `POST /categories`
- Prioridad: Media
- Precondiciones: API disponible.
- Datos: Payload válido con `unexpected=true`.
- Pasos: Enviar `POST /categories` con un payload válido más el campo `unexpected` y revisar la respuesta.
- Resultado esperado: HTTP 422.
- Resultado obtenido: HTTP 422; el campo no permitido fue rechazado.
- Estado: PASSED

### CP-PROD-19 — Nombre de producto en blanco

- Título: Nombre de producto en blanco
- Requisito/regla: RN03 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe la categoría 1.
- Datos: Producto válido con `name="   "`.
- Pasos: Enviar `POST /products` con el nombre compuesto solo por espacios y `category_id=1`.
- Resultado esperado: HTTP 422.
- Resultado obtenido: HTTP 422; el nombre en blanco fue rechazado.
- Estado: PASSED

### CP-PROD-20 — Precio no finito

- Título: Precio no finito
- Requisito/regla: RN04 / Endpoint: `POST /products`
- Prioridad: Alta
- Precondiciones: Existe la categoría 1.
- Datos: Precio `NaN`, `Infinity` o `-Infinity`.
- Pasos: Enviar `POST /products` una vez por cada valor de precio, con los demás campos válidos.
- Resultado esperado: HTTP 422; no almacenar valores no finitos.
- Resultado obtenido: HTTP 422 en los tres casos.
- Estado: PASSED

### CP-PROD-21 — Campo desconocido en producto

- Título: Campo desconocido en producto
- Requisito/regla: Contrato estricto del payload / Endpoint: `POST /products`
- Prioridad: Media
- Precondiciones: Existe la categoría 1.
- Datos: Payload válido con `unexpected=true`.
- Pasos: Enviar `POST /products` con un payload válido más el campo `unexpected` y revisar la respuesta.
- Resultado esperado: HTTP 422.
- Resultado obtenido: HTTP 422; el campo no permitido fue rechazado.
- Estado: PASSED
