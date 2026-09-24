from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import products_db

client = TestClient(app)

INITIAL_PRODUCTS = products_db.copy()

@pytest.fixture(autouse=True)
def reset_products_db():
    products_db.clear()
    products_db.extend(INITIAL_PRODUCTS)

# Tipo: Integración | Naturaleza: Positiva (Prueba el estado de salud de la API esperando un código 200)
def test_health():
    endpoint = "/health"
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    
# Tipo: Integración | Naturaleza: Positiva (Consulta la lista completa de productos esperando código 200)
def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
# Tipo: Integración | Naturaleza: Positiva (Consulta un producto existente por ID esperando código 200)
def test_get_existing_products():
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    
# Tipo: Integración | Naturaleza: Negativa (Consulta un producto que no existe esperando un error 404)
def test_get_non_existing_product():
    response = client.get("/products/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"
    
# Tipo: Integración | Naturaleza: Negativa (Envía un ID inválido con letras esperando un error de validación 422)
def test_invalid_product_id():
    response = client.get("/products/abc")
    assert response.status_code == 422
    assert "detail" in response.json()
    
# Tipo: Integración | Naturaleza: Positiva (Filtra los productos activos mediante parámetros de consulta esperando código 200)
def test_filter_active_products():
    response = client.get("/products?active=true")
    assert response.status_code == 200
    data = response.json()
    assert all(product["active"] is True for product in data)
  
# Tipo: Integración | Naturaleza: Positiva (Filtra los productos por categoría específica esperando código 200)
def test_filter_products_by_category():
    response = client.get("/products?category=Accesorios")
    assert response.status_code == 200
    data = response.json()
    assert all(product["category"] == "Accesorios" for product in data)

# Tipo: Integración | Naturaleza: Positiva (Crea un nuevo producto exitosamente enviando datos correctos esperando un código 201)
def test_create_product():
    new_product = {
        "name": "New Product",
        "category": "Accesorios",
        "price": 100.0,
        "stock": 10,
        "active": True
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_product["name"]
    assert data["category"] == new_product["category"]
    assert data["active"] == new_product["active"]
    assert data["price"] == new_product["price"]
    assert data["stock"] == new_product["stock"]
    
# Tipo: Integración | Naturaleza: Negativa (Intenta crear un producto con un precio negativo esperando que la API lo rechace con un código 422)
def test_create_product_negative_price():
    new_product = {
        "name": "New Product",
        "category": "Accesorios",
        "price": -10,
        "stock": 5,
        "active": True
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any(
        error["loc"][-1] == "price" 
        for error in data["detail"]
    )
    
# Tipo: Integración | Naturaleza: Positiva (Actualiza completamente un producto existente mediante PUT esperando código 200)
def test_update_product():
    updated_product = {
        "name": "Updated Product",
        "category": "Accesorios",
        "price": 50.0,
        "stock": 10,
        "active": False
    }
    response = client.put("/products/1", json=updated_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_product["name"]
    assert data["category"] == updated_product["category"]
    assert data["active"] == updated_product["active"]
    assert data["price"] == updated_product["price"]
    assert data["stock"] == updated_product["stock"]
    
# Tipo: Integración | Naturaleza: Positiva (Actualiza parcialmente el precio de un producto mediante PATCH esperando código 200)
def test_update_price_patch():
    updated_price = {
        "price": 75.0
    }
    response = client.patch("/products/1", json=updated_price)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == updated_price["price"]
    
# Tipo: Integración | Naturaleza: Negativa (Intenta actualizar un producto que no existe esperando un error 404)
def test_update_non_existing_product():
    updated_product = {
        "name": "Updated Product",
        "category": "Accesorios",
        "price": 50.0,
        "stock": 10,
        "active": False
    }
    response = client.put("/products/999", json=updated_product)
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Product not found"
    
# Tipo: Integración | Naturaleza: Positiva (Elimina un producto existente mediante DELETE esperando un código 200)
def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

# Tipo: Integración | Naturaleza: Negativa y Frontera | Parametrizada (Valida múltiples escenarios de error por datos inválidos en la creación de productos, esperando un código 422)
@pytest.mark.parametrize(
    "payload",
    [
        # Nombre menor a 3 caracteres (Frontera negativa)
        {"name": "Ab", "category": "Accesorios", "price": 50.0, "stock": 10, "active": True},
        # Precio menor o igual a cero (Negativa / Frontera)
        {"name": "Producto", "category": "Accesorios", "price": 0.0, "stock": 10, "active": True},
        # Stock negativo (Negativa)
        {"name": "Producto", "category": "Accesorios", "price": 50.0, "stock": -3, "active": True},
    ]
)
def test_create_product_validation_parametrized(payload):
    response = client.post("/products", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()