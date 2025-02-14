import sqlite3
import os

def insert_shopping_lists(cursor):
    shopping_list_query = """
    INSERT INTO shopping_lists (title, total_sum, purchased_count) 
    VALUES (?, ?, ?)
    """
    # Data to be inserted as a list of tuples
    shopping_lists_data = [
        ('Weekly Groceries', 45.50, 10),
        ('BBQ Party', 120.00, 15),
        ('Office Snacks', 30.25, 5),
        ('Birthday Supplies', 75.00, 8),
        ('Camping Trip', 60.75, 12)
    ]
    cursor.executemany(shopping_list_query, shopping_lists_data)

def insert_shopping_list_items(cursor):
    shopping_list_items_query = """
    INSERT INTO shopping_list_items (shopping_list_id, product_id, quantity, is_purchased) 
    VALUES (?, ?, ?, ?)
    """
    # Data to be inserted as a list of tuples
    shopping_list_items_data = [
        (1, 1, 2.0, 1),
        (1, 3, 1.0, 0),
        (2, 5, 1.0, 1),
        (2, 6, 2.0, 0),
        (2, 7, 3.0, 1),
        (3, 8, 3.0, 0),
        (3, 9, 2.0, 1),
        (3, 10, 1.0, 1),
        (4, 11, 2.0, 1),
        (4, 12, 1.0, 0),
        (4, 13, 1.0, 1),
        (4, 14, 1.0, 0),
        (5, 15, 1.0, 1),
        (5, 16, 2.0, 0),
        (5, 17, 1.0, 1)
    ]
    cursor.executemany(shopping_list_items_query, shopping_list_items_data)

if __name__ == "__main__":
    db_path = "cook_and_cart.db"
    db_path = os.path.join(os.getcwd(), "utils", db_path)
    
    # Ensure the directory exists (optional step, depending on your structure)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Insert shopping lists and related items
    insert_shopping_lists(cursor)
    insert_shopping_list_items(cursor)

    # Commit changes and close the connection
    connection.commit()
    connection.close()
