# Matriz de trazabilidad

| ID | Descripción | Caso(s) relacionado(s) | Cobertura |
|---|---|---|---|
| RF01 | Crear categoría válida | CP-CAT-01 | Cubierto |
| RF02 | Listar categorías | CP-CAT-02 | Cubierto |
| RF03 | Consultar categoría existente | CP-CAT-03 | Cubierto |
| RF04 | Consultar categoría inexistente | CP-CAT-04 | Cubierto |
| RF05 | Crear producto válido asociado | CP-PROD-01 | Cubierto |
| RF06 | Listar productos | CP-PROD-02 | Cubierto |
| RF07 | Consultar producto existente | CP-PROD-03 | Cubierto |
| RF08 | Consultar producto inexistente | CP-PROD-04 | Cubierto |
| RF09 | Actualizar producto válido | CP-PROD-05 | Cubierto |
| RF10 | Actualizar producto inexistente | CP-PROD-06 | Cubierto |
| RF11 | Eliminar producto existente | CP-PROD-07 | Cubierto |
| RF12 | Eliminar producto inexistente | CP-PROD-08 | Cubierto |
| RN01 | Nombre de categoría obligatorio, 3–60 caracteres | CP-CAT-05, CP-CAT-06 | Cubierto |
| RN02 | Nombre de categoría único sin distinguir mayúsculas | CP-CAT-07 | Cubierto |
| RN03 | Nombre de producto obligatorio, 3–80 caracteres | CP-PROD-09, CP-PROD-10 | Cubierto |
| RN04 | Precio estrictamente mayor que 0 | CP-PROD-11, CP-PROD-12, CP-PROD-13 | Cubierto |
| RN05 | Stock mayor o igual que 0 | CP-PROD-14, CP-PROD-15 | Cubierto |
| RN06 | `category_id` existente | CP-PROD-16, CP-PROD-18 | Cubierto |
| RN07 | Stock igual a 0 aceptado | CP-PROD-14 | Cubierto |
| RN08 | Actualización conserva validaciones | CP-PROD-17, CP-PROD-18 | Cubierto |

## Relación con automatización

Los tests activos de `test/test_categories.py` y `test/test_products.py` se identifican mediante comentarios `CP-CAT-XX` y `CP-PROD-XX`, respectivamente, y cubren los casos documentados.

## Cobertura adicional de Categorías

| ID de caso | Escenario | Endpoint | Tipo | Estado |
|---|---|---|---|---|
| CP-CAT-06 | Nombre exactamente de 3 caracteres | `POST /categories` | Frontera positiva / RN01 | Cubierto |
| CP-CAT-08 | ID de categoría con formato inválido | `GET /categories/{id}` | Negativa de validación | Cubierto |
| CP-CAT-09 | Nombre ausente | `POST /categories` | Negativa / RN01 | Cubierto |
| CP-CAT-10 | Descripción demasiado larga | `POST /categories` | Negativa de validación | Cubierto |
| CP-CAT-16 | Actualizar categoría existente | `PATCH /categories/{id}` | Positiva adicional | Cubierto |
| CP-CAT-11 | Actualizar categoría inexistente | `PATCH /categories/{id}` | Negativa adicional | Cubierto |
| CP-CAT-12 | Eliminar categoría existente | `DELETE /categories/{id}` | Positiva adicional | Cubierto |
| CP-CAT-13 | Eliminar categoría inexistente | `DELETE /categories/{id}` | Negativa adicional | Cubierto |
| CP-CAT-14 | Filtrar categorías activas | `GET /categories?active=true` | Positiva adicional | Cubierto |
| CP-CAT-15 | Buscar categorías por nombre | `GET /categories?search=comp` | Positiva adicional | Cubierto |

Estas pruebas amplían el mínimo del contrato evaluable y documentan funcionalidades que ya existían en el proyecto original. No sustituyen la cobertura obligatoria de RF01–RF12 y RN01–RN08.


## Regresiones de validación

| ID | Descripción | Caso(s) relacionado(s) | Cobertura |
|---|---|---|---|
| RN01 | Nombres de categoría no vacíos y con espacios normalizados | CP-CAT-17 | Cubierto |
| Validación de payload | Nombre nulo rechazado en PATCH sin error interno | CP-CAT-18 | Cubierto |
| Contrato de payload | Campos desconocidos rechazados en categorías y productos | CP-CAT-19, CP-PROD-21 | Cubierto |
| RN03 | Nombres de producto no vacíos | CP-PROD-19 | Cubierto |
| RN04 | Precio finito y estrictamente mayor que 0 | CP-PROD-20 | Cubierto |
