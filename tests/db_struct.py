import os
import sqlite3

def print_db_structure(db_path):
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")
    else:
        for (table_name,) in tables:
            print(f"Table: {table_name}")
            # Get column info for the table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
            for cid, name, col_type, notnull, dflt_value, pk in columns:
                print(f"  Column: {name} | Type: {col_type} | NotNull: {bool(notnull)} | Default: {dflt_value} | PrimaryKey: {bool(pk)}")
            print()  # newline between tables

    cursor.close()
    conn.close()

def main():
    # Hard-coded path to the database file
    db_path = os.path.join(os.getcwd(), "utils", "cook_and_cart.db")
    print(f"Database structure for: {db_path}\n")
    print_db_structure(db_path)

if __name__ == '__main__':
    main()