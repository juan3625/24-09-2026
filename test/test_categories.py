from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.database import categories_db
from app.main import app

client = TestClient(app)

INITIAL_CATEGORIES = [
    {
        "id": 1,
        "name": "Computadores",
        "description": "Equipos de cómputo",
        "active": True,
    },
    {
        "id": 2,
        "name": "Accesorios",
        "description": "Periféricos y accesorios tecnológicos",
        "active": True,
    },
    {
        "id": 3,
        "name": "Cámaras",
        "description": "Cámaras digitales y de seguridad",
        "active": False,
    },
]


@pytest.fixture(autouse=True)
def reset_categories_db():
    categories_db.clear()
    categories_db.extend(deepcopy(INITIAL_CATEGORIES))


# CP-CAT-02 / RF02
@pytest.mark.positive
def test_list_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


# CP-CAT-03 / RF03
@pytest.mark.positive
def test_get_existing_category():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Computadores"


# CP-CAT-04 / RF04
@pytest.mark.negative
def test_get_non_existing_category():
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# CP-CAT-08 / Validación de path parameter
# Este caso adicional verifica el comportamiento de entrada inválida.
@pytest.mark.negative
def test_invalid_category_id():
    response = client.get("/categories/abc")
    assert response.status_code == 422


# CP-CAT-01 / RF01
@pytest.mark.positive
def test_create_valid_category():
    payload = {"name": "Monitores", "description": "Pantallas para computadores"}
    response = client.post("/categories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["name"] == "Monitores"
    assert data["active"] is True


# CP-CAT-05 / RN01
@pytest.mark.boundary
def test_category_name_too_short():
    response = client.post("/categories", json={"name": "AB"})
    assert response.status_code == 422


# CP-CAT-06 / RN01
@pytest.mark.boundary
def test_category_name_exactly_three_characters_is_accepted():
    response = client.post("/categories", json={"name": "Red"})
    assert response.status_code == 201


# CP-CAT-09 / RN01
# Caso adicional para la obligatoriedad del nombre.
@pytest.mark.negative
def test_category_name_is_required():
    response = client.post("/categories", json={"description": "Sin nombre"})
    assert response.status_code == 422


# CP-CAT-07 / RN02
@pytest.mark.negative
def test_category_duplicate_is_case_insensitive():
    response = client.post("/categories", json={"name": "computadores"})
    assert response.status_code == 409


# CP-CAT-10 / Validación de descripción
# Caso adicional para el límite máximo de description.
@pytest.mark.boundary
def test_description_too_long():
    response = client.post("/categories", json={"name": "Monitores", "description": "x" * 201})
    assert response.status_code == 422


# CP-CAT-16 / Funcionalidad existente de PATCH
# Este endpoint adicional se conserva del proyecto original.
@pytest.mark.positive
def test_update_existing_category():
    response = client.patch("/categories/1", json={"name": "Computadores portátiles"})
    assert response.status_code == 200
    assert response.json()["name"] == "Computadores portátiles"
    assert response.json()["active"] is True


# CP-CAT-11 / Recurso inexistente en PATCH
# Caso adicional para la funcionalidad existente de actualización parcial.
@pytest.mark.negative
def test_update_non_existing_category():
    response = client.patch("/categories/999", json={"name": "Monitores"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# CP-CAT-12 / Funcionalidad existente de DELETE
# Este endpoint adicional se conserva del proyecto original.
@pytest.mark.positive
def test_delete_existing_category():
    response = client.delete("/categories/1")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/categories/1").status_code == 404


# CP-CAT-13 / Recurso inexistente en DELETE
# Caso adicional para la funcionalidad existente de eliminación.
@pytest.mark.negative
def test_delete_non_existing_category():
    response = client.delete("/categories/999")
    assert response.status_code == 404


# CP-CAT-14 / Filtrado adicional de Categorías
# Este endpoint adicional se conserva del proyecto original.
@pytest.mark.positive
def test_filter_active_categories():
    response = client.get("/categories", params={"active": "true"})
    assert response.status_code == 200
    assert response.json()
    assert all(category["active"] is True for category in response.json())


# CP-CAT-15 / Búsqueda adicional de Categorías
# Este endpoint adicional se conserva del proyecto original.
@pytest.mark.positive
def test_search_categories_by_name():
    response = client.get("/categories", params={"search": "comp"})
    assert response.status_code == 200
    assert [category["name"] for category in response.json()] == ["Computadores"]


# CP-CAT-18 / Validación de payload
# Regresión: un nombre nulo explícito no debe provocar un error interno.
@pytest.mark.negative
def test_update_category_with_null_name_is_rejected():
    response = client.patch("/categories/1", json={"name": None})
    assert response.status_code == 422


# CP-CAT-17 / RN01
# Regresión: los nombres en blanco no son nombres válidos.
@pytest.mark.negative
def test_category_blank_name_is_rejected():
    response = client.post("/categories", json={"name": "   "})
    assert response.status_code == 422


# CP-CAT-19 / Contrato estricto del payload
# Regresión: los campos fuera del contrato deben rechazarse explícitamente.
@pytest.mark.negative
def test_category_unknown_field_is_rejected():
    response = client.post(
        "/categories", json={"name": "Nueva", "unexpected": True}
    )
    assert response.status_code == 422


# CP-CAT-20 / RN01 (frontera superior)
# Frontera positiva: exactamente 60 caracteres (max_length) debe aceptarse.
@pytest.mark.boundary
def test_category_name_exactly_sixty_characters_is_accepted():
    response = client.post("/categories", json={"name": "A" * 60})
    assert response.status_code == 201


# CP-CAT-21 / RN01 (frontera superior)
# Frontera negativa: 61 caracteres supera el max_length y debe rechazarse.
@pytest.mark.boundary
def test_category_name_sixty_one_characters_is_rejected():
    response = client.post("/categories", json={"name": "A" * 61})
    assert response.status_code == 422


# CP-CAT-22 / Validación de descripción (frontera superior)
# Frontera positiva: exactamente 200 caracteres (max_length) debe aceptarse.
@pytest.mark.boundary
def test_description_exactly_two_hundred_characters_is_accepted():
    response = client.post(
        "/categories", json={"name": "Monitores", "description": "x" * 200}
    )
    assert response.status_code == 201