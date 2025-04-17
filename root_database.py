# File: root_database.py --------------------------------------------------------------------

import sqlite3
from typing import List, Dict
import os
import functools
import logging
from error_handler import catch_errors


class DatabaseManager:
    _instance = None

    @catch_errors
    def __init__(self, db_path="utils/cook_and_cart.db"):
        if DatabaseManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            # Check if the database file exists; if not, create it (which also creates the directory)
            if not os.path.exists(db_path):
                DatabaseManager.create_database(db_path)
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            DatabaseManager._instance = self

    @staticmethod
    @catch_errors
    def get_instance():
        if DatabaseManager._instance is None:
            DatabaseManager()
        return DatabaseManager._instance

    @catch_errors
    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    @catch_errors
    def fetchall(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    @catch_errors
    def fetchone(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()

    @catch_errors
    def executemany(self, query: str, params: List[tuple]):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params)
            conn.commit()
        return cursor

    @staticmethod
    @catch_errors
    def create_database(db_path):
        # Ensure that the database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Check if the database already exists
        db_exists = os.path.exists(db_path)

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON;")

        if not db_exists:
            # Create tables if the database is new
            create_tables = """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                price_per_unit REAL,
                category TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                instructions TEXT NOT NULL,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                UNIQUE(recipe_id, product_id)
            );
            
            CREATE TABLE IF NOT EXISTS shopping_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                total_sum REAL DEFAULT 0.0,
                purchased_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS shopping_list_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shopping_list_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                is_purchased BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                UNIQUE(shopping_list_id, product_id)
            );
            
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_message TEXT NOT NULL,
                error_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                traceback TEXT,
                func_name TEXT
            );
            """
            cursor.executescript(create_tables)
            print("Tables created successfully.")
        else:
            # If the database exists, check if 'unit' column exists in recipe_ingredients.
            cursor.execute("PRAGMA table_info(recipe_ingredients);")
            columns = cursor.fetchall()
            column_names = [col["name"] for col in columns]
            if "unit" not in column_names:
                cursor.execute(
                    "ALTER TABLE recipe_ingredients ADD COLUMN unit TEXT NOT NULL DEFAULT '';")
                print("Column 'unit' added to recipe_ingredients table.")

        # Create triggers for updating purchased_count in shopping_lists.
        create_triggers = """
        CREATE TRIGGER IF NOT EXISTS trg_item_purchased
        AFTER UPDATE OF is_purchased ON shopping_list_items
        FOR EACH ROW
        WHEN NEW.is_purchased = 1 AND OLD.is_purchased = 0
        BEGIN
            UPDATE shopping_lists
            SET purchased_count = purchased_count + 1
            WHERE id = NEW.shopping_list_id;
        END;
        
        CREATE TRIGGER IF NOT EXISTS trg_item_unpurchased
        AFTER UPDATE OF is_purchased ON shopping_list_items
        FOR EACH ROW
        WHEN NEW.is_purchased = 0 AND OLD.is_purchased = 1
        BEGIN
            UPDATE shopping_lists
            SET purchased_count = purchased_count - 1
            WHERE id = NEW.shopping_list_id;
        END;
        
        CREATE TRIGGER IF NOT EXISTS trg_item_insert_purchased
        AFTER INSERT ON shopping_list_items
        FOR EACH ROW
        WHEN NEW.is_purchased = 1
        BEGIN
            UPDATE shopping_lists
            SET purchased_count = purchased_count + 1
            WHERE id = NEW.shopping_list_id;
        END;
        
        CREATE TRIGGER IF NOT EXISTS trg_item_delete_purchased
        AFTER DELETE ON shopping_list_items
        FOR EACH ROW
        WHEN OLD.is_purchased = 1
        BEGIN
            UPDATE shopping_lists
            SET purchased_count = purchased_count - 1
            WHERE id = OLD.shopping_list_id;
        END;
        """
        try:
            cursor.executescript(create_triggers)
            print("Triggers created successfully.")
        except sqlite3.OperationalError as e:
            print(f"Error creating triggers: {e}")

        # Create indices to improve query performance.
        create_indices = """
        CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_recipe_id ON recipe_ingredients(recipe_id);
        CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_product_id ON recipe_ingredients(product_id);
        CREATE INDEX IF NOT EXISTS idx_shopping_list_items_shopping_list_id ON shopping_list_items(shopping_list_id);
        CREATE INDEX IF NOT EXISTS idx_shopping_list_items_product_id ON shopping_list_items(product_id);
        CREATE INDEX IF NOT EXISTS idx_shopping_lists_purchased_count ON shopping_lists(purchased_count);
        """
        cursor.executescript(create_indices)

        insert_products = """
        INSERT INTO products (name, unit, price_per_unit, category) VALUES
        ('Kanafilee', 'kg', 15.00, 'Liha ja kala'),
        ('Naudan ulkofileepihvi', 'kg', 25.00, 'Liha ja kala'),
        ('Lohi', 'kg', 20.00, 'Liha ja kala'),
        ('Kananmunat', 'kpl', 0.35, 'Maitotuotteet'),
        ('Maito', 'l', 1.20, 'Maitotuotteet'),
        ('Voi', 'kg', 12.00, 'Maitotuotteet'),
        ('Cheddar-juusto', 'kg', 15.00, 'Maitotuotteet'),
        ('Jogurtti', 'l', 2.00, 'Maitotuotteet'),
        ('Kerma', 'l', 2.50, 'Maitotuotteet'),
        ('Kookosmaito', 'l', 2.00, 'Maitotuotteet'),
        ('Jauhot', 'kg', 1.00, 'Leipä ja viljatuotteet'),
        ('Sokeri', 'kg', 1.50, 'Leipä ja viljatuotteet'),
        ('Suola', 'kg', 0.50, 'Mausteet ja öljyt'),
        ('Oliiviöljy', 'l', 8.00, 'Mausteet ja öljyt'),
        ('Basilika (kuiva)', 'g', 0.03, 'Mausteet ja öljyt'),
        ('Riisi', 'kg', 2.00, 'Kuivatuotteet'),
        ('Pasta', 'kg', 1.80, 'Kuivatuotteet'),
        ('Murskatut tomaatit', 'l', 1.50, 'Muut'),
        ('Tomaatit', 'kg', 3.00, 'Kasvikset ja hedelmät'),
        ('Kurkut', 'kg', 2.50, 'Kasvikset ja hedelmät'),
        ('Perunat', 'kg', 0.80, 'Kasvikset ja hedelmät'),
        ('Sipulit', 'kg', 1.00, 'Kasvikset ja hedelmät'),
        ('Paprika', 'kg', 4.00, 'Kasvikset ja hedelmät'),
        ('Sitruuna', 'kpl', 0.70, 'Kasvikset ja hedelmät'),
        ('Minttu (tuore)', 'kpl', 0.75, 'Kasvikset ja hedelmät'),
        ('Sitruunamehu', 'ml', 0.01, 'Maitotuotteet'),
        ('Tumma suklaa', 'g', 0.02, 'Makeiset'),
        ('Vesi', 'l', 0.00, 'Juomat');
        """

        cursor.execute(insert_products)

        conn.commit()
        conn.close()

        if not db_exists:
            print(f"Database '{db_path}' created successfully.")
        else:
            print(f"Database '{db_path}' updated successfully.")
