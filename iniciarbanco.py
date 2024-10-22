import mysql.connector

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': ''
}


#estabelecendo conexão
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
print("Conexão estabelecida com sucesso.")

SCHEMA = "db/schema.sql"

# Declara o SQL para o banco
with open(SCHEMA, 'r') as f:
    sql_script = f.read()

conn.commit()
conn.close()
cursor.close()
print("Script executado com sucesso.")    
