import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("SELECT id, name, symbol, active FROM res_currency WHERE name IN ('AED', 'EGP', 'USD', 'EUR');")
rows = cur.fetchall()
print("CURRENCIES IN DB:", rows)

cur.close()
conn.close()
