# controllers.py

from models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem
from database import DatabaseManager
from typing import List, Dict


class RecipeController:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        print(self.db.get_product_by_id(1))

    def add_recipe(self, name: str, instructions: str, tags: str, ingredients: List[dict]):
        recipe = Recipe(
            id=0,  # Tietokanta asettaa tämän automaattisesti
            name=name,
            instructions=instructions,
            tags=tags,
            created_at=None,
            updated_at=None,
            ingredients=[RecipeIngredient(**ing) for ing in ingredients]
        )
        return self.db.add_recipe(recipe)

    def update_recipe(self, recipe_id: int, name: str = None, instructions: str = None, ingredients: List[dict] = None):
        recipe = self.db.get_recipe_by_id(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")

        if name:
            recipe.name = name
        if instructions:
            recipe.instructions = instructions
        if ingredients:
            recipe.ingredients = [RecipeIngredient(
                **ing) for ing in ingredients]

        self.db.update_recipe(recipe_id, recipe)
        return recipe

    def get_all_recipes(self) -> Dict[int, Recipe]:
        return self.db.get_all_recipes()
    
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self.db.get_recipe_by_id(recipe_id)
    
    def get_all_tags(self) -> List[str]:
        return self.db.get_all_tags()

    def get_ingredients_by_recipe_id(self, recipe_id: int) -> List[RecipeIngredient]:
        return self.db.get_ingredients_by_recipe_id(recipe_id)


class ShoppingListController:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        
    def add_shopping_list(self, title: str, items: List[dict]):
        shopping_list = ShoppingList(
            id=0,  # Tietokanta asettaa tämän automaattisesti
            title=title,
            total_sum=0,
            purchased_count=0,
            created_at=None,
            updated_at=None,
            items=[ShoppingListItem(**item) for item in items]
        )
        return self.db.add_shopping_list(shopping_list)
    
    def update_shopping_list(self, shopping_list_id: int, title: str = None, items: List[dict] = None):
        shopping_list = self.db.get_shopping_list_by_id(shopping_list_id)
        if not shopping_list:
            raise ValueError("Shopping list not found")

        if title:
            shopping_list.title = title
        if items:
            shopping_list.items = [ShoppingListItem(
                **item) for item in items]

        self.db.update_shopping_list(shopping_list_id, shopping_list)
        return shopping_list

    def get_all_shopping_lists(self) -> Dict[int, ShoppingList]:
        return self.db.get_all_shopping_lists()
    
    def get_shopping_list_by_id(self, shopping_list_id: int) -> ShoppingList:
        return self.db.get_shopping_list_by_id(shopping_list_id)
    
    def get_items_by_shopping_list_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        return self.db.get_products_by_shoplist_id(shopping_list_id)


class ProductController:
    def __init__(self):
        self.db = DatabaseManager.get_instance()

        

    def add_product(self, name: str, unit: str, price_per_unit: float, category: str):
        product = Product(
            id=0,  # Tietokanta asettaa tämän automaattisesti
            name=name,
            unit=unit,
            price_per_unit=price_per_unit,
            category=category,
            created_at=None,
            updated_at=None
        )
        return self.db.add_product(product)
    
    def get_all_products(self) -> Dict[int, Product]:
        return self.db.get_all_products()
    
    def get_all_categories(self) -> List[str]:
        return self.db.get_all_categories()

    def update_product(self, product_id: int, name: str = None, description: str = None, price_per_unit: float = None, category: str = None):
        product = self.db.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        if name:
            product.name = name
        if description:
            product.description = description
        if price_per_unit:
            product.price_per_unit = price_per_unit
        if category:
            product.category = category

        self.db.update_product(product_id, product)
        return product

    def delete_product(self, product_id: int):
        self.db.delete_product(product_id)