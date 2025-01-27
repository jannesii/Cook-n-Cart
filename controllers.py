# controllers.py

from models import Recipe, RecipeIngredient, Product, ShoppingList, ShoppingListItem
from repositories import RecipeRepository, ProductRepository, ShoppingListRepository
from typing import List, Dict


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
            recipe_ingredient = RecipeIngredient(
                product_id=ing['product_id'],
                quantity=ing['quantity']
            )
            self.repo.add_recipe_ingredient(recipe_id, recipe_ingredient)

        # Optionally, fetch updated ingredients
        recipe.ingredients = self.repo.get_ingredients_by_recipe_id(recipe_id)

        return recipe

    def update_recipe(self, recipe_id: int, name: str = None, instructions: str = None, ingredients: List[dict] = None):
        recipe = self.repo.get_recipe_by_id(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found")

        if name:
            recipe.name = name
        if instructions:
            recipe.instructions = instructions
        if ingredients:
            # Remove existing ingredients
            self.repo.remove_ingredients_from_recipe(recipe_id)
            # Add new ingredients
            for ing in ingredients:
                recipe_ingredient = RecipeIngredient(
                    product_id=ing['product_id'],
                    quantity=ing['quantity']
                )
                self.repo.add_recipe_ingredient(recipe_id, recipe_ingredient)

        self.repo.update_recipe(recipe_id, recipe)
        return recipe


class ShoppingListController:
    def __init__(self):
        self.repo = ShoppingListRepository()

    def get_all_shopping_lists(self) -> Dict[int, ShoppingList]:
        return self.repo.get_all_shopping_lists()

    def get_shopping_list_by_id(self, shopping_list_id: int) -> ShoppingList:
        return self.repo.get_shopping_list_by_id(shopping_list_id)

    def add_shopping_list(self, title: str, items: List[dict]):
        shopping_list = ShoppingList(
            id=0,  # Database will assign the actual ID
            title=title,
            total_sum=0,
            purchased_count=0,
            created_at=None,
            updated_at=None,
            items=[]
        )
        shopping_list = self.repo.add_shopping_list(shopping_list)

        # Add items to the shopping list
        shopping_list_items = []
        for item in items:
            shopping_list_item = ShoppingListItem(
                product_id=item['product_id'],
                quantity=item['quantity'],
                is_purchased=item.get('is_purchased', False)
                # id, shopping_list_id, created_at, updated_at are handled by the database
            )
            shopping_list_items.append(shopping_list_item)

        self.repo.add_items_to_shopping_list(shopping_list.id, shopping_list_items)
        shopping_list.items = self.repo.get_items_by_shopping_list_id(shopping_list.id)

        return shopping_list

    def update_shopping_list(self, shopping_list_id: int, title: str = None, items: List[dict] = None):
        shopping_list = self.repo.get_shopping_list_by_id(shopping_list_id)
        if not shopping_list:
            raise ValueError("Shopping list not found")

        if title:
            shopping_list.title = title
        if items:
            # Remove existing items
            self.repo.remove_items_from_shopping_list(shopping_list_id)
            # Add new items
            for item in items:
                shopping_list_item = ShoppingListItem(
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    is_purchased=item.get('is_purchased', False)
                )
                self.repo.add_item_to_shopping_list(shopping_list_id, shopping_list_item)

        self.repo.update_shopping_list(shopping_list_id, shopping_list)
        return shopping_list


class ProductController:
    def __init__(self):
        self.repo = ProductRepository()

    def get_all_products(self) -> Dict[int, Product]:
        return self.repo.get_all_products()

    def get_all_categories(self) -> List[str]:
        return self.repo.get_all_categories()

    def get_items_by_shopping_list_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        return self.repo.get_products_by_shoplist_id(shopping_list_id)

    def add_product(self, name: str, unit: str, price_per_unit: float, category: str):
        product = Product(
            id=0,  # Database will assign the actual ID
            name=name,
            unit=unit,
            price_per_unit=price_per_unit,
            category=category,
            created_at=None,
            updated_at=None
        )
        return self.repo.add_product(product)

    def update_product(self, product_id: int, name: str = None, description: str = None, price_per_unit: float = None, category: str = None):
        product = self.repo.get_product_by_id(product_id)
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

        self.repo.update_product(product_id, product)
        return product

    def delete_product(self, product_id: int):
        self.repo.delete_product(product_id)
