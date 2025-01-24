import sqlite3
from typing import List
import os


def main():
    db_path = "cook_and_cart.db"
    db_path = os.path.join(os.getcwd(), "utils", db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    query ="""
    SELECT * FROM recipes
    """
    
    cursor.execute(query)
    connection.commit()

if __name__ == "__main__":
    main()