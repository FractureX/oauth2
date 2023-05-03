import psycopg2
import json
import os

class Database():
    connection_data = json.load(open('config_data.json', 'r')) ["PGSQL"]
    connection = None

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
            print(e)
            self.connection = None
    
    def disconnect(self):
        if (self.connection is not None):
            self.connection.close()
        self.connection = None