# controllers.py

from models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem
from database import DatabaseManager
from typing import List

class RecipeController:
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    def create_recipe(self, name: str, instructions: str, image_url: str, ingredients: List[dict]):
        recipe = Recipe(
            id=0,  # Tietokanta asettaa tämän automaattisesti
            name=name,
            instructions=instructions,
            image_url=image_url,
            created_at=None,
            updated_at=None,
            ingredients=[RecipeIngredient(**ing) for ing in ingredients]
        )
        return self.db.add_recipe(recipe)

    def get_all_recipes(self) -> List[Recipe]:
        query = "SELECT * FROM recipes"
        rows = self.db.fetchall(query)
        recipes = []
        for row in rows:
            recipe = Recipe(
                id=row['id'],
                name=row['name'],
                instructions=row['instructions'],
                image_url=row['image_url'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                ingredients=self.get_ingredients_by_recipe_id(row['id'])
            )
            recipes.append(recipe)
        return recipes

    def get_ingredients_by_recipe_id(self, recipe_id: int) -> List[RecipeIngredient]:
        query = "SELECT * FROM recipe_ingredients WHERE recipe_id = ?"
        rows = self.db.fetchall(query, (recipe_id,))
        ingredients = []
        for row in rows:
            ingredient = RecipeIngredient(
                id=row['id'],
                recipe_id=row['recipe_id'],
                product_id=row['product_id'],
                quantity=row['quantity'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            ingredients.append(ingredient)
        return ingredients

    # Lisää muita metodit, kuten päivitys ja poisto
