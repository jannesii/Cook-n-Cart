# database.py

import sqlite3
from models import Recipe, Product, RecipeIngredient, ShoppingList, ShoppingListItem
from typing import List

class DatabaseManager:
    _instance = None

    def __init__(self, db_path='recipes.db'):
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
        INSERT INTO recipes (name, instructions, image_url)
        VALUES (?, ?, ?)
        """
        cursor = self.execute_query(query, (recipe.name, recipe.instructions, recipe.image_url))
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
        self.execute_query(query, (recipe_id, ingredient.product_id, ingredient.quantity))

    # Lisää muita CRUD-metodeja tarpeen mukaan
