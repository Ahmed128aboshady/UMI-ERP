import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='postgres', password='admin', dbname='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_roles WHERE rolname='odoo';")
    if not cur.fetchone():
        cur.execute("CREATE ROLE odoo WITH LOGIN PASSWORD 'odoo' CREATEDB SUPERUSER;")
        print("CREATED ROLE 'odoo' SUCCESSFULLY!")
    else:
        print("ROLE 'odoo' ALREADY EXISTS.")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Error creating role: {e}")
