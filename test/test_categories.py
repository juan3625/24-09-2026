from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import products_db, categories_db
from app.schemas import CategoryCreate

client = TestClient(app)

INITIAL_CATEGORIES = categories_db.copy()

@pytest.fixture(autouse=True)
def reset_categories_db():
    categories_db.clear()
    categories_db.extend(INITIAL_CATEGORIES)

# ==========================================
# 1. PRUEBAS DE INTEGRACIÓN (Prueban la comunicación entre las rutas HTTP, FastAPI, esquemas y la base de datos simulada)
# ==========================================

# Tipo: Integración | Naturaleza: Positiva (Consulta la ruta GET general esperando código 200 y una lista)
def test_list_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Tipo: Integración | Naturaleza: Positiva (Consulta un recurso existente por ID esperando código 200)
def test_get_existing_category():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# Tipo: Integración | Naturaleza: Negativa (Consulta un recurso que no existe esperando un error 404 controlado)
def test_get_non_existing_category():
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"

# Tipo: Integración | Naturaleza: Negativa (Envía un parámetro con formato inválido en la URL esperando un error de validación 422)
def test_invalid_category_id():
    response = client.get("/categories/abc")
    assert response.status_code == 422

# Tipo: Integración | Naturaleza: Positiva (Crea un registro exitosamente mediante POST esperando código 201)
def test_create_category_valid():
    new_cat = {"name": "Hogar", "description": "Artículos para el hogar", "active": True}
    response = client.post("/categories", json=new_cat)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Hogar"
    assert "id" in data

# Tipo: Integración | Naturaleza: Negativa (Intenta crear un registro con datos no válidos a través de la API esperando un rechazo 422)
def test_create_category_short_name():
    new_cat = {"name": "Hi", "description": "Muy corto"}
    response = client.post("/categories", json=new_cat)
    assert response.status_code == 422

# Tipo: Integración | Naturaleza: Negativa (Intenta crear un registro omitiendo un campo obligatorio esperando un rechazo 422)
def test_create_category_missing_name():
    new_cat = {"description": "Sin nombre"}
    response = client.post("/categories", json=new_cat)
    assert response.status_code == 422

# Tipo: Integración | Naturaleza: Positiva (Actualiza parcialmente un registro existente mediante PATCH esperando código 200)
def test_update_existing_category():
    update_data = {"name": "Computadores Actualizados"}
    response = client.patch("/categories/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Computadores Actualizados"

# Tipo: Integración | Naturaleza: Negativa (Intenta actualizar un recurso inexistente esperando un error 404)
def test_update_non_existing_category():
    response = client.patch("/categories/999", json={"name": "Nada"})
    assert response.status_code == 404

# Tipo: Integración | Naturaleza: Positiva (Elimina un registro existente mediante DELETE esperando una respuesta sin contenido 204)
def test_delete_existing_category():
    response = client.delete("/categories/1")
    assert response.status_code == 204

# Tipo: Integración | Naturaleza: Negativa (Intenta eliminar un recurso que no existe esperando un error 404)
def test_delete_non_existing_category():
    response = client.delete("/categories/999")
    assert response.status_code == 404

# Tipo: Integración | Naturaleza: Positiva (Usa parámetros de consulta para filtrar resultados y valida el comportamiento exitoso con código 200)
def test_filter_active_categories():
    response = client.get("/categories?active=true")
    assert response.status_code == 200
    data = response.json()
    assert all(c["active"] is True for c in data)

# Tipo: Integración | Naturaleza: Negativa y Frontera | Parametrizada (Valida múltiples escenarios de error por datos inválidos en la creación de categorías, esperando un código 422)
@pytest.mark.parametrize(
    "payload",
    [
        # Nombre menor al límite permitido (Frontera negativa)
        {"name": "Hi", "description": "Muy corto", "active": True},
        # Omisión de campo obligatorio (Negativa)
        {"description": "Sin nombre", "active": True},
    ]
)
def test_create_category_validation_parametrized(payload):
    response = client.post("/categories", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()

# Tipo: Integración | Naturaleza: Frontera | Parametrizada (Valida los 3 casos límite clave: inferior inválido, inferior válido y superior inválido)
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        # 1. Frontera inferior inválida (2 caracteres, por debajo del mínimo permitido)
        ({"name": "Ab", "description": "Frontera inferior inválida", "active": True}, 422),
        # 2. Frontera inferior válida (4 caracteres, límite mínimo exacto)
        ({"name": "Abcd", "description": "Frontera inferior válida", "active": True}, 201),
        # 3. Frontera superior inválida (90 caracteres, superando el límite máximo de 80)
        ({"name": "A" * 90, "description": "Frontera superior inválida", "active": True}, 422),
    ]
)
def test_category_boundary_cases(payload, expected_status):
    response = client.post("/categories", json=payload)
    assert response.status_code == expected_status
    if expected_status == 201:
        assert "id" in response.json()
    else:
        assert "detail" in response.json()