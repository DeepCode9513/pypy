from venv import create
import psycopg2
import psycopg2.extras

hostname = "nocdbserver.southafricanorth.cloudapp.azure.com"
port_id = "5432"
database = "integraDB"
username = "postgres"
pwd = "war49jik#"


conn = None
cur = None
try:
    conn = psycopg2.connect(
        host=hostname, dbname=database, password=pwd, port=port_id, user=username
    )
    conn.autocommit = True
    cur = conn.cursor() 

    query = """CREATE TABLE respublica( 
        id SERIAL PRIMARY KEY, 
        is_time TIMESTAMP, 
        alert_site VARCHAR,
        ip_address VARCHAR,
        link_state VARCHAR      
    )
"""

    cur.execute(query)
    #for record in cur.fetchall():
     #   print(record["clientname"], record["status"])

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


