import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("SELECT id, name, url, store_fname FROM ir_attachment;")
rows = cur.fetchall()
print("ATTACHMENTS IN DB:", rows)

cur.close()
conn.close()
