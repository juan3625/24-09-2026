from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.database import categories_db, products_db
from app.main import app

client = TestClient(app)

INITIAL_CATEGORIES = deepcopy(categories_db)
INITIAL_PRODUCTS = deepcopy(products_db)


@pytest.fixture(autouse=True)
def reset_databases():
    categories_db.clear()
    categories_db.extend(deepcopy(INITIAL_CATEGORIES))
    products_db.clear()
    products_db.extend(deepcopy(INITIAL_PRODUCTS))


def valid_product(**overrides):
    payload = {
        "name": "Teclado mecánico",
        "price": 250000,
        "stock": 10,
        "category_id": 1,
    }
    payload.update(overrides)
    return payload


# CP-PROD-01 / RF05
@pytest.mark.positive
def test_cp_prod_01_create_valid_product():
    response = client.post("/products", json=valid_product())
    assert response.status_code == 201
    assert response.json()["name"] == "Teclado mecánico"


# CP-PROD-02 / RF06
@pytest.mark.positive
def test_cp_prod_02_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) >= 1


# CP-PROD-03 / RF07
@pytest.mark.positive
def test_cp_prod_03_get_existing_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


# CP-PROD-04 / RF08
@pytest.mark.negative
def test_cp_prod_04_get_unknown_product_returns_404():
    response = client.get("/products/99999")
    assert response.status_code == 404


# CP-PROD-05 / RF09
@pytest.mark.positive
def test_cp_prod_05_update_existing_product():
    response = client.put("/products/1", json=valid_product(name="Mouse actualizado"))
    assert response.status_code == 200
    assert response.json()["name"] == "Mouse actualizado"


# CP-PROD-06 / RF10
@pytest.mark.negative
def test_cp_prod_06_update_unknown_product_returns_404():
    response = client.put("/products/99999", json=valid_product())
    assert response.status_code == 404


# CP-PROD-07 / RF11
@pytest.mark.positive
def test_cp_prod_07_delete_existing_product():
    response = client.delete("/products/1")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/products/1").status_code == 404


# CP-PROD-08 / RF12
@pytest.mark.negative
def test_cp_prod_08_delete_unknown_product_returns_404():
    response = client.delete("/products/99999")
    assert response.status_code == 404


# CP-PROD-09 / RN03
@pytest.mark.boundary
def test_cp_prod_09_name_shorter_than_three_characters_is_rejected():
    response = client.post("/products", json=valid_product(name="AB"))
    assert response.status_code == 422


# CP-PROD-10 / RN03
@pytest.mark.boundary
def test_cp_prod_10_name_of_exactly_three_characters_is_accepted():
    response = client.post("/products", json=valid_product(name="TVX"))
    assert response.status_code == 201


# CP-PROD-11 / RN04
@pytest.mark.boundary
def test_cp_prod_11_zero_price_is_rejected():
    response = client.post("/products", json=valid_product(price=0))
    assert response.status_code == 422


# CP-PROD-12 / RN04
@pytest.mark.negative
def test_cp_prod_12_negative_price_is_rejected():
    response = client.post("/products", json=valid_product(price=-1000))
    assert response.status_code == 422


# CP-PROD-13 / RN04
@pytest.mark.boundary
def test_cp_prod_13_minimum_positive_price_is_accepted():
    response = client.post("/products", json=valid_product(price=0.01))
    assert response.status_code == 201


# CP-PROD-14 / RN05/RN07
@pytest.mark.boundary
def test_cp_prod_14_zero_stock_is_accepted():
    response = client.post("/products", json=valid_product(stock=0))
    assert response.status_code == 201


# CP-PROD-15 / RN05
@pytest.mark.boundary
def test_cp_prod_15_negative_stock_is_rejected():
    response = client.post("/products", json=valid_product(stock=-1))
    assert response.status_code == 422


# CP-PROD-16 / RN06
@pytest.mark.negative
def test_cp_prod_16_unknown_category_is_rejected():
    response = client.post("/products", json=valid_product(category_id=99999))
    assert response.status_code == 404


# CP-PROD-17 / RN08
@pytest.mark.boundary
def test_cp_prod_17_invalid_price_on_update_is_rejected():
    response = client.put("/products/1", json=valid_product(price=0))
    assert response.status_code == 422


# CP-PROD-18 / RN06/RN08
@pytest.mark.negative
def test_cp_prod_18_unknown_category_on_update_is_rejected():
    response = client.put("/products/1", json=valid_product(category_id=99999))
    assert response.status_code == 404


# CP-PROD-19 / RN03
# Regresión: los nombres compuestos solo por espacios deben rechazarse.
@pytest.mark.negative
def test_product_blank_name_is_rejected():
    response = client.post("/products", json=valid_product(name="   "))
    assert response.status_code == 422


# CP-PROD-20 / RN04
# Regresión: NaN e Infinity no son precios válidos para una API monetaria.
@pytest.mark.negative
def test_product_non_finite_price_is_rejected():
    for invalid_price in ("NaN", "Infinity", "-Infinity"):
        response = client.post("/products", json=valid_product(price=invalid_price))
        assert response.status_code == 422


# CP-PROD-21 / Contrato estricto del payload
# Regresión: los campos fuera del contrato deben rechazarse explícitamente.
@pytest.mark.negative
def test_product_unknown_field_is_rejected():
    response = client.post(
        "/products", json={**valid_product(), "unexpected": True}
    )
    assert response.status_code == 422


# CP-PROD-22 / RN03 (frontera superior)
# Frontera positiva: exactamente 80 caracteres (max_length) debe aceptarse.
@pytest.mark.boundary
def test_cp_prod_22_name_exactly_eighty_characters_is_accepted():
    response = client.post("/products", json=valid_product(name="A" * 80))
    assert response.status_code == 201


# CP-PROD-23 / RN03 (frontera superior)
# Frontera negativa: 81 caracteres supera el max_length y debe rechazarse.
@pytest.mark.boundary
def test_cp_prod_23_name_eighty_one_characters_is_rejected():
    response = client.post("/products", json=valid_product(name="A" * 81))
    assert response.status_code == 422