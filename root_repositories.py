# repositories.py

from root_database import DatabaseManager
from root_models import Recipe, Product, RecipeIngredient, ShoppingList, ShoppingListItem, ErrorLog
from typing import List, Dict
import functools
import logging
from error_handler import catch_errors


class RecipeRepository:
    @catch_errors
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    @catch_errors
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        query = "SELECT * FROM recipes WHERE id = ?"
        row = self.db.fetchone(query, (recipe_id,))
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

    @catch_errors
    def get_all_recipes(self) -> Dict[int, Recipe]:
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
        recipes_dict: Dict[int, Recipe] = {
            recipe.id: recipe for recipe in recipes}
        return recipes_dict

    @catch_errors
    def get_all_tags(self) -> List[str]:
        query = "SELECT tags FROM recipes"
        rows = self.db.fetchall(query)
        tags = []
        for row in rows:
            if row['tags']:
                tags.extend([tag.strip()
                            for tag in row['tags'].split(',') if tag.strip()])
        return tags

    @catch_errors
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
                # <-- Added to retrieve the unit from the database.
                unit=row['unit'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            ingredients.append(ingredient)
        return ingredients

    @catch_errors
    def add_recipe(self, recipe: Recipe) -> int:
        query = """
        INSERT INTO recipes (name, instructions, tags)
        VALUES (?, ?, ?)
        """
        cursor = self.db.execute_query(
            query, (recipe.name, recipe.instructions, recipe.tags))
        recipe_id = cursor.lastrowid
        return recipe_id

    @catch_errors
    def add_recipe_ingredient(self, recipe_id: int, ingredient: RecipeIngredient):
        query = """
        INSERT INTO recipe_ingredients (recipe_id, product_id, quantity, unit)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(
            query, (recipe_id, ingredient.product_id,
                    ingredient.quantity, ingredient.unit)
        )

    @catch_errors
    def remove_ingredients_from_recipe(self, recipe_id: int):
        query = "DELETE FROM recipe_ingredients WHERE recipe_id = ?"
        self.db.execute_query(query, (recipe_id,))

    def delete_recipe(self, recipe_id: int):
        query = "DELETE FROM recipes WHERE id = ?"
        self.db.execute_query(query, (recipe_id,))

    def update_recipe(self, recipe_id: int, recipe: Recipe):
        query = """
        UPDATE recipes
        SET name = ?,
            instructions = ?,
            tags = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        self.db.execute_query(
            query, (recipe.name, recipe.instructions, recipe.tags, recipe_id))


class ProductRepository:
    @catch_errors
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    @catch_errors
    def get_all_products(self) -> Dict[int, Product]:
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

        products_dict: Dict[int, Product] = {
            product.id: product for product in products}
        return products_dict

    @catch_errors
    def get_product_by_id(self, product_id: int) -> Product:
        query = "SELECT * FROM products WHERE id = ?"
        row = self.db.fetchone(query, (product_id,))
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

    @catch_errors
    def get_all_categories(self) -> List[str]:
        query = "SELECT category FROM products"
        rows = self.db.fetchall(query)
        categories = []
        for row in rows:
            categories.append(row['category'])
        return categories

    @catch_errors
    def get_products_by_shoplist_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        query = "SELECT * FROM shopping_list_items WHERE shopping_list_id = ?"
        rows = self.db.fetchall(query, (shopping_list_id,))
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

    @catch_errors
    def add_product(self, product: Product):
        query = """
        INSERT INTO products (name, unit, price_per_unit, category)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (product.name, product.unit,
                                      product.price_per_unit, product.category))

    @catch_errors
    def update_product(self, product_id: int, product: Product):
        query = """
        UPDATE products
        SET name = ?, unit = ?, price_per_unit = ?, category = ?
        WHERE id = ?
        """
        self.db.execute_query(query, (product.name, product.unit,
                                      product.price_per_unit, product.category, product_id))

    @catch_errors
    def delete_product(self, product_id: int):
        query = "DELETE FROM products WHERE id = ?"
        self.db.execute_query(query, (product_id,))


class ShoppingListRepository:
    @catch_errors
    def __init__(self):
        self.db = DatabaseManager.get_instance()
        self.product_repo = ProductRepository()

    @catch_errors
    def get_all_shopping_lists(self) -> Dict[int, ShoppingList]:
        query = "SELECT * FROM shopping_lists"
        rows = self.db.fetchall(query)

        if not rows:
            print("No shopping lists found!")
            return {}

        shopping_lists = []

        for row in rows:
            # Fetch items for this shopping list including the unit column.
            items_query = "SELECT * FROM shopping_list_items WHERE shopping_list_id = ?"
            items_rows = self.db.fetchall(items_query, (row['id'],))

            items = [
                ShoppingListItem(
                    id=item_row['id'],
                    shopping_list_id=item_row['shopping_list_id'],
                    product_id=item_row['product_id'],
                    quantity=item_row['quantity'],
                    unit=item_row['unit'],  # NEW: include unit from the row
                    is_purchased=item_row['is_purchased'],
                    created_at=item_row['created_at'],
                    updated_at=item_row['updated_at'],
                ) for item_row in items_rows
            ]

            # Create the ShoppingList object with the items
            shopping_list = ShoppingList(
                id=row['id'],
                title=row['title'],
                total_sum=row['total_sum'],
                purchased_count=row['purchased_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                items=items  # Include the items here
            )
            shopping_lists.append(shopping_list)

        # Convert to a dictionary with the ID as the key
        shopping_lists_dict: Dict[int, ShoppingList] = {
            shopping_list.id: shopping_list for shopping_list in shopping_lists
        }
        return shopping_lists_dict

    @catch_errors
    def get_shopping_list_by_id(self, shopping_list_id: int) -> ShoppingList:
        query = "SELECT * FROM shopping_lists WHERE id = ?"
        row = self.db.fetchone(query, (shopping_list_id,))
        if row:
            # Here we assume that the products repository's method is also updated
            shopping_list = ShoppingList(
                id=row['id'],
                title=row['title'],
                total_sum=row['total_sum'],
                purchased_count=row['purchased_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                items=self.product_repo.get_products_by_shoplist_id(row['id'])
            )
            return shopping_list
        return None

    @catch_errors
    def add_shopping_list(self, shoppinglist: ShoppingList):
        query = """
        INSERT INTO shopping_lists (title, total_sum, purchased_count)
        VALUES (?, ?, ?)
        """
        cursor = self.db.execute_query(
            query, (shoppinglist.title, shoppinglist.total_sum, shoppinglist.purchased_count))
        list_id = cursor.lastrowid
        return list_id

    @catch_errors
    def add_shopping_list_items(self, shopping_list_id: int, items: List[ShoppingListItem]):
        for item in items:
            print(
                f"Attempting to insert item with values: shopping_list_id={shopping_list_id}, "
                f"product_id={item.product_id}, quantity={item.quantity}, "
                f"unit={item.unit}, is_purchased={item.is_purchased}")
            try:
                query = """
                INSERT INTO shopping_list_items 
                (shopping_list_id, product_id, quantity, unit, is_purchased, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
                self.db.execute_query(
                    query, (item.shopping_list_id, item.product_id, item.quantity, item.unit, item.is_purchased)
                )
            except Exception as e:
                print(f"Error inserting item: {item}, Error: {e}")


    @catch_errors
    def update_shopping_list(self, shopping_list_id: int, shopping_list: ShoppingList):
        query = """
        UPDATE shopping_lists
        SET title = ?, total_sum = ?, purchased_count = ?
        WHERE id = ?
        """
        self.db.execute_query(query, (shopping_list.title, shopping_list.total_sum,
                                      shopping_list.purchased_count, shopping_list_id))
        self.db.execute_query(
            "DELETE FROM shopping_list_items WHERE shopping_list_id = ?", (shopping_list_id,))
        for item in shopping_list.items:
            self.add_shopping_list_items(shopping_list_id, item)

    @catch_errors
    def get_items_by_shopping_list_id(self, shopping_list_id: int) -> List[ShoppingListItem]:
        # NEW: Update the SELECT statement to include the unit column.
        query = """
        SELECT id, shopping_list_id, product_id, quantity, unit, is_purchased, created_at, updated_at
        FROM shopping_list_items
        WHERE shopping_list_id = ?
        """
        rows = self.db.fetchall(query, (shopping_list_id,))
        items = []
        for row in rows:
            item = ShoppingListItem(
                id=row['id'],
                shopping_list_id=row['shopping_list_id'],
                product_id=row['product_id'],
                quantity=row['quantity'],
                unit=row['unit'],  # NEW: read the unit value
                is_purchased=row['is_purchased'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )
            items.append(item)
        return items

    @catch_errors
    def get_purchased_count_by_shopping_list_id(self, shopping_list_id: int) -> int:
        query = """
        SELECT COUNT(*) AS purchased_count
        FROM shopping_list_items
        WHERE shopping_list_id = ? AND is_purchased = 1
        """
        row = self.db.fetchone(query, (shopping_list_id,))
        if row:
            return row['purchased_count']

    @catch_errors
    def update_shopping_list_items(self, items: List[ShoppingListItem]):
        """Updates the quantity, unit, or purchase status of multiple items in the shopping list."""
        for item in items:
            # NEW: Update query now also sets the unit column.
            query = """
            UPDATE shopping_list_items
            SET quantity = ?, unit = ?, is_purchased = ?, updated_at = CURRENT_TIMESTAMP
            WHERE shopping_list_id = ? AND product_id = ?
            """
            self.db.execute_query(
                query, (item.quantity, item.unit, item.is_purchased, item.shopping_list_id, item.product_id))

    @catch_errors
    def update_purchased_status(self, item_id: int, is_purchased: bool):
        """Updates the purchase status of a single item in the shopping list."""
        query = """
        UPDATE shopping_list_items
        SET is_purchased = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        self.db.execute_query(query, (is_purchased, item_id))

    @catch_errors
    def update_total_sum(self, shopping_list_id: int, total_sum: float):
        """Updates the total sum of a shopping list."""
        query = """
        UPDATE shopping_lists
        SET total_sum = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        self.db.execute_query(query, (total_sum, shopping_list_id))

    @catch_errors
    def delete_shopping_list_item(self, item_id: int):
        """Removes an item from the shopping list."""
        query = "DELETE FROM shopping_list_items WHERE id = ?"
        self.db.execute_query(query, (item_id,))

    @catch_errors
    def delete_shopping_list_by_id(self, shoplist_id: int):
        try:
            # Delete all items in the shopping list first (cascade delete might also work)
            delete_items_query = "DELETE FROM shopping_list_items WHERE shopping_list_id = ?"
            self.db.execute_query(delete_items_query, (shoplist_id,))

            # Delete the shopping list itself
            delete_list_query = "DELETE FROM shopping_lists WHERE id = ?"
            self.db.execute_query(delete_list_query, (shoplist_id,))
        except Exception as e:
            raise Exception(f"Failed to delete shopping list: {str(e)}")


class ErrorRepository:
    @catch_errors
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    @catch_errors
    def insert_error_log(self, error_log: ErrorLog) -> int:
        """
        Inserts a new error log into the database.

        Parameters:
            error_log (ErrorLog): An instance containing the error details.

        Returns:
            int: The ID of the newly inserted error log.
        """
        query = """
        INSERT INTO error_logs (error_message, traceback, func_name)
        VALUES (?, ?, ?)
        """
        cursor = self.db.execute_query(
            query, (error_log.error_message, error_log.traceback, error_log.func_name))
        return cursor.lastrowid

    @catch_errors
    def delete_error_log(self, error_id: int):
        """
        Deletes an error log from the database by its ID.

        Parameters:
            error_id (int): The primary key of the error log to delete.
        """
        query = "DELETE FROM error_logs WHERE id = ?"
        self.db.execute_query(query, (error_id,))

    @catch_errors
    def get_all_error_logs(self, sort_order: str = "DESC") -> List[ErrorLog]:
        """
        Retrieves all error logs from the database, sorted by error_time.

        Parameters:
            sort_order (str): Sort order by 'ASC' or 'DESC'. Default is "DESC".

        Returns:
            List[ErrorLog]: A list of ErrorLog objects.
        """
        # Validate and set the sort order.
        order = "ASC" if sort_order.upper() == "ASC" else "DESC"
        query = f"SELECT * FROM error_logs ORDER BY error_time {order}"
        rows = self.db.fetchall(query)
        error_logs: List[ErrorLog] = []

        for row in rows:
            # Directly access the row items using keys.
            error_log = ErrorLog(
                id=row["id"],
                error_message=row["error_message"],
                error_time=row["error_time"],
                # Returns None if the field is NULL.
                traceback=row["traceback"],
                # Returns None if the field is NULL.
                func_name=row["func_name"]
            )
            error_logs.append(error_log)
        return error_logs

    @catch_errors
    def get_error_logs_as_string(self, sort_order: str = "DESC") -> str:
        """
        Retrieves all error logs from the database and returns a single formatted string 
        with a clear separation between each error log.

        Parameters:
            sort_order (str): Sort order by 'ASC' or 'DESC'. Default is "DESC".

        Returns:
            str: A formatted string containing all error logs.
        """
        error_logs = self.get_all_error_logs(sort_order)
        if not error_logs:
            return "No error logs found."

        log_strings = []
        for log in error_logs:
            # Build a formatted string for each error log using direct attributes.
            log_str = (
                f"Error ID: {log.id}\n"
                f"Time: {log.error_time}\n"
                f"Function: {log.func_name if log.func_name else 'N/A'}\n"
                f"Message: {log.error_message}\n"
                f"Traceback: {log.traceback if log.traceback else 'None'}\n"
            )
            log_strings.append(log_str)

        # Define a clear separation line between logs.
        separator = "\n" + "-" * 50 + "\n"
        # Join all error log strings using the separator.
        return separator.join(log_strings)
