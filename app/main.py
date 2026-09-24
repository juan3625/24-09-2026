from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Query
from app.database import products_db, categories_db
from app.schemas import ( Product, ProductCreate, ProductUpdate, Category, CategoryCreate, CategoryUpdate)


app = FastAPI(
    title="Product and Category API",
    description="API for managing products and categories",
    version="1.0.0"
)

@app.get("/",tags=["Productos"])
def read_root():
    return {"mensaje": "hi World api functional"}

@app.get("/products", response_model=list[Product],tags=["Productos"])
def get_products(category: str | None = None, active: bool | None = None, search: str | None = None):
    result = products_db
    
    if category is not None:
        result = [
            product
            for product in result
            if product["category"].lower() == category.lower()
        ]
        
    if active is not None:
        result = [
            product
            for product in result
            if product["active"] == active
        ]
        
    if search is not None:
        result = [
            product
            for product in result
            if search.lower() in product["name"].lower()
        ]
        
    return result

@app.get("/products/{product_id}", response_model=Product,tags=["Productos"])
def get_product_by_id(product_id: int):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_next_product_id() -> int:
    if not products_db:
        return 1
    return max(product["id"] for product in products_db) + 1

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED,tags=["Productos"])
def create_product(product: ProductCreate):
    new_product = { "id": get_next_product_id(), **product.model_dump() } 
    products_db.append(new_product)
    return new_product

@app.patch("/products/{product_id}", response_model=Product,tags=["Productos"])
def update_product(product_id: int, product_update: ProductUpdate):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        product[key] = value
    
    return product

@app.put("/products/{product_id}", response_model=Product,tags=["Productos"])
def replace_product(product_id: int, product: ProductCreate):
    index = next((i for i, p in enumerate(products_db) if p["id"] == product_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = {"id": product_id, **product.model_dump()}
    products_db[index] = updated_product
    return updated_product

@app.delete("/products/{product_id}", response_model=Product,tags=["Productos"])
def delete_product(product_id: int):
    global products_db
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    products_db.remove(product)
    return product


# --- Endpoints de Categorías ---
@app.get("/categories", response_model=List[Category],tags=["Categorías"])
def get_categories(active: Optional[bool] = None, search: Optional[str] = None):
    results = categories_db
    if active is not None:
        results = [c for c in results if c["active"] == active]
    if search is not None:
        results = [c for c in results if search.lower() in c["name"].lower()]
    return results

@app.get("/categories/{category_id}", response_model=Category,tags=["Categorías"])
def get_category(category_id: int):
    category = next((c for c in categories_db if c["id"] == category_id), None)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED,tags=["Categorías"])
def create_category(category: CategoryCreate):
    new_id = max([c["id"] for c in categories_db], default=0) + 1
    new_category = {
        "id": new_id,
        "name": category.name,
        "description": category.description,
        "active": category.active
    }
    categories_db.append(new_category)
    return new_category

@app.patch("/categories/{category_id}", response_model=Category,tags=["Categorías"])
def update_category(category_id: int, category: CategoryUpdate):
    index = next((i for i, c in enumerate(categories_db) if c["id"] == category_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    stored_data = categories_db[index]
    update_data = category.model_dump(exclude_unset=True)
    updated_category = {**stored_data, **update_data}
    categories_db[index] = updated_category
    return updated_category

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Categorías"])
def delete_category(category_id: int):
    index = next((i for i, c in enumerate(categories_db) if c["id"] == category_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    categories_db.pop(index)
    return None


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/example")
def example(category: str | None = None, limit: int | None = 10):
    return {"category": category, "limit": limit}