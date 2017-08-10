import sqlalchemy


oracle_db = sqlalchemy.create_engine('oracle://username:password@database')
connection = oracle_db.connect()
result = connection.execute("SELECT test_column FROM test_table")
for row in result:
    print(row)