import cx_Oracle
#import pyodbc
import pymysql


class UseDatabaseOracle:
    def __init__(self, config: str) -> None:
        """Initialize configuration attribute from config.file"""
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """Initialize connection to DB and cursor"""
        self.conn = cx_Oracle.connect(self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Commit DB changes and close cursor/connection"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class UseDatabaseMSSQL:
    def __init__(self, config: str) -> None:
        """Initialize configuration attribute from config.file"""
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """Initialize connection to DB and cursor"""
        self.conn = pymysql.connect(self.configuration)
        #self.conn = pyodbc.connect(self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Commit DB changes and close cursor/connection"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
