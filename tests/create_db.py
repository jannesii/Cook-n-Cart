import sqlite3
import os


def create_database(db_path):
    # Varmista, että tietokannan hakemisto on olemassa
    # os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Tarkista, onko tietokanta jo olemassa
    db_exists = os.path.exists(db_path)

    # Yhdistä SQLite-tietokantaan
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ota käyttöön vierasavainten tuki
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Taulujen luominen
    create_tables = """
    CREATE TABLE  products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        unit TEXT NOT NULL,
        price_per_unit REAL,
        category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    
    CREATE TABLE  recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        instructions TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );


    CREATE TABLE  recipe_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        UNIQUE(recipe_id, product_id)
    );

    CREATE TABLE  shopping_lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        total_sum REAL DEFAULT 0.0,
        purchased_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE  shopping_list_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shopping_list_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        is_purchased BOOLEAN NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (shopping_list_id) REFERENCES shopping_lists(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
        UNIQUE(shopping_list_id, product_id)
    );
    """

    cursor.executescript(create_tables)

    # Triggereiden luominen ilman
    create_triggers = """
    -- Trigger: Kun is_purchased muuttuu 0 -> 1
    CREATE TRIGGER trg_item_purchased
    AFTER UPDATE OF is_purchased ON shopping_list_items
    FOR EACH ROW
    WHEN NEW.is_purchased = 1 AND OLD.is_purchased = 0
    BEGIN
        UPDATE shopping_lists
        SET purchased_count = purchased_count + 1
        WHERE id = NEW.shopping_list_id;
    END;

    -- Trigger: Kun is_purchased muuttuu 1 -> 0
    CREATE TRIGGER trg_item_unpurchased
    AFTER UPDATE OF is_purchased ON shopping_list_items
    FOR EACH ROW
    WHEN NEW.is_purchased = 0 AND OLD.is_purchased = 1
    BEGIN
        UPDATE shopping_lists
        SET purchased_count = purchased_count - 1
        WHERE id = NEW.shopping_list_id;
    END;

    -- Trigger: Kun ostetaan uusi tuote
    CREATE TRIGGER trg_item_insert_purchased
    AFTER INSERT ON shopping_list_items
    FOR EACH ROW
    WHEN NEW.is_purchased = 1
    BEGIN
        UPDATE shopping_lists
        SET purchased_count = purchased_count + 1
        WHERE id = NEW.shopping_list_id;
    END;

    -- Trigger: Kun poistetaan ostettu tuote
    CREATE TRIGGER trg_item_delete_purchased
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
        # cursor.executescript(create_triggers)
        print("Triggereiden luominen onnistui.")
    except sqlite3.OperationalError as e:
        print(f"Virhe triggereiden luomisessa: {e}")

    # Indeksien luominen
    create_indices = """
    CREATE INDEX  idx_recipe_ingredients_recipe_id ON recipe_ingredients(recipe_id);
    CREATE INDEX  idx_recipe_ingredients_product_id ON recipe_ingredients(product_id);
    CREATE INDEX  idx_shopping_list_items_shopping_list_id ON shopping_list_items(shopping_list_id);
    CREATE INDEX  idx_shopping_list_items_product_id ON shopping_list_items(product_id);
    CREATE INDEX  idx_shopping_lists_purchased_count ON shopping_lists(purchased_count);
    """

    cursor.executescript(create_indices)

    # Tallenna muutokset ja sulje yhteys
    conn.commit()
    conn.close()

    if not db_exists:
        print(f"Tietokanta '{db_path}' luotiin onnistuneesti.")
    else:
        print(f"Tietokanta '{db_path}' päivitettiin onnistuneesti.")


if __name__ == "__main__":
    # Määritä tietokannan polku
    database = "cook_and_cart.db"
    database_path = os.path.join(os.getcwd(), "utils", database)

    # Luo tietokanta ja tarvittavat taulut
    create_database(database_path)
