from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class APIModel(BaseModel):
    """Configuración común para rechazar payloads ambiguos o mal formados."""

    model_config = ConfigDict(extra="forbid")


def _clean_required_text(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("must not be blank")
    return cleaned


class CategoryCreate(APIModel):
    """Datos permitidos al crear una categoría."""

    name: str = Field(..., min_length=3, max_length=60, examples=["Periféricos"])
    description: str | None = Field(default=None, max_length=200)
    active: bool = Field(default=True)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return _clean_required_text(value)


class CategoryUpdate(APIModel):
    """Campos opcionales para una actualización parcial de categoría."""

    name: str | None = Field(default=None, min_length=3, max_length=60)
    description: str | None = Field(default=None, max_length=200)
    active: bool | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("name must not be null when provided")
        return _clean_required_text(value)


class Category(CategoryCreate):
    """Representación completa de una categoría."""

    id: int

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ProductCreate(APIModel):
    """Payload de creación y actualización completa de un producto."""

    name: str = Field(..., min_length=3, max_length=80, examples=["Teclado mecánico"])
    price: float = Field(..., gt=0, allow_inf_nan=False, examples=[250000])
    stock: int = Field(..., ge=0, examples=[10])
    category_id: int = Field(..., examples=[1])

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return _clean_required_text(value)


class ProductUpdate(ProductCreate):
    """PUT conserva las mismas validaciones que la creación."""

    pass


class Product(ProductCreate):
    """Representación completa de un producto."""

    id: int

    model_config = ConfigDict(from_attributes=True, extra="forbid")
