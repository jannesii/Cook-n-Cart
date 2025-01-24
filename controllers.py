# controllers.py

from models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem
from database import DatabaseManager
from typing import List, Dict

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
                tags=row['tags'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                ingredients=self.get_ingredients_by_recipe_id(row['id'])
            )
            recipes.append(recipe)
        return recipes
    
    def get_all_recipes_as_dict(self) -> Dict[int, Recipe]:
        recipes = self.get_all_recipes()
        recipes_dict: Dict[int, Recipe] = {recipe.id: recipe for recipe in recipes}
        return recipes_dict

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

class ShoppingListController:
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        
    def get_all_shopping_lists(self) -> List[ShoppingList]:
        query = "SELECT * FROM shopping_lists"
        rows = self.db.fetchall(query)
        shopping_lists = []
        for row in rows:
            shopping_list = ShoppingList(
                id=row['id'],
                title=row['title'],
                total_sum=row['total_sum'],
                purchased_count=row['purchased_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )
            shopping_lists.append(shopping_list)
        return shopping_lists
    
    def get_all_shopping_lists_as_dict(self) -> List[Dict]:
        shopping_lists = self.get_all_shopping_lists()
        shopping_lists_dict: Dict[int, ShoppingList] = {shopping_list.id: shopping_list for shopping_list in shopping_lists}
        return shopping_lists_dict
        
        
    
class ProductController:
        def __init__(self):
            self.db = DatabaseManager.get_instance()

        def get_all_products(self) -> List[Product]:
            query = "SELECT * FROM products"
            rows = self.db.fetchall(query)
            products = []
            for row in rows:
                product = Product(
                    id=row['id'],
                    name=row['name'],
                    unit=row['unit'],
                    price_per_unit=row['price_per_unit'],
                    category=row['category'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                products.append(product)
            return products
        
        def get_all_products_as_dict(self):
            tuotteet = self.get_all_products()
            # Create a dictionary with id as the key
            products_dict: Dict[int, Product] = {product.id: product for product in tuotteet}
            return products_dict

        def create_product(self, name: str, description: str, price: float):
            product = Product(
                id=0,  # Tietokanta asettaa tämän automaattisesti
                name=name,
                description=description,
                price=price,
                created_at=None,
                updated_at=None
            )
            return self.db.add_product(product)

        def modify_product(self, product_id: int, name: str, description: str, price: float):
            query = """
            UPDATE products
            SET name = ?, description = ?, price = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """
            self.db.execute(query, (name, description, price, product_id))

        def delete_product(self, product_id: int):
            query = "DELETE FROM products WHERE id = ?"
            self.db.execute(query, (product_id,))