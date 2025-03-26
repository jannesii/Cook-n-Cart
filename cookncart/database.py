# database.py

import sqlite3
from typing import List, Dict
import os


class DatabaseManager:
    _instance = None

    def __init__(self, db_path="cookncart/utils/cook_and_cart.db"):
        if DatabaseManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            DatabaseManager._instance = self

    @staticmethod
    def get_instance():
        if DatabaseManager._instance is None:
            DatabaseManager()
        return DatabaseManager._instance

    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetchall(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetchone(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def executemany(self, query: str, params: List[tuple]):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params)
            conn.commit()
        return cursor


