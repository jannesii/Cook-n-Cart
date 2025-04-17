# File: root_controllers.py --------------------------------------------------------------------

from typing import Dict, List
import json
import functools
import logging

from root_models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem, ErrorLog
from root_repositories import RecipeRepository, ProductRepository, ShoppingListRepository, ErrorRepository
from error_handler import catch_errors
from datetime import datetime

CONFIG_FILE = "utils/config.json"


class RecipeController:
    def __init__(self):
        self.repo = RecipeRepository()

    @catch_errors
    def get_all_recipes(self) -> Dict[int, Recipe]:
        return self.repo.get_all_recipes()

    @catch_errors
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self.repo.get_recipe_by_id(recipe_id)

    @catch_errors
    def get_all_tags(self) -> List[str]:
        return self.repo.get_all_tags()

    @catch_errors
    def get_ingredients_by_recipe_id(self, recipe_id: int) -> List[RecipeIngredient]:
        return self.repo.get_ingredients_by_recipe_id(recipe_id)

    @catch_errors
    def add_recipe(self, name: str, instructions: str, tags: str, ingredients: List[dict]):
        # Create the Recipe without ingredients.
        recipe = Recipe(
            id=0,  # Database assigns this
            name=name,
            instructions=instructions,
            tags=tags,
            created_at=None,
            updated_at=None,
            ingredients=[]
        )
        # Add the recipe to the repository to get the assigned id.
        recipe_id = self.repo.add_recipe(recipe)
        recipe.id = recipe_id  # Update the recipe id.

        # Now create RecipeIngredient instances with the correct recipe_id.
        for ing in ingredients:
            recipe_ingredient = RecipeIngredient(
                product_id=ing['product_id'],
                quantity=ing['quantity'],
                unit=ing.get('unit', '')
            )
            self.repo.add_recipe_ingredient(recipe_id, recipe_ingredient)

        # Optionally, fetch updated ingredients.
        recipe.ingredients = self.repo.get_ingredients_by_recipe_id(recipe_id)
        return recipe

    @catch_errors
    def update_recipe(self, recipe_id: int, name: str = None, instructions: str = None, tags: str = None, ingredients: List[dict] = None):
        recipe = self.repo.get_recipe_by_id(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")
        if name:
            recipe.name = name
        if instructions:
            recipe.instructions = instructions
        if tags is not None:
            recipe.tags = tags
        if ingredients is not None:
            # Remove existing ingredients and add new ones.
            self.repo.remove_ingredients_from_recipe(recipe_id)
            for ing in ingredients:
                recipe_ingredient = RecipeIngredient(
                    product_id=ing['product_id'],
                    quantity=ing['quantity'],
                    unit=ing.get('unit', '')
                )
                self.repo.add_recipe_ingredient(recipe_id, recipe_ingredient)
        self.repo.update_recipe(recipe_id, recipe)
        return recipe

    @catch_errors
    def delete_recipe(self, recipe_id: int):
        # Remove ingredients first, then delete the recipe.
        self.repo.remove_ingredients_from_recipe(recipe_id)
        self.repo.delete_recipe(recipe_id)


class ShoppingListController:
    def __init__(self):
        self.repo = ShoppingListRepository()
        self.product_repo = ProductRepository()
        self.weight_unit, self.volume_unit = self.load_units()

    @catch_errors
    def load_units(self):
        """Lataa asetetut yksiköt config.json-tiedostosta."""
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                return settings.get("weight_unit", "kg"), settings.get("volume_unit", "l")
        except (FileNotFoundError, json.JSONDecodeError):
            return "kg", "l"  # Oletusyksiköt

    @catch_errors
    def save_units(self):
        """Tallentaa yksikköasetukset config.json-tiedostoon."""
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}
        config["settings"] = config.get("settings", {})
        config["settings"]["weight_unit"] = self.weight_unit
        config["settings"]["volume_unit"] = self.volume_unit
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

    @catch_errors
    def update_weight_unit(self, new_unit: str):
        self.weight_unit = new_unit
        self.save_units()

    @catch_errors
    def update_volume_unit(self, new_unit: str):
        self.volume_unit = new_unit
        self.save_units()

    @catch_errors
    def update_total_sum(self, shopping_list_id: int, total_sum: float):
        """
        Päivittää ostoslistan kokonaisarvon tietokannassa.
        """
        self.repo.update_total_sum(shopping_list_id, total_sum)

    @catch_errors
    def calculate_total_cost(self, shopping_list_id: int):
        items = self.repo.get_items_by_shopping_list_id(shopping_list_id)
        total_cost = 0.0
        for item in items:
            product = self.product_repo.get_product_by_id(item.product_id)
            if product:
                # Calculation remains as price * quantity.
                total_cost += product.price_per_unit * item.quantity
        total_cost = round(total_cost, 2)
        return total_cost

    @catch_errors
    def get_all_shopping_lists(self) -> Dict[int, ShoppingList]:
        shopping_lists = self.repo.get_all_shopping_lists()
        for shopping_list in shopping_lists.values():
            shopping_list.items = self.repo.get_items_by_shopping_list_id(
                shopping_list.id)
        return shopping_lists

    @catch_errors
    def get_shopping_list_with_prices(self, shopping_list_id: int):
        shopping_list = self.repo.get_shopping_list_by_id(shopping_list_id)
        if not shopping_list:
            raise ValueError("Shopping list not found")
        items_with_prices = []
        for item in shopping_list.items:
            product = self.product_repo.get_product_by_id(item.product_id)
            if product:
                total_price = round(product.price_per_unit * item.quantity, 2)
                items_with_prices.append({
                    "product_id": item.product_id,
                    "name": product.name,
                    # Use the unit from the shopping list item if available; otherwise use the product default.
                    "unit": item.unit if item.unit else product.unit,
                    "price_per_unit": product.price_per_unit,
                    "quantity": item.quantity,
                    "total_price": total_price,
                    "is_purchased": item.is_purchased
                })
        return {
            "shopping_list_id": shopping_list.id,
            "title": shopping_list.title,
            "items": items_with_prices,
            "total_sum": shopping_list.total_sum
        }

    @catch_errors
    def get_shopping_list_by_id(self, shopping_list_id: int) -> ShoppingList:
        shopping_list = self.repo.get_shopping_list_by_id(shopping_list_id)
        if shopping_list:
            shopping_list.total_sum = self.calculate_total_cost(
                shopping_list_id)
        return shopping_list

    @catch_errors
    def get_purchased_count(self, shopping_list_id: int) -> int:
        return self.repo.get_purchased_count_by_shopping_list_id(shopping_list_id)

    @catch_errors
    def add_shopping_list(self, title: str, items: List[dict]):
        shopping_list = ShoppingList(
            id=0,  # Database will assign the ID
            title=title,
            total_sum=0,
            purchased_count=0,
            created_at=None,
            updated_at=None,
            items=[]
        )
        shopping_list_id = self.repo.add_shopping_list(shopping_list)
        shopping_list.id = shopping_list_id  # Update with the correct ID

        return shopping_list

    @catch_errors
    def update_shopping_list(self, shopping_list_id: int, title: str = None, items: List[dict] = None):
        shopping_list = self.repo.get_shopping_list_by_id(shopping_list_id)
        if not shopping_list:
            raise ValueError("Shopping list not found")
        if title:
            shopping_list.title = title
        if items:
            # Delete existing shopping list items.
            self.repo.delete_shopping_list_item(shopping_list_id)
            for item in items:
                shopping_list_item = ShoppingListItem(
                    id=0,
                    shopping_list_id=shopping_list_id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    # NEW: Use unit provided, defaulting to empty string.
                    unit=item.get('unit', ""),
                    is_purchased=item.get('is_purchased', False),
                    created_at=None,
                    updated_at=None,
                )
                self.repo.add_shopping_list_items(
                    shopping_list_id, shopping_list_item)
        shopping_list.total_sum = self.calculate_total_cost(shopping_list_id)
        self.repo.update_shopping_list(shopping_list_id, shopping_list)
        return shopping_list

    @catch_errors
    def update_purchased_status(self, item_id: int, is_purchased: bool):
        if is_purchased:
            is_purchased = 1
        else:
            is_purchased = 0
        self.repo.update_purchased_status(item_id, is_purchased)

    @catch_errors
    def delete_shopping_list_by_id(self, shoplist_id: int):
        self.repo.delete_shopping_list_by_id(shoplist_id)

    @catch_errors
    def get_items_by_shopping_list_id(self, shoplist_id):
        return self.repo.get_items_by_shopping_list_id(shoplist_id)

    @catch_errors
    def get_product_id_by_shopping_list_item_id(self, shopping_list_item_id: int) -> int:
        """
        Retrieves the product id for the shopping list item with the given id.
        This method expects that your repository provides a method to fetch a single
        shopping list item by its id (e.g., get_shopping_list_item_by_id).
        """
        item = self.repo.get_shopping_list_item_by_id(shopping_list_item_id)
        if not item:
            raise ValueError(
                f"Shopping list item with id {shopping_list_item_id} not found.")
        return item.product_id


class ProductController:
    def __init__(self):
        self.repo = ProductRepository()
        self.weight_unit, self.volume_unit = self.load_units()
        self.currency, self.currency_multiplier = self.load_currency()

    @catch_errors
    def load_currency(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                currency = settings.get("currency", "€")
            multiplier = 1
            return currency, multiplier
        except (FileNotFoundError, json.JSONDecodeError):
            return "€", 1

    @catch_errors
    def get_price_with_currency(self, price_per_unit: float) -> str:
        converted_price = price_per_unit * self.currency_multiplier
        return f"{converted_price:.2f} {self.currency}"

    @catch_errors
    def load_units(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                return settings.get("weight_unit", "kg"), settings.get("volume_unit", "l")
        except (FileNotFoundError, json.JSONDecodeError):
            return "kg", "l"

    @catch_errors
    def get_all_products(self) -> Dict[int, Product]:
        return self.repo.get_all_products()

    @catch_errors
    def get_product_by_id(self, product_id: int):
        return self.repo.get_product_by_id(product_id)

    @catch_errors
    def get_all_categories(self) -> List[str]:
        return self.repo.get_all_categories()

    @catch_errors
    def get_items_by_shopping_list_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        return self.repo.get_products_by_shoplist_id(shopping_list_id)

    @catch_errors
    def calculate_total_cost(self, product_id: int, quantity: float):
        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return self.get_price_with_currency(product.price_per_unit * quantity)

    @catch_errors
    def add_product(self, name: str, unit: str, price_per_unit: float, category: str):
        product = Product(
            id=0,
            name=name,
            unit=unit,
            price_per_unit=price_per_unit,
            category=category,
            created_at=None,
            updated_at=None
        )
        return self.repo.add_product(product)

    @catch_errors
    def update_product(self, product_id: int, name: str = None, price_per_unit: float = None, category: str = None, unit: str = None):
        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if name:
            product.name = name
        if price_per_unit:
            product.price_per_unit = price_per_unit
        if category:
            product.category = category
        if unit:
            product.unit = unit
        self.repo.update_product(product_id, product)
        return product

    @catch_errors
    def delete_product(self, product_id: int):
        self.repo.delete_product(product_id)


class ErrorController:
    def __init__(self):
        self.repo = ErrorRepository()

    @catch_errors
    def log_error(self, error_message: str, tb: str = "", func_name: str = "") -> int:
        """
        Creates a new error log entry and inserts it into the database.

        Parameters:
            error_message (str): The error message describing the problem.
            tb (str): The traceback details (optional).
            func_name (str): The name of the function where the error occurred (optional).

        Returns:
            int: The ID of the newly inserted error log.
        """
        # Create an ErrorLog instance.
        # Note: 'id' is set to 0 and 'error_time' is set to the current datetime.
        error_log = ErrorLog(
            id=0,  # Database will auto-assign a new ID.
            error_message=error_message,
            error_time=datetime.now(),
            traceback=tb,
            func_name=func_name
        )
        return self.repo.insert_error_log(error_log)

    @catch_errors
    def delete_error_log(self, error_id: int):
        """
        Deletes an error log entry from the database.

        Parameters:
            error_id (int): The ID of the error log record to delete.
        """
        self.repo.delete_error_log(error_id)

    @catch_errors
    def get_all_error_logs(self, sort_order: str = "DESC") -> List[ErrorLog]:
        """
        Retrieves all error log entries sorted by the error time.

        Parameters:
            sort_order (str): "ASC" for ascending or "DESC" for descending order. Default is "DESC".

        Returns:
            List[ErrorLog]: A list of error log records.
        """
        return self.repo.get_all_error_logs(sort_order)

    @catch_errors
    def get_all_error_logs_as_one_string(self, sort_order: str = "DESC") -> str:
        """
        Retrieves all error logs from the database and returns a single formatted string 
        with a clear separation between each error log.

        Parameters:
            sort_order (str): Sort order by 'ASC' or 'DESC'. Default is "DESC".

        Returns:
            str: A formatted string containing all error logs.
        """
        return self.repo.get_error_logs_as_string(sort_order)
