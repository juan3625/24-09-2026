from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.database import categories_db

# 1. Esquema base para los campos comunes del producto
class ProductBase(BaseModel):
    name: str = Field(..., min_length=4,max_length=80, example="Product Name")
    price: float = Field(..., gt=0, example=99.99)
    active: bool = Field(..., example=True)
    stock: int = Field(..., ge=0, example=10)
    category: str = Field(..., example="Product Category")

# 2. Esquema para CREAR (aquí SÍ validamos que la categoría exista en la BD)
class ProductCreate(ProductBase):
    @field_validator('category')
    @classmethod
    def validate_category_exists(cls, value: str) -> str:
        category_exists = any(cat["name"] == value for cat in categories_db)
        if not category_exists:
            raise ValueError(f"La categoría '{value}' no existe en el sistema.")
        return value

# 3. Esquema para RESPUESTAS / SALIDAS (No ejecuta el validador de existencia para evitar bloqueos al consultar datos existentes)
class Product(ProductBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        orm_mode = True

# 4. Esquema para ACTUALIZAR
class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=4,max_length=80, example="Product Name")
    price: float | None = Field(None, gt=0, example=99.99)
    active: bool | None = Field(None, example=True)
    stock: int | None = Field(None, ge=0, example=10)
    category: str | None = Field(None, example="Product Category")
   
    @field_validator('category')
    @classmethod
    def validate_category_exists(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if not value.strip():
                raise ValueError("La categoría no puede estar vacía")
            category_exists = any(cat["name"] == value for cat in categories_db)
            if not category_exists:
                raise ValueError(f"La categoría '{value}' no existe en el sistema.")
        return value 


# ESQUEMAS PARA CATEGORÍAS
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, description="Nombre de la categoría")
    description: Optional[str] = Field(None, max_length=200, description="Descripción opcional")
    active: bool = Field(True, description="Estado de la categoría")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=60)
    description: Optional[str] = Field(None, max_length=200)
    active: Optional[bool] = None

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True