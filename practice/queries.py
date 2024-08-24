from contextlib import contextmanager

import mysql.connector
from flask import json


class SQLQueries:

    def __init__(self, app):
        self.app = app

    @contextmanager
    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.app.config['MYSQL_HOST'],
                user=self.app.config['MYSQL_USER'],
                password=self.app.config['MYSQL_PASSWORD'],
                database=self.app.config['MYSQL_DB']
            )
            print(f"connected ===>>>>> {connection.is_connected()}")
            if connection.is_connected():
               return connection
            else: return None
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    @contextmanager
    def get_cursor(self):
        with self.get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                return cursor
            finally:
                cursor.close()
                print("Cursor closed.")

    def create_table(self):
        connection = self.get_db_connection()
        if connection is not None:
            with connection as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS prediction (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(255) UNIQUE NOT NULL,
                        modes JSON NOT NULL,
                        deflection JSON NOT NULL,
                        frequency JSON NOT NULL 
                    )
                ''')
                # cursor.connection.commit()  # Commit after executing the query
            return "Table created successfully"

    def add_to_table(self, user_id, modes, deflection, frequency):
        with self.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO prediction (user_id, modes, deflection, frequency)
                VALUES (%s, %s, %s, %s)
            ''', (
                user_id,
                json.dumps(modes),
                json.dumps(deflection),
                json.dumps(frequency)))
            # cursor.connection.commit()  # Commit after executing the query
        return "Data inserted successfully."

    def fetch_from_table(self, user_id):
        with self.get_cursor() as cursor:
            cursor.execute('''
                SELECT * FROM prediction
            ''')
            results = cursor.fetchall()
            print(f"The data fetched are ====>>> {results}")
        return results
