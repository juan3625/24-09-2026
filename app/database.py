categories_db: list[dict] = [
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

products_db: list[dict] = [
    {
        "id": 1,
        "name": "Mouse inalámbrico",
        "price": 120000,
        "stock": 5,
        "category_id": 2,
    },
    {
        "id": 2,
        "name": "Monitor",
        "price": 850000,
        "stock": 0,
        "category_id": 1,
    },
]
