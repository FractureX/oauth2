import psycopg2
from psycopg2.extras import RealDictCursor
import json
from fastapi import HTTPException, status

class Database:
    
    connection = None
    connection_data = json.load(open('config_data.json', 'r')) ["PGSQL"]

    def raise_exception(response):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = response
        )

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host = self.connection_data["HOST"],
                port = self.connection_data["PORT"],
                database = self.connection_data["DATABASE"],
                user = self.connection_data["USER"],
                password = self.connection_data["PASSWORD"],
                cursor_factory = RealDictCursor
            )
        except psycopg2.Error as e:
            self.raise_exception(e.pgerror)
    
    def disconnect(self):
        if (self.connection is not None):
            self.connection.close()
        self.connection = None
    
    def select(self, query: str, data: list = None) -> dict | None:
        try:
            response = self.connect()
            if (response is not None):
                self.raise_exception(response)
            cursor = self.connection.cursor()
            cursor.execute(query = query, vars = data)
            data = [dict(row) for row in cursor.fetchall()]
            return data
        except psycopg2.Error as e:
            self.raise_exception(e.pgerror)
            return None
        finally:
            self.disconnect()
            
