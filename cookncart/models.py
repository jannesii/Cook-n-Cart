# models.py

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Product:
    id: int
    name: str
    unit: str
    price_per_unit: float
    category: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Recipe:
    id: int
    name: str
    instructions: str
    tags: str
    created_at: datetime
    updated_at: datetime
    ingredients: List['RecipeIngredient']


@dataclass
class RecipeIngredient:
    id: Optional[int] = field(default=None)
    recipe_id: Optional[int] = field(default=None)
    product_id: int = field(default=0)
    quantity: float = field(default=1.0)
    unit: str = field(default="")  # New field for weight/unit (e.g., "ml", "g", etc.)
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)


@dataclass
class ShoppingList:
    id: int
    title: str
    total_sum: float
    purchased_count: int
    created_at: datetime
    updated_at: datetime
    items: List['ShoppingListItem']


@dataclass
class ShoppingListItem:
    id: int
    shopping_list_id: int
    product_id: int
    quantity: float
    is_purchased: bool
    created_at: datetime
    updated_at: datetime
