# controllers.py
from typing import Dict, List
import json
from typing import List, Dict

from root_models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem
from root_repositories import RecipeRepository, ProductRepository, ShoppingListRepository
CONFIG_FILE = "utils/config.json"


class RecipeController:
    def __init__(self):
        self.repo = RecipeRepository()

    def get_all_recipes(self) -> Dict[int, Recipe]:
        return self.repo.get_all_recipes()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self.repo.get_recipe_by_id(recipe_id)

    def get_all_tags(self) -> List[str]:
        return self.repo.get_all_tags()

    def get_ingredients_by_recipe_id(self, recipe_id: int) -> List[RecipeIngredient]:
        return self.repo.get_ingredients_by_recipe_id(recipe_id)

    def add_recipe(self, name: str, instructions: str, tags: str, ingredients: List[dict]):
        # Create the Recipe without ingredients
        recipe = Recipe(
            id=0,  # Database assigns this
            name=name,
            instructions=instructions,
            tags=tags,
            created_at=None,
            updated_at=None,
            ingredients=[]
        )
        # Add the recipe to the repository to get the assigned id
        recipe_id = self.repo.add_recipe(recipe)
        recipe.id = recipe_id  # Update the recipe id

        # Now create RecipeIngredient instances with the correct recipe_id
        for ing in ingredients:
            # Expect each ingredient dict to have both 'quantity' and 'unit'
            recipe_ingredient = RecipeIngredient(
                product_id=ing['product_id'],
                quantity=ing['quantity'],
                # Use an empty string or a default if not provided
                unit=ing.get('unit', '')
            )
            self.repo.add_recipe_ingredient(recipe_id, recipe_ingredient)

        # Optionally, fetch updated ingredients
        recipe.ingredients = self.repo.get_ingredients_by_recipe_id(recipe_id)

        return recipe

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
            # Remove existing ingredients and add new ones
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

    def delete_recipe(self, recipe_id: int):
        # Remove ingredients first, then delete the recipe itself.
        self.repo.remove_ingredients_from_recipe(recipe_id)
        self.repo.delete_recipe(recipe_id)


class ShoppingListController:
    def __init__(self):
        self.repo = ShoppingListRepository()
        self.product_repo = ProductRepository()
        self.weight_unit, self.volume_unit = self.load_units()

    def load_units(self):
        """ Lataa asetetut yksiköt config.json-tiedostosta. """
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                return settings.get("weight_unit", "kg"), settings.get("volume_unit", "l")
        except (FileNotFoundError, json.JSONDecodeError):
            return "kg", "l"  # Oletusyksiköt

    def save_units(self):
        """ Tallentaa yksikköasetukset config.json-tiedostoon. """
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

    def update_weight_unit(self, new_unit: str):
        self.weight_unit = new_unit
        self.save_units()

    def update_volume_unit(self, new_unit: str):
        self.volume_unit = new_unit
        self.save_units()
        
    def update_total_sum(self, shopping_list_id: int, total_sum: float):
        """
        Päivittää ostoslistan kokonaisarvon tietokannassa.
        """
        self.repo.update_total_sum(shopping_list_id, total_sum)

    def calculate_total_cost(self, shopping_list_id: int):

        items = self.repo.get_items_by_shopping_list_id(shopping_list_id)
        total_cost = 0.0

        for item in items:
            product = self.product_repo.get_product_by_id(item.product_id)
            if product:
                # Use the standardized conversion from the ProductController.
                total_cost += product.price_per_unit * item.quantity

        total_cost = round(total_cost, 2)
        # self.repo.update_total_sum(shopping_list_id, total_cost)

        return total_cost

    def get_all_shopping_lists(self) -> Dict[int, ShoppingList]:
        # Fetch all shopping lists from the repository
        shopping_lists = self.repo.get_all_shopping_lists()

        # Populate items for each shopping list
        for shopping_list in shopping_lists.values():
            shopping_list.items = self.repo.get_items_by_shopping_list_id(
                shopping_list.id)

        return shopping_lists

    def get_shopping_list_with_prices(self, shopping_list_id: int):

        shopping_list = self.repo.get_shopping_list_by_id(ShoppingList)
        if not shopping_list:
            raise ValueError("Shopping list not found")

        items_with_prices = []
        for item in shopping_list.items:
            product = self.repo.get_product_by_id(item.product_id)
            if product:
                total_price = round(product.price_per_unit * item.quantity, 2)
                items_with_prices.append({
                    "product_id": item.product_id,
                    "name": product.name,
                    "unit": product.unit,
                    "price_per_unit": product.price_per_unit,
                    "quantity": item.quantity,
                    "total_price": total_price,  # Kokonaishinta
                    "is_purchased": item.is_purchased
                })

        return {
            "shopping_list_id": shopping_list,
            "title": shopping_list.title,
            "items": items_with_prices,
            "total_sum": shopping_list.total_sum
        }

    def get_shopping_list_by_id(self, shopping_list_id: int) -> ShoppingList:
        shopping_list = self.repo.get_shopping_list_by_id(shopping_list_id)
        if shopping_list:
            shopping_list.total_sum = self.calculate_total_cost(
                shopping_list_id)
        return shopping_list
    
    def get_purchased_count(self, shopping_list_id: int) -> int:
        return self.repo.get_purchased_count_by_shopping_list_id(shopping_list_id)

    def add_shopping_list(self, title: str, items: List[dict]):
        # Create a new ShoppingList object
        shopping_list = ShoppingList(
            id=0,  # Database will assign the ID
            title=title,
            total_sum=0,
            purchased_count=0,
            created_at=None,
            updated_at=None,
            items=[]
        )
        # Insert shopping list into the database and retrieve the assigned ID
        shopping_list_id = self.repo.add_shopping_list(shopping_list)
        shopping_list.id = shopping_list_id  # Update the object with the correct ID

        # Add items to the shopping list
        shopping_list_items = []
        for item in items:
            product = item.get('product')
            if not product or 'quantity' not in item:
                raise ValueError(
                    "Invalid product data: 'product' or 'quantity' is missing.")

            shopping_list_item = ShoppingListItem(
                id=0,  # Assigned by the database
                shopping_list_id=shopping_list_id,
                product_id=product.id,  # Access the Product object's ID
                quantity=item['quantity'],
                is_purchased=item.get('is_purchased', False),
                created_at=None,
                updated_at=None
            )
            shopping_list_items.append(shopping_list_item)

        self.repo.add_shopping_list_items(
            shopping_list_id, shopping_list_items)

        query = "SELECT * FROM shopping_list_items WHERE shopping_list_id = ?"
        rows = self.repo.db.fetchall(query, (shopping_list_id,))

        # Fetch items from the database to update the ShoppingList object
        shopping_list.items = self.repo.get_items_by_shopping_list_id(
            shopping_list_id)

        return shopping_list

    def update_shopping_list(self, shopping_list_id: int, title: str = None, items: List[dict] = None):
        shopping_list = self.repo.get_shopping_list_by_id(shopping_list_id)
        if not shopping_list:
            raise ValueError("Shopping list not found")

        if title:
            shopping_list.title = title
        if items:
            # Poistetaan vanhat tuotteet
            self.repo.delete_shopping_list_item(shopping_list_id)

            # Lisätään uudet tuotteet
            for item in items:
                shopping_list_item = ShoppingListItem(
                    id=0,
                    shopping_list_id=shopping_list_id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    is_purchased=item.get('is_purchased', False),
                    created_at=None,
                    updated_at=None,
                )
                self.repo.add_shopping_list_items(
                    shopping_list_id, shopping_list_item)

        # Päivitetään hinta
        shopping_list.total_sum = self.calculate_total_cost(shopping_list_id)

        self.repo.update_shopping_list(shopping_list_id, shopping_list)
        return shopping_list
    
    def update_purchased_status(self, item_id: int, is_purchased: bool):
        """
        Päivittää ostoslistan tuotteen ostetun tilan.
        """
        if is_purchased:
            is_purchased = 1
        else:
            is_purchased = 0

        self.repo.update_purchased_status(item_id, is_purchased)

    def delete_shopping_list_by_id(self, shoplist_id: int):
        """
        Deletes the shopping list with the given ID.
        """
        self.repo.delete_shopping_list_by_id(shoplist_id)

    def get_items_by_shopping_list_id(self, shoplist_id):
        shoppinglist = []
        shoppinglist = self.repo.get_items_by_shopping_list_id(shoplist_id)
        return shoppinglist


class ProductController:
    def __init__(self):
        self.repo = ProductRepository()
        self.weight_unit, self.volume_unit = self.load_units()
        self.currency, self.currency_multiplier = self.load_currency()

    def load_currency(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                currency = settings.get("currency", "€")

            multiplier = 1
            return currency, multiplier
        except (FileNotFoundError, json.JSONDecodeError):
            return "€", 1

    def get_price_with_currency(self, price_per_unit: float) -> str:
        converted_price = price_per_unit * self.currency_multiplier
        return f"{converted_price:.2f} {self.currency}"

    def load_units(self):
        # ... (existing unit loading code)
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                return settings.get("weight_unit", "kg"), settings.get("volume_unit", "l")
        except (FileNotFoundError, json.JSONDecodeError):
            return "kg", "l"  # Default units

    def get_all_products(self) -> Dict[int, Product]:

        return self.repo.get_all_products()

    def get_product_by_id(self, product_id: int):
        return self.repo.get_product_by_id(product_id)

    def get_all_categories(self) -> List[str]:
        return self.repo.get_all_categories()

    def get_items_by_shopping_list_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        return self.repo.get_products_by_shoplist_id(shopping_list_id)

    def calculate_total_cost(self, product_id: int, quantity: float):

        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return self.get_price_with_currency(product.price_per_unit * quantity)

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

    def update_product(self, product_id: int, name: str = None, price_per_unit: float = None, category: str = None):
        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        if name:
            product.name = name
        if price_per_unit:
            product.price_per_unit = price_per_unit
        if category:
            product.category = category

        self.repo.update_product(product_id, product)
        return product

    def delete_product(self, product_id: int):
        self.repo.delete_product(product_id)
