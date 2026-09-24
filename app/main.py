from fastapi import FastAPI, HTTPException, Response, status

from app.database import categories_db, products_db
from app.schemas import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    Product,
    ProductCreate,
    ProductUpdate,
)

app = FastAPI(
    title="Products & Categories API",
    description="API REST para administrar productos y categorías de una tienda tecnológica",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Products & Categories API is running"}


# Categories

def get_next_category_id() -> int:
    return max((category["id"] for category in categories_db), default=0) + 1


def find_category(category_id: int) -> dict | None:
    return next((category for category in categories_db if category["id"] == category_id), None)


def category_name_exists(name: str, excluding_id: int | None = None) -> bool:
    normalized_name = name.casefold()
    return any(
        category["id"] != excluding_id and category["name"].casefold() == normalized_name
        for category in categories_db
    )


@app.get("/categories", response_model=list[Category])
def get_categories(active: bool | None = None, search: str | None = None):
    """Lista categorías y conserva los filtros existentes por estado y nombre."""
    result = categories_db
    if active is not None:
        result = [category for category in result if category["active"] == active]
    if search is not None:
        term = search.casefold()
        result = [category for category in result if term in category["name"].casefold()]
    return result


@app.get("/categories/{category_id}", response_model=Category)
def get_category_by_id(category_id: int):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    if category_name_exists(category.name):
        raise HTTPException(status_code=409, detail="Category name already exists")
    new_category = {"id": get_next_category_id(), **category.model_dump()}
    categories_db.append(new_category)
    return new_category


@app.patch("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category_update: CategoryUpdate):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = category_update.model_dump(exclude_unset=True)
    if "name" in update_data and category_name_exists(update_data["name"], excluding_id=category_id):
        raise HTTPException(status_code=409, detail="Category name already exists")
    category.update(update_data)
    return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    categories_db.remove(category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Products

def get_next_product_id() -> int:
    return max((product["id"] for product in products_db), default=0) + 1


def find_product(product_id: int) -> dict | None:
    return next((product for product in products_db if product["id"] == product_id), None)


def require_category(category_id: int) -> None:
    if find_category(category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    require_category(product.category_id)
    new_product = {"id": get_next_product_id(), **product.model_dump()}
    products_db.append(new_product)
    return new_product


@app.get("/products", response_model=list[Product])
def get_products():
    return products_db


@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    require_category(product_update.category_id)
    product.update(product_update.model_dump())
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db.remove(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
