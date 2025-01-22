import sqlite3
from typing import List


def main():
    db_path = "/utils/cook_and_cart.db"
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