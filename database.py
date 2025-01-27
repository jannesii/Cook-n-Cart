# database.py

import sqlite3
from models import Recipe, Product, RecipeIngredient, ShoppingList, ShoppingListItem
from typing import List, Dict
import os


class DatabaseManager:
    _instance = None

    def __init__(self, db_path=os.path.join(os.getcwd(), "utils", "cook_and_cart.db")):
        if DatabaseManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            DatabaseManager._instance = self

    @staticmethod
    def get_instance():
        if DatabaseManager._instance is None:
            DatabaseManager()
        return DatabaseManager._instance

    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetchall(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetchone(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()

    # Lisää metodit CRUD-toiminnoille

    def add_recipe(self, recipe: Recipe):
        query = """
        INSERT INTO recipes (name, instructions, tags)
        VALUES (?, ?, ?)
        """
        cursor = self.execute_query(
            query, (recipe.name, recipe.instructions, recipe.tags))
        recipe_id = cursor.lastrowid
        # Lisää ainesosat
        for ingredient in recipe.ingredients:
            self.add_recipe_ingredient(recipe_id, ingredient)
        return recipe_id

    def add_recipe_ingredient(self, recipe_id: int, ingredient: RecipeIngredient):
        query = """
        INSERT INTO recipe_ingredients (recipe_id, product_id, quantity)
        VALUES (?, ?, ?)
        """
        self.execute_query(
            query, (recipe_id, ingredient.product_id, ingredient.quantity))

    def add_product(self, product: Product):
        query = """
        INSERT INTO products (name, unit, price_per_unit, category)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (product.name, product.unit,
                           product.price_per_unit, product.category))

    def add_shopping_list(self, shoppinglist: ShoppingList):
        query = """
        INSERT INTO shopping_lists (title, total_sum, purchased_count)
        VALUES (?, ?, ?)
        """
        cursor = self.execute_query(
            query, (shoppinglist.title, shoppinglist.total_sum, shoppinglist.purchased_count))
        list_id = cursor.lastrowid
        for items in shoppinglist.items:
            self.add_shopping_list_items(list_id, items)
        return list_id

    def add_shopping_list_items(self, shoppingList_id: int, shoppingListitems: ShoppingListItem):
        query = """
        INSERT INTO shopping_list_items (shopping_list_id, product_id, quantity, is_purchased)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (shoppingList_id, shoppingListitems.product_id,
                           shoppingListitems.quantity, shoppingListitems.is_purchased))

    """---------------------------------------------------------------------------------------------------------------------
        GET METHODS
    ---------------------------------------------------------------------------------------------------------------------"""

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        query = "SELECT * FROM recipes WHERE id = ?"
        row = self.fetchone(query, (recipe_id,))
        if row:
            recipe = Recipe(
                id=row['id'],
                name=row['name'],
                instructions=row['instructions'],
                tags=row['tags'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                ingredients=self.get_ingredients_by_recipe_id(recipe_id)
            )
            return recipe
        return None

    def get_ingredients_by_recipe_id(self, recipe_id: int) -> List[RecipeIngredient]:
        query = "SELECT * FROM recipe_ingredients WHERE recipe_id = ?"
        rows = self.fetchall(query, (recipe_id,))
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

    def get_all_tags(self) -> List[str]:
        query = "SELECT tags FROM recipes"
        rows = self.fetchall(query)
        tags = []
        for row in rows:
            tags.append(row['tags'])
        return tags

    def get_all_categories(self) -> List[str]:
        query = "SELECT category FROM products"
        rows = self.fetchall(query)
        categories = []
        for row in rows:
            categories.append(row['category'])
        return categories

    def get_all_recipes(self) -> Dict[int, Recipe]:
        query = "SELECT * FROM recipes"
        rows = self.fetchall(query)
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
        recipes_dict: Dict[int, Recipe] = {
            recipe.id: recipe for recipe in recipes}
        return recipes_dict

    def get_all_products(self) -> Dict[int, Product]:
        query = "SELECT * FROM products"
        rows = self.fetchall(query)
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

        products_dict: Dict[int, Product] = {
            product.id: product for product in products}
        return products_dict

    def get_product_by_id(self, product_id: int) -> Product:
        query = "SELECT * FROM products WHERE id = ?"
        row = self.fetchone(query, (product_id,))
        if row:
            product = Product(
                id=row['id'],
                name=row['name'],
                unit=row['unit'],
                price_per_unit=row['price_per_unit'],
                category=row['category'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            return product
        return None

    def get_products_by_shoplist_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        query = "SELECT * FROM shopping_list_items WHERE shopping_list_id = ?"
        rows = self.fetchall(query, (shopping_list_id,))
        items = []
        for row in rows:
            item = ShoppingListItem(
                id=row['id'],
                shopping_list_id=row['shopping_list_id'],
                product_id=row['product_id'],
                quantity=row['quantity'],
                is_purchased=row['is_purchased'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            items.append(item)
        return items

    def get_all_shopping_lists(self) -> Dict[int, ShoppingList]:
        query = "SELECT * FROM shopping_lists"
        rows = self.fetchall(query)
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
        shopping_lists_dict: Dict[int, ShoppingList] = {
            shopping_list.id: shopping_list for shopping_list in shopping_lists}
        return shopping_lists_dict

    def get_shopping_list_by_id(self, shopping_list_id: int) -> ShoppingList:
        query = "SELECT * FROM shopping_lists WHERE id = ?"
        row = self.fetchone(query, (shopping_list_id,))
        if row:
            shopping_list = ShoppingList(
                id=row['id'],
                title=row['title'],
                total_sum=row['total_sum'],
                purchased_count=row['purchased_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                items=self.get_products_by_shoplist_id(row['id'])
            )
            return shopping_list
        return None

    """---------------------------------------------------------------------------------------------------------------------
        UPDATE METHODS
    ---------------------------------------------------------------------------------------------------------------------"""

    def update_recipe(self, recipe_id: int, recipe: Recipe):
        query = """
        UPDATE recipes
        SET name = ?, instructions = ?, image_url = ?
        WHERE id = ?
        """
        self.execute_query(
            query, (recipe.name, recipe.instructions, recipe.image_url, recipe_id))
        # Update ingredients
        self.execute_query(
            "DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))
        for ingredient in recipe.ingredients:
            self.add_recipe_ingredient(recipe_id, ingredient)

    def update_product(self, product_id: int, product: Product):
        query = """
        UPDATE products
        SET name = ?, unit = ?, price_per_unit = ?, category = ?
        WHERE id = ?
        """
        self.execute_query(query, (product.name, product.unit,
                           product.price_per_unit, product.category, product_id))

    def update_shopping_list(self, shopping_list_id: int, shopping_list: ShoppingList):
        query = """
        UPDATE shopping_lists
        SET title = ?, total_sum = ?, purchased_count = ?
        WHERE id = ?
        """
        self.execute_query(query, (shopping_list.title, shopping_list.total_sum,
                           shopping_list.purchased_count, shopping_list_id))
        self.execute_query(
            "DELETE FROM shopping_list_items WHERE shopping_list_id = ?", (shopping_list_id,))
        for items in shopping_list.items:
            self.add_shopping_list_items(shopping_list_id, items)

    def delete_product(self, product_id: int):
        query = "DELETE FROM products WHERE id = ?"
        self.execute_query(query, (product_id,))
