import psycopg2
import json
from fastapi import HTTPException, status

class Database():

    def __init__(self, hola):
        self.hola = hola

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host = self.connection_data["HOST"],
                port = self.connection_data["PORT"],
                database = self.connection_data["DATABASE"],
                user = self.connection_data["USERNAME"],
                password = self.connection_data["PASSWORD"]
            )
        except psycopg2.Error as e:
            self.connection = None
            return e
    
    def disconnect(self):
        if (self.connection is not None):
            self.connection.close()
        self.connection = None
    
    def select(self, query, data: list):
        response = self.connect()
        if (response is not None):
            return HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST, 
                detail = response
            )
        cursor = self.connection.cursor()
        print(cursor.description)
        cursor.execute(query = query, vars = data)
        data = cursor.fetchall()
        