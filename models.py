# models.py

from dataclasses import dataclass
from typing import List
import sqlite3
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
    id: int
    recipe_id: int
    product_id: int
    quantity: float
    created_at: datetime
    updated_at: datetime


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
